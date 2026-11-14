"""Canonical codes for configurations (embedded interior graph + degrees).

A configuration here: m interior vertices, deg[v], irot[v] = cyclic list of
interior neighbours of v (rotation filtered to interior), gaps[v] = number of
ring runs in v's full rotation, ring_in_gap etc. are folded into deg.
"""
from collections import deque


def shape_codes(irot, mirror=False):
    """Return (mincode, [orders]) over all roots/starts.
    orders[i] = list of vertices in BFS order (the canonical labelling).
    Requires the interior graph to be connected; vertices with no interior
    neighbour only allowed if m == 1."""
    m = len(irot)
    rot = [list(reversed(r)) for r in irot] if mirror else irot
    best = None
    orders = []
    for root in range(m):
        starts = rot[root] if rot[root] else [None]
        for st in starts:
            lab = {root: 0}
            order = [root]
            code = []
            q = deque([(root, st)])
            while q:
                v, frm = q.popleft()
                r = rot[v]
                if r:
                    k = r.index(frm) if frm is not None else 0
                    seq = r[k:] + r[:k]
                else:
                    seq = []
                code.append(len(seq))
                for w in seq:
                    if w not in lab:
                        lab[w] = len(order)
                        order.append(w)
                        q.append((w, v))
                    code.append(lab[w])
            if len(order) != m:
                return None, []  # disconnected
            code = tuple(code)
            if best is None or code < best:
                best = code
                orders = [order]
            elif code == best:
                orders.append(order)
    return best, orders


def cfg_from_pool(c):
    m = c['m']
    irot = [[t[1] for t in r if t[0] == 'I'] for r in c['rot']]
    gaps = []
    for r in c['rot']:
        s = ''.join(t[0] for t in r)
        if 'I' not in s:
            gaps.append(1)
        else:
            gaps.append(sum(1 for i in range(len(s)) if s[i] == 'R' and s[i - 1] == 'I'))
    return dict(m=m, deg=list(c['deg']), irot=irot, gaps=gaps, name=c['name'],
                kind=c['kind'])


def full_code(c, mirror=False):
    """Shape code + degree vector, minimised over canonical labellings."""
    sc, orders = shape_codes(c['irot'], mirror)
    if sc is None:
        return None
    dv = min(tuple(c['deg'][v] for v in o) for o in orders)
    return (sc, dv)


def delete_vertex(c, v):
    m = c['m']
    keep = [u for u in range(m) if u != v]
    idx = {u: i for i, u in enumerate(keep)}
    irot = [[idx[w] for w in c['irot'][u] if w != v] for u in keep]
    return dict(m=m - 1, deg=[c['deg'][u] for u in keep], irot=irot)
