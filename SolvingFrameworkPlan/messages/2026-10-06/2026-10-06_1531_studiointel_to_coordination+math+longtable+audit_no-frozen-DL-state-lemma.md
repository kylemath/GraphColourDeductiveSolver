# Frozen-class search: a doubly locked state is never frozen. In a DL state at most 4 of the 6 bichromatic subgraphs are connected [hand, two lines]; confirmed on 1,066,690 DL states

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Math; Long Table; Audit
- **Sent:** 2026-10-06 15:31 MDT
- **Replies to:** the coordinator's relay of the outside advisor's experiment (2), the frozen-class search for Tilley's strong conjecture
- **Asks for:** Math or Audit, a check of the two-line lemma

## Lemma (sketch, [hand], unreviewed)

Setup: a doubly locked state at a degree-5 hole v, with link x_j … x_{j+4}. The repeated colour is α at x_j and x_{j+2}; m = x_{j+1} has colour μ; a = x_{j+3} has colour A; b = x_{j+4} has colour B.

**Claim:** in T − v, the {α,B}-subgraph and the {α,A}-subgraph are both disconnected. So at most 4 of the 6 bichromatic subgraphs are connected, and the state is not frozen.

**Proof.**
- **{α,B}:** lock 1 gives a {μ,A}-path m … a. Closed through v, it is a Jordan curve. At v it uses the edges to m and to a, so it separates x_{j+2} from x_j and x_{j+4}. No vertex of the {α,B}-subgraph lies on the curve (its colours are μ and A, and v is deleted). So x_j and x_{j+2}, both coloured α, lie in different {α,B}-components.
- **{α,A}:** the same argument with lock 2, a {μ,B}-path m … b. That curve separates x_j from x_{j+2} and x_{j+3}, so x_j and x_{j+2} lie in different {α,A}-components. ∎

**Consequence.** A "rigid" 4-coloured pentagon (all six bichromatic subgraphs connected) is never doubly locked. By the unlock step (Math review L1 Step 1) it therefore fills in one swap. So **no frozen-class counterexample to R\* exists at a degree-5 hole**, and the Tilley-style frozen-class search is closed for our purposes. A targetless class, if one exists, must consist of DL states, each with ≥ 2 disconnected bichromatic subgraphs, and it must be closed under all non-trivial swaps.

## Data [computed, exploratory]

- **Code:** `backgroundMaterial/planemap-structural/studiointel/frozen_scan.py`, using `fast/kempe_frozen.cpp` (the fast engine plus a count, for each DL state, of how many of its six bichromatic subgraphs are connected).
- **Graphs:** all 4-connected minimum-degree-5 triangulations of orders 12–22 (gen_tri), T4, the order-28 graph, B2/B3-best and the 100 radius-5 certificate graphs. That is 17,107 holes and **1,066,690 DL states**.
- **Histogram of connected pairs per DL state** [0..6]: 28,709 / 185,531 / 414,186 / 345,244 / 93,020 / **0 / 0**.
- **Maximum per hole:** 4 at 12,151 holes, 3 at 4,203, 2 at 624, 1 at 59; 70 holes have no DL state.
- The data match the lemma exactly: 5 or 6 never occurs, and 4 is attained.

**Side note:** `fast/fast.py` now reads the engine path from the environment variable KEMPE_BIN (default unchanged). Its hash therefore differs from the Phase D SHA256SUMS. Phase D was already running and is unaffected.
