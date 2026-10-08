# Track H review (Track C discipline): independent check

Reviewer: an independent agent, 7 Oct 2026, night. I did not write any of Track H. No Track H or Track F code was imported or copied. The definitions come from `QuarterFloor.lean`, `NoFrozen.lean`, `QuarterLockParity.lean`, `VacancyShortFill.lean` (`Target`, `pairGraph`, `KempeStep`, `PurePath`/`PureFill`), `RStar.lean` (`PureClean`) and `TrackF/LockParity.md`.

Compute: at most 2 worker processes at a time, all under `nice -n 10`, about 45 minutes of wall time. Nothing was committed, and nothing outside this directory was modified.

## Verdicts

| # | item | verdict | counts |
|---|---|---|---|
| 1 | `lp_general_min.txt`: one Kempe class is exactly one all-DL π-cycle of length 10 with no filled state, and D1, D2, P1–P3 and lock parity hold at every state | **CONFIRMED** (with documentation errors, see 1.3) | 264 absolute colourings of G − h in 2 Kempe classes (240 + 24). The 240-class is 10 renaming-orbits × 24, has 0 filled states and is one π-cycle of length 10 (π defined at 10/10 states and never leaves the class). DL 10/10; D1, D2, P1, P2, P3, LP1, LP2 10/10 each (both the boundary form and the odd-degree-count form); rigid 10/10; Kempe degree 2 at all 10; σ is a renaming at 10/10 |
| 2a | Lemma H0, "every state of an all-DL π-cycle satisfies D1/D2" | **CONFIRMED** (the "in particular" clause; the proof is correct) | 0 failures in 46,000 states on 2,913 all-DL π-cycles (perturbed general graphs). Also 0 failures of the proof's core step (a π-image has ¬inB) |
| 2a′ | Lemma H0, first sentence as literally stated ("s unfilled, π(s) defined, s = π(t) ⇒ D1 ∧ D2", any graph) | **FAILED** as stated; true on triangulated surfaces | 6-vertex counterexample (wheel W₅). Random general graphs: 902,545 / 913,643 failures; perturbed cex graphs: 13,409 / 163,619; every failure is at a non-DL s. Triangulated surfaces: 0 / 1,577,426 (sphere 990,002, RP² 416,508, torus 108,064, Klein 62,852) |
| 2b | Lemma H3 (edge balance on closed triangulated surfaces) | **CONFIRMED** (hand proof checked line by line; data) | 0 failures: 24,076,962 + 13,464,516 + 4,495,173 + 2,843,424 partition checks (sphere, RP², torus, Klein) in the general form 2E_k = 2n − 2χ − 5 + ℓ_k. The unfilled form (E₁ = E₂ + 1 = E₃ + 1, c − β = χ, χ+1, χ+1) also has 0 failures on 24,048,813 checks |
| 3 | "Rigid isolation" evidence on the sphere | **CONFIRMED** (as data; 0 counterexamples on a fresh sample) | 0 rigid → rigid among **59,441** rigid DL states: 51,914 at 28,855 holes of 3,166 plantri / Census29 sphere triangulations, plus 7,527 at 34,655 holes of 10,000 random flip spheres |
| 3′ | Track H's claim "Klein 0, torus 0" (rigid isolation holding off the sphere apart from RP²) | **FAILED** (a sampling artefact; it strengthens the "genuinely spherical" reading) | Fresh data: torus **23** rigid → rigid of 2,467 rigid states, Klein **1** of 1,401, RP² 29 of 5,205. All 53 were re-confirmed by a second, networkx-based computation |

## 1. The main negative result (`rv_cex.py`, `out_cex.txt`)

### 1.1 What was checked

For the graph in `TrackH/lp_general_min.txt` (hole h = 0, link = adj[0] in the file's order), the checker:
- verifies the graph is simple and symmetric;
- verifies `Pent`: the link is exactly N(h) and consecutive link vertices are adjacent;
- enumerates every proper 4-colouring of G − h (absolute colours);
- joins colourings by every Lean `KempeStep`: swapping a whole component of `pairGraph(a,b)` on G − h, over every pair a ≠ b and every component, including components that avoid the link;
- classifies each class by `Target` (some colour missing on N(h)) and computes everything else directly from the Lean definitions: `RepeatAt`, `Lock1`, `Lock2`, inA/inB, D1/D2, P1–P3 (|δ(X)| in G, with edges to h counted), LP in both the boundary and odd-degree-count forms, π, σ, and pair component counts.

### 1.2 Definitions: no discrepancy found

- **Induced link.** The link is an induced 5-cycle (no chord x_i x_{i+2}). `Pent` does not require this, but here it holds.
- **"Filled" is Lean `Target`.** That means ∃ colour missing on N(h), i.e. at most 3 link colours, and the class is a `KempeEquiv` class. "No filled state in the class" is therefore exactly "no `PurePath` from these colourings reaches `Target`", which is the failure of `PureFill` that `PureClean` quantifies over.
  - Lean colourings also carry a value at h, which `KempeStep` never changes, so the classes correspond one to one.
- **π.** π is the swap of K_{αA}(x_{j+2}), defined when x_j ∉ K_{αA}(x_{j+2}), as in LockParity §5.2.
- **The class is closed under renaming** (240 = 10 × 24), so "class up to renaming" and "Kempe class" agree here.

### 1.3 Discrepancies and caveats (documentation, not substance)

1. **Wrong link degrees in the README.** TrackH/README §4 gives "link degrees 9,6,8,4,5". The file's actual link degrees are **5, 8, 11, 8, 8** in G (4, 7, 10, 7, 7 in G − h).
2. **"min" is not minimised.** `lp_general_min.txt` has the same edge set as `lp_general_cex.txt` (28 vertices, 109 edges both).
3. **G is not 4-colourable.** Every one of the 264 colourings of G − h is unfilled, so χ(G) = 5.
   - The other Kempe class (24 absolute, 1 state up to renaming) is an isolated DL state with inA = inB = 1. It violates D1, D2, P1 and P2, with counts (1,1,1,1,1,1).
   - This does not weaken the logical claim: the 10-state class satisfies every hole-local hypothesis and has no filled state. But the paper should say that the counterexample graph has no filled colouring at all. The "local facts ⇏ LPC" conclusion is reached through a 5-chromatic graph.
4. **Far from a triangulation.** 5 edges lie in no triangle, and the H3 balance fails at every state. My recomputation reproduces Track H's "class imbalance 78" (Σ|E₁ − E₂ − 1| + |E₂ − E₃| over the 10 states; `out_cex_balance.txt`), and |E(G − h)| = 104 ≡ 2 (mod 3).
5. **Companion file.** As a side check, `lpc_general_min.txt` (21 vertices) is also one rigid all-DL 10-cycle with 0 filled states and D everywhere, while P1 holds at only 4/10 states. This matches the README's "P fails".

## 2. Lemmas H0 and H3

### 2.1 H0: hand proof review

- **The proof is correct.** I checked the roles of π(t): with frame j₀ + 3 they are (α, B, μ, A), and the swapped set is still an {α, A} = {α_s, B_s} component that contains x_j but not x_{j+2}. So a π-image has ¬inB, and π(s) being defined gives ¬inA.
- **The first sentence over-claims.** ¬inA and ¬inB give D1/D2 only when L1 = L2 = 1, and the proof says "at a DL state" without putting that in the hypothesis.
  - Counterexample (any graph): the wheel W₅. Take h plus the bare link 5-cycle, and colour the link (α, μ, A, α, B). This s is a π-image of an unfilled t, π(s) is defined, and L1 = L2 = 0 with inA = inB = 0, so D1 and D2 both fail.
  - Fix: add "s DL" to the hypothesis, or restrict to closed triangulated surfaces. On surfaces the data show no failure, and a local argument suggests why: ¬Lock2 ⇒ inA by walking the boundary of the {μ,B}-component of x_{j+1}, which passes h once. That argument is mine and unreviewed.
- **The "in particular" clause** (all-DL π-cycles) is what Track H uses, and it is correct.

### 2.2 H0: data

**Fresh triangulations** (`rv_surf.py`, `rv_h0h3.py`). Random simplicial triangulations grown by stellar subdivision and random flips from the octahedron, the 7-vertex torus, the 6-vertex RP² and a 16-vertex Klein bottle; every complex is validated, and χ and orientability are recomputed. Every degree-5 hole was used, with n = 10–30.

| surface | graphs | holes | unfilled states | π-images with π defined | H0 literal failures | D-violating states (sanity) |
|---|---|---|---|---|---|---|
| sphere | 10,000 | 34,655 | 4,314,923 | 990,002 | 0 | 0 |
| RP² | 20,000 | 66,645 | 2,404,859 | 416,508 | 0 | 576,123 |
| torus | 20,000 | 64,278 | 798,327 | 108,064 | 0 | 319,358 |
| Klein | 10,000 | 34,733 | 498,162 | 62,852 | 0 | 208,094 |

- Theorem P (P1–P3) had 0 failures at every unfilled state on all four surfaces.
- Random surfaces contained **no** all-DL π-cycles, so the cycle clause of H0 could not be exercised there.

**General graphs** (`rv_h0gen.py`). These exercise the cycle clause.

| sample | graphs with colourings | all-DL π-cycles | cycle states | H0 cycle failures | literal-sentence failures |
|---|---|---|---|---|---|
| 1–6 random edge toggles of the three Track H cex graphs | 17,962 | 2,913 | 46,000 | **0** | 13,409 / 163,619 (all at non-DL s) |
| random graphs, hole + induced 5-cycle, n = 9–16 | 4,223 | 0 | – | – | 902,545 / 913,643 (all at non-DL s) |

### 2.3 H3: hand proof review

The proof is correct; I re-derived each step.
- Each face of T − h is properly 3-coloured, and its three edges fall one into each of the three partitions.
- The faces of T − h number f − 5. Link edges lie in one face of T − h and all other edges in two, because by (F3) the only faces at h are the five {h, x_t, x_{t+1}}.
- An unfilled link (α, μ, α, A, B) has ℓ = (3, 1, 1).
- With f = 2(n − χ), this gives E_k = n − χ − (5 − ℓ_k)/2; the README's "n − χ − (3 − ℓ_k)/2 − 1" is the same expression.
- c_k − β_k = |V(T − h)| − E_k follows because each vertex lies in exactly one of the two pair graphs.

**Two notes:**
- The second half (c − β) is just V − E once E_k is known. The real content is the edge count.
- The general form 2E_k = 2n − 2χ − 5 + ℓ_k also holds at filled states, and I checked it there too.

**Data:** 0 failures on all four surfaces (see the verdict table).

### 2.4 Side checks

- **H4** (lower bound (1,1,2,1,2,1) on component counts at DL states with D): 0 failures, on 1,577,426 surface states and 3,718,935 sphere DL states.
- **H5** (a rigid state's Kempe moves are renamings, π or π⁻¹): 0 failures at 16,600 rigid states on random surfaces.

## 3. Rigid isolation on the sphere (`rv_ri.py`, `out/ri_summary.txt`)

**Rigidity**, computed independently: a state is rigid when it is DL, D1 and D2 hold, and the component counts (#αμ, #AB, #αA, #μB, #αB, #μA) over active vertices of G − h equal (1,1,2,1,2,1). For each rigid c I computed π(c) and tested it for rigidity in its own frame. Inputs were checked to be sphere triangulations (E = 3n − 6, rotation faces all triangles, V − E + F = 2), and the 13 Census29 graphs Track H used were excluded.

| source (fresh) | graphs | holes | colourings | DL | rigid | π(c) rigid | π(c) single-lock | π(c) DL non-rigid |
|---|---|---|---|---|---|---|---|---|
| Census29 frame-22…29 (all) | 443 | 6,735 | 13.8M | 1.31M | 21,092 | **0** | 16,577 | 4,515 |
| Census29 frame-30 (every 10th), 31 (every 40th), 32 (every 160th) | 326 | 5,223 | 20.4M | 2.04M | 19,006 | **0** | 14,357 | 4,649 |
| plantri −m5 n = 20, 22 (all) | 724 | 10,479 | 3.08M | 0.32M | 10,571 | **0** | 7,749 | 2,822 |
| plantri −m4 n = 15 (1/20), 17 (1/400) | 1,250 | 5,400 | 0.68M | 50,609 | 803 | **0** | 602 | 201 |
| plantri −m3 n = 12 (1/30), 14 (1/2000) | 423 | 1,018 | 18,775 | 2,368 | 442 | **0** | 419 | 23 |
| random flip spheres n = 10–30 (`rv_h0h3.py`) | 10,000 | 34,655 | 8.0M | 0.99M | 7,527 | **0** | – | – |
| **total** | 13,166 | 63,510 | | | **59,441** | **0** | | |

Notes:
- π(c) is never filled, never lockless and never undefined from a rigid state, and D/P had 0 failures throughout (the sphere sanity checks).
- The excess of non-rigid DL images over the rigid vector was 1 in 7,642 cases, 3 in 4,234, 5 in 333 and 7 in 1. So the near misses have excess 1, as Track H reports.
- **Possible overlap:** frame-24's 4 graphs may also appear in Track H's "plantri24 every 60th" sample.
- **Off the sphere,** rigid → rigid steps occur on RP² (29), the torus (23) and the Klein bottle (1). A networkx recomputation confirmed 53/53. Track H's "torus 0, Klein 0" is a small-sample artefact (194 and 613 rigid states). The conclusion "RI is genuinely spherical" is strengthened, not weakened.
- **Scope:** this is data on small triangulations (n ≤ 32), as Track H's is. Rigid states become rarer as n grows (rigid / DL ≈ 0.8% at frame-32), so the sample does not tell us how RI behaves for large n.

## Files

| file | content |
|---|---|
| `rv_core.py` | colouring enumeration, Kempe moves, locks, D, P, LP, π, component counts, rigidity |
| `rv_cex.py`, `out_cex.txt` | item 1 checker and output (`python3 rv_cex.py ../TrackH/lp_general_min.txt ../TrackH/lpc_general_min.txt`) |
| `rv_cex_balance.py`, `out_cex_balance.txt` | H3 balance at the 10 cex states |
| `rv_surf.py`, `rv_h0h3.py`, `run_item2.sh` | fresh surface generator; H0/H3/H4/H5/rigid-isolation tests. Outputs in `out/h0h3_*.log`; graphs in `out/h0h3_*.json.gz` |
| `rv_h0gen.py` | H0 on general graphs and the W₅ counterexample to the literal sentence (`out/h0gen_*.log`) |
| `rv_rr_recheck.py` | networkx recheck of off-sphere rigid → rigid steps (`out/rr_recheck_*.log`; gunzip the `.json.gz` first) |
| `rv_ri.py`, `run_item3.sh` | rigid isolation on sphere triangulations (`out/ri_*.json`, `out/ri_summary.txt`; plantri inputs in `out/pl/`) |
