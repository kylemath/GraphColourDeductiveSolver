#!/usr/bin/env python3
"""Regression and mutation tests for wp22v_verify.py (WP22-interface.md regression cases).
Expected values come from other teams' documents (data constants copied below as DATA only)."""
import sys, os, json, io, tempfile, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp22v_verify as V

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s %s" % ("ok  " if cond else "FAIL", name, detail))


# --- data (copied from l-attack.md section 0, MathConjectureR.md, lattack_witness.py data) -------
W6_FACES = [[1,16,5],[2,4,6],[2,33,22],[3,16,8],[4,2,22],[4,14,21],[4,22,14],[5,31,1],[5,33,6],[6,4,11],[6,10,20],[6,11,34],[6,20,5],[6,33,2],[8,13,17],[8,14,3],[9,14,8],[10,1,31],[10,6,34],[11,10,34],[11,17,13],[13,1,10],[13,8,16],[13,10,11],[14,17,21],[16,1,13],[16,3,5],[17,9,8],[17,11,21],[17,14,9],[20,31,5],[21,11,4],[22,3,14],[31,20,10],[33,3,22],[33,5,3]]
W6_COL = {1:2,2:2,3:2,4:0,5:0,6:3,8:3,9:2,10:0,11:2,13:1,14:1,17:0,20:1,21:3,22:3,31:3,33:1,34:1}
T4_FACES = [(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
A3_WIT_FACES = [(0,1,2),(0,2,3),(0,3,4),(0,4,5),(0,5,1),(1,6,2),(2,7,3),(3,8,4),(4,9,5),(5,10,1),(6,7,2),(6,11,7),(7,8,3),(7,12,8),(8,9,4),(8,13,9),(9,10,5),(9,14,10),(10,6,1),(10,15,6),(11,12,7),(12,13,8),(13,14,9),(14,15,10),(15,11,6),(16,11,15),(16,12,11),(16,13,12),(16,14,13),(16,15,14)]
A3_WIT_COL = {1:0,2:1,3:0,4:2,5:3,6:2,7:3,8:1,9:0,10:1,11:0,12:2,13:3,14:2,15:3,16:1}


def cert_file(faces, v, col, claim):
    fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    json.dump({"faces": [list(f) for f in faces], "v": v, "colouring": {str(k): c for k, c in col.items()}, "claim": claim}, fh)
    fh.close()
    return fh.name


def run_cert(faces, v, col, claim, orient=False):
    p = cert_file(faces, v, col, claim)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = V.cmd_cert(p, orient=orient)
    os.unlink(p)
    return code, buf.getvalue()


# ---------------------------------------------------------------------------------- W6
code, out = run_cert(W6_FACES, 16, W6_COL, {"radius": 2})
check("W6 certificate accepted, radius 2, strict orientation", code == 0 and "RADIUS 2" in out and "start doubly locked: True" in out, repr(out.strip().replace("\n", " | ")))
T = V.Tri(W6_FACES); H = V.Hole(T, T.idx[16])
check("W6 link order from faces is a cyclic rotation of 5,1,13,8,3 (either orientation)", (lambda l: l in [[5,1,13,8,3][k:]+[5,1,13,8,3][:k] for k in range(5)] or l[::-1] in [[5,1,13,8,3][k:]+[5,1,13,8,3][:k] for k in range(5)])([T.labels[x] for x in H.link]))
# W6 F-chain: lock status along the F orbit: l-attack says chain of length 6 (steps 0..5 locked, step 6 not)
s = H.canon(bytes(V.HOLE if l == 16 else W6_COL[l] for l in T.labels)); chain = 0
while s is not None and H.linkcolours(s) == 4 and H.doubly_locked(s) and chain < 50:
    chain += 1; s = H.F(s)
check("W6 chain length of F-iterates (expected 6 per l-attack.md)", chain == 6, "got %d" % chain)

# ---------------------------------------------------------------------------------- A_3 centre
faces3 = V.build_A(3)
T3 = V.Tri(faces3); H3 = V.Hole(T3, T3.idx[0])
edges = lambda fs: {frozenset(p) for f in fs for p in ((f[0], f[1]), (f[1], f[2]), (f[0], f[2]))}
check("my A_3 has the same edge set as the witness A3_FACES data (labels v=0, ring 1+5i+t, cap 16)", edges(faces3) == edges(A3_WIT_FACES))
check("orders of A_3, A_4, A_5 are 17, 22, 27; degrees only 5 and 6, twelve of degree 5",
      all(V.census_graph(r)[1].n == 5 * r + 2 and set(V.census_graph(r)[2]) <= {5, 6} and V.census_graph(r)[2].count(5) == 12 for r in (3, 4, 5)))
code, out = run_cert(A3_WIT_FACES, 0, A3_WIT_COL, {"radius": 3})
r_wit = out.split("\n")[0]
print("     witness colouring result:", r_wit)
check("A_3 witness colouring certificate: doubly locked and radius in {2,3}", "start doubly locked: True" in out and ("RADIUS 2" in r_wit or "RADIUS 3" in r_wit))
states = V.enumerate_states(H3)
inf = []
for s in states:
    if H3.linkcolours(s) != 4:
        continue
    seen, cur, ok = set(), s, True
    while cur is not None and cur not in seen:
        seen.add(cur)
        if H3.linkcolours(cur) != 4 or not H3.doubly_locked(cur):
            ok = False; break
        cur = H3.F(cur)
    if ok and cur is not None:
        inf.append(s)
check("A_3 centre: 20 canonical infinite-chain classes (a-structure.md: 20)", len(inf) == 20, "got %d" % len(inf))
ring0 = [s for s in inf if tuple(s[1:6]) == (0, 1, 0, 2, 3)]
rads = sorted(V.kempe_search(H3, s)[1] for s in ring0)
check("A_3 centre: 4 infinite-chain colourings with ring 0 = 01023, radii [2,2,3,3]", rads == [2, 2, 3, 3], str(rads))
allrads = {}
for s in inf:
    k = V.kempe_search(H3, s)[1]; allrads[k] = allrads.get(k, 0) + 1
check("A_3 centre: all 20 infinite-chain classes have radius 2 or 3", set(allrads) <= {2, 3}, str(allrads))
check("witness colouring is one of the infinite-chain states", H3.canon(bytes(V.HOLE if l == 0 else A3_WIT_COL[l] for l in T3.labels)) in inf)

# ---------------------------------------------------------------------------------- T4
t4 = V.orient_faces(T4_FACES)
try:
    V.Tri(T4_FACES); strict = True
except V.Invalid:
    strict = False
check("T4 face list as published is unoriented: strict Tri() rejects it (expected, orient_faces helper needed)", not strict)
T4 = V.Tri(t4); H4 = V.Hole(T4, T4.idx[4])
check("T4: 17 vertices, 30 faces, hole 4 of degree 5, degrees twelve 5s and five 6s", T4.n == 17 and len(t4) == 30 and sorted(len(a) for a in T4.adj).count(5) == 12 and sorted(len(a) for a in T4.adj).count(6) == 5)
st4 = V.enumerate_states(H4)
filled = [s for s in st4 if H4.filled(s)]
check("T4: 68 canonical colourings, 22 filled", len(st4) == 68 and len(filled) == 22, "got %d / %d" % (len(st4), len(filled)))
hist_all, hist_dl, unreached = {}, {}, 0
for s in st4:
    res = V.kempe_search(H4, s)
    if res[0] != "RADIUS":
        unreached += 1; continue
    hist_all[res[1]] = hist_all.get(res[1], 0) + 1
    if H4.linkcolours(s) == 4 and H4.doubly_locked(s):
        hist_dl[res[1]] = hist_dl.get(res[1], 0) + 1
check("T4: radius histogram over all states {0:22,1:25,2:15,3:4,4:2}", hist_all == {0: 22, 1: 25, 2: 15, 3: 4, 4: 2}, str(dict(sorted(hist_all.items()))))
check("T4: 21 doubly locked states {2:15,3:4,4:2}", hist_dl == {2: 15, 3: 4, 4: 2}, str(dict(sorted(hist_dl.items()))))
check("T4: nothing unreached", unreached == 0)
# certificate on a radius-4 T4 state
s4 = next(s for s in st4 if H4.linkcolours(s) == 4 and H4.doubly_locked(s) and V.kempe_search(H4, s)[1] == 4)
col4 = {T4.labels[u]: s4[u] for u in range(T4.n) if u != H4.h}
code, out = run_cert(t4, 4, col4, {"radius": 4})
check("T4 radius-4 certificate via cert command", code == 0 and "RADIUS 4" in out)

# ---------------------------------------------------------------------------------- mutation tests
w6 = dict(W6_COL)
bad = dict(w6); bad[1] = w6[5]   # vertex 1 adjacent to 5 (edge in face [1,16,5]) -> monochromatic
code, out = run_cert(W6_FACES, 16, bad, {"radius": 2})
check("mutation: corrupted colour rejected with 'improper colouring' (exit 2)", code == 2 and "improper colouring" in out, out.strip())
bad = dict(w6); del bad[13]
code, out = run_cert(W6_FACES, 16, bad, {"radius": 2})
check("mutation: missing colour rejected ('misses vertex 13')", code == 2 and "misses vertex 13" in out, out.strip())
nf = [f for f in W6_FACES if f != [33, 5, 3]]
code, out = run_cert(nf, 16, w6, {"radius": 2})
check("mutation: deleted face rejected as not a triangulation", code == 2 and "NOT-TRIANGULATION" in out, out.strip())
nf = [list(f) for f in W6_FACES]; nf[0] = [1, 5, 16]
code, out = run_cert(nf, 16, w6, {"radius": 2})
check("mutation: reversed face rejected (orientation)", code == 2 and "NOT-TRIANGULATION" in out, out.strip())
nf = [list(f) for f in W6_FACES]; nf[5] = [4, 14, 22]
code, out = run_cert(nf, 16, w6, {"radius": 2})
check("mutation: face list with relabelled vertex rejected", code == 2 and "NOT-TRIANGULATION" in out, out.strip())
code, out = run_cert(W6_FACES, 16, w6, {"radius": 3})
check("mutation: claim radius 3 (true 2) contradicted, exit 1", code == 1 and "CONTRADICTED: claimed radius 3, recomputed radius 2" in out, out.strip().split("\n")[-1])
code, out = run_cert(W6_FACES, 16, w6, {"radius": None, "class_closed_no_filled": True, "class_size": 99})
check("mutation: claim of targetless class on a class with a filled state contradicted, exit 1", code == 1 and "filled state exists at distance 2" in out, out.strip().split("\n")[-1])
code, out = run_cert(W6_FACES, 5, w6, {"radius": 2})
check("mutation: hole of wrong degree rejected", code == 2 and "degree" in out, out.strip())
bad = dict(w6)
for x in (1, 13, 8): bad[x] = 0 if bad[x] != 0 else 1
# force link colour collapse: give link vertices (5,1,13,8,3) colours so only 3 appear, keeping properness not required here
cap_p = cert_file(W6_FACES, 16, w6, {"radius": 2})
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    codec = V.cmd_cert(cap_p, cap=3)
os.unlink(cap_p)
check("cap: a state cap of 3 states yields CAPPED and exit 2", codec == 2 and "CAPPED" in buf.getvalue(), buf.getvalue().strip().split("\n")[0])

# ---------------------------------------------------------------------------------- planted
code = V.cmd_planted()
check("planted kill case: unreachable target -> CLOSED-NO-FILLED with correct class size; true target -> radius", code == 0)
res_p = V.kempe_search(H4, s4, V.planted_pred)
res_t = V.kempe_search(H4, s4)
check("planted on T4 radius-4 state: planted CLOSED (size 68 = whole space), true RADIUS 4", res_p[:2] == ("CLOSED", 68) and res_t[:2] == ("RADIUS", 4), str((res_p[:2], res_t[:2])))
claim = {"radius": None, "class_closed_no_filled": True, "class_size": 68}
kc, msg = V.verify_claim(res_p, claim, True)
kc2, msg2 = V.verify_claim(res_t, claim, True)
check("claim logic: targetless claim confirmed on planted result (0), contradicted on true result (1)", (kc, kc2) == (0, 1), msg + " / " + msg2)

# ---------------------------------------------------------------------------------- census / census-check
tmp = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False); tmp.close()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    V.cmd_census("A_3", tmp.name)
lines = open(tmp.name).read().splitlines()
check("census A_3 writes 12 holes: 2 x 30 + 10 x 14 = 200 records", len(lines) == 200, "got %d" % len(lines))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    c = V.cmd_census_check(tmp.name, limit=0)
check("census-check recomputes all 200 records with the per-state BFS, 0 mismatches", c == 0 and " 0 mismatches" in buf.getvalue(), buf.getvalue().strip())
recs = [json.loads(l) for l in lines]
recs[0]["radius"] = 5
for r_ in recs[1:]:
    pass
tmp2 = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
tmp2.write("\n".join(json.dumps(r_) for r_ in recs) + "\n"); tmp2.close()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    c = V.cmd_census_check(tmp2.name, limit=0)
check("mutation: census record with wrong radius is reported (exit 1, 1 mismatch)", c == 1 and "1 mismatches" in buf.getvalue() and "radius recomputed" in buf.getvalue())
os.unlink(tmp.name); os.unlink(tmp2.name)

print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
if FAIL:
    print("FAILED:", FAIL)
sys.exit(1 if FAIL else 0)
