#!/usr/bin/env python3
"""[exploratory] Local compute item 6, parts (4), (6), (7): raw labelled fractions, renaming stabilisers, and the
filled/unfilled structure of Kempe classes. Plain Python (../common/kempe_py.py), no team code.

(6) Raw labelled colourings. A canonical class C (states up to renaming) lifts to labelled colourings. For a labelled
    colouring c in the lift, its LABELLED Kempe class K is found two ways:
    - voltage method: BFS over C keeping one labelled representative per state; every move that lands on a known state
      gives a permutation sigma in S4 with c' = sigma o rep(t); these generate the stabiliser G = {pi : pi(K) = K};
    - explicit labelled BFS (no renaming at all), when |C| * 24 <= LAB_CAP: size and #filled of K counted directly.
    Raw fraction = #filled(K) / |K|. The number of labelled classes over C is 24 / |G|.
(4) For classes at exactly 1/4 (degree-5 holes): link colour patterns of the filled states (letters by first occurrence
    from link position 0, rotation order) and the position of the singleton colour.
(7) Bipartite graph inside a class between filled and unfilled states, using only swaps whose component meets the link in
    exactly ONE vertex ("single-link-vertex swaps"); edges counted between distinct states. Also counted: filled<->unfilled
    moves by any other swap (component meets the link in 0 or >= 2 vertices). Degree distributions of both sides, and
    whether the class splits into 4-sets {one filled state + 3 unfilled neighbours} (b-matching by max flow: each filled
    state takes exactly 3 unfilled neighbours, each unfilled state exactly 1 filled neighbour).
usage: quarter_struct.py --orders 12 ... 20 --degrees 5 6 7 > raw-12-20.jsonl        (6) on every class of every hole
       quarter_struct.py --quarter holes-*.jsonl > quarter-classes.jsonl              (4)(6)(7) on every 1/4 class"""
import json, os, sys, itertools
from collections import Counter, deque
from multiprocessing import Pool
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "common"))
from kempe_py import Space, gentri_rotation, adj_from_rot
GENTRI = os.path.join(H, "..", "..", "..", "studiointel", "gentri")
LAB_CAP = 400000
PERMS = list(itertools.permutations(range(4)))


def compose(a, b): return tuple(a[b[i]] for i in range(4))   # (a o b)(i) = a(b(i))


def closure(gens):
    G = {(0, 1, 2, 3)}; fr = list(G)
    while fr:
        nx = []
        for g in fr:
            for h in gens:
                k = compose(g, h)
                if k not in G: G.add(k); nx.append(k)
        fr = nx
    return G


def group_name(G):
    n = len(G)
    if n == 1: return "trivial"
    if n == 24: return "S4"
    if n == 12: return "A4"
    if n == 2: return "C2"
    if n == 3: return "C3"
    if n == 6: return "S3"
    if n == 8: return "D4"
    if n == 4:
        cyc = any(compose(g, g) != (0, 1, 2, 3) for g in G)
        if cyc: return "C4"
        fixed = [g for g in G if g != (0, 1, 2, 3)]
        return "V4(normal, double transpositions)" if all(sum(g[i] == i for i in range(4)) == 0 for g in fixed) else "V4(non-normal)"
    return "order%d" % n


def lab_moves(S, c):
    cm = [0, 0, 0, 0]
    for i, x in enumerate(c): cm[x] |= 1 << i
    out = []
    for p, q in itertools.combinations(range(4), 2):
        M = cm[p] | cm[q]
        while M:
            K = S.flood(M & -M, cm[p] | cm[q]); M &= ~K
            out.append((tuple((q if x == p else p) if K >> i & 1 else x for i, x in enumerate(c)), K))
    return out


def analyse_hole(rot, hole, want_quarter=False):
    adj = adj_from_rot(rot); S = Space(adj, hole, link=rot[hole]); S.build_graph(); cl, ncl = S.classes()
    filled = [S.filled(k) for k in range(len(S.states))]
    members = [[] for _ in range(ncl)]
    for s in range(len(S.states)): members[cl[s]].append(s)
    linkmask = sum(1 << i for i in S.linki); res = []
    for k in range(ncl):
        C = members[k]; nf = sum(filled[s] for s in C); s0 = C[0]
        # voltage method
        rep = {s0: S.states[s0]}; q = deque([s0]); gens = set()
        while q:
            s = q.popleft()
            for c2, K in lab_moves(S, rep[s]):
                t = S.index[S.canon(c2)]
                if t not in rep: rep[t] = c2; q.append(t)
                else:
                    r = rep[t]; sig = [None] * 4
                    for i in range(S.N): sig[r[i]] = c2[i]
                    if None in sig:  # a colour unused in r (cannot happen when every state uses 4 colours)
                        miss = [x for x in range(4) if x not in sig]; sig = [x if x is not None else miss.pop() for x in sig]
                    gens.add(tuple(sig))
        G = closure(gens)
        rec = {"size": len(C), "filled": nf, "stabiliser_order": len(G), "stabiliser": group_name(G),
               "labelled_classes_over_C": 24 // len(G), "raw_size_voltage": len(C) * len(G), "raw_filled_voltage": nf * len(G)}
        if len(C) * len(G) <= LAB_CAP:
            start = S.states[s0]; seen = {start}; q = deque([start]); fcount = 0
            while q:
                c = q.popleft(); fcount += len({c[i] for i in S.linki}) <= 3
                for c2, _ in lab_moves(S, c):
                    if c2 not in seen: seen.add(c2); q.append(c2)
            rec["raw_size_explicit"] = len(seen); rec["raw_filled_explicit"] = fcount
        if want_quarter and 4 * nf == len(C):
            rec.update(structure(S, C, filled, linkmask))
        res.append(rec)
    return res


def pattern(S, s):
    mp = {}; return "".join("abcd"[mp.setdefault(S.states[s][i], len(mp))] for i in S.linki)


def structure(S, C, filled, linkmask):
    Cset = set(C); F = [s for s in C if filled[s]]; U = [s for s in C if not filled[s]]
    pats = Counter(pattern(S, s) for s in F); upats = Counter(pattern(S, s) for s in U)
    single = Counter()
    for s in F:
        cols = [S.states[s][i] for i in S.linki]
        single[[i for i in range(len(cols)) if cols.count(cols[i]) == 1][0] if len(S.linki) == 5 else -1] += 1
    nb = {s: set() for s in C}; other = 0; kinds = Counter()
    for s in F:
        for t, p, q, K in S.moves(s):
            if t == s or filled[t]: continue
            nl = bin(K & linkmask).count("1"); kinds[nl] += 1
            if nl == 1: nb[s].add(t); nb[t].add(s)
            else: other += 1
    fdeg = Counter(len(nb[s]) for s in F); udeg = Counter(len(nb[s]) for s in U)
    # b-matching: source -> filled (cap 3) -> unfilled (cap 1) -> sink
    match = {}; load = Counter()

    def aug(u, seen):
        for f in nb[u]:
            if f in seen: continue
            seen.add(f)
            if load[f] < 3: match[u] = f; load[f] += 1; return True
            for u2 in [x for x, y in match.items() if y == f]:
                if aug(u2, seen): match[u] = f; return True
        return False
    for u in U: aug(u, set())
    return {"filled_link_patterns": dict(pats), "unfilled_link_patterns": dict(upats),
            "singleton_position_counts": {str(k): v for k, v in sorted(single.items())},
            "filled_to_unfilled_moves_by_link_vertices_in_component": {str(k): v for k, v in sorted(kinds.items())},
            "filled_to_unfilled_moves_not_single_link": other,
            "bipartite_filled_degree_dist": {str(k): v for k, v in sorted(fdeg.items())},
            "bipartite_unfilled_degree_dist": {str(k): v for k, v in sorted(udeg.items())},
            "four_set_decomposition_exists": len(match) == len(U) and 3 * len(F) == len(U)}


def work_hole(t):
    n, gi, line, v, wq = t
    rot = gentri_rotation(line)
    return {"order": n, "gentri_index": gi, "hole": v, "deg": len(rot[v]), "classes": analyse_hole(rot, v, wq)}


def main():
    tasks = []
    if "--quarter" in sys.argv:
        seen = set(); lines = {}
        for fn in sys.argv[sys.argv.index("--quarter") + 1:]:
            for l in open(fn):
                r = json.loads(l)
                if any(4 * f == s for s, f in r["classes"]):
                    key = (r["order"], r["gentri_index"], r["hole"])
                    if key in seen: continue
                    seen.add(key)
                    if r["order"] not in lines: lines[r["order"]] = [x for x in open(os.path.join(GENTRI, "tri%d.txt" % r["order"])) if x.strip()]
                    tasks.append((r["order"], r["gentri_index"], lines[r["order"]][r["gentri_index"]], r["hole"], True))
    else:
        i = sys.argv.index("--orders") + 1; orders = []
        while i < len(sys.argv) and not sys.argv[i].startswith("--"): orders.append(int(sys.argv[i])); i += 1
        i = sys.argv.index("--degrees") + 1; degs = set()
        while i < len(sys.argv) and not sys.argv[i].startswith("--"): degs.add(int(sys.argv[i])); i += 1
        for n in orders:
            for gi, l in enumerate(x for x in open(os.path.join(GENTRI, "tri%d.txt" % n)) if x.strip()):
                rot = gentri_rotation(l)
                tasks += [(n, gi, l, v, False) for v in range(len(rot)) if len(rot[v]) in degs]
    with Pool(6) as pool:
        for r in pool.imap(work_hole, tasks, chunksize=2): print(json.dumps(r), flush=True)


if __name__ == "__main__":
    main()
