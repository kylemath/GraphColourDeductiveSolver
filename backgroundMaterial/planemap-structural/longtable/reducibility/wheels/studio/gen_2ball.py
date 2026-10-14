"""Studio Job 9 (exploratory): second-ring (2-ball) configurations around the 66666 hole.
Interior: hole v (deg 5), x_0..x_4 (deg 6), and the first ring y_0..y_9 = p_0 s_0 p_1 s_1 ... p_4 s_4 with
p_i the private neighbour of x_i and s_i shared by x_i, x_{i+1}.  Each y gets a degree in {5,6,7,8}; y has k known
neighbours (p: x_i, s_{i-1}, s_i -> 3; s: x_i, x_{i+1}, p_i, p_{i+1} -> 4) and o = d - k outward edges, fanned onto the
new ring: y_j sees t_{j-1}, (o-2) private ring vertices, t_j; when o = 1 (an s of degree 5) t_j = t_{j-1}.
Ring length r = sum(d_p - 4) + sum(d_s - 5).  Assignments are taken up to the dihedral symmetry of the wheel
(rotation by a (p, s) pair, reflection).  Pruned: a Birkhoff diamond or RSST 2.122 among the interior (known-degree)
vertices (picyc's definition: edge ab, face-neighbours c, d of degree 5, c not adjacent to d; diamond: deg a = deg b = 5;
2.122: {deg a, deg b} = {5, 6}).
Writes configs_2ball.txt (WheelMain format; name = degree word of y_0..y_9) and 2ball_index.json."""
import itertools, json, collections, sys
P = lambda i: 6 + 2 * (i % 5); S = lambda i: 7 + 2 * (i % 5)   # interior ids: 0 hole, 1..5 x, 6.. y (y_j = 6 + j)
def canon(t):
    best = None
    for k in range(5):
        r = t[2 * k:] + t[:2 * k]; best = r if best is None or r < best else best
        # reflection: p_i -> p_{-i}, s_i -> s_{-i-1}
        f = [None] * 10
        for i in range(5): f[2 * i] = t[2 * ((-i) % 5)]; f[2 * i + 1] = t[2 * ((-i - 1) % 5) + 1]
        f = tuple(f); r = f[2 * k:] + f[:2 * k]; best = r if r < best else best
    return best
def build(deg):
    # deg: tuple of 10 degrees for y_0..y_9 (y_{2i} = p_i, y_{2i+1} = s_i)
    m = 16; intadj = [set() for _ in range(m)]; D = [5] + [6] * 5 + list(deg)
    def E(a, b): intadj[a].add(b); intadj[b].add(a)
    for i in range(5):
        E(0, 1 + i); E(1 + i, 1 + (i + 1) % 5)
        E(1 + i, P(i)); E(1 + i, S(i)); E(1 + i, S(i - 1)); E(1 + (i + 1) % 5, S(i))
    for j in range(10): E(6 + j, 6 + (j + 1) % 10)
    o = [D[6 + j] - len(intadj[6 + j]) for j in range(10)]
    if any(x < 1 for x in o) or all(x == 1 for x in o): return None
    # ring construction: start at a y with o >= 2 so that t_{j-1} exists
    j0 = next(j for j in range(10) if o[j] >= 2)
    ring = []; ringadj = [[] for _ in range(m)]
    order = [(j0 + k) % 10 for k in range(10)]
    first_t = None; prev_t = None
    # t_{j0-1}: created at the end (the shared vertex closing the cycle); use placeholder -1
    for j in order:
        y = 6 + j; nb = []
        nb.append(prev_t if prev_t is not None else 'T0')
        if o[j] >= 2:
            for _ in range(o[j] - 2): ring.append(len(ring)); nb.append(ring[-1])
            ring.append(len(ring)); t = ring[-1]; nb.append(t); prev_t = t
        ringadj[y] = nb
    # T0 = t_{j0-1} = the last shared vertex created (prev_t), closing the cycle
    for y in range(6, 16):
        ringadj[y] = [prev_t if x == 'T0' else x for x in ringadj[y]]
        ringadj[y] = list(dict.fromkeys(ringadj[y]))
    r = len(ring)
    return r, m, D, [sorted(s) for s in intadj], ringadj
def faces_int(intadj):
    F = set()
    for a in range(len(intadj)):
        for b in intadj[a]:
            for c in intadj[a] & intadj[b] if isinstance(intadj[a], set) else set(intadj[a]) & set(intadj[b]):
                F.add(tuple(sorted((a, b, c))))
    return F
def bad_config(D, intadj):
    A = [set(x) for x in intadj]; F = faces_int(A)
    for a in range(len(A)):
        for b in A[a]:
            if b < a: continue
            cs = [f for f in F if a in f and b in f]
            if len(cs) != 2: continue
            c, d = [[x for x in f if x not in (a, b)][0] for f in cs]
            if D[c] == 5 and D[d] == 5 and d not in A[c]:
                if D[a] == 5 and D[b] == 5: return 'diamond'
                if {D[a], D[b]} == {5, 6}: return '2.122'
    return None
if __name__ == '__main__':
    seen = set(); out = open('configs_2ball.txt', 'w'); idx = {}; tally = collections.Counter()
    for deg in itertools.product((5, 6, 7, 8), repeat=10):
        c = canon(deg)
        if c in seen: continue
        seen.add(c)
        b = build(c)
        if b is None: tally['invalid'] += 1; continue
        r, m, D, ia, ra = b
        why = bad_config(D, ia)
        name = ''.join(map(str, c))
        idx[name] = dict(r=r, pruned=why)
        if why: tally['pruned_' + why] += 1; continue
        tally['ring%d' % r] += 1
        fmt = lambda L: ';'.join(','.join(map(str, x)) if x else '-' for x in L)
        out.write('b%s %d %d %s %s\n' % (name, r, m, fmt(ra), fmt(ia)))
    json.dump(idx, open('2ball_index.json', 'w'))
    print(len(seen), dict(sorted(tally.items())))
