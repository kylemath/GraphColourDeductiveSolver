#!/usr/bin/env python3
"""[exploratory] Local compute item 3: inert-disc moves under lock-path quantifiers (plain Python, no team code imported).

Frame (Intern A, InternA-inert-disc.md): link x0..x4 in rotation order at hole v; unfilled state; repeat c(x_j) = c(x_{j+2});
m = x_{j+1}, a = x_{j+3}, b = x_{j+4}, mu = c(m). K1 = {mu, c(a)}-component of m, K2 = {mu, c(b)}-component of m.
DL iff a in K1 and b in K2. A lock-1 path is a SIMPLE path m ~ a inside K1 (lock-2: m ~ b inside K2).
For a lock path P, J(P) = v + P is a cycle of T. Its two sides are found GEOMETRICALLY from the rotation system (edges at each
cycle vertex are split by the two cycle edges; BFS in T - J from each side's seeds), so chords of J are handled.
D1(P) = side of J(P) containing x_{j+2}; D2(P) = side containing x_j.
Moves checked: from every DL state s, every swap s -> t with dist(t) = dist(s) - 1 (a first move of a shortest filling
sequence from s), swapped component K, K containing no link vertex. Counted:
 - Qall  (coordinator): K disjoint from K1 and K2, and for lock i = 1 or 2, K inside D_i(P) for EVERY simple lock-i path P;
 - Qall_A (Intern A's cycle-6 form): for i = 1 or 2, for every simple lock-i path P: K disjoint from P and K inside D_i(P);
 - Qchain: K disjoint from K_i and K inside the component of T - v - K_i that contains x_{j+2} (i = 1) or x_j (i = 2);
 - Qexists_shortest: K disjoint from K1, K2 and inside D_i(P) for SOME shortest lock-i path (Studio's inertdisc_a.py setting);
 - Qexists_simple: same with some simple lock path.
Hole orbits under the map's automorphisms (both orientations) are found by canonical BFS codes; one hole per orbit is scanned.
usage: qall_scan.py --orders 17 18 19 20      (graph lists: studiointel/gentri/triN.txt)
       qall_scan.py --plantri "LINE" HOLE [--colouring JSON]   (single hole; with a colouring, a full replay of that state)"""
import json, os, sys, itertools
from collections import Counter, deque
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, plantri_ascii, gentri_rotation, adj_from_rot
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")


def dart_code(rot, u, w, sgn):
    """BFS code of the map from dart u->w, orientation sgn (+1 as given, -1 mirrored)."""
    pos = [{x: i for i, x in enumerate(r)} for r in rot]
    num = {u: 0}; q = [(u, w)]; code = []
    for (x, first) in q:
        r = rot[x]; k = len(r); i0 = pos[x][first]
        for t in range(k):
            y = r[(i0 + sgn * t) % k]
            if y not in num: num[y] = len(num); q.append((y, x))
            code.append(num[y])
        code.append(-1)
    return tuple(code)


def vertex_orbits(rot):
    codes = {u: min(dart_code(rot, u, w, s) for w in rot[u] for s in (1, -1)) for u in range(len(rot))}
    orb = {}
    for u in range(len(rot)): orb.setdefault(codes[u], []).append(u)
    return list(orb.values()), min(codes.values())


def simple_paths(Kset, A, s, t, cap=200000):
    out = []; path = [s]; on = {s}

    def dfs(x):
        if len(out) >= cap: return
        if x == t: out.append(list(path)); return
        for y in A[x]:
            if y in Kset and y not in on:
                on.add(y); path.append(y); dfs(y); path.pop(); on.discard(y)
    dfs(s)
    return out, len(out) >= cap


def sides(rot, adj, cyc):
    """cyc: list of vertices of a cycle (in order). Returns (left, right) vertex sets of T - cyc (geometric sides)."""
    C = set(cyc); k = len(cyc); seeds = (set(), set())
    for i, x in enumerate(cyc):
        prv, nxt = cyc[i - 1], cyc[(i + 1) % k]; r = rot[x]; d = len(r); i0 = r.index(nxt)
        side = 0
        for t in range(1, d):
            y = r[(i0 + t) % d]
            if y == prv: side = 1; continue
            if y not in C: seeds[side].add(y)
    res = []
    for sd in seeds:
        seen = set(sd); st = list(sd)
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in C and y not in seen: seen.add(y); st.append(y)
        res.append(seen)
    assert not (res[0] & res[1]), "sides overlap: not a plane cycle?"
    return res


def disc(rot, adj, cyc, ref):
    L, R = sides(rot, adj, cyc)
    return L if ref in L else R


def comp_avoiding(adj, start, banned):
    seen = {start}; st = [start]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in banned and y not in seen: seen.add(y); st.append(y)
    return seen


def scan_hole(rot, hole, want_state=None, examples_cap=3):
    adj = adj_from_rot(rot); link = list(rot[hole])
    S = Space(adj, hole, link=link); S.build_graph(); dist = S.dist_to_filled()
    A = {u: sorted(adj[u] - {hole}) for u in adj if u != hole}
    cnt = Counter(); ex = []; trunc = False
    ids = range(len(S.states)) if want_state is None else [want_state]
    detail = []
    for si in ids:
        if dist[si] <= 0: continue
        s = S.states[si]; c = {u: s[S.idx[u]] for u in S.order}; lc = [c[x] for x in link]
        if len(set(lc)) <= 3: continue
        j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
        xj, m, x2, a, b = (link[(j + t) % 5] for t in range(5))
        cm = S.cmasks(s)
        Km = {}
        for t in (a, b):
            M = cm[c[m]] | cm[c[t]]; Km[t] = set(S.mask_vertices(S.flood(1 << S.idx[m], M)))
        if a not in Km[a] or b not in Km[b]: continue  # not DL
        cnt["DL_states"] += 1
        lazy = {}

        def lockdata(i):
            if i in lazy: return lazy[i]
            tgt, ref = (a, x2) if i == 1 else (b, xj)
            P, tr = simple_paths(Km[tgt], A, m, tgt)
            dl = min(len(p) for p in P)
            D = [disc(rot, adj, [hole] + p, ref) for p in P]
            chainside = comp_avoiding({u: adj[u] for u in adj}, ref, Km[tgt] | {hole})
            lazy[i] = (P, D, dl, tr, chainside); return lazy[i]
        for t, p, q, K in S.moves(si):
            if t == si or dist[t] != dist[si] - 1: continue
            cnt["moves_checked"] += 1
            Kv = set(S.mask_vertices(K))
            if Kv & set(link): continue
            cnt["moves_offlink"] += 1
            off_chains = not (Kv & (Km[a] | Km[b]))
            flags = {}
            for i in (1, 2):
                P, D, dl, tr, chainside = lockdata(i); trunc |= tr
                inside = [Kv <= Di for Di in D]
                flags["Qall_L%d" % i] = off_chains and all(inside)
                flags["QallA_L%d" % i] = all(Kv <= Di and not (Kv & set(Pp)) for Pp, Di in zip(P, D))
                flags["Qchain_L%d" % i] = not (Kv & Km[a if i == 1 else b]) and Kv <= chainside
                flags["QexS_L%d" % i] = off_chains and any(ins for ins, Pp in zip(inside, P) if len(Pp) == dl)
                flags["Qex_L%d" % i] = off_chains and any(inside)
            for key in ("Qall", "QallA", "Qchain", "QexS", "Qex"):
                if flags[key + "_L1"] or flags[key + "_L2"]:
                    cnt[key] += 1; cnt["%s_dist%d_%s" % (key, dist[si], "L1" if flags[key + "_L1"] else "L2")] += 1
            if want_state is not None or ((flags["Qall_L1"] or flags["Qall_L2"] or flags["QallA_L1"] or flags["QallA_L2"]) and len(ex) < examples_cap):
                rec = {"state_dist": dist[si], "frame_j": j, "pair_colours": [p, q], "component": sorted(Kv),
                       "lock1_simple_paths": len(lockdata(1)[0]), "lock2_simple_paths": len(lockdata(2)[0]),
                       "inside_D1_per_lock1_path": [[Pp, Kv <= Di] for Pp, Di in zip(lockdata(1)[0], lockdata(1)[1])][:20],
                       "inside_D2_per_lock2_path": [[Pp, Kv <= Di] for Pp, Di in zip(lockdata(2)[0], lockdata(2)[1])][:20],
                       "image_dist": dist[t], "flags": flags}
                if want_state is None: rec["colouring"] = {str(u): c[u] for u in S.order}
                (detail if want_state is not None else ex).append(rec)
    return {"hole": hole, "states": len(S.states), "rho": max(dist), "counts": dict(cnt), "examples": ex, "detail": detail,
            "path_enum_truncated": trunc, "dist_of_state": dist[want_state] if want_state is not None else None}


def main():
    if sys.argv[1] == "--plantri":
        rot = plantri_ascii(sys.argv[2]); hole = int(sys.argv[3])
        if "--colouring" in sys.argv:
            col = {int(k): v for k, v in json.loads(sys.argv[sys.argv.index("--colouring") + 1]).items()}
            adj = adj_from_rot(rot); S = Space(adj, hole, link=rot[hole]); st = S.state_of(col)
            print(json.dumps(scan_hole(rot, hole, want_state=st), indent=1)); return
        print(json.dumps(scan_hole(rot, hole))); return
    orders = [int(x) for x in sys.argv[sys.argv.index("--orders") + 1:]]
    for n in orders:
        tot = Counter(); first = {}; holes = 0; trunc = False
        lines = [l for l in open(os.path.join(GENTRI, "tri%d.txt" % n)) if l.strip()]
        for gi, line in enumerate(lines):
            rot = gentri_rotation(line)
            orbs, _ = vertex_orbits(rot)
            for orb in orbs:
                h = min(orb)
                if len(rot[h]) != 5: continue
                holes += 1
                r = scan_hole(rot, h); trunc |= r["path_enum_truncated"]
                tot.update(r["counts"])
                for key in ("Qall", "QallA", "Qchain", "QexS", "Qex"):
                    if r["counts"].get(key) and key not in first:
                        first[key] = {"order": n, "gentri_index": gi, "plantri_ascii": to_ascii(rot), "hole": h, "orbit_size": len(orb)}
                        if key in ("Qall", "QallA") and r["examples"]: first[key]["example"] = r["examples"][0]
        print(json.dumps({"order": n, "graphs": len(lines), "deg5_hole_orbits": holes, "counts": dict(sorted(tot.items())),
                          "first": first, "path_enum_truncated": trunc}), flush=True)


def to_ascii(rot):
    return "%d %s" % (len(rot), ",".join("".join(chr(97 + w) for w in r) for r in rot))


if __name__ == "__main__":
    main()
