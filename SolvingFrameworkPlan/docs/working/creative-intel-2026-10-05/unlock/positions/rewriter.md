# Rewriter: apex slide and the Jordan rule

A state is a circular word on the link of the current hole, together with a predicate for each colour pair. The word is the colouring of the link in the rotation at the hole. For colours $a$ and $b$, the predicate records which link vertices lie in the same component of the $a$–$b$ subgraph of the deletion. Rules rewrite that state. The argument is equational. The lemma it is aimed at carries the quantifiers of $\mathrm{VH}\exists$, and the length of a path may depend on the triangulation.

## Two words on the $5$-cycle

**[hand]** A proper $4$-colouring of a $5$-cycle is of type $(2,2,1)$, or of type $(2,1,1,1)$ with the repeated colour at cyclic distance $2$. The type $(2,2,1)$ uses three colours, so the state is a fill.

**[hand]** Let $\tau_i$ be the fan at a degree-$5$ vertex $v$ with apex $x_i$, and write the link $x_i,x_{i+1},x_{i+2},x_{i+3},x_{i+4}$ in order. For $c$ proper on $\tau_i$, Corollary 3.3 says $(v,c)$ is a fill if and only if $c(x_{i+1})=c(x_{i+3})$ and $c(x_{i+2})=c(x_{i+4})$. Lemma 3.2 gives uniqueness of $c(x_i)$ on the link, so those two equalities are the alternating word on the path opposite the apex, and the word is the $(2,2,1)$ orbit. That word is the normal form a filling system would have to reach.

## The apex slide as a rewrite

**[hand]** Let $c$ be proper on $\tau_i$. By Lemma 3.2, $c(x_i)$ occurs once on the link of $v$, and the slide $v\to x_i$ is legal. As a rule it sends the hole $v$ to the hole $x_i$. The old hole $v$ receives colour $c(x_i)$. The new link is the link of $x_i$ in $T$.

The two faces $v\,x_{i-1}\,x_i$ and $v\,x_i\,x_{i+1}$ place $x_{i-1}$, $v$, $x_{i+1}$ consecutively on that new link, in that order or its reverse, coloured $c(x_{i-1})$, $c(x_i)$, $c(x_{i+1})$. Because the fan is legal, the chords $x_ix_{i+2}$ and $x_ix_{i+3}$ are absent from $T$, so the new link meets the old vertex set exactly in the triple $\{x_{i-1},v,x_{i+1}\}$. Every further vertex of the link of $x_i$ lies in the interior of $T$. The old circular word does not name those vertices, their colours, or their order, and the old predicates are components in $T-v$, while the predicates after the slide are components in $T-x_i$.

**[hand]** The obstruction is that the rule demands this new link. The interior of the triangulation supplies it. A rewrite on circular words has only the old $5$-cycle, and the right-hand side is not a word on that cycle.

**[hand]** Proposition 4.4 is the terminal case. If the slide $(v,c)\to(x_i,c')$ lands in a fill, then $(v,c)$ is already a fill, or one Kempe swap of $T-v$ that recolours only $x_i$ takes $(v,c)$ into a fill, and the two fills give the same colouring of $T$. A slide that lands in a fill rewrites as a same-hole swap. The slide whose landing state still uses four or more colours on its link is the rule above, and its right-hand side is the link the interior supplies.

## The same-hole rule

**[hand]** One Kempe swap at the same hole keeps the link cycle fixed. It is a rewrite of the old word and of the old chain predicates: the two colours are exchanged on one component, and every predicate that meets those colours is rewritten. The local effect is this. A swap on a pair that separates two link vertices deletes one blocking path. That is the degree-$4$ Jordan step.

On the degree-$4$ link coloured $(0,1,2,3)$ at $(a,b,c,d)$, the opposite pairs are $\{b,d\}$ on $\{1,3\}$ and $\{a,c\}$ on $\{0,2\}$. If the predicate joins $b$ to $d$, a simple $1$–$3$ path in the deletion, closed through the hole, separates $a$ from $c$. The rule swaps the $\{0,2\}$-component of $a$, the pair that separates. The word becomes $(2,1,2,3)$. The blocking path from $b$ to $d$ is deleted from the obstruction, and the link uses three colours. The symmetric clause swaps $\{1,3\}$ when $a$ is joined to $c$. The two joins exclude each other, so every four-colour degree-$4$ state has a redex, and one application reaches a fill.

**[hand]** A locked degree-$5$ start has word $(\alpha,\beta,\alpha,\gamma,\delta)$, up to rotation and reflection. Place it as $p_0,p_1,p_2,p_3,p_4$, so the $\beta$-vertex $p_1$ lies between the two $\alpha$'s and $p_3,p_4$ carry $\gamma,\delta$. Locked means that $T-v$ contains both a $\beta\gamma$-path $p_1\to p_3$ and a $\beta\delta$-path $p_1\to p_4$. Both useful pairs fail to separate. The swap that would recolour only $p_1$ on $\{\beta,\gamma\}$, or only $p_1$ on $\{\beta,\delta\}$, is the swap that reaches three colours, and the lock says neither component is a singleton at $p_1$.

The Jordan rule deletes one blocking path, by one swap, on one colour pair. Two paths are present. One swap cannot delete both. Swapping the joined $\beta\gamma$-component sends the word to $(\alpha,\gamma,\alpha,\beta,\delta)$. Swapping the joined $\beta\delta$-component sends the word to $(\alpha,\delta,\alpha,\gamma,\beta)$. Each still uses four colours. A swap on a pair that does separate deletes one join and leaves a four-colour word: the path that is present separates a pair whose exchange keeps four colours on the link. The right-hand side is not the fill named by Corollary 3.3.

**[hand]** This is why a one-rule Knuth–Bendix system on the link word does not fill. Orient the Jordan deletion as the only rule. A word of type $(2,2,1)$ is a normal form, and inside the fan it is the fill of Corollary 3.3. The locked word $(\alpha,\beta,\alpha,\gamma,\delta)$ is not that form. Its useful pairs are joins, so the rule has no redex on them. A redex on any separating pair deletes one blocking path and leaves four colours. The locked word is therefore irreducible under the filling reading of the rule, and it is not a fill.

The chain predicate is already in the state, and on the locked word it is exactly the pair of joins the rule fails to clear. A chord of $\tau_i$ is fixed with the fan, before the colouring; the two locked paths run in $T-v$, where those chords are absent, and the separation they force is the separation of a pair that does not fill. The letter the apex-slide rule still has to read is the link of $x_i$.

## The quantifiers the rule serves

**[lead]** For every spherical triangulation of minimum degree $5$, some degree-$5$ vertex and some legal fan are fixed before the colourings. Every colouring admitted by that fan reaches a fill by some finite path of slides and Kempe swaps, and the length may depend on the triangulation. That is the sentence $\mathrm{VH}\exists$. The Jordan rule is the degree-$4$ step of such a path. On a locked degree-$5$ word it stops after deleting one path.

**[open]** The apex slide is the continuation that leaves the $5$-cycle. Its right-hand side is a later link. A frozen link uses all four colours at least twice, so it has at least eight vertices, and a degree-$5$ start is never frozen. The question which bichromatic blocks that later word freezes for every interior, and which blocks a change of interior unlocks, is a question about the new link. The length of the path is not the datum the rule is missing.

Feasibility that a rewrite system on link words alone produces the fill is **Low**; the extra datum the rewrite needs is a new link.
