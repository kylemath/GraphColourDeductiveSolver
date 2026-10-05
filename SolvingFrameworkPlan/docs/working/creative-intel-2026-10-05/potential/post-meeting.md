# Post-meeting: attacks on the joint page

5 October 2026. Witness, Ranker, and Physicist, against `lift-kill.md`. The pre-meeting is left as it was written.

## The second swap and the set $I$

**Witness.** The joint page says the second swap removes exactly $\{0,6,15,23\}$ from $I$. That is the step that produces the drop from $16$ to $12$. If the intersection is a different set, the four values are wrong and the lead fails with them.

The start tuple and the tuple after the slide are printed in section A. The first swap exchanges $\{1,2\}$ on vertices $1,2,4,5,10,11$, which the after-slide tuple colours $1,2,1,2,1,2$. The tuple immediately before the second swap is therefore

$$
(0,2,1,3,2,1,0,3,\cdot,3,2,1,3,0,3,2,1,2,1,0,2,1,3,0).
$$

This is the third tuple in the Witness table. Compare it with $c^0$,

$$
(0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,\cdot,1,0,2,1,3,0),
$$

under the Witness definition: coloured, different from $17$, and equal to $c^0$. Vertex $8$ is the hole. Vertex $17$ is coloured $2$ and is excluded by $x\neq 17$.

| Vertex | Current | $c^0$ | In $I$ |
|---|---|---|---|
| $0$ | $0$ | $0$ | yes |
| $1$ | $2$ | $1$ | no |
| $2$ | $1$ | $2$ | no |
| $3$ | $3$ | $3$ | yes |
| $4$ | $2$ | $1$ | no |
| $5$ | $1$ | $2$ | no |
| $6$ | $0$ | $0$ | yes |
| $7$ | $3$ | $3$ | yes |
| $9$ | $3$ | $3$ | yes |
| $10$ | $2$ | $1$ | no |
| $11$ | $1$ | $2$ | no |
| $12$ | $3$ | $3$ | yes |
| $13$ | $0$ | $0$ | yes |
| $14$ | $3$ | $3$ | yes |
| $15$ | $2$ | $2$ | yes |
| $16$ | $1$ | $1$ | yes |
| $18$ | $1$ | $1$ | yes |
| $19$ | $0$ | $0$ | yes |
| $20$ | $2$ | $2$ | yes |
| $21$ | $1$ | $1$ | yes |
| $22$ | $3$ | $3$ | yes |
| $23$ | $0$ | $0$ | yes |

That is sixteen vertices: $\{0,3,6,7,9,12,13,14,15,16,18,19,20,21,22,23\}$. The swapped set is $\{0,1,4,6,15,17,23\}$. Their membership is: $0$ in, $1$ out, $4$ out, $6$ in, $15$ in, $17$ out, $23$ in. The intersection is $\{0,6,15,23\}$.

The exchange sends those four to $2,2,0,2$. None equals $c^0$. Vertex $1$ goes from $2$ to $0$, and $c^0(1)=1$. Vertex $4$ goes from $2$ to $0$, and $c^0(4)=1$. Vertex $17$ goes from $2$ to $0$ and stays outside the definition. No swapped vertex enters $I$. The drop is $16-4=12$.

The Ranker definition $V\setminus\{h_0,h\}$ with $h_0=17$ and $h=8$ excludes the same two vertices, and $c^0$ does not colour $17$, so painting $17$ with $0$ does not put $17$ into $I$ under that wording either. The two formulas agree on this step.

The attack fails. The second swap does remove exactly $\{0,6,15,23\}$.

## A lexicographic patch

**Physicist.** The defect count $3,2,2,1$ dies because the middle step is flat. Pair it with the agreement cardinality in the lexicographic product $\mathbb{N}\times\mathbb{N}$, smaller first. The pairs are

$$
(3,23),\ (2,22),\ (2,16),\ (1,12).
$$

Each step drops. On the middle step the defect count stays $2$ and $|I|$ goes from $22$ to $16$. The same patch with the coordinates reversed is

$$
(23,3),\ (22,2),\ (16,2),\ (12,1),
$$

which drops because the first coordinate drops. A third try, the excess in front of the defect count, is $(1,3)$, $(1,2)$, $(1,2)$, $(0,1)$. The middle pair is flat. That patch dies on the same step that killed the defect count.

**Ranker.** The reversed pair is $(|I|, N_1)$. The forward pair drops on the flat step of $N_1$ only because $|I|$ drops. Either way the moving coordinate on the step that killed the defect count is $|I|$. The patch is the same lead. It does not revive the defect count, the chain length, or the excess.

The Witness adds the five-swap values already on the joint page. A pair whose first coordinate is $|I|$ stalls where $|I|$ stalls: the fourth pure swap is flat and the fifth rises. The patch inherits the stall.

## The deletion sentence

**Ranker.** Section E said that the belt invariant is already false on this hole, because the fifth swap restores six vertices. That identifies a belt statement with a claim about graph $7228$. The belt invariant says that a named return on the belt only deletes vertices from the untouched interval. It does not speak about this swap. The restoration shows that the copied deletion property fails on the fifth swap. It does not show that the belt sentence is false.

The same speaker then recomputes the fourth pure swap, looking for a miscount that would make $23,15,9,4,4,10$ into a descent. After the third swap, $I=\{15,19,20,22\}$. The fourth set is $\{2,3,5,9,12,14,19,21\}$. The intersection is $\{19\}$. Vertex $19$ carries $0=c^0(19)$ and goes to $1$. Vertex $21$ carries $0$ against $c^0(21)=1$ and goes to $1$. One leaves and one enters. $|I|$ stays $4$. The fifth swap then restores $0,3,6,12,13,14$ and raises $|I|$ to $10$. The six values stand.

The Ranker restates the dissent. The four mixed-path drops are what the navigator called surviving the path, and the attack page priced that survival at Medium. The joint page refused the raise.

**Witness.** The dissent was already on the page, and the arithmetic the Ranker just repeated is why the refusal stands. A descent on the mixed walk, a stall on the fourth pure swap, and a rise on the fifth are one integer with no rule that chooses among them. From the start, the slide drops $|I|$ by $1$ and the opening pure swap drops it by $8$. The integer accepts both.

## What the attacks changed

The intersection $\{0,6,15,23\}$ stands. The lexicographic patch is the same lead. The six pure-path values stand. One sentence in the verdict over-identified the belt invariant with a claim about this hole.

Revised: in `lift-kill.md`, the ranks $q$ and $\mathrm{lin}$ are no longer called dead; the page says they are not revived. The feasibility paragraph no longer says the belt invariant is false on this hole. It now says that on the belt the invariant is deletion by a named return, and that this deletion property does not hold for the fifth swap, which restores six vertices. The verdict is otherwise unchanged: the lift of $\Phi$ is not a proof, and the plan does not rise to Medium.

The step in front of this team was a termination measure for a filling walk at one chosen pair. The attacks did not produce one. The sentences that die are the distinct-colour count, the missing-colour count, the defect count, the $\beta\gamma$-length, the degree height, the excess, the link-meeting multiset, and every sentence that still names a rail, a pole, or an unwrapped index. $|I|$ remains a lead on the mixed path and is not a measure for the walk.
