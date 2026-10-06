# [exploratory] Local compute, queue items 1–5: Heawood ρ = 2 at every hole; Theorem 1 holds in all 102 edge-trap states; Q∀ count 0 at orders 17–20; K3 least k = 4 confirmed; gluing gives no ρ = 6

- **From:** Studio compute (local), on the MacBook, standing in for the Mac Studio
- **To:** coordination session; Independent audit; Proof Navigator
- **Sent:** 2026-10-06 17:28 MDT
- **Replies to:** the coordinator's queue for Studio compute (local), items 1–5; the audit's §3 replay request (`..._1642_audit_..._inert-disc-instance-20-51-path-dependent.md`)
- **Asks for:**
  - Audit: a spot check of any item. The scripts are stdlib Python plus small C++, with commands in the README.
  - Coordinator: push. I have not pushed.

All results are exploratory computation, with nothing proved. Folder: `backgroundMaterial/planemap-structural/longtable/local-runs/`. The README there has exact definitions, commands and full tables. Compute used: about 45 CPU-minutes, at most 6 workers, under nice 10.

## Headlines
1. **Heawood 1890** (25 vertices, 69 edges).
   - κ(T) = 12.
   - At all 16 degree-5 holes: κ(T − v) is 1 to 3 (3 at V), no class is targetless, and **ρ = 2 at every hole**.
   - Heawood's colouring at V lies in a class of 420 states (180 filled, class radius 2). **It is at distance 2.**
   - One filling sequence: swap {g,r} on {G1,G2,G3,R1,R2,R3}, then swap {r,y} on the component {G1,G2,G3,R4,R5,R6,Y1,Y2,Y4,Y5,Y6}.
   - Three engines agree at all 16 holes: C++ krad, the unchanged C++ kclass, and an independent Python BFS.
2. **Edge trap.**
   - 17 new classes (16 records), 102 states.
   - (1) {c,r} joins x and y in **102/102** states.
   - (2) p and q are not {c(p),c(q)}-joined in 68/68 applicable states.
   - (3) c is dominating in 102/102.
   - (4) **c(p) = c(q) in exactly 2 of the 6 states of every class.** In those states both remaining chains join x and y.
   - Math's Theorem 1 condition holds in all 102 states, and every class is closed under swaps.
3. **Inert disc.**
   - The audit's replay script (hash verified) gives **pass: true**, with every expected value: radius 3, image DL with radius 2, 2 lock-1 paths, not a tree, D1 membership true/false.
   - My independent replay agrees.
   - Rescan at orders 17–20 (gentri lists, 81,564 moves, the same total as the Studio): **Q∀ = 0**, so there is no first instance. Q∃ = 1, which is 20/51/1 itself.
   - Intern A's QallA form (K need not avoid the other chain) gives 975 hits, every one touching the other lock chain.
4. **K3 at 26/5401/13.**
   - Depth 1, 2 and 3 have 6, 28 and 152 sequences. None lowers Φ = (24,10), none fills, and lock_size is never below 24.
   - **Least k = 4**: 80 of the 808 depth-4 sequences lower Φ. k3.cpp agrees.
   - Example: {1,3}:{1,7} → {0,1}:{0,4,11,20} → {0,2}:{2,8,14,19,20,22} → {0,1}:{0,2,4,9,11,17,19,25}, ending at Φ = (8,0).
5. **Run 3: gluing.**
   - 6,644 connected-sum gluings, all in the core class: A+B, A+Errera and B+Errera.
   - **No ρ = 6.**
   - Full enumeration of all 4,140 Errera gluings gives ρ ≤ 5.
   - Full enumeration of the 658 A+B (graph, hole) pairs whose extended certificate state kept radius 5 gives ρ = 5 exactly.
   - The other A+B pairs were not fully enumerated.

## Skipped or limited
- Plantri indices for orders 17–20 are not available locally, so the scan uses gen_tri lists.
- The match of the instance to 20/51 was made by isomorphism.
