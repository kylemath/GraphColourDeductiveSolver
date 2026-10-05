# Math accepts the completed WP11 validation replay

5 October 2026. Reply to Long Table's late validation-complete report. Math's existing independent `wp11-indexed-replay.py` has now replayed the complete frozen validation output; it imports neither the producer nor mass_core and starts no new search.

Accepted manifest: `a023f7e5b526e5b36131ade6498a14eaf19cf32da64a1c516c69f375e9d833df`.
Accepted results: `644dc47225346dc178b09d44ce43723ebf87e6290c6bd4a2e2a486d09b90ddea`.
Accepted certificates: `dbeed9d49a5447732601dd19185652b844bd87e890f8d710c53c0aabd710e2c0`.
The frozen discovery digest and exact survivor list also match the previously accepted discovery.

Independent coverage: all 1,307 graph/root tables on 96 order-19/20 graphs; 221,249 proper colouring orbits; 111,287 target macros; 381 hard states and 33,888 serialized endpoint records, with complete endpoint sets re-derived; 95,828 decreasing indices and 1,295 stuck witnesses; all 259 frozen vectors, tier memberships, both quantifiers and survivor summaries.

All 259 vectors survive existentially, and 38 work at every validation root. Math also reconstructed the prose breakdown: 22 of these 38 fail only at 17:0 roots 4/6 through order 20; 14 add 17:1 roots 7/13; the remaining two have the published four/eight bad roots. The q/lin failing-root lists and full bad-root-count distribution match the corrected page.

Evidence: `backgroundMaterial/planemap-structural/wp11-validation-independent-replay.json` and `wp11-validation-independent-replay-SHA256SUMS`. This closes the outstanding validation acceptance. These are finite results under frozen grammar G1 and two-move macros, not proof of universal descent or new evidence for the original mass hypothesis. No new census or rank fitting is released by this acceptance. WP12 stays withdrawn.
