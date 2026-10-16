# Job 29 (Studio): neighbour-aware wlp3, DESIGN ONLY (not built, not run) [exploratory]

Written 16 Oct 2026 on Long Table's instruction. It is gated on the explore thread's oracle check H-B0. If H-B0 says the
lever is not there, drop it. Context: explore round 18 (`loop/lf/FINDINGS.md`).
- Every completion of the 49 hard d = 7 rows is killed by a D configuration centred at another 7.
- That 7 lies on u's link in 45% of cases and at ring 2 in 48%. It is never u itself.
- The single-receiver LP charges u alone, so it cannot use those kills.

## 0. Two levers, and which one the data asks for

- (L1) **Forbidding through neighbours (no new rules).**
  - A receiver row of u over arrangement a is needed only if some completion of a has no reducible configuration
    anywhere near u. That includes configurations centred at a neighbouring 7 v.
  - This lowers the max receiver load. It is what H-LF measured.
- (L2) **Big-to-big rules.** Charge moves along u–v edges between adjacent big vertices, depending on both 2-balls.
  - This is the RSST-style sharing of §7 class (b).
  - Test G showed that (b) alone cannot beat a closed defect. In combination with (L1) it can rebalance a 7 that is
    overloaded next to a lightly loaded big neighbour.
- **Recommendation:** build (L1) first as an *oracle cut* (§3), measure t*, and add (L2) only if (L1) leaves a
  binding pair u–v with slack at v. Both are specified below.

## 1. Joint (u, v) arrangement

- u has exact degree d (7..10 at first). v is a big vertex at distance 1 (a link position w_j ≥ 7) or 2 (an s_j ≥ 7,
  or a p-private ≥ 7 of a 6 or 7 link vertex).
- **Overlap.**
  - v = w_j: v's link contains u, w_{j−1}, w_{j+1}, s_{j−1}, s_j, i.e. 5 of v's d_v letters are in u's
    arrangement. Free: d_v − 5 link letters of v, plus v's s-ring, d_v letters of which 2 are in u's.
  - v = s_j: v's link contains w_j, w_{j+1}, i.e. 2 known letters. Free: d_v − 2 link letters, plus v's s-ring.
- **Joint arrangement J = (a, j, b_v):** a is u's arrangement (link w, s), j is the position, and b_v is v's 2-ball
  letters outside the overlap. A configuration centred at v (an f-window at v, or a B-free key) is read off b_v
  together with the overlap.
- **Canonical keys.** For a window at v, use lemmaA `la.ckey` on the configuration built from J, i.e. the ring-free
  canonical key of the interior graph with degrees. The explore thread's bridge (948 named D/C configurations
  already keyed by `la.ckey`) is the registry.
  - A joint arrangement is killed if some window at v that fits in J has a key in the D/C registry.

## 2. Rules (lever L2)

- New variables x[τ] ≥ 0 for an oriented edge type τ = (u's rooted word at v, v's rooted word at u). Here a rooted
  word is the vertex's link word starting at the other end, as wlp.py `root`, but for big vertices.
- These are restricted to d_u, d_v ∈ {7, 8} at first. Above that, the letter 9 = "≥ 9" stands, as now.
- **Receiver row of u:** Σ_{5-nbrs} y[root] + Σ_{big nbrs v} (x[τ(v→u)] − x[τ(u→v)]) ≤ d − 6 + t.
  - Inflow from v and outflow to v both depend on v's link word. So u's DP needs, at each big link position j, v's
    rooted word, i.e. d_v − 5 extra letters at position j. Note: v's s-ring is not needed for the rule, only for L1
    kills.
- **Sender rows:** unchanged.
- **Antisymmetry:** τ(u→v) and τ(v→u) are distinct variables, and both appear with opposite signs in the two
  receiver rows. Charge is conserved by construction.

## 3. L1 as an oracle cut (recommended implementation)

Embedding v's 2-ball in sep3's DP is too large (§5). Instead:
1. sep3 returns violated arrangements a, as now.
2. For each a, run a **completion oracle**:
   - defectb7-style search over the free letters of each big neighbour v at distance ≤ 2, with letters 5–9 and the
     p slots;
   - at each completion, check every window centred at those v against the `la.ckey` registry;
   - **a is killed iff every completion contains a registered D/C window.** This is the H-B0 oracle.
3. A killed a goes into a forbidden list, as an exact arrangement: `c` command plus a new `x` command in sep3. sep3
   is re-queried.
   - It must be forbidden exactly, not as a pattern, because the kill uses letters outside u's 2-ball that the
     pattern language cannot express.
4. Memoise by canonical arrangement key. Many violated a share their v-neighbourhood.
5. When the oracle times out (H-LF hit the 2-minute cap on 27 of 49 rows), do **not** forbid: an unfinished
   search is not a kill.

## 3a. The oracle: what it enumerates, and how much

**New code, `nbroracle`** (C++, reusing gen28's `make` logic for window building and the `la.ckey` key):
- It takes a u-arrangement a (d_u = 7: link w_0..6, s_0..6) and its big neighbours: v = w_j ≥ 7 (distance 1) and
  v = s_j ≥ 7 (distance 2).
- **Per-neighbour test (sound and sufficient; the first version).** Forbid a if there is one big neighbour v of
  exact degree (letter 7 or 8) such that every filling of v's 2-ball outside the known letters contains a
  registered D/C window centred at v. This is weaker than "every joint filling dies somewhere", but it is a plain
  enumeration.
  - **v = w_j, d_v = 7.** v's link has 7 letters, 5 known (u, w_{j±1}, s_{j−1}, s_j), so 2 unknown. v's s-ring
    has 7 letters, about 2 known, so about 5 unknown. That is about 7 unknown letters, **5^7 ≈ 7.8·10^4 fillings**.
    Each filling needs the windows at v (up to 2^5 sender sets, most pruned by ring > 16) built and keyed, about
    20–50 µs each. That is **≈ 1–3 min per (v-overlap key) uncached**. This is right at the 2-min cap; with the memo
    keyed by v's known letters, a round reuses most of them.
  - **v = w_j, d_v = 8.** About 9 unknown letters, **5^9 ≈ 2·10^6 fillings**, so ≈ 40–100 min. These **time out**
    at a 2-min cap unless pruned. Pruning: stop a filling branch as soon as a window that fits is D; enumerate in
    DFS order, keeping the letters that most often complete a window first.
  - **v = s_j, d_v = 7.** Only 2 link letters are known, so about 5 + 7 = 12 unknown, **5^12 ≈ 2.4·10^8**. Out of
    reach without pruning, so skipped in the first version.
  - **v of letter 9+.** It has no exact degree, so windows centred at v do not exist. Skip it.
- **Joint test (complete; a later version).** No joint filling of all the neighbours' balls is window-free at every
  v. This is a CSP over the union of the balls (DFS with a check at each v once its ball is assigned). It is
  exponential in the number of big neighbours. H-LF's much smaller 6-sea space already hit the 2-min cap on 27 of 49
  rows, so expect **most** arrangements to time out.
- **Expected timeout fraction at a 2-min cap (first version).**
  - Arrangements whose only exact-degree big neighbours are 7s on the link: few time out once memoised, perhaps
    10–30% in the first round, falling after that.
  - Arrangements that need an 8 neighbour, or a ring-2 v: nearly all time out.
  - In the tight d = 7 family, the 7-on-link cases are what H-LF's kills used (45%). So the first version can at
    best reach about that share. Ring-2 kills (48%) need the joint or ring-2 version.
- **Before any forbid is trusted:** run the oracle on H-LF's 49 rows and compare. A forbid there must agree with the
  explore thread's kills. A disagreement points to a bridge or enumeration bug.

## 4. Soundness checklist

0. **(Long Table, first.) The oracle is NOT the 6-sea defect search.** defectb7 and defectc9, as the explore thread
   uses them, set everything outside K to degree 6. There, "all completions die" excludes *isolated defects* only;
   it says nothing about arbitrary neighbourhoods.
   - For a forbid, the oracle must enumerate every filling of each neighbour v's 2-ball, with every unknown letter in
     {5, 6, 7, 8, 9+}.
   - In the window match, 9+ is a *free B*: a window may use a 9+ vertex only as a ring vertex, never at an exact
     degree.
   - This is new code (§3a), not an existing tool.
1. **Completion exhaustiveness.** "Every completion dies" must range over all extensions consistent with a,
   including degrees ≥ 9 via the 9 = "≥ 9" letter. The configuration found must contain only exact degrees or free
   ring vertices; no exact 9 may stand for "≥ 9".
2. **Window validity.** A registered window at v must appear in G as built. That is the same caveat as all
   receiver-centred patterns: simple ring, and pinches as in `defect_check2`, i.e. filled variants. State it over
   filled configurations, as Job 26 notes.
3. **Bridge correctness.** An `la.ckey` match must mean an isomorphic interior with equal degrees and the same ring
   attachment. Test the bridge on a control set: H-LF's 50 / 50 control, plus a negative control of not-D keys.
4. **Timeouts are never kills** (§3.5).
5. **L2 conservation.** Every big–big transfer appears in exactly two receiver rows with opposite signs, including
   for d ≥ 11 via the Karp tail (add max outflow to the tail bound).
6. **Validation.**
   - With the oracle off and x = 0, it must reproduce the current t* (13/49 as of round 12).
   - With the oracle on and the D/C registry emptied, t* must not move.

## 5. Size of sep3's state

- **Full joint DP (not recommended).**
  - At each big link position j, add v's d_v − 5 free link letters (5^2 = 25 for d_v = 7) for L2.
  - For L1, add v's s-ring, about d_v further letters (5^7 ≈ 7.8·10^4). The per-position factor is about 2·10^6.
  - With up to 3 big positions at d = 7 that is beyond reach.
- **L2 only:** a factor 25 per big position, at most 3 positions at d = 7, so ≤ 1.6·10^4 on the bound matrices.
  - Still heavy. It is feasible with state merging, i.e. keep only v's rooted-word *class* used by the x variables
    (canonical up to reflection, about 40% fewer).
- **L1 oracle:** sep3 is unchanged except for an exact-arrangement forbid list. Its cost is in the oracle.

## 6. Cost estimate

- **L1 oracle cut:**
  - ~300 lines: oracle driver around defectb7 / defectc9, memo, sep3 `x` command, wlp3 loop.
  - Oracle CPU: H-LF used 2 min per row at K = 4 with free letters 5–7. The tight d = 7 family is ~200–600 rows
    per round, so ~10–20 core-hours per round at a 2-min cap, falling as the memo fills.
  - Wall time: about 1–2 days of work.
- **L2:**
  - ~400 more lines: x variables, joint state at big positions, Karp tail.
  - The LP grows by the number of x columns (≈ 10^3–10^4).
  - About 2–3 days, and only if L1 leaves big-big slack.
- **Cheapest first test (if H-B0 says go).** Run the L1 oracle offline on round 12's certificate and tight rows,
  forbid the killed ones, re-solve once, and report t*. This needs no sep3 change beyond the forbid list.
