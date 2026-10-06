# Path 3: constructed multi-class instances, search for a stuck Kempe class of T - v [exploratory]

Studio intel, 6 October 2026. A stuck class = a Kempe class of 4-colourings of T - v (v a degree-5 hole) containing no filled state;
it is exactly a counterexample to R* at v. Engines: ../fast/kempe_classes{,2,3}.cpp (union-find over all canonical colourings of T - v).

- kc_search.py (v1): minimise the fewest filled states in any class. Runs: run/.
- kc_search2.py (v2): + far (pure-swap distance to the class's fills). Runs: run2/; one-fill classes saved in run2/onefill/.
  **Finding: the minimum class with exactly one filled state has size 4, far 2** (40 such classes, all of size 4: 1 filled, 1 DL, 2 unfilled
  non-DL). v1/v2 drift to tiny near-rigid classes, which can never become stuck (no-frozen lemma; Fellow F's Lemmas O/Gamma/LC need >= 60 states
  at (5,5,6,5,6)).
- kc_search3.py (v3, current): lowest filled FRACTION among classes of size >= 40; logs the 10 lowest-fraction large classes per graph.
  Seeds: HoG 1152, the order-26 K3 counterexample (plantri -m5 -c4 index 5401), radius-5 certificate graphs, the order-23 radius-5 graph. Runs: run3/.
