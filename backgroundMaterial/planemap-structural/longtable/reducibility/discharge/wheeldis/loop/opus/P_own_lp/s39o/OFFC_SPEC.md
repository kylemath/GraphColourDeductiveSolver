# OFFC_SPEC — off-centre matching (`offc`) and whole-window raw patterns (`rpatN`) for the stacked engine

Round s39o, Opus P_own_lp. This spec is written so that Studio can mirror it independently. Code:
`s39o/eng/offc.py` (exec'd from `pcheck.load_patterns()` only when the flag `offc` is set), the `rpatN=` loader in
`s39o/eng/pcheck.py`, the builder `s39o/rpatN_build.py`, and the controls `s39o/rpatN_check.py` and `s39o/offc_phys.py`.
With `offc` off and no `rpatN=`, the engine is byte-identical in behaviour to `s33z/eng` (control (a), section 7).

## 0. What was there before

`pcheck.instances(d)` expands every pattern `P = {slot: letter set}` over the 2d rotations and reflections of **u's own ring**:
`w_i -> w_{i+r}`, `s_i -> s_{i+r}`, or `w_i -> w_{r-i}`, `s_i -> s_{r-i-1}`. The DFS separator (`bin/jsep3`, `bin/jsep5` at
d = 7 with l3q) and `admissible()` kill an arrangement when one instance has every slot letter in its set. So a registry
configuration counted only when it sat in the window **with its own centre on u**. Off-centre occurrences (the configuration
inside the 1.5-ball but not centred at u, for example around a 7 at `s_0`) were never seen.

`s28q/eng/pcheck.py` and `s33z/eng/pcheck.py` are **separate copies** (md5 `84291878…` and `3725f3d1…`). `s33z/eng` has its own
`pcheck.py`, `prelay2.py` and `privcell.py`. `s33z/eng/pcheck_s33_pre_noC.py` is byte-identical to `s28q/eng/pcheck.py`. The new
code lives in `s39o/eng`, which is a copy of `s33z/eng` plus this change.

## 1. The window: what a row determines

A row (or a DFS cell, once its slots are filled) is `d, LINK = w_0..w_{d-1}, SWORD = s_0..s_{d-1}`, with letters 5, 6, 7, 8, 9.
Letter 9 means degree ≥ 9 and is **never exact**. u has exact degree d.

The engine's own reading (`admissible()`, `recv_coef`): `s_i` is the apex of the edge `w_i w_{i+1}`, and a five `w_i` has the
link `(u, w_{i+1}, s_i, s_{i-1}, w_{i-1})`. In the plane 2-ball (explore's `cen54.build`, `LZ/Layered`, with ring 3 fresh),
ring 2 around `w_i` is the arc `s_{i-1}, p_{i,1}, …, p_{i,k}, s_i`, with `k = w_i − 5` private vertices (`k = 4` for a 9).
The privates are never exact.

**Known vertices (the 1.5-ball):** u, every `w_i`, and every `s_i`. A known vertex is **exact** iff it is u or its letter is
5..8.

**Edges among known vertices:**
- `u – w_i` for every i;
- `w_i – w_{i+1}`;
- `w_i – s_i` and `w_{i+1} – s_i` (the apex);
- `s_{i-1} – s_i` **iff `w_i = 5`** (when `w_i ≥ 6`, its privates sit between them on ring 2);
- no other pair is adjacent. In particular, u is never adjacent to an `s_i`, `w_i` is not adjacent to `w_j` for |i − j| ≥ 2, and
  `s_i` is not adjacent to `s_j` for |i − j| ≥ 2.

**Faces (triangles) among known vertices:** `u w_i w_{i+1}`; `w_i w_{i+1} s_i`; and `w_i s_{i-1} s_i` iff `w_i = 5`. Every
3-cycle of known vertices is one of these.

**Which vertices have a fully known link:** u (link `w_0..w_{d-1}`); and every `w_i = 5` (link `u, w_{i+1}, s_i, s_{i-1},
w_{i-1}`). A `w_i ≥ 6` has privates. An `s_i` always has 1 to 4+ neighbours on ring 3, plus privates of `w_i` / `w_{i+1}` when
they are not 5. These are never known.

Why non-adjacency is safe: two known vertices that are non-adjacent in the 2-ball lie within distance 2 of u. An extra edge
between them, or an identification, would close a cycle of length ≤ 5 through u that has vertices on both sides. Internal
6-connectivity of a minimal counterexample (Birkhoff) forbids this. This is the same model the u-centred matcher already uses.

## 2. The configuration K of a registry entry

The registry entries are the `pat=` lines (D, `r= m=` on the line), the `cpat=` entries (C, `r= m=` on the header line), the
`nf=` file, the raw `rpat=` patterns (e.g. `rpatD.txt`) and `rpatN=` (section 3). The pcell f-patterns are **not** registry
entries for offc. Each entry is a degree-d0 pattern `P`. Let EX be its slots whose set is a single letter in 5..8. A `B`
slot (7, 8, 9), a multi-letter mask, or a free slot is **not** in EX.

1. **Ambiguity.** If `s_{i-1}, s_i ∈ EX` and `w_i ∉ EX`, the cut window's `s_{i-1} s_i` adjacency is not fixed by the entry.
   The entry is **skipped** (no off-centre use). A67: 1,075 D and 116 C entries.
2. `Ku` = the induced known-vertex graph of the degree-d0 window (section 1) on `{u} ∪ EX`. Degrees are u = d0 and the
   singleton letters elsewhere. The s–s rule reads `w_i ∈ EX` with letter 5 (a `w_i` not in EX never gives an s–s edge).
   `K0 = Ku − u`.
3. Ring size of a connected K with n vertices, degree sum Σ and E interior edges: `r(K) = Σ − E − 3n + 3`. This is Euler's
   formula for the triangulated disc of the free completion.
4. **Choice of K:**
   - an `rpatN` entry: `K = Ku` (u is the centre by construction, section 3);
   - no `(r, m)` on record (`nf=`, `rpat=`): `K = Ku`. This is a superset of the verified interior, because every interior
     vertex of a sound pattern is pinned exactly. Embedding a superset implies embedding the verified configuration, so this
     is conservative;
   - `m = |EX| + 1` and `r(Ku) = r`: `K = Ku` (A67: 16,264 D and 2,042 C entries);
   - `m = |EX|` and `K0` is connected and `r(K0) = r`: `K = K0`, so **u is not part of the configuration** (A67: 49 D). An
     example is `f7_.....55_....575`, `r=8 m=5`: interior `w5 w6 s4 s5 s6` = 5 5 5 7 5 with ring 8;
   - otherwise the entry is skipped (A67: 10 C entries with `r=0 m=0`).
   - K must be connected.
5. Entries named RSST 2.126 or RSST 8406.123 are skipped by name (`OFFC_EXCL`). Neither is in `rpatD.txt`, the A67 args
   registry, or `rpatN.txt`. They are kept out of every solve.

## 3. rpatN (whole-window raw patterns)

File format: one pattern per line, `d LINK SWORD [# comment]`. Each character is 5–8 (exact letter), `N` (= {6,7,8,9}; only in
LINK) or `.` (free). Option `rpatN=FILE[,FILE]`. It is loaded into `PATS[d]` like any other pattern, with source tag `RPATN`.

Building it (`rpatN_build.py KCFILE OUT`): start from each kc line `NAME r m RINGNB INTNB`, where vertex v has degree
`|ring nb| + |interior nb|` and the interior triangles are the 3-cliques of the interior graph. For every vertex c with
degree d in 7..17, enumerate every embedding of the configuration with `c -> u` into the degree-d window. An embedding is
injective, every image is exact with equal degree, it is induced among the images (adjacent iff adjacent, section 1), and
every interior triangle lands on a face. Each embedding becomes a pattern: the image slots get their letters. In addition,
for each `w_i ∉` image with `s_{i-1}, s_i ∈` image, `w_i` gets {5} if the configuration has the edge and `N` if it does not.
All other slots are free. The patterns are kept up to rotation and reflection.

Input: explore's round-55 `loop/k55/row55_hits_kc.txt` (commit 57526d20, branch `claude/project-thread-nh6pv2`), md5
`47afb28d71c487132281b3bd5b217b01` (verified). It holds 35 configurations of the 2026 set. Each one is two-engine D: verdict D
in `loop/k53/N54_res.txt`, and `D=true` in both `N54_kcc.out` and `N54_df.out` (35/35 verified). The build gives 64 centres
of degree ≥ 7, 598 embeddings, **37 distinct patterns** and no `N` constraints → `s39o/rpatN.txt`.

## 4. Off-centre embeddings (the `offc` flag)

For every accepted K and every row degree d = 7..DMAX (17), enumerate every embedding φ of K into the **abstract**
degree-d window, whose slot letters are unknowns:

- φ is injective into the known vertices `{u, w_i, s_i}`;
- `φ(x) = u` only if `deg_K(x) = d`. Otherwise `deg_K(x) ∈ 5..8` and the image slot is pinned to that letter. Letter 9 never
  matches, and an unknown (private, ring-3) vertex is never an image (strict §14′);
- induced: for images a, b, `ab ∈ K` iff they are adjacent in the window (section 1). The `s_{i-1} s_i` pairs whose `w_i` is
  not an image become a letter condition on `w_i`: {5} if the edge is in K, {6,7,8,9} if it is not;
- every 3-clique of K lands on a window face (section 1).

Each φ gives the pattern `{φ(x): {deg_K(x)} for x with φ(x) ≠ u} ∪ {w_i: condition}`. Embeddings are enumerated up to the
rotations of the window (the first vertex in order goes to u, w_0 or s_0). The patterns are canonicalised over the 2d
symmetries and added to `PATS[d]` with source tag `OFFC`. The embeddings include those through u, so "anywhere in the
1.5-ball" includes the centre.

Because the result is ordinary patterns, the existing machinery stays **exhaustive**. The separator DFS (all modes, every d ≤
DMAX), `admissible()` (warm rows, lowerR2 row re-derivation), upperR2 and binderR2 all skip a killed arrangement and keep
searching. No post-filter is needed. The tail d > DMAX stays pattern-free, as before. The result is cached as a pickle keyed
by the md5 of the recorded entries, `offc.py` and DMAX (`offccache=DIR`). A67 builds in about 117 s; a cache read takes
under 2 s.

A67 numbers (args_A67 + rpatD): 20,315 entries → 15,990 distinct configurations → 14,722 new patterns (d7 5,731; d8 4,845;
d9 2,759; d10 860; d11 125; d12 72; d13..17 66 each). Adding rpatN gives 14,758.

## 5. Worked example: d12 row 555555555555/757575757575

Window: twelve 5s around u (12), and `s_even = 7`, `s_odd = 5`. Every `w_i = 5`, so all `s_{i-1} s_i` are edges. The 7 at `s_0`
has known neighbours `w_0, w_1, s_11, s_1` (all 5) and 3 unknown ring-3 neighbours.

`f7_.....55_....575` (pat= D, `r=8 m=5`): EX = `w5=5 w6=5 s4=5 s5=7 s6=5`, |EX| = 5 = m, so u is not part of K. K0: edges
w5w6, w5s4, w5s5, w6s5, w6s6, s4s5 (w5 = 5), s5s6 (w6 = 5), E = 7. `r = 27 − 7 − 15 + 3 = 8` ✓. K is a 7 with a fan of four
5s, where the two middle 5s are adjacent and the outer ones are joined to it through them. In the d12 row it embeds with
`s5 -> s_0 (7)`, `{w5, w6} -> {w_0, w_1}` and `{s4, s6} -> {s_11, s_1}`. Every image is exact with equal degree. The pairs
`w_0 w_1`, `w_0 s_11`, `w_1 s_1`, `w_0 s_0` and `w_1 s_0` are edges, `s_11 s_0` and `s_0 s_1` are edges because w_0 and w_1
are 5, and the non-edges `s_11 w_1`, `s_11 s_1` and `w_0 s_1` are non-edges. The faces `w_0 w_1 s_0`, `w_0 s_11 s_0` and
`w_1 s_0 s_1` are faces. u is not used. It embeds 12 ways: 6 sevens, ×2 for the orientation. The resulting pattern at d = 12
is `w_0 = w_1 = 5, s_0 = 7, s_11 = s_1 = 5` (plus rotations and reflections).

The seven off-centre hits on this row are the registry's `f7_.....55_....575`, `f8_......55_.....575`, `f9_.......55_......575`,
`f10_........55_.......575` and `f11_.........55_........575`, which are the same 5-vertex K, all `u ∉ K`. Add
`f7_...5555_.......` (u ∈ K, a 7 with four consecutive 5s; here it is centred on an s 7, the same graph) and the 2026
configuration `nl0040_r8` (from rpatN under offc). All fire (control (b)). Explore's `rsst023_122o122` is the same graph as
`f7_...5555_.......`. Our raw `rpatD` copy `122.122` keeps u (no `r/m` on record), so it does not fire off-centre here.

## 6. Physical test (control (c))

`offc_phys.py NROWS SEED [broken]`. For every sampled row, it builds the actual plane 2-ball as a networkx graph (u, link,
ring-2 arcs with privates, the faces of section 1). It re-derives every configuration independently: name entries from the
networkx graph of their own name window with the section 2 rule, and rpatN from the kc file itself. It then runs node-induced
subgraph isomorphism (`GraphMatcher.subgraph_isomorphisms_iter`) with degree pins on exact vertices and a face check on
triangles. Each `(row, configuration)` pair is compared with the engine's `offc_embed` patterns on that row. The broken
control (`offcbroken`: the engine takes `s_{i-1} s_i` as adjacent whatever `w_i` is) must give mismatches.

## 7. Controls (results in LOG.md, round s39o)

(a) Flag off reproduces A67 (`sol_q66.json`, `cert_q66L.json`): binder loads, `LOWER-R2: VALID t ≥ 55686/438047` and
`UPPER-R2: FEASIBLE at t = 0.128957775395`. (b) The d12 row's 7 off-centre hits fire. (c) The physical test gives 0
mismatches, and the broken control gives > 0.
