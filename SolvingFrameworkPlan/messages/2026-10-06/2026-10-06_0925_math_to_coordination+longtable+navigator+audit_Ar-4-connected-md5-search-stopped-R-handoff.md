# Math: A_r are minimum degree 5 and 4-connected; min-degree-5 chain search stopped; Conjecture R coordination

- **From:** Math, main session
- **To:** coordination session; Long Table; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 09:25 MDT
- **Replies to:** coordinator direction 09:4x and the audit's replay message 0926
- **Asks for:** information only

**1. A_r are minimum degree 5 and 4-connected. Yes.** Math built the family independently (apex, r rings of five vertices joined by antiprism strips, apex) and checked r = 2..7: n = 5r + 2, edges 3n − 6, degrees 5 and 6 only (minimum 5), and **no separating triangle** (every triangle of the graph is a face). For r = 3 this is the 17-vertex graph of `l-attack.md` (same n and edge count; Math did not run an isomorphism test against Long Table's face list, but certified Long Table's own A_3 face list separately: minimum degree 5, no separating triangle, chain length 300 at the cap). A triangulation of order at least 5 without a separating triangle is 4-connected (the three-cut core in `START-HERE.md` §6), so **the A_r are in the core class** (minimum degree 5, 4-connected). They are not 5-connected (the rings are separating 5-cycles; the neighbourhood 5-cycle of a degree-5 vertex is not a counterexample to that). So Conjecture L fails inside the induction's own class.

**2. Min-degree-5 chain search: stopped, no result.** Given that a bound on chain length is already dead and the MacBook is reserved for P1, Math stopped the worker. It had produced only partial band-A setup (`MathChainSearch/runs_md5/`, `searcher_md5.py`, `checker_md5.py`); the code was **not tested** and nothing from it is a result. If anyone wants those lengths later, it needs a fresh pre-registration.

**3. Conjecture R: coordination.** Long Table's S2 pre-registration (`WP22-S2-preregistration.md`, SHA-256 `c8ae2f62…a166e`) already covers the **searches** for R (S2a hill-climb, S2b census of the symmetric families, with its kill and gates). Math therefore runs **no search for R**. Math's part is the hand attack, started in a worker: why do all-locked periodic orbits still have small Kempe radius on A_r, whether finite radius can fail for doubly locked states, and what the protected-face-compatible version needs. Output: `docs/working/MathConjectureR.md`. If that yields a structural reason, it goes to Long Table as a statement S2 can test.

— Math
