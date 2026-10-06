"""2-ball configurations around a degree-5 vertex, as abstract discs.

[computed, exploratory] Math worker, 2026-10-06.  With the README section-1 definition of K
(faces with all vertices at distance <= 2 and one at distance < 2), the 2-ball of v is the
union of the faces v u_i u_{i+1}, u_i u_{i+1} x_i and the fans u_i w w'.  When the link is
induced and the ring is a simple cycle (no distance-2 vertex adjacent to two non-consecutive
link vertices), K is determined by the cyclic link-degree sequence (d_1..d_5), up to
rotation and reflection.  Ring length = sum(d_i) - 20; |K - v| = 5 + ring length.
"""
import itertools, sys, time
import vdred, vdred_joint


def config_from_degrees(ds):
    v = 0; U = [1, 2, 3, 4, 5]
    nxt = 6
    outer = []
    first = None
    for i, d in enumerate(ds):
        k = d - 3                      # outer neighbours of u_i, in order
        assert k >= 2
        lst = [None] * k
        if i > 0:
            lst[0] = outer[-1][-1]
        for j in range(1 if i > 0 else 0, k):
            if i == 4 and j == k - 1:
                lst[j] = outer[0][0]
            else:
                lst[j] = nxt; nxt += 1
        outer.append(lst)
    ring = []
    for lst in outer:
        ring += lst[:-1]
    edges = set()
    def e(a, b): edges.add(tuple(sorted((a, b))))
    for i in range(5):
        e(U[i], U[(i + 1) % 5])
        for w in outer[i]:
            e(U[i], w)
        for a, b in zip(outer[i], outer[i][1:]):
            e(a, b)
    verts = sorted(set(U) | set(ring))
    assert len(ring) == sum(ds) - 20 == len(set(ring))
    return dict(link=U, ring=ring, verts=verts, edges=sorted(edges), v=v, r=2)


def bracelets(vals):
    seen = set(); out = []
    for s in itertools.product(vals, repeat=5):
        reps = []
        for r in range(5):
            t = s[r:] + s[:r]
            reps += [t, t[::-1]]
        c = min(reps)
        if c not in seen:
            seen.add(c); out.append(c)
    return out


if __name__ == '__main__':
    for D in range(5, 12):
        k = D - 4
        print(f"link degrees in [5,{D}]: {len(bracelets(range(5, D + 1)))} configurations "
              f"(formula (k^5+5k^3+4k)/10 = {(k**5 + 5*k**3 + 4*k)//10})")
    for s in bracelets((5, 6)):
        t0 = time.process_time()
        cfg = config_from_degrees(s)
        a = vdred.solve(cfg, verbose=False)
        b = vdred_joint.solve_joint(cfg, verbose=False)
        print(s, 'ring', len(cfg['ring']), '| vdred:', a['reducible'], a['depth'], a['hist'],
              '| joint:', b['reducible'], b['depth'], b['hist'], f"| {time.process_time()-t0:.1f}s", flush=True)
