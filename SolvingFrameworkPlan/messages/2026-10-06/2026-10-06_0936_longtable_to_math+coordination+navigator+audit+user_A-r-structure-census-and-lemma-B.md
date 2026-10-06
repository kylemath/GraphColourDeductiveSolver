# The structure of A_r: an exact reduction, a census to r = 8, a conjectured walk structure; no proof for all r

- **From:** Long Table (Creative Intel), main session (report of the A-Structure team; its census numbers cross-checked against the audit's)
- **To:** Math; the coordination session; Navigator; Audit; the user
- **Sent:** 2026-10-06 09:36 MDT
- **Replies to:** `2026-10-06_0924_math_…_conjecture-R.md` ("the A_r structure is yours to prove")
- **Asks for:** Math, a look at Lemma B and the walk description (Conjecture J) when convenient. **The all-$r$ statement is not proved.**

Report `docs/working/creative-intel-2026-10-05/a-structure.md`; scripts `explore-vhphi/astruct_*.py` (own definitions, at most one process, longest run 95 s).

1. **[hand] Lemma A.** $F$ and the double-lock test commute with the 5-fold rotation of $A_r$ and with colour renamings.
2. **[hand] Lemma B (exact reduction).** If $s,Fs,F^2s,F^3s$ are doubly locked and $F^4s=\pi\circ s\circ\sigma$ ($\sigma$ = rotation by 3 positions, $\pi$ a colour permutation), then the chain is infinite. So an infinite chain on $A_r$ needs only four lock checks and one equality, for one explicit colouring.
3. **[computed] Census, all colourings, $r=3..8$** (orders 17 to 42): 20, 20, 60, 100, 220, 420 classes $=20\,J_{r-2}$ (Jacobsthal numbers). All have period 20 up to renaming; the raw period 60 of the $A_3$ witness is $3\times20$ because $F^4s=\pi s\sigma$ with $\pi$ a 3-cycle in every solution. **Cross-check:** the audit's independent census (120, 120, 360 colourings of $A_3,A_4,A_5$ with the colour of $x_0$ fixed) equals 20, 20, 60 classes times the 6 renamings, as it should. Orders 37 and 42 ($r=7,8$) and $r=6$ are not independently checked.
4. **[hand + computed] $r=2$ (icosahedron):** no state has even the first lock, because the cap forces ring 1 to use at most 3 colours (all 60 states checked).
5. **[computed] Walk structure and [conjecture J].** From depth 2 each ring has 3 admissible colourings, each with 2 successors: a walk on a triangle $K_3$. The solutions equal all paths of the layered graph for $r=4..8$; walks between distinct $K_3$ vertices number $J_{r-2}$, which would give existence for every $r\ge3$ and $J_0=0$ at $r=2$. **Conjecture J:** the description holds for all $r$. Missing: a uniform proof that the Kempe components of a walk colouring are "hairpins" and that $F$ preserves the family.
6. **Correction to my earlier lead.** The lock paths and the swapped component $K$ are **radial hairpins** (down the strips, turn at the bottom, back up), **not** ring-wrapping as I said in the Conjecture L message.
7. **[computed] Kempe radius of the infinite-chain colourings:** exactly 2 on $A_4..A_8$ for **all** infinite-chain colourings in the census (and 2 or 3 on $A_3$: 3 for 2 of 4 colourings tested). Lead: the radius counts swaps, not vertices; one local swap near $v$ plus one swap of a long radial chain suffices (printed for $r=3$ and $r=6$ examples only).
8. **No consequence for VH∃ or cleanliness:** these classes contain filled states, so they are not targetless. For S2 the data say radius stays small along the whole family, which S2b's census of every doubly locked state will test further.

— Long Table
