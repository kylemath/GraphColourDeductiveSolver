# Track K review: hand proof of Conjecture F

8 Oct 2026. Independent adversarial review of `TrackK/FProof.md` and `TrackK/README.md`. I did not write the proof. All code in `scripts/` is written from scratch: it imports nothing from TrackC, TrackI or TrackK, and only the definitions were read.

## Verdict

**The proof of F is CORRECT.** Every step either is a complete argument or rests on a standard fact that is cited correctly. I found no WRONG step.

There are four GAPs. All are presentational or stale-reference; none touches the logic:
- **K1.** State the orientation convention for `hand` inside the statement of F.
- **K2.** n must count exactly the vertices of the map (no isolated vertices).
- **K3.** The W cited in the Remarks is the old, false form.
- **K4.** Small topological details in Proposition 1.

Data: **0 failures** across about 1.02M states (998,390 hole states, 840,715 of them on the sphere; 22,550 no-hole colourings) and every finite table (counts below).

## Step verdicts

| step | verdict | notes |
|---|---|---|
| §0 conventions (map-sense triangulation, parallel edges, cw, Fisk sign) | CORRECT | Every face has 3 distinct vertices, so it has 3 distinct edges and no edge has the same face on both sides. F = 2n−4 and E = 3n−6 follow from V−E+F = 2 and 3F = 2E. |
| T1 (cw ⇔ positive) | CORRECT | Exhaustive: 24/24. |
| T2 (each new face is cw ⇔ `hand`) | CORRECT | Exhaustive: 72/72. Also checked on the actual new faces of T°: 0 failures. |
| T3 (σ equal across an xy-edge ⇔ z ≠ w) | CORRECT | Exhaustive: 48/48. This is exactly the statement that "(d,a,b,c) even" is a coherent orientation of ∂Δ³. |
| Lemma 0 (all d_t equal; cw − ccw = 4d; cw = F/2 + 2d) | CORRECT | The standard edge-cancellation proof of the degree. It works edge-by-edge on the map's edges, so parallel edges are fine. It holds on any closed oriented surface (checked on the torus too). |
| Lemma 0′ (d ≡ deg(A)) | CORRECT | Number of face corners at a = deg a in a map triangulation; each face has at most one A-vertex; F is even. This matches the paper's Theorem 3 ("deg(f) has the same parity as deg(A)"). |
| Prop 1, region/chain bijection | CORRECT | Every face centre lies on S_i, since each face has exactly two crossing edges. So S² − S_i is the union of the open dual cells D_v and the open dual arcs e* of non-crossing edges, and its components are the XY- and ZW-chains. |
| Fact (a): Jordan–Schoenflies/Euler on 2-factor regions | CORRECT (minor GAP K4) | k disjoint PL simple closed curves cut S² into k+1 regions, each S² minus b_R discs (Schoenflies plus innermost-curve induction). See K4 for the details to state. |
| Fact (b): χ(R_Q) = \|V(Q)\| − \|E(Q)\| = 2 − b_Q; Σ_{XY} b_Q = k_i | CORRECT | Checked per region, not just in aggregate: every curve borders exactly one XY-region and one ZW-region (`sides_ok`), and V − E = 2 − b for every chain (`G_i = 0`). |
| Prop 1(a), 1(b); Tutte's identity | CORRECT | (a) − (b) is exactly eq. (4) of arXiv:1912.07205. |
| Theorem F0 | CORRECT | N = 3 + Σk_i. Σ_{X≠A} e(A,X) = deg(A) because the colouring is proper. 2(n−1+d) ≡ 2(n+1+d) mod 4. |
| Literature citation | CORRECT | See "Literature check" below. |
| T° is a valid sphere map | CORRECT | T is simple, so the link is a 5-cycle on distinct vertices, the star of h is a closed disc, and deleting h leaves an open pentagonal face. The fan from x₁ gives three faces on distinct vertices, oriented coherently (darts checked: x₃→x₁ in F1 and x₁→x₃ in F2, and so on). Parallel edges arise when x₁x₃ or x₁x₄ is already an edge of T; that is allowed by §0, and the Euler and face-incidence checks (`Map.validate`) pass on every T°. A vertex of degree 2 can appear in T° (x₂ or x₀ of degree 3 in T); this is still a valid map and F0 still applies. |
| Colouring stays proper on T° | CORRECT | The diagonals are coloured μA and μB, with μ ∉ {A, B}. |
| Step 1: N(T−h) = N(T°) + (1−L1) + (1−L2) | CORRECT, exactly | Only the μA and μB pair graphs gain an edge. Adding an edge merges two components iff they were different. When a diagonal coincides with an existing edge, L = 1 automatically and the count is unchanged: 0 failures of "existing x₁x₃ ⇒ L1" and "existing x₁x₄ ⇒ L2" on all 256,674 states with a pre-existing diagonal. |
| Step 2: cw(T°) = cw + 3·hand | CORRECT | Old faces keep T's orientation; the new faces are oriented as the pentagon. Uses T2. |
| Step 3: mod-4 bookkeeping | CORRECT | 2N = 2N(T°) + 4 − 2L1 − 2L2. Since −2L ≡ 2L and 3·hand ≡ −hand (mod 4), F follows. The Remark "N + L1 + L2 ≡ n + d(T°) (mod 2)" is also correct (checked). |
| §5 torus: residue = 2G | CORRECT | Generally, r_i = k_i + 1 − g + G_i. Then 2N(T°) − cw(T°) − n′ = 8 − 8g + 4m + 2G ≡ 2G (mod 4) on every orientable genus g, and Steps 1–2 are local. TrackK's unchecked expectation (G_i = 1 ⇔ every curve of S_i is contractible) is **now checked**: I test "every curve separates", which on the torus is equivalent to "bounds a disc". 0 failures on 482k partition instances; G_i ∈ {0, 1} always. |
| Consequences (Theorem 6 and Remark 7 via W) | GAP K3 (stale text) | F itself does not use W. |

## Gaps and fixes

**K1 (statement; raised independently by the Track C Lean work).** `hand` depends on the link being labelled along the face orientation, so that the faces at h are (h, x_t, x_{t+1}) in the orientation used for cw.
- Reversing only the labelling swaps A and B, so `hand` becomes 1 − `hand` (table E1, 24/24).
- The residue then changes by an odd amount, so F fails at every state. Data: "mismatched convention gives odd residue" holds on all 998,390 hole states.
- FProof.md §3 "Setting" does fix this explicitly ("in the orientation used for cw; this is `oriented_link`"). The proof is therefore fine.
- *Fix:* move the convention into the statement of F itself (as `TrackC/README.md` §7.2 `handS` does). Also note that F is invariant under reversing *both* the global orientation and the link: checked on 998,390 states, and algebraically cw ↦ (2n−9) − cw and hand ↦ 1 − hand cancel because cw − hand ≡ n+1 (mod 2).

**K2 (statement).** n must be the number of vertices of the map, so there can be no isolated vertices. An isolated vertex adds 1 to n and 3 to N (it is a singleton chain in the three pairs containing its colour), so F's residue moves by 6 − 1 ≢ 0.
- FProof §0 defines n as the number of vertices of a cellularly embedded triangulation, which excludes isolated vertices, so the proof is fine.
- *Fix:* say it explicitly, matching Lean's `ConjectureF` hypothesis.

**K3 (stale reference).** FProof.md Remarks (line 97) and TrackK/README.md "Consequences" cite Lemma W as "Δcw ≡ 2 m_h(K) mod 4" for all swaps, "a sketch, unreviewed", and say "Route Q now needs W reviewed, nothing else".
- That general form is **false**: Δcw can be odd (`TrackC/README.md` §7.1).
- The corrected W carries a link boundary term β. It is now formal (`ChainMod4.lean`), and β = 0 for π at DL states and for link-free swaps, which are the only cases used for Theorem 6 and Remark 7.
- *Fix:* replace the citation with the corrected W (β = 0 cases), and change "needs W reviewed" to "W is formal (§7); F ⇒ Theorem 6 and F ⇒ Remark 7 are formal; what remains is F itself in Lean".
- The proof of F does not use W anywhere, so this does not affect F.

**K4 (minor rigour in Proposition 1).** Spell out three things:
1. The components of S_i are vertex-disjoint cycles of the dual multigraph. There are no dual loops by §0, and dual digons are allowed. So they are pairwise disjoint PL simple closed curves, and Schoenflies applies.
2. Each curve is two-sided and borders exactly two distinct regions, one XY and one ZW. Locally this holds at every crossing edge, and it is constant along the curve because a collar is connected.
3. χ is a homotopy invariant, so χ(R_Q) computed from the graph Q (V − E) equals χ(S² − b discs) = 2 − b.

(1)–(2) are verified in data (`two_reg`, `sides_ok`, 0 failures).

Scope note (not a gap): Remark §3 says "any proper triangulation of the pentagon would do". True for F0, but only the fan from x₁ makes the new edges the lock edges.

## Literature check (arXiv:1912.07205, Mohar & Singer, "The Last Temptation of William T. Tutte")

- **Theorem 1 (Tutte).** For a plane triangulation with n vertices and colour class A, the paper gives "J_A(f) = 2|A| − deg(A) + n − 3".
  - Here J_A = p(A,B)+p(A,C)+p(A,D)−p(B,C)−p(B,D)−p(C,D).
  - deg(A) is the sum of the degrees of the A-vertices.
  - The proof derives p(A,B) − p(C,D) = |A|+|B| − e(A,B) − 1, using faces of T[A∪B] ↔ CD-chains.
- **§3 (Fisk).** deg(f) = t⁺ − t⁻, independent of the triangle. Theorem 3 states that the homology degree "has the same parity as deg(A)".
- **TrackK's citation is accurate**, both the formula and Thm 1/Thm 3. One caution: Theorem 3's surface version *defines* J_A by the formula with +g and only asserts a mod-2 relation. It is not a chain-count theorem off the sphere, consistent with F failing on the torus.

## Data (independent code; `scripts/`)

| run | log | states | failures |
|---|---|---|---|
| T1/T2/T3 + E1 (reversal flips hand) + E2 (π relabel keeps hand) | `kr_tables.log` | 24 / 72 / 48 / 24 / 24 | 0 |
| sphere min deg 3, n = 8–40, 600 graphs, Kempe walks | `run_min3.log` | 265,747 hole states (148,993 with a parallel diagonal) + 6,000 no-hole | 0 |
| sphere min deg 5, n = 12, 14–40, 600 graphs | `run_min5.log` | 274,009 hole + 6,000 no-hole | 0 |
| Census29 `frame-22..32.txt`, 543 graphs | `run_census.log` | 241,199 hole + 5,430 no-hole | 0 |
| **exhaustive**: every colouring of T−h, 300 random spheres n = 7–11 | `run_exhaustive.log` | 59,760 unfilled states (37,680 parallel; 10,128 both diagonals parallel) | 0 |
| bipyramids incl. 3-colourings (no hole) | `run_bipyr.log` | 2,000 (202 three-coloured) | 0 |
| torus, n = 20–40, 500 graphs | `run_torus.log` | 157,675 hole + 3,120 no-hole | 0 mispredictions of residue = 2G; G = 0/1/2/3 on 16,620 / 56,936 / 59,456 / 24,663 |

**What each state checks.**
- On T: F (S7); orientation-reversal invariance; mismatched convention ⇒ odd residue; existing diagonal ⇒ lock.
- On T° (built with explicit edge records, diagonals always new edges, Euler/incidence validated):
  - S1, S2, and T2 per new face;
  - Lemma 0 (four d_t equal, cw − ccw = 4d, cw = F/2 + 2d) and Lemma 0′ for all four colours;
  - per partition: 2-regularity, sides, χ = 2 − b per region, (a) exact, (a) mod 2, (b), Σ b_XY = k;
  - F0 and the parity form;
  - on the torus: the genus-corrected (a) and (b), G_i ∈ {0,1}, and G_i = 1 ⇔ all curves separating.

**Sabotage.** Dropping the 2(L1+L2) term (`KR_SABOTAGE=1`) gives 139/275 S7 failures, so the harness detects errors.

Not reproduced: TrackK's 272 min-degree-5 parallel-diagonal states. My min-5 generator and the Census frame class produced none, because they need a separating triangle through x₁, x₃. Parallel diagonals are heavily covered by the min3, exhaustive and torus runs instead.

## Files

- `scripts/kr_tables.py`: exhaustive T1–T3, E1, E2.
- `scripts/kr_core.py`: oriented triangulations, flips, min-5 generator, census parser, the filled map T° with explicit (multi)edges, and the per-map analysis.
- `scripts/kr_check.py`: per-state step checks. Usage: `nice -n 10 python3 -I kr_check.py FAMILY SEED NGRAPHS STEPS`.
- `scripts/kr_exhaustive.py`: all colourings of small spheres.
- Logs: `scripts/*.log`. Total compute was about 13 CPU-minutes, on at most 2 workers at nice 10.
