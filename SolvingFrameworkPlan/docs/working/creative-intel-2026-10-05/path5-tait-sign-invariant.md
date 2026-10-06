# Path 5: Tait sign sum with a correction at P, on T − v. The idea is dead.

Long Table, Path-5 agent, 2026-10-06. Labels: [hand] = proved here by hand; [exploratory] = smoke run (under 1 s).
Script: `backgroundMaterial/planemap-structural/longtable/explore-vhphi/pathways/p5_tait_sign.py`.

**Verdict.** I = S + g(word) mod 4 can be made a Kempe invariant. It is then **constant on every colouring of
T − v**, so it separates nothing. The mod-8 lift carries the one extra bit, and that bit is the disc-degree
parity already killed in `disc-degree-parity.md`. It is not constant even within one class. Path 5 stops for
this family of functionals (all linear functionals of the signed face counts plus a correction from the word).

## Set-up
H is the dual of D = T − v, and P is the degree-5 node. φ is a Tait colouring. s(n) = ±1 by the cyclic order
of the colours at a cubic node n. S = Σ_n s(n), and w is the cyclic Tait word at P (60 words, type (3,1,1)).

## 1. Cycles avoiding P [hand]
An (a,b)-cycle C alternates colours, so |C| is even. A swap reverses s on every node of C, so ΔS = −2Σ_C s.
That sum has an even number of ±1 terms, so it is even, and ΔS ≡ 0 (mod 4). ∎

## 2. P-paths [hand]
Take an (a,b)-path from P to P with k cubic nodes, so it has k + 1 edges. The edges alternate a and b. So k is even
when the two P-edges have the same colour, and k is odd when they differ. Then ΔS = −2Σ_C s ≡ 2k (mod 4).
The word changes by a↔b at the two ends: (a,a)→(b,b), or (a,b)→(b,a).
S mod 2 = #faces of D, which is fixed, so g mod 2 is constant. Write g = 2β. The constraint system is
**β(w') − β(w) ≡ [the two end colours differ] (mod 2)**, one equation for each planar (non-crossing) pairing move.
- [exploratory] With non-crossing pairings: all 60 words are connected and there are **0 contradictions**.
  β is unique up to a constant and depends on orientation. It is stored as a table in the script; no short
  closed form was found.
- If crossing pairings are allowed as well, there are 344 contradictions. So planarity is what makes the
  system solvable.

## 3. Why the solution is trivial [hand]
Translation by t ∈ Z₂² is a double transposition of the vertex colours. This is a rotation of the tetrahedron,
and it fixes every Tait colour. So s(n) = ε·(the orientation sign of the face's vertex colouring), with a single
ε for all four colour triples. Hence **S = ε Σ_F n_F**, where n_F is the signed count of faces coloured F.
On the disc, (n_F) is a 2-chain whose boundary is the walk γ(w), so (n_F) = n⁰(w) + d·(1,1,1,1). Therefore
**S = ε(f(w) + 4d)**. Two consequences:
- S mod 4 is a function of the word alone, so I is constant on all colourings.
- S mod 8 adds the bit d mod 2, which is the relative degree of `disc-degree-parity.md`.

More generally, any functional Σ λ_F n_F + g(w) reduces to (Σλ_F)·d + (a function of w). So the whole family
stands or falls with d, and d is not invariant.

## 4. Smoke tests [exploratory]
Each line gives the class size in labelled colourings, then the values of I = S + g mod 4, then the values of S + g mod 8.

| instance | classes | I mod 4 | S + g mod 8 |
|---|---|---|---|
| icosahedron − v | 1 (480) | {3} | {3, 7} |
| T4 − v | 1 (1632) | {3} | {3, 7} |
| order 18 #1, hole 0 | 144, 1416 (6, 59 canonical) | {3}, {3} | {3,7}, {3,7} |
| order 18 #6, hole 4 | 144, 1920 (6, 80) | {3}, {3} | {3,7}, {3,7} |
| order 20 #64, hole 0 | 1344, 3312 | {3}, {3} | {3,7}, {3,7} |

The three multi-class instances come from the coordinator's `kempe-census/multiclass-smallest3.json`. Their
classes were recomputed here by whole-component swaps, and the sizes match.
- **Mod 4:** constant on each class, but **no separation** in any instance.
- **Mod 8:** not constant on any class.
- **Exact loop that kills mod 8:** the six-step T4 loop of `disc-degree-parity.md`. The word stays (1,3,2,1,1)
  and S goes from 1 to −3, so ΔS ≡ 4 (mod 8).

## 5. What was not tried, and why
- **Mod 12** (Fisk/Mohar–Salas): the mod-3 part needs an Eulerian triangulation. D has a degree-5 hole, and
  interior swaps already change d by amounts with no mod-3 constraint. The algebra does not justify it.
- **Node-weighted Σ w(n)s(n):** this falls outside the family above, but nothing in the algebra suggests weights.
  A swap reverses s along an arbitrary bichromatic cycle, so the weights would have to sum to 0 (mod m) on every
  realisable cycle. That is not a word-level condition.
- **A non-linear invariant in the Mohar–Salas sense:** left for a fresh idea. Path 5 has nothing further to run;
  I recommend closing it early.
