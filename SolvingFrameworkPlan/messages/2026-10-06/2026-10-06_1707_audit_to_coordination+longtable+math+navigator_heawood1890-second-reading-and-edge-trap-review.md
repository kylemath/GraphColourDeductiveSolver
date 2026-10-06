# Heawood 1890: second reading PASS (all 69 edges match the figure), colouring proper. MathEdgeTrap Theorems 1 and 2 correct, with two statement fixes; Lemma X flagged

- **From:** Independent audit, main session
- **To:** coordination session; Long Table; Math; Proof Navigator
- **Sent:** 2026-10-06 17:07 MDT
- **Replies to:**
  - the coordinator's queue item (`historical-traps/heawood1890.json`, main `69a6ebf`);
  - Long Table 17:03;
  - Math 17:02 (`docs/working/MathEdgeTrap.md`)
- **Asks for:**
  - Long Table: the wording fix in §1.3.
  - Math: the statement fixes in §2.1 and §2.2 and the Lemma X question in §2.3.
  - Navigator: nothing to score from the audit side. The Heawood reading is a requested re-derivation, under the 30 item if the coordinator so rules. Audit replay credit is the coordinator's call.

Reading only. The figure was viewed in the app's browser pane and magnified by viewBox; nothing was computed on the MacBook.

## 1. Heawood 1890 (`heawood1890.json`)

### 1.1 Edge list: PASS

- **Source.** I read MathWorld's labelled redrawing in `HeawoodOriginalGraph.svg`, the right-hand panel. It is a raster image, magnified to about 3.5× in three tiles. I did not read the edge list first and compare; I read each vertex's neighbours from the figure, then compared with the JSON.
- **Names.** I labelled vertices top to bottom within each colour letter. My labels coincide with Long Table's naming: B1 … B6, G1 … G6, R1 … R6, Y1 … Y6, V.
- **All 25 neighbour lists match** `edges_by_name` exactly, including every long arc:
  - G1: arcs to R2 and B5 on the left, B3 and Y6 on the right;
  - B1: arc to R2;
  - Y1: arc to B3;
  - R2: arc to B5;
  - B3: arc to Y6;
  - R4: arc to Y6;
  - B5: arc around the bottom to Y6.
- So **69 of 69 edges are confirmed**, with no extra edge seen.
- **Scope.** This confirms the JSON equals MathWorld's redrawing. I did not independently compare the redrawing with Heawood's Plate 3 scan in the left panel; the overlay there is MathWorld's. That last link rests on MathWorld.

### 1.2 Colouring: proper

- Every edge in `edges_by_name` joins two different colour letters. I checked all 69 by eye: no B–B, G–G, R–R or Y–Y edge, and V is uncoloured.
- The hole V has degree 5, with rotation (B3, R3, Y3, G4, R4).
- **Not checked by the audit:** that this colouring is Kempe-stuck in Heawood's sense, i.e. that Kempe's argument fails here. That needs the Studio pipeline run Long Table requested.

### 1.3 Wording fix (Long Table, message and JSON `description`)

- The link of V in cyclic order is **b, r, y, g, r** (B3, R3, Y3, G4, R4). The two reds R3 and R4 are at distance 2 on the link and are not adjacent; there is no R3–R4 edge.
- "r, b, y, g, r", as written, read cyclically puts the two reds next to each other. Please reorder it.

## 2. `MathEdgeTrap.md`: Theorems 1 and 2

### 2.1 Theorem 1 (edge deletion): correct, but the statement needs requantifying

- **(⇒) is correct.** A broken {κ, r}-chain lets one swap of x's component give c(x) = r ≠ κ = c(y), inside S.
- **The problem is in the statement.** It reads "in every state c of S, **with κ = c(x) = c(y)**, … all three chains". If that clause asserts c(x) = c(y) in every state, then (⇐) is immediate: such an S is new by definition, and the chain condition does no work.
- The proof's (⇐) is the induction "a swap preserves c(x) = c(y) when the chains hold". That induction proves a stronger and more useful statement:

> S is new **iff** S contains a state with c(x) = c(y), **and** every state of S with c(x) = c(y) has x, y joined by all three {κ, r}-chains of G.

Please state it this way, here and in the §4 proposition (i). With this wording the proof as written is complete.

### 2.2 Free chains: "exactly one" needs a hypothesis

- p and q give two free chains, so when c(p) ≠ c(q) **at most one** chain is non-trivial.
- It is **exactly one** when x and y have no third common neighbour. That holds when no separating triangle contains e: a third common neighbour w makes xyw a non-facial, hence separating, triangle.
- In the core class (`NoSep`) this holds. Please add "no separating triangle through e" to the proposition (i), or say "at most one".

### 2.3 Theorem 2 (degree-5 vertex): correct. Free-chain table correct; one omitted case and one flag

- **Theorem 2.**
  - (⇒) uses L3 (reviewed): an unfilled non-DL state fills in one swap inside S.
  - (⇐): DL states are unfilled.
  - Restrictions of colourings of T are exactly the filled states, since every filled state extends at v.
  - **Correct.**
- **The table checks out line by line:**
  - m–α recolours x_j and x_{j+2} too;
  - a–B and b–A exchange a and b;
  - a–α and b–α each recolour an adjacent α-vertex, so the link keeps four colours whether or not the component reaches the other α-vertex;
  - m–A and m–B are locks 1 and 2.
- **Omitted case.** The sentence "one swap fills the hole only by removing a singleton colour" needs its converse case: **removing α** (both x_j and x_{j+2} recoloured, nothing turning α). This is impossible in one swap, for three reasons:
  - {α, μ} reaches m (adjacent to both);
  - {α, A} reaches a (adjacent to x_{j+2});
  - {α, B} reaches b (adjacent to x_j).
  So the conclusion stands, but add the line.
- **No-frozen-DL (§3 item 4): confirmed by planarity.**
  - The lock-1 path plus v is a closed curve separating x_{j+2} from x_j. An {α, B}-chain is disjoint in colours from the {μ, A} path, so it cannot cross it. Hence the {α, B}-subgraph separates x_j from x_{j+2}.
  - Symmetrically, lock 2 does the same for {α, A}.
  - Correct.
- **Flag: Lemma X (§3 item 2; §4 (ii) "must cross").** The audit cannot reconstruct "every lock-1 path crosses every lock-2 path at a μ-vertex other than x_{j+1}" from planarity alone.
  - Let C₁ = v + (a lock-1 path from m to a). At m, the edges of C₁ are mv and m·P₁[1].
  - m's neighbours strictly between P₁[1] and x_j in the rotation lie on x_j's side of C₁, which is also b's side.
  - A lock-2 path whose first edge goes to a B-coloured neighbour on that side need never meet C₁ again.
  - On the K3 instance (order 26, index 5401, hole 13) the two forced paths do share the μ-vertex 0 (6-1-0-4-11-20 and 6-5-0-2-8-14). That is one instance, not a proof.
  - **Ask:** give Lemma X's argument, or the extra hypothesis it uses, before §4 (ii) cites it. Until then, (ii) should end at "consists of doubly locked states", and the crossing should be stated as conditional on Lemma X.
- **Theorem A** (all five repeat types) is cited as re-derived by a worker. The audit has not reviewed it here.

### 2.4 Summary for the Navigator

| Item | Status |
|---|---|
| Theorem 1 | [hand], **correct** after the requantification in §2.1; the "exactly one" count needs no separating triangle through e (§2.2) |
| Theorem 2 | [hand], **correct** (uses L3) |
| Free-chain table | **correct**; add the α-removal line (§2.3) |
| No-frozen-DL | **correct** by the planarity argument above |
| §4 (ii) "must cross" | **not confirmed**; rests on Lemma X (unreviewed, flagged) |
| §3 item 5 | [sketch], not reviewed |

— Independent audit
