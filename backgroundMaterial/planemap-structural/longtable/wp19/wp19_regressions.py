"""WP19 regressions (declaration section "Regressions"), run before any phase. Exit non-zero on
failure. Output saved as regressions-output.txt. Reads no order-23 or order-24 data.

1. Icosahedron: ell <= 1 and kappa <= 1 everywhere, L = 1 at all 60 pairs, U at every pair.
2. Order-14 dipyramid start (order14_fan_check.py / fan-link.md): ell = 2 and locked.
3. 17:1 (manifest discovery order 17, graph_index 1): m = 3, exactly 38 of 60 pairs satisfy U.
4. 22:93 (0-based line 93 of triangulations-min5-22.txt), v = 17: the start recorded in
   wp18/mechanism-kempe-long.json with l = 4, kappa = 5 has ell = 4 and kappa = 5 here.
5. Malformed-certificate rejection is the checker's job (wp19_check.py), not tested here.
6. Colour-renaming invariance on one random start per regression graph: the start's colours
   are permuted at random and ell, kappa and locked are recomputed by an independent
   per-start breadth-first search on raw (never canonicalised) colourings.
Cross-checks: per-pair T* class counts and all-locked class counts agree with
swarm/vh_exists_check.analyse; per-pair L agrees with the WP18 outputs where recorded.
"""
import itertools
import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(L / "swarm"))
from wp19_core import (CAP_KEMPE, CAP_MIXED, HOLE, Guard, canon, deletion_states, filled,  # noqa: E402
                       graph_report, kempe_distances, legal_fans, mixed_distances, parse_ascii)
import vh_exists_check  # noqa: E402
from icosahedron_fan import rotation_from_triangles, validate_sphere  # noqa: E402

random.seed(19)
man = json.loads((L / "wp11-run-manifest.json").read_text())


def manifest(order, idx):
    return next(g["ascii"] for g in man["discovery_graphs"] + man["validation_graphs"]
                if g["order"] == order and g["graph_index"] == idx)


def dists(rot, v):
    g = Guard(None, None)
    sbh = {h: deletion_states(rot, h, g) for h in range(len(rot))}
    return sbh, mixed_distances(rot, sbh, g), kempe_distances(rot, v, sbh[v], g)


# ------------------------------------------------ independent raw BFS for invariance

def raw_moves(rot, st, slides=True):
    h = st.index(HOLE)
    for a, b in itertools.combinations(range(4), 2):
        seen = set()
        for s in range(len(st)):
            if st[s] not in (a, b) or s in seen:
                continue
            comp, stack = {s}, [s]
            while stack:
                x = stack.pop()
                for y in rot[x]:
                    if y not in comp and st[y] in (a, b):
                        comp.add(y)
                        stack.append(y)
            seen |= comp
            yield tuple(b if (i in comp and c == a) else a if (i in comp and c == b) else c
                        for i, c in enumerate(st))
    if slides:
        cols = [st[w] for w in rot[h]]
        for u in rot[h]:
            if cols.count(st[u]) == 1:
                nx = list(st)
                nx[h], nx[u] = st[u], HOLE
                yield tuple(nx)


def raw_bfs(rot, st, cap, slides):
    if filled(rot, st):
        return 0
    seen, fr = {st}, [st]
    for d in range(1, cap + 1):
        nx = []
        for x in fr:
            for y in raw_moves(rot, x, slides):
                if y in seen:
                    continue
                if filled(rot, y):
                    return d
                seen.add(y)
                nx.append(y)
        fr = nx
    return None


def invariance(rot, name, G):
    P = random.choice([P for P in G["pairs"] if P["starts"]])
    v = P["v"]
    sbh, ld, kd = dists(rot, v)
    (c1, c2) = [tuple(c) for c in P["chords"]]
    S = [s for s in sbh[v] if s[c1[0]] != s[c1[1]] and s[c2[0]] != s[c2[1]]]
    s = random.choice(S)
    perm = list(range(4))
    while perm == list(range(4)):
        random.shuffle(perm)
    t = tuple(HOLE if x == HOLE else perm[x] for x in s)
    assert canon(t) == s
    ell_raw = raw_bfs(rot, t, CAP_MIXED, True)
    kap_raw = raw_bfs(rot, t, CAP_KEMPE, False)
    ell = ld.get(s)
    k = kd.get(s)
    kap = None if (k is None or k > CAP_KEMPE) else k
    four = len({t[w] for w in rot[v]}) == 4
    locked_raw = four and not any(filled(rot, y) for y in raw_moves(rot, t, False))
    locked = four and k != 1
    assert (ell_raw, kap_raw, locked_raw) == (ell, kap, locked), (name, ell_raw, ell, kap_raw, kap)
    print(f"  invariance {name}: pair ({v},{P['fan_index']}) start {list(s)} perm {perm}: "
          f"ell={ell} kappa={kap if kap is not None else ('nofill' if k is None else 'capped')} "
          f"locked={locked} (raw BFS agrees)")


def crosscheck_vh(rot, name, G):
    r = vh_exists_check.analyse(rot)
    mine = {(P["v"], P["fan_index"]): P for P in G["pairs"]}
    assert len(r["pairs"]) == len(mine)
    for q in r["pairs"]:
        P = mine[(q["v"], q["fan"])]
        assert P["starts"] == q["S"] and P["tstar_classes"] == q["Tstar_classes"], (name, q)
        assert P["locked_classes"] == q["U_bad_classes"], (name, q)
    print(f"  vh_exists_check agrees on {name}: |S|, T* classes, all-locked classes at "
          f"{len(mine)} pairs; U-failing pairs {sum(1 for q in r['pairs'] if q['U_bad_classes'])}")


def crosscheck_wp18(name, G, phase_file, order, idx):
    p = L / "wp18" / phase_file
    if not p.exists():
        return
    d = json.loads(p.read_text())
    g = next((g for g in d["graphs"] if g["order"] == order and g["graph_index"] == idx), None)
    if g is None or "report" not in g:
        return
    rows = {(r["v"], r["fan_index"]): r for r in g["report"]["rows"]}
    for P in G["pairs"]:
        r = rows[(P["v"], P["fan_index"])]
        assert (r["L"], r["L_at_least"], r["starts"]) == (P["L"], P["L_at_least"], P["starts"])
    print(f"  WP18 {phase_file} agrees on {name}: L, L_at_least, starts at {len(rows)} pairs; "
          f"m={g['report']['m']}")


def run(rot, name, **kw):
    t = time.time()
    G = graph_report(rot, **kw)
    dt = time.time() - t
    assert G["interrupted"] is None
    print(f"{name}: n={len(rot)} pairs={len(G['pairs'])} m={G['m']} U_exists={G['U_exists']} "
          f"U_pairs={sum(1 for P in G['pairs'] if P['U'])} kills={[k['stmt'] for k in G['kills']]} "
          f"seconds={dt:.2f} peak_rss_kb={G['peak_rss_kb']}")
    return G


# 1. Icosahedron
a = manifest(12, 0)
rot = parse_ascii(a)
G = run(rot, "icosahedron 12:0", order=12, graph_index=0, ascii_=a)
assert len(G["pairs"]) == 60
for P in G["pairs"]:
    assert P["L"] == 1 and P["U"] is True and P["unresolved_reason"] is None
    assert all(c == 0 for k, c in P["hist_l"].items() if k not in ("0", "1"))
    assert all(c == 0 for k, c in P["hist_k"].items() if k not in ("0", "1"))
assert G["m"] == 1 and G["kills"] == []
print("  ell <= 1 and kappa <= 1 everywhere, L = 1 at 60 pairs, U at every pair: OK")
crosscheck_vh(rot, "12:0", G)
crosscheck_wp18("12:0", G, "wp18-P1.json", 12, 0)
invariance(rot, "12:0", G)

# 2. Order-14 dipyramid (gyroelongated hexagonal dipyramid), hole U0, fan {N L0, N L1}
names = ["N", "S"] + [f"U{i}" for i in range(6)] + [f"L{i}" for i in range(6)]
ix = {x: i for i, x in enumerate(names)}
tri = []
for i in range(6):
    j = (i + 1) % 6
    tri += [("N", f"U{i}", f"U{j}"), ("S", f"L{j}", f"L{i}"), (f"U{i}", f"L{i}", f"L{j}"),
            (f"U{i}", f"L{j}", f"U{j}")]
tri = [tuple(ix[x] for x in t) for t in tri]
try:
    rm = rotation_from_triangles(tri, list(range(14)))
except RuntimeError:
    rm = rotation_from_triangles([(c, b, a) for a, b, c in tri], list(range(14)))
rot = [rm[v] for v in range(14)]
validate_sphere(rot, 5)
col = {"N": 1, "S": 0, "U1": 0, "U2": 3, "U3": 0, "U4": 2, "U5": 0, "L0": 2, "L1": 3,
       "L2": 1, "L3": 2, "L4": 3, "L5": 1}
st = canon(tuple(col.get(x, HOLE) for x in names))
G = run(rot, "dipyramid 14 (order14_fan_check.py)")
v = ix["U0"]
want = {tuple(sorted((ix["N"], ix["L0"]))), tuple(sorted((ix["N"], ix["L1"])))}
fan = [f for f in legal_fans(rot, v) if {tuple(sorted(f[1])), tuple(sorted(f[2]))} == want]
assert len(fan) == 1
sbh, ld, kd = dists(rot, v)
i, c1, c2 = fan[0]
assert st in sbh[v] and st[c1[0]] != st[c1[1]] and st[c2[0]] != st[c2[1]]
four = len({st[w] for w in rot[v]}) == 4
assert ld.get(st) == 2 and four and kd.get(st) != 1
print(f"  start {list(st)} at (v={v}, fan {i}): ell = 2, kappa = {kd.get(st)}, locked: OK")
crosscheck_vh(rot, "dipyramid", G)
invariance(rot, "dipyramid", G)

# 3. 17:1
a = manifest(17, 1)
rot = parse_ascii(a)
G = run(rot, "17:1", order=17, graph_index=1, ascii_=a)
assert G["m"] == 3, G["m"]
assert len(G["pairs"]) == 60 and sum(1 for P in G["pairs"] if P["U"]) == 38
print("  m = 3 and 38 of 60 pairs satisfy U: OK")
crosscheck_vh(rot, "17:1", G)
crosscheck_wp18("17:1", G, "wp18-P1.json", 17, 1)
invariance(rot, "17:1", G)

# 4. 22:93, v = 17, the l = 4, kappa = 5 start
a = (L / "wp17-last-roots" / "triangulations-min5-22.txt").read_text().splitlines()[93]
rot = parse_ascii(a)
rec = [r for r in json.loads((L / "wp18" / "mechanism-kempe-long.json").read_text())
       if r["order"] == 22 and r["graph"] == 93 and r["v"] == 17 and r["l"] == 4 and r["kappa"] == 5]
assert len(rec) == 1
st = tuple(rec[0]["start"])
G = run(rot, "22:93", order=22, graph_index=93, ascii_=a)
sbh, ld, kd = dists(rot, 17)
assert st in sbh[17] and ld.get(st) == 4 and kd.get(st) == 5
fans = [i for i, c1, c2 in legal_fans(rot, 17) if st[c1[0]] != st[c1[1]] and st[c2[0]] != st[c2[1]]]
assert fans
for P in G["pairs"]:
    if P["v"] == 17 and P["fan_index"] in fans:
        assert P["hist_l"]["4"] >= 1 and P["hist_k"]["5"] >= 1
print(f"  start {list(st)} at v = 17 (in S(17, tau_i) for i in {fans}): ell = 4, kappa = 5: OK")
crosscheck_vh(rot, "22:93", G)
crosscheck_wp18("22:93", G, "wp18-P4.json", 22, 93)
invariance(rot, "22:93", G)

print("ALL WP19 REGRESSIONS PASSED")
