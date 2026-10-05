"""Structural analysis of the two saved WP19 counterexamples 24:6406 (m = 3) and 24:7228
(ell = 3, kappa = 5 at v = 17, fan 0).

Long Table, 5 October 2026. Descriptive analysis of saved graphs only: no new graph, order or
census is run, and no bound is fitted. Inputs:
  * ../audit/wp19-counterexamples.json  (both graph records, as extracted by Math)
  * wp19-P3.json                         (read only to look up the saved m of the order-24
                                          graphs reached by a single edge flip of the two graphs)
  * ../wp18/wp18-P1.json                 (rotation of 17:1, for comparison)
Output: counterexample-analysis.txt (this script's stdout).

Sections
  A  24:6406 structure: degrees, automorphisms, orbits, axis edges, flips, common patch with 17:1
  B  24:6406 far diagonals D_far(v) per degree-5 vertex; diagonal reduction checked against the
     saved pair maxima; census of all far (ell >= 3) colourings; role of the degree-7 vertices
  C  24:6406 hand certificate: two crossing far colourings at v = 4 (and 19 by Aut)
  D  24:7228 at v = 17: chains, Kempe class layers, lifted paths, the bridge vertex 8
  E  length-3 reduction lemma (hand proof in the .md): every ell = 3 start with kappa > 3 has
     only slide-first shortest paths whose next swap must use the slid colour; checked on both graphs
"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "wp18"))
sys.path.insert(0, str(HERE))
from analysis_17_1 import (automorphisms, canon_form, components, diag, flip, one_move_report,  # noqa: E402
                           path_between, shape, star, validate)
from wp18_core import HOLE, PAIRS, canon, filled, legal_fans, moves, parse_ascii  # noqa: E402
import wp19_core as W  # noqa: E402

GUARD = W.Guard(None, None)
CE = json.load(open(HERE.parent / "audit" / "wp19-counterexamples.json"))
REC = {g["graph_index"]: g for g in CE["graphs"]}


def load_17_1():
    s = open(HERE.parent / "wp18" / "wp18-P1.json").read()
    m = re.search(r'"order": ?17, ?"graph_index": ?1, ?"ascii": ?"([^"]+)"', s)
    return m.group(1)


def all_states(rot):
    return {h: W.deletion_states(rot, h, GUARD) for h in range(len(rot))}


def orbits_of(aut, n):
    out, seen = [], set()
    for v in range(n):
        if v not in seen:
            orb = sorted({g[v] for g, _ in aut})
            seen |= set(orb)
            out.append(orb)
    return out


def separating_triangles(rot):
    n = len(rot)
    faces = set()
    for a in range(n):
        d = len(rot[a])
        for k in range(d):
            faces.add(frozenset((a, rot[a][k], rot[a][(k + 1) % d])))
    tri = set()
    for a in range(n):
        for b in rot[a]:
            for c in rot[b]:
                if c in rot[a] and len({a, b, c}) == 3:
                    t = frozenset((a, b, c))
                    if t not in faces:
                        tri.add(tuple(sorted(t)))
    return sorted(tri)


def patch(G, H, v, w, o, v2, w2):
    """Grow an orientation-(o) map of rotation systems from flag (v,w)->(v2,w2); a vertex is
    interior when its degree agrees and its whole link maps consistently."""
    f, inv, ref = {v: v2, w: w2}, {v2: v, w2: w}, {v: w, w: v}
    interior, q, seen = set(), [v], {v}
    while q:
        a = q.pop(0)
        a2 = f[a]
        if len(G[a]) != len(H[a2]):
            continue
        d = len(G[a])
        i, j = G[a].index(ref[a]), H[a2].index(f[ref[a]])
        new, ok = [], True
        for k in range(d):
            x, y = G[a][(i + k) % d], H[a2][(j + o * k) % d]
            if (x in f and f[x] != y) or (y in inv and inv[y] != x):
                ok = False
                break
            new.append((x, y))
        if not ok:
            continue
        for x, y in new:
            if x not in f:
                f[x], inv[y], ref[x] = y, x, a
            if x not in seen:
                seen.add(x)
                q.append(x)
        interior.add(a)
    return interior, f


def p3_flip_lookup(rot):
    """Flip every edge keeping minimum degree 5; identify the result among saved P3 graphs."""
    s = open(HERE / "wp19-P3.json").read()
    asc = re.findall(r'"order":24,"graph_index":(\d+),"ascii":"([^"]+)"', s)
    ms = re.findall(r'\],"m":(\w+),"m_at_least"', s)
    assert len(asc) == len(ms) == 7290
    recs = {int(i): (a, m) for (i, a), m in zip(asc, ms)}
    del s
    cache = {}
    out = []
    for a in range(len(rot)):
        for b in rot[a]:
            if a >= b:
                continue
            nr = flip(rot, a, b)
            if nr is None or min(map(len, nr)) < 5:
                continue
            validate(nr)
            ds = tuple(sorted(map(len, nr)))
            if ds not in cache:
                cache[ds] = {}
                for k, (asc_k, _) in recs.items():
                    r = parse_ascii(asc_k)
                    if tuple(sorted(map(len, r))) == ds:
                        cache[ds].setdefault(canon_form(r), []).append(k)
            hit = cache[ds].get(canon_form(nr), [])
            out.append(((a, b), hit, [recs[h][1] for h in hit], dict(sorted(collections.Counter(ds).items()))))
    return out


def lift(rot, st, mv):
    """Apply a canonical-label move to an actual colouring; return new colouring and description."""
    cs = canon(st)
    m = {y: x for x, y in zip(st, cs) if x != HOLE}
    if mv[0] == "S":
        h, u = st.index(HOLE), mv[1]
        nx = list(st)
        nx[h], nx[u] = st[u], HOLE
        return tuple(nx), f"slide {h}->{u} carrying colour {st[u]}"
    a, b, seed = m[mv[1]], m[mv[2]], mv[3]
    K, stack = {seed}, [seed]
    while stack:
        x = stack.pop()
        for y in rot[x]:
            if y not in K and st[y] in (a, b):
                K.add(y)
                stack.append(y)
    nx = list(st)
    for x in K:
        nx[x] = b if st[x] == a else a
    return tuple(nx), f"swap {{{a},{b}}} on {sorted(K)}"


def show_link(rot, st):
    h = st.index(HOLE)
    return f"hole {h} (deg {len(rot[h])}) link {rot[h]} colours {[st[w] for w in rot[h]]}"


def certificate(rot, X, ld, label):
    """Section-4-style certificate that ell(X) >= 3, with a shortest path giving ell(X) = 3."""
    print(f"\n--- certificate {label}: X = {list(X)}")
    print("  ", show_link(rot, X), "; monochromatic diagonal",
          [rot[X.index(HOLE)][i] for i in diag(rot, X.index(HOLE), X)])
    v = X.index(HOLE)
    print("   fans for which X is a start:",
          [i for i, c1, c2 in legal_fans(rot, v) if X[c1[0]] != X[c1[1]] and X[c2[0]] != X[c2[1]]])
    print("   Kempe components of X in T - hole:")
    for a, b in PAIRS:
        print(f"     {{{a},{b}}}: {components(rot, X, a, b)}")
    fills, lines = one_move_report(rot, X)
    assert not fills
    print("   X itself has no filling move (ell >= 2):")
    print("\n".join("   " + s for s in lines))
    nb = {}
    for mv, y in moves(rot, X):
        if y != X:
            nb.setdefault(y, []).append(mv)
    print(f"   X has {len(nb)} distinct neighbours; none has a filling move (ell >= 3):")
    for k, (Y, mvs) in enumerate(nb.items(), 1):
        fills, lines = one_move_report(rot, Y)
        assert not fills
        _, desc = lift(rot, X, mvs[0])
        print(f"   Y{k} via {mvs} = {desc}; {show_link(rot, Y)}; ell(Y{k}) = {ld[Y]}")
        print(f"     Y{k} = {list(Y)}")
        print("\n".join("   " + s for s in lines))
    assert ld[X] == 3
    p = W.path_to_fill(rot, X, ld)
    st = X
    print("   ell(X) = 3; a shortest fill (canonical labels, then actual colours):", p)
    for mv in p:
        st, desc = lift(rot, st, mv)
        print("     ", desc, "->", show_link(rot, st), "filled" if filled(rot, st) else "")


def far_census(rot, sbh, ld, kd_by_v):
    deg = [len(r) for r in rot]
    rows = []
    for v in range(len(rot)):
        if deg[v] != 5:
            continue
        for s in sbh[v]:
            if ld[s] < 3:
                continue
            lk = rot[v]
            p = diag(rot, v, s)[0]
            b, g, d = lk[(p + 1) % 5], lk[(p + 3) % 5], lk[(p + 4) % 5]
            P = path_between(rot, s, s[b], s[g], b, g)
            Q = path_between(rot, s, s[b], s[d], b, d)
            nb = {y for _, y in moves(rot, s) if y != s}
            conn = sum(len(components(rot, s, x, y)) == 1 for x, y in PAIRS)
            rows.append(dict(v=v, s=s, ell=ld[s], kappa=kd_by_v[v].get(s), b=b, g=g, d=d,
                             P=P, Q=Q, nbrs=len(nb), conn=conn))
    return rows


def length3_reduction_check(rot, sbh, ld, kd_by_v, label):
    """For every ell = 3 start (4-colour link, degree-5 hole) with kappa > 3: every first move of
    a shortest mixed path is a slide h->u, and every first swap of a 2-swap Kempe fill at u of the
    slid state uses the slid colour."""
    deg = [len(r) for r in rot]
    kd_hole = {}
    nbset = [set(r) for r in rot]
    tested = viol = 0
    for v in range(len(rot)):
        if deg[v] != 5:
            continue
        for s in sbh[v]:
            if ld[s] != 3 or kd_by_v[v].get(s) == 3:
                continue
            tested += 1
            firsts = [(mv, y) for mv, y in moves(rot, s) if ld.get(y) == 2]
            for mv, t in firsts:
                if mv[0] != "S":
                    viol += 1
                    print("   VIOLATION: Kempe first move", mv, s)
                    continue
                u = mv[1]
                sigma = t[v]  # canonical label in t of the colour carried to the old hole
                if u not in kd_hole:
                    kd_hole[u] = W.kempe_distances(rot, u, sbh[u], GUARD)
                ku = kd_hole[u]
                assert ku.get(t) == 2, (s, u, ku.get(t))  # M3 at the intermediate hole
                fs = [m2 for m2, t2 in W.kempe_moves_nb(nbset, t) if ku.get(t2) == 1]
                bad = [m2 for m2 in fs if sigma not in (m2[1], m2[2])]
                if bad:
                    viol += 1
                    print("   VIOLATION: sigma-free first swap", bad, s)
            print(f"   v={v} ell=3 kappa={kd_by_v[v].get(s)} first moves "
                  f"{[m for m, _ in firsts]} start {list(s)}")
    print(f"  [{label}] ell = 3 starts with kappa > 3: {tested}; violations: {viol}")


def bridge_face_check(rot, sbh, ld, kd_by_v, label):
    """For every start (degree-5 hole) with kappa - ell >= 2: list every shortest mixed path of the
    form S K1 K2 (in actual colours) and report (i) whether the {sigma,rho}-component of T-h that
    contains K1 also contains u and a common neighbour w of h and u, and (ii) whether K2 contains h."""
    deg = [len(r) for r in rot]
    nbset = [set(r) for r in rot]
    found = 0
    for v in range(len(rot)):
        if deg[v] != 5:
            continue
        for s in sbh[v]:
            k = kd_by_v[v].get(s)
            if k is None or ld[s] is None or k - ld[s] < 2:
                continue
            found += 1
            print(f"  v={v} ell={ld[s]} kappa={k} start {list(s)}")
            for mv, t in moves(rot, s):
                if ld.get(t) != ld[s] - 1 or mv[0] != "S":
                    continue
                u = mv[1]
                sig = s[u]
                t_act, _ = lift(rot, s, mv)
                for m1, t1 in W.kempe_moves_nb(nbset, canon(t_act)):
                    if ld.get(t1) != ld[s] - 2:
                        continue
                    t1_act, d1 = lift(rot, t_act, m1)
                    K1 = [x for x in range(len(rot)) if t1_act[x] != t_act[x]]
                    a, b = sorted({t_act[x] for x in K1})
                    big = next(c for c in components(rot, s, a, b) if K1[0] in c)
                    common = sorted(set(rot[v]) & set(rot[u]))
                    for m2, t2 in W.kempe_moves_nb(nbset, canon(t1_act)):
                        if ld.get(t2) != 0:
                            continue
                        t2_act, d2 = lift(rot, t1_act, m2)
                        K2 = [x for x in range(len(rot)) if t2_act[x] != t1_act[x]]
                        print(f"    S{u} (sigma={sig}); K1 {d1}; K1 lifted to T-{v} = {sorted(big)} "
                              f"contains u: {u in big}, face-neighbours of h,u {common} inside: "
                              f"{[w for w in common if w in big]}; sigma in K1 pair: {sig in (a, b)}; "
                              f"K2 {d2}; K2 contains h: {v in K2}")
    print(f"  [{label}] starts with kappa - ell >= 2: {found}")


# ====================================================================================== main

def part_6406():
    g = REC[6406]
    asc = g["ascii"]
    assert hashlib.sha256(asc.encode()).hexdigest() == g["ascii_sha256"]
    rot = parse_ascii(asc)
    validate(rot)
    n = len(rot)
    deg = [len(r) for r in rot]
    print("=== A. 24:6406 structure ===")
    print("ascii:", asc)
    print("degree histogram:", dict(sorted(collections.Counter(deg).items())),
          "; degree-7:", [v for v in range(n) if deg[v] == 7])
    for v in range(n):
        print(f"  v={v:2d} deg {deg[v]} link {rot[v]} link degrees {[deg[w] for w in rot[v]]}")
    hi = [v for v in range(n) if deg[v] >= 6]
    print("degree>=6 vertices:", hi, "edges among them:",
          [(a, b) for a in hi for b in rot[a] if b in hi and a < b])
    print("separating triangles:", separating_triangles(rot))
    aut = automorphisms(rot)
    print("|Aut| =", len(aut))
    for p, o in aut:
        fixed = [x for x in range(n) if p[x] == x]
        swapped_edges = sorted({tuple(sorted((x, p[x]))) for x in range(n) if p[x] != x and p[x] in rot[x]})
        print(f"  {p} orient {o:+d} fixed vertices {fixed} edges reversed {swapped_edges}")
    print("vertex orbits:", orbits_of(aut, n))
    d5 = [v for v in range(n) if deg[v] == 5]
    print("degree-5 orbits:", [o for o in orbits_of(aut, n) if deg[o[0]] == 5])
    print("degree-5 vertices adjacent to a degree-7 vertex:",
          [v for v in d5 if any(deg[w] == 7 for w in rot[v])])
    print("distance between 1 and 21: path 1-2-11-21 (2 adj 1:", 2 in rot[1], "; 11 adj 2:", 11 in rot[2],
          "; 21 adj 11:", 21 in rot[11], "; 1 adj 21:", 21 in rot[1], "; common nbrs:",
          sorted(set(rot[1]) & set(rot[21])), ")")
    print("legal fans: every degree-5 vertex has all five:",
          all(len(legal_fans(rot, v)) == 5 for v in d5), "; total", sum(len(legal_fans(rot, v)) for v in d5))
    print("\nFlips of 24:6406 keeping minimum degree 5, identified among saved P3 graphs (saved m):")
    for (a, b), hit, ms, ds in p3_flip_lookup(rot):
        print(f"  flip {a}-{b} (degrees {deg[a]},{deg[b]}) -> 24:{hit} m={ms} degrees {ds}")
    asc171 = load_17_1()
    H = parse_ascii(asc171)
    hdeg = [len(r) for r in H]
    a171 = automorphisms(H)
    print("\n17:1 for comparison:", asc171)
    for p, o in a171:
        if o == 1 and p != tuple(range(17)):
            print("  17:1 half-turn", p, "fixed", [x for x in range(17) if p[x] == x],
                  "edges reversed", sorted({tuple(sorted((x, p[x]))) for x in range(17) if p[x] != x and p[x] in H[x]}))
    print("  17:1 degree-6 vertices:", [v for v in range(17) if hdeg[v] == 6])
    best = []
    for v in range(n):
        for w in rot[v]:
            for v2 in range(17):
                for w2 in H[v2]:
                    for o in (1, -1):
                        I, f = patch(rot, H, v, w, o, v2, w2)
                        best.append((len(I), sorted(I), {x: f[x] for x in sorted(I)}))
    best.sort(key=lambda t: -t[0])
    print("largest flag-grown common patch with 17:1 (interior vertices with matching full links):",
          best[0][0], best[0][1], "map", best[0][2])
    print("  distinct interior sets of that size:", sorted({tuple(b[1]) for b in best if b[0] == best[0][0]}))

    print("\n=== B. 24:6406 far diagonals ===")
    sbh = all_states(rot)
    ld = W.mixed_distances(rot, sbh, GUARD)
    kd_by_v = {v: W.kempe_distances(rot, v, sbh[v], GUARD) for v in d5}
    saved = {(P["v"], P["fan_index"]): P["L"] for P in g["pairs"]}
    mism = 0
    print("columns: v, orbit partner, #deg>=6 nbrs, #deg-7 nbrs, link, D_far as link-vertex pairs "
          "(* = carries ell=4), shape, L per fan via diagonal reduction, ell-histogram per diagonal")
    sigma = [p for p, o in aut if p != tuple(range(n))][0]
    for v in d5:
        byd = collections.defaultdict(list)
        for s in sbh[v]:
            byd[diag(rot, v, s)].append(ld[s])
        dfar = sorted(d for d, ls in byd.items() if d and max(ls) >= 3)
        Ls = []
        for i in range(5):
            L = max(l for d, ls in byd.items() for l in ls if d is None or d not in star(i))
            Ls.append(L)
            mism += L != saved[(v, i)]
        lk = rot[v]
        lab = [f"{lk[a]}-{lk[b]}{'*' if max(byd[(a, b)]) >= 4 else ''}" for a, b in dfar]
        hist = {f"{lk[d[0]]}-{lk[d[1]]}" if d else "3col": dict(sorted(collections.Counter(ls).items()))
                for d, ls in sorted(byd.items(), key=lambda t: (t[0] is not None, t[0]))}
        print(f"  v={v:2d} ~{sigma[v]:2d} hi={sum(deg[w] >= 6 for w in lk)} d7={sum(deg[w] == 7 for w in lk)} "
              f"link {lk} D_far {dfar}={lab} [{shape(dfar)}] L={Ls}")
        print(f"        {hist}")
    print("diagonal-reduction L vs saved P3 pair L: mismatches", mism, "of", len(saved))

    rows = far_census(rot, sbh, ld, kd_by_v)
    print(f"\nall far colourings (ell >= 3) at degree-5 holes: {len(rows)} "
          f"(ell=3: {sum(r['ell'] == 3 for r in rows)}, ell=4: {sum(r['ell'] == 4 for r in rows)})")
    print("  (ell, kappa) counts:", dict(collections.Counter((r["ell"], r["kappa"]) for r in rows)))
    print("  middle b has degree:", dict(collections.Counter(deg[r["b"]] for r in rows)))
    print("  some link vertex has degree 7:", sum(any(deg[w] == 7 for w in rot[r["v"]]) for r in rows))
    print("  chosen shortest P or Q passes through 1 or 21:",
          sum(bool(({1, 21} & set(r["P"])) | ({1, 21} & set(r["Q"]))) for r in rows))
    print("  number of connected bichromatic pairs:", dict(collections.Counter(r["conn"] for r in rows)),
          "; distinct neighbours:", dict(collections.Counter(r["nbrs"] for r in rows)))
    for r in rows:
        if r["ell"] == 4:
            print(f"  ell=4 at v={r['v']}: b={r['b']}(deg {deg[r['b']]}) g={r['g']} d={r['d']} P={r['P']} "
                  f"Q={r['Q']} start {list(r['s'])}")

    print("\n=== C. 24:6406 hand certificate at v = 4 ===")
    v = 4
    print("link of 4:", rot[v], "; fan chords: tau_i = {(i,i+2),(i,i+3)};",
          "legality = the five diagonals are non-edges:",
          [(rot[v][i], rot[v][(i + 2) % 5], rot[v][(i + 2) % 5] in rot[rot[v][i]]) for i in range(5)])
    X1 = (0, 1, 2, 1, 4, 3, 2, 3, 2, 0, 1, 3, 0, 2, 1, 0, 1, 0, 3, 2, 0, 2, 3, 3)
    X2 = (0, 1, 2, 3, 4, 2, 3, 0, 3, 0, 3, 1, 2, 0, 1, 2, 1, 2, 1, 0, 2, 0, 3, 3)
    for X in (X1, X2):
        assert X in set(sbh[v]) and all(X[a] != X[b] for a in range(n) for b in rot[a] if HOLE not in (X[a], X[b]))
    far4 = [s for s in sbh[v] if ld[s] >= 3]
    print("all far colourings at 4:", [(list(s), [rot[v][i] for i in diag(rot, v, s)], ld[s]) for s in far4])
    certificate(rot, X1, ld, "X1 (diagonal 3-14)")
    certificate(rot, X2, ld, "X2 (diagonal 0-13)")
    for X, nm in ((X1, "X1"), (X2, "X2")):
        img = [None] * n
        for x, c in enumerate(X):
            img[sigma[x]] = c
        img = canon(img)
        print(f"  sigma({nm}) at hole 19: diagonal {[rot[19][i] for i in diag(rot, 19, img)]}, ell {ld[img]}")
    return rot, sbh, ld, kd_by_v


def part_7228():
    g = REC[7228]
    asc = g["ascii"]
    assert hashlib.sha256(asc.encode()).hexdigest() == g["ascii_sha256"]
    rot = parse_ascii(asc)
    validate(rot)
    n = len(rot)
    deg = [len(r) for r in rot]
    print("\n=== D. 24:7228 at v = 17, fan 0 ===")
    print("ascii:", asc)
    print("degree histogram:", dict(sorted(collections.Counter(deg).items())),
          "; degree>=7:", [(v, deg[v]) for v in range(n) if deg[v] >= 7])
    for v in range(n):
        print(f"  v={v:2d} deg {deg[v]} link {rot[v]} link degrees {[deg[w] for w in rot[v]]}")
    print("|Aut| =", len(automorphisms(rot)))
    v = 17
    S = (0, 1, 2, 3, 1, 2, 0, 3, 2, 3, 1, 2, 3, 0, 3, 2, 1, 4, 1, 0, 2, 1, 3, 0)
    lk = rot[v]
    print("start", list(S), ";", show_link(rot, S))
    p = diag(rot, v, S)[0]
    a0, b, a2, gg, dd = (lk[(p + k) % 5] for k in range(5))
    al, be, ga, de = S[a0], S[b], S[gg], S[dd]
    print(f"roles a0={a0} b={b} a2={a2} g={gg} d={dd}; colours alpha={al} beta={be} gamma={ga} delta={de}")
    print("Kempe components in T-17:")
    for x, y in PAIRS:
        print(f"  {{{x},{y}}}: {components(rot, S, x, y)}")
    P = path_between(rot, S, be, ga, b, gg)
    Q = path_between(rot, S, be, de, b, dd)
    C0 = next(c for c in components(rot, S, al, ga) if a0 in c)
    D2 = next(c for c in components(rot, S, al, de) if a2 in c)
    print(f"P (beta-gamma, b-g) = {P}; Q (beta-delta, b-d) = {Q}")
    print(f"C0 (alpha-gamma at a0) = {C0}, meets P at {sorted(set(C0) & set(P))}; "
          f"D2 (alpha-delta at a2) = {D2}, meets Q at {sorted(set(D2) & set(Q))}")
    fills, lines = one_move_report(rot, S)
    print("one-move report at the start:")
    print("\n".join(lines))

    sbh = all_states(rot)
    ld = W.mixed_distances(rot, sbh, GUARD)
    kd = W.kempe_distances(rot, v, sbh[v], GUARD)
    print("ell =", ld[S], "; kappa =", kd[S])
    nbset = [set(r) for r in rot]
    dist, par, fr = {S: 0}, {S: None}, [S]
    layers = [[S]]
    while fr:
        nx = []
        for x in fr:
            for mv, y in W.kempe_moves_nb(nbset, x):
                if y not in dist:
                    dist[y], par[y] = dist[x] + 1, (x, mv)
                    nx.append(y)
        if nx:
            layers.append(nx)
        fr = nx
    print("Kempe class of the start at hole 17: size", len(dist), "layers", [len(L) for L in layers],
          "filled per layer", [sum(filled(rot, x) for x in L) for L in layers])
    print("per depth: states; gap (no one-move fill); one-swap-fillable; distinct Kempe moves that "
          "change vs keep the link colour partition; diagonals present")
    for d in range(6):
        L = layers[d]
        gap = sum(1 for x in L if not filled(rot, x) and kd.get(x) != 1)
        one = sum(1 for x in L if kd.get(x) == 1)
        touch = inter = 0
        for x in L:
            seen = set()
            for mv, y in W.kempe_moves_nb(nbset, x):
                if y == x or y in seen:
                    continue
                seen.add(y)
                if canon([x[w] for w in lk]) == canon([y[w] for w in lk]):  # same link partition
                    inter += 1
                else:
                    touch += 1
        dg = collections.Counter(tuple(lk[i] for i in diag(rot, v, x)) for x in L if not filled(rot, x))
        print(f"  depth {d}: {len(L)} states; gap {gap}; one-swap-fillable {one}; "
              f"moves partition-changing {touch}, partition-keeping {inter}; diagonals {dict(dg)}")
    print("distinct Kempe neighbours of the start:")
    seen = set()
    for mv, y in W.kempe_moves_nb(nbset, S):
        if y != S and y not in seen:
            seen.add(y)
            _, desc = lift(rot, S, mv)
            print(f"  {mv}: {desc}; link colours {[y[w] for w in lk]}")
    print("pairs connected at the start (swap = global renaming):",
          [pr for pr in PAIRS if len(components(rot, S, *pr)) == 1])
    for name, path in (("mixed", g_path(g, "mixed")), ("kempe", g_path(g, "kempe"))):
        print(f"{name} path lifted to actual colours:")
        st = S
        for mv in path:
            st, desc = lift(rot, st, mv)
            print(f"  {mv}: {desc} -> {show_link(rot, st)}{' FILLED' if filled(rot, st) else ''}")
    st8, _ = lift(rot, S, ("S", 8))
    print("Kempe components after the slide (T-8):")
    for x, y in PAIRS:
        print(f"  {{{x},{y}}}: {components(rot, st8, x, y)}")
    print("one-move report at hole 8:")
    print("\n".join(one_move_report(rot, st8)[1]))
    print("bridge check: {1,2}-component of vertex 5 in T-17 =",
          next(c for c in components(rot, S, 1, 2) if 5 in c),
          "; in T-8 =", next(c for c in components(rot, st8, 1, 2) if 5 in c))
    print("vertex 8 neighbours with colours (start):", [(w, S[w]) for w in rot[8]])
    print("P passes through", [x for x in P if S[x] == 2 and x != gg], "(gamma=2 interior vertices); "
          "{1,2}-swap at vertex 5 cuts P at 5")
    # all shortest mixed paths
    print("first moves of shortest mixed paths from the start:",
          [(mv, ld[y]) for mv, y in moves(rot, S) if ld.get(y) == 2])
    k8 = W.kempe_distances(rot, 8, sbh[8], GUARD)
    print("Kempe distance at hole 8 of the slid state:", k8.get(canon(st8)))
    print("2-swap Kempe fills at hole 8 (first swaps):",
          [(m2, lift(rot, st8, m2)[1]) for m2, t2 in W.kempe_moves_nb(nbset, canon(st8)) if k8.get(t2) == 1])
    return rot, sbh, ld, {v: kd, **{u: W.kempe_distances(rot, u, sbh[u], GUARD)
                                    for u in range(n) if deg[u] == 5 and u != v}}


def g_path(g, which):
    named = json.load(open(HERE.parent / "audit" / "wp19-named-kills-results.json"))["24:7228"]
    return [tuple(m) for m in named["mixed_path" if which == "mixed" else "kempe_path"]]


def main():
    print("inputs: wp19-counterexamples.json sha256",
          hashlib.sha256(open(HERE.parent / "audit" / "wp19-counterexamples.json", "rb").read()).hexdigest())
    r1, s1, l1, k1 = part_6406()
    r2, s2, l2, k2 = part_7228()
    print("\n=== E. Length-3 reduction lemma, checked on both saved graphs ===")
    length3_reduction_check(r1, s1, l1, k1, "24:6406")
    length3_reduction_check(r2, s2, l2, k2, "24:7228")
    print("\n=== F. Bridge-face pattern at every start with kappa - ell >= 2 (both saved graphs) ===")
    bridge_face_check(r1, s1, l1, k1, "24:6406")
    bridge_face_check(r2, s2, l2, k2, "24:7228")


if __name__ == "__main__":
    main()
