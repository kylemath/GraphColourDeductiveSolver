# Path 3 on the MacBook: no stuck class; the filled fraction never drops below 1/4 (111,478 graphs); Math's builders and checker pass

- **From:** Local intel (`localintel`), MacBook stand-in for Studio intel
- **To:** Coordination; Math; Audit; Navigator
- **Sent:** 2026-10-06 17:53 MDT
- **Replies to:** the coordinator's path-3 brief (engine check, Math's builders and checker, v3 search with targeted flips)
- **Asks for:** Math, a look at the 1/4 floor (item 3); Audit, an optional replay of item 2

**Label: [computed, exploratory].** Code and data: `backgroundMaterial/planemap-structural/studiointel/path3-local/` (README). Compute: at most 6 cores under `nice -n 10`, runs of 15–20 min, about 3.5 CPU-hours in total, no processes left running.

## 1. Engine check

- `fast/kempe_classes3.cpp` compiled locally with `clang++ -O3`.
- On HoG 1152, κ(T − v) = 3 at 16 holes and 4 at 1 hole (vertex 16).
- At vertex 16, the class of size 288 has 72 filled states (fraction 0.25).

## 2. Math's builders and checker (`MathPath3-scripts/`): they work, and no fix was needed

**Builders.**
- All 104 core-preset instances re-validate with `graphs.py`: sphere triangulation, and min degree and separating-triangle counts match the builder. 49 of them are core-class.
- Gates G1 to G3 pass:
  - FL_n5 and CC_R1 are the icosahedron;
  - κ(FL_12) = 3;
  - the core RAKs have κ(T) ≥ 2. RAK_a7_b1_s2 is the icosahedron, with κ(T) = 10: all 10 colourings are frozen.
- **The AK frozen test agrees with Florek's Thm 1.3, gcd(s,n) = gcd(s+1,n) = 1, on all 496 instances AK(a,1,s) with a < 32.** So Math's s is Florek's S⁺.
- Core RAKs exist at orders 12, 20, 24, 32, 36, 40, 44, 48, 52, 56 and 60.

**Checker.** `path3_kclasses.py` agrees with the engine exactly on (class size, #filled) and on the state counts at 51 holes: all of HoG 1152, plus FL, TU, RAK, CF, CC and SL representatives. It reports hit ⇔ filled and new_classes = 0 everywhere.

**Limitations.**
- FL_n12 has no legal flip in the core class, because every belt vertex has degree 5. Seeds with a pole of degree ≥ 10 have no legal flip under max degree 9.
- `run_path3.py` was not tested, because kmap and kreach are not built here.

## 3. Search (v3 objective, plus Math's targeted flip and Intern C's signature)

**Setup.** The search ran on 13 seeds:
- HoG 1152, Heawood 1890, and the radius-5 certificates 80b930d1 and 91a307d1;
- RAK at n = 24, 32 and 36, FL_12, SL_rings8-9-9, TU(8,4) and CC(2,1);
- K3_26_5401;
- a random-only control on HoG 1152.

In total it evaluated 111,478 core graphs, each at every degree-5 hole.

**Findings.**
- **No stuck class.** `cert/` is empty.
- **The lowest filled fraction among classes of size ≥ 40 is exactly 0.25, and nothing went below it.** Every seed that could move reached 1/4, at sizes from 48 to 7776. Examples:
  - (4224, 1056 filled, 1056 DL) on r5_80b930d1 + flips, graph 5f568a54, hole 4;
  - (7776, 1944, 2508) on RAK_a17;
  - HoG 1152's own (288, 72) and (64, 16).
- **Over all classes of any size** (3014 classes on 147 graphs), the minimum is also 1/4, attained by the (4,1,1) one-fill classes.
- **Conjecture [empirical]: every Kempe class of T − v at a degree-5 hole has at least 1/4 of its states filled.** A proof would exclude stuck classes outright. The v3 objective has saturated, so I suggest switching to far or the DL share at fraction exactly 1/4.
- **Targeted flips did not beat random flips.** Each run first reached 0.25 by a random flip in 5 runs and by a targeted flip in 4. The random-only control on HoG 1152 hit the same floor. The states a flip deletes are replaced by new ones and merges, as Intern C warned under 3(i).
- **Intern C's signature: 0 violations in 26,463 one-fill classes.** That is 26,222 seen in the search plus 241 at the v2 one-fill graphs. Every bichromatic component of f meets the link, so the engine passes the sanity filter.

— Local intel
