# R* by selection: pair holes, three selection statements, kill tests (Long Table sub-agent, 6 Oct 2026, about 15:30 MDT)

Labels: [hand] argued here, unreviewed; [sketch] direction only; [read] read off committed records, with no new search. The only compute on this machine was a census of degrees and triangulation checks (0.04 s), plus a 0.04 s smoke test. Script: `backgroundMaterial/planemap-structural/longtable/explore-vhphi/pathways/sel_selection.py`. Notation follows `rstar-tait-angle.md` and `pd2_lock_proof.md`. **pure-clean(v)**: no Kempe class of T − v is targetless.

## 1. Two holes u, v at distance 2 (the pentakis pair)

In the pentakis dodecahedron, u and v at distance 2 share an *edge* ww′ of degree-6 vertices. This is a 5-6-6-5 diamond with ring 8. Seen from u, v is the ring apex w_k over the link edge ww′. It is a degree-5 ring vertex with exactly one outside neighbour.

- **Lemma 0 (no common state) [hand].** In every 4-colouring of T − u, the 5-cycle N(v) uses exactly 3 colours, so v is coloured and has no choice. A state at u is DL only if N(u) uses 4 colours, and then it is not a state of T − v. **Consequence:** a targetless class at u and a targetless class at v never share a state. The statement **P: "u or v is pure-clean"** has no coupling at the level of states. Any proof of P must derive graph structure from a targetless class at u and use it at v. That is a configuration argument, i.e. an item for the selection list (§2), with nothing gained from the pair. **P is parked, not killed.** It is consistent with every record, because no targetless class has ever been seen (Studio intel 15:03), so data cannot test it.
- **The joint-move version is a different target, J2 [hand].** Delete both: in T − {u,v}, require that every Kempe class contain a state in which *both* links use ≤ 3 colours. Then J2 for one pair implies the Four Colour Theorem directly. In a minimum counterexample, T − {u,v} is 4-colourable by minimality; J2 fills both links; u and v are non-adjacent, so both can be coloured.
- **Proposition J [hand].** If pure-clean(u) holds, every class of T − {u,v} that contains a state with N(v) on ≤ 3 colours contains a goal state. *Proof.* Colour v; this gives a state of T − u. Take a T − u Kempe path to a filled state. Each T − u swap of a component K restricts to swaps of the components of K − v in T − {u,v}. ∎ **So, given R* at u and at v, J2 can fail only at a double-DL class**: a class of T − {u,v} where both links use 4 colours in every state. That is the whole new content of the pair idea.
- **Where the Tait criterion enters [sketch].** In T − {u,v}, a lock path of u that ran through v is cut. By L3 (an unfilled state that is not DL fills in one swap), u then fills in one swap, possibly making N(v) 4-coloured: the hole "teleports" from u to v. In T − {u,v}, w has only deg w − 2 coloured neighbours: w′ plus a 3-path y1 y2 y3. So w is often free, and recolouring w changes both links at once. **A double-DL class needs every lock path of each hole to avoid the other hole, at every state.** No contradiction found; Lemma 0 shows this is not about R*.

## 2. Selection statements "some degree-5 vertex has property X"

| X | proved clean when X holds? | unavoidable? | verdict |
|---|---|---|---|
| **X1**: ≥ 4 neighbours of degree 5, i.e. (5⁵) or (5,5,5,5,d) | **yes**: Theorem H and Theorem HP (compiled) | **no.** Pentakis; the stacks S(n,r) below for r ≥ 3, n ≥ 6; sixring28; 13 of the 19 distinct Studio radius-5 graphs [read] | **keep as list item 1.** It already covers T4, A_r, belts G_n (holes (5,5,5,5,n)), and 6 radius-5 graphs (80b930d1, 91a307d1, 2a9ef333, 59998957, 5b7066bf, f1d2cb92). For R* their radius-5 holes are irrelevant. |
| **X2**: all five link degrees ≤ 6 | no (open rows) | holds in all 25 distinct graphs in hand (named + certificates), but **X1 ∨ X2 is killed [hand + census]** | **killed** |
| **X3**: some hole with ≤ 2 big neighbours (the 300-bounty class suffices) | open | **no**: pentakis (5 big), S(n,3) (3 big) | **killed as a stand-alone selection** |
| **X4**: an X1 hole, or some hole with max radius ρ ≤ 3 | no proof route yet | T4 has ρ = 4 at **all 12 holes** (`pb_hi.out`), but T4 has X1. All 19 radius-5 certificate graphs have min-ρ ∈ {2, 3} [read, meta.json] | **kept (data level).** Kill test T3 |

**The stack family S(n,r) [hand + census].** Take r stacked n-gonal antiprism rings with two poles of degree n. Then S(5,r) = A_r and S(n,2) = belt G_n. For r ≥ 3:
- every degree-5 vertex lies in an end ring;
- its link is (n, 5, 6, 6, 5): three big neighbours, one of them the pole, of unbounded degree;
- the census confirms Euler, min degree 5 and no separating triangle for n ≤ 12 and r ≤ 4;
- all degree-5 vertices are equivalent under the symmetries.

So **S(n,3), n ≥ 7, kills X1 ∨ X2**. **Any unavoidable list needs an item with ≥ 3 big neighbours including one of unbounded degree.** This corrects `rstar-selection.md` §3: the belts were the wrong witness, because Theorem HP covers them. Because the degree-5 vertices are equivalent, a targetless class at one of them would refute R* for S(n,r) outright. S(n,r) is a sharp family, like pentakis.

## 3. Studio kill tests (exploratory; caps per run; nothing run here beyond the smoke test)

The script is `sel_selection.py` (stdlib; reuses `pb_lib`, Math's `graphs.py`, and the order-28 faces in `docs/66666/build_data.py`).
- **T1, stacks:** `stack 6 3`, `stack 7 3 one`, `stack 8 3 one`, `stack 7 4 one`, `stack 9 3 one`.
  - Output: states, classes, **targetless classes**, and max radius at one representative hole.
  - **Kill:** any targetless class kills R* for that graph. Also watch for radius growing with n: unbounded radius in a family that selection cannot avoid.
  - Orders 20 to 30. Estimate 10³–10⁵ states each, about 10 CPU-min cap per graph.
  - Check first: S(6,3) (n = 20) and S(7,3) (n = 23) may already be in Math's exhaustive census of orders ≤ 23.
- **T2, two holes:** `pair pentakis` (one pair suffices by symmetry), `pair sixring28 all`, `pair T4 all`, `pair S6_3`.
  - Output per diamond pair: classes of T − {u,v}, **J2-FAIL classes** and **double-DL classes**.
  - **Kill J2:** any J2-FAIL class.
  - 26 to 30 coloured vertices, 10 CPU-min cap per graph.
- **T3, X4 aggregate:** over *all* Phase C and D graphs (not only the certificate graphs), report per graph: whether it has an X1 hole, and min over holes of ρ.
  - **Kill X4:** a graph with no X1 hole and min-ρ ≥ 4.
  - Cost is about zero, because the per-hole ρ is already recorded. `certmin` does this for the certificate files.
- **T4, for Math's `vdred` (configuration test, owner Math):** the pentakis 2-ball plus the stars of its five degree-5 ring apices. That is 20 inside vertices with ring m₀y₀m₁y₁…m₄y₄ (10). It sits between the failing 2-ball and the passing, pentakis-specific 3-ball. Second configuration: the 2-ball of S(n,3) at an end-ring vertex, n = 6, 7, 8, to see whether depth grows with n. Cost: like the pentakis 3-ball (11 s) up to about 10⁶ game nodes.

## 4. Kills and keeps

- **Killed:** X1 ∨ X2 (by S(n,3)); X3 alone; "selection lowers the radius target below 4" (T4).
- **Parked:** P (no mechanism, by Lemma 0).
- **Kept:**
  - X1 as list item 1, with its coverage;
  - J2 as an alternative 4CT-sufficient target, reduced by Proposition J to "no double-DL class";
  - X4 as a data-level guide;
  - S(n,r) as a new sharp family for the adversary.

## Caveat added 6 Oct, evening (the coordinator's census, Studio, orders 12–22)

About 97% of degree-5 hole instances have a single Kempe class of T − v. There, R*_v only re-checks colourability. So radius data from single-class holes, including most of the figures above (T4 − v is a single class of 1,632 colourings), **is not evidence for R***. Only multi-class instances count. Selection statements should be judged on multi-class holes.
