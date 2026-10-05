"""Independent WP11 certificate replay. Imports no producer or mass_core code.
Default mode checks only explicitly supplied certificates, never a corpus search.
"""
import argparse, hashlib, itertools, json
from pathlib import Path

FEATURES = ['q','lin','L','Lall','links','shortLinks','repMass','hubToggles']
PAIRS = tuple(itertools.combinations(range(4), 2))

def need(test, message):
    if not test: raise ValueError(message)

def canonical(c):
    names = {}; out = []
    for x in c:
        if x not in names: names[x] = len(names)
        out.append(names[x])
    return tuple(out)

def graph_check(g):
    rot = g['rotation']; n = len(rot)
    need(n == g['order'] and n > 0, 'graph order')
    for u, row in enumerate(rot):
        need(len(row) == len(set(row)) and len(row) >= 5, 'simple/minimum-degree graph')
        for v in row:
            need(type(v) is int and 0 <= v < n and v != u and u in rot[v], 'symmetric edges')
    if g['ascii'] is not None:
        raw = g['ascii']; order, text = raw.split(' ', 1)
        parsed = [[ord(x)-ord('a') for x in row] for row in text.split(',')]
        need(int(order) == n and parsed == rot, 'ASCII/rotation disagreement')
        need(hashlib.sha256(raw.encode()).hexdigest() == g['ascii_sha256'], 'ASCII hash')
    pending = {(u,v) for u in range(n) for v in rot[u]}; faces = 0
    while pending:
        start = min(pending); cur = start; cycle = []
        while cur not in cycle:
            need(cur in pending, 'face orbits overlap')
            cycle.append(cur); pending.remove(cur)
            u,v = cur; row = rot[v]; cur = (v, row[(row.index(u)+1)%len(row)])
        need(cur == start and len(cycle) == 3, 'nontriangular face')
        faces += 1
    reached = {0}; stack = [0]
    while stack:
        for v in rot[stack.pop()]:
            if v not in reached: reached.add(v); stack.append(v)
    need(len(reached) == n, 'disconnected graph')
    edges = sum(map(len,rot))//2
    need(n-edges+faces == 2, 'Euler characteristic')
    return rot, [u for u in range(n) if len(rot[u]) == 5]

def setup(rot, r, rec):
    need(r in range(len(rot)) and len(rot[r]) == 5, 'ineligible root')
    vertices = [v for v in range(len(rot)) if v != r]
    need(rec['vertex_order'] == vertices and rec['boundary_cyclic_order'] == rot[r], 'vertex/boundary coordinates')
    index = {v:i for i,v in enumerate(vertices)}
    adj = tuple(frozenset(index[w] for w in rot[v] if w != r) for v in vertices)
    boundary = frozenset(index[v] for v in rot[r])
    return adj, boundary, vertices

def proper(c, adj):
    return len(c) == len(adj) and all(type(x) is int and 0 <= x < 4 for x in c) and all(c[u] != c[v] for u,row in enumerate(adj) for v in row)

def enumerate_states(adj):
    # Restricted-growth names enumerate precisely one representative per colour orbit.
    answer = set(); c = [-1]*len(adj)
    def visit(i, highest):
        if i == len(adj): answer.add(tuple(c)); return
        forbidden = {c[j] for j in adj[i] if j < i}
        for x in range(min(3,highest+1)+1):
            if x not in forbidden:
                c[i] = x; visit(i+1,max(highest,x))
        c[i] = -1
    visit(0,-1)
    return answer

def parts(c, adj):
    result = []
    for a,b in PAIRS:
        unseen = {u for u,x in enumerate(c) if x == a or x == b}
        while unseen:
            seed = min(unseen); unseen.remove(seed); reached = {seed}; stack = [seed]
            while stack:
                for v in adj[stack.pop()]:
                    if v in unseen: unseen.remove(v); reached.add(v); stack.append(v)
            result.append(((a,b),frozenset(reached)))
    return result

def features(c, adj, B):
    ps = parts(c,adj); boundary_colours = [c[v] for v in B]
    p = max(0,len(set(boundary_colours))-3)
    f = {name:0 for name in FEATURES}
    f['hubToggles'] = sum(len(K)==2 and bool(K-B) for _,K in ps)
    if p:
        rho, = [x for x in set(boundary_colours) if boundary_colours.count(x)==2]
        for pair,K in ps:
            exterior = len(K-B); hits = K&B
            if hits:
                f['q'] += exterior*exterior; f['lin'] += exterior
                if rho in pair: f['repMass'] += exterior*exterior
            if len(hits) >= 2:
                f['links'] += 1; f['shortLinks'] += not exterior
                f['Lall'] += len(hits)
                f['L'] += sum(boundary_colours.count(c[v])==1 for v in hits)
    n = len(adj)+1
    bounds = [6*n*n,6*n,9,15,12,12,6*n*n,3*n]
    need(all(0<=f[k]<=b for k,b in zip(FEATURES,bounds)), 'feature bound')
    return p,f

def score(c, adj, B, weights):
    p,f = features(c,adj,B)
    return (p,sum(w*f[k] for w,k in zip(weights,FEATURES)))

def exchange(c,pair,K):
    a,b = pair
    return tuple(b if x==a and u in K else a if x==b and u in K else x for u,x in enumerate(c))

def step(c, move, adj, vertices):
    pair = tuple(move['pair']); labels = move['component']
    need(len(pair)==2 and all(type(x) is int for x in pair) and pair in PAIRS, 'colour pair')
    need(labels == sorted(set(labels)), 'component label duplicates/order')
    need(all(v in vertices for v in labels), 'component vertex outside deletion')
    K = frozenset(vertices.index(v) for v in labels)
    need((pair,K) in parts(c,adj), 'swap is not an entire active component')
    out = exchange(c,pair,K)
    need(proper(out,adj), 'swap lost properness')
    return out

def macro(c, data, adj, vertices):
    c1 = step(c,data['move1'],adj,vertices)
    if data['move2'] is None:
        need(data['intermediate'] is None, 'single-move intermediate')
        end = c1
    else:
        need(tuple(data['intermediate']) == c1, 'intermediate renaming/error')
        end = step(c1,data['move2'],adj,vertices)
    need(tuple(data['endpoint']) == end, 'incorrect raw endpoint')
    if 'endpoint_canonical' in data:
        need(tuple(data['endpoint_canonical']) == canonical(end), 'incorrect canonical endpoint')
    return end

def full_endpoints(c,adj):
    ends = {c}
    for pair,K in parts(c,adj):
        c1 = exchange(c,pair,K); ends.add(c1)
        for pair2,K2 in parts(c1,adj): ends.add(exchange(c1,pair2,K2))
    return ends

def check_stuck(rec,rot,w):
    adj,B,V = setup(rot,rec['root'],rec); st = rec['stuck']; c = tuple(st['coloring'])
    need(proper(c,adj) and canonical(c)==c, 'invalid stuck start')
    p,f = features(c,adj,B); rank = score(c,adj,B,w)
    need(p==1 and st['features']==f and tuple(st['rank'])==rank, 'stuck features/rank')
    supplied = {c}
    for ep in st['endpoints']:
        end = macro(c,ep,adj,V); endrank = score(end,adj,B,w)
        need(tuple(ep['endpoint_rank'])==endrank, 'endpoint rank')
        need(not endrank < rank, 'claimed stuck state actually descends')
        supplied.add(end)
    actual = full_endpoints(c,adj)
    need(supplied==actual, 'incomplete macro endpoint set')
    need(all(not score(end,adj,B,w)<rank for end in actual), 'independent decrease found')
    return {'root':rec['root'],'macro_endpoints':len(actual)}

def check(cert,producer_dir=None):
    need(cert['schema']=='wp11-cert-v1' and cert['macro_bound']==2, 'schema/macro bound')
    need(cert['features']==FEATURES, 'feature registry')
    w = cert['weights']; need(len(w)==8 and all(type(x) is int and 0<=x<=3 for x in w), 'weight types/range')
    support = sum(x>0 for x in w)
    need(support>0 and (all(x in (0,1) for x in w) or support==2), 'weight outside tier 1')
    if producer_dir is not None:
        for filename,digest in cert['producer'].items():
            need(filename in ('wp11_cert.py','mass_core.py'), 'unexpected producer file')
            need(hashlib.sha256((producer_dir/filename).read_bytes()).hexdigest()==digest, 'producer hash')
        need(set(cert['producer'])=={'wp11_cert.py','mass_core.py'}, 'missing producer hash')
    rot,roots = graph_check(cert['graph'])
    need(cert['degree_five_roots']==roots, 'incomplete degree-five root set')
    kind = cert['kind']
    if kind=='pass':
        adj,B,V = setup(rot,cert['root'],cert)
        allstates = enumerate_states(adj)
        supplied = [tuple(s['coloring']) for s in cert['states']]
        need(len(supplied)==len(set(supplied)), 'duplicate state')
        need(set(supplied)==allstates and cert['state_count']==len(allstates), 'incomplete colouring state set')
        witnesses = 0
        for rec,c in zip(cert['states'],supplied):
            need(proper(c,adj) and canonical(c)==c, 'invalid pass start')
            p,f = features(c,adj,B); rank = score(c,adj,B,w)
            need(rec['p']==p and rec['features']==f and tuple(rec['rank'])==rank, 'state features/rank')
            if p:
                ep = rec['witness']; need(ep is not None, 'missing descent witness')
                end = macro(c,ep,adj,V); endrank = score(end,adj,B,w)
                need(ep['endpoint_features']==features(end,adj,B)[1] and tuple(ep['endpoint_rank'])==endrank, 'witness features/rank')
                need(endrank<rank, 'witness does not descend'); witnesses += 1
        return {'kind':kind,'root':cert['root'],'independently_enumerated_states':len(allstates),'descent_witnesses':witnesses}
    if kind=='all_roots_fail_witness':
        return {'kind':kind,'checked':[check_stuck(cert['failing_root'],rot,w)]}
    if kind=='existential_fail_witness':
        need(sorted(r['root'] for r in cert['roots'])==roots, 'missing/duplicate failing root')
        return {'kind':kind,'checked':[check_stuck(rec,rot,w) for rec in cert['roots']]}
    raise ValueError('unknown certificate kind')

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('certificates',nargs='+',type=Path)
    ap.add_argument('--producer-dir',type=Path); ap.add_argument('--output',type=Path)
    args = ap.parse_args(); results = []
    for p in args.certificates:
        result = check(json.loads(p.read_text()),args.producer_dir)
        result.update(file=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        results.append(result); print(json.dumps(result),flush=True)
    if args.output:
        args.output.write_text(json.dumps({'scope':'named schema fixtures only; no WP11 discovery', 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':results},indent=2)+'\n')
if __name__=='__main__': main()
