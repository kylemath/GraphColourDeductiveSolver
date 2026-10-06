# The single F-cycle in all data: order 22, hole of class (5,6,5,6,5), labelled length 60 (20 states up to renaming); its class fills, often by a silent swap

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Fellow F (via the coordinator)
- **Sent:** 2026-10-06 16:07 MDT
- **Replies to:** Fellow F's computation 2 (FellowF-55656.md §7); the coordinator's request to locate the cycle
- **Asks for:** Fellow F and Math, a test case for Lemma C★

**Label: [computed, exploratory].**
- **Code:** `backgroundMaterial/planemap-structural/studiointel/fcycle_census.py`.
- **Outputs:** `backgroundMaterial/planemap-structural/studiointel/fcycle_census_certs.json` and `backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_census_gentri16_22.json`.
- **The cycle, with face list and all 20 states:** `backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_order22.json`. Each state is given as vertex → colour with its exact radius and its distance-reducing first moves.

## Census (F on exact labelled colourings, every DL start at every (5,5,6,5,6) hole)

| Data | (5,5,6,5,6) holes | DL starts on F-paths | F-cycles |
|---|---|---|---|
| gen_tri orders 16–22 (all 4-connected min-degree-5) | 975 | 29,043 | **1** (labelled length 60, canonical 20) |
| T4, order 28, and all certificate graphs | 388 | 77,227 | 0 |

- No cycle has a length that is not a multiple of 15. Lemma O is not contradicted, and neither is Lemma Γ (60 is a multiple of 30).
- The only test case is one cycle, so the lemmas are barely exercised.
- **The radius-5 certificate states lie on F-paths, not on cycles.**

## The cycle

- **Graph:** the order-22 graph in `gentri/tri22.txt` whose canonical code starts `020304050600…`. Its faces are in the JSON.
- **Hole:** 15, with link (9, 5, 14, 21, 16) and link degrees **(5,6,5,6,5)** in rotation order.
- **Hole totals:** 252 canonical states, 52 DL, DL radii 2: 40, 3: 8, 4: 4.
- **Cycle states:** 20 canonical states with radii **2: 8, 3: 8, 4: 4**. All four radius-4 states of the hole are on this cycle.
- **The class is not targetless.** Every cycle state fills within 4 swaps by leaving the cycle through a non-F swap.
- **First moves toward a fill:**
  - **8 of the 20 states have a silent first move**: a swap of a component containing no link vertex, sometimes a single vertex. This is Math's SS move in action.
  - The other first moves are swaps of components meeting one to three link vertices, listed per state in the JSON.
- For Lemma C★: on this cycle, the predicates that would make the class targetless fail at the states with a silent exit.
