"""Exact frontier DP (faster version of dp.py, one pass gives count, max and min charge with witnesses).
Assignments of letters to a cyclic list of free vertices that contain none of the forbidden partial assignments."""
import itertools
def ch(l): return 6 - (9 if l == 99 else l)
def reduce_pats(pats):
    pats = sorted(set(pats), key=len); out = []
    for p in pats:
        if not any(q <= p for q in out): out.append(p)
    return out
def unwind(w):
    d = {}
    while w is not None: w, (x, l) = w; d[x] = l
    return d
def solve(free, dom, pats):
    """returns (count, max, wit_max, min, wit_min); charge(99) = -3. count 0 -> (0, None, None, None, None)"""
    pats = [p for p in reduce_pats(pats) if all(x in dom and l in dom[x] for x, l in p)]
    n = len(free)
    if frozenset() in pats: return 0, None, None, None, None
    if n == 0: return 1, 0, {}, 0, {}
    cls = {}
    for x in free:
        men = sorted({l for p in pats for y, l in p if y == x})
        rest = [l for l in dom[x] if l not in men]
        cl = [(l, 1, l, l) for l in men]
        if rest: cl.append((None, len(rest), max(rest, key=ch), min(rest, key=ch)))
        cls[x] = cl
    # order: rotation minimising the largest frontier
    best = None
    for st in range(n):
        order = free[st:] + free[:st]; pos = {x: i for i, x in enumerate(order)}
        sp = [(min(pos[x] for x, _ in p), max(pos[x] for x, _ in p)) for p in pats]
        w = max(sum(1 for k in range(i + 1) if any(a <= k <= i < b for a, b in [(pos_k, None)][0:0]) ) for i in range(1)) if False else 0
        cnt = [0] * n
        for x in order:
            px = pos[x]; lastuse = max([b for (a, b), p in zip(sp, pats) if any(y == x for y, _ in p)], default=px)
            for i in range(px, lastuse): cnt[i] += 1
        w = max(cnt)
        if best is None or w < best[0]: best = (w, order)
    order = best[1]; pos = {x: i for i, x in enumerate(order)}
    lastuse = {x: max([max(pos[y] for y, _ in p) for p in pats if any(y == x for y, _ in p)], default=pos[x]) for x in order}
    actv = []; S = {(): (1, 0, None, 0, None)}; maxst = 1
    for i, x in enumerate(order):
        full = actv + [x]; idx = {y: k for k, y in enumerate(full)}
        fires = {}
        for p in pats:
            if max(pos[y] for y, _ in p) == i:
                lx = dict(p)[x]; fires.setdefault(lx, []).append(tuple((idx[y], l) for y, l in p if y != x))
        nact = [y for y in full if lastuse[y] > i]; proj = [idx[y] for y in nact]
        NS = {}
        for key, (c, mx, wmx, mn, wmn) in S.items():
            for (l, mult, rmx, rmn) in cls[x]:
                t = key + (l,)
                fl = fires.get(l)
                if fl and any(all(t[k] == ll for k, ll in p) for p in fl): continue
                nk = tuple(t[k] for k in proj)
                v = (c * mult, mx + ch(rmx), (wmx, (x, rmx)), mn + ch(rmn), (wmn, (x, rmn)))
                o = NS.get(nk)
                if o is None: NS[nk] = v
                else:
                    a = (o[1], o[2]) if o[1] >= v[1] else (v[1], v[2]); b = (o[3], o[4]) if o[3] <= v[3] else (v[3], v[4])
                    NS[nk] = (o[0] + v[0], a[0], a[1], b[0], b[1])
        S = NS; actv = nact; maxst = max(maxst, len(S))
        if not S: return 0, None, None, None, None
    c = sum(v[0] for v in S.values()); bx = max(S.values(), key=lambda v: v[1]); bn = min(S.values(), key=lambda v: v[3])
    return c, bx[1], unwind(bx[2]), bn[3], unwind(bn[4])
def brute(free, dom, pats):
    pats = [tuple(p) for p in pats]; cnt = 0; mx = mn = None
    for vals in itertools.product(*[dom[x] for x in free]):
        a = dict(zip(free, vals))
        if any(all(a[y] == l for y, l in p) for p in pats): continue
        cnt += 1; c = sum(ch(v) for v in vals)
        mx = c if mx is None else max(mx, c); mn = c if mn is None else min(mn, c)
    return cnt, mx, mn
