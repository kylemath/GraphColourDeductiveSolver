# Night: single-cycle bound, pairing, assembly for the π-winding

Night worker, 7 October 2026 (started 6 October 23:5x; written 00:14 MDT). **Exploratory. Hand work plus small single-core checks. Unreviewed.**

Cited notes:
- **EH**: `NightEulerHole.md` (Theorem W, π, λ).
- **TA**: `NightThetaAttempt.md` §7.
- **WM**: `NightWindingMeander.md` (tokens, Proposition H, saturation).
- Run data: `local-runs/22-winding-escape/` and `local-runs/23-positive-cycles/` (orders ≤ 24, full gentri).

Labels:
- [proved]: a complete argument is given here, modulo EH Theorem W and QFB.
- [sketch]: an argument with a named gap.
- [conjecture]: not proved.
- [data]: computed with the scratchpad scripts of §6.

**Nothing here proves the floor, R\*, or any pairing statement.**

## Verdict

1. **Target 1 (single-cycle bound) is false on the sphere** [proved from definitions + data].
   - An all-DL π-cycle has w = L/5.
   - A plane triangulation with 37 vertices (flipped A₇, `run_dd/best-A7_exc.json`, hole 22) has an all-DL π-cycle of length 800, so w = +160. I re-traced it with my own π (§1).
   - So the length of an all-DL π-cycle is **not** bounded by 20 on the sphere. The premise "the sphere limits Γ-cycles to length 20" is false.
2. **Target 2, the strict pairing, survives** [data], but only in the form "each positive Z has a link-preserving neighbour of winding ≤ −w(Z)".
   - It holds in all 125 positive cycles at orders ≤ 24 (run 23).
   - It holds in all 13 positive classes sampled from the adversarial core graphs (§3), including w = +160 against −1042.
   - The mechanism is described exactly in Tait terms (§2): a link-free swap is a flip along closed dual curves that avoid P. It fixes both tokens, and it changes λ only through the lock-2 / M3 bit, i.e. through the crossing parity of WM's Proposition H.
   - No sign theorem for that change is proved.
3. **Target 3: injectivity is false, but weighted transport holds** [data].
   - "At most one positive cycle per class" is false. Adversarial classes contain up to 10 positive cycles.
   - In five classes, Hall's condition fails for a one-to-one assignment: 4 positive cycles share one negative neighbour.
   - What holds in every class tested is the **capacitated transport**: the positive windings can be routed to negative neighbours (one link-preserving swap from a DL state), with each negative cycle N carrying at most |w(N)|.
   - Transport ⇒ floor [proved, trivial]. Transport, the floor and the strict pairing each imply 4CT (§4), so none of them can follow from Jordan-only geometry.

---

## 1. Target 1: what bounds w(Z)

**Lemma 1.1 [proved].** For every π-cycle Z with F_Z filled states, w(Z) = (|Z| − 4F_Z)/5. This is also in WM.
- Hence −3|Z|/5 ≤ w(Z) ≤ |Z|/5.
- w(Z) = |Z|/5 ⇔ F_Z = 0 ⇔ Z is a Γ-cycle ⇔ every state of Z is DL.

*Proof.*
- Per cycle, 3F_Z − U_Z = −5w(Z) (EH Theorem W, per-cycle form), and U_Z = |Z| − F_Z.
- If F_Z = 0, every step is unfilled. A φ_B⁻¹ step would land on a filled state, so every step is R₊₃ (λ = +1) and every state has lock 2.
- Every state is also an R₊₃ image, so it has lock 1 (QFB). Hence it is DL.
- Conversely, an all-DL cycle has only R₊₃ steps. ∎

**Resolution of the "+1 per rotation versus w = 4 at L = 20" question.**
- λ = +1 is the change of σ over one rotation.
- w = Σλ/5 counts **net half-turns of the unordered token pair** (WM Lemma 1.2), and five rotations make one half-turn.
- So the 20-cycle has w = 20/5 = 4. This is consistent: w = L/5 for every all-DL cycle.

**The long DL cycles are genuine π-cycles [data, own code].**
- I used the 37-vertex graph `studiointel/path3-local/run_dd/best-A7_exc.json` (Euler check: 37 − 105 + 70 = 2), at hole 22.
- I found the class of 21,078 states (F = 8,922) by random colourings and Kempe BFS.
- I computed π exactly as EH §3 / `escape.py`, and asserted Theorem W on the class (Σw = −2,922 ✓).
- The class has 147 π-cycles. The positive ones (L, w, F_Z, #DL) are (800, **+160**, 0, 800), (20, +4, 0, 20) and (20, +4, 0, 20).
- The windings of the other cycles go down to −1,042 (two cycles of length 7,670).
- The 880-cycle of the C6 log (faces not saved) uses the same R₊₃ component. By Lemma 1.1 it is a π-cycle with w = **+176** [proved, conditional on C6's description "all-DL Γ-cycle"].

**So no bound on w(Z) independent of |Z| holds** [proved by example]. The order-≤ 22 picture (w ∈ {1, 2, 4}) was a small-order effect. Run 23 already has w = +8 at order 24.

**Torus question.** It is moot: the sphere itself allows unboundedly long all-DL π-cycles in practice (800 at n = 37). Unboundedness in principle is not proved. On the torus, π is not even defined in general (Lemma Π uses Jordan; WM §3).

## 2. Target 2: what a link-preserving swap does

Notation from WM §1:
- t is the triple Tait colour at P; s₁ and s₂ are the singles, on the token edges.
- C is the dual {s₁,s₂}-path joining the two tokens.
- B_T is the {t,s_T}-loop of the moving token.

**Lemma 2.1 (link-free swaps are flips along closed curves off P) [proved].**
- Let K′ be a {p,q}-component containing no link vertex, and let c = p + q.
- Swapping K′ exchanges the two Tait colours ≠ c along every curve of ∂K′.
- Every such curve is closed and avoids P: a dual curve passes through P only across a link edge with exactly one end in K′, and there is none.
- Consequences:
  - The link colouring is fixed, so the type (U_j or F_i), the tokens and σ are unchanged.
  - λ can change only through the bit that selects the π-row: lock 2 for unfilled states, M3 for filled ones.

**Lemma 2.2 (two kinds of swap) [proved].** Take an unfilled state, with Tait word (t,t,s₁,t,s₂).
- **t-chains** are swaps of a link-free {α,μ}- or {A,B}-component (α+μ = A+B = t).
  - They flip s₁ ↔ s₂ along closed components C′ of the C-system. C is unchanged as a curve.
  - Every {t,s}-curve, B_T included, is reconnected at its s_T-edges on C′: those edges become s_T′-edges, and the s_T′-edges of C′ become s_T-edges.
  - This is the shift-by-one reconnection of TA §6, now along a closed curve C′.
- **Other pairs** ({α,A}, {α,B}, {μ,A}, {μ,B}; sum s₁ or s₂) flip t ↔ s′ along closed {t,s′}-cycles.
  - They reconnect C itself, at its s′-edges on those cycles.

In both cases the new λ is read off from Proposition H: lock 2 ⇔ odd crossing parity of the new B_T with the new C.

**The sign question, stated exactly [sketch].**
- A t-chain swap changes lock 2 iff the reconnected B_T′ crosses C with the opposite parity.
- B_T′ is made of arcs of the old {t,s_T}-curves, which may be arcs of B_T or of closed {t,s_T}-cycles off P, spliced along C′. The arcs along C′ never cross C, because C′ and C are disjoint curves.
- So the parity change equals the parity of the crossings with C of the old arcs that are cut out or spliced in.
- Jordan forces only the total over each **closed** {t,s_T}-cycle to be even, not the total over each arc. **This is the gap.** There is no reason, per state, for the change to have a sign. It must be a statement about the whole orbit.

**Shadowing [proved, elementary].**
- Suppose κ (a link-free swap of K′) and the π-component at s are disjoint, and neither swap changes the other's component or the selecting bit.
- Then κ commutes with that π-step and λ(κs) = λ(s).
- So the π-orbit of t = κs **shadows** Z, with equal λ, until the first state where the selecting bit differs or K′ is absorbed into a π-component.
- Winding differences arise only at those break points.

**Test at gentri 17 #3, hole 0 (0-based #3, line 4 of tri17.txt) [data].**
- The class has 100 states: Z = (L 20, w +4), all DL, and the cycle (80, −16).
- At each of the 20 states, the link-free swaps fall into three patterns:
  - {α,μ}-component of size 2: maps Z to itself, so it shadows forever.
  - {α,μ}-component of size 5 (10 states): t is **not DL**. Its π-step is φ_B⁻¹ (−1), then τ, τ, φ_A (λ = −3, −3, −1) and so on, inside the −16 cycle. The swap breaks lock 2 immediately.
  - {A,B}-component of size 6 (10 states): t is DL, takes one R₊₃ step (+1), and then lock 2 fails (−1, −1, …), inside the −16 cycle. It shadows Z for one step.
- All three are t-chains, as WM observed. No {α,A}/{α,B} exit exists.
- In the 21,078 class (§1), from the +160 cycle, the swaps landing on negative cycles split as follows:
  - 1,996 land at a DL t with λ(t) = +1 (shadow ≥ 1 step);
  - 474 land at a non-DL t with λ = −1;
  - 72 land at a non-DL t with λ = +1.
- "Reverses the turning direction" is therefore **not** a per-swap fact. The same cycle also has link-free swaps into w = 0, +4 and +160 cycles. Only existence holds [data].

**Statement P (pairing) [conjecture; data 125/125 at orders ≤ 24 and 13/13 adversarial classes].** Every positive π-cycle Z has a DL state s and a link-free swap s → t with w(π-cycle of t) ≤ −w(Z).

## 3. Target 3: assembly

**Lemma 3.1 [proved, trivial].** Suppose there is a transport: weights f(Z,N) ≥ 0 on pairs (positive Z, negative N adjacent by a link-free swap) with Σ_N f(Z,N) = w(Z) and Σ_Z f(Z,N) ≤ |w(N)|. Then Σ_Z w(Z) ≤ 0 over the class, and the floor holds there.
- Strict pairing with an **injective** assignment is a special case.

**Injectivity fails; transport holds [data].** I sampled classes of the six saved C6 adversarial graphs: every degree-5 hole, 40 random colourings each, classes found by Kempe BFS. That gave 13 classes with positive cycles.
- Every one of them has ≥ 2 positive cycles, with up to 10 (A₆ hole 31: +132, 6 × +12, 3 × +4).
- Strict one-to-one matching to distinct negative neighbours with w ≤ −w(Z) fails in 5 classes. For example, A₇ hole 22, class of 2,124: four positive cycles (+16, +8, +4, +4), whose only negative neighbour is one −276 cycle.
- Capacitated max-flow, using swaps from DL states only, routes **all** positive winding in all 13 classes:
  - totals 168, 32, 32, 232, 32, 32, 216, 216, and so on;
  - each total is far below the capacity of the negative neighbours.
- Order 24 (run 23 special cases):
  - g906 h22 has two +4 cycles sharing negative neighbours, with two −40 cycles available;
  - g6864 h21 has +1 and +2, against neighbours −34 and −23.
  - Transport holds trivially in both.

**Conjecture T (transport) [conjecture].** In every Kempe class of T − v (T a plane triangulation, deg v = 5), the positive π-windings can be transported to negative cycles one link-free swap away, within the capacities |w(N)|.
- T ⇒ floor by Lemma 3.1.
- T is the right replacement for "pairing + one positive cycle".

## 4. Strength (why none of this can be proved by Jordan alone) [proved]

Let T be a minimal counterexample to 4CT (simple, min degree 5), and v a degree-5 vertex.
- T − v is 4-colourable and no state is filled, so every class has F = 0.
- By Lemma 1.1, every π-cycle is a Γ-cycle with w = L/5 > 0, and **there is no negative cycle**.
- So Statement P, Conjecture T and the floor all fail at T. Each of them, proved for all plane triangulations, implies 4CT.
- All local facts used above (Lemma Π, Proposition H, Lemmas 2.1–2.2, shadowing) hold verbatim in T.
- So a proof of P or T must import a counting input of unavoidability strength (TA §5, WM §2). The flip/crossing-parity mechanism of §2 only says **where** the sign change happens, not why it is paid for.

## 5. Status

| Item | Status |
|---|---|
| w(Z) = (\|Z\| − 4F_Z)/5; all-DL ⇔ Γ-cycle; w ≤ \|Z\|/5 | [proved] |
| Single-cycle bound (w ≤ 4, or any bound independent of \|Z\|) | **false** (w = +160 at n = 37, sphere) [data, own code] |
| All-DL π-cycle length bounded by 20 on the sphere | **false** (800) |
| At most one positive cycle per class | **false** (up to 10; order 24 already 2) |
| Link-free swap = flip along closed curves off P; fixes tokens; changes λ only via lock-2/M3 parity | [proved] |
| Sign of that change along an orbit | open; per swap it has no sign [data] |
| Pairing P (exists neighbour ≤ −w) | [conjecture], 125/125 + 13 adversarial classes |
| Injective pairing | **false** in 5 adversarial classes |
| Transport T ⇒ floor | [proved]; T itself [conjecture], 13/13 adversarial + all order ≤ 24 |
| P, T, floor each ⇒ 4CT | [proved] |

## 6. Reproduction (scripts in the session scratchpad, not committed)

- `cyc.py`: loads a C6 `best-*.json` face list, builds T − v, finds random 4-colourings, runs Kempe BFS, and computes π and λ exactly as `22-winding-escape/escape.py`.
- `find.py` / `pair.py`: the 21,078 class at A₇ hole 22, with its π-cycles and the neighbour windings of the positive cycles.
- `sweep.py` / `flow.py`: all degree-5 holes of the six C6 graphs, 40 colourings each; checks P, injective matching and capacitated max-flow (Edmonds–Karp).
- `g17.py`: gentri 17 #3 hole 0 swap patterns, using `common/kempe_py.py`.
- Single core under nice. The whole sweep took about 15 minutes on AC power.
