import json, sys, glob, os, math, collections as C
import numpy as np
sys.path.insert(0, 'code')
from parts import parse
from mir import mirror
T = 2
G = json.load(open('db/rules_graph.json'))
N = G['nodes']                      # 604 parts of the 588 set (incl. 71 RSST drules)
FULL = (5, 9)
def rng_txt(lo, hi):
    if (lo, hi) == FULL: return '*'
    if lo == hi: return '=9+' if lo == 9 else f'={lo}'
    if hi == 9: return f'>={lo}'
    if lo == 5: return f'<={hi}'
    return f'in{lo}..{hi}'
def word(lo, hi):
    if (lo, hi) == FULL: return 'any degree'
    if lo == hi: return '9 or more' if lo == 9 else str(lo)
    if hi == 9: return f'{lo} or more'
    if lo == 5: return f'at most {hi}'
    return f'{lo} to {hi}'
rules = []
for n in N:
    r = dict(n); r['lang'] = 'part'; r['src'] = 'rsst' if n['t'] == 'RSST' else 'ext588'; rules.append(r)
# ---- N2 parts (fullstack_t0 parts79: amount at charge 10(6-d) -> x6 /60)
p79 = json.load(open('data/parts79.json'))['parts']
import importlib
for p in p79:
    if not p['tag'].startswith('N2'): continue
    sl = [[s[0][0], s[0][1], s[1][0], s[1][1], [list(f) for f in s[2]]] for s in p['subs']]
    h = p['hub']; w = 6 * p['amount']
    cons = []
    def lab(j):
        o = (j - T) % h
        if o > h // 2: o -= h
        return 'T' if o == 0 else (f'R{o}' if o > 0 else f'L{-o}')
    for j, s in enumerate(sl):
        if (s[0], s[1]) != FULL: cons.append(lab(j) + rng_txt(s[0], s[1]))
        if (s[2], s[3]) != FULL: cons.append(f'h({lab((j-1)%h)},{lab(j)})' + rng_txt(s[2], s[3]))
        for k, f in enumerate(s[4]):
            if tuple(f) != FULL: cons.append(f'f{k+1}({lab(j)})' + rng_txt(*f))
    rules.append(dict(id=len(rules), tag=p['tag'], t='N2', hub=h, w=w, m=None, s=-1, fam=-1, fac=0, np=len(cons),
                      c=f'H{h} +{w}/60 -> T | ' + ' '.join(cons),
                      e=f'A degree-{h} vertex sends {w}/60 of charge to its target neighbour T (narrow part added by the outside team in place of RSST configuration 128.1324802; {len(cons)} conditions).',
                      sl=sl, lang='part', src='n2'))
# ---- Inoue et al. 2026 graph rules
RD = 'gcds/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/pubrules/data/nl2026/R'
def layout(n, edges, fixed=None, seed=0):
    rng = np.random.default_rng(seed); P = rng.normal(size=(n, 2))
    if fixed:
        for k, v in fixed.items(): P[k] = v
    A = np.zeros((n, n))
    for a, b in edges: A[a, b] = A[b, a] = 1
    for it in range(600):
        D = P[:, None] - P[None]; d = np.sqrt((D ** 2).sum(-1)) + 1e-9
        F = (D / d[..., None] ** 3 * 0.15).sum(1) - (A[..., None] * D * (d[..., None] - 1)).sum(1) * 0.1
        if fixed:
            for k in fixed: F[k] = 0
        P += np.clip(F, -0.2, 0.2)
    P -= P.mean(0); s = np.abs(P).max() or 1
    return (P / s).round(4).tolist()
g26 = []
for f in sorted(glob.glob(RD + '/*.rule')):
    L = [l.split() for l in open(f) if l.strip()]
    n, s, d, a = map(int, L[0])
    vs = []; E = set()
    for row in L[1:]:
        vid, lo, hi = int(row[0]), int(row[1]), int(row[2]); nb = [int(x) for x in row[3:]]
        arc = nb and nb[-1] == -1
        nb = [x for x in nb if x != -1]
        vs.append(dict(lo=lo, hi=hi if hi else 99, nb=nb, arc=arc))
        for x in nb: E.add((min(vid, x) - 1, max(vid, x) - 1))
    E = sorted(E)
    pos = layout(n, E, fixed={s - 1: (-0.7, 0.0), d - 1: (0.7, 0.0)} if n > 1 else None)
    tag = os.path.basename(f)[:-5]
    adjsd = (min(s, d) - 1, max(s, d) - 1) in E
    def dw(v):
        lo, hi = v['lo'], v['hi']
        hi9 = min(hi, 9) if hi < 99 else 9
        return word(min(lo, 9), hi9 if hi < 99 else 9) if not (hi >= 99 and lo <= 5) else 'any degree'
    others = C.Counter()
    for i, v in enumerate(vs):
        if i in (s - 1, d - 1): continue
        others[dw(v)] += 1
    w = 6 * a
    e = (f"A vertex of degree {dw(vs[s-1])} sends {w}/60 of charge to {'an adjacent' if adjsd else 'a nearby (not adjacent)'} vertex of degree {dw(vs[d-1])}, "
         f"when the picture around them has {n-2} more vertices: " + ', '.join(f'{k}× degree {v}' for v, k in others.most_common()) + '.') if n > 2 else \
        f"A vertex of degree {dw(vs[s-1])} sends {w}/60 of charge to an adjacent vertex of degree {dw(vs[d-1])}."
    def rt(v):
        lo, hi = v['lo'], (v['hi'] if v['hi'] < 99 else 9)
        return rng_txt(min(lo, 9), min(hi, 9))
    c = f"S{rt(vs[s-1])} -> D{rt(vs[d-1])} {w}/60 | " + ' '.join(f"v{i+1}{rt(v)}" for i, v in enumerate(vs) if i not in (s - 1, d - 1)) + f" | {len(E)} edges"
    g26.append(dict(id=len(rules), tag=tag, t='2026', w=w, lang='graph', src='nl26', nv=n, sv=s - 1, dv=d - 1,
                    vr=[[min(v['lo'], 9), min(v['hi'], 9) if v['hi'] < 99 else 9] for v in vs], ge=E, pos=pos, adj=adjsd,
                    np=sum(1 for v in vs if not (v['lo'] <= 5 and v['hi'] >= 99)), c=c, e=e, m=None, s=-1, fam=-1, fac=0))
    rules.append(g26[-1])
print('rules', len(rules), C.Counter(r['src'] for r in rules))
# ---- distances
def roles(sl, h):
    out = {}
    for j, s in enumerate(sl):
        o = (j - T) % h
        if o > h // 2: o -= h
        out[('s', o)] = (s[0], s[1]); out[('h', o)] = (s[2], s[3])
        for k, f in enumerate(s[4]): out[('f', o, k)] = tuple(f)
    return out
def part_roles(r):
    p = dict(hub=r['hub'], slots=tuple((s[0], s[1], s[2], s[3], tuple(tuple(f) for f in s[4])) for s in r['sl']))
    a = roles(p['slots'], r['hub']); b = roles(mirror(p, T, 1, 'with_spoke'), r['hub'])
    return [a, b]
def graph_roles(r):
    # BFS order from source then destination, neighbours in listed order
    n = r['nv']; adj = C.defaultdict(list)
    for a, b in r['ge']: adj[a].append(b); adj[b].append(a)
    order = [r['sv'], r['dv']]; q = list(order)
    while q:
        v = q.pop(0)
        for x in sorted(adj[v]):
            if x not in order: order.append(x); q.append(x)
    order += [i for i in range(n) if i not in order]
    return [{('v', k): tuple(r['vr'][v]) for k, v in enumerate(order)}]
def rname(k):
    if k[0] == 'v': return f'vertex {k[1]+1}'
    o = k[1]; s = 'T' if o == 0 else (f'R{o}' if o > 0 else f'L{-o}')
    return {'s': f'spoke {s}', 'h': f'hat at {s}'}.get(k[0]) or f'fan {k[2]+1} at {s}'
def vtxt(v):
    if v is None: return 'absent'
    return rng_txt(v[0], v[1]).lstrip('=') or 'any'
def diff(A, B):
    best = None
    for a in A:
        for b in B:
            ch = [(k, a.get(k), b.get(k)) for k in sorted(set(a) | set(b), key=str) if a.get(k) != b.get(k)]
            if best is None or len(ch) < len(best): best = ch
    return [f'{rname(k)}: {vtxt(x)} to {vtxt(y)}' for k, x, y in best]
def dist(A, B):
    best = 99
    for a in A:
        for b in B:
            ks = set(a) | set(b); best = min(best, sum(1 for k in ks if a.get(k) != b.get(k)))
    return best
RO = {r['id']: (part_roles(r) if r['lang'] == 'part' else graph_roles(r)) for r in rules}
# mirror pairs
def pairs_of(ids):
    used = set(); out = []
    byid = {i: rules[i] for i in ids}
    for i in ids:
        if i in used: continue
        r = rules[i]; mate = None
        if r['lang'] == 'part':
            if r['src'] == 'n2':
                cand = [j for j in ids if j not in used and j != i and rules[j]['src'] == 'n2' and rules[j]['tag'].rstrip('m') == r['tag'].rstrip('m')]
            else:
                cand = [r['m']] if r['m'] is not None and r['m'] != i and r['m'] in byid and r['m'] not in used else []
        else:
            base = r['tag'].rsplit('_', 1)[0] if '_' in r['tag'] else None
            cand = [j for j in ids if j not in used and j != i and base and rules[j]['tag'].startswith(base + '_')]
        g = [i] + cand[:1]; used |= set(g); out.append(g)
    return out
TREES = []
def seq_for(ids):
    pr = pairs_of(ids); n = len(pr)
    D = np.zeros((n, n))
    for a in range(n):
        for b in range(a + 1, n):
            la, lb = rules[pr[a][0]]['lang'], rules[pr[b][0]]['lang']
            D[a, b] = D[b, a] = dist(RO[pr[a][0]], RO[pr[b][0]]) if la == lb else 99
    # average-linkage leaf order
    memb = {i: [i] for i in range(n)}; dd = {i: {j: D[i, j] for j in range(n) if j != i} for i in range(n)}
    active = set(range(n)); nxt = n
    while len(active) > 1:
        v, i, j = min((dd[i][j], i, j) for i in active for j in dd[i] if j in active and i < j)
        memb[nxt] = memb[i] + memb[j]; dd[nxt] = {}
        for k in active - {i, j}:
            x = (dd[i][k] * len(memb[i]) + dd[j][k] * len(memb[j])) / (len(memb[i]) + len(memb[j])); dd[nxt][k] = x; dd[k][nxt] = x
        active -= {i, j}; active.add(nxt); nxt += 1
    order = memb[list(active)[0]] if n else []
    fams = {}
    for k in (1, 2, 3, 4):
        par = list(range(n))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for a in range(n):
            for b in range(a + 1, n):
                if D[a, b] <= k: par[f(a)] = f(b)
        fams[k] = [f(x) for x in range(n)]
    # minimum spanning tree (Prim)
    posof = {x: i for i, x in enumerate(order)}
    tree = []
    if n > 1:
        intree = [False] * n; intree[order[0]] = True
        bd = D[order[0]].copy(); bf = [order[0]] * n
        for _ in range(n - 1):
            y = min((j for j in range(n) if not intree[j]), key=lambda j: (bd[j], posof[j]))
            x = bf[y]; intree[y] = True
            tree.append([posof[x], posof[y], int(D[x, y]), diff(RO[pr[x][0]], RO[pr[y][0]]) if D[x, y] < 99 and D[x, y] <= 6 else []])
            for j in range(n):
                if not intree[j] and D[y, j] < bd[j]: bd[j] = D[y, j]; bf[j] = y
    TREES.append(tree)
    seq = []
    for pos, x in enumerate(order):
        prev = order[pos - 1] if pos else None
        nn = sorted(range(n), key=lambda y: D[x, y])[1:6]
        seq.append(dict(pair=pr[x], dprev=None if prev is None else int(D[x, prev]),
                        near=[[pr[y][0], int(D[x, y])] for y in nn], fam={k: int(fams[k][x]) for k in fams}))
    return seq
# ---- configs
cf633 = json.load(open('db/configs.json'))
def tutte(m, r, int_adj, ringn):
    pos = [[0.0, 0.0] for _ in range(m)]
    rp = [(math.cos(2 * math.pi * k / r - math.pi / 2), math.sin(2 * math.pi * k / r - math.pi / 2)) for k in range(r)]
    for _ in range(300):
        for u in range(m):
            xs = [pos[v] for v in int_adj[u]] + [rp[k] for k in ringn[u]]
            pos[u] = [sum(x for x, _ in xs) / len(xs), sum(y for _, y in xs) / len(xs)]
    return [[round(a, 4), round(b, 4)] for a, b in pos]
configs = []
for c in cf633:
    c = dict(c); c['set'] = 'rsst'; configs.append(c)
name2 = {c['n']: c['id'] for c in configs}
reg = json.load(open('data/verified_registry.json'))['configs']
reg_ids = []
for c in reg:
    if c['source'] in ('RSST_582', 'RSST_2o126_LEAN') and c['name'] in name2:
        reg_ids.append(name2[c['name']]); continue
    m, r = c['m'], c['ring']
    ringn = [[t[1] for t in c['rot'][u] if t[0] == 'R'] for u in range(m)]
    ie = sorted({tuple(sorted((u, v))) for u in range(m) for v in c['int_adj'][u]})
    re_ = sorted({(u, k) for u in range(m) for k in ringn[u]})
    o = dict(id=len(configs), n=c['name'], k=c['kind'], X=c['X'] if c['X'] != '-' else '', r=r, m=m, deg=c['deg'], a=1,
             ev=c.get('evidence', ''), fam=0, fs=0, nb=[], ie=ie, re=re_, pi=tutte(m, r, c['int_adj'], ringn), cov=None, set='854')
    configs.append(o); reg_ids.append(o['id'])
nl_ids = []
for f in sorted(glob.glob('ext2/rc/D/*.conf')):
    L = [l.split() for l in open(f) if l.strip()]
    nv, r = map(int, L[0]); m = nv - r
    deg = []; int_adj = [[] for _ in range(m)]; ringn = [[] for _ in range(m)]
    for row in L[1:]:
        vid, dg = int(row[0]), int(row[1]); nb = [int(x) for x in row[2:]]
        u = vid - r - 1; deg.append(dg)
        for x in nb:
            if x > r: int_adj[u].append(x - r - 1)
            else: ringn[u].append(x - 1)
    ie = sorted({tuple(sorted((u, v))) for u in range(m) for v in int_adj[u]})
    re_ = sorted({(u, k) for u in range(m) for k in ringn[u]})
    o = dict(id=len(configs), n=os.path.basename(f)[:-5], k='D', X='', r=r, m=m, deg=deg, a=1, ev='published D-reducible; all 8,200 D on our two engines (20 Oct)',
             fam=0, fs=0, nb=[], ie=ie, re=re_, pi=tutte(m, r, int_adj, ringn), cov=None, set='nl26')
    configs.append(o); nl_ids.append(o['id'])
print('configs', len(configs), len(reg_ids), len(nl_ids))
# ---- proofs
ids = lambda pred: [r['id'] for r in rules if pred(r)]
rsst_r = ids(lambda r: r['src'] == 'rsst'); all588 = ids(lambda r: r['src'] in ('rsst', 'ext588')); n2 = ids(lambda r: r['src'] == 'n2'); nl = ids(lambda r: r['src'] == 'nl26')
flow = json.load(open('db/flow.json'))['avg']
proofs = [
 dict(id='rsst', label='RSST 1996 / Coq 2005', sub="Robertson, Sanders, Seymour and Thomas's 32 rules (71 parts with copies and mirrors) and 633 configurations. Gonthier's Coq proof (2005) formalises exactly this set, so it is the same rules and configurations.",
      rules=rsst_r, configs=list(range(633)), flow=[r for r in flow if r[2] == 'RSST']),
 dict(id='nl26', label='Inoue et al. 2026', sub="43 rules (84 with mirrors), written as general pattern graphs with a source and a destination, and 8,200 D-reducible configurations (plus two one-vertex ones not drawn). Charge 10(6-d) rescaled to 1/60.",
      rules=nl, configs=nl_ids, flow=None),
 dict(id='ext588', label='Outside team 588', sub="The outside team's compressed proof: RSST's 71 parts plus 533 added parts (493 push, 40 tunnel), and 588 of RSST's 633 configurations. Engine result, not yet independently verified end to end.",
      rules=all588, configs=list(range(633)), used=[c['id'] for c in cf633 if c['a']], flow=flow),
 dict(id='ext854', label='Outside team 854', sub="The outside team's full-world proof: RSST's 71 parts plus 8 narrow N2 parts, and 878 verified configurations (854 used per its README): 582 RSST configurations, the extra RSST configuration 2.126, 280 from the 2026 set + 15 windows.",
      rules=rsst_r + n2, configs=reg_ids, flow=[r for r in flow if r[2] == 'RSST'], flownote='N2 parts not included in the flow numbers'),
]
for p in proofs:
    p['seq'] = seq_for(p['rules']); p['tree'] = TREES[-1]; print(C.Counter(e[2] for e in p['tree'])); print(p['id'], len(p['rules']), len(p['seq']), len(p['configs']))
json.dump(dict(rules=rules, configs=configs, proofs=proofs, edges=G['edges'], factors=G['factors'], symbols=G['symbols']),
          open('db/atlas4.json', 'w'), separators=(',', ':'))
print(os.path.getsize('db/atlas4.json'))
