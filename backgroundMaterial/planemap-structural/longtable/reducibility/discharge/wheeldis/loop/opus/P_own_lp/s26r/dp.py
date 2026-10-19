"""Exact count / extremal charge of assignments to a cyclic list of free vertices avoiding forbidden partial assignments.
No sampling: frontier dynamic programme over a linear order, with letters merged into classes that no pattern tells apart."""
import itertools
def reduce_pats(pats):
    pats = sorted(set(pats), key=len); out = []
    for p in pats:
        if not any(q <= p for q in out): out.append(p)
    return out
def solve(free, dom, pats, mode):
    """free: list of vertices in cycle order; dom[x]: allowed letters; pats: list of frozenset((x, letter)).
    mode 'max' / 'min': value = (count, best charge, witness) with charge(l) = 6 - l (99 -> -3).
    Returns (count, best, witness dict)."""
    ch = lambda l: 6 - (9 if l == 99 else l)
    pats = [p for p in reduce_pats(pats) if all(l in dom[x] for x, l in p)]
    n = len(free)
    if n == 0: return (0 if frozenset() in pats else 1), 0, {}
    if frozenset() in pats: return 0, None, None
    # classes
    cls = {}
    for x in free:
        men = sorted({l for p in pats for y, l in p if y == x})
        rest = [l for l in dom[x] if l not in men]
        cl = [(l, 1, l) for l in men]
        if rest:
            b = max(rest, key=ch) if mode == 'max' else min(rest, key=ch)
            cl.append((None, len(rest), b))
        cls[x] = cl
    best_order = None
    for st in range(n):
        order = free[st:] + free[:st]; pos = {x: i for i, x in enumerate(order)}
        last = [max(pos[x] for x, _ in p) for p in pats]
        w = 0
        for i in range(n):
            act = {x for p, lp in zip(pats, last) if lp > i for x, _ in p if pos[x] <= i}
            w = max(w, sum(0 for _ in act) + len(act))
        if best_order is None or w < best_order[0]: best_order = (w, order)
    order = best_order[1]; pos = {x: i for i, x in enumerate(order)}
    fire = [[] for _ in range(n)]
    for p in pats:
        lp = max(pos[x] for x, _ in p); fire[lp].append(tuple(sorted(p, key=lambda t: pos[t[0]])))
    actafter = []
    for i in range(n):
        actafter.append(sorted({x for p in pats if max(pos[y] for y, _ in p) > i for x, _ in p if pos[x] <= i}, key=lambda y: pos[y]))
    better = (lambda a, b: a > b) if mode == 'max' else (lambda a, b: a < b)
    S = {(): (1, 0, ())}          # state: tuple of letters (None = other) for active vertices; value (count, best, wit)
    actv = []
    for i, x in enumerate(order):
        NS = {}
        for key, (cnt, bst, wit) in S.items():
            asg = dict(zip(actv, key))
            for (l, mult, rep) in cls[x]:
                asg[x] = l
                dead = False
                for p in fire[i]:
                    if all(asg.get(y) == ll for y, ll in p): dead = True; break
                if dead: continue
                nk = tuple(asg[y] for y in actafter[i])
                nv = (cnt * mult, bst + ch(rep), wit + ((x, rep),))
                o = NS.get(nk)
                if o is None: NS[nk] = nv
                else:
                    if better(nv[1], o[1]): NS[nk] = (o[0] + nv[0], nv[1], nv[2])
                    else: NS[nk] = (o[0] + nv[0], o[1], o[2])
            asg.pop(x, None)
        S = NS; actv = actafter[i]
    if not S: return 0, None, None
    cnt = sum(v[0] for v in S.values())
    bk = max(S.values(), key=lambda v: v[1]) if mode == 'max' else min(S.values(), key=lambda v: v[1])
    return cnt, bk[1], dict(bk[2])
def brute(free, dom, pats, mode):
    ch = lambda l: 6 - (9 if l == 99 else l)
    pats = [tuple(p) for p in pats]; cnt = 0; best = None
    for vals in itertools.product(*[dom[x] for x in free]):
        a = dict(zip(free, vals))
        if any(all(a[y] == l for y, l in p) for p in pats): continue
        cnt += 1; c = sum(ch(v) for v in vals)
        if best is None or (c > best if mode == 'max' else c < best): best = c
    return cnt, best
