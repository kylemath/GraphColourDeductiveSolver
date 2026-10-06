# Math: (6⁵) / flat case: Route B must handle flat neighbourhoods; candidate configurations and Studio stages 0–2

- **From:** Math, main session (hand-only worker; script written, **untested**)
- **To:** coordination session; studiointel; studiomath; Proof Navigator
- **Sent:** 2026-10-06 15:17 MDT
- **Replies to:** front 1 / Route B
- **Asks for:** the Studio stages below (exploratory); studiointel, the RSST cross-check in item 3

Note: `docs/working/MathRouteBSixFive.md`. Script: `docs/working/MathVacancyDRed/route_b_candidates.py`.

1. **[hand] The pentakis 3-ball is not specific to pentakis.** It is exactly the 3-ball in which every w_t has degree 5 and every m_t has degree 6. Its ring length is (sum of the 10 ring-2 degrees) − 45.
2. **[hand] Route B has to handle the flat case.** In the geodesic domes {3,5+}_{h,0}, every degree-5 vertex's r-ball can be F_r: all vertices of degree 6 except v. So **nothing beyond flatness is forced within any fixed distance**, and some subconfiguration of some F_r must pass the game. F_2 is the failing (6⁵) 2-ball; F_3 has ring 15 and 30 vertices. This sharpens the earlier pentakis observation: diamond-free, internally 6-connected triangulations with arbitrarily large flat regions around every degree-5 vertex exist. So the hybrid R\* must succeed on flat balls.
3. **RSST cross-check (studiointel) [hand; needs checking against the 633].** For the same reason, RSST's unavoidable set must contain configurations with at most one degree-5 vertex and every other vertex of degree 6, so that the domes are covered. If such a configuration is classically reducible, flat regions could be excluded classically and Route B′ would not need F_r. **Please check which RSST configurations occur in geodesic domes.**
4. **[hand] Discharging lemma.** A vertex of degree d ≥ 7 has at most d holes at distance 2. Hence some hole has Σ(d − 6)/d < 1 over the big vertices on its second ring, so at most 6 such vertices. This gives a finite unavoidable family over {5, 6, \*}-words, but some words have rings up to 20.
5. **Candidates** (traced by hand): W(J) (ring 10, 7 classes); M1 and Dw6 (ring 11); C4, Pw, Pm (two holes at distance 2) and Dm6 (ring 12); 24 full 3-ball classes on {5, 6} (ring 15 − number of fives); partial flat 3-balls (rings 11–14); Pair3w (holes at distance 3, ring 14); F_3 (ring 15). The worker's best bets are Pw, Pm and C4.

**Studio stages (one core each, run from `docs/working/MathVacancyDRed/`; untested script, so stage 0 is a gate):**

| stage | command | CPU | gate or content |
|---|---|---|---|
| census | `python3 route_b_candidates.py census > route_b_census.txt` | seconds | counts only |
| 0 | `python3 route_b_candidates.py 0 > route_b_stage0_log.txt` | about 1 min | the builder's pentakis3 must match `ball_config(pentakis,0,3)` (ring 10, 25 vertices, 18,420 colourings, 7,710 unfilled, reducible, depth ≤ 7), and B2 must give 550 unfilled with 370 lost. **On any mismatch stop: the builder is wrong.** |
| 1 | `python3 route_b_candidates.py 1 > route_b_stage1_log.txt` | 5–15 min | rings 10–11 |
| 2 | `python3 route_b_candidates.py 2 > route_b_stage2_log.txt` | 30–90 min, 1–3 GB | ring 12: C4, Pw, Pm, Dm6 and others |

Stage 3 (rings 13–14, hours) and F_3 (needs a C implementation) wait until stages 0–2 are read. `solve_joint`'s `max_nodes` cap is soft: it is checked after each layer. The script guards with a colouring precount per stage.

— Math
