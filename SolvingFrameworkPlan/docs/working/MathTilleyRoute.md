# Targetless components and Tilley's Kempe-locking: a route test

Math research worker, 6 October 2026. Hand work plus a small exact Python check on explicit graphs (A_3, A_4, A_5, T4, the two `lt_certs`), about 3 CPU-seconds in total. No census, no declared experiment, no status change, nothing committed, no other file edited. Scripts are in the session scratchpad (`tilley.py`, `tilley2.py`), not committed. Labels: [hand], [cited], [computed], [open].

## Verdict, first

The route **reproduces known facts**; it gives no new path to VH∃ or to 4CT.

1. A targetless component C at a degree-5 vertex v forces **class-level** Tilley locks at all five edges v x_i [hand, §2]. The proof uses only the Tilley bridge (accepted by Math at 20:42) and an identity: "doubly locked" is the same as "first-order Tilley-locked at all three singleton edges". This is the SEP/D1 picture of `tilley-separability.md` §7 and §11, stated per component. It is not new.
2. It does **not** force Tilley's **whole-edge** Kempe-locking [hand, §3]. Tilley's definition quantifies over every colouring of T − v x_i with c(v) = c(x_i), not only those that come from C. On a 4-colourable T, every degree-5 vertex has at least one incident edge that is not Kempe-locked.
3. The chain "minimum counterexample ⇒ Kempe-locked at every edge ⇒ Birkhoff diamond ⇒ reducible, contradiction" is **Tilley's own observation** [cited]. It never uses targetless components or VH∃. Its only open link is Tilley's conjecture, which by itself already implies 4CT [§4].
4. [computed, §5] The infinite all-DL F-orbits of A_r are **not** Tilley-locked: on A_3, A_4 and A_5, not one DL state lies in a locked Tilley class at any of its singleton edges. T4 has locked Tilley classes (at 18 edges, each with an endpoint of degree 5, four of them with both endpoints of degree 5), but no whole-edge lock. No edge of A_3, T4 or W6 is Kempe-locked in Tilley's sense.

## 1. Definitions used

**Tilley [cited; verified].** Source: arXiv:1809.02807, HTML version, read on 6 Oct 2026 by targeted extraction (WebFetch). Quoted: "T is said to be Kempe-locked with respect to the edge xy if, in every 4-coloring of G_xy in which the colors of x and y are the same, there are precisely three Kempe chains that include both x and y". Here G_xy = T − xy. This matches `literature-check.md` line 75.
- Theorem (Tilley): "A minimum counterexample to the 4-color conjecture must be Kempe-locked with respect to each of its edges."
- Conjecture (Tilley): "The existence of a Birkhoff diamond configuration with endpoints x and y in a planar triangulation T with an edge xy is a necessary, but not sufficient, condition for T to be Kempe-locked." Tilley adds that if this holds, "the 4-color theorem would follow trivially".
- Also in the paper (per the extraction, not read line by line): "The degrees of x and y in an edge xy that is Kempe-locked by a Birkhoff diamond must be at least 6." I did not check whether this is proved there or observed.

**Class-level lock (ours).** For a colouring c of G_xy with c(x) = c(y), its Tilley class is its Kempe class in G_xy. The class is *locked* if every member keeps c(x) = c(y).

[hand] A class is locked exactly when every member is first-order locked (all three chains {c(x),k} through x contain y). If some member is not, swapping that chain separates x and y. If every member is, then every Kempe change either avoids both x and y or swaps both. So "T is Kempe-locked at xy" is the same as "every Tilley class at xy is locked".

**Ours (from MathConfinementAttack and MathCleanVertexAttack).** States are proper 4-colourings of T − v. Moves are whole-component swaps and singleton slides. A targetless component is a move-component with no filled state. A state is DL (doubly locked) if both Step 1 locks hold.

## 2. Targetless ⇒ class-level locks at every edge v x_i [hand]

Set-up: v has degree 5 with link x_0..x_4, and s is an unfilled state with word (α,β,α,γ,δ) (repeat index j = 0, singletons x_1, x_3, x_4). For a singleton x_i, let s^i be s with v coloured c(x_i). It is a proper colouring of G_i = T − v x_i with c(v) = c(x_i).

**Lemma 1 (identity).** s^1 is first-order locked iff both locks hold: P1, a βγ path x_1~x_3, and P2, a βδ path x_1~x_4, both in T − v. s^3 is first-order locked iff P1 holds. s^4 is first-order locked iff P2 holds. Hence **s is DL iff s^1, s^3 and s^4 are all first-order locked.**

Proof. In G_1, colour v with β. The {β,α} chain of v contains x_1 through the edge x_0x_1 (x_0 is α and adjacent to v). The {β,γ} chain contains x_1 iff the chain of x_3 reaches x_1. Its only other route from v is through x_3, the unique γ link vertex. That is P1, and a path through v is useless because v is the β end. The {β,δ} chain is the same with P2. For s^3 (v coloured γ), the {γ,α} chain contains x_3 through v x_2 x_3. The {γ,δ} chain contains x_3 through v x_4 x_3. The {γ,β} chain needs P1. s^4 is symmetric, using P2. ∎ (This is the "first-order lock" item of `tilley-separability.md` §11, written per state.)

**Proposition 2.** Let C be a targetless component, and let s be in C with its hole at v. Then for each singleton x_i of s, the Tilley class of s^i in G_i is locked. By Theorem A, all five repeat indices occur in C at v, and each x_i is a singleton for three of them. So **each of the five edges v x_i carries at least one locked Tilley class**, made of colourings that restrict to states of C.

Proof. Suppose a Tilley sequence separated v from x_i. By the bridge (`tilley-separability.md` §1, accepted by Math at 20:42), it becomes a sequence of pure swaps at the hole v that ends in a filled state. Swaps are moves, so that filled state would lie in C. This contradicts targetlessness. ∎

This is SEP failing at every state of C, and at every state one swap away from it. So it is the known implication "D1 ⇒ no targetless component at a degree-5 vertex". **Not new.**

## 3. Targetless does not force Tilley's whole-edge lock [hand]

(a) **The quantifier is different.** A whole-edge lock at v x_i constrains every colouring of G_i with c(v) = c(x_i). Their restrictions to T − v are either unfilled states with x_i as a singleton, in any component, or filled states whose link has x_i as its singleton. Proposition 2 constrains only those in C.

(b) **Lemma 3.** If T is 4-colourable and deg v = 5, then some edge v x_j is not Kempe-locked.

Proof. Take a proper colouring c of T. The link 5-cycle uses exactly 3 colours, avoiding c(v), in the pattern (2,2,1), with singleton x_j. Recolour v to c(x_j). This is proper on G_j, since x_j was the only neighbour of v with that colour. The {c(x_j), old c(v)} chain of v in G_j is {v}, because no other neighbour of v has either colour. Swapping it separates v from x_j. ∎

So in any 4-colourable T, which every T we would test is (only a 4CT counterexample is not), no degree-5 vertex has all five edges Kempe-locked, whatever the targetless structure. A VH∃ failure T that is 4-colourable is outside the scope of Tilley's theorem and Tilley's conjecture, both of which concern whole-edge locks.

(c) **If T is not 4-colourable** (a minimum 4CT counterexample), every state at every hole is targetless, because a filled state anywhere gives a colouring of T. Every edge is also Kempe-locked (Tilley). Both are restatements of non-colourability, so the implication "targetless ⇒ locked" holds but carries no information.

## 4. The chain of implications

Route as posed: (VH∃-failure or 4CT-counterexample) ⇒ targetless at v ⇒ Tilley-locked at v x_i ⇒ Birkhoff diamond ⇒ reducible ⇒ contradiction.

| # | Link | Status |
|---|---|---|
| L0 | T a minimum counterexample to 4CT ⇒ every state at every degree-5 hole is targetless | [hand], trivial (§3c) |
| L1 | T a minimum counterexample ⇒ Kempe-locked at every edge | [cited] Tilley; also [hand] in one line: colour T/xy by minimality and uncontract; a separating chain would colour T. **Does not use L0.** |
| L1' | targetless component C at degree-5 v (T 4-colourable) ⇒ class-level locks at all five edges v x_i | [hand] §2 |
| L1'' | targetless at v ⇒ whole-edge lock at v x_i (T 4-colourable) | **false in general for some i** (Lemma 3); for the remaining i, [open] and not implied by §2 |
| L2 | Kempe-locked at xy ⇒ Birkhoff diamond with endpoints x, y | **[open]**: Tilley's conjecture. Search evidence [cited]: all 4-connected triangulations of orders 6–17, random samples at 18–20, all 5-connected triangulations of orders 12–24 |
| L2' | a single locked class at xy ⇒ Birkhoff diamond K_xy | [open], strictly stronger than L2, and not what Tilley tested. Tension [computed + cited, unverified]: T4 has class-locked edges with both endpoints of degree 5, while Tilley reports degree ≥ 6 at the ends of a diamond-locked edge |
| L3 | the Birkhoff diamond is reducible | [cited] Birkhoff 1913; it is also D-reducible (`literature-check.md`) |
| L4 | L1 + L2 + L3 ⇒ 4CT | [hand], given L2; Tilley says so himself ("would follow trivially") |

**Reading.**
- On the counterexample side, the route is L1 + L2 + L3. Targetless components play no role, and the whole weight sits on Tilley's conjecture, which implies 4CT by itself. So the route only **reproduces the known implication "Tilley's conjecture ⇒ 4CT"**.
- On the VH∃ side (T 4-colourable), we get only L1', and Tilley's results do not apply. To close it we would need both L2', which is stronger than Tilley's conjecture and in tension with the T4 data, and a new lemma: "a Birkhoff diamond at v x_i gives a VH-good pair". Reducibility is a statement about extending colourings in a minimum non-colourable T, so it does not refute a 4-colourable VH∃ failure. [open; no route seen]

## 5. Computation [computed]

Scripts: `tilley.py`, `tilley2.py` (session scratchpad). Exact enumeration of all canonical proper 4-colourings of T − v. For each singleton edge v x_i, BFS over Kempe changes in G_i = T − v x_i with v coloured, to decide whether the class is locked. Graphs: A_r built as a centre, r rings of 5 and a far centre ((k,t) ~ (k+1,t), (k+1,t−1)), giving A_3 identical in counts to `lt_certs/A3.json`; T4 from the face list in `MathConjectureR.md`; `lt_certs/W6.json`. Sanity: state, filled and DL counts reproduce `MathConjectureR.md` (A_3 100/40/30, A_4 520/200/80, A_5 2720/1040/530, T4 68/22/21). The assertion "DL ⇒ first-order locked at the singleton edges" (Lemma 1, one direction) held on every DL state.

| Graph, hole | DL states | (DL state, singleton edge) pairs | in a locked Tilley class | whole-edge locks at v |
|---|---|---|---|---|
| A_3, centre | 30 | 90 | 0 | none |
| A_4, centre | 80 | 240 | 0 | none |
| A_5, centre | 530 | 1590 | 0 | none |
| T4, v = 4 | 21 | 63 | 12 (6 at edge 4–0, 6 at edge 4–9; one class each, size 6; T − v colour classes 4,4,4,4) | none |
| lt_cert A3, v = 0 | 30 | 90 | 0 | none |
| lt_cert W6, v = 12 | 17 | 51 | 0 | none |

All-edge scan (every edge xy, every colouring of G_xy with c(x) = c(y)):
- A_3: 45 edges, 0 whole-edge locks, 0 locked classes.
- W6: 54 edges, 0 whole-edge locks, 0 locked classes.
- T4: 45 edges, 0 whole-edge locks, and 18 edges with at least one locked class. Their degree pairs are (5,6) on 14 edges and (5,5) on 4.

Readings, with no universal content:
- (i) The A_r infinite F-orbits stay DL, which is first-order locking at every step, yet every one of their Tilley classes is unlocked. So DL along an orbit is strictly weaker than a Tilley class lock. This agrees with the A_r fills using swaps outside F/B (`MathConjectureR.md`, K2).
- (ii) T4 shows locked Tilley classes with no targetless component: every T4 state fills within 4 moves. So class-level locks are not even sufficient for targetlessness, as expected from the bridge being one-way.
- (iii) The equitable 4,4,4,4 pattern of the order-17 locks (`tilley-separability.md` §8) recurs on T4. This is post hoc.
- (iv) No targetless component exists on any of these graphs, so the implication in (1) cannot be tested directly. Only its local signatures (DL, class locks) can.

## 6. Claim ledger

- [hand]: the class-lock ⇔ first-order equivalence (§1), Lemma 1, Proposition 2, Lemma 3, §3c, the chain table (§4).
- [cited]: Tilley's definition, theorem, conjecture and degree remark (arXiv:1809.02807, extraction only); Birkhoff's reducibility.
- [computed]: §5, exact on the six listed holes and the three all-edge scans.
- [open]: L2 (Tilley's conjecture), L2', "Birkhoff diamond ⇒ VH-good pair", and VH∃.
- Candid summary: the route restates SEP/D1 on the VH∃ side, and restates "Tilley's conjecture ⇒ 4CT" on the counterexample side. It gives no new reduction.
