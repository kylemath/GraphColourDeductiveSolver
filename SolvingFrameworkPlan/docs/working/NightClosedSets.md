# Night: swap-closed unfilled sets (extending no-frozen from |S| = 1)

Night worker, 7 October 2026 (written 00:24 MDT). **Exploratory. Hand work plus small single-core checks. Unreviewed.**

Cited notes: **NF** = `StudioMathLean/.../PlaneMap/NoFrozen.lean`; **QRP** = `QuarterRotationPlanar.lean` (`rot3_bijOn_planar`, `kempe_hex`); **WM** = `NightWindingMeander.md`; **CB** = `NightCycleBound.md`; **TA** = `NightThetaAttempt.md`.

Labels: [proved] complete argument here (modulo the cited Lean files); [sketch] gap named; [conjecture]; [data] scratchpad scripts of §8.

**Nothing here proves R\*.** A swap-closed unfilled set at a degree-5 hole of a plane triangulation is exactly a targetless Kempe class, and its non-existence implies 4CT (§6).

## Verdict

1. **Closure made precise** [proved]. S is a union of targetless Kempe classes, every state is DL, and each state has exactly 8 link-touching Kempe components whose swaps (all in S) are listed in §1. New consequence: **|S| ≡ 0 (mod 5)** and S is a disjoint union of Γ-cycles. This is the direct generalisation of the no-frozen lemma (|S| = 1 is the case "not ≡ 0 mod 5"), and it uses separation exactly where NF does.
2. **Extremal choice fails for every quantity tried** [proved + data]. Rotation is equivariant on the swapped components (K_B(R₊₃s) = K_A(s)), so no quantity can descend along rotations; descent must use another swap. For all 14 candidate quantities (both min and max), there are DL states whose whole Kempe neighbourhood is DL and no neighbour is strictly smaller, including at the deepest DL states that exist (depth 3) and on the +160 cycle.
3. **The coordinator's per-state lemma** ("at a DL state some link-free component meets a lock chain, and swapping it breaks a lock") is **false** state by state [data]: saturated DL states have no link-free component at all, and many DL states have every link-free swap landing on a DL state.
4. **First point where the induction cannot proceed:** the descent step at a Q-minimiser of S (§6). Everything before it is formal or elementary; the descent step, for any state-function Q, holds in a hypothetical minimal counterexample only if 4CT does.

---

## 1. What "closed under all swaps" gives

Setting: T plane triangulation, h of degree 5, G = T − h, link x₀…x₄ in rotation order. An unfilled state has link (α, μ, α, A, B) at positions j, …, j+4; j is unique (renaming-invariant). m = x_{j+1}, a = x_{j+3}, b = x_{j+4}. Lock 1: m, a in one {μ,A}-component L₁. Lock 2: m, b in one {μ,B}-component L₂.

**Lemma C1 [proved; graph-only].** Let S be nonempty, closed under every whole-component Kempe swap, with no filled state. Then S is a union of Kempe classes and every state of S is DL.
- Swaps are involutions, so closure = union of components of the Kempe graph.
- Unfilled without lock 1: swap the {μ,A}-component of m (it misses a); the link becomes (α, A, α, A, B), filled. Without lock 2: swap the {μ,B}-component of m; link (α, B, α, A, B), filled. Both contradict closure.

**Lemma C2 (the eight link-touching components) [proved; uses NF].** At a DL state the components meeting the link are exactly:

| pair | component | link vertices | swap result |
|---|---|---|---|
| {α,μ} | Λ_αμ | x_j, x_{j+1}, x_{j+2} (consecutive) | link-preserving |
| {A,B} | Λ_AB | x_{j+3}, x_{j+4} (adjacent) | link-preserving |
| {μ,A} | L₁ | m, a | link-preserving (lock-1 renaming) |
| {μ,B} | L₂ | m, b | link-preserving (lock-2 renaming) |
| {α,A} | K_A | x_{j+2}, x_{j+3} | R₊₃: unfilled at j+3 |
| {α,A} | K_A⁰ | x_j | unfilled at j+3, word (A,B,A,μ,α) |
| {α,B} | K_B | x_j, x_{j+4} | R₊₂ = R₊₃⁻¹: unfilled at j+2 |
| {α,B} | K_B⁰ | x_{j+2} | unfilled at j+2 |

- K_A ≠ K_A⁰ and K_B ≠ K_B⁰ is exactly NF (`not_reach_alpha_A_of_lock2`, `not_reach_alpha_B_of_lock1`). This is the **only** place the sphere enters Lemma C2.
- Consequently the number of link-meeting components is the constant 8 on DL states (the quantity "meet" of §3 is stationary everywhere, as observed), and Σk − 8 = number of link-free components (WM Lemma 2.2).

**Corollary C3 (|S| ≡ 0 mod 5) [proved; uses QRP].** Write S_j for the states of S with repeat position j.
- By `rot3_bijOn_planar`, R₊₃ (swap of K_A) maps Lock2-at-j states bijectively onto Lock1-at-(j+3) states, with inverse R₊₂ (swap of K_B). In S every state is DL and R₊₃(S) ⊆ S, so R₊₃ is a permutation of S mapping S_j onto S_{j+3}.
- Hence |S_0| = … = |S_4| and **|S| = 5|S_0|**. Every R₊₃-orbit has length L with 3L ≡ 0 (mod 5), i.e. 5 | L: S is a disjoint union of Γ-cycles (all-DL π-cycles, w = L/5, CB Lemma 1.1).
- The no-frozen lemma is the statement |S| ≠ 1; C3 extends it to |S| ∉ {1,2,3,4} and to every |S| ≢ 0 (mod 5). On the torus the frozen set has |S| = 1 (consistent with WM §4: 3F − U = −1 ≢ 0 mod 5).
- [proved] K_A⁰-swap maps S_j → S_{j+3} and K_B⁰-swap maps S_j → S_{j+2}; the K_A⁰-swap at j is the K_B⁰-swap at j+3 read backwards. These give no further congruence that I could find.

**Closure conditions, stated as constraints on one s ∈ S [proved, by C1].** Every swap of s lands on a DL state. Concretely:
- (C-rot) R₊₃s is DL: there is an {A,B}-path from b to x_{j+2} in R₊₃s (new lock 2; new lock 1 is the old L₂, untouched). Symmetrically for R₊₂.
- (C-0) swap(s, K_A⁰) is DL: there is an {α,B}-path from b to x_{j+2} after the swap (new lock 1 is again L₂). Similarly for K_B⁰.
- (C-lf) For every link-free component K′ of every pair, both locks survive the swap.

**Half-safety of link-free swaps [proved, trivial].** A link-free {μ,A}- or {α,B}-swap preserves lock 1 (L₁ is another component of the same pair, or the colours are disjoint); a link-free {μ,B}- or {α,A}-swap preserves lock 2. Only t-chains ({α,μ}, {A,B}) can threaten both. A link-free swap of K′ can break lock i only if K′ ∩ Lᵢ ≠ ∅ (necessary, not sufficient: the swap also creates new lock-colour vertices that may reroute the lock).

## 2. The extremal choice and why rotation cannot descend

**Lemma E1 (rotation equivariance) [proved].** Let s′ = R₊₃s (repeat position j′ = j+3, word (α′,μ′,α′,A′,B′) = (α, B, α, μ, A)). Then, as vertex sets,
- K_B(s′) = K_A(s) (swapping it back is R₊₂);
- K_B⁰(s′) = K_A⁰(s) (the {α,A}-component of x_j is disjoint from K_A, so untouched);
- L₁(s′) = L₂(s) (the {μ,B}-chain, untouched);
- K_A(s′) = the {α,μ}-component of x_j in s′, and L₂(s′) = the new {A,B}-chain of (C-rot).

So along a Γ-cycle s₀, s₁, … the sequences satisfy |K_B(s_{i+1})| = |K_A(s_i)| etc.: every quantity of §3 built from these sets is a cyclic shift along the cycle and cannot be monotone. **A descent at the minimiser must use one of the other six link-touching swaps or a link-free swap.**

**The task's step 3, carried out [sketch → fails].** Choose s ∈ S with |K_A(s)| minimal, rotate to s′.
- Jordan in s (TA): K_A lies on the x_{j+2}-side of the lock-2 curve h–m–L₂–b–h (it cannot meet {μ,B}); K_B on the x_j-side of the lock-1 curve.
- Jordan in s′: K_A(s′) (pair {α,μ}) lies on the x_j-side of the new lock-2 curve h–b–(new {A,B}-chain)–x_{j+2}–h.
- **There is no inclusion between K_A(s′) and K_A(s)** (different colour pairs, regions bounded by different chains). Minimality of |K_A(s)| therefore says nothing about s′, and the same holds for the K_A⁰/K_B⁰ and lock swaps (they change the pair that plays the role of {α,A}). This is the first concrete point where the argument stops; the data of §3 show it is not an artefact of the choice.

## 3. Candidate quantities tested as proxies [data]

Proxy (since no swap-closed unfilled set is known): an **interior** DL state is one whose every non-renaming Kempe neighbour is DL; Q is **stationary** at an interior state if no neighbour has strictly smaller Q. A descent lemma for Q (needed at the minimiser of S, which is interior at every radius) is refuted by any stationary interior state. **Depth** of a DL state = Kempe distance to the nearest non-DL state (interior ⇔ depth ≥ 2).

Exhaustive gentri, orders 17–21, every degree-5 hole: 89,017 DL states; interior 1,759 (depth 2: 1,661; depth 3: 98; **no DL state of depth ≥ 4**). Order 17 alone: 775 DL, 158 interior, 38 of depth 3.

| Q | stationary interior (min) | (max) | stationary at depth 3 (min) | 17#3 Γ-cycles: states with no DL-neighbour smaller (of 40) | +160 cycle (800): no DL-neighbour smaller | +160: stationary interior |
|---|---|---|---|---|---|---|
| \|K_A\| | 632 | 573 | 48 | 20 | 366 | 106 |
| \|K_B\| | 631 | 600 | 50 | 20 | 326 | 112 |
| \|K_A\|+\|K_B\| | 388 | 444 | 32 | 10 | 160 | 106 |
| min(\|K_A\|,\|K_B\|) | 931 | 614 | 60 | 30 | 510 | 106 |
| \|K_A⁰\|+\|K_B⁰\| | 395 | 430 | 21 | **0** | 31 | 10 |
| \|L₁\| | 874 | 1212 | 53 | 40 | 226 | 167 |
| \|L₂\| | 879 | 1231 | 60 | 40 | 233 | 40 |
| \|L₁\|+\|L₂\| | 662 | 1019 | 31 | 40 | 70 | 25 |
| d(m,a) in L₁ | 926 | 878 | 44 | 10 | 200 | 40 |
| d(m,a)+d(m,b) | 514 | 758 | 29 | **0** | 40 | **0** |
| Σk (all components) | 1056 | 227 | 72 | 20 | 208 | **0** |
| link-meeting components | 1759 (constant 8) | 1759 | 98 | 40 | 800 | 310 |
| link-free components | 1056 | 227 | 72 | 20 | 208 | **0** |
| {α,A}-vertices outside K_A | 580 | 603 | 39 | 10 | 95 | 14 |

- +160 cycle: `run_dd/best-A7_exc.json`, hole 22, the class of 21,078 states (F = 8,922; found at the 2nd random colouring). Its Γ-cycles: L = 800, 20, 20. Depths on the 800-cycle: 490 at depth 1, 310 at depth 2; max depth in the whole class is 2.
- Gentri 17 #3 holes 0 and 16: the only Γ-cycles at orders ≤ 21 (L = 20 each).
- Reading: every quantity is stationary somewhere among interior states, including at the deepest states available. The two that never stall on the named Γ-cycles (|K_A⁰|+|K_B⁰|, d(m,a)+d(m,b), and Σk on the +160 cycle) stall at 21–1056 interior states elsewhere. Note the data cannot test anything at depth ≥ 4 (no such states exist at these orders), while the minimiser of a hypothetical S has infinite depth.
- Depth ≤ 3 is consistent with Conjecture R's known maximum radius 4 (T4, order 17; `MathRadiusCensus/PREREG_DRAFT.md`): radius ≤ depth + 1.

## 4. The coordinator's mid-task lemma

Proposed: "at a DL state on the sphere, some two-colour component meeting no link vertex contains a lock-chain vertex", to be used with (C-lf).

- **False per state** [data]: DL states with **no link-free component at all** (saturated, Σk = 8): 136, 90, 161, 1,169, 3,266 at orders 17–21 (4,822 total; the order-17 to 19 figures match WM §2). At such a state the lemma fails vacuously, and (C-lf) is empty.
- **The premise "such a swap must break a lock at once" is also false** [data]: DL states at which **every** link-free swap lands on a DL state: 26,072 of 89,017 (includes the saturated ones); 10 of 20 states on each 17#3 Γ-cycle; 310 of 800 on the +160 cycle (exactly the interior ones). CB §2 already records 1,996 link-free swaps from the +160 cycle into negative cycles landing at DL states.
- What is true is the class-level form: WM Corollary 2.3 (a π-cycle of saturated states is a whole class) and the transport data. In a targetless S, (C-lf) is a constraint on every state; refuting it needs a class-level count, which is R\*-strength (§6).

## 5. Torus sanity

Frozen torus state (local-runs/18-torus-floor, n = 16): S = {s}, every pair graph connected.
- C1 holds (graph-only).
- **C2 fails at its one sphere step:** {α,A} is connected, so K_A = K_A⁰ ∋ x_j (NF's separation fails), and the swap of K_A is a renaming; R₊₃s = s.
- **C3 fails accordingly:** R₊₃ does not move j up to renaming, |S| = 1 ≢ 0 (mod 5).
- Any descent step fails vacuously: s has no non-renaming neighbour.
So the argument breaks on the torus exactly at the separation step, as required.

## 6. Where the induction cannot proceed

The chain is:
1. S closed, unfilled ⇒ all DL (C1) [proved, graph-only].
2. ⇒ 8 link-touching components, rotations defined, S = ⊔ Γ-cycles, |S| ≡ 0 mod 5 (C2, C3) [proved; NF + QRP; sphere enters here only].
3. Choose s ∈ S minimising Q; show some swap of s lands on a DL state with smaller Q, or on a non-DL state. **This step cannot be carried out.**
   - Along rotations it is impossible for any Q (E1).
   - For the 14 natural planar Q, the required local statement is false at interior states of depth 2 and 3 on the sphere (§3).
   - For **any** state-function Q the statement "every DL state of depth ≥ r has a DL neighbour with smaller Q" implies R\* (then a Q-minimiser of a targetless class contradicts it), hence 4CT: in a minimal counterexample T with deg v = 5, every Kempe class of T − v is a swap-closed unfilled set, and steps 1–2 hold verbatim there (CB §4). So step 3 must import a counting/unavoidability input; no Jordan/Euler fact at one state, or along one Γ-cycle, supplies it.

**Precise first failure:** step 3, at the comparison between s and R₊₃s: the minimised object (K_A(s), pair {α,A}) and the corresponding object at the rotated state (K_A(R₊₃s), pair {α,μ}) are components of different colour pairs with no inclusion, and every non-rotation swap likewise re-labels the pair; the data show this is not repaired by any of the tested quantities.

**What survives** [proved]: |S| ≡ 0 (mod 5) for every swap-closed unfilled set on the sphere (no-frozen is the case |S| = 1). [conjecture, data-only] DL depth ≤ 3 on the sphere (orders ≤ 21 exhaustive, A₇ class depth ≤ 2); this is a bounded form of R\* and is at least 4CT-strength.

## 7. Status

| Item | Status |
|---|---|
| Closed unfilled S = union of targetless classes, all DL | [proved] |
| Exactly 8 link-touching components at a DL state (sphere via NF) | [proved] |
| \|S\| ≡ 0 mod 5; S = ⊔ Γ-cycles | [proved], modulo QRP |
| Rotation equivariance K_B(R₊₃s) = K_A(s) | [proved] |
| Descent for \|K_A\| (task step 3) | fails: no inclusion; 632 stationary interior states [data] |
| Descent for 13 other quantities | fails at interior states, incl. depth 3 [data] |
| Coordinator's per-state link-free lemma | false [data] |
| Max DL depth ≤ 3 | [conjecture], orders 17–21 + A₇ class |
| Torus: breaks at C2 (separation) | [proved] |

## 8. Reproduction (session scratchpad, not committed)

- `q.py`: gentri orders given on the command line, every degree-5 hole, uses `longtable/local-runs/common/kempe_py.py` with `link = rot[h]`; computes DL, the 14 quantities, interior/depth, saturated and link-free-closed counts, Γ-cycles (all-DL R₊₃ orbits). Orders 17–21: 24 s single core.
- `a7.py`: `best-A7_exc.json` hole 22; random colouring + Kempe BFS until the 21,078 class (seed 1, trial 1); same tests on its Γ-cycles. A few minutes single core, AC power.
