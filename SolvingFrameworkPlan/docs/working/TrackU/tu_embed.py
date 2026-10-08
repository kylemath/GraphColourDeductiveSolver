#!/usr/bin/env python3
"""Track U: find an orientable rotation system on an abstract G5 graph (rotation at v fixed to f0..f4) whose dual,
with a degree-5 vertex h re-inserted in the pentagon at v, is a SIMPLICIAL triangulation T of an orientable
surface.  Then G is the Tait dual of T at hole h (tt_lib.tait_dual convention: f_t dual to link edge x_t x_{t+1}),
so TrackS/TrackL's colouring engine can be run on (T, h) as an independent check.
usage: tu_embed.py GRAPHLINES_FILE [index] [tries]  -> prints 'name nprimal rot' line (TrackF format) + genus"""
import sys, random


def faces(n, E, rot):
    """rot[x] = list of edge ids in cyclic order. darts (x, e). next dart after arriving at y via e: (y, succ_y(e))"""
    pos = [{e: i for i, e in enumerate(r)} for r in rot]
    seen = set(); F = []
    for x in range(n):
        for e in rot[x]:
            if (x, e) in seen: continue
            face = []; d = (x, e)
            while d not in seen:
                seen.add(d); face.append(d)
                a, b = E[d[1]]; y = b if a == d[0] else a
                r = rot[y]; d = (y, r[(pos[y][d[1]] + 1) % len(r)])
            F.append(face)
    return F


def defects(n, E, rot):
    F = faces(n, E, rot)
    side = {}
    bad = 0
    for fi, f in enumerate(F):
        vs = [d[0] for d in f]
        if len(vs) < 3: bad += 3
        bad += len(vs) - len(set(vs))
        for d in f: side.setdefault(d[1], []).append(fi)
    pairs = {}
    for e, s in side.items():
        if s[0] == s[1]: bad += 1
        else:
            k = tuple(sorted(s)); pairs[k] = pairs.get(k, 0) + 1
    bad += sum(c - 1 for c in pairs.values())
    # distinct triangles: two cubic vertices with the same 3 faces
    tri = {}
    for x in range(1, n):
        fs = frozenset(side[e][0] for e in rot[x]) | frozenset(side[e][1] for e in rot[x])
    return bad, F


def primal(n, E, fv, rot, F):
    """build primal rotation: vertices = faces (0..|F|-1), h = |F|"""
    side = {}
    fid = {}
    for fi, f in enumerate(F):
        for d in f: fid[d] = fi
    def other_face(d):
        x, e = d; a, b = E[e]; y = b if a == x else a
        return fid[(y, e)]
    H = len(F); prot = []
    for fi, f in enumerate(F):
        r = []
        for d in f:
            r.append(other_face(d))
            # after traversing edge d we arrive at y; if y == v, the face passes through v: insert h
            x, e = d; a, b = E[e]; y = b if a == x else a
            if y == 0: r.append(H)
        prot.append(r)
    # h: faces around v.  face between f_t and f_{t+1} ... link vertex x_t lies between f_{t-1} and f_t
    # f_t is dual to link edge x_t x_{t+1}: x_t and x_{t+1} are the two faces on the sides of f_t.
    link = []
    for t in range(5):
        a, b = fid[(0, fv[t])], other_face((0, fv[t]))
        link.append((a, b))
    # find x_0..x_4 with {x_t, x_{t+1}} = sides of f_t
    for x0 in link[0]:
        xs = [x0]; ok = True
        for t in range(5):
            s = set(link[t]); s.discard(xs[-1])
            if len(s) != 1 or (len(xs) > 0 and xs[-1] not in link[t]): ok = False; break
            xs.append(s.pop())
        if ok and xs[5] == xs[0]:
            prot.append(xs[:5]); return prot
    return None


def search(n, E, fv, tries=200, rnd=random.Random(1)):
    inc = [[] for _ in range(n)]
    for k, (a, b) in enumerate(E): inc[a].append(k); inc[b].append(k)
    best = None
    for _ in range(tries):
        rot = [list(fv)] + [rnd.sample(inc[x], 3) for x in range(1, n)]
        bad, F = defects(n, E, rot)
        for it in range(4000):
            if bad == 0: break
            x = rnd.randrange(1, n); rot[x] = rot[x][::-1]
            b2, F2 = defects(n, E, rot)
            if b2 <= bad or rnd.random() < 0.05: bad, F = b2, F2
            else: rot[x] = rot[x][::-1]
        if bad == 0:
            g = (2 - n + len(E) - len(F) - 0) // 2   # V - E + F with V = n (v counted as a vertex), faces of G
            # primal: V' = F + 1, E' = |E| + 5, F' = n - 1 + 5 ; chi = V' - E' + F' = F - |E| + n
            chi = len(F) - len(E) + n
            if best is None or chi > best[0]:
                best = (chi, [list(r) for r in rot], F)
                if chi >= 0: break
    return best


def main():
    lines = [l for l in open(sys.argv[1]) if l.strip()]
    idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    tries = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    p = list(map(int, lines[idx].split()))
    n, m = p[0], p[1]; E = [(p[2 + 2 * i], p[3 + 2 * i]) for i in range(m)]; fv = p[2 + 2 * m: 7 + 2 * m]
    res = search(n, E, fv, tries)
    if res is None: print('NONE', file=sys.stderr); return
    chi, rot, F = res
    prot = primal(n, E, fv, rot, F)
    print('genus(orientable) =', (2 - chi) // 2, 'chi =', chi, 'primal vertices =', len(prot), file=sys.stderr)
    print('emb%d_%d %d %s' % (idx, len(prot), len(prot), ';'.join(','.join(map(str, r)) for r in prot)), 'h=%d' % (len(prot) - 1))


if __name__ == '__main__':
    main()
