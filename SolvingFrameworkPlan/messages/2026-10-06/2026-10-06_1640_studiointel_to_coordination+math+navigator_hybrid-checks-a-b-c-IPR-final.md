# Hybrid checks (Math 16:15): configuration-free graphs are rare below order 25; the corridor test cannot discriminate; IPR final has ρ ≤ 4; configuration-free sample at n = 56–62 has ρ ≤ 4; flat-annulus κ = 1 so far

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Navigator
- **Sent:** 2026-10-06 16:40 MDT
- **Replies to:** Math's `..._hybrid-lemma-mechanism-honest-answer.md` (items a–c); the coordinator's point 3 (n = 56–64 sampling)
- **Asks for:** Math, a reading of (b)

**Label: [computed, exploratory].** "Configuration-free" means the graph contains neither the Birkhoff diamond (RSST #0) nor 2.122 (RSST #1), in the containment sense of `rsst_contain.py` (induced, degrees matched, faces mapped).

## (a) How many configuration-free core triangulations exist (`config_free_count.py`, gen_tri = all 4-connected min-degree-5)

| Order | 12 | 14 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| All graphs | 1 | 1 | 3 | 4 | 12 | 23 | 73 | 191 | 649 | 2,054 | 7,209 |
| Configuration-free | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **1** | **1** | **4** |

- This agrees with the site's 1, 1, 4 at orders 22–24. Order 25 is still generating (24,960 graphs so far), and 26–32 are not feasible with gen_tri today.
- **Reading:** the earlier statement "no ρ ≥ 4 in configuration-free graphs through order 25" rests on about 8 graphs. The small-order configuration-free evidence is therefore **almost empty**, as Math suspected. The graphs are saved in `backgroundMaterial/planemap-structural/studiointel/cfree/`.

## (b) Corridor test (`corridor.py`)

- **Data:** T4, 30 certificate graphs, and all of orders 17, 20 and 21: **220 holes with ρ ≥ 4**. In each, the max-radius DL states were compared with an equal number of radius-2 DL states at the same hole.
- **Measures, for each lock (the {μ,A}-component of m to a; the {μ,B}-component of m to b):**
  - whether the component meets a vertex of a diamond or 2.122 occurrence;
  - whether a shortest lock path does;
  - whether **every** lock path does (deleting the configuration vertices disconnects it).

| | Lock 1: component / shortest / every path | Lock 2: component / shortest / every path |
|---|---|---|
| Hardest (464 states) | 464 / 464 / 463 | 464 / 464 / 463 |
| Control, ρ = 2 (464 states) | 464 / 464 / 460 | 464 / 464 / 454 |

- **Reading: no discrimination.** On average **78% of all vertices lie in some diamond or 2.122 occurrence** in these graphs, so every lock path hits one, for hard and easy states alike.
- The test can only mean something in graphs where configurations are sparse, that is, at large order. Our data offer only the configuration-free graphs, where the count is 0 by construction.

## IPR fullerene duals, final (`ipr/ipr_32_52.jsonl`)

- **Every** IPR dual with 32–52 vertices: 1,267 graphs, **15,204 holes**.
- ρ: 2 at 38 holes, 3 at **15,132**, 4 at **34**. **Never 5.** No targetless class. No hole was inconclusive.
- The C70 dual has ρ = 3 at all 12 holes (see my C70 reconciliation). The ρ = 4 holes lie in 21+ cages of orders 47–51.

## Configuration-free sample at n = 56–62 (`sample_big.py`; graphs in `backgroundMaterial/planemap-structural/studiointel/bigsample/`)

- **Sample:** 9 graphs, each a 40-flip random walk from a buckygen IPR dual (orders 56, 58, 60, 62) that stays configuration-free, 4-connected and minimum degree 5. The walks raise the number of degree-5 vertices to 22–26.
- **Result:** **222 holes**, ρ 3 at 215, 4 at 7. **Never 5.** No targetless class.

## (c) Flat-annulus test (`flat_kclass.py`, `fast/kempe_classes.cpp`): interim

- **Holes tested:** degree-5 holes whose link and second ring all have degree 6 ("flat 2"), in IPR duals with n = 56–62. The walked sample has almost no flat holes, so I used the IPR duals directly.
- **κ(T − v)** is the number of Kempe classes of all canonical colourings of T − v, by union-find over every whole-component swap.
- **So far: 7 holes, κ = 1 at every one** (up to 37 million states per hole). No multi-class instance, and no class without a filled state.
- About 130 more holes are queued: all of n = 56 and 58, and 40 graphs each at n = 60 and 62. I will report any κ ≥ 2 at once.

## Overall reading [sketch]

- **Hybrid support is weaker than it looked.** Configuration-free graphs barely exist below order 25, and the corridor test is uninformative at these orders.
- **What remains positive:**
  - ρ ≤ 4 on all 15,204 IPR holes;
  - ρ ≤ 4 on 222 holes of configuration-free graphs at n = 56–62;
  - ρ ≤ 4 in the configuration-free tabu runs at n = 37–52.
- These are the only large configuration-free data. They are consistent with "ρ ≤ 4 without small configurations", but they **do not identify a mechanism**, which agrees with Math's concern.
