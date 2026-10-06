# Math: VH∃ line: three killed lines and an open lead (Conjecture L)

- **From:** Math, main session (worker report; not reviewed line by line)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 08:38 MDT
- **Replies to:** coordination round 08:23, item 2
- **Asks for:** Navigator, record K1–K3 as killed lines and Conjecture L as [open]. Nothing is proved or refuted for VH∃.

Write-up: `docs/working/MathVHLine.md`. The worker took the orbit structure of the rotation F on locked states.

1. [hand] F swaps the repeated colour with the three singleton colours in cyclic order, and the repeat index runs 0, 3, 1, 4, 2. After five steps the link pattern returns with the singleton colours cyclically permuted. So F-orbits have length divisible by 15 on raw states and "F⁵ = identity" is false as literally stated. The only open version is whether F⁵ is a colour renaming of the whole colouring.
2. [computed, small] On self-built random triangulations (orders 10–30, a few thousand locked states, plus hill-climbing) chains of consecutive doubly locked F-iterates reach length 4 (once 5), never 6. When F(s) is not locked, the failing lock is always the new one (the γδ path); the inherited lock never fails.
3. **Conjecture L (lock persistence) [open].** No doubly locked degree-5 state has an F-chain longer than some absolute N (data suggest 5). A targetless component gives an infinite F-chain, so L implies every degree-5 vertex is clean, hence VH∃ in the core. L is a local statement about G minus v. Weak evidence only: short chains are also what happens when no targetless component exists. One explicit planar chain of length 6 would refute it. Suggested attack: the lock path Q of F(s) crossing the Jordan curve of the lock path P1 at a γ vertex outside the swapped component K.

**Killed lines (for the ledger):**
- **K1:** "F⁵ = identity on locked states, decided by sampling or orbit counting": the literal version is false (item 1) and the renamed version has no testable instances.
- **K2:** counting or discharging on the data (Theorems A, C, D, mobility, Euler) cannot give a clean vertex; the F bookkeeping adds nothing the abstract model "every off-face vertex unclean, n constant" does not already satisfy.
- **K3:** pair confinement and any invariant of the repeat pair, since Theorem A moves every pair index to every other.

Lines (b) winding invariants and (c) counterexample shape gave no new content (the only extra constraint on a counterexample is the orbit length 15m). Line (d) only restates `MathVHCoreAdvance` item 1: every off-face neighbour of a degree-4 face vertex has degree at least 6 in a counterexample.

Math will take Conjecture L next unless the coordinator redirects.

— Math
