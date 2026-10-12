# Track G: is there a "stream function" for π? [exploratory]

Studio, 7 Oct 2026, evening. Nothing here is committed, and nothing outside `TrackG/` was changed. Every claim is **data** unless marked **hand**. Compute: at most 2 single-threaded workers under `nice -n 10`, about 95 min of wall time (18:31–20:05). The local/all pooled LPs on the 22–29 pool were stopped at that point.

## Question (Kyle's fluid-mechanics analogy)

- Theorem W (4F − N = −5Σw per class) reads like a discrete circulation identity.
- A frozen orbit is a closed streamline with no source.
- Lock-parity violations come from crossing non-separating cycles, an H¹ effect.

So: is there a real-valued ψ on the states of a Kempe class, built from local or homological data, that strictly increases along every DL→DL π-step? Such a ψ would make all-DL π-cycles impossible. And on surfaces other than the sphere, does ψ fail exactly through H¹?

## Verdict

**No usable handle, at either level tested.**

1. **State-level ψ: infeasible as a fixed formula.**
   - No linear ψ built from the feature basis (ring word, lock bits, odd-vertex counts of the lock-parity components, component sizes, chain counts, chain lengths, Kempe distances) is monotone on DL π-runs across graphs. The best pooled formula satisfies 36% of the steps.
   - Per hole the LP is often feasible, but a sign-randomised null is feasible just as often. That feasibility is dimension counting, not structure.
2. **The obstruction is structural, not a missing feature.**
   - On the sphere, all-DL π-cycles exist (17 in the census, plus 2 at C30#0 and 2 at C40#0). A state function cannot increase around a cycle, so no ψ is monotone on all DL steps.
   - The "circulation" of an all-DL cycle is w = L/5 > 0, since λ = +1 at every R3 step. Theorem W then says only that such a class needs compensating filled states. The class-level potential statement "Σw ≤ 0" is exactly the quarter floor, i.e. LPC-¼. That is the target itself restated, not a new handle (hand).
3. **The class-level certificate exists, is short and has a nearly uniform local form, but it is not topological.**
   - In every cycle class (sphere and off-sphere), every all-DL cycle state reaches a single-lock or no-lock state within at most 2 Kempe moves on the sphere (at most 4 off the sphere). A filled state follows one move later by Lemma A.
   - The **hole's own α–μ swap σ = swap K_{αμ}(x_{j+2})** leaves DL at ≥ 1 state of every one of the 1,429 all-DL cycles. The rate is at least 25% of the cycle's states (data conjecture "σ-escape", below).
4. **Off the sphere, the certificate never breaks.**
   - Every off-sphere cycle class contains filled states, as TrackF already found, so there is no failure to localise.
   - H¹ shows up as follows:
     - every lock-parity violator's crossing pair is non-separating (20,124 of 20,124; this is §5.1 of LockParity.md confirmed by direct ℤ/2 computation);
     - non-separating lock cycles are enriched about 2× at the states with the slowest escapes.
   - It does not show up as a failure of the escape certificate.
   - Adding ℤ/2-homology bits to the ψ features does not make the LP feasible: any gain is matched by the null.

## 1. Setup (`tg_engine.py`)

- **Engine.** `kempe_py.Space` (Track A's bitmask engine; no planarity is used, so it runs on any triangulated surface).
- **π.** As in LockParity.md §5.2 and TrackF `lpc_detail.py`: swap K_{αA}(x_{j+2}), defined iff x_j ∉ K_{αA}(x_{j+2}). On the sphere, at DL states, this is R3 of `escape.pi_of`.
- **Checks.**
  - C30#0 reproduces TrackF's 100-state class [40 F, 30 DL, 30 S] with one 20-cycle at both 55555 holes.
  - The cycle holes, cycle lengths and [N, F] of cycle classes agree with Census29 (13 graphs, 17 cycles) and TrackF kclass3 (686 off-sphere holes).
- **Features** (computed in the frame of each state, so ψ = θ·φ is a genuine state function):

| feature set | content |
|---|---|
| `ring` | j one-hot, link degree word rotated to the frame |
| `lockpar` | number of odd-G-degree vertices in K_{αA}(x₂), K_{αB}(x₂), K_{αμ}(x₂), K_{μA}(x₁), K_{μB}(x₁), K_{AB}(x₃) (the lock-parity lemma's quantities) |
| `comp` | `lockpar` plus the sizes of the same six components |
| `global` | colour-class sizes by role; number of Kempe chains per role pair |
| `chains` | shortest lock-chain lengths, and α–A / α–B chain lengths x₂→x₀ (0 if the chain is absent) |
| `dist` | Kempe degree, Kempe distance to the nearest filled state and to the nearest non-DL unfilled state |
| `local` | ring + comp + chains |
| `all` | everything (40 features) |
| `hom` (off-sphere) | ℤ/2 classes of the closed chains h·x₁(μA)x₃·h, h·x₁(μB)x₄·h, h·x₂(αA)x₀·h, h·x₂(αB)x₀·h (shortest paths; separating iff a boundary mod 2, by face 2-colouring) |

**Data** (`tg_collect.py`, `run_all.sh`, `run_c30.sh`):
- sphere:
  - census orders 22–29, exhaustive (443 graphs, 6,719 holes);
  - a 25% sample of order 30 (295 graphs);
  - the 13 census graphs with all-DL cycles (orders 30–32);
  - C30#0 and C40#0;
- off-sphere: every cycle hole of TrackF `cyc_graphs` (604 holes: torus, Klein, RP²) and `cyc555_graphs` (82 holes).

## 2. State-level ψ: LP feasibility (`tg_lp.py`)

LP: find θ with θ·(φ(πs) − φ(s)) ≥ 1 on every DL→DL π-step not on an all-DL cycle. The LP minimises total slack, so it is infeasible iff the optimum is > 0. "Null" reverses each step with probability ½: the step graph stays acyclic, so an arbitrary ψ still exists, and only feature expressiveness is tested.

**Census 22–28** (65,590 steps, 2,194 holes, 147 graphs; `out/lp_census22-28.txt`):

| features | holes feasible | null | graphs feasible | null | pooled: share of steps satisfied | held out (cycle graphs 30–32, C30/C40): ≥ 1 / > 0 |
|---|---|---|---|---|---|---|
| ring | 644 / 2194 | 390 | 5 / 147 | 0 | 0.013 | 0.07 / 0.55 |
| lockpar | 470 | 351 | 3 | 0 | 0.084 | 0.12 / 0.57 |
| comp | 1246 | 983 | 7 | 1 | 0.19 | 0.22 / 0.61 |
| global | 945 | 640 | 4 | 0 | 0.21 | 0.22 / 0.57 |
| chains | 86 | 48 | 1 | 0 | 0.001 | 0.01 / 0.49 |
| dist | 26 | 21 | 0 | 0 | 0.02 | 0.03 / 0.03 |
| local | 1878 | 1843 | 12 | 2 | 0.30 | 0.32 / 0.66 |
| all | 2134 | 2100 | 16 | 2 | 0.36 | 0.35 / 0.67 |

- **Train 22–28, test 29** (223,022 steps; `out/lp_train22-28_test29.txt`): the share of test steps with Δψ > 0 is 0.50–0.69 for every set, which is barely above a coin flip.
- **Census 29 alone** (`out/lp_census29_perhole.txt`):
  - lockpar is feasible at 233 / 4525 holes (null 107) and 1 / 296 graphs;
  - comp at 1179 / 4525 holes (null 595) and 1 / 296 graphs.
  - Real beats null per hole by about 2×, so the components carry some directional signal locally. It never assembles into a per-graph ψ.
- **Train 22–29** (288,612 steps), **test on the order-30 sample plus all off-sphere steps** (353,580 non-cycle steps; `out/lp_train22-29_test30s4_off.txt`):

| features | pooled share satisfied | test Δψ ≥ 1 | test Δψ > 0 | all-DL cycle steps Δψ > 0 |
|---|---|---|---|---|
| lockpar | 0.06 | 0.07 | 0.59 | 0.49 |
| comp | 0.19 | 0.21 | 0.63 | 0.50 |
| global | 0.16 | 0.17 | 0.62 | 0.43 |

  (local / all were stopped at the compute limit; on 22–28 they reach only 0.30 / 0.36.)
- **Reading.**
  - Per-hole feasibility tracks the null closely once there are ≥ 12 features. Holes have about 30 steps in about 20 short runs, so a 40-dimensional θ fits almost anything.
  - Per graph the real data beat the null slightly (16 vs 2), but 89% of graphs are still infeasible.
  - **No graph-independent formula exists in these bases.**
  - Single features (`out/lp_*.txt` header, census 22–28): none is monotone along DL steps.
    - The strongest drift is in the chain counts: the number of {α,A} chains goes up / down on 14% / 42% of steps, and {α,B} on 42% / 14% (mirror images under the role cycle).
    - The lock-parity count odAA goes up on 44% of steps and down on 28%.
    - dF and dS are constant on 96% of DL steps.
- **Why no fixed formula can work (hand).**
  - Along a DL run, j advances by 3 (mod 5) and the colour roles cycle (α, μ, A, B) → (α, B, μ, A). Any feature that is a function of the local picture alone is periodic along the run.
  - Monotonicity must come from global data (component sizes and the like), and nothing forces those to drift in one direction.
  - The trivial ψ that works on runs, "position in the run" (the lifted λ-angle), is an orbit invariant, not a state function. It becomes multivalued exactly on all-DL cycles, with winding L/5.
- **DL runs.** Runs are short on the sphere (census 22–29 + order-30 sample, 11,359 holes: 248,794 runs of 2 states, 81,532 of 3, …, longest 21) and longer in TrackF's search graphs (up to 67, a bias of the search objective).

## 3. Class-level certificate (`tg_collect.py` cert, `tg_cycles.py`)

Because sphere all-DL cycles exist inside classes with filled states, the honest class-level question is how a cycle's class is forced to contain a filled state. Three certificates were measured for every class containing an all-DL cycle (sphere 20 distinct classes / 21 cycles; `out/summary.txt` counts 21 because the order-30 sample repeats p30.r10#1252; off-sphere 782 classes / 1,408 cycles):

| | sphere | off-sphere, parity-clean | off-sphere, with violators |
|---|---|---|---|
| classes / cycles | 20 / 21 | 329 / 630 | 453 / 778 |
| class contains a filled state | 20 | 329 | 453 |
| max distance, cycle state → non-DL state (dS) | 2 | 3 (4 classes) | 4 |
| max distance, cycle state → filled state (dF) | 3 | 4 | 5 |
| first exit lands on a filled state | never | never | never |
| Menger: vertex-disjoint drains cycle → filled = #cycle states | 16 / 20 | 325 / 329 | 389 / 453 |
| σ leaves DL at ≥ 1 cycle state | 21 / 21 | 630 / 630 | 778 / 778 |
| min share of cycle states where σ leaves DL | 0.35 | 0.25 | 0.25 |
| σ-escape rate at non-cycle DL states (mean) | 0.24 | 0.03 | 0.22 |

- **Escape types** (role pair : link positions met by the component). At sphere cycle states, 238 of the 420 states escape by σ (`aM:all`). The rest escape by interior components of {α,μ}, {α,A} touching x₀, {α,B} touching x₂, or link-free swaps.
- **Exit targets.** Exits go to no-lock states (521) and single-lock states (L1-only 336, L2-only 304). No exit goes directly to a filled state. A filled state is always one more move away (Lemma A).
- **Typical anatomy.**
  - At C30#0 the cycle reads `.s.s.s.s…` (σ escapes at every second state; dS alternates 2, 1).
  - At C40#0 σ escapes at all 20 states.
  - Census cycles mix `s` and `e`, e.g. p30.r10#1252: `ses.s.seseses.s.sess`.
  - 549 of the 630 parity-clean off-sphere cycles are exactly `.s.s…` / `s.s.…`, the C30#0 pattern. These are the verbatim copies TrackF noted.
- **Data conjecture σ-escape.** On any triangulated surface, every all-DL π-cycle at a degree-5 hole contains a state s at which σ(s) = swap K_{αμ}(x_{j+2}) is not DL.
  - With Lemma A this gives a filled state at distance ≤ 2 from that s.
  - It therefore implies LPC (and on the sphere PureClean ⇒ R\* ⇒ 4CT), so it is 4CT-strength and should not be expected to be easier.
  - Its merit is that it is a *single named move at a single state*, i.e. a uniform local form of the certificate.
  - Support: 1,429 cycles, min rate 25%.
  - Not tested: whether σ-escape holds at some state of every all-DL *orbit segment* of length ≥ 20.
- **The potential side.** A pure-cycle class would have Σw = N/5 > 0 by Theorem W (λ = +1 on every R3 step). So the only class-level potential that forbids it, among those of Theorem W's kind, is Σw ≤ 0, i.e. the quarter floor. Max-flow/min-cut adds nothing: the drains are full in 94–99% of classes, and the min cut is just the cycle itself.

## 4. Off the sphere: where does it break?

- **Nowhere in the certificate.**
  - Every off-sphere cycle class has filled states.
  - σ escapes on every cycle.
  - The only quantitative change is deeper escapes (dS 3–4) in classes with violators.
- **H¹ is where TrackF said it is.**
  - Every D1/D2 failure (lock-parity violator) in these classes has both crossing cycles (the lock chain through h and the α-chain through h) homologically non-trivial mod 2: D1 10,177 / 10,177 and D2 9,947 / 9,947.
  - Violators are the π-path ends: H¹ creates sources and sinks for π. It is not what makes a cycle closed.
- **Cycle states and H¹.**
  - On the sphere: 0 non-separating lock cycles (by Jordan).
  - Off the sphere, in parity-clean classes, 400 / 17,760 cycle states (2.3%) have a non-separating lock cycle. They lie on 73 / 630 cycles.
  - In violator classes the figure is 3,292 / 18,440 (17.9%).
  - States with slow escape (dS ≥ 3) have a non-separating lock cycle in 105 / 300 cases (35%). That is about 2× enrichment, not localisation.
- **ψ with homology features.** On off-sphere DL steps (38,752; `out/lp_off.txt`, `out/lp_off_hom.txt`):
  - adding `hom` raises per-hole feasibility for small feature sets (lockpar 83 → 139 / 478), but the null rises too (38 → 66);
  - for local / all the gain is 257 → 269 and 316 → 321, with the null moving 210 → 250 and 296 → 315;
  - the pooled share of steps satisfied stays at about 0.30.
  - So H¹ data does not supply the missing monotone quantity.

## 5. What would have to be true for the analogy to pay

- The analogy is accurate as bookkeeping:
  - λ is a discrete vorticity, and Theorem W is Stokes;
  - all-DL cycles are closed streamlines with circulation L/5;
  - on other surfaces H¹ supplies sources and sinks (violators = path ends, each one a crossing pair of non-separating cycles).
- But LPC is the statement "a source-free class is not all closed streamlines". A stream function certifies the absence of closed streamlines, and closed streamlines do occur on the sphere. So the argument would need a *class-level* conserved quantity whose sign is fixed by local duality (D1/D2) alone: LPC-¼ / Σw ≤ 0. Nothing tested here supplies it.
- The one concrete by-product worth keeping is the **σ-escape** data conjecture (§3): a local, single-move form of the certificate that holds on all 1,429 cycles, on four surfaces.

## Files

| path | content |
|---|---|
| `tg_engine.py` | per-hole state data: π, DL, locks, D failures, features, ℤ/2 homology of chain cycles, Kempe distances |
| `tg_collect.py` | DL→DL step features (`out/*.steps.jsonl`), per-hole summaries (`*.hole.jsonl`), cycle-class certificates (`*.cert.jsonl`) |
| `tg_lp.py` | LP feasibility (per hole, per graph, pooled, null, held-out) |
| `tg_cycles.py` | per-cycle anatomy: σ / other escape string, dS string, homology string, escape types and targets (`out/cycles_*.jsonl`) |
| `tg_summary.py` | aggregate tables → `out/summary.txt` (step files are stored gzipped, `out/*.steps.jsonl.gz`; both scripts read them) |
| `run_all.sh`, `run_cycles.sh`, `run_c30.sh` | the runs (nice'd, ≤ 2 workers) |
| `out/lp_*.txt` | LP results |
