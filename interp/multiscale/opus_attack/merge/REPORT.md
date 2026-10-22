# Attack on the weak-level merge step (a_W): report

22 Oct 2026. Everything is in `/mnt/project-files/multiscale/opus_attack/merge/`. Labels: [P] proved here, [M] measured (exact on the instance), [C] conjecture or interpretation.

## Verdict: FALSE

(a_W) is false as stated. No constants R, w exist. There is an explicit family of weakly 1-level pairs (A, B) where the minimum repair radius grows linearly with a free length parameter ℓ:

- R(ℓ) ≥ ℓ/2 with the collar width held at w = 3 (also at w = 4).
- Exact SAT values at w = 3: R = 2, 3, 4 at ℓ = 4, 6, 8.
- At ℓ = 10: R ≥ 5. Both the SAT run (R = 0..4 UNSAT for all 24 renamings) and the solver-free certificate give this.

The failure comes from **properness alone**. It happens before re-levelling is even required, so it rules out every merge rule of the form "recolour only N_R(conflicts) ∪ N_w(∂U)".

## 1. The statement tested

This is (a_W) of `hierarchy/weak/RESULTS.md` / doc rev 6:

> There are constants R, w such that, for every planar triangulation G of min degree 5: if A, B are disjoint discs with U = A∪B a disc, and c_A, c_B are weakly 1-level (every pocket, i.e. every piece after cutting along internal chords, has τ ≤ 1 in its own boundary gauge), then some renaming π and some weakly 1-level c_U agree with c_A ∪ π·c_B outside N_R(conflicts) ∪ N_w(∂U).

Conventions are the authors':
- conflicts = endpoints of monochromatic A–B edges;
- N_R and N_w are distances inside U, as `multi_bfs(..., U)` in `wk.py`;
- N_0(∂U) = ∂U;
- τ is computed with `wk.Disc(...).pockets` and `wk.tau_walk`.

I tested the **necessary** condition: is there a renaming π and a *proper* colouring of U that equals the glue outside Z = N_R(K_π) ∪ N_w(∂U)? Any failure here is a failure of (a_W).

Embedding: U lives in the flat triangular lattice, with every interior degree equal to 6. Such a disc sits inside one face of a large subdivided icosahedron (min degree 5), and (a_W) only refers to U. Caveat: I did not build the closed sphere; see §6.

## 2. Mechanism: the twisted seam [P]

- U is flat, so any proper colouring of U has a single-valued Kondev–Henley height.
- Write a renaming as π = (Q, t), with Q ∈ D3 permuting e_g, e_h, e_{g+h}. All 24 renamings arise this way; `twist.py` asserts it.
- A seam stretch S is **π-conflict-free with offset T** if the glue is proper along S and h_A = Q·h_B + T there.
- Take two such stretches with T₁ ≠ T₂ (necessarily T₂ − T₁ ∈ 2Λ∖0). Suppose both survive outside Z and are joined through A∖Z and through B∖Z. Then the glued colouring has height monodromy T₂ − T₁ ≠ 0 around a loop in U∖Z. That is impossible in a flat disc, so **no recolouring of Z alone gives a proper colouring of U**.
- To escape, Z must swallow a stretch (R ≳ ℓ/2), cut A through (R ≳ blob half-width), or cut B through (R + w ≳ distance to ∂U).
- The construction plants, for **each of the 24 renamings**, its own pair of length-ℓ stretches with different offsets. It uses SAT on height functions (`twist.build`), with every pocket of A and of B constrained to a radius-1 ball whose centre the solver chooses.

The obstruction is not a large mismatch:
- the twisted pairs need only |h_A − Q h_B| ≲ 3;
- the strict τ of the whole of A is only 1.5–2.0;
- the Mismatch Lemma W / 4K bound holds throughout.

The bounded mismatch is real; it just does not imply bounded R.

Role of chords [M]:
- With one chordless A against one single-pocket B, my constructor fitted at most 13 of the 24 twists in one run (greedy). The failures depended on the stretch positions and the mix of T-classes; I suspect a Z3-type phase constraint along the seam, but it is not pinned down.
- At ℓ = 8, all 24 twists were UNSAT with a single-pocket B (bottom margin 10). They became SAT once B was pinched below the necklace tip into a left pocket and a right pocket with different centres.
- So the pockets' freedom to have different ball centres is exactly what the weak invariant gives away.
- It is open whether chordless A, B can also be twisted against all 24 renamings. That would also break the original LML (a).

## 3. Families and results

### E1: the requested angle, drift accumulated over many pockets (`exp1.py`)

- A = necklace of k+1 blobs joined by single chords; the seam crosses 2k+1 pocket stretches.
- Pocket n has its boundary in Ball(n·v, 1) with v = (2,4), i.e. drift √3 per pocket, the most Lemma W allows.
- B is level.

| k (chords) | blob M, h | strict τ(A) | R at w = −1 / 1 / 3 |
|---|---|---|---|
| 1 | 3, 3 | 1.5 | 0 / 0 / 0 |
| 2 | 3, 3 | 2.0 | 1 / 1 / 1 |
| 4 | 3, 3 | 4.36 | 1 / 1 / 1 |
| 8 | 3, 3 | 7.81 | 1 / 1 / 1 |
| 12 | 3, 3 | 11.27 | 1 / 1 / 1 |
| 8 | 5, 5 | 7.81 | 2 / 2 / 2 |

R does **not** grow with the number of pockets crossed, even though strict τ(A) reaches 11. [P] Reason: the drift is seen only modulo 2Λ. Once Z covers the necks, each blob's interior is its own component of U∖Z and absorbs its own 2Λ translation. So the growth in the [P] bound (mismatch ≤ 2K·#pockets) is harmless. This angle is a dead end.

### E5: twisted seams, R(ℓ)

Built with `exp5.py` / `build_cx.py`. A and B are checked weakly 1-level both with the authors' `wk.tau_walk` and with my own τ; every pocket has τ = 1.000.

| file | ℓ | nU (nA / nB) | chords A / B | pockets A / B | strict τ(A) | exact R, w = 3 [M] | certificate R ≥ at w = −1 / 3 / 4 / 5 / 6 [P] |
|---|---|---|---|---|---|---|---|
| `cx_ell4.pkl` | 4 | 4,500 (1,154 / 3,346) | 11 / 4 | 12 / 5 | 2.0 | **2** | – / 1 / – / – / – |
| `cx_ell6b.pkl` | 6 | 11,229 (3,210 / 8,019) | 11 / 4 | 12 / 5 | 2.0 | **3** | 3 / 3 / 2 / – / – |
| `cx_ell8.pkl` | 8 | 16,997 (5,132 / 11,865) | 12 / 8 | 13 / 9 | 1.5 | **4** | 4 / 4 / 4 / 3 / 2 |
| `cx_ell10.pkl` | 10 | 22,885 (7,106 / 15,779) | 12 / 8 | 13 / 9 | 2.0 | **≥ 5** (R ≤ 4 UNSAT for all 24; the R = 5 call crashed the solver) | 5 / 5 / 5 / 4 / 3 |

Reading the table:
- The certificate is computed for each renaming and minimised over all 24.
- It decreases at large w only because each instance has a finite side margin (9, 10, 11). Once R + w + 2 exceeds the margin, the collar plus the repair zone can cut B through.
- For any target (R, w), take ℓ > 2R + 1, blob half-width > R + 1 and margin > R + w + 3.

Cross-check of my exact checker against the authors' repair code (`crosscheck.py` runs `wk.proper_repair_at` in `do_merge`'s all-24-renamings order, no collar; their pysat calls are routed to my solver because python-sat is not installed in this container):

| instance | theirs | mine | renaming |
|---|---|---|---|
| ell4 | 2 | 2 | (3,0,1,2) |
| ell6b | 3 | 3 | (3,0,1,2) |
| ell8 | 4 | 4 | (3,2,0,1) |

## 4. Reproducing the counterexample

Solver-free verification, about 1 minute per file:

```
cd /mnt/project-files/multiscale/opus_attack/merge
python3 check_cx.py cx_ell8.pkl 3 3     # VERDICT: 24/24 renamings obstructed at R=3, w=3
python3 check_cx.py cx_ell10.pkl 4 3    # 24/24 at R=4, w=3
python3 check_cx.py cx_ell6b.pkl 2 3    # 24/24 at R=2, w=3
```

`check_cx.py` verifies:
- that A, B and U are discs and U is flat;
- that c_A and c_B are proper;
- weak 1-levelness **with the authors' `wk.Disc` / `wk.tau_walk`**;
- for each renaming, it integrates the glued height on U∖Z and prints an edge that closes a loop with non-zero monodromy. The monodromy is always a 2Λ vector of length 2√3, such as (4,8) or (8,4).

The saved outputs are `check_ell8_R3_w3.txt`, `check_ell10_R4_w3.txt` and `check_ell6b_R2_w3.txt`. As a consistency check, `check_cx.py cx_ell8.pkl 4 3` obstructs only 3/24 renamings, matching exact R = 4.

Exact runs: `python3 evalcx.py FILE 3 exact`. Logs: `exact_ell{4,6b,8,10}.log`. JSON summaries: `eval_ell8.json`, `eval_ell10.json`.

Data format: each pickle holds the lattice points `pts` ((i,j) coordinates; neighbours ±(1,0), ±(0,1), ±(−1,1)), `A` and `B` as point indices, the heights `h` (colour = `heights.colouring`, i.e. h mod 2Λ), the stretch metadata and the pocket centres.

## 5. Code

| file | role |
|---|---|
| `msat.c` | my CDCL solver; no SAT binding is importable here. Tested against brute force on 2,500 random CNFs, plus a variant cross-check on 60 n = 200 threshold instances. Every model is verified in Python, and the UNSAT results are backed by the solver-free certificate. |
| `lat.py` | lattice, CNF I/O |
| `heights.py` | height-function colourings |
| `mergecheck.py` | my exact merge checker: joint free set N_R(K) ∪ N_w(∂U), with optional pocket-levelness walk encoding |
| `twist.py` | twist construction, monodromy certificate |
| `neck.py` | necklace geometry |
| `exp1.py` | drift family |
| `exp2.py`, `exp4.py`, `pairs.py` (`pairs.jsonl`) | chordless twist experiments |
| `exp5.py`, `build_cx.py`, `order.py` | counterexample construction |
| `evalcx.py`, `check_cx.py`, `crosscheck.py` | evaluation and checking |
| `pysat_stub.py` | lets the authors' modules import, routing their SAT calls to `msat` |

No file outside this folder was modified, and bytecode writing is disabled.

To rebuild ell8:

```
python3 build_cx.py "__import__('order').SEL" 12 20 6 10 2 8 8 cx_ell8.pkl
```

This takes about 7 minutes. The positional arguments are k, h, M, ms, mb, ℓ, avoid.

## 6. Calibration and caveats

- **Status of the evidence.** The obstruction is [P] and checked on each instance without a solver. The exact values are SAT-exact, with 0 UNKNOWN answers, and they match the authors' repair routine on 3 instances.
- **(a_W) as stated, for all weakly 1-level inputs: FALSE**, confidence about 95%.
- Residual risks:
  1. **The ambient sphere was not built.** I did not build the closed min-degree-5 G; all checks use U. If N_R were measured in G instead of U, outside shortcuts could shrink distances. U is a convex lattice region, so this is very unlikely to matter.
  2. **(a_W) quantifies over all weakly level inputs.** The route could be rescued by a stronger invariant that the recursion's own merges preserve and that forbids coherent twisted stretches, e.g. an offset or Z3-phase coherence condition along ∂. Nothing like that is in the current write-up.
- Why the authors never saw it: their ~3,100 merges use SAT- or random-produced level colourings, which do not contain long coherent twisted stretch pairs for every renaming. The pocket count was the wrong suspect.
- Not done:
  - vortices and high-degree hubs near seam ends; not needed, since the counterexample is fully flat;
  - lopsided splits;
  - a chordless counterexample (13/24 renamings is the best found; open);
  - the closing step (b_W), where the same twist idea should be tried next.
