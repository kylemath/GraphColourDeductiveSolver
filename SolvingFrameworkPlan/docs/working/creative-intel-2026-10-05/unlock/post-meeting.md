# Post-meeting

Unlock team, Creative Intel, 2026-10-05. Rewriter, Spin, and Obstruction attack the joint page. Two of the three attacks found errors of writing. The mathematical claims they attacked survive. The joint page is corrected in place. The pre-meeting is left as it stood.

## The triple colour

**Spin.** The independence sentence is too strong. Colour the vertices $0,1,2,3,4$ of $C_5$ by $(0,1,0,2,0)$. Colour $0$ occurs three times, on $\{0,2,4\}$. The pairs $\{0,2\}$ and $\{2,4\}$ are at cyclic distance $2$, so neither is an edge. The colouring is proper, and the defect theorem has lost the bound of two.

The attack fails. The third pair inside $\{0,2,4\}$ is $\{0,4\}$, and $4\sim 0$ is an edge of $C_5$. Both ends have colour $0$, so $(0,1,0,2,0)$ is not a proper colouring. The same edge is what the general count predicts. A $3$-set with no edge would need a complement vertex in each of the three gaps between its members, and the complement of a $3$-set has only two vertices. The pairs at distance $2$ are legal for a repeated colour. Closing them with a third vertex of that colour uses the edge that the distance-$2$ pairs had avoided. No proper colouring of $C_5$ uses a colour three times. The type list in §A is unchanged.

## The consecutive triple

**Rewriter.** Section B says the chart is translated until $x_i$ lies at $(1,0)$ and $v$ at $(0,0)$. A translation cannot do both once $v$ is at the origin and $x_i$ sits at angle $2\pi i/5$ with $i\not\equiv 0$. The order of directions is then asserted, not computed. Separately: is $(x_{i-1},\, v,\, x_{i+1})$ forced, or can the rotation put $v$ between the two link neighbours in the opposite orientation only?

The translation sentence is an error. The motion that preserves the rotation at $v$ and sends $x_i$ to angle $0$ is a rotation about $v$, not a translation. The direction comparison was missing: with $\theta=2\pi/5$, the direction from $x_i$ to $x_{i+1}$ has argument in $(\pi/2,\pi)$, the direction to $v$ is $\pi$, and the direction to $x_{i-1}$, represented in $[0,2\pi)$, has argument in $(\pi,2\pi)$.

**Revised:** the positive-rotation paragraph of §B now rotates about $v$ and compares those three arguments. The claimed order is the same one the pre-meeting fixed. Counterclockwise, the triple is $(x_{i+1},\, v,\, x_{i-1})$, coloured $c(x_{i+1})$, $c(x_i)$, $c(x_{i-1})$ in the new state.

The opposite orientation is that triple read backwards: $(x_{i-1},\, v,\, x_{i+1})$, coloured $c(x_{i-1})$, $c(x_i)$, $c(x_{i+1})$. It is not a second way of seating the vertices. The two facial triangles along $vx_i$ are adjacent wedges at $x_i$, so in every orientation the spoke to $v$ lies between the edges to $x_{i-1}$ and to $x_{i+1}$. Reversing orientation reverses the order. It does not place $x_{i-1}$ next to $x_{i+1}$ with $v$ outside the triple.

The published slide on $7228$ matches the positive order, and it is a slide to a link vertex, so the local geometry is the same as for an apex. The link of vertex $17$ is $(7,16,23,18,8)$ in the recorded order. Read that order as $(x_0,\ldots,x_4)$ and slide to $x_4=8$. Then $x_{i+1}=7$, the old hole is $17$, and $x_{i-1}=18$. The positive triple predicted by the corrected paragraph is $(7,17,18)$. The recorded link of vertex $8$ is $(1,7,17,18,19,9)$, which contains $7,17,18$ in that order. The old colours are $c(7)=3$, $c(8)=2$, $c(18)=1$, and the new colours on those three vertices are $3,2,1$, that is $c(x_{i+1})$, $c(x_i)$, $c(x_{i-1})$. The forward list is not $(18,17,7)$. The sequence $c(x_{i-1})$, $c(x_i)$, $c(x_{i+1})$ is the reverse reading, and it is the reading the positive rotation does not use.

The fragment stays signed. The right-hand side is still not a circular $5$-word. The further neighbours of the apex remain unnamed by the old word, in either orientation.

## The locked letter, and the quotation

**Obstruction.** In §F the locked word is $(\alpha,\beta,\alpha,\gamma,\delta)$, so $\alpha$ occurs twice, and the next sentence sets $\alpha=c(x_i)$. The apex colour occurs once. It is one of $\beta,\gamma,\delta$ in that word, not the repeated colour. The uniqueness sentence was written with the letter of the double colour. Separately, the block quotation of Remark 2.3 omitted two sentences of the remark and was offered as the remark's text.

Both points land.

**Revised:** the image argument in §F now lets $\rho=c(x_i)$ and lets $\eta$ be the colour missing from the new link. The letter $\rho$ is a singleton colour of the locked word. The swap is the singleton $\{\,x_i\,\}$ on $\{\rho,\eta\}$ in $T-v$. That swap would fill the old link, which the lock forbids, so the apex image lies outside $F$. The geometric conclusion is the one §B already had: $\rho$ occurs once. The letter clash was the error, and the fill of the image was not an extra assumption.

**Revised:** the quotation in §D is the continuous text of Remark 2.3 from the definition of $\mathrm{VH}^{\mathrm{fam}}(T)$ through the sentence that selecting the pair after one colouring is not available, and that selecting it after all of them gains nothing. Restoring the two omitted sentences does not change the equivalence. The Obstruction's reading agrees with that text. The family sentence is equivalent to $\mathrm{VH}\exists$ because the pairs are finite and a start may be chosen independently at each pair. A rule that reads one colouring's chains and then replaces the fan selects the pair after that colouring. The remark states that this selection is not available. It is not the family equivalence, and the joint page does not treat it as one.

The retirement of the two-chord sentence is untouched. The chords still lie in the vacant face, and they are still not edges of $T-v$. The curve obtained by putting $v$ back on one blocking path still separates a pair whose swap leaves four colours.

## What was not revised

The defect theorem, the type list, the $7228$ colour count $(1,3,2,1,0,3)$, the lock with both paths, the refusal of a same-order induction, the output sentence, and both feasibility ratings stand. The pre-meeting already fixed the positive order $(x_{i+1},\, v,\, x_{i-1})$ and the rating **Low**. Those assertions were not reopened. No length cap was added, and no induction on the slid hole was proposed.
