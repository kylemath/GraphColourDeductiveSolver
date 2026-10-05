"""Analysis of 17:1, the only graph with m(T) = 3 in WP18 (orders 12-22).

Descriptive analysis of 17:1 itself and of graphs already in the WP18 outputs. It runs no
new declared test and reads no graph outside wp18-P1..P4.json. Output: analysis-17-1.txt.

Sections
  A  structure of 17:1: degrees, automorphisms, stabilisers, flip neighbours 17:0 and 17:3
  B  the diagonal reduction: L(v, tau_i) = max ell over colourings of T-v whose monochromatic
     link diagonal is not at i; checked against every recorded row of P1-P4
  C  far diagonals D_far(v) (colourings with ell >= 3) at every degree-5 vertex of 17:1, 17:0,
     17:3 and 14:0; and the shape of D_far at every degree-5 vertex of all 961 graphs
  D  all ell = 3 starts at the L = 3 pairs of 17:1, up to automorphism
  E  certificate for the lemma: the start X at v = 7 has ell(X) = 3
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from wp18_core import HOLE, PAIRS, canon, deletion_states, legal_fans, moves, parse_ascii, shortest_fill  # noqa: E402

PHASES = ["P1", "P2", "P3", "P4"]


def load_all():
    out = {}
    for p in PHASES:
        d = json.load(open(HERE / f"wp18-{p}.json"))
        for g in d["graphs"]:
            out[(g["order"], g["graph_index"])] = g
    return out


# ---------------------------------------------------------------- automorphisms

def automorphisms(rot):
    """All automorphisms of the embedded triangulation, as (perm tuple, +1 preserving / -1 reversing)."""
    n = len(rot)
    deg = [len(r) for r in rot]
    u0, w0 = 0, rot[0][0]
    res = []
    for u in range(n):
        if deg[u] != deg[u0]:
            continue
        for w in rot[u]:
            for o in (1, -1):
                f = {u0: u, w0: w}
                ok = True
                queue = [(u0, w0, u, w)]
                done = set()
                while queue and ok:
                    a, b, a2, b2 = queue.pop()
                    if a in done:
                        continue
                    done.add(a)
                    if deg[a] != deg[a2]:
                        ok = False
                        break
                    i, j, d = rot[a].index(b), rot[a2].index(b2), deg[a]
                    for k in range(d):
                        x, y = rot[a][(i + k) % d], rot[a2][(j + o * k) % d]
                        if x in f and f[x] != y:
                            ok = False
                            break
                        f[x] = y
                        if x not in done:
                            queue.append((x, a, y, a2))
                if ok and len(f) == n and len(set(f.values())) == n:
                    res.append((tuple(f[i] for i in range(n)), o))
    return res


def canon_form(rot):
    n = len(rot)
    best = None
    for u in range(n):
        for w in rot[u]:
            for o in (1, -1):
                lab, order, first = {u: 0}, [u], {u: w}
                code = []
                i = 0
                while i < len(order):
                    x = order[i]
                    d = len(rot[x])
                    j = rot[x].index(first[x])
                    row = []
                    for k in range(d):
                        z = rot[x][(j + o * k) % d]
                        if z not in lab:
                            lab[z] = len(order)
                            order.append(z)
                            first[z] = x
                        row.append(lab[z])
                    code.append(tuple(row))
                    i += 1
                code = tuple(code)
                if best is None or code < best:
                    best = code
    return best


def flip(rot, a, b):
    """Flip edge ab (faces a b c and b a e) to edge ce; None if ce is already an edge."""
    d = len(rot[a])
    ia = rot[a].index(b)
    c, e = rot[a][(ia + 1) % d], rot[a][(ia - 1) % d]
    if e in rot[c]:
        return None
    new = [list(r) for r in rot]
    new[a].remove(b)
    new[b].remove(a)
    for x, y in ((c, e), (e, c)):
        r = new[x]
        for k in range(len(r)):
            if {r[k], r[(k + 1) % len(r)]} == {a, b}:
                r.insert(k + 1, y)
                break
    return new


def validate(rot):
    n = len(rot)
    assert sum(map(len, rot)) // 2 == 3 * n - 6
    seen, faces = set(), 0
    for v, ns in enumerate(rot):
        assert all(v in rot[w] for w in ns)
        for w in ns:
            if (v, w) in seen:
                continue
            dd, k = (v, w), 0
            while dd not in seen:
                seen.add(dd)
                k += 1
                x, y = dd
                dd = (y, rot[y][(rot[y].index(x) + 1) % len(rot[y])])
            assert k == 3
            faces += 1
    assert n - (3 * n - 6) + faces == 2


# ---------------------------------------------------------------- colourings, diagonals

def diag(rot, v, s):
    """Monochromatic link diagonal (p, p+2) of a deletion colouring at v, or None if <= 3 colours."""
    cols = [s[w] for w in rot[v]]
    if len(set(cols)) <= 3:
        return None
    for p in range(5):
        if cols[p] == cols[(p + 2) % 5]:
            return (p, (p + 2) % 5)
    raise AssertionError


DIAGS = [(p, (p + 2) % 5) for p in range(5)]


def star(i):
    return {(i, (i + 2) % 5), ((i + 3) % 5, i)}


def vertex_profile(rot, v, memo):
    """Per diagonal: list of ell over deletion colourings of T - v."""
    byd = collections.defaultdict(list)
    for s in deletion_states(rot, v):
        if s not in memo:
            memo[s] = shortest_fill(rot, s)[0]
        byd[diag(rot, v, s)].append(memo[s])
    return byd


def shape(dfar):
    """Shape of a set of pentagon diagonals as a subgraph of the pentagram 5-cycle."""
    k = len(dfar)
    if k <= 1:
        return f"{k} diagonal(s)"
    if k == 5:
        return "all 5"
    common = set.intersection(*[set(d) for d in dfar])
    if common:
        return f"{k} through one apex (star)"
    if k == 2:
        return "2 crossing"
    # k = 3 or 4: path or (for 3) path+isolated? 3 edges of a 5-cycle: path P4, or P3 + edge
    ends = collections.Counter(x for d in dfar for x in d)
    if k == 3 and max(ends.values()) == 2 and sum(1 for c in ends.values() if c == 1) == 2:
        return "3 consecutive (pentagram path)"
    if k == 4:
        return "4 consecutive (pentagram path)"
    return f"{k} other"


# ---------------------------------------------------------------- Kempe helpers

def components(rot, st, a, b):
    seen, out = set(), []
    for s in range(len(st)):
        if st[s] in (a, b) and s not in seen:
            c, S = {s}, [s]
            while S:
                x = S.pop()
                for y in rot[x]:
                    if y not in c and st[y] in (a, b):
                        c.add(y)
                        S.append(y)
            seen |= c
            out.append(sorted(c))
    return out


def path_between(rot, st, a, b, x, y):
    """A shortest {a,b}-path from x to y in the deletion (hole excluded), or None."""
    prev = {x: None}
    q = collections.deque([x])
    while q:
        z = q.popleft()
        if z == y:
            p = []
            while z is not None:
                p.append(z)
                z = prev[z]
            return p[::-1]
        for t in rot[z]:
            if t not in prev and st[t] in (a, b):
                prev[t] = z
                q.append(t)
    return None


def one_move_report(rot, st):
    """Explain why state st has no filling move (or say which move fills).

    Lemma 1 (one-move fill criterion): with a 4-coloured link, swapping a {a,b}-component K
    leaves <= 3 colours iff K contains every link vertex of colour a and none of colour b (or
    the reverse); a slide of u fills iff the neighbours of u other than the hole use <= 2 colours.
    """
    h = st.index(HOLE)
    link = rot[h]
    cols = [st[w] for w in link]
    lines = []
    fills = False
    if len(set(cols)) <= 3:
        return True, ["filled"]
    for a, b in PAIRS:
        A = [w for w in link if st[w] == a]
        B = [w for w in link if st[w] == b]
        comps = components(rot, st, a, b)
        cof = {x: i for i, c in enumerate(comps) for x in c}
        ok_for = []
        for P, Q, pc in ((A, B, a), (B, A, b)):
            ids = {cof[x] for x in P}
            if len(ids) == 1 and not any(cof[y] in ids for y in Q):
                ok_for.append(pc)
        if ok_for:
            fills = True
            lines.append(f"  pair {{{a},{b}}}: FILLS (removes colour {ok_for})")
            continue
        # blocking witness: an {a,b}-path from a link a-vertex to a link b-vertex, or two
        # link a-vertices (resp. b) in different components
        wit = None
        for x in A:
            for y in B:
                if cof[x] == cof[y]:
                    p = path_between(rot, st, a, b, x, y)
                    wit = f"path {'-'.join(map(str, p))}"
                    break
            if wit:
                break
        if wit is None:
            wit = "link vertices of each colour lie in different components: " + str(
                {x: cof[x] for x in A + B})
        lines.append(f"  pair {{{a},{b}}}: blocked, {wit}")
    for u in link:
        if cols.count(st[u]) == 1:
            others = sorted({st[w] for w in rot[u] if w != h})
            if len(others) <= 2:
                fills = True
                lines.append(f"  slide {u}: FILLS")
            else:
                lines.append(f"  slide {u}: N({u})-{h} = {[w for w in rot[u] if w != h]} "
                             f"coloured {[st[w] for w in rot[u] if w != h]}, {len(others)} colours")
    return fills, lines


def act(g, st):
    out = [None] * len(st)
    for x, c in enumerate(st):
        out[g[x]] = c
    return canon(out)


# ---------------------------------------------------------------- main

def main():
    graphs = load_all()
    print(f"graphs loaded: {len(graphs)}")
    G171 = graphs[(17, 1)]
    rot = parse_ascii(G171["ascii"])
    validate(rot)
    n = len(rot)
    deg = [len(r) for r in rot]

    # ---------------- A
    print("\n=== A. Structure of 17:1 ===")
    print("ascii:", G171["ascii"])
    print("degree sequence:", dict(collections.Counter(deg)))
    six = [v for v in range(n) if deg[v] == 6]
    print("degree-6 vertices:", six, "edges among them:",
          [(a, b) for a in six for b in rot[a] if b in six and a < b])
    for v in range(n):
        print(f"  v={v:2d} deg {deg[v]} link {rot[v]} link degrees {[deg[w] for w in rot[v]]}")
    aut = automorphisms(rot)
    print("|Aut| =", len(aut), "; orientation-preserving:", sum(1 for _, o in aut if o == 1))
    for g, o in aut:
        fixed = [x for x in range(n) if g[x] == x]
        print(f"  {g} orient {o:+d} fixed vertices {fixed}")
    orbits, seen = [], set()
    for v in range(n):
        if v not in seen:
            orb = sorted({g[v] for g, _ in aut})
            seen |= set(orb)
            orbits.append(orb)
    print("vertex orbits:", orbits)
    for v in range(n):
        if deg[v] != 5:
            continue
        for g, o in aut:
            if g[v] == v and g != tuple(range(n)):
                perm = [rot[v].index(g[w]) for w in rot[v]]
                print(f"  stabiliser of {v}: link positions map 0..4 -> {perm} (orient {o:+d})")
    # pair orbits under Aut
    rows = {(r["v"], r["fan_index"]): r for r in G171["report"]["rows"]}

    def fan_image(g, v, i):
        chords = {frozenset((g[a], g[b])) for a, b in [tuple(c) for c in rows[(v, i)]["chords"]]}
        for (v2, i2), r2 in rows.items():
            if v2 == g[v] and {frozenset(c) for c in r2["chords"]} == chords:
                return (v2, i2)
        raise AssertionError

    pair_orbits, seen = [], set()
    for key in sorted(rows):
        if key in seen:
            continue
        orb = sorted({fan_image(g, *key) for g, _ in aut})
        seen |= set(orb)
        pair_orbits.append(orb)
        assert len({rows[k]["L"] for k in orb}) == 1
    print(f"(v,tau) orbits: {len(pair_orbits)}")
    for orb in pair_orbits:
        print(f"  L={rows[orb[0]]['L']} {orb}")
    print("Flip neighbours of 17:1 among order-17 graphs (flips keeping min degree 5):")
    cf = {k: canon_form(parse_ascii(graphs[k]["ascii"])) for k in graphs if k[0] == 17}
    for a in range(n):
        for b in rot[a]:
            if a < b:
                nr = flip(rot, a, b)
                if nr is None or min(map(len, nr)) < 5:
                    continue
                validate(nr)
                c = canon_form(nr)
                hit = [k for k, v in cf.items() if v == c]
                print(f"  flip {a}-{b}: -> {hit if hit else 'not an order-17 plantri graph?'} "
                      f"(m = {[graphs[k]['report']['m'] for k in hit]})")
    rot3 = parse_ascii(graphs[(17, 3)]["ascii"])
    d3 = [len(r) for r in rot3]
    apex = [v for v in range(17) if d3[v] == 5 and all(d3[w] == 5 for w in rot3[v])]
    print("17:3: |Aut| =", len(automorphisms(rot3)), "; vertices with all-degree-5 links:", apex,
          "; degree-6 vertices:", [v for v in range(17) if d3[v] == 6])
    for a in apex:
        ring1 = rot3[a]
        print(f"  apex {a}: ring {ring1}, ring degrees {[d3[w] for w in ring1]}")

    # ---------------- B
    print("\n=== B. Diagonal reduction, checked on every recorded row of P1-P4 ===")
    print("Claim: L(v,tau_i) = max ell over colourings of T-v whose monochromatic diagonal is not at i")
    print("(3-colour links count as ell = 0).")
    shapes_good = collections.Counter()
    shapes_bad = collections.Counter()
    mism = 0
    nrows = 0
    good_per_graph = {}
    profiles = {}
    for key in sorted(graphs):
        g = graphs[key]
        r = parse_ascii(g["ascii"])
        memo = {}
        by_v = collections.defaultdict(list)
        for row in g["report"]["rows"]:
            by_v[row["v"]].append(row)
        good = 0
        for v, vrows in by_v.items():
            prof = vertex_profile(r, v, memo)
            if key[0] == 17 or key == (14, 0):
                profiles[(key, v)] = prof
            for row in vrows:
                i = row["fan_index"]
                vals = [l for dg, ls in prof.items() for l in ls if dg is None or dg not in star(i)]
                nrows += 1
                if max(vals) != row["L"]:
                    mism += 1
            dfar = sorted(dg for dg, ls in prof.items() if dg is not None and max(ls) >= 3)
            sh = shape(dfar)
            isgood = min(row["L"] for row in vrows) <= 2
            good += isgood
            (shapes_good if isgood else shapes_bad)[sh] += 1
        good_per_graph[key] = (good, len(by_v))
    print(f"rows checked: {nrows}; mismatches: {mism}")
    print("Shape of D_far(v) (far = ell >= 3) over all degree-5 vertices of all 961 graphs:")
    print("  at good vertices (some legal fan with L <= 2):", dict(shapes_good))
    print("  at bad vertices (every legal fan L >= 3):    ", dict(shapes_bad))
    cnt = collections.Counter(gd for gd, _ in good_per_graph.values())
    print("graphs by number of good degree-5 vertices:", dict(sorted(cnt.items())))
    byo = collections.defaultdict(list)
    for (o, _), (gd, nv) in good_per_graph.items():
        byo[o].append((gd, nv))
    print("good degree-5 vertices by order (graphs, mean fraction, min count, min fraction):")
    for o in sorted(byo):
        xs = byo[o]
        print(f"  order {o}: {len(xs)} graphs, mean {sum(a / b for a, b in xs) / len(xs):.3f}, "
              f"min {min(a for a, _ in xs)}, min fraction {min(a / b for a, b in xs):.2f}")
    print("graphs with <= 4 good vertices:",
          sorted((v, k) for k, v in good_per_graph.items() if v[0] <= 4))

    # ---------------- C
    print("\n=== C. Far diagonals per degree-5 vertex (ell histogram by monochromatic diagonal) ===")
    for key in [(17, 1), (17, 0), (17, 3), (14, 0)]:
        r = parse_ascii(graphs[key]["ascii"])
        print(f"graph {key[0]}:{key[1]}  m = {graphs[key]['report']['m']}")
        for (k2, v), prof in sorted(profiles.items()):
            if k2 != key:
                continue
            hist = {str(dg): dict(sorted(collections.Counter(ls).items())) for dg, ls in
                    sorted(prof.items(), key=lambda t: (t[0] is not None, t[0]))}
            dfar = sorted(dg for dg, ls in prof.items() if dg is not None and max(ls) >= 3)
            nd6 = sum(len(r[w]) > 5 for w in r[v])
            print(f"  v={v:2d} (#deg>=6 nbrs {nd6}) D_far={dfar} [{shape(dfar)}]  {hist}")

    # ---------------- D
    print("\n=== D. ell = 3 starts at the L = 3 pairs of 17:1, up to automorphism ===")
    memo = {}
    reps = [orb[0] for orb in pair_orbits if rows[orb[0]]["L"] == 3]
    for (v, i) in reps:
        fan = next(f for f in legal_fans(rot, v) if f[0] == i)
        c1, c2 = fan[1], fan[2]
        st_all = deletion_states(rot, v)
        starts = [s for s in st_all if s[c1[0]] != s[c1[1]] and s[c2[0]] != s[c2[1]]]
        # stabiliser of the pair
        stab = [g for g, _ in aut if fan_image(g, v, i) == (v, i)]
        done = set()
        print(f"pair (v={v}, tau_{i}) chords {c1},{c2}; link {rot[v]}; |stabiliser of pair| = {len(stab)}")
        for s in starts:
            if s not in memo:
                memo[s] = shortest_fill(rot, s)[0]
            if memo[s] != 3 or s in done:
                continue
            done |= {act(g, s) for g in stab}
            cols = [s[w] for w in rot[v]]
            dg = diag(rot, v, s)
            p = dg[0]
            # normalise: alpha at p, p+2; beta at p+1; gamma p+3; delta p+4
            bpos, gpos, dpos = (p + 1) % 5, (p + 3) % 5, (p + 4) % 5
            lk = rot[v]
            pbg = path_between(rot, s, s[lk[bpos]], s[lk[gpos]], lk[bpos], lk[gpos])
            pbd = path_between(rot, s, s[lk[bpos]], s[lk[dpos]], lk[bpos], lk[dpos])
            nb = {}
            for mv, nx in moves(rot, s):
                if nx != s:
                    nb.setdefault(nx, mv)
            nl = []
            for nx, mv in nb.items():
                if nx not in memo:
                    memo[nx] = shortest_fill(rot, nx)[0]
                h = nx.index(HOLE)
                nl.append(f"{mv[0]}{'' if mv[0] == 'K' else mv[1]}->hole {h}(deg {len(rot[h])}) ell {memo[nx]}")
            ncomp = [len(components(rot, s, a, b)) for a, b in PAIRS]
            print(f"  start {s}")
            print(f"    link colours {cols}, repeated on diagonal {dg} = vertices "
                  f"{lk[dg[0]]},{lk[dg[1]]}; unique-colour link vertices "
                  f"{[lk[bpos], lk[gpos], lk[dpos]]} with degrees {[deg[lk[bpos]], deg[lk[gpos]], deg[lk[dpos]]]}")
            print(f"    beta-gamma path {pbg}; beta-delta path {pbd}")
            print(f"    Kempe components per pair {dict(zip(PAIRS, ncomp))}")
            print(f"    distinct neighbours ({len(nb)}): {nl}")

    # ---------------- E
    print("\n=== E. Certificate: start X at v = 7 has ell(X) = 3 ===")
    v = 7
    X = (0, 1, 2, 1, 3, 2, 3, 4, 0, 3, 0, 2, 1, 0, 1, 2, 3)
    assert X.index(HOLE) == v
    assert all(X[a] != X[b] for a in range(n) for b in rot[a] if HOLE not in (X[a], X[b]))
    print("X =", X, "(proper on T - 7)")
    print("link of 7:", rot[v], "colours", [X[w] for w in rot[v]], "diagonal", diag(rot, v, X))
    print("fans for which X is a start:",
          [i for i, c1, c2 in legal_fans(rot, v) if X[c1[0]] != X[c1[1]] and X[c2[0]] != X[c2[1]]])
    fills, lines = one_move_report(rot, X)
    assert not fills
    print("X itself (no filling move, so ell(X) >= 2):")
    print("\n".join(lines))
    print("Kempe components of X:")
    for a, b in PAIRS:
        print(f"  {{{a},{b}}}: {components(rot, X, a, b)}")
    nb = {}
    for mv, nx in moves(rot, X):
        if nx != X:
            nb.setdefault(nx, []).append(mv)
    print(f"X has {len(nb)} distinct neighbours (states differing only by colour renaming identified):")
    for k, (Y, mvs) in enumerate(nb.items(), 1):
        h = Y.index(HOLE)
        fills, lines = one_move_report(rot, Y)
        assert not fills
        print(f" Y{k} via {mvs}: hole {h} (deg {len(rot[h])}), link {rot[h]} colours {[Y[w] for w in rot[h]]}")
        print(f"   Y{k} = {Y}")
        print("\n".join(lines))
    ell, path = shortest_fill(rot, X)
    assert ell == 3
    print("ell(X) = 3; a shortest fill:", path)
    # mirror image under the stabiliser of 7
    for g, o in aut:
        if g[v] == v and g != tuple(range(n)):
            X2 = act(g, X)
            print("image of X under the stabiliser of 7:", X2, "colours", [X2[w] for w in rot[v]],
                  "diagonal", diag(rot, v, X2), "fans:",
                  [i for i, c1, c2 in legal_fans(rot, v) if X2[c1[0]] != X2[c1[1]] and X2[c2[0]] != X2[c2[1]]])
    print("Hence every fan at 7 has a start with ell >= 3: L(7, tau) >= 3 for all five tau; same at 13 by Aut.")

    # ---------------- F
    print("\n=== F. Kempe rigidity vs ell, every 4-colour-link deletion state, orders 12-20 (P1, P2) ===")
    print("columns: number of the six colour pairs whose bichromatic subgraph of T - hole is connected")
    tab = collections.Counter()
    for key in sorted(graphs):
        if key[0] > 20:
            continue
        r = parse_ascii(graphs[key]["ascii"])
        memo = {}
        for v in range(len(r)):
            if len(r[v]) != 5:
                continue
            for s in deletion_states(r, v):
                if diag(r, v, s) is None:
                    continue
                l = shortest_fill(r, s)[0]
                k = sum(1 for a, b in PAIRS if len(components(r, s, a, b)) == 1)
                tab[(min(l, 3), k)] += 1
    for l in (1, 2, 3):
        tot = sum(tab[(l, k)] for k in range(7))
        lab = "ell>=3" if l == 3 else f"ell={l}"
        print(f"  {lab}: {tot} states; fraction by #connected pairs "
              f"{ {k: round(tab[(l, k)] / tot, 3) for k in range(7) if tab[(l, k)]} }")


if __name__ == "__main__":
    main()
