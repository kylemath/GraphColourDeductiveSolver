#!/usr/bin/env python3
"""ST-120 B5 M2: certificate exporter for RSSTCheckCore.checkDeg (route (c)).

Reuses RSST-1SHOT (job_RSST1SHOT/code/rcore.py 3d133146): the parts, the window, the fit rules (rcore.fit, re-run here
with every test kept separately, as the Lean symbolic evaluator keeps them), the configurations and the host graph.

For every link word of length d (itertools.product order, no symmetry reduction) it runs exactly the DFS that the
Lean checker replays (RSSTCheckCore.dfs): instances = fits moving u's charge as conjunctions of (code, range) tests +
OPEN flag; variables = the codes tested, in site order (s_i, then p_i.1..3); classes = {9 and every letter with 9's
truth pattern} and every other letter alone; ub = 10(6-d) + #in - #(out with no condition and not OPEN); kill
requirements from embeddings of the kill list into the host graph (codes with their needed letters). It writes one
line per link word: ORDER|k:e,e,..;k:e,.. listing only the embeddings the DFS used.

Codes: apex s_j -> 100+j, private p_i.(k+1) -> 200+3i+k. Window vertices: u 0, w_i 1+i, s_i 1+d+i, p_i.(k+1) 1+2d+3i+k.

usage: python3 -I export_cert.py D OUTFILE [--model 633|582|583|names:FILE] [--links N] [--dump-inst FILE] [--sample K SEED] [--parts FILE]
"""
import os, sys, time, itertools, json, collections, hashlib
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(H, '..', '..', '..'))
sys.path.insert(0, os.path.join(OUT, 'job_RSST1SHOT', 'code'))
import rcore as R

FULL = R.FULL
ROTCACHE = os.environ.get('B5_ROTCACHE', '1') == '1'

def vcode(d, h):
    if h == 'u': return 0
    if h[0] == 'w': return 1 + h[1]
    if h[0] == 's': return 1 + d + h[1]
    return 1 + 2 * d + 3 * h[1] + (h[2] - 1)

def var_code(nm):
    if nm[0] == 's': return 100 + int(nm[1:])
    a, b = nm[1:].split('.'); return 200 + 3 * int(a) + int(b) - 1

def parse_rng(tok):
    if tok == '*': return FULL
    if tok.startswith('='): return (int(tok[1:]), int(tok[1:]))
    if tok.startswith('>='): return (int(tok[2:]), 9)
    if tok.startswith('<='): return (5, int(tok[2:]))
    if tok.startswith('in'): a, b = tok[2:].split('..'); return (int(a), int(b))
    raise ValueError(tok)

def load_parts_file(fn):
    """A part list in parts71.txt / B2 lean_parts.txt format: TAG<tab>N<tab>SPOKE[HAT|FAN,FAN]  ... (rcore.parts_text).
    Every part moves 1 unit to its third spoke (B4's eval_sound hypothesis)."""
    out = []
    for line in open(fn):
        if not line.strip() or line.startswith('#'): continue
        tag, n, body = line.rstrip('\n').split('\t')
        subs = []
        for tok in body.split('  '):
            sp, rest = tok.split('[', 1); hat, fans = rest.rstrip(']').split('|')
            subs.append((parse_rng(sp), parse_rng(hat), tuple(parse_rng(f) for f in fans.split(',')) if fans else ()))
        assert len(subs) == int(n), line
        out.append((tag, subs))
    return out

class Fail(Exception): pass

def _test(W, v, r, conds, st):
    """rcore._test, but every test is kept (no intersection): (code, lo, hi)."""
    if r == FULL: return
    k = W.deg(v)
    if k[0] == 'dec':
        if not (r[0] <= k[1] <= r[1]): raise Fail
    elif k[0] == 'open':
        st['open'] = True
    else:
        conds.append((var_code(k[1]), r[0], r[1]))

def fit(W, h, part, a):
    """rcore.fit with raw tests."""
    S = W.rot[h]; n = len(part)
    if len(S) != n: return None
    conds = []; st = {'open': False}
    try:
        for j in range(n):
            sp, hat, fans = part[j]
            x, xp, xn = S[(a + j) % n], S[(a + j - 1) % n], S[(a + j + 1) % n]
            _test(W, x, sp, conds, st)
            if hat != FULL:
                _test(W, W.succ(x, xp), hat, conds, st)
            if any(f != FULL for f in fans):
                if x == 'u' or x[0] == 'w':
                    hv = W.succ(x, xp); hn = W.succ(xn, x)
                    Rr = W.rot[x]; t = (Rr.index(hv) + 1) % len(Rr); F = []
                    while Rr[t] != hn: F.append(Rr[t]); t = (t + 1) % len(Rr)
                    if len(F) != len(fans): raise Fail
                    for f, v in zip(fans, F): _test(W, v, f, conds, st)
                else:
                    st['open'] = True
    except Fail:
        return None
    return (tuple(conds), st['open'])

def instances(W):
    d = W.d; ins, outs = [], []
    byn = collections.defaultdict(list)
    for tag, p in R.PARTS: byn[len(p)].append((tag, p))
    if 5 <= d <= 8:
        for tag, p in byn[d]:
            for a in range(d):
                r = fit(W, 'u', p, a)
                if r: outs.append(r)
    for i in range(d):
        L = W.link[i]
        if L > 8: continue
        for tag, p in byn[L]:
            r = fit(W, ('w', i), p, L - 2)
            if r: ins.append(r)
    return ins, outs

def embeddings(host, adj, p):
    """All injective induced degree-preserving maps of p's interior into the host graph (rcore.all_embeddings), keeping
    one embedding per minimal requirement. Returns list of (requirement frozenset of (host, letter) on variable hosts,
    embedding list host per interior index)."""
    order, deg, E = p['order'], p['deg'], p['E']; phi = {}; used = set(); found = {}
    U = sorted(deg)
    def rec(k):
        if k == len(order):
            req = frozenset((phi[x], deg[x]) for x in phi if len(host[phi[x]]) > 1)
            if req not in found: found[req] = [phi[x] for x in U]
            return
        x = order[k]; nb = [y for y in order[:k] if y in E[x]]
        for t in sorted(adj[phi[nb[0]]] if nb else host.keys(), key=repr):   # sorted: reproducible across runs
            if t in used or deg[x] not in host[t]: continue
            if any((y in E[x]) != (phi[y] in adj[t]) for y in order[:k]): continue
            phi[x] = t; used.add(t); rec(k + 1); del phi[x]; used.discard(t)
    rec(0)
    keep = []
    for rq in sorted(found, key=len):
        if not any(q <= rq for q, _ in keep): keep.append((rq, found[rq]))
    return keep

def kill_sel(model):
    """Indices (into the 633, rsst.txt order) of a kill list, in that order. '633' all; '582' proved (D2/C2cons);
    '583' proved + 2.126; 'names:FILE' the configurations named in FILE (RSST names like 2.126, one per line).
    The Lean kill list must be the same selection in the same order (py/gen_killset.py)."""
    if model == '633': return list(range(633))
    if model == '582': return [i for i, p in enumerate(R.CONFIGS) if p['proved']]
    if model == '583': return [i for i, p in enumerate(R.CONFIGS) if p['proved'] or p['name'] == '2.126']
    if model.startswith('names:'):
        nm = set(l.strip() for l in open(model[6:]) if l.strip() and not l.startswith('#'))
        return [i for i, p in enumerate(R.CONFIGS) if p['name'] in nm]
    raise SystemExit('unknown model ' + model)

KSEL = {}
def kpos(model):
    if model not in KSEL: KSEL[model] = {ci: k for k, ci in enumerate(kill_sel(model))}
    return KSEL[model]

def link_reqs(W, model, relevant):
    host, adj, var = R.window_hostgraph(W)
    hc = collections.Counter()
    for v, S in host.items():
        for x in S: hc[x] += 1
    out = []
    for ci, p in enumerate(R.CONFIGS):
        if ci not in kpos(model): continue
        if len(p['deg']) > len(host): continue
        if any(hc[x] < m for x, m in p['dm'].items()): continue
        for rq, emb in embeddings(host, adj, p):
            req = tuple(sorted((var_code(var[h]), L) for h, L in rq))
            if relevant is not None and any(c not in relevant for c, _ in req): continue
            out.append((req, ci, [vcode(W.d, h) for h in emb]))
    out.sort(key=lambda t: (len(t[0]), not R.CONFIGS[t[1]]['proved']))
    return out

REQ_CACHE = {}

def link_reqs_rot(d, link, model, relevant):
    """link_reqs through a cache over rotations: compute for the least rotation Lc (Lc[j] = link[(j+r)%d]) and
    move vertex codes / requirement codes by j -> j+r (the window is rotation-equivariant). The Lean checker
    re-verifies every embedding, so this is only a speed-up."""
    rots = [(tuple(link[(j + r) % d] for j in range(d)), r) for r in range(d)]
    Lc, r = min(rots)
    key = (Lc, model)
    if key not in REQ_CACHE:
        W = R.Window(d, list(Lc), None)
        REQ_CACHE[key] = link_reqs(W, model, None)
    def mv(v):           # window vertex code of Lc -> of link
        if v == 0: return 0
        if v <= d: return 1 + (v - 1 + r) % d
        if v <= 2 * d: return 1 + d + (v - d - 1 + r) % d
        q = v - 2 * d - 1; return 1 + 2 * d + 3 * ((q // 3 + r) % d) + q % 3
    def mc(c):           # code of Lc -> of link
        if c < 200: return 100 + (c - 100 + r) % d
        q = c - 200; return 200 + 3 * ((q // 3 + r) % d) + q % 3
    out = []
    for req, ci, emb in REQ_CACHE[key]:
        req2 = tuple(sorted((mc(c), L) for c, L in req))
        if any(c not in relevant for c, _ in req2): continue
        out.append((req2, ci, [mv(v) for v in emb]))
    return out

def site_key(c):
    return (c - 100, 0, 0) if c < 200 else ((c - 200) // 3, 1, (c - 200) % 3)

def tst(lo, hi, l): return lo <= l <= hi

def classes_of(v, insts):
    ts = [(lo, hi) for cs, o in insts for (c, lo, hi) in cs if c == v]
    pat = lambda x: tuple(tst(lo, hi, x) for lo, hi in ts)
    c9 = [x for x in (5, 6, 7, 8, 9) if pat(x) == pat(9)]
    return [c9] + [[x] for x in (5, 6, 7, 8) if pat(x) != pat(9)]

def simp1(v, S, inst):
    cs, o = inst
    if any(c == v and all(not tst(lo, hi, l) for l in S) for c, lo, hi in cs): return None
    return (tuple(t for t in cs if not (t[0] == v and all(tst(t[1], t[2], l) for l in S))), o)

def simpR1(v, S, R_):
    req, idx = R_
    if any(c == v and S != [l] for c, l in req): return None
    return (tuple(t for t in req if t[0] != v), idx)

class Budget(Exception): pass

def run_dfs(base, vs, ins, outs, reqs, used, stats, maxnodes):
    stats['nodes'] += 1
    if stats['nodes'] > maxnodes: raise Budget       # maxnodes is absolute: do_link sets it per link
    ub = base + len(ins) - sum(1 for cs, o in outs if not cs and not o)
    if ub <= 0: stats['ub_leaves'] += 1; return True
    empt = [ix for rq, ix in reqs if not rq]
    if empt:
        pick = next((ix for ix in empt if ix in used), empt[0]); used.add(pick); stats['kill_leaves'] += 1
        return True
    if not vs: return False
    (v, cls), rest = vs[0], vs[1:]
    for S in cls:
        i2 = [y for y in (simp1(v, S, x) for x in ins) if y is not None]
        o2 = [y for y in (simp1(v, S, x) for x in outs) if y is not None]
        r2 = [y for y in (simpR1(v, S, x) for x in reqs) if y is not None]
        if not run_dfs(base, rest, i2, o2, r2, used, stats, maxnodes): return False
    return True

def do_link(d, link, model, stats, maxnodes=10 ** 8):
    W = R.Window(d, list(link), None)
    ins, outs = instances(W)
    base = 10 * (6 - d)
    ub0 = base + len(ins) - sum(1 for cs, o in outs if not cs and not o)
    if ub0 <= 0:
        stats['links_ub0'] += 1; stats['nodes'] += 1; return '', ins, outs
    allc = ins + outs
    rel = sorted(set(c for cs, o in allc for (c, lo, hi) in cs), key=site_key)
    vs = [(v, classes_of(v, allc)) for v in rel]
    rq = link_reqs_rot(d, link, model, set(rel)) if ROTCACHE else link_reqs(W, model, set(rel))
    reqs = [(req, k) for k, (req, ci, e) in enumerate(rq)]
    used = set()
    ok = run_dfs(base, vs, ins, outs, reqs, used, stats, stats['nodes'] + maxnodes)   # per-link node budget
    if not ok:
        stats['FAILED_links'] += 1
        return None, ins, outs
    stats['links_dfs'] += 1; stats['embs'] += len(used)
    embs = ';'.join('%d:%s' % (kpos(model)[rq[k][1]], ','.join(map(str, rq[k][2]))) for k in sorted(used))
    return '%s|%s' % (','.join(map(str, rel)), embs), ins, outs

def inst_str(inst):
    cs, o = inst
    return '%s%s' % ('&'.join('%d:%d-%d' % t for t in sorted(cs)), '+O' if o else '')

def main():
    d = int(sys.argv[1]); outf = sys.argv[2]
    model = '633'; nlinks = None; dump = None; sample = None
    a = sys.argv[3:]
    while a:
        if a[0] == '--model': model = a[1]; a = a[2:]
        elif a[0] == '--links': nlinks = int(a[1]); a = a[2:]
        elif a[0] == '--dump-inst': dump = a[1]; a = a[2:]
        elif a[0] == '--sample': sample = (int(a[1]), int(a[2])); a = a[3:]
        elif a[0] == '--parts':                      # replace the 71 parts (e.g. 71 + N2) by a parts file
            R.PARTS[:] = load_parts_file(a[1]); a = a[2:]
        else: raise SystemExit('bad arg ' + a[0])
    stats = collections.Counter(); t0 = time.time()
    lines = []; dl = []
    allL = list(itertools.product((5, 6, 7, 8, 9), repeat=d))
    if sample is not None:          # instance dumps only (the certificate is then not a full one)
        import random
        allL = sorted(random.Random(sample[1]).sample(allL, sample[0]))
    for n, link in enumerate(allL):
        if nlinks is not None and n >= nlinks: break
        line, ins, outs = do_link(d, link, model, stats)
        if line is None:
            print('FAILED link', ''.join(map(str, link)), flush=True); line = ''
        lines.append(line)
        if dump is not None:
            dl.append('%s in %s out %s' % (''.join(map(str, link)), ' '.join(sorted(inst_str(x) for x in ins)),
                                          ' '.join(sorted(inst_str(x) for x in outs))))
        if n % 2000 == 0:
            print(n, dict(stats), round(time.time() - t0), flush=True)
    hdr = '# ST-120 B5 certificate d=%d model=K%s links=%d (allWords order); exporter export_cert.py; rcore 3d133146' % (d, model, len(lines))
    txt = hdr + '\n' + '\n'.join(lines) + '\n'
    open(outf, 'w').write(txt)
    if dump is not None: open(dump, 'w').write('\n'.join(dl) + '\n')
    summ = {'d': d, 'model': model, 'links': len(lines), 'stats': dict(stats), 'secs': round(time.time() - t0, 1),
            'bytes': len(txt.encode()), 'md5': hashlib.md5(txt.encode()).hexdigest()}
    print(json.dumps(summ))
    open(outf + '.summary.json', 'w').write(json.dumps(summ) + '\n')

if __name__ == '__main__':
    main()
