# NightCutParity — odd-window cut parity and 20 ∣ L [exploratory]

2026-10-07. Inputs: NightGammaLength.md, NightLog-2026-10-06 (Jobs AN, AO, AS, AT), the tables `xTab/wTab/mTab` of QuarterWindow.lean, `jobuv/jobat-summary.txt`, the constructed cycles `jobas/best-A7f*.json`.
Script: `backgroundMaterial/.../27-studio-positive-config/jobuv/nightcutparity.py`, output `nightcutparity-output.txt` (about 7 s, 1 core, on AC).
The census inputs (`in-plantri-*.txt`) are not in this checkout. So the data checks in §4 use the 26 constructed cycles (160 periods) only. The census check is a Studio job (§6).

Scope: all-DL orbits at a `Hole6`, with the period-10 tables of QuarterWindow. These are the (5,5,5,5,6) holes, with p = x_q of degree 6 and one middle neighbour m.

## 0. The proposed derivation is wrong at step (3)

The brief argued that "a vertex's colour changes over a period ⇔ it is swapped an odd number of times", so S_b would be the set of non-α vertices.

**This is false.** A vertex swapped by {α,A} and then by {A,B}… can change colour after two swaps. The ring shows the failure directly:
- every non-α ring vertex changes colour over a period (σ moves it);
- yet every ring edge is cut 4 times, and S_b ∩ ring = ∅ (160/160).

If S_b were the non-α class, the ring edges joining an α vertex to a non-α vertex would be cut an odd number of times. The table says they are cut 4 times.

What holds instead is the following.

## 1. Every swap is an {ω, ·} swap [proved, table computation]

From the tables (rows 0–9, with row 10 = σ(row 0)), each step changes the colours of some ring vertices. All of these changes use **the same pair**, and that pair **always contains α**. The pairs are:

| step | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| pair | αA | αμ | αB | αA | αμ | αB | αA | αμ | αB | αA |

(These are letters of the anchoring R3k4 state.)

Since σ fixes α, the absolute colour ω := α is the same in every period. **Every step of an all-DL orbit is a Kempe swap of {ω, X} for some X.** Data: 26/26 cycles. Every swapped pair shares one colour, and that colour is c(x_j) of the frame.

## 2. Exact form of D_b [proved]

Let A_b be the ω-class at the start of period b, and let n_v be the number of the period's 10 components that contain v.

A swap of {ω, X} on K moves each v ∈ K into or out of the ω-class. Hence **n_v is odd ⇔ v changes ω-membership**, so

  S_b := {v : n_v odd} = A_b △ A_{b+1}, and D_b = ∂(A_b △ A_{b+1}).

Here an edge is cut ⇔ [u∈K] + [v∈K] = 1, so the cut parity of uv over the period is [u∈S_b] + [v∈S_b].

Two facts about T − h: it is connected, and it contains a triangle. Two disjoint independent sets cannot cover a graph with a triangle. So for X ⊆ V(T−h), ∂X = ∅ ⇔ X ∈ {∅, V}, and A △ A′ = V is impossible. Consequences:

- **Odd-window XOR.** The XOR of D over periods b, …, b+k−1 is ∂(A_b △ A_{b+k}). It is **empty ⇔ A_{b+k} = A_b**. So "the odd-window XOR is never empty" is exactly "**the ω-class at period starts never recurs at odd distance**". The brief's step (4) ("S_b is constant") is false. S_b is constant only when A has period 2.
- **Even-cut lemma, one-line proof (at Hole6).** Closure gives c_L = σ^m c_0, and σ fixes ω, so A_m = A_0. The total cut parity is therefore ∂(A_0 △ A_m) = ∅.
- **"D_b identical in all periods" ⇔ A_{b+2} = A_b** (the ω-class has period 2). This held in 2,548/2,728 census cycles. On the constructions it happens only in the L = 40 cycles of A7f1, where the A-period is q = 2 < m = 4.
- **The ring is never in S_b**: this is the table fact that ring edges are cut an even number of times (4).
- **Uniqueness fails, so this is not circular.** Fix A_b and the ring colours. The 3-colouring of V ∖ A_b is not unique: there are 1–24 extensions (scratch count). So "A never recurs at odd distance" is genuinely stronger than "m is even". It is a statement about the ω-class alone.

## 3. A vertex whose ω-membership flips every period [reduction proved; one Kempe fact open]

Let **u\*** be the apex of the face outside the ring on the ring edge w3–y. Here y = w_{q+4}, and u\* ≠ x4. Minimum degree 5 gives u\* ∉ ring, since u\* ≠ w2 and u\* ≠ m.

**If u\* ∈ S_b for every b, then 20 ∣ L.** Proof: u\*'s ω-membership flips every period. A_m = A_0 (by §2), so m is even and L = 10m ≡ 0 (mod 20). The same fact gives u\* ∈ A_b △ A_{b+k} for every odd k, so the odd-window XOR is never empty and always contains the two edges u\*w3 and u\*y.

**Reduction (proved).** Let δ = [c(u\*) = c(x4)]. Note that x4 and u\* are the two apexes on either side of the edge w3y, and both are adjacent to w3 and y. Go through the period step by step with pair P:

- **P = {c(w3), c(y)}:** neither x4 nor u\* is swapped. δ is unchanged.
- **P contains exactly one of c(w3), c(y), say c(w3):** each of x4 and u\* that has the other letter of P lies in w3's component. So each one is swapped ⇔ w3 is swapped. δ is unchanged in both cases (δ = 1, and δ = 0).
- **P = the complement of {c(w3), c(y)} ("free"):** both x4 and u\* carry letters of P. δ flips ⇔ exactly one of them is swapped.

The table gives two facts:
- the free steps are exactly **steps 0 and 7**, and x4 is swapped at both;
- at period start ω ∉ {c(w3), c(y)} = {B, μ}, so ω ∈ {c(x4), c(u\*)}. Exactly one of these holds: u\* ∈ A_b, or δ_b = 1. Hence the flip of u\*'s ω-membership is the flip of δ.

Hence

  **u\* ∈ S_b ⇔ δ_{b+1} ≠ δ_b ⇔ exactly one of K_0, K_7 contains u\*.**

**Gap (one Kempe-chain statement).** In each period, u\* lies in exactly one of the following two components:
- K_0 = the {α,A}-component of x4 at step 0 (it contains x3 and w2);
- K_7 = the {α,μ}-component of x4 at step 7 (it contains p and z).

In the data, at step 0 (row-0 letters: x4 = A, w3 = B, y = μ, u\* ∈ {α, A}):
- u\* ∈ K_0 ⇔ u\* = α (δ = 0).

At step 7, after steps 1–6 have forced everything locally:
- u\* = μ and x4 = α in both cases;
- u\* ∈ K_7 ⇔ u\* ∉ K_0.

So the alternation is **global**: whether u\* rode with x4's chain at step 0 decides whether it is chained to x4 at step 7.

**Lead.** At step 0 the two DL locks are the {μ,A} chain x2 ~ x4 and the {μ,B} chain x2 ~ p. Both must enter through y:
- the only μ/A neighbour of x4 other than h is y;
- the only μ/B neighbour of p is y.

So the closed curves h–x2⋯y–x4–h and h–x2⋯y–p–h both pass through y. Where they leave y, relative to w3 and u\* in y's rotation, decides on which side u\* lies. That is the natural Jordan-curve route to (i) at step 0 and (ii) at step 7.

## 4. Data [constructions only]

From `nightcutparity-output.txt`: 26 all-DL Γ-cycles from A7 plus flips (L = 80: 14, L = 40: 12), both orientations, 160 periods.

| check | result |
|---|---|
| every swapped pair contains ω | 26/26 |
| S_b = A_b △ A_{b+1} | 160/160 |
| S_b ∩ ring = ∅ | 160/160 |
| no odd-distance recurrence of A | 26/26 |
| u\* ∈ S_b | 160/160 |
| u\* swapped exactly 3 times per period | 160/160 |
| exactly one of K_0, K_7 contains u\* | 160/160 |

The two patterns appear 80 times each:
- δ_b = 1: u\* ∉ K_0, u\* ∈ K_7;
- δ_b = 0: u\* ∈ K_0, u\* ∉ K_7.

Consistency with Job AT: u\*w3 and u\*y lie in every D_b, so |D_b| ≥ 2. The observed minimum is 8.

## 5. Status

| statement | status |
|---|---|
| every all-DL step at a Hole6 is an {ω,·} swap, ω = α fixed by σ | **proved** (tables) |
| D_b = ∂(A_b △ A_{b+1}); odd-window XOR empty ⇔ A_{b+k} = A_b | **proved** |
| even-cut lemma at Hole6 (one-line proof via A_m = A_0) | **proved** |
| "S_b = the non-α class" (the brief's step 3–4) | **false** (ring ∩ S_b = ∅; the ring edges would be cut an odd number of times) |
| u\* flips ω-membership each period ⇔ exactly one of K_0, K_7 contains u\* | **proved** (table and adjacency) |
| **exactly one of K_0, K_7 contains u\*** ⇒ 20 ∣ L and the odd-window XOR is never empty | implication **proved**; the premise is **open** (160/160 periods) |

## 6. Next

- **Studio job.** Rerun `nightcutparity.py` Part 2 on the census (orders 25–27) at (5,5,5,5,6) holes. Also test whether some fixed vertex lies in every S_b at the other patterns, where the tables differ.
- **Proof.** Prove the K_0/K_7 alternation by the Jordan argument with the lock chains through y (§3). That is a finite case analysis on y's rotation, and once done, 20 ∣ L becomes a theorem at Hole6.
