# s78_kstar (Team D, round 6): W6's K* transfer as an engine family

Engine: `eng/` is a copy of `s75_teamA/eng` taken 17:32Z. Its Python files are byte-identical to s75 apart from the hooks listed below; their s75 md5s are in `eng/SOURCE_MD5_s75teamA.txt`. At 17:41Z jsepf was rebased onto the s75 **no-clamp** separator (`jsepf.cpp` md5 bd45945d, bin fbe2ad73). The unmodified nc source is kept as `eng/jsepf_nc_base.cpp`, the nc binary as `eng/bin/jsepf.s75nc`, and my diff as `eng/kstar_jsepf_vs_nc.patch`. The original `s75_teamA/eng` was never edited.

## 1. The family as implemented

**K\* = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]**, one amount column `ks[K1]` in [0, kscap] (default kscap = 3). Here B = {7, 8, 9+} and S = {5, 6}. Both endpoints have degree exactly 7.

A degree-7 vertex u pays K1 to a degree-7 neighbour v once per oriented match. Read u's link starting at v and walking toward c- (the common neighbour on the S side). The pattern is:

| position | vertex | condition |
|---|---|---|
| S.L0 | v | degree 7 |
| S.L-1 | c- | in S |
| S.L-2 | next link vertex of u | = 5 |
| S.L-3 | next again | = 5 |
| S.L+1 | c+, the other common neighbour of u and v | in B |
| S.A-1 | apex of u across the link edge (c-, S.L-2): the third vertex of that face, not u | in B |

The two orientations of one pair (u, v) cannot both match, because one needs c+ in B and c- in S and the other needs the reverse. So u pays v at most K1.

### Rows (centre link w_0..w_6, apexes s_i = apex(w_i, w_{i+1}))

**Payer row (d = 7 centre u).** For each link vertex 7 at i and each e1 = ±1, with c- = w_{i+e1}, the conditions are:
- w_{i-e1} in B;
- w_{i+e1} in S;
- w_{i+2e1} = 5 and w_{i+3e1} = 5;
- apex(i+e1, i+2e1) in B, which is s_{i+1} when e1 = +1 and s_{i-2} when e1 = -1.

Each match gives coefficient -1. Every letter involved lies in the payer's own 2-ball (link plus apexes), so the payer side is exact. No second-ring row family is needed: the payer context is a function of the row itself.

**Payee row (d = 7 centre v).** For each link vertex 7 at j (the payer u) and each e1 = ±1, set k = j + e1 (so c- = w_k), c+ = w_{j-e1}, a = apex(j, k) and o = u's other apex. Exact conditions:
- w_{j-e1} in B, w_k in S, a = 5.

Conditions read through a mask (credit when **possible**):
- **S.L-3**: the payer's private vertex next to a can be 5, i.e. bit 5 of `L3T[(e1, w_k, w_{j+2e1}, w_{j+3e1}, w_{j+4e1}, a, o)] & ~extra7(j, e1)`.
- **S.A-1** when c- = 5: c-'s other apex apex(k, k+e1) is in B. This letter is exact.
- **S.A-1** when c- = 6: S.A-1 is the 6's private vertex, and `(amask(k) & ~extra6(k))` must meet B.

Each match gives coefficient +1. Hidden letters are maximised slot by slot: the payee row takes the credit whenever some allowed letter fires the rule. This is the grammar's semantics and it over-counts inflow, so it is sound.

**All other rows** carry no K\* coefficient: senders, cons2, and receivers of degree 8 and above. Both endpoints of K\* have degree exactly 7.

### Separator (jsepf argv[13], d = 7 only)

**WIN.** At U = 7, `window_table_R2` adds `K1 * (KUB0 + KUB1)`. KUB is the payee slot evaluated in the window centred at c- = k, with two simplifications:
- L3T is OR-ed over w_{j+4e1}, the one letter outside the window;
- the f2b extras are dropped.

KUB0 is the case "payer at k-1", KUB1 is "payer at k+1". Each has 13800 windows set out of 5^9.

**Leaf.** After the f2b and q7m corrections and before EVAL, jsepf adds two terms:
- the exact payer outflow, -K1 per firing;
- K1 * (exact payee slot - KUB) for each window and side, where the exact slot uses amask & ~extra6 and L3T & ~extra7.

Both terms are ≤ 0. jsepf refuses a negative amount (exit 87) and refuses exact > KUB (exit 81), so K\* can never put a positive term outside WIN.

**nc slack.** Because every K\* leaf term is ≤ 0, K\* adds nothing to the nc SLACK. The K\* block exits on the plain cut. Nothing is clamped.

**Mode-2 ids.** The mode-2 class of a c = 0 window is (a, b, e, f, q, r), which does not contain p or s. K\* therefore pushes leaf ids: 1800000001 per payer firing and 1800000002 per payee firing.

### LP and checks

- `prelay2.py`: column `('ks','K1')` with bounds [0, kscap]. Under keeppen it carries xpen, like lq. Each iteration logs `kstar it N: t K1 rc`.
- Solution JSONs carry `'ks': [['K1', v]]` and `'kstar': true`.
- `upperR2` refuses in three cases: ks present while the flag is off, an unknown key, or a value outside [0, kscap]. In-out blends treat a missing ks as 0.
- `lowerR2` caps ks at kscap.

### Files

- `eng/kstar.py`: the Python family (exec'd after f2bglue.py).
- `eng/jsepf.cpp`: rebased onto nc, built with `c++ -O2 -std=c++17 -pthread -o bin/jsepf jsepf.cpp`.
- Hooks in `eng/pcheck.py`:
  - argv[13] is passed at d = 7;
  - jsepf stderr is now logged; s75 discarded it, so clamp and K\* counters were never visible;
  - a failure prints its exit code.
- Hooks in `eng/prelay2.py`, `eng/pinout.py` and `eng/f2bglue.py`: the `ksforce` test generator and the K\* coverage and window-gap stats.
- Control flags, never for real runs:
  - `ksplant`: the Python payee ignores extra7, so the C++ and Python values disagree;
  - `ksnowin`: no window bound, so jsepf must refuse.

Scripts:
- `env78.sh`: STACK=s75|s77, FAM=base|rrz|full, KS=0|1, KSCAP.
- `upper78.sh`, `runK78.sh`, `runL78.sh`, `watch78.sh`.
- `tests/`: the acceptance tests.

## 2. Reading of the grammar, and why

The orientation was taken from **W6's code**, not from the prose. `tests/w6/grammar.py` and `tests/w6/gext.py` are copied unchanged; their md5s are in tests/w6/SOURCE_MD5.txt. In gext.py `EPOS`:
- S.L±k is the sender's link counted from the receiver (S.L0);
- S.A-1 is the apex between S.L-1 and S.L-2.

The payer counts a slot only if the context surely fires; the payee counts it if it possibly fires (`coef_rows`).

`tests/test_orient.py` builds W6's own picture of each d = 7 arrangement, following `certpics.recv_pic`:
- link and apexes exact;
- 6-privates `amask & ~extra6`;
- 7-privates `L3T & ~extra7`.

It then compares grammar.py's column for K\* with the engine's K1 coefficient on every arrangement. Half the arrangements are planted with K\* patterns. Two controls:
- the mirror rule must also agree;
- a deliberately mis-oriented copy (S.A+1 instead of S.A-1) must disagree.

The only free choice I made is that a 9+ letter counts as B. B = {7, 8, 9+} in the grammar.

## 3. Tests (logs in logs/, scripts in tests/)

See REPORT.md for the numbers.

## 4. K solve (prepared, not launched)

See REPORT.md.
