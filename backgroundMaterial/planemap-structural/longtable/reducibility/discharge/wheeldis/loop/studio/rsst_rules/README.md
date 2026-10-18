# Independent RSST-rule scoring of R*'s centre (Studio, sealed task, 18 Oct)
`rsst_score.py` scores u (R*'s d = 7 centre) by RSST's 32 discharging rules over the 250,000 round-42 cases.
- Rules: Gonthier's Coq encoding (fourcolor proof/discharge.v, local opam install), 38 base parts with multiplicity,
  71 after symmetrize_drules. Semantics as stated in part.v/discharge.v; nothing from any other team.
- Geometry: grow.py's build2 (u, link, second ring, a fresh third ring).
- Result (`rsst_score.txt`): no case needed a third-ring degree, so every charge is exact.
  - RSST-free cases: 134,232, all with charge 0.
  - Cases containing an RSST configuration (grow.py containment, all 633): 115,768. Of these, 91,393 have charge 0,
    23,750 have +1 and 625 have +2.
  - Positive charge: 24,375 cases, all of them RSST-containing. The +1 comes from one extra unit into u from w2
    (12,500 cases) or from w4 (12,500), with 625 cases getting both.

## d = 7 receiver 7665566/6675666 (sealed, 18 Oct ~23:50Z): rsst_lt7.py
- The same scorer (rsst_score.py's rules and fit test, unchanged) on this arrangement, through grow.py's build2 with
  D, LK and SV swapped. Privates are derived from the arrangement: w_i has d_i − 5 of them, so w0 ×2 and w1, w2, w5, w6
  ×1, with w3, w4 (fives) none. That is 6 slots over 5..9 = 15,625 cases, with the third ring free. The code asserts
  that each s_i is adjacent to exactly w_i and w_{i+1}, the same reading as Team B's.
- Result (rsst_lt7.txt; per case in rsst_lt7_cases.txt):
  - Charge histogram 0: 3,072 / 1: 5,888 / 2: 4,480 / 3: 1,760 / 4: 380 / 5: 43 / 6: 2. All exact (no third-ring
    degree needed).
  - Non-zero 12,553, max +6.
  - Every non-zero case contains an RSST configuration (633, embedded in the 2-ball alone).
  - 0 embeddings need a 9+ vertex: variable slots take 5..8 only, and every fixed degree is <= 7.
- Not done: the per-case comparison with Team B's non-zero list. Reading their branch's result files was blocked by a
  permission denial on this machine.
