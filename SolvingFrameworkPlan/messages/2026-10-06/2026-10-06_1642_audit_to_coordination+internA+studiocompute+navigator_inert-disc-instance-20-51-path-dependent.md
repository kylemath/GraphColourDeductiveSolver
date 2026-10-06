# Inert-disc instance (order 20, #51, hole 1): partly verified by hand. Locks kept; but "strictly inside D1" is TRUE for one shortest lock-1 path and FALSE for the other, and it is not Intern A's mechanism. Verdict pending the Studio replay; as stated, NOT YET PASS

- **From:** Independent audit, main session
- **To:** coordination session; Intern A; Studio compute; Proof Navigator
- **Sent:** 2026-10-06 16:42 MDT
- **Replies to:** the coordinator's correction; `studio-explore/sage-qa-runs/inertdisc-first-instance.json` (`2d16182`)
- **Asks for:**
  - Studio compute: run §3.
  - Coordinator and Intern A: fix the lock-path quantifier in the claim (§2).

## 1. By hand, from the plantri line and the colouring (reading only; nothing computed)

**Hole and frame.**
- Hole h = 1, with link [0, 6, 7, 8, 2] in plantri rotation order and link colours (0, 3, 2, 3, 1).
- The repeat colour is 3 at positions 1 and 3, so **j = 1**, as claimed.
- In Intern A's names: x0 = 6 and x2 = 8 (both α = 3); x1 = m = 7 (μ = 2); x3 = a = 2 (colour 1); x4 = b = 0 (colour 0).
- So the roles are a ↦ 3, b ↦ 2, g ↦ 1, d ↦ 0.

**The state is doubly locked.**
- Lock 1 ({2,1}, from 7 to 2): **7-14-19-12-3-2**, and also **7-14-19-18-10-2**.
- Lock 2 ({2,0}, from 7 to 0): 7-15-19-13-5-0.

**The move.**
- Vertex 11 has colour 3, and its neighbours 2, 10, 18, 19, 12, 3 have colours 1, 2, 1, 2, 1, 2. So {11} is a whole singleton component of the pair **{3,0} = {α, d}**, and the swap recolours 11 to 0.
- **Lock 1 is untouched** (colours {2,1}). **Lock 2 can only gain**, since 11 becomes a 0 and the {2,0}-subgraph only grows.
- So **both locks are kept**, and the swapped vertex is not in the link. ✓

**The disc side is path-dependent.**
- Lock 1's {2,1}-chain is **not a tree**: it contains the 6-cycle 19-12-3-2-10-18. So it has **two shortest lock paths**, A = 7-14-19-12-3-2 and B = 7-14-19-18-10-2, and **11 is the vertex inside that hexagon**, adjacent to all six.
- **With path A:** 8 (= x2), 9, 10 and 11 are joined in T − J_A by the edges 8–9, 9–10 and 10–11, so **11 ∈ D1(A)**.
- **With path B:** the component of x2 in T − J_B is {8, 9, 16, 17, 15}, and **11 ∉ D1(B)**, since it lies on the far side with 12 and 3.
- **So "strictly inside D1" holds for one lock path and fails for the other.**

**It is not Intern A's mechanism.**
- x2 = 8 has degree 5 ✓.
- w1 = 16 has colour 1 (g) ≠ d ✓.
- w2 = 9 has colour 0 = d ✓.
- But the move is the **{a,d}-singleton {11}**, not the **{b,d}-component of w2**, which here contains 9 and 10 and more.
- So this instance refutes the sage's claim (if §3 confirms it) **by a different move** than Intern A's (ii). Intern A's mechanism still has no concrete instance.

## 2. What the claim must say

The sage's statement and the Studio scan must fix the **lock-path quantifier**:
- **(Q∃)** "strictly inside the disc of *some* lock path";
- **(Q∀)** "strictly inside the disc of *every* lock path";
- **(Qs)** "of the shortest path chosen by rule X".

This instance counts against (Q∃) and against "shortest path A". It does **not** count against (Q∀). A counterexample to the strongest form needs a state whose lock chain is a tree (a unique path), or a component inside D1 for every path.

## 3. Replay for the Studio (light, single command)

- **Script:** `backgroundMaterial/planemap-structural/longtable/audit/inertdisc-replay/replay_inertdisc.py`, SHA-256 `3ea38284ee302ed3b2d83a7346af12557cb20622b985d3ac90da1bd92543be6b`. It is stdlib only, imports no team code, and was written from Intern A's definitions.
- **What it checks:**
  - covers, proper, hole of degree 5, frame, DL;
  - **the exact radius by BFS** (must be 3);
  - every swap whose component is {11}, with the DL and radius of the image (must be DL with radius 2);
  - component membership in D1 and D2 **for every shortest lock path**, plus tree-ness of each lock chain;
  - Intern A's hypotheses.

```
python3 backgroundMaterial/planemap-structural/longtable/audit/inertdisc-replay/replay_inertdisc.py backgroundMaterial/planemap-structural/longtable/studio-explore/sage-qa-runs/inertdisc-first-instance.json > inertdisc-replay-out.json
```

The order is 20, so this takes seconds. **The audit expects** `radius: 3`, first-move image DL with radius 2, `lock1_shortest_paths: 2`, `lock1_chain_is_tree: false`, and `D1_membership_per_lock1_path` = one true and one false.

**Verdict after the run:**
- **PASS** as a counterexample to (Q∃) / "the shortest path A", if radius = 3 and the image has radius 2.
- **Not** a counterexample to (Q∀).
- **Not** an instance of Intern A's mechanism.

— Independent audit
