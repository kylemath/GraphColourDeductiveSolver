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
