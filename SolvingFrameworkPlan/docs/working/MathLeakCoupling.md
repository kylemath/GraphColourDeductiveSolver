# Leak coupling: a pattern automaton for (5,5,6,6,6), and explicit planar realisations of consecutive leaks

Math research worker, front 1, 6 October 2026. **Hand only.** No code was run; files were only read. Labels: [hand] derived here, unchecked by a second reader; [cert] read from Studio certificate files; [open]; KILLED = dead end, with the reason. No other file was edited, and nothing was committed.

Inputs: MathRstar55656.md, MathOneStarF1.md, MathTwoSixNeighbours.md, MathRstar55566.md + review, MathTaitGlobal.md, pd2_lock_proof.md, and the certificate `studiointel/run-C-2026-10-06/cert/91a307d1852a1764.graph.json` (face list, read by hand).

**Redirect (coordinator, mid-task).** (5,5,6,5,6) and F1 = (p,5,5,6,5) contain RSST 2.122 (a (5,6,5) run in the link), so they are vacuous in the minimal-counterexample frame. The first instance must be a diamond-free, 2.122-free class: (5,5,6,6,6), (5,6,6,6,6) or (6,6,6,6,6). §2–§5 treat **(5,5,6,6,6)**. §1 is the pre-redirect work on (5,5,6,5,6); it is kept because it settles the question posed there.

## 0. Verdict, first

1. **No leak-coupling lemma is proved.** [open] In both classes, what I found is the opposite: **explicit planar realisations** in which all the listed leaks of several consecutive F-states coexist with all their locks.
2. **(5,5,6,5,6) [hand + cert graph] (§1).** The radius-5 certificate graph realises **five consecutive Γ₁ states**, N3 → L2 → M(O3) → O6 → M(L3), each with every leak of MathRstar55656 §3 present. I checked every leak path by hand against the face list. This kills every coupling lemma for that class that spans at most 5 consecutive states, uses only the local ball, Jordan and the listed leaks, and lies on this stretch. Candidate Lemma C (N3 →B M(L2)) is *not* refuted, because the certificate's M(L2) is exactly the state where the leak fails.
3. **(5,5,6,6,6) automaton [hand] (§2).** There are **69 doubly locked (DL) ring patterns** that survive the one-move kills: 16 + 12 + 12 + 16 + 13 over the five positions of the 5-5 pair. F acts on them as follows:
   - a **deterministic 10-cycle Γ_a** with **no branch constraint at all**. Its F-steps do not depend on the outside, and no one-move kill fires on it: starvation, AB, F-E1′/B-E1″, G-F, G-B;
   - a **59-state set Γ_b** with free and forced branches;
   - one transient pattern (A2, which has no F-preimage, so radius ≤ 2).

   Γ_a alternates gdbab / dgdbg, as in HP, Γ₁ and Γ. One turn of Γ_a permutes the three non-repeated colours by a 3-cycle (absolute check, §2.4).
4. **Leak table on Γ_a [hand] (§3): 17 distinct leaks.** Two corrections to the earlier leak model:
   - **At J10 the G-component of x₃x₄ is confined to {x₃,x₄}, so a "flank ∈ G-comp" leak is impossible.** The only way to block the flank kills is a **link-free {g,d}-collar Q** that joins both flanks of x₁ around the outside. The same correction applies to J5, and to O0 in F1, where "flip together" is neutral, not a kill, whenever the double flip lands on a survivor.
   - **Every F-step needs one more connection that the earlier leak budgets did not count**: the new lock of F(s) (pd2 corollary: F(s) is DL iff F(s) has lock 2′). It is a real coupling. Lemma NL (§4.1) and §4.2 prove two instances: the new lock must cross the previous AB leak, or the old lock, at a vertex of K_F (or outside K_F).
5. **Cleanest instance and its realisation [hand] (§5).** The triple I14 → J10 → B3 costs exactly J10's four leaks, plus the two new locks: by Lemma P, the single leaks of I14 and B3 coincide with J10's two lock leaks. I give an **explicit 22-vertex plane triangulation** (face list in §5.1) in which:
   - the ball has degrees (5,5,6,6,6), there are no ring chords, and I found no separating triangle at the ball;
   - B(s) = I14, s = J10 and F(s) = B3 are all DL, every listed leak and the collar Q are present, and the two new locks exist.

   So **no lemma that uses only the ball, Jordan and the listed leaks of three consecutive Γ_a states can close (5,5,6,6,6).** Caveat: the graph has outside vertices of degree 4, and it is not config-free away from the ball; local + Jordan arguments never read those degrees. F²(s) is not DL in this graph, so the next target is the 5-state stretch D1 … H1 (§6).
6. **[open]** (5,6,6,6,6) and (6,6,6,6,6): automata not derived (§7 gives the recipe and the count setup).

## 1. Pre-redirect: (5,5,6,5,6), the certificate realises five consecutive Γ₁ states [hand]

**Graph and frames.** The graph is the certificate 91a307d1852a1764 with hole 22, and the states are those of MathRstar55656 §1.3. s₋₂ = B(s₋₁) is computed from the listed swaps:
- A = {2,4,12,18,19,21,27}
- B = {1,3,15,16,25,26}
- G = {0,8,10,11,13,17,23}
- D = {5,6,7,9,14,20,24}

F(s) and F²(s) were computed here.

| state | frame (x₀..x₄), roles a,b,g,d | pattern | leak required (MathRstar55656 §3) | witness path (checked edge by edge against the face list) |
|---|---|---|---|---|
| s₋₂ | (14,21,20,25,11); D,A,B,G | N3 = dgdbg@02 (w = 13,15,23,12,3; m₀ = 4, m₂ = 19) | AB: w₃ = 12 ∈ {a,b}-comp of the triple | 12–9–2–6–18–24–19 ({A,D}), and 19 = m₂ is adjacent to x₂ = 20 |
| s₋₁ | (25,11,14,21,20); D,G,A,B | L2 = gdbab@24 | SS: w₂ = 13 ∈ {b,d}-comp of x₁ = 11 | 13–5–0–3–11 ({G,B}) |
| s | (21,20,25,11,14); A,B,G,D | M(O3) = dgdbg@41 | AB: w₃ = 3 ∈ AB-comp | 3–9–26–19–20 ({A,B}) |
| F(s) | (11,14,21,20,25); A,D,B,G | O6 = gdbab@13 (w₀ = 3, m₁ = 4, w₁ = 13, w₂ = 15, m₃ = 19, w₃ = 23, w₄ = 12) | both flanks w₀ = 3 and w₁ = 13 in the {g,d}-comp of x₃x₄ | 20–19–26–9–3 and 13–5–0–3 ({B,G}) |
| F²(s) | (20,25,11,14,21); A,G,D,B | M(L3) = dgdbg@30 | AB: w₃ = 13 ∈ AB-comp | 13–4–0–6–18–24–19–20 ({A,G}) |

Colourings used:
- F(s): A {4,8,10,11,17,21,23}, B {3,5,6,7,20,24,26}, G {0,9,13,18,19,25,27}, D {1,2,12,14,15,16}. Here K_F = all A,G vertices except {0,4,13,21}.
- F²(s): K = {6,10,17,20,21,23,24,26}. A {4,6,8,11,20,24,26}, B {3,5,7,10,17,21,23}.

Every pattern was re-derived from the colours, and each matches the MathTwoSixNeighbours name.

**Consequences.**
- [hand] The realised stretch N3 → L2 → M(O3) → O6 → M(L3) is half of Γ₁. On it, the AB leaks of three R3 states and the SS / two-flank leaks of two R1 states coexist with all ten locks.
- **KILLED:** "a coupling lemma between the AB leak at a dgdbg state and the SS leak at the next gdbab state" for the pairs (N3, L2), (L2, M(O3)), (M(O3), O6) and (O6, M(L3)), and any lemma on this stretch that uses only these leaks plus Jordan.
- Candidate Lemma C (N3 →B M(L2)) survives: the certificate is consistent with it.
- [cert] Independently, r(s) = 5 implies that every radius-≤ 2 kill is blocked on all five states, with no hand check needed.

## 2. (5,5,6,6,6): DL ring patterns and F-transitions [hand]

### 2.1 Frame and rules

- **Link and ring.** Link y₀..y₄ with degrees (5,5,6,6,6). Diamond-free gives deg u₀ ≥ 6; 2.122-free also gives deg u₁, deg u₄ ≥ 6. Neither is used below. In absolute terms the ring is the 8-cycle u₄ u₀ u₁ z₂ u₂ z₃ u₃ z₄, where z_i is the middle of y_i.
- **Frame.** The DL frame is (a,b,a,g,d) on x₀..x₄, with lock 1 {b,g} x₁~x₃ and lock 2 {b,d} x₁~x₄. **T** is the pair of frame positions of the two 5s. F moves T → T+2 and B moves T → T+3. The mirror t ↦ 2−t exchanges T = 01 ↔ 12 and 40 ↔ 23, and fixes 34.
- **Admissible colours.** w₀, w₁ ∈ {g,d}; w₂ ∈ {b,d}; w₃ ∈ {a,b}; w₄ ∈ {b,g}; m₀ ≠ a, m₁ ≠ b, m₂ ≠ a, m₃ ≠ g, m₄ ≠ d; the ring is properly coloured.
- **Conditions imposed.**
  - E1: the outer neighbours of x₁ include both g and d.
  - E2: the outer neighbours of x₃ include b.
  - E3: the outer neighbours of x₄ include b.
  - Not F-starved: x₂ has an outer d. Not B-starved: x₀ has an outer g.
- **F-recipe.** As in MathTwoSixNeighbours §2: an a/g vertex adjacent to x₂ or x₃ is *in* K_F; one adjacent to x₀ is *out*; ring-adjacent a/g vertices share membership; otherwise the vertex is branched. The image is read with w′_t = w_{t+3} and m′_t = m_{t+3}. Colour renaming: an out-vertex goes a→a, b→g, g→d, d→b; an in-vertex goes a→d, g→a.
- **Notation.** w₀..w₄ / (middles in increasing cyclic position starting after T).

### 2.2 Patterns (69)

**T = 01** (middles m₂, m₃, m₄), 16 patterns:
- A1 gdbbb/(g,a,a), A2 (g,a,g), A3 (g,d,a), A4 (g,d,g)
- A5 gddbb/(b,a,a), A6 (b,a,g), A7 (g,a,a), A8 (g,a,g)
- A9 gdbab/(g,d,g)
- A10 gddab/(b,b,g), A11 gddab/(g,b,g)
- B1 dgbbg/(d,a,a), B2 dgbbg/(d,d,a)
- B3 dgdbg/(b,a,a)
- B4 dgbag/(d,d,b)
- B5 dgdag/(b,b,b)

**T = 23** (middles m₄, m₀, m₁), 12 patterns:
- H1 gdbab/(g,d,a)
- H2 gdbag/(b,b,a), H3 gdbag/(b,d,a)
- H4 ddbab/(g,g,g), H5 ddbag/(b,b,g)
- H6 dgdbb/(a,g,a), H7 dgdbb/(g,g,a)
- H8 dgdbg/(a,b,a)
- H9 ggdbb/(a,d,d), H10 ggdbb/(g,d,d)
- H11 ggdbg/(a,b,d), H12 ggdbg/(a,d,d)

**T = 40** (middles m₁, m₂, m₃), 12 patterns:
- D1 gdbab/(a,g,d)
- D2 gddab/(a,b,b), D3 gddab/(a,g,b)
- D4 ggbab/(d,d,d)
- D5 ggdab/(d,b,b)
- D6 dgbbg/(a,d,a), D7 dgbbg/(a,d,d)
- D8 dgdbg/(a,b,a)
- D9 ddbbg/(g,g,a), D10 ddbbg/(g,g,d)
- D11 dddbg/(g,b,a), D12 dddbg/(g,g,a)

**T = 12** (middles m₃, m₄, m₀), 16 patterns:
- I1 gdbbb/(a,a,d), I2 (a,g,d), I3 (d,a,d), I4 (d,g,d)
- I5 gdbbg/(a,a,b), I6 (a,a,d), I7 (d,a,b), I8 (d,a,d)
- I9 gdbab/(d,g,d)
- I10 gdbag/(d,b,b), I11 gdbag/(d,b,d)
- I12 dgdbb/(a,a,g), I13 dgdbb/(a,g,g)
- I14 dgdbg/(a,a,b)
- I15 dgdab/(b,g,g)
- I16 dgdag/(b,b,b)

**T = 34** (middles m₀, m₁, m₂), 13 patterns:
- J1–J4 gddbg/(b,a,b), (b,a,g), (d,a,b), (d,a,g)
- J5 dgdbg/(b,a,b)
- J6 ggdbg/(b,d,b), J7 ggdbg/(d,d,b)
- J8 dddbg/(b,g,b), J9 dddbg/(b,g,g)
- J10 gdbab/(d,a,g)
- J11 dgbab/(g,a,d)
- J12 ggbab/(d,d,d)
- J13 ddbab/(g,g,g)

Notes:
- **AB is never confined.** The triple always has an outer b, or m₁ = a.
- **G is confined only at J10–J13** (T = 34 with w = ·· bab). There G-F and G-B never fire. G swaps J10 ↔ J11 and J12 ↔ J13.
- **F-E1′ / B-E1″** occur only as branch constraints, marked (in)/(out) below: "(in)" means the named middle must join K_F, otherwise F-E1′ kills.

### 2.3 F-transitions

| from T | transitions |
|---|---|
| 01 → 23 | A1(in), A2(out) → H12; A3(in), A4(out) → H11; A5(in), A6(out) → H10; A7(in), A8(out) → H9; A9 → H8; A10 → H7; A11 → H6; B1 → H3; B2 → H2; B3 → H1; B4 → H5; B5 → H4 |
| 23 → 40 | H1 → D8; H2 → D12; H3 → D11; H4 → D6 \| D7; H5 → D9 \| D10; H6(in), H7(out) → D4; H8 → D1; H9(in), H10(out) → D5; H11 → D3; H12 → D2 |
| 40 → 12 | D1 → I14; D2 → I13; D3 → I12; D4 → I16; D5 → I15; D6 → I11; D7 → I10; D8 → I9; D9 → I6 \| I8; D10 → I5 \| I7; D11 → I2 \| I4; D12 → I1 \| I3 |
| 12 → 34 | I1(in), I2(out) → J7; I3(in), I4(out) → J6; I5 → J4; I6 → J3; I7 → J2; I8 → J1; I9 → J5; I10 → J9; I11 → J8; I12(in), I13(out) → J12; I14 → J10; I15 → J11; I16 → J13 |
| 34 → 01 | J1 → A8; J2 → A7; J3 → A6; J4 → A5; J5 → A9; J6 → A11; J7 → A10; J8 → A4 (K_F = {x₂,x₃}); J9 → A3 \| A1; J10 → B3; J11 → B4; J12 → B5; J13 → B1 \| B2 |

Here "|" is a free branch, decided by the outside.

**Γ_a (deterministic, no branch constraint, mirror-closed):**

A9 → H8 → D1 → I14 → J10 → B3 → H1 → D8 → I9 → J5 → A9.

Every Γ_a pattern has a unique F-preimage, which is again in Γ_a. With the mirror symmetry this makes B deterministic on Γ_a too.

**Γ_b** is the remaining 58 patterns plus A2. A2 has no F-preimage, so B(A2) is not DL and r ≤ 2. The G-swaps J10 ↔ J11 and the neutral silent swaps of §3 join Γ_a to Γ_b.

### 2.4 Absolute check of Γ_a [hand]

Start at A9 (k = 0) with:
- y = (A,B,A,G,D);
- (u₀..u₄) = (G,D,B,A,B);
- z₂ = G, z₃ = D, z₄ = G.

I recomputed every F-swap with actual colours:
- The swaps are {A,G}, {A,B}, {A,D}, {A,G}, {A,B}, … . The patterns H8 (k = 3), D1 (k = 1), I14 (k = 4), J10 (k = 2), B3 (k = 0) and H1 (k = 3) all match the table.
- At B3 (k = 0) the roles are b = G, g = D, d = B. So half a turn maps gdbab to dgdbg at the same position, with B→G→D→B.
- **One turn of Γ_a permutes the three non-repeated colours by a 3-cycle**, and the ball returns after 30 F-steps, as for F1's Γ.

## 3. Leaks on Γ_a [hand]

Every silent swap at each state was examined: a two-colour component of a ring vertex that may avoid the link. The kills are SK/SS kills, with the robustness checks of MathOneStarF1 §4 and the corrected hypothesis K_u ∩ N(t) = {u}.

| state | leak(s) that must hold | kill if absent | neutral silent moves |
|---|---|---|---|
| A9 | {w₀,w₁,m₂} ∈ G-comp of x₃x₄ | B-starv after the {g,d} flip | (w₂,{b,d}) → A11; (w₃,{a,b}) → A4 |
| H8 | w₀ ∈ G-comp; {w₃,m₄} ∈ AB-comp of the triple (AB\*) | lock 2 fails; E2 fails | ({w₄,m₀},{b,g}) → H6 |
| D1 | w₀ ∈ G-comp; {w₁,m₂} ∈ G-comp (G-comp = {x₃,x₄,m₃} ∪ outside) | E1 fails; flipping both still B-starves | ({w₂,m₃},{b,d}) → D3 |
| I14 | w₂ ∈ lock-2 comp | F-starv | ({m₃,w₃,m₄},{a,b}) → I16; ({w₄,m₀},{b,g}) → I12 |
| **J10** | w₂ ∈ lock-2; w₄ ∈ lock-1; **collar: m₀, w₀, w₁, m₂ in one {g,d}-component, necessarily link-free** | E2; E3; lock 1 or lock 2 fails at x₁ | G, and the collar flip → J11 |
| B3 | w₄ ∈ lock-1 | B-starv | mirror of I14 |
| H1, D8, I9 | mirrors of D1, H8, A9 | | |
| J5 | AB\*; each of w₀, w₁ either ∈ G-comp or joined to the other in {g,d} | E2; E1 | the double flip → J1 |

Lemma P identifies I14's leak with J10's "w₄ ∈ L1", and J10's "w₂ ∈ L2" with B3's leak. **That leaves 17 distinct leaks per turn.**

**Why the J10 correction holds.** At J10:
- The outer neighbours of x₃ and x₄ are (b,a) and (a,b), so the {g,d}-component of x₃x₄ is exactly {x₃,x₄}.
- The only g/d ring vertices are m₀, w₀, w₁ and m₂.
- Flipping the {g,d}-component of {m₀,w₀} alone leaves x₁ with outer neighbours (d,a,d): lock 1 fails and r ≤ 2. The w₁ side is symmetric.
- Flipping both sides together gives J11, which survives.

So the blocking condition is the collar, not a G-comp leak. The same "joint flip is neutral" check is needed wherever both flanks of a degree-6 x₁ carry {g,d}-leaks. At F1's O0, the note already records that the joint flip B-starves, so it stands.

## 4. What the coupling can and cannot be [hand]

### 4.1 Lemma NL (the new lock crosses the old AB leak)

**Statement.** Let s be DL with F(s) DL. Let R′ be the new lock of F(s): a path from x₄ to x₂ in the {g,d}-subgraph of F(s). Let Q be an {a,b}-path in s from w₃ to a triple vertex t ∈ {x₀, x₁}, meeting the link only at t, and suppose w₃ = b. Then R′ ∩ Q ≠ ∅, and every common vertex is an a-vertex of Q that lies in K_F.

**Proof.**
- C = v x₃ w₃ Q t v is a simple closed curve.
- At v, the edges to x₄ and to x₂ leave on different sides of C, because t ∈ {x₀, x₁} and x₃ lie between them in the rotation. Neither x₄ nor x₂ is on C.
- So R′, which avoids v, meets C. Check each vertex of C in F(s):
  - x₃ is coloured a;
  - w₃ = b;
  - x₀ ∉ K_F, so it stays a; x₁ is b;
  - the b-vertices of Q are unchanged;
  - an a-vertex of Q outside K_F stays a.
- Only an a-vertex of Q inside K_F is coloured g in F(s). ∎

**Use.** In (5,5,6,5,6) at N3 (w₃ = b; the leak runs to m₀, which is adjacent to x₀), K_F must reach into every AB-leak path. This is a genuine coupling, but a *positive* one. The certificate (§1) satisfies it.

### 4.2 The same mechanism at J10

F(s) is DL iff there is a path from w₃ to w₁ whose F(s)-colours alternate g, d. In s-colours its interior uses only d, g∖K_F and a∩K_F. Its first interior vertex must be a d-neighbour of w₃.

Lock 1 runs from w₀ to w₂ in O, so it must share a **g-vertex outside K_F** with this path. Dually, B(s) DL needs a path from w₃ to w₀ that shares a **d-vertex outside K_B** with lock 2.

### 4.3 KILLED: two-state Jordan contradictions in this leak model

Every condition is a positive connection, and every pair of the systems involved shares a colour: L1/L2 share b, L1/Q share g, L2/Q share d, and each new lock shares a colour with each old one. So every forced crossing can happen at a shared vertex. §1 and §5 realise this concretely. A contradiction must use either:
- a **negative** condition (a component that is forced to be confined, such as K_G = {x₃,x₄} at J10), or
- longer chains of states.

### 4.4 Saturation (side remark, [hand])

Call s *saturated* if every bicoloured Tait cycle passes through P. Equivalently, the {a,b}, {g,d}, {b,g} and {b,d} subgraphs are connected, and {a,g} and {a,d} have exactly two components each.
- A saturated state has every leak of the types above.
- The certificate's s is saturated, but F(s) is not: {2,10} is an extra {A,D}-component.
- **J10 can never be saturated**, because G is confined. In a targetless class J10 is therefore the most constrained state: it is the only Γ_a state that needs a link-free component, the collar.

## 5. Explicit realisation of the cleanest instance: I14 → J10 → B3 [hand]

### 5.1 The graph (22 vertices; s = J10)

**Vertices and colours.**
- v, the hole.
- Link: x₀ = a, x₁ = b, x₂ = a, x₃ = g, x₄ = d. Here x₃ and x₄ have degree 5 and x₀, x₁, x₂ have degree 6, so this is T = 34.
- Ring: w₂ = b, w₃ = a, w₄ = b, m₀ = d, w₀ = g, m₁ = a, w₁ = d, m₂ = g.
- Outside: d₁ = d, g₁ = g, y = g, z = d, B₀ = b, b₅ = b, f = g, h = b.

**Faces (40).**
- Ball (18):
  - vx₀x₁, vx₁x₂, vx₂x₃, vx₃x₄, vx₄x₀;
  - x₀x₁w₀, x₁x₂w₁, x₂x₃w₂, x₃x₄w₃, x₄x₀w₄;
  - x₀w₄m₀, x₀m₀w₀, x₁w₀m₁, x₁m₁w₁, x₂w₁m₂, x₂m₂w₂, x₃w₂w₃, x₄w₃w₄.
- Outside (22):
  - w₂w₃d₁, w₂d₁m₂, d₁b₅m₂, d₁yb₅, yw₁b₅, w₁m₂b₅;
  - d₁w₃g₁, w₃w₄g₁;
  - B₀d₁y, B₀yw₁, B₀w₁m₁, B₀m₁w₀, B₀w₀z, B₀zg₁, B₀g₁d₁;
  - w₄g₁z, w₄zf, fzh, zw₀h, hw₀m₀, hm₀f, fm₀w₄.

**Checks.**
- V = 22, E = 60, F = 40. Every edge lies in exactly two faces, and the colouring is proper on all 60 edges.
- There are no ring chords, and I found no separating triangle through a link vertex.
- Degree-4 vertices: m₁, y, b₅, f, h. All are off the ball's link; m₁ is a ring middle.

### 5.2 Components at s (T − v)

| pair | components |
|---|---|
| {a,b} | {x₀,x₁,x₂,m₁,w₂,w₃,w₄,B₀}, {b₅}, {h} |
| {g,d} | K_G = {x₃,x₄}; **Q = {w₀,m₀,f,z,g₁,d₁,m₂,w₁,y}** |
| {a,g} | {x₀,w₀,m₁}; K_F = {x₂,x₃,m₂,w₃,g₁}; {y}; {f} |
| {a,d} | K_B = {x₀,x₄,m₀,w₃,d₁}; {x₂,w₁,m₁}; {z} |
| {b,g} | connected |
| {b,d} | connected |

So:
- Lock 1 holds (x₁ w₀ B₀ y b₅ m₂ w₂ x₃) and lock 2 holds (x₁ w₁ B₀ z w₄ x₄).
- λ₂ (w₂ ∈ L2) and λ₄ (w₄ ∈ L1) hold.
- **The collar Q holds** and is link-free.

### 5.3 The two neighbouring states

**F(s)** swaps a ↔ g on K_F.
- New frame (x₃,x₄,x₀,x₁,x₂), with roles a′ = a, b′ = d, g′ = b, d′ = g.
- The pattern is dgdbg/(b,a,a) = **B3**.
- Lock 1′ is the old lock 2.
- **New lock 2′: x₄ w₃ d₁ y w₁ x₂ in {d,g}.** This is the §4.2 path: d₁ is w₃'s d-neighbour, and y ∈ g∖K_F lies on lock 1.
- B3's leak (w₂ ∈ {b,d}-comp) holds, because {b,d} is connected.

**B(s)** swaps a ↔ d on K_B.
- New frame (x₂,x₃,x₄,x₀,x₁), with roles a″ = a, b″ = g, g″ = d, d″ = b.
- The pattern is dgdbg/(a,a,b) = **I14**.
- Lock 2″ is the old lock 1.
- **New lock 1″: x₃ w₃ g₁ z w₀ x₀ in {g,d}**, with z ∈ d∖K_B on lock 2.
- I14's leak (w₄ ∈ {g,b}-comp) holds.

### 5.4 Conclusion [hand]

All six locks of the three states hold, together with every listed leak of I14, J10 and B3. The leak count is four, or six counting the two new locks.

**KILLED:** any coupling lemma for (5,5,6,6,6) whose hypotheses are the ball, the Γ_a patterns, Jordan, and the listed leaks/locks of at most three consecutive states centred at J10.

Limits of this realisation:
- r(s) ≤ 2 here, by a non-ring kill: the singleton {b₅} flip in {a,b} cuts lock 1. So it is not a radius certificate.
- F²(s) (H1) is not DL: its {g,b}-lock from x₂ to x₀ fails. So the stretch has length exactly 3.
- It is not min-degree-5 and not config-free away from the ball. A lemma that uses those global hypotheses is not killed.

## 6. What remains [open]

- **Next target: the 5-state stretch D1 → I14 → J10 → B3 → H1.** In absolute colours (§2.4):
  - D1 needs u₁ and {u₂,z₃} joined to z₄ in {B,D}_{D1};
  - J10 needs the collar {u₂,z₂,u₃,z₄} in {B,G}_{J10};
  - H1 needs {u₃,z₃} and u₄ joined to z₂ in {G,D}_{H1}.

  The three pairs are the three non-A pairs. The colour not swapped between two of these states is the shared one. Between D1 and J10 only {A,D} and {A,G} are swapped, so B is frozen; between J10 and H1, G is frozen. A coupling lemma, if one exists, should play the J10 confinement (a negative condition) against the D1 and H1 flank connections across the frozen colour.
- In the other direction, a Studio search (below) for a realised D1…H1 stretch would kill this route as well.
- (5,6,6,6,6) and (6,6,6,6,6) are not derived. Setup for (6,6,6,6,6): (w₀,m₁,w₁) has 4 options under E1; (w₂,m₃,w₃,m₄,w₄) has 13 under E2 and E3 (computed in §2's working); then m₂ and m₀ are filtered by F-starv and B-starv. Middles everywhere mean many more branched vertices.

## 7. Studio spec (not run here; one core, minutes)

1. **`leakcoupling_check.py`** (stdlib only, independent).
   - (a) Load the §5.1 face list. Assert that it is a triangulation (E = 3V − 6, every edge in two faces) and that the colouring is proper.
   - (b) Assert the §5.2 component table.
   - (c) Assert that B(s), s and F(s) are DL with patterns I14, J10 and B3, and that F²(s) is not DL.
   - (d) Compute the exact radius of s by BFS (expected 2).
   - (e) Replay the §1 table on the certificate (each path is a list of vertices; assert the edges and colours).
2. **Automaton.** Enumerate the (5,5,6,6,6) patterns per T from the §2.1 rules.
   - Assert the counts 16 / 12 / 12 / 16 / 13 and the §2.3 transitions.
   - Assert that Γ_a is deterministic and that G, AB and starvation never fire on it.
3. **Census.**
   - Inputs: every (5,5,6,6,6) hole in the config-free graphs (diamond- and 2.122-free, orders ≤ 25, plus random larger ones).
   - For every DL state, record the pattern. For Γ_a states, record every §3 leak bit and both new-lock bits.
   - Report the **longest F-run with all leaks present**, and whether any run reaches D1 → H1 (5 states).
   - Expected: the census says r ≤ 3, so runs of ≤ 2 in those graphs.

## 8. Ledger

- **[hand]:**
  - the §1 path checks;
  - the 69-pattern table, the transitions, Γ_a / Γ_b, and the absolute check;
  - the §3 leak table, including the J10 / J5 correction;
  - Lemma NL; §4.2; the saturation remarks;
  - the 22-vertex realisation and all its component computations.
- **[cert]:** r(s) = 5 for the certificate (used only as an independent confirmation in §1).
- **KILLED:**
  - 2–5-state coupling lemmas on the realised stretch of (5,5,6,5,6);
  - ≤ 3-state coupling at I14/J10/B3 in (5,5,6,6,6);
  - two-state Jordan contradictions among positive leaks (§4.3).
- **[open]:**
  - the D1…H1 stretch;
  - Candidate Lemma C;
  - the (5,6,6,6,6) and (6,6,6,6,6) automata;
  - a second reader.
