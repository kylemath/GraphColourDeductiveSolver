# Director's note: three teams on VH∃

Long Table (Creative Intel), 2026-10-05 11:49 MDT. This note accepts the three manager reports from the session opened at 11:08. It is not a status change. Math has not reviewed it. No graph was generated and no census was run.

The standing order is `SolvingFrameworkPlan/docs/working/VHExistsAttack.md`. Each team names the step of a VH∃ argument it touches.

## What moved

**Interface.** **[hand]** A good pair whose filling path keeps every hole off a separating triangle lifts to the glued triangulation. Neighbourhoods agree off the triangle, a Kempe step lifts by the clique shortcut, and an interior slide lifts because the links agree. The third vertex of the triangle is what makes every pair of interface vertices adjacent; once the two ends of one excursion are known, that vertex is idle on the replacement path. An apex on the triangle is not this lemma. **[hand]** $H_2$, order $31$, is a success by this lift, so a separating triangle is not itself a failure. **[hand]** A smallest failure therefore has no interior witness on any separating triangle.

**[hand, pending a line-by-line review]** For every spherical triangulation of order at least $5$, the $3$-vertex cuts are exactly the separating triangles, so "no separating triangle" and "$4$-connected" are the same property. $K_4$ is the order-$4$ exception. The degree identity is $\deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 4$, and $3+3-2=4$ is attained, so the bound is not $5$. The director checked the statement and the exceptions, and did not re-line every step of the $3$-connectedness argument in `interface/positions/connectivity.md`.

**Potential.** **[computed]** On $24{:}7228$, vertex $17$, fan $0$, the untouched-set cardinality $|I|$ takes the values $23,22,16,12$ on the published mixed path and $23,15,9,4,4,10$ on the published five-swap path. The director recomputed both sequences from the published vertex sets. The fourth pure swap is flat and the fifth rises, restoring six vertices to the start colouring. The filled state has $|I|=10$, so a small untouched set is not a fill. **[hand]** Distinct link-colour counts, the defect count $3,2,2,1$, the $\beta\gamma$-chain length $8$ then $8$, and a degree height all fail a strict drop on the mixed path. $|I|$ remembers the start colouring, rises on the reverse walk, and has no rule that chooses the next move. It is a score of two walks already found. The lift of the belt potential does not rise to Medium.

**Unlock.** **[hand]** Every proper colouring of a $5$-cycle uses a colour once. No colour occurs three times, because three vertices of $C_5$ span an edge, and $C_5$ is not $2$-colourable, so the only types on at most four colours are $(2,2,1)$ and $(2,1,1,1)$. A degree-$5$ hole is never frozen. The published slide $17\to 8$ lands on $(1,3,2,1,0,3)$, still four colours, so the defect can move without filling. **[hand]** The apex slide puts $v$ between $x_{i-1}$ and $x_{i+1}$ on the new link, and the rest of that link is not a function of the old word. A rewrite on circular $5$-words does not produce the fill. **[hand]** The two chords of a fan lie in the vacant face and do not force a bichromatic path in $T-v$ to miss a crossing. Choosing the fan after reading one colouring is not the family equivalence in Remark 2.3 of `vh-exists.md`.

## What did not move

VH∃ is open. No controller replaces the belt's next-zero rule. No length bound was reopened. The same-order call at a slid hole stays circular.

The gap the Interface manager refused to paper over is still open, and it is now one sentence:

> Whether every double-locked interior of the coloured link $(p,a,q,b_2,b_1)=(0,1,2,1,3)$, and not only the order-$9$ certificate, reaches a $3$-colour link by Kempe swaps at the fixed hole $f$.

On that certificate both locks are present and two named swaps fill. The certificate has a vertex of degree $3$. It is not a failure. Beside that sentence, the carry across an inner triangle $(p,a,q)$ is unfinished. Each of $p$, $a$ and $q$ loses the neighbour $f$ in the inner completion, so that completion lies in the minimum-degree-$5$ class only when all three had degree at least $6$. Least order supplies a pair in that case and does not move the pair across the triangle. In the other case least order does not apply.

## Feasibility

| Question | Rating |
|---|---|
| The interior-witness lift | High |
| "$4$-connected" equals "no separating triangle" for order $\ge 5$ | High, pending a line-by-line review of the connectivity note |
| A smallest failure contains a separating triangle | Medium-Low |
| A controller for $\|I\|$ exists off the belt | Low |
| A rewrite on link words, or an apex slide alone, yields VH∃ | Low |
| The missing fill lemma, with no length cap and no same-order induction | Low |

## Where the pages are

| Team | Pre-meeting | Joint page | Post-meeting |
|---|---|---|---|
| Interface | `interface/pre-meeting.md` | `interface/interior-witness.md` | `interface/post-meeting.md` |
| Potential | `potential/pre-meeting.md` | `potential/lift-kill.md` | `potential/post-meeting.md` |
| Unlock | `unlock/pre-meeting.md` | `unlock/defect-and-rewrite.md` | `unlock/post-meeting.md` |

Role positions are in each team's `positions/` directory. They were written before the joint pages. The post-meetings were written after, and the Interface post-meeting has a second sitting.

## Next steps

1. Math: review the interior-witness lift and the connectivity argument. The director's own check did not re-line the $3$-connectedness proof.
2. Leave the double-lock sentence as the next hand question on line 1. An answer that only treats the order-$9$ certificate does not close it.
3. Stop the belt-potential lift. $|I|$ passed the mixed-path screen and failed as a potential. Do not raise that plan to Medium.
4. Do not reopen a length bound, a fitted rank, or a same-order induction at the slid hole.
