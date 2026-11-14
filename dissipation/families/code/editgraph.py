"""Edit graph on a set of configurations.

Edge types (each counted separately):
  deg1   same embedded interior shape (same orientation), degree vectors differ
         at exactly one vertex, by exactly 1
  degk   same shape, differ at exactly one vertex, by more than 1
  add0   B minus one vertex == A exactly (shape + all degrees): containment
  add1   B minus one vertex == A in shape, and degrees differ at one vertex
  mirror A is the mirror image of B (A != B as oriented configurations)
Also: mirror-symmetric count, twin present / absent counts, exact duplicates.
"""
from collections import defaultdict
from canon import shape_codes, full_code, delete_vertex


class UF:
    def __init__(s, n):
        s.p = list(range(n))

    def f(s, x):
        while s.p[x] != x:
            s.p[x] = s.p[s.p[x]]
            x = s.p[x]
        return x

    def u(s, a, b):
        a, b = s.f(a), s.f(b)
        if a != b:
            s.p[a] = b


def ham(a, b):
    return [i for i in range(len(a)) if a[i] != b[i]]


def ushape(irot):
    a, oa = shape_codes(irot)
    b, ob = shape_codes(irot, mirror=True)
    if a is None:
        return None, []
    if a < b:
        return a, oa
    if b < a:
        return b, ob
    return a, oa + ob


def build(cfgs, unoriented=False):
    SC = ushape if unoriented else shape_codes
    n = len(cfgs)
    sc = []
    by_shape = defaultdict(list)
    fulls = {}
    for i, c in enumerate(cfgs):
        code, orders = SC(c['irot'])
        degs = [tuple(c['deg'][v] for v in o) for o in orders]
        sc.append((code, degs))
        by_shape[code].append(i)
        fc = (code, min(degs))
        fulls.setdefault(fc, []).append(i)
    edges = defaultdict(set)
    dup = sum(len(v) - 1 for v in fulls.values())
    # degree edits
    for code, idx in by_shape.items():
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                dj = sc[j][1][0]
                best = None
                for di in sc[i][1]:
                    h = ham(di, dj)
                    if best is None or len(h) < len(best[0]):
                        best = (h, di)
                h, di = best
                if len(h) == 1:
                    k = h[0]
                    t = 'deg1' if abs(di[k] - dj[k]) == 1 else 'degk'
                    edges[t].add((min(i, j), max(i, j)))
    # vertex deletion
    for j, c in enumerate(cfgs):
        for v in range(c['m']):
            r = delete_vertex(c, v)
            code, orders = SC(r['irot'])
            if code is None or code not in by_shape:
                continue
            dsub = [tuple(r['deg'][u] for u in o) for o in orders]
            for i in by_shape[code]:
                di = sc[i][1][0]
                h = min(len(ham(di, d)) for d in dsub)
                if h == 0:
                    edges['add0'].add((i, j))
                elif h == 1:
                    edges['add1'].add((i, j))
    # mirror
    sym = 0
    twin = 0
    notwin = 0
    for i, c in enumerate(cfgs):
        if unoriented:
            break
        mc = full_code(c, mirror=True)
        own = (sc[i][0], min(sc[i][1]))
        if mc == own:
            sym += 1
            continue
        js = fulls.get(mc, [])
        if js:
            twin += 1
            for j in js:
                edges['mirror'].add((min(i, j), max(i, j)))
        else:
            notwin += 1
    return dict(n=n, shapes=len(by_shape), dup=dup, edges=edges,
                sym=sym, twin=twin, notwin=notwin, by_shape=by_shape)


def components(n, edge_sets):
    uf = UF(n)
    for es in edge_sets:
        for a, b in es:
            uf.u(a, b)
    comp = defaultdict(list)
    for i in range(n):
        comp[uf.f(i)].append(i)
    sizes = sorted((len(v) for v in comp.values()), reverse=True)
    return comp, sizes


def summary(res, types=('deg1', 'degk', 'add0', 'add1', 'mirror')):
    n = res['n']
    out = dict(n=n, shapes=res['shapes'], dup=res['dup'], sym=res['sym'],
               twin=res['twin'], notwin=res['notwin'])
    for t in types:
        out['E_' + t] = len(res['edges'].get(t, ()))
    for label, ts in [('C_deg1', ['deg1']),
                      ('C_deg', ['deg1', 'degk']),
                      ('C_deg_add', ['deg1', 'degk', 'add0', 'add1']),
                      ('C_all', ['deg1', 'degk', 'add0', 'add1', 'mirror'])]:
        comp, sizes = components(n, [res['edges'].get(t, ()) for t in ts])
        out[label] = len(sizes)
        out[label + '_single'] = sum(1 for s in sizes if s == 1)
        out[label + '_max'] = sizes[0]
    return out
