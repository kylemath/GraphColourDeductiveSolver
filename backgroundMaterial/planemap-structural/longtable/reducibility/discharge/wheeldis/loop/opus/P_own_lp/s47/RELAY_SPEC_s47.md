# RELAY_SPEC s47: separation and upper check for l3qV V = 8 (stack l3qV=7,8 with fb6)

s47, 21 Oct 2026. This is a delta on §44 (`P_own_lp/s44/RELAY_SPEC_s44.md`, fb, including the §44.8 lowerR2 repair) and §45
(`P_own_lp/s45/RELAY_SPEC_s45.md`, l3qV row terms, tables and pricing). §21 (`P_own_lp/s28q/RELAY_SPEC_s21.md`) is the V = 7
construction and is unchanged. §45.5 left `solveR2` and `upperR2` refusing any l3qV ≠ 7 because separation and the upper check
were not built. This round builds them **for V = 8 only** (first-order pricing: V = 8 bundle rc −12/421 on the s42a A78 cert,
V = 9 prices at 0). `l3qV` containing 9 is still refused by `solveR2` and `upperR2` (exit 7).

> **Provenance** (unchanged from §45): the 7 → 8 channel is part of RSST rule 9 / Gonthier's `drule9` (payee letter 7+) and
> of the 2026 set's rule009. Any number from an l3qV run must cite RSST drule9 and 2026 rule009 as the source.

## 47.1 Engine
- `P_own_lp/s47/eng` is built in this order:
  1. a copy of `s44/eng` as of commit 4045b217 (the §44.8 repair) — the `.py` files, `jsep6.cpp` and `bin/`;
  2. `python3 s45/port_l3qV.py s47/eng/prelay2.py` (§45: option, V-tables, row terms, mrowL labels, lowerR2 label check);
  3. `python3 s47/port_s47.py s47/eng` (this section: prelay2.py and pcheck.py);
  4. `s47/eng/jsep7.cpp` = `jsep6.cpp` plus the edits of §47.3, compiled `g++ -O3 -march=native -std=c++17 -pthread -o bin/jsep7 jsep7.cpp`.
- md5s are in `s47/engine_src_md5.txt`.
- **Default `l3qV=7`.** Every new branch is guarded by `8 in LQVX` (or `LQVX` non-empty), and `LQVX` is empty by default.
  The binary selection falls back to the s44 one. So the default code path is s44/eng's (control (a)).

## 47.2 What is unchanged
- **Row terms** are §45.2 exactly: payer −1 on `lq[(8, c, a, a2)]` in d = 7 receiverR2 rows at every link 8, both sides; payee
  +1 on `lQ[(8, c, a', m)]` in d = 8 receiverR2 rows at every link 7, both sides; m = T_8(σ, c, w2, w3, w4, a', o) (§45.3).
- **mrowL** rows, labels `['mrowL', [8, c, a, m], [8, c, a, a2]]`, one per a2 ∈ m, generated in the solve exactly as for V = 7
  (the first time a receiver row's coefficients contain `('lQ', (8, c, a, m))`).
- **Caps and penalties.** `lq[(8, ·)]` is a `lq` column: bounds [0, lqcap] (lqcap = 3 in every run), cost xpen under keeppen,
  cost reset to 0 when the penalty is removed. `lQ[(8, ·)]` is ≥ 0, uncapped, no cost. lowerR2 prices `lq` at lqcap (all V).
- **lowerR2** is s45's (V = 8 rows re-derived by `recv_coef_R2`; V = 8 mrowL labels accepted by s45's check), on top of §44.8.
- **senderR2 rows** have no l3q terms (V = 7 or 8), so their generation and their upper check are unchanged.
- **cons2 rows** (6-centred conservation) have no l3q terms: `cons2_coef` and `cons2_delta` read only g, h, v, z6/Z6 and fb;
  l3q's payer is a 7-centre and its payees are 7- or 8-centres. So cons2 separation (`cons2_delta` over all 5^6 apex words) and
  the conservation part of the upper check are unchanged. "Covering the conservation side" therefore means: nothing to add,
  and this is a reading choice (R2 below), not an omission.
- **d ≥ 9 rows, the tail d = 18..30 and Karp** are unchanged (V = 9 not built; no V = 8 term at d ≥ 9).
- The **V = 7** window term, leaf correction (jsep5 / jsep6 argv[7]) and l3q.bin are unchanged, except that the V = 7 payer array
  PQ is filled from 3-tuple `lq` keys only (R8).

## 47.3 Separation and upper check (the new code)
Both `solveR2` (mode 2, top K distinct rows) and `upperR2` (mode 0, every violated row) evaluate a receiver row as
**window sum + leaf corrections**. The V = 8 terms are added in the same two places as V = 7 (§21.6):

**(i) Python, after every LP (solve) / on loading the solution (upper): `write_l3qV(8)`** writes `WORK/l3q8.bin`, called at the
end of `write_l3q`. Layout identical to l3q.bin: `QX8[2·5^6]`, `PQ8[125]`, `MK8[2·5^6]`, float64.
- Index of a table key (σ, c, w2, w3, w4, a, o): `((((((σ=+1 ? 0 : 1)·5 + c)·5 + w2)·5 + w3)·5 + w4)·25 + a·5 + o` with letters
  as indices 0..4 (5..9).
- `Qeff8(c, a, m) = max(lQ[(8, c, a, m)] from the LP/solution (0 if absent), max_{a2 ∈ m} lq[(8, c, a, a2)])`.
- `UB8(c, a) = max over the V = 8 table's keys with that (c, a) of Qeff8(c, a, mask)`; 0 for (c, a) outside {5, 6}^2.
- `QX8[i] = Qeff8(c, a, m) − UB8(c, a)` (≤ 0) and `MK8[i] = m` at every table key; QX8 = 0 and MK8 = −1 elsewhere.
- `PQ8[(c·5 + a)·5 + a2] = lq[(8, c, a, a2)]`; 0 elsewhere.
- Noise: as `write_l3q` — if QX8.max > 1e−15 or PQ8.min < −1e−15, assert |noise| ≤ 1e−9 and clip (log line `write_l3qV: noise`).

**(ii) Window term (`l3q_winV`, prelay2.py, called right after `l3q_win` in `window_table_R2`).** Only for U = 8 (so only
d = 8 rows). At a window whose centre slot is a link 7 (index c = 2), add `UB8(e, r) + UB8(b, q)`, where the window is
(a, b, c, e, f; p, q, r, s) = (w_{i−2}, w_{i−1}, w_i, w_{i+1}, w_{i+2}; s_{i−2}, s_{i−1}, s_i, s_{i+1}):
+ side c = w_{i+1} = e, a = s_i = r; − side c = w_{i−1} = b, a = s_{i−1} = q. This is `l3q_win` with UB → UB8 and U = 7 → U = 8.
The **payer** term at a d = 7 link 8 is ≤ 0 and is **not** put in the window (as V = 7's payer): the window stays an upper bound.

**(iii) Leaf correction (`bin/jsep7`, argv[9] = l3q8.bin).** After the V = 7 block and its prune test, for the full row:
- d = 7: for every i with w_i = 8 (index 3), σ = +1 then −1: `tot −= PQ8[(W(i+σ)·5 + W(i+2σ))·5 + W(i+3σ)]`.
- d = 8: for every i with w_i = 7 (index 2), σ = +1 then −1: c, w2, w3, w4 = W(i+σ), W(i+2σ), W(i+3σ), W(i+4σ);
  a = S(i) if σ = +1 else S(i−1); o = S(i−1) if σ = +1 else S(i); `tot += QX8[index(σ, c, w2, w3, w4, a, o)]`.
  Indices mod 8, so w4 is the antipode w_{i+4} = w_{i−4} on both sides.
- then `if (!(tot > cut)) return;` (the prune test, as after the V = 7 block), then the fy2 block if any.
- Every correction is ≤ 0, so every DFS bound (window sum, H, V) stays an upper bound and the leaf value is the exact row load
  at Qeff8. jsep7 refuses a file with QX8 > 1e−15 (exit 12) or PQ8 < −1e−15 (exit 13), unreadable file exit 11.
- **Mode-2 distinctness:** the row's class multiset gets `1200000000 + payer index` for every d = 7 link-8 side with c, a
  indices ≤ 1 (letters ≤ 6), and `1300000000 + (c·5 + a)·32 + MK8` for every d = 8 link-7 side with MK8 ≥ 0 (V = 7 uses
  1000000000 / 1100000000).

**(iv) Binary selection (`run_sep`, pcheck.py).** jsep7 runs iff `LQVX` is non-empty, `l3q8.bin` has been written and
d ∈ {7, 8}. Arguments: `hdr win threads sym cls|none bonus|none(d≠7) l3q.bin|none(d≠7) none l3q8.bin`. With `fy2` it replaces
jsep6 at d = 7, 8 with the same first 8 arguments plus argv[9]. Otherwise the s44 choice (jsep5 at d = 7 with l3q, jsep3/4 else).

**(v) upperR2 additions.** Q is Qeff8 for every mask, so every V = 8 mrowL row holds by construction (as §21.3 for V = 7).
The solution's `lq`/`lQ` keys are checked: a key that is not a 3-tuple must be (V, c, a, a2) / (V, c, a, m) with V ∈ l3qV,
c, a ∈ {5, 6}, a2 a letter, 0 ≤ m < 32; otherwise the check stops with `SOLUTION HAS lq / lQ KEYS OF A FAMILY THAT IS OFF OR
MALFORMED` (so a V = 8 solution checked with the default l3qV=7 is refused, not silently read as V = 7). lq values must lie in
[0, lqcap] and lQ ≥ 0 (all V, unchanged line).

## 47.4 Reading choices (all of them, for a spec-only reproduction)
- **R1.** UB8 is a max over the *table's* masks for (c, a), not over all 32 masks (as V = 7). With a full table (5000 masks) every
  mask a row can read is in it. A partial table (`l3qpartial`) is used only by controls (b) and (d), never by a run.
- **R2.** No l3q term in senderR2 or cons2 rows, V = 7 or 8 (§47.2). Separation and upper check of those rows are untouched.
- **R3.** The d = 7 payer term at a link 8 is leaf-only (−PQ8). Nothing is added to U = 7 windows in a real run.
- **R4.** Leaf order: V = 7 correction → prune test → V = 8 correction → prune test → fy2. At d = 8 the V = 7 block is inactive
  (it is d = 7 only), so only the V = 8 payee block applies there.
- **R5.** The side loop is σ = +1 then −1 at each position, as V = 7; the payer key's c, a, a2 are read along u's link away from
  the 8 (i+σ, i+2σ, i+3σ); the payee key's apex a is the apex across (w_i, w_{i+σ}) — s_i for +, s_{i−1} for − — and o the other.
- **R6.** A d = 8 link-7 side with c or a ≥ 7 has QX8 = 0 (MK8 = −1) and UB8 = 0: no term, no id. A d = 7 link-8 side with c or
  a ≥ 7 has PQ8 = 0 (no such column exists): no term, no id.
- **R7.** Distinctness ids as (iii); they only affect which of several equal-class rows mode 2 returns, never a load.
- **R8.** `write_l3q` (V = 7) fills PQ from 3-tuple keys only; V = 8 keys go to PQ8 only. The two families never share an entry.
- **R9.** The V = 8 table is `s45/l3qtabV.py EXDIR TD TC OUT sg 8 exname=s40f/exname_rm128.txt`, full (no `keys=`), both sides.
  On both registries the exname hold-out removes nothing from the l3q registry (A83: 4500 → 4500; A78: 4412 → 4412), so the
  table equals the no-exname one. No pcell mask clearing (PCL3) is applied to V = 8 tables (pcell is not used by these runs).
- **R10.** The tables are loaded by `l3q_loadV` (§45), which asserts 5000 masks unless `l3qpartial`.
- **R11.** `brokensignV` (control (c) only): the d = 7 payer term at a link 8 is read with the wrong sign and coarsened to keep
  the DFS sound: U = 7 windows at a link 8 (index 3) get `+ max_{a2} lq[(8, e, f, a2)] + max_{a2} lq[(8, b, a, a2)]`
  (+ side c = w_{i+1} = e, a = w_{i+2} = f; − side c = w_{i−1} = b, a = w_{i−2} = a), and PQ8 is written as 0.
- **R12.** The solve's mrowL generation, the cert labels and lowerR2's label check for V = 8 are s45's port items 3 and 4.

## 47.5 Tables
| registry | file | masks | md5 |
|---|---|---|---|
| registry | file | masks | md5 |
|---|---|---|---|
| reg_A84 (main 517b0129), σ = ±1 | `s47/tabV8_A84/tabV8_{1,-1}.json` | 2 × 2500 | built by the launcher once reg_A84 is ready (`s47/tabV8_A84.sh`); md5s land in `s47/tabV8_A84/md5.txt` |
| reg_A83 (main 240b5a08), σ = +1 | `s47/tabV8_A83/tabV8_1.json` | 2500 | b0115b14c4bc57b264784eed6cbad884 |
| reg_A83, σ = −1 | `s47/tabV8_A83/tabV8_-1.json` | 2500 | 38c234742881dc134bff2df12c098c4c |
| reg_A78 (controls), σ = +1 | `s47/tabV8_A78/tabV8_1.json` | 2500 | b0115b14c4bc57b264784eed6cbad884 |
| reg_A78, σ = −1 | `s47/tabV8_A78/tabV8_-1.json` | 2500 | 38c234742881dc134bff2df12c098c4c |

- The A83 and A78 V = 8 tables are byte-identical (50 of 2500 masks per side differ from 31). The run target moved to A84
  after they were built; the A83 tables are kept as a record, not used by any run.
- The 8 masks of s45's cert-key tables (`s45/tabV/tabV8cert_{1,-1}.json`) equal the full A78 table at those keys (`ctl_tabcheck.txt`).

## 47.6 Controls (all nice 10, threads 1; logs in `s47/`)
Inputs: the s42a A78 solution `s42a/run_A78/sol_q42aA78.json` and cert `cert_q42aA78L.json`, s42a's arguments (reg_A78,
exname `s42a/exname_A78.txt` = the same 128 names as exname_rm128, rpatN3, `l3q lqcap=3`, no fb).

| control | what | result |
|---|---|---|
| (a) | s47/eng, default l3qV, `upperR2 nomax` on sol_q42aA78 | log **byte-identical** to `s42a/run_A78/upper.log` with the `, N.Ns)` timings stripped (`ctl_a_diff.txt` empty); FEASIBLE at t = 0.109439356774 |
| (b) | same with `l3qV=7,8` (s45 cert-key V = 8 tables, `l3qpartial`) | **FEASIBLE at t = 0.109439356774** (`ctl_b_upper_V8.log`) |
| (b') | same with the full A78 V = 8 table | **FEASIBLE at t = 0.109439356774** (`ctl_b2_upper_V8full.log`); with timings stripped it differs from (a) only by the two added `l3qV:` lines |
| (d) | `lowerR2` on cert_q42aA78L with `l3qV=7,8` (cert-key tables, `l3qpartial`) | **VALID t ≥ −244/421** (`ctl_d_lower_V8.log`), equal to s45's l3qV=7,8,9 pricing run (`s45/pricer45_q42a.out`): 44/421 − 3·(24 + 24 + 48)/421, the three negative V = 8 lq columns (8,6,5,5), (8,6,5,6), (8,6,6,5) priced at lqcap 3; no negative lQ |
| (d') | same with the full A78 V = 8 table | VALID t ≥ −244/421 (`ctl_d2_lower_V8full.log`) |
| jsep7 | `test_jsep7.py` (as s28q/test_jsep5.py): random windows, random V = 7 and V = 8 q / Q, random mask tables; every mode-2 row jsep7 returns at d = 7, 8 vs the Python load (window + `l3q_terms` + `l3q_terms_payeeV` at Qeff / Qeff8) | **2400 rows, 0 mismatches** (d = 7: 100 rows with V = 8 payer terms; d = 8: 1200 rows with V = 8 payee terms). Broken control (no l3q8.bin): 1398 mismatches (198 at d = 7, 1200 at d = 8) |
| (c) | hand-made V = 8 solution: sol_q42aA78 with t + 0.003 and q[(8, 6, 6, 5)] = 0.002 (Q left to Qeff8), full A78 table (`ctl_c/sol_f1.json`) | correct check: senders 0, conservation 0, **d = 7: 0 violated**, d = 8: 6 violated → INFEASIBLE (6). **brokensignV: d = 7: 20 violated** (cap of the report; all on link 8665566, the row carrying lq (8,6,6,5) twice, excess 0.001 = 2·0.002 − 0.003), d = 8: 6 → INFEASIBLE (26) |
| (c, partial) | t + 0.02, q = 0.015, cert-key tables | correct d = 7: 0, d = 8: 20; broken d = 7: 20, d = 8: 20 |
| (c3) | q[(8, 6, 6, 5)] = 1, t + 0.02 | d = 8: 20 violated (payee credit live) |
| (c4) | the V = 8 solution checked with default l3qV=7 | refused: `SOLUTION HAS lq / lQ KEYS OF A FAMILY THAT IS OFF OR MALFORMED (l3qV=7): [(8, 6, 6, 5)]` |
| (s1) | smoke solve: `solveR2 l3qV=7,8`, warm = first 3000 rows of rows_q42aA78, 3 LP rounds, then lowerR2 on its cert | runs through jsep7 at d = 7, 8 (rows added at every d each round), the LP uses V = 8 columns (5 lq > 0, 3 lQ > 0), its cert has 2 V = 8 mrowL rows and lowerR2 accepts it (VALID −1: an unconverged early LP, a mechanics check only) |

**What (c) shows and what it does not.** The mis-signed payer term makes the check fail at d = 7, on the rows carrying the V = 8
payer key, where the correct check finds none. A hand-made solution that the correct check accepts *in full* could not be
built from sol_q42aA78 by adding q8 and raising t: the rows that bind at d = 7 (8665566, lq (8,6,6,5) twice) and at d = 8
(lQ (8,6,6,31) twice) move by the same 2·q, so any (Δt, q) that clears d = 8 also clears the broken d = 7 rows (scanned
(0.003, 0.002), (0.02, 0.015), (0.4, 0.2), (1.0, 0.5); with large q, d = 8 rows with three or more (6, 6) link-7 sides bind first).
A fully feasible V = 8 solution needs a re-optimised LP (the stacked run).

## 47.7 Run (launcher `s44/run44d.sh`)
- **Registry A84** (main 517b0129, 2,707 D / 1,218 C, `s33z/reg_A84`, prep `s33z/prep_tag.sh A84 517b0129`).
- Flags: `xon apexcls filt16 killtab=reg_A84/f/kill/kill6 hat5 consall l3q l3qtab=reg_A84/tab_{1,-1}.json lqcap=3 fb fbdir=6
  fbcap=3 l3qV=7,8 l3qtab8=s47/tabV8_A84/tabV8_{1,-1}.json rpatN=s39o/rpatN3.txt`, args reg_A84/args_A84.txt, rpat rpatD.txt,
  exname s40f/exname_rm128.txt (the same 128 hold-outs as run44c), consbasis s21/cf/cons2basis_cls.json.
- **Hold-out check at A84:** `out/job30/ringmerge_cpat_sweep.out` at 517b0129 has md5 a2ec92e5…, identical to the 618c0899 and
  240b5a08 copies, with 129 FAIL lines; those minus f9_....5565B_....6655. are exactly the 128 names of exname_rm128. The
  launcher repeats this check at start and stops (exit 6) if it fails.
- Engine s47/eng, tag q47A84, outputs `s47/run_A84/`. Stages as run44c: K keeppen (xpen 1e−3, lpmax 900, 4 h cap) → L nosep +
  binder_keys → lowerR2 → U upperR2 nomax → binderR2.
- Warm: run44c's rows (`s44/eng/rows_q44fbA83*.txt`, `s44/run_A83/rows_q44fbA83*.txt`) + run44c's warm list (s44 A78, s42a A78,
  n3 A74 rows + the s42a WQ set). Warm rows are re-derived with the s47 flags, so they carry their V = 8 terms.
- Order: hold-out check → wait for `s33z/reg_A84/prep_done.txt` → start the A84 V = 8 table build in the background →
  wait for run44c (`s44/run_A83/ALL.done`, or the run44c.sh PID read once by `pgrep` at start no longer alive, `kill -0`) →
  wait for `s47/tabV8_A84/tabV8.done` → stages. Warm rows from A83 are re-admitted only if `admissible` at A84. nice 10, threads 1 (TH=2 in the environment raises it).
