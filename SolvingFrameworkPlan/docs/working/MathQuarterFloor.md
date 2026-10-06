# The quarter floor: every Kempe class of T − v is at least 1/4 filled?

Math lead, 6 October 2026. Hand only, written in about an hour. **Verdict up front: no proof, and I do not yet see why.** Below are: an exact local model that produces a natural factor 4; two candidate counting mechanisms, neither proved; and the data that would decide between them.

Notation. A state is a colouring of T − v up to renaming. It is **filled** when the link uses at most 3 colours. The data (local intel, c24d895; unreviewed) say that every class has filled fraction ≥ 1/4, with equality exactly at class sizes 4, 48, 288, 4224 and 7776.

## 1. The exact local model at the hole (Tait dual) [hand]

Colours are in Z₂², and dual edges are coloured by c(u) + c(w) (Tait). Let P be the pentagon node of the dual of T − v.
- **P's word.** P's five edge colours are nonzero and sum to 0, so their multiplicities are **(3,1,1)**: one majority colour c₁ and two singletons c₂, c₃. (Multiplicities (2,2,1) or (4,1) give a nonzero sum.)
- **Filled in the dual.** **Filled ⇔ the two singleton edges are adjacent** around P. This agrees with the dictionary in `MathTaitGlobal.md`.
- **Count.** Up to renaming (the S₃ action on {c₁, c₂, c₃}), a word is just the position pair of the singletons. There are 5 adjacent pairs (filled) and 5 non-adjacent pairs (unfilled), 10 in all. This matches the audit's count of 10 link orbits.
- **Kempe moves at P.** A Kempe swap switches one bichromatic path or cycle of the dual. Switches **through P** are the only moves that change P's word:
  - **Pair {c₂, c₃} (the singletons).** P has degree 2 in this subgraph, so there is one P-to-P path joining the two singleton edges. Switching it exchanges their colours, and the **positions are unchanged**, so filled status is unchanged.
  - **Pair {c₁, c₂}.** P has degree 4 (three c₁ edges and the c₂ edge). Its two P-to-P paths form one of the **two non-crossing matchings** of those 4 edge positions in cyclic order. Switching the path through the c₂ edge **moves that singleton** to its partner's position. Switching the other path, which joins two c₁ edges, makes c₂ the majority; the **new singletons are the remaining c₁ edge and the c₃ edge**.
  - **Pair {c₁, c₃}:** the same, with the other non-crossing matching choice.
- **Local type of a state.** A state's local type is (word, M₂, M₃), where M₂ and M₃ ∈ {2 choices} are the non-crossing matchings of the {c₁, c₂}- and {c₁, c₃}-paths at P. That gives **2 × 2 = 4 matching combinations per word.**
- **Moves away from P.** Switching cycles or paths that avoid P leaves the word fixed, but can change M₂ and M₃ by rerouting paths.

**The factor 4.** It is natural here: for each word there are exactly **four** (M₂, M₃) combinations. Exact equality at 1/4, at sizes all divisible by 4, suggests that classes at the floor are unions of "blocks" of four states, each containing exactly one filled state.

## 2. Candidate mechanisms (neither proved)

**(A) Matching blocks.** Conjecture: for every unfilled state s, there is a filled state f(s) in the same class, obtained by a short sequence of P-switches, such that **each filled state is reached from at most three unfilled states**. The heuristic: for a fixed outside structure, the 4 combinations of (M₂, M₃) at a word give 4 different local futures, and at least one of them leads to an adjacent-singleton word within the class.
- **Problem:** doubly locked states are ≥ 2 swaps from a fill, and the move from a word to an adjacent-singleton word depends on M₂ and M₃. I could not make "at most 3-to-1" rigorous: different unfilled states can route to the same filled state through different paths.

**(B) Fan admission.** Each unfilled state has exactly 3 singleton positions, so it is admitted by 3 fans, i.e. it is a colouring of three different triangulations T\*_τ. Each filled state has exactly **1** singleton, so it is admitted by 1 fan. So Σ_τ |S ∩ col(T\*_τ)| = 3U + F, where U and F are the class's unfilled and filled counts.
- A class-wise inequality U ≤ 3F would follow from a relation such as "per fan, the admitted states of S are at least as many filled as unfilled". **I see no reason for that**, and the audit's quantifier trap warns that counting alone does not see Kempe classes. Recorded as a lead only.

## 3. The size-4 classes (1 filled, 2 non-DL, 1 DL)

A filled state f, two unfilled states that are **not** doubly locked (each fills in one swap, necessarily into f), and one doubly locked state d (two swaps from f). By Math's one-filled-state note (corrected by intern C, 37af166), every bichromatic component of T − v meets the link in f.
- **Under (A):** the block is {f, n₁, n₂, d}: one word with its four (M₂, M₃) combinations, one of which is filled. This is consistent with the counts (1 + 2 + 1).
- **Under (B):** the fan count is 3·3 + 1 = 10, and no inequality is visible.
- **The decisive check:** do the four states of a size-4 class have the **same outside structure** (the same bichromatic cycles away from P) and differ **only** in P's matching combination and word? If yes, (A) is the mechanism.

## 4. Identity or artefact?

- **For an identity.** The floor is hit **exactly**, at sizes 4, 48, 288, 4224 and 7776, all divisible by 4. (7776 = 6⁵, which suggests a product structure over the five link edges.) It is never beaten over 111,478 graphs. Exact attainment with structured sizes looks like a combinatorial identity (a block decomposition) rather than chance.
- **For caution.** These are small orders and core graphs only. If the floor is a theorem, it **implies R\*** at every degree-5 vertex of every triangulation, and so **implies the Four Colour Theorem** by the minimal-counterexample frame. A short counting proof of it would therefore be a short proof of 4CT. That makes "artefact of small graphs" a priori more likely than "simple identity". At minimum the floor will not follow from local counting alone, because the outside structure enters through M₂ and M₃.

## 5. Checks that would decide it (local compute, through the coordinator)

1. **Block test.** For every class at exactly 1/4, group states by their "outside structure": the set of bichromatic cycles and paths not through P, i.e. the colouring outside the 1-ball up to the P-switches. Are the classes unions of blocks of four that agree outside P and differ in (word, M₂, M₃)? Does each block contain exactly one filled state?
2. **Fan test.** For each class, compute the admitted counts per fan, and test whether "per fan, filled ≥ unfilled/3" holds.
3. **Scale test.** Look for any class with filled fraction < 1/4 at larger orders and on configuration-free graphs (fullerene duals). By the remark in §4, a single violation is far more likely than a theorem.
