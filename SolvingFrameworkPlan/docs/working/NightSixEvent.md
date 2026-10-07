# NightSixEvent: the six-event lemma in component counts, on closed orbits

Night worker, 7 October 2026 (written 04:58 MDT). **[exploratory] Unreviewed.** MacBook on AC (pmset: AC power, 100%, charged). Python on 1 core: about 2 s for the dump and 2 min for gentri 20–23.

Builds on `NightW2Euler.md` (pair dualities, the recursion, the six events), `NightW2.md` §1–§3, §10–§11, and the Lean frames `QuarterW2Frame`, `QuarterFixR1`, `QuarterWindow`, `QuarterLockJ`, `QuarterMirror`.

Scripts and outputs: `backgroundMaterial/planemap-structural/longtable/local-runs/34-nightsixevent/`.
- `cyc.py` writes, for every state of every Γ-cycle and of every open DL run through an R3k2 state, the six component counts in that state's frame, σ-fixedness, locks, and the {α,·} edge counts.
- Data: the 34 hole-orientations of `jobak-66dump.json` plus p25 #668 (`dump.jsonl`: 62 Γ-cycles of length 20, so 124 periods and 1,240 Γ steps). As an open-run control, gentri orders 20–23 (`gentri.jsonl.gz`, no Γ-cycles). Γ gap statistics are cross-checked on Job AY (`jobay-periods.jsonl`: 304 degree-6 cycles, 896 periods).

Labels: **[proved]** by hand; **[data]** with counts; **[killed]**.

## Verdict

1. **[proved] In counts, the six events are three numbers equal to 1.** Write f, g, h for C(αμ), C(αB), C(αA) at a state, in its own frame.
   - On an all-DL orbit, W2 fails in a period ⇔ f₄ = f₆ = f₈ = 1.
   - The two outer events ("merge at step 3", "split at step 8") are exactly g₃ ≥ 2 and h₉ ≥ 2. These are Lock1@3 and Lock2@9, which hold automatically on a closed orbit.
   - The six events come in pairs, one pair per fixed point. So a DL period has 0, 2 or 4 of them, never 5. "At most 5 of 6" is a bookkeeping artefact.
2. **[proved] Per-step count identities.** Step i (the {α,A}-swap on K) satisfies:
   - it fixes (C, rank) of G_{αA} and of G_{μB};
   - **ΔE(αB) − ΔE(αμ) = 1 exactly**, by a local face count that uses only the hole (§2.2);
   - from this and the dualities, ΔC(μA) = ΔC(αB) + 1 + ΔC(AB) − ΔC(αμ), and ΔR is odd.

   The change is confined to the Lock2 disc. No a-priori bound on |ΔC| exists beyond that confinement. The observed ranges are in §2.3.
3. **[killed] "The closure kills the outer events" is the wrong target.** On a closed orbit the outer events are forced, not forbidden (Verdict 1). Time reversal maps the window 4..8 to itself (4 ↔ 8, 6 ↔ 6, g ↔ h, `QuarterMirror`), not to the previous period. So there is no implication chain of the form "outer event ⇒ contradiction ten steps back". What the closure must forbid is the middle: f₄ = f₆ = f₈ = 1.
4. **[data, new] On Γ, F₄ forbids every fixed point at positions 5, 7 and 8, not just F₈.**
   - Over 48 F₄ windows (dump) and all 896 Job AY periods: F₄ ∧ F₅, F₄ ∧ F₇ and F₄ ∧ F₈ each occur 0 times. By the mirror, F₈ forbids positions 7, 5 and 4.
   - Open runs: dump 1 / 4 / 23; gentri 135 / 115 / 76.
   - In absolute-graph language, after G₁₂ is connected at R3k2, **none of the three α-graphs is connected again at positions 5, 7, 8 on Γ.** Only position 6 (G₁₃) may be connected.
5. **[data] No local or fixed-distance version.** gentri has 4 W2\* failures (F₄ ∧ F₈) with DL at both positions 3 and 9. Two of them are full W2 failures, with run extents (back, fwd) = (2,2) and (3,1).
6. **Not proved.** The single missing implication is in §4.

## 1. The six events as counts [proved]

**Role rotation.** μ_{i+1} = B_i, A_{i+1} = μ_i, B_{i+1} = A_i (NightW2Euler §2; `frm_step`, sig = ![0,3,1,2]). So each absolute graph G_{1c} passes through the roles **free → A → B → free**, one role per step:
- it is changed by the step that leaves its free slot (f_i → h_{i+1});
- it is frozen by the next step (h_{i+1} = g_{i+2});
- it is changed by the step after that (g_{i+2} → f_{i+3}).

Hence every step i does exactly two things:
- it **splits or reshapes the free graph**, f_i → h_{i+1} (≥ 2 if state i+1 is DL);
- it **merges or reshapes the B-graph**, g_i → f_{i+1} (σ fixed at i+1 ⇔ the result is 1).

(Checked: g_{i+1} = h_i on 1,240/1,240 Γ steps; fix ⇔ f = 1 on 1,240/1,240.)

**The window.** Free slots: G₁₂ at positions 4, 7, 10; G₁₃ at positions 3, 6, 9; G₁₄ at positions 5, 8.

| event (NightW2Euler §3) | count statement | on an all-DL orbit |
|---|---|---|
| step 3 merges G₁₂ | g₃ ≥ 2 and f₄ = 1 | g₃ ≥ 2 is Lock1@3, automatic |
| step 4 splits G₁₂ | f₄ = 1 and h₅ ≥ 2 | h₅ ≥ 2 is Lock2@5, automatic |
| step 5 merges G₁₃ | g₅ ≥ 2 and f₆ = 1 | automatic part: Lock1@5 |
| step 6 splits G₁₃ | f₆ = 1 and h₇ ≥ 2 | automatic part: Lock2@7 |
| step 7 merges G₁₄ | g₇ ≥ 2 and f₈ = 1 | automatic part: Lock1@7 |
| step 8 splits G₁₄ | f₈ = 1 and h₉ ≥ 2 | h₉ ≥ 2 is Lock2@9, automatic |

(DL ⇒ g, h ≥ 2 is rank(μA) = g − 2 ≥ 0 and rank(μB) = h − 2 ≥ 0.)

So **six events ⇔ f₄ = f₆ = f₈ = 1** on an all-DL orbit, and each fixed point carries its own merge/split pair. On open runs, the "missing outer events" are lock deaths, g₃ = 1 or h₉ = 1 (NightW2Euler §4). That is a property of open runs; on Γ it cannot occur.

Via the dualities, f_i = 1 ⇔ rank(AB)_i = 0, i.e. the forest-pair form of Lemma Fix (`fixed_at_pos`).

## 2. What one R₊₃ step does to the counts

### 2.1 Fixed and moving pairings [proved]

The {α,A}-swap on K exchanges, along K's boundary edges, αμ ↔ Aμ and αB ↔ AB.
- It fixes C and rank of G_{αA} and G_{μB}.
- It moves only the pairings {αμ|AB} and {αB|μA}.

Let x = ΔC(αμ), y = ΔC(αB), u = ΔC(AB), v = ΔC(μA), all in the old colour names. Write the dualities at both states; the frame rotates, so the chord corrections move: rank(AB) goes from f − 1 to C(αμ) − 2, and rank(μA) goes from g − 2 to C(αB) − 1. Then:
- Δrank(αμ) = u and Δrank(AB) = x − 1;
- Δrank(αB) = v and Δrank(μA) = y + 1;
- **v = y + 1 + u − x**, and ΔR = 2(y + u) + 1 is odd. This is NightW2Euler's parity, now proved.

### 2.2 The edge lemma [proved; data 2,137/2,137]

**ΔE(αB) − ΔE(αμ) = 1 on every DL → DL step.** Equivalently, e(K_A, B) − e(K_α, B) − e(K_A, μ) + e(K_α, μ) = 1.

*Proof.* Count the contribution of each triangle of T − h to the left side. A triangle meeting K has either:
- two K-vertices (one α, one A) and a third vertex X ∈ {μ, B}, contributing (+1 − 1) = 0; or
- one K-vertex and two vertices coloured μ and B, contributing 0.

Every edge lies in two triangles except the five link edges, which lie in one. So 2·LHS = (link-edge contributions). K ∋ x_{j+2}, x_{j+3}, and K ∌ x_j because Lock2 separates them. So the only link edges from K to {μ, B} are:
- x_{j+1}x_{j+2} (μ–α of K), contributing +1;
- x_{j+3}x_{j+4} (A of K–B), contributing +1.

Hence LHS = 1. ∎

The vertex changes of G_{αμ} and G_{αB} are equal (|K_A| − |K_α|). So Δχ(αμ) − Δχ(αB) = 1, and with 2.1 this gives d₂ = d₁ + 1, which is the duality's "+1" made local.

### 2.3 Confinement and sizes [proved / data]

- **Confinement.** Lock2 (the {μ,B}-chain x_{j+1} → x_{j+4}, untouched by the swap) closes through h to a Jordan curve. K lies in the open side D₂ containing x_{j+2} and x_{j+3}. Every component of G_{αμ} or G_{αB} that avoids D₂ ∪ N(K) is unchanged.
- **The B-graph before the step.** G_{αB} cannot cross Lock1 (μA, through x_{j+3} ∈ K). Its ≥ 2 components are "inside Lock1" (∋ x_{j+2}) and "outside" (∋ x_j, x_{j+4}).
- **What a full merge needs.** For g_i → 1, the new α-vertices K_A must touch every old αB-component not meeting K_α, through B-neighbours. In particular they must bridge Lock1. That is possible only through A-vertices of the Lock1 chain that lie in K and turn α; x_{j+3} is always one of them.
- **[data] Γ ranges** (1,240 steps): Δg = f_{i+1} − g_i ∈ [−3, 2] and Δf = h_{i+1} − f_i ∈ [−2, 3]; ΔR ∈ {±1 (1,004), ±3 (236)}. Open runs reach ΔR = ±5. Per-position tables are in `an1-out.txt` and `an3-out.txt`.
- **No general bound on |ΔC|.** A single swap can split or merge arbitrarily many components, since K is unbounded. I found no sign rule tied to the lock chains beyond confinement and the merge requirement above.

## 3. Closed orbits: what the data says the closure does [data]

Γ = 124 periods (dump) for windows; 896 Job AY periods for gaps.

**Fixed-point gaps** (`an6-out.txt`, cyclic on Γ):
- Within 4..8, Γ never has a fixed pair (4,5), (4,7), (4,8), (5,8) or (7,8). Γ does have (4,6) ×71, (6,8) ×71, (5,6), (6,7), (5,7) (Job AY).
- Open runs (dump / gentri): (4,5) 1/135, (4,7) 4/115, (4,8) 23/76.
- Gap 4 does occur on Γ elsewhere: positions 9 → 3, ×2 in Job AY. Gap 6 also occurs: 8 → 14, ×10. So "no gap 4" is specific to the position-4 start, not a uniform spacing rule.

**Trajectories after F₄** (`an5-out.txt`). On Γ the 48 F₄ windows have:
- G₁₂ free-value at 7: f₇ ∈ {2, 3};
- G₁₄ at 5 and 8: f₅, f₈ ≥ 2;
- G₁₃ at 6: f₆ = 1 in 36/48.

On open F₄ windows, f₇ = 1 is common, and so are f₅ = 1 and f₈ = 1.

**No fixed-distance statement** (`gentri.jsonl.gz`). There are 4 W2\* failures with DL at 3 and 9, 2 of them full W2 failures, with (back, fwd) = (2,2) and (3,1). With Job AL's order-27 runs of 21–29 steps, this kills every "DL within c steps" version. The closure enters globally.

## 4. The single missing implication, and its test

**Target (W2\* on Γ, the 0/896 statement that implies W2):**

> On an all-DL π-orbit at a Hole6 of period 10 (`gamma_period_ten`), C(G₁₂) = 1 at R3k2 ⇒ C(G₁₄) ≥ 2 at R3k0 (absolute colours of `QuarterW2Frame`).

In counts:
- a₂(4) = 1 ⇒ a₄(8) ≥ 2;
- a₄ runs g₄ →K₄ f₅ →K₅ h₆ = g₇ →K₇ f₈. Here K₄ and K₇ are the two {1,3}-swaps through p (`steps_pos4_to_7`).
- So the failure is "K₇ completes a merge of G₁₄, after K₄ split G₁₂ from a single component."

What I could not supply is the global input: some quantity carried around the closed orbit that a₂(4) = 1 ∧ a₄(8) = 1 would force to drift. The obvious ones are dead:
- R is periodic with odd steps, and linear potentials cancel (NightPotential);
- the edge lemma gives ΣΔE(αB_i) − ΣΔE(αμ_i) = L, a pure counting identity with no sign content.

**Sharpest test I can state.** On Γ (dump + Job AY), F₄ ⇒ ¬F₅ ∧ ¬F₇ ∧ ¬F₈ (0 counterexamples), against 135/115/76 on open gentri runs. The test is whether the **weakest** of these, F₄ ⇒ ¬F₇, has a proof on Γ:
- it is a statement about one graph, G₁₂, at two consecutive free slots (4 and 7);
- in between, G₁₂ is split by K₄, frozen by K₅, and re-merged by K₆ ({1,4}, ∋ x₃, x₄, m, z).

Request for a Studio job:
- On every Γ period with F₄, and on every open run with F₄ ∧ F₇, list the G₁₂-components at position 6 that K₆'s old-1 vertices (new 4) do not reach. These are the components that stop a₂(7) = 1.
- If on Γ one of them is always the component of w₃ (colour 2 throughout positions 4–8, NightW2 §10.1), and on the open F₄ ∧ F₇ runs it never is, then the missing one-line implication is: **"on Γ, w₃'s G₁₂-component at position 6 avoids N(K₆)."**
- This would tie F₄ ⇒ ¬F₇ to the ring candidate R of NightW2 §10.4.
- If no such component exists, then F₄ ⇒ ¬F₇ is as global as W2\* itself, and this route is dead.

## Reproduction

In `local-runs/34-nightsixevent/` (1 core):
- `python3 cyc.py dump dump.jsonl` (2 s);
- `python3 cyc.py 20,21,22,23 gentri.jsonl` (2 min; stored gzipped, so `gunzip -k` it first);
- `an1.py` (recursion and Δ tables), `an3.py` (ΔR), `an5.py` (a-trajectories after F₄), `an6.py` (fixed-point gaps); outputs in `an*-out.txt`;
- `an7.py dump.jsonl` checks the edge lemma (reads `E` from `dump.jsonl`; output `an7-out.txt`).
