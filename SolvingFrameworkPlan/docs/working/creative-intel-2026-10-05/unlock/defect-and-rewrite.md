# Defect and rewrite

Unlock, joint page, 2026-10-05. The assertions are those fixed in the pre-meeting. Indices on a $5$-cycle are read modulo $5$. Colours are $\{0,1,2,3\}$. A state is a hole together with a proper colouring of the deletion. The fill set $F$ is the set of states whose link uses at most three colours. A legal fan $\tau_i$ at a degree-$5$ vertex $v$ has apex $x_i$ and chords $x_ix_{i+2}$, $x_ix_{i+3}$, neither an edge of $T$. The link of $v$ in positive rotation is $x_0,\ldots,x_4$.

## A. The defect theorem

**[hand]** Let $C_5$ have vertices $0,1,2,3,4$ and edges $i\sim i+1$. Every set of three vertices spans an edge. The complement of a $3$-set has two vertices. If a $3$-set $A$ contained no edge, no two elements of $A$ would be consecutive on the cycle, so each element of $A$ would be followed by at least one element of the complement before the next element of $A$. Three elements would require three complement vertices. Only two exist. A colour class of a proper colouring is an independent set, so no colour occurs three times.

$C_5$ is not $2$-colourable. If $c$ took values in $\{0,1\}$ and were proper, then $c(i+1)\ne c(i)$ for every $i$, so $c(i)\equiv c(0)+i\pmod 2$. Then $c(4)=c(0)$, while $4\sim 0$.

A proper colouring therefore uses $k$ colours with $3\le k\le 4$, each multiplicity in $\{1,2\}$, summing to $5$.

If $k=3$, the parts $a\ge b\ge c$ satisfy $1\le c\le b\le a\le 2$ and $a+b+c=5$. Then $a=2$, so $b+c=3$, and the bounds force $b=2$, $c=1$. The type is $(2,2,1)$.

If $k=4$, four parts, each at least $1$ and at most $2$, sum to $5$. The excess over $4$ is $1$, so one part equals $2$ and the other three equal $1$. The type is $(2,1,1,1)$.

The integer solutions $(3,2)$, $(3,1,1)$ and $(5)$ each have a part at least $3$. The three vertices of that colour span an edge, so those solutions are not proper colourings. Five colours are outside the palette. Both surviving types have a part equal to $1$.

Type $(2,2,1)$ uses three colours on the link. The state lies in $F$. It is a three-colour fill. The multiplicity-$1$ colour is still a singleton, so a slide along its vertex is legal, and the state is already a fill.

Type $(2,1,1,1)$ uses four colours, so the state is unfilled. The three parts equal to $1$ are three distinct colours, on three distinct vertices. Each occurs once on the link, so each determines a legal singleton slide. The two vertices of the repeated colour are non-adjacent, hence at cyclic distance $2$. Up to rotation, reflection, and renaming, the word is $(\alpha,\beta,\alpha,\gamma,\delta)$ with $\alpha,\beta,\gamma,\delta$ pairwise distinct.

A frozen link is a proper colouring in which all four colours occur at least twice. It then has at least eight vertices, and it admits no singleton slide. A $5$-cycle has five vertices. By the type list, every proper colouring of it has a singleton, so every degree-$5$ state has a legal slide. A degree-$5$ hole is never frozen.

A singleton slide need not fill. On order $24$, graph $7228$, the link of vertex $17$ is $(7,16,23,18,8)$, coloured $(3,1,0,1,2)$. The type is $(2,1,1,1)$. The slide $17\to 8$ carries colour $2$. The link of vertex $8$ is $(1,7,17,18,19,9)$, coloured $(1,3,2,1,0,3)$. All four colours occur. The state is unfilled.

## B. The apex slide is not a rewrite of the old word

**[hand]** Let $c$ be proper on $T-v$ and proper on $\tau_i$. The link edges give $c(x_i)\ne c(x_{i-1})$ and $c(x_i)\ne c(x_{i+1})$. Properness on the two chords gives $c(x_i)\ne c(x_{i+2})$ and $c(x_i)\ne c(x_{i+3})$. The five link vertices are distinct, so $c(x_i)$ occurs once on the link of $v$. The slide $v\to x_i$ is legal. Write $c'$ for the new colouring: $c'(v)=c(x_i)$, and $c'=c$ off $\{v,x_i\}$.

The edge $vx_i$ lies in two facial triangles, $v\,x_{i-1}\,x_i$ and $v\,x_i\,x_{i+1}$. At $x_i$ those two triangles are adjacent wedges along the spoke to $v$. The neighbours $x_{i-1}$, $v$, $x_{i+1}$ are therefore consecutive on the link of $x_i$, and $v$ is the middle vertex. No orientation moves $v$ out from between them.

The sense is fixed by the positive rotation at $v$. Place that rotation in the oriented plane with $v$ at the origin and $x_j$ at angle $2\pi j/5$. Rotate the plane about $v$ until $x_i$ lies at angle $0$, hence at $(1,0)$ on the unit circle. Rotation about $v$ preserves orientation. Then $x_{i+1}$ lies at angle $\theta=+2\pi/5$ and $x_{i-1}$ at angle $-\theta$. The direction from $x_i$ to $v$ is angle $\pi$. The direction from $x_i$ to $x_{i+1}$ is the argument of $(\cos\theta-1,\sin\theta)$. Since $\theta\in(0,\pi)$, one has $\sin\theta>0$, and $\cos\theta-1<0$, so this argument lies in $(\pi/2,\pi)$, strictly before the direction to $v$. The direction from $x_i$ to $x_{i-1}$ is the argument of $(\cos\theta-1,-\sin\theta)$. Representatives in $[0,2\pi)$ put that argument in $(\pi,2\pi)$, strictly after the direction to $v$. Counterclockwise order is increasing argument: toward $x_{i+1}$, toward $v$, toward $x_{i-1}$. The positive rotation at $x_i$ reads
$$
(x_{i+1},\, v,\, x_{i-1}),
$$
coloured
$$
\bigl(c(x_{i+1}),\, c(x_i),\, c(x_{i-1})\bigr)
$$
in the state $(x_i,c')$. The opposite orientation reads $(x_{i-1},\, v,\, x_{i+1})$, coloured $\bigl(c(x_{i-1}),\, c(x_i),\, c(x_{i+1})\bigr)$. That is the same triple reversed.

The fan is legal, so $x_ix_{i+2}$ and $x_ix_{i+3}$ are absent from $T$. The only vertices of $\{v,x_0,\ldots,x_4\}$ adjacent to $x_i$ are $v$, $x_{i-1}$ and $x_{i+1}$. Since the minimum degree is $5$, the link of $x_i$ has at least two further vertices. They lie in $V(T)\setminus\{v,x_0,\ldots,x_4\}$. The circular word on $x_0,\ldots,x_4$ does not name them, their colours, or their place in the rotation. The chain predicates of the old state record which link vertices lie in the same component of $T-v$. After the slide the predicates are components of $T-x_i$. A rewrite whose input is a circular $5$-word, with or without those predicates, has no right-hand side equal to the link of $x_i$.

Feasibility of filling by a rewrite system on circular $5$-words alone: **Low**. The slide is the move that leaves the $5$-cycle, and its right-hand side is not such a word. The moves that remain on the word are the Kempe swaps at the same hole, and the next section records that one such swap does not fill the locked word.

## C. One swap deletes one blocking path

**[hand]** On a degree-$4$ link $a,b,c,d$ coloured $0,1,2,3$, with the diagonal $ac$ absent from $T$, one blocking path is enough. If $b$ and $d$ lie in different components of $(T-v)[1,3]$, the swap of the component of $b$ sends the link to $0,3,2,3$. If they lie in the same component, a simple $b$–$d$ path $P$ in those colours, closed through $v$, is a Jordan curve in the embedding of $T$. The rotation at $v$ puts $a$ and $c$ on opposite sides of that curve, so $a$ and $c$ lie in different components of $(T-v)[0,2]$. The swap of the component of $a$ sends the link to $2,1,2,3$. One swap deletes the obstruction coming from that one path, and the link uses three colours.

On a degree-$5$ link the same one-path step meets two paths. Place the locked word as $p_0,p_1,p_2,p_3,p_4$ coloured $(\alpha,\beta,\alpha,\gamma,\delta)$, with the four names pairwise distinct. Locked means that $T-v$ contains both a $\beta\gamma$-path $p_1\to p_3$ and a $\beta\delta$-path $p_1\to p_4$. The six colour pairs are as follows. A component that misses the link leaves the word unchanged.

- On $\{\alpha,\beta\}$ the link edges $p_0p_1$ and $p_1p_2$ put $p_0,p_1,p_2$ in one component. The swap sends the link to $(\beta,\alpha,\beta,\gamma,\delta)$.
- On $\{\gamma,\delta\}$ the edge $p_3p_4$ forces the swap $(\alpha,\beta,\alpha,\delta,\gamma)$.
- On $\{\alpha,\gamma\}$ the edge $p_2p_3$ puts $p_2$ and $p_3$ together, and $p_0$ either joins them or does not. The three swaps send the link to $(\gamma,\beta,\gamma,\alpha,\delta)$, $(\alpha,\beta,\gamma,\alpha,\delta)$ and $(\gamma,\beta,\alpha,\gamma,\delta)$.
- On $\{\alpha,\delta\}$ the edge $p_4p_0$ puts $p_0$ and $p_4$ together, and $p_2$ either joins them or does not. The three swaps send the link to $(\delta,\beta,\delta,\gamma,\alpha)$, $(\delta,\beta,\alpha,\gamma,\alpha)$ and $(\alpha,\beta,\delta,\gamma,\delta)$.
- On $\{\beta,\gamma\}$ there is no link edge between $p_1$ and $p_3$. If they lie in different components, the swap of $p_1$ produces $(\alpha,\gamma,\alpha,\gamma,\delta)$ and the swap of $p_3$ produces $(\alpha,\beta,\alpha,\beta,\delta)$, each on three colours. If the $\beta\gamma$-path is present, both ends move, and the image is $(\alpha,\gamma,\alpha,\beta,\delta)$, on four colours.
- On $\{\beta,\delta\}$ there is no link edge between $p_1$ and $p_4$. Separation gives $(\alpha,\delta,\alpha,\gamma,\delta)$ or $(\alpha,\beta,\alpha,\gamma,\beta)$, each on three colours. The $\beta\delta$-path sends both ends together, and the image is $(\alpha,\delta,\alpha,\gamma,\beta)$, on four colours.

Each of the images in the first four pairs uses four colours. In the locked placement both paths are present, so the two three-colour branches are closed. Every swap available at $v$ leaves four colours. One swap does not fill.

The two three-colour branches are the reason both paths belong in the lock. If the $\beta\gamma$-path is absent, the swap of the component of $p_1$ on $\{\beta,\gamma\}$ fills. If the $\beta\delta$-path is absent, the swap of the component of $p_1$ on $\{\beta,\delta\}$ fills. This is the standard lock. It is not a bound on the length of a later path.

## D. The two-chord sentence does not follow

The sentence under retirement is this one.

> The two chords of $\tau$ split the face $C_v$ into the triangles $x_ix_{i+1}x_{i+2}$, $x_ix_{i+2}x_{i+3}$ and $x_ix_{i+3}x_{i+4}$, and therefore a bichromatic path in $T-v$ misses at least one of the two crossings those chords mark.

**[hand]** The splitting is a fact about the embedding of $T^\ast_\tau$. The two chords are drawn in the face bounded by $C_v$ in $T-v$, the face left when $v$ is deleted. They are not edges of $T-v$: legality is exactly the statement that the edge set of $T^\ast_\tau$ is the edge set of $T-v$ with those two chords adjoined. A path in $T-v$ is carried by edges of $T-v$. Those edges meet the vacant face only along $C_v$. The interiors of the chords lie in the vacant face, and the path does not enter that face. A shared point of the path and a chord can lie on $C_v$ only as a common endpoint. The chords do not separate the path from anything in the opposite disk, because the path never meets them.

A curve that is not in the graph does not do the work of the degree-$4$ diagonal. In that argument the separating curve is $\Gamma=v\,b\,P\,d\,v$, drawn in the embedding of $T$ with $v$ present, while $P$ lies in $T-v$. Rebuilding that curve on the locked word uses one of the two paths, not the fan chords. Take $P$ the $\beta\delta$-path from $p_1$ to $p_4$, and set $\Gamma=v\,p_1\,P\,p_4\,v$. The spokes $vp_1$ and $vp_4$ put $p_0$ and $p_2$ on opposite sides of $\Gamma$, so a path in the remaining two colours cannot join them. The swap licensed by that separation is one of the four-colour images in §C. Take instead the $\beta\gamma$-path from $p_1$ to $p_3$. The curve through $v$ separates $p_2$ from $p_4$, and the swap of that separated pair again leaves four colours. The pair joined by the path is the pair whose separation would have filled. The pair the curve separates is a pair whose swap does not fill. The degree-$4$ rebuild, carried out with $v$ present, does not yield the retired sentence.

The word "therefore" does not follow from the splitting. The antecedent is the drawing of two non-edges in the vacant face. The consequent is an absence among paths in $T-v$. Joint presence of the two paths is a property of the colouring of $T-v$. Legality of the fan is the absence of the same chords from $T$. The second does not constrain the first.

**[hand]** Remark 2.3 equates two sentences, and the Obstruction's reading of it agrees with the remark. The remark's equivalence is the following.

> One could therefore assume only $\mathrm{VH}^{\mathrm{fam}}(T)$: for every family $(c_{v,\tau})$ with $c_{v,\tau}\in S(v,\tau)$, some pair has $(v,c_{v,\tau})$ reaching $F$. This suffices for Theorem A by the same proof. It is equivalent to $\mathrm{VH}^\exists(T)$. ($\Leftarrow$) is clear. ($\Rightarrow$): if every pair $p$ had a start $c_p$ not reaching $F$, the family $(c_p)$ would violate $\mathrm{VH}^{\mathrm{fam}}$; the pairs are finitely many and are chosen independently. So the review's warning stands in substance. Selecting the pair after one colouring is not available, and selecting it after all of them gains nothing.

The pair in $\mathrm{VH}\exists$ is chosen before the colourings. The equivalent relaxation chooses, for a whole family at once, some pair whose chosen start reaches $F$. A rule that reads the paths of a single colouring and then replaces $\tau$ chooses the pair after that colouring. That is a different sentence. Nothing in the equivalence licenses it.

## E. The apex class is the circular variant

**[hand]** The sentence "the apex slide lands in a Kempe class that contains a fill" says that, at the hole $x_i$, some sequence of swaps of $T-x_i$ reaches $F$. The triangulation is still $T$, on $n$ vertices. The states along that sequence are states of $M(T)$. Quoting a fill there quotes a fill at the same order.

The induction that uses $\mathrm{VH}\exists$ colours $T^\ast_\tau$. That graph is the triangulation of order $n-1$ obtained by deleting $v$ and drawing the two chords of the original fan, before any slide. The inductive colouring claim supplies one start in $S(v,\tau)$. The hypothesis is applied once, to $T$. The slide $v\to x_i$ produces a state of the same $T$. It does not produce a second copy of $T^\ast_\tau$, and it does not produce a spherical triangulation of order $n-1$ to which that colouring claim applies: $T-x_i$ is the deletion at the new hole, with a face of length $\deg(x_i)$.

This page does not propose an induction on the slid hole. A later state $(x_i,c')$ is a state of $T$. Treating a fill in its Kempe class as an inductive conclusion is the circular variant.

**[compiled]** The short-fill theorem takes a mixed filling path of length $n\le 2$, on an arbitrary simple graph with an initially proper deletion colouring, and returns a pure Kempe filling path at the original hole of length at most $n$. The three-move obstruction assumes a proper deletion start with no pure fill within three swaps, together with a target-reaching mixed path of length three, and concludes that the path starts with a legal singleton slide and that any two-swap finish after that slide has the slid colour in its first pair. Both theorems take a path as data. A bound on a longer path is not a conclusion of either.

**[hand]** A component that misses $F$ contains no mixed path of length at most $2$ from the start to $F$, so the short-fill theorem has nothing to convert. The shape in the next section supplies no path of length three, so the three-move obstruction has nothing to read. Neither theorem is a reason that the component meets $F$.

## F. The shape that remains

**[hand]** Let $\mathcal K$ be a component of $M(T)$ that meets $S(v,\tau_i)$ and misses $F$. Take a start $c$ in the meeting. Then $(v,c)\notin F$. By §A the link is of type $(2,1,1,1)$, and up to dihedral action and renaming it is $(\alpha,\beta,\alpha,\gamma,\delta)$. If either useful path were absent, §C would give a swap at $v$ into $F$, and that swap is an edge of $M(T)$, so $\mathcal K$ would meet $F$. Both paths are present.

The apex colour occurs once, by the count in §B, so the slide $v\to x_i$ is legal. Its image is adjacent to $(v,c)$ and therefore lies in $\mathcal K$.

The image itself is unfilled. Let $\rho=c(x_i)$. By §B the colour $\rho$ occurs once on the link, so in the word $(\alpha,\beta,\alpha,\gamma,\delta)$ it is one of the three singleton colours. It is not the repeated colour. Suppose the image lay in $F$. Some palette colour $\eta$ would then be missing from the new link. The new link carries $v$ coloured $\rho$, so $\eta\ne\rho$. The start uses all four colours, so $\eta$ occurs on the old link. In $T-v$ the vertex $x_i$ has no neighbour coloured $\rho$, by properness, and no neighbour coloured $\eta$, because every neighbour of $x_i$ other than $v$ keeps its colour and $\eta$ is missing from the new link. The $\{\rho,\eta\}$-component of $x_i$ in $T-v$ is the singleton $\{x_i\}$. Swapping it replaces $\rho$ by $\eta$ on the link of $v$. The colour $\rho$ was unique there and $\eta$ was already present, so the resulting link uses three colours. That swap would be an edge from $(v,c)$ into $F$, which the lock forbids. The apex image of a locked start lies outside $F$.

**[lead]** The output of this team is one sentence. A non-filling component at a degree-$5$ legal fan contains a locked start of type $(2,1,1,1)$, both blocking paths in $T-v$, and the legal apex slide, whose image stays in the component and outside $F$; it does not contain a reason that the component meets $F$. This is the shape of the missing lemma, not the lemma.

**[open]** Whether any sentence whose data are the embedding of $T$, the vertex $v$ and the fan $\tau$, fixed before the colourings, forces such a component to meet $F$.

Feasibility that this shape can be filled without a length cap and without a same-order induction: **Low**. The three sentences that offered to fill it were the two-chord selection, a rewrite on the old $5$-word, and a Kempe class at the new hole. The first does not follow. The second has no right-hand side on the old word. The third quotes a fill at order $n$. No replacement is in hand.

## Next

A later sentence has to force the component into $F$ from the embedding of $T$, with $(v,\tau)$ fixed before the colourings. It cannot be a length cap, a per-colouring change of fan, or a call at the slid hole. This page does not contain that sentence.
