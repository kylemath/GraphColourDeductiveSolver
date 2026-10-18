# Round B5 (Long Table request, 18 Oct 23:30Z): RSST rules on the d=7 receiver 7665566 / 6675666

Reading: u of degree 7, link w0..w6 = 7,6,6,5,5,6,6, s_i the second-ring vertex between w_i and w_{i+1},
s-word s0..s6 = 6,6,7,5,6,6,6. Free: the six privates of the link (w0 has 2, w1, w2, w5, w6 one each, the fives none),
each in {5,6,7,8,9+}, 5^6 = 15,625 cases; third ring free. Private key in `sweep.out` lists them in ring-2 order
starting after s6: (w0, w0, w1, w2, w5, w6).

- `score.py` (round B1's RSST port and disc builder, same method as R*): u's RSST score, min and max over the third
  ring. min = max in every case. **3,072 cases score 0; 12,553 are non-zero** (1: 5,888, 2: 4,480, 3: 1,760,
  4: 380, 5: 43, 6: 2). Max score never negative.
- `contain.py` (own containment test, new this round): an RSST configuration "appears" when its inner vertices map
  injectively to disc vertices of known degree (u, link, second ring only) with equal degrees, matching cyclic
  neighbour order (either orientation) and an induced inner subgraph. A disc 9 means 9+ and is never matched in
  the strict mode. **All 12,553 non-zero cases contain a published configuration, strict mode, for every third
  ring** (`contain.out.gz`: key, score lo, hi, first hit strict, first hit with 9 = 9).
  Most frequent first hits: 2.126 (3,125), 3.1324806 (2,400), 122.61866 (1,728), 2.260517966 (1,600), 122.126 (1,600),
  122.431 (1,536), 2.7566 (500), 122.368 (64).
- Control (`rstar_control.py`): on R*'s non-zero cases (round 42 found each dead to RSST configurations) the test
  hits 300/300 sampled; it also hits 135/300 R* zero-score cases, as expected (configurations can appear anywhere).
- One engine (our code). Studio's independent cross-check, as for R*, would make it two.

**Two-engine check (23:55Z).** Studio's independent scoring (`studio_lt7_cases_31dc6d2e.txt`, copied from
loop/studio/rsst_rules/rsst_lt7_cases.txt at 31dc6d2e) against ours, case by case: same 15,625 keys both ways
(0 only-Studio, 0 only-ours), 0 charge mismatches with the privates in the same order; Studio's configuration count
is >= 1 in every one of our 12,553 non-zero cases, and Studio has no non-zero case without a configuration.
