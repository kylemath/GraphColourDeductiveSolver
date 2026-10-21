# Build Gemini's chiral C3 triple wheel T_C3 and its sub-clusters as wheeldis configuration lines.
# Vertex names as in Gemini's logbook post (21 Oct 2026): hubs u_i (7), link a_i(6) b_i(6) c_i(5) d_i(5),
# wings p_i(6) q_i(7) r_i(5) s_i(6); x_i, y_i are the further ring vertices around b_i and r_i.
import itertools, sys
def mod(i): return i % 3
adj = {}
def add(x, y):
    adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
for i in range(3):
    u, u1, u2 = f"u{i}", f"u{mod(i+1)}", f"u{mod(i+2)}"
    a, b, c, d, a1 = f"a{i}", f"b{i}", f"c{i}", f"d{i}", f"a{mod(i+1)}"
    p, q, r, s, x, y, sm = f"p{i}", f"q{i}", f"r{i}", f"s{i}", f"x{i}", f"y{i}", f"s{mod(i-1)}"
    for v in (u1, u2, a, b, c, d, a1): add(u, v)
    for v in (b, p, sm): add(a, v)          # a_i ~ u_i, u_{i-1} (added from u_{i-1}), b_i, p_i, s_{i-1}, d_{i-1} (from d)
    for v in (c, p, x, q): add(b, v)
    for v in (d, q, r): add(c, v)
    for v in (a1, r, s): add(d, v)
    for v in (q, y, s): add(r, v)
    # ring cycle edges
    add(p, x); add(x, q); add(q, y); add(y, s); add(s, f"p{mod(i+1)}")
deg = {f"u{i}": 7 for i in range(3)}
for i in range(3):
    deg.update({f"a{i}": 6, f"b{i}": 6, f"c{i}": 5, f"d{i}": 5, f"r{i}": 5})
ringorder = []
for i in range(3): ringorder += [f"p{i}", f"x{i}", f"q{i}", f"y{i}", f"s{i}"]

def window(name, interior):
    interior = list(interior)
    # ring = neighbours of interior not in interior, in cyclic order along a ring cycle
    ringset = set()
    for v in interior: ringset |= adj[v] - set(interior)
    # find cyclic order: walk the ring cycle using edges among ring vertices that bound the cluster
    # for these windows the ring order is the subsequence of the full outer cycle plus the hub/link vertices
    full = ringorder + []
    # build cyclic order by walking: start from a ring vertex, go to a ring neighbour not yet used that is adjacent to interior
    order = [sorted(ringset)[0]]
    while True:
        cur = order[-1]
        nxt = [w for w in adj[cur] if w in ringset and w not in order]
        if not nxt: break
        # prefer the neighbour sharing an interior face with cur: choose one with a common interior neighbour
        nxt.sort(key=lambda w: -len((adj[cur] & adj[w]) & set(interior)))
        order.append(nxt[0])
    assert set(order) == ringset, (set(order) ^ ringset)
    assert order[0] in adj[order[-1]], "ring not closed"
    r, m = len(order), len(interior)
    ridx = {v: k for k, v in enumerate(order)}; iidx = {v: k for k, v in enumerate(interior)}
    ringadj = []; intadj = []
    for v in interior:
        rn = sorted(ridx[w] for w in adj[v] if w in ridx)
        inn = sorted(iidx[w] for w in adj[v] if w in iidx)
        assert len(rn) + len(inn) == deg[v], (v, rn, inn, deg[v])
        ringadj.append(",".join(map(str, rn)) if rn else "-")
        intadj.append(",".join(map(str, inn)))
    V = r + m
    E = sum(len(adj[v] & (set(interior) | ringset)) for v in interior)  # interior edges counted twice for int-int
    ii = sum(len(adj[v] & set(interior)) for v in interior) // 2
    ir = sum(len(adj[v] & ringset) for v in interior)
    Etot = ii + ir + r
    assert Etot == 3 * V - 3 - r, ("Euler disc check failed", Etot, 3 * V - 3 - r)
    line = f"{name} {r} {m} {';'.join(ringadj)} {';'.join(intadj)}"
    print(f"# {name}: interior {interior}\n# ring order {order}\n# V={V} E={Etot} ok", file=sys.stderr)
    return line

hubs = ["u0", "u1", "u2"]
link = lambda i: [f"a{i}", f"b{i}", f"c{i}", f"d{i}", f"a{mod(i+1)}"]
C18 = hubs + sorted(set(link(0) + link(1) + link(2))) + ["r0", "r1", "r2"]
C14 = hubs + sorted(set(link(0) + link(1))) + ["r0", "r1"]
C13 = ["u0", "u1"] + sorted(set(link(0) + link(1))) + ["r0", "r1"]
for nm, I in (("TC3_C13", C13), ("TC3_C14", C14), ("TC3_C18", C18)):
    print(window(nm, I))

# sub-windows of C13, to find the smallest reducible piece
subs = {
 "TC3_P11_u0u1_links": ["u0","u1"] + sorted(set(link(0)+link(1))),
 "TC3_P12_plus_r0": ["u0","u1"] + sorted(set(link(0)+link(1))) + ["r0"],
 "TC3_P12_plus_r1": ["u0","u1"] + sorted(set(link(0)+link(1))) + ["r1"],
 "TC3_P7_u0_link0_r0": ["u0"] + link(0) + ["r0"],
 "TC3_P10_u0_link0_r0_u1_b1c1d1": ["u0"] + link(0) + ["r0","u1","b1","c1","d1"],
 "TC3_P9_u0_link0_r0_b1c1": ["u0"] + link(0) + ["r0","b1","c1"],
 "TC3_P8_u0u1_link0_r0": ["u0","u1"] + link(0) + ["r0"],
}
for nm, I in subs.items():
    try:
        print(window(nm, I))
    except AssertionError as e:
        print(f"# {nm}: skipped ({e})", file=sys.stderr)
