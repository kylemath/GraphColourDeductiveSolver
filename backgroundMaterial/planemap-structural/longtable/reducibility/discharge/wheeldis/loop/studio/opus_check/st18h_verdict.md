# Stage 18 (RELAY_SPEC section 15, hat channel H5; Opus 8f71209b): Studio spec-only check

**Verdicts (19 Oct ~08:50Z):**
- **Upper: sol_st18h.json (md5 8b31e1712f4b5649ef58777931cdf9a4) is FEASIBLE at t = 17/107** on registry 880d25c6
  (argsA54_pinned). Log: st18h_check.log.
- **Lower: cert_st18hL.json (md5 e758d613025e4b2e5e972fbddec524d9) is VALID at exactly t >= 10/63.** All 138 rows were
  rebuilt. Log: st18hL_lower.log.
- **Both-ends key consistency:** 9,139 diamonds, 0 mismatches. Log: st18_keys.log.
- Re-solve: not done. Studio's own LP (wlp3r6) cannot express this class (g2/h2/filter/hat5). The fallback, the exact
  lower rebuild, is done.
- Flag-off regression: Studio cannot run Opus's engine. The 6/35 value is s19c's, which Studio second-checked
  (50150249).

## Independence statement
- Built from RELAY_SPEC.md alone: sections 12, 13, 14' and 15 at 8f71209b (14' layout from fcdd458e; the 15 prose fix
  at ee11d33e was not needed, since it changes no row). No Opus code was read.
- Opus files opened: RELAY_SPEC.md; sol_st18h.json; cert_st18hL.json; and st18h.log, only its "sender rows" count line,
  grepped to compare the structure count. File names in s18d/ were listed (git ls-tree), but no engine, cmd script,
  rows file, cons basis or other log was opened.
- Studio code: st18_keys.py (key reader and both-ends test, on explore's grow.py frames); st18_check.py (=
  st16_check.py + hat5); sep3r_ak.cpp (SEP_EXACT6 + SEP_RTAB); st16_filter.py kill tables (md5-identical to s16ap/kill6).

## Both-ends key consistency (st18_keys.py)
- 4,000 random grow.build2 frames centred on a big b (d in {7, 8, 9}, random link and ring letters): 9,139 diamonds
  (b, x, v, y) with v an apex five, covering all 25 (x, y) spoke shapes.
- K was read three ways: the sender-row formula (v's link, hat and fan classes), the receiver-row formula (b's link and
  apexes), and the physical reading from each spoke's rotation (v, other spoke, b, Z1, Z2 / Zo).
- 0 mismatches for sender vs receiver, sender vs physical and receiver vs physical, and 0 between the two orientations
  of v's link.
- Broken-key control (s_{i-1} and s_{i+1} swapped at the receiver): 12,706 of 31,954 keys change.

## Upper (st18_check.py, HAT5=1, V6=0, filter on)
- Registry: dcount 15,881. Patterns D 15,881 / C 1,679 / RPAT 158. r_3/r_4.cfast are empty in our root, so nothing
  was dropped.
- Bounds clean: 86 r values, 0 negative values, max x 0.077.
- senderR2 with all five hat classes enumerated: **20,676 rows** (equal to Opus's log), 0 violated (min slack −9e−14).
- cons2 (r does not enter): 1,424 × 729; 994 with a five, 0 violated; 430 without, 0 violated.
- Studio relaxed rows (+ relaxed r) vs spec rows: 820 arrangements, 0 mismatches, relaxed never below exact.
- C++ exact leaf weights vs spec rows: 220 compared, max 4.7e-10.
- Receivers d = 7..17, exhaustive (sep3r_ak, SEP_EXACT6 + SEP_RTAB; relaxed r in the bound, exact r at the leaf):
  **0 exact violators at every d.**
- DP d = 18..30 (Studio max-plus with the relaxed r) clean. Karp λ = 0.556074766, covering d >= 13.158.

## Lower (cert_st18hL, LOWER_ONLY)
- 138 rows (27 senderR2, 74 cons2, 25 mrowR2, 12 receiverR2), all mrowR2 canonical. tco = 1, **D = 10/63**.
- Nonzero reduced costs, all >= 0: M[766675531] 14/135, M[767675531] 14/135, M[777775531] 52/945, r[506506] 4/135,
  r[506507] 58/945, r[506509] 52/945, r[5067] 2/189, r[5068] 4/315, r[507508] 4/315, r[507509] 52/945.

## Readings
- Section 15's prose ("b sends r[K] to v") disagreed with its rows; Opus's ee11d33e corrected the prose to five ->
  big. Studio implemented the rows as written: the five's row +r, the big's load +r.
- Hats at five-spokes are enumerated without an extra admissibility test, since section 15 states none. The row count
  20,676 matches Opus's.
