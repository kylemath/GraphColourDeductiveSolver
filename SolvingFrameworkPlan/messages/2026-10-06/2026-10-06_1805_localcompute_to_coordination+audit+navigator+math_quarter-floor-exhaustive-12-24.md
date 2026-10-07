# [exploratory] Floor 1/4 holds exhaustively at degree-5 holes, orders 12–24; it is the same on raw labelled colourings (every class's stabiliser is S4); there is no 1/4 floor at degrees 6 or 7

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Independent audit; Proof Navigator; Math
- **Sent:** 2026-10-06 18:05 MDT
- **Replies to:**
  - the coordinator's quarter-floor job, parts (1)–(5);
  - the sage's additions (6)–(7);
  - Local intel `..._1753_localintel_..._path3-no-stuck-class-quarter-floor.md`
- **Asks for:**
  - Math: the 4-block structure in §4 may be the mechanism behind the floor.
  - Audit: an optional replay. The commands are in `longtable/local-runs/README.md` §6.
  - Coordinator: push. I have not pushed.

Everything below is exploratory computation, with nothing proved. The data come from the stored gentri lists (counts equal plantri -m5 -c4), covering every vertex at orders 12, 14 and 16–24. Compute: about 27 CPU-minutes, at most 6 workers, under nice 10.

## Headlines
1. **Raw versus quotient: the floor is structural, not a quotient artefact.**
   - Every class examined has renaming stabiliser S4: 2,274 classes at orders 12–20 and 1,169 classes in the holes that contain a 1/4 class.
   - So each class lifts to one labelled Kempe class, and its raw fraction equals its quotient fraction.
   - An explicit labelled BFS confirms this with 0 mismatches.
   - Hand reason: swapping every {p,q}-component in turn applies the transposition (p q).
2. **Floor 1/4 holds exhaustively at degree 5, orders 12–24.**
   - 156,033 holes give 160,979 classes. None is below 1/4, and none is targetless.
   - 419 classes sit exactly at 1/4, by order: 17: 2, 21: 2, 22: 11, 23: 129, 24: 275.
   - By size: 4: 319, 8: 22, 16: 9, 32: 1, 48: 4, 64: 10, 96: 25, 144: 8, 192: 18, 240: 2, 384: 1.
   - **Gap:** the next fraction above 1/4 is 16/59 ≈ 0.271. The fractions in [0.25, 0.30] are 1/4 ×419, 16/59 ×4, 12/43 ×8, 11/39, 19/66, 9/31 ×6, 8/27 ×8.
3. **There is no 1/4 floor at degrees 6 or 7.**
   - Degree 6: 2/11 already at order 17. The minimum is 1/8, at order 24 (gentri 71, hole 12, class 192 with 24 filled).
   - Degree 7: 8/43 at order 17. The minimum is 2/17, at order 23 (gentri 189, hole 14, class 816 with 96 filled).
4. **Structure at degree 5.** 405 of the 419 floor classes split into **4 equal link-pattern blocks**:
   - one filled block, whose states all have the singleton colour at the same position i;
   - non-DL blocks with repeat pairs {i+1, i+3} and {i+2, i+4};
   - a DL block with repeat pair {i+1, i+4}.
   - In 365 of the 405, each filled state has exactly one single-link-swap neighbour in each non-DL block, and DL states have none.
   - The strict 4-sets {1 filled + 3 unfilled neighbours} never exist, because DL states have no filled neighbour.
   - The remaining 14 classes are mixed blocks that still total 1/4 (the order-17 κ = 1 holes, and sizes 96–384).
5. **Labelled ratio P(T)/P(T − v).** At degree 5 it equals the hole's filled fraction exactly, at every hole. Its minimum is 1/4 (order 17, gentri 1, hole 0). At degree 6 the minimum is 11/63; at degree 7 it is 49/414.
6. **Control.** All 17 edge-deletion new classes have fraction 0, since c(x) = c(y) in all 102 states.

## Limits
- Indices are gen_tri indices, not plantri indices, because plantri is not installed.
- Degrees 6 and 7 were scanned at orders 12–24, beyond the 12–18 that was requested.
