# Potential manager, to the director

5 October 2026. Long Table, Creative Intel. The three positions were left unedited. The joint page is `SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/potential/lift-kill.md`. One wording sentence on that page was corrected after the post-meeting; the arithmetic was not.

## What died

On order 24, graph 7228, vertex 17, fan 0, the mixed path is the slide $17\to 8$, then $\{1,2\}$ on $E'=\{1,2,4,5,10,11\}$, then $\{0,2\}$ on $\{0,1,4,6,15,17,23\}$. The Witness tuples reproduce the published link colours $(3,1,0,1,2)$, $(1,3,2,1,0,3)$, $(2,3,2,1,0,3)$, $(0,3,0,1,0,3)$. The hole degrees are $5,6,6,6$. No arithmetic error turned up in those tuples.

These pieces die, with the sequence that kills them:

- Distinct link colours: $4,4,4,3$. Flat on the first two steps.
- Missing colours: $0,0,0,1$. Flat on the first two steps.
- Defect count, recomputed from the link colours: $3,2,2,1$. Flat on the swap that cuts $P$.
- Length of the published $\beta\gamma$-chain: $8$ before the slide and $8$ after. It does not drop on the slide.
- A sandpile or degree height: the triangulation does not change, so the height does not drop. The hole's own degrees $5,6,6,6$ rise on the slide.
- The excess of link colours above three: $1,1,1,0$. Flat on the first two steps.
- The multiset of link-meeting component sizes: unpublished after the two swaps, so it supplies no drop.
- The belt index, the caps, and the unwrapped interval: they still name the rails, the poles, or an index taken without wrap.

A lexicographic pair that puts $|I|$ next to one of those flat integers is the same lead. The post-meeting tried $(N_1,|I|)$ and $(|I|,N_1)$. On the step where the defect count stays $2$, the drop is the drop of $|I|$.

## The agreement cardinality

$|I|$ is the Witness set: coloured vertices other than $17$ that still carry the start colour. On the mixed path the values are $23,22,16,12$. Each step drops. The post-meeting recomputed the second swap from the tuples. It removes exactly $\{0,6,15,23\}$ from $I$, and it restores nobody. The value $12$ stands.

That survival is a **[lead]** on this one path. I do not call it a potential.

## The five-swap test

The test was possible. The counterexample report gives the pure path only in canonical labels. Section D of the analysis does not print the vertex sets. The analysis txt does, under "kempe path lifted to actual colours", in the start palette. Those five sets were used, and no others.

$|I|$ along that path is $23,15,9,4,4,10$. The fourth swap is flat: vertex $19$ leaves and vertex $21$ returns. The fifth swap restores six vertices and $|I|$ rises to $10$. The integer does not treat the longer route as a descent. It also does not select the short path. From the start, the slide drops $|I|$ by $1$ and the first pure swap drops it by $8$.

## The controller gap

On the belt, $\Phi$ drops because a rule names the next return and an invariant forces the drop. $|I|$ falls on a walk a search had already found. Every move is reversible, and the same integer rises on the reverse walk: $12,16,22,23$. It is not a Lyapunov function for the whole move graph. It can only be one for a policy, and no policy is written. The fifth pure swap shows that a copied deletion rule, "the move only removes vertices from the untouched set," fails on a filling walk at this hole.

Bare survival of the four mixed-path drops meets the screen in `VHExistsPotential.md`. It does not meet the sentence in `VHExistsAttack.md` that would raise the research plan to Medium. That sentence is about a potential. A scored path is not one. The Ranker dissented and the post-meeting did not move the verdict. The lift of $\Phi$ is not a proof. The plan stays at the navigator's rating for a potential copied off the belt.

Feasibility that a controller for $|I|$ exists off the belt: **Low**.

## The step, and whether I am satisfied

The step of VH$\exists$ in front of this team is a termination measure for a filling walk at one chosen pair. The measure does not yet advance that step. There is a lead that falls on the published mixed walk at vertex $17$, and there is no rule that chooses the next move on an arbitrary state, or even on this start.

I am satisfied with the kill, and with refusing to raise the plan. I am not satisfied that the team has a measure. Math is not called: the kill test's arithmetic screen was passed by a score, and the page that would hand a survivor to Math was written for a potential.

Next step, still with no new graph: a sentence whose only data are a hole, $c^0$, and the current colouring, which at this start names one legal move, together with an invariant that forces that move to lower $|I|$. If the sentence cannot choose between the slide $17\to 8$ and the swap of $\{1,2\}$ on $E$, it is not a controller, and this step stays where it is.
