# W16: simulated-annealing flip walks on small tori; objective = #vertices whose LP row is inadmissible + degree penalties.
# Records every state with objective 0 (all rows admissible, degrees in the allowed set) by its row multiset.
import sys, os, random, time, math, pickle, json, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
import torus as TT, w16lib as W

_RAW = {}
def vstat(T, v, allowed):
    d = T.deg[v]
    if d < 5: return 3 * (5 - d)
    if d > 9: return 3 * (d - 9)
    pen = 0 if d in allowed else 1
    w, s, r, ap = TT.words(T, v)
    if min(w) < 5 or min(s) < 5: return pen + 1
    if d == 5:
        if any(T.deg[x] == 6 and min(T.deg[y] for y in T.adj[x]) < 5 for x in r): return pen + 1
        F = tuple(TT.letter(T.deg[T.rot(x)[(T.rot(x).index(v) + 3) % 6]]) if T.deg[x] == 6 else 0 for x in r)
        key = (tuple(w), tuple(min(x, 7) for x in s), F)
    elif d == 6: key = (tuple(w), tuple(min(x, 7) for x in s))
    else:
        pv = W.privates(T, v)
        if any(min(x) < 5 for x in pv if x): return pen + 1
        key = (tuple(w), tuple(s), pv)
    st = _RAW.get(key)
    if st is None:
        st = 0 if W.row_status(W.vertex_row(T, v)) is None else 1
        if st == 0 and d >= 7 and W.payee_kills(d, w, s, pv): st = 1
        _RAW[key] = st
    return pen + st

def objective(T, allowed):
    return sum(vstat(T, v, allowed) for v in range(T.n))
def ball2(T, S):
    b = set(S)
    for _ in range(2): b |= {y for x in list(b) for y in T.adj[x]}
    return b

def anneal(T, allowed, steps, T0=1.0, T1=0.08, rng=random, found=None, tag='', need=None, nmin=0):
    st = [vstat(T, v, allowed) for v in range(T.n)]; n6 = sum(1 for x in T.deg if x != 6); cur = sum(st) + max(0, nmin - n6)
    for it in range(steps):
        temp = T0 * (T1 / T0) ** (it / steps)
        u, v = rng.choice(list(T.opp.keys()))
        a = T.opp[(u, v)]; b = T.opp[(v, u)]
        if T.deg[u] <= 3 or T.deg[v] <= 3: continue
        if not T.flip(u, v): continue
        B = ball2(T, (u, v, a, b)); nst = {x: vstat(T, x, allowed) for x in B}
        n6new = sum(1 for x in T.deg if x != 6)
        new = cur - max(0, nmin - n6) + max(0, nmin - n6new) + sum(nst[x] - st[x] for x in B)
        if new <= cur or rng.random() < math.exp((cur - new) / temp):
            cur = new; n6 = n6new
            for x in B: st[x] = nst[x]
            if cur == 0 and found is not None:
                labs, cnt = W.pattern_rows(T)
                if need is None or need(cnt):
                    key = frozenset(cnt)
                    if key not in found:
                        found[key] = dict(faces=sorted(T.faces), n=T.n, cnt=cnt, tag=tag, degs=collections.Counter(T.deg))
        else:
            T.flip(a, b)   # undo
    return cur

def local_repair(T, allowed, found, tag, need, depth=2, maxtry=3000):
    """exhaustive flips (up to depth) on edges near bad vertices; records zero states; returns final objective."""
    def bad_vertices():
        return [v for v in range(T.n) if vstat(T, v, allowed) > 0]
    cur = objective(T, allowed)
    if cur == 0: return 0
    tries = 0
    def near_edges():
        bv = bad_vertices(); B = set(bv)
        for x in list(B): B |= T.adj[x]
        return [(u, v) for (u, v) in T.opp if u < v and (u in B or v in B)]
    for (u, v) in near_edges():
        a = T.opp[(u, v)]; b = T.opp[(v, u)]
        if T.deg[u] <= 4 or T.deg[v] <= 4 or not T.flip(u, v): continue
        o1 = objective(T, allowed); tries += 1
        if o1 == 0:
            labs, cnt = W.pattern_rows(T)
            if need(cnt) and frozenset(cnt) not in found:
                found[frozenset(cnt)] = dict(faces=sorted(T.faces), n=T.n, cnt=cnt, tag=tag + '/rep1', degs=collections.Counter(T.deg))
            return 0
        if depth >= 2 and o1 <= cur + 1:
            for (x, y) in near_edges():
                if tries > maxtry: break
                a2 = T.opp[(x, y)]; b2 = T.opp[(y, x)]
                if T.deg[x] <= 4 or T.deg[y] <= 4 or not T.flip(x, y): continue
                o2 = objective(T, allowed); tries += 1
                if o2 == 0:
                    labs, cnt = W.pattern_rows(T)
                    if need(cnt) and frozenset(cnt) not in found:
                        found[frozenset(cnt)] = dict(faces=sorted(T.faces), n=T.n, cnt=cnt, tag=tag + '/rep2', degs=collections.Counter(T.deg))
                    return 0
                T.flip(a2, b2)
        T.flip(a, b)
        if tries > maxtry: break
    return cur

if __name__ == '__main__':
    out = sys.argv[1]; seed = int(sys.argv[2]); budget = float(sys.argv[3])   # seconds
    W.init()
    rng = random.Random(seed); found = {}
    if os.path.exists(out): found = pickle.load(open(out, 'rb'))
    configs = [((5, 6, 7, 8, 9), None), ((5, 7), None), ((5, 8), None), ((5, 6, 7), None), ((5, 7, 8), None), ((5, 6, 8), None),
               ((5, 6, 7, 8), None), ((5, 6, 7, 8, 9), None), ((5, 6, 7), None), ((5, 6, 8), None), ((5, 6, 7, 9), None), ((5, 6, 9), None)]
    lat = [(p, q, r) for p in range(3, 9) for r in range(3, 9) for q in range(p) if 9 <= p * r <= int(os.environ.get('NMAX', '24'))]
    t0 = time.time(); runs = 0
    while time.time() - t0 < budget:
        allowed, _ = rng.choice(configs); p, q, r = rng.choice(lat)
        try:
            T = TT.lattice_torus(p, q, r); T.check()
        except AssertionError:
            continue
        nb = len(found)
        nmin = rng.choice([T.n // 4, T.n // 3, T.n // 2]) if 6 in allowed else 0
        res = anneal(T, set(allowed), steps=rng.choice([4000, 8000, 16000]), rng=rng, nmin=nmin, found=found, tag='%s/%d,%d,%d' % (''.join(map(str, allowed)), p, q, r),
                     need=lambda cnt: any(l[0] != 'C' for l in cnt))
        if 0 < res <= 5:
            res2 = local_repair(T, set(allowed), found, '%s/%d,%d,%d' % (''.join(map(str, allowed)), p, q, r), lambda cnt: any(l[0] != 'C' for l in cnt))
            res = '%s->%s' % (res, res2)
        runs += 1
        try:
            bad = [(T.deg[v], W.row_status(W.vertex_row(T, v)) or ('kill' if T.deg[v] >= 7 else 'pen')) for v in range(T.n) if vstat(T, v, set(allowed))]
        except Exception as e: bad = [str(e)[:40]]
        print('   bad:', bad, flush=True)
        if True:
            print('run %d n=%d allowed=%s final obj %s, found %d (+%d) [%.0fs]' % (runs, T.n, allowed, res, len(found), len(found) - nb, time.time() - t0), flush=True)
            pickle.dump(found, open(out + '.tmp', 'wb')); os.replace(out + '.tmp', out)
    pickle.dump(found, open(out + '.tmp', 'wb')); os.replace(out + '.tmp', out)
    print('done: %d runs, %d distinct admissible row sets' % (runs, len(found)))
