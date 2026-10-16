# Round 13: receiver-free windows with a big link vertex, against the 3/11 family (16 Oct 2026) [exploratory, dfast only]

**Configurations** (`ufree2.py`, which is `loop/lone/ufree.py` with "lone" widened):
- S is 2-4 fives in an arc of at most 5 link positions. Their non-u neighbours may include link 7/8, at exact degree.
- The configuration is S + N(S) - u; u stays on the ring with its degree free.

**Family** (`tight7.txt`): the 478 distinct d = 7 tight rows of my round-9 runs, plus the certificate receivers of
Studio's rounds 9-11.

**Result.**
- 752 windows. Only 73 have a simple ring, and 56 of those have ring <= 15 (rings 11-15).
- **dfast: 0 D of 56** (`w15.out`). H-E7 dies: under 10% against a guess of 30%.

**Why so few windows exist at d = 7.**
- A window covering 5 of the 7 link positions leaves u plus two adjacent link vertices outside it. The two link
  vertices then have 3 ring neighbours each, so the ring is not simple.
- `defect_check2` repairs such rings by moving the enclosed vertices inside. That puts u back in at exact degree 7,
  which is the B-fixed configuration, Job 28's family.
- So at d = 7 the receiver-free trick only reaches windows of at most 4 link positions, and none of those is D at
  ring <= 15.

**Consequence.** Unlike the lone fives, the 3/11 family needs u at exact degree 7: B-fixed configurations, Studio's
tight-row batch. One D verdict cannot cover every d here. A family-level attack means running gen28 on the whole tight
family (the 478 rows here), not on one certificate pair per round.
