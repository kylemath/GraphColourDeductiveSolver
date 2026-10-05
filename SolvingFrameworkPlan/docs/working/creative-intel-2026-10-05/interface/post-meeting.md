# Post-meeting: interface

Interface team, 5 October 2026. The joint page is `interior-witness.md`. Each speaker quotes one sentence of that page as it stood before the revisions below.

## Adversary

The sentence was: "The same shortcut still returns a path in the side when the hole is the vertex $f\in F$ and the surviving interface is a single edge. That reading is recorded in (C)."

The attack lands on the label, not on the shortcut. Section (C) is a six-pair split of one coloured link. It does not say where an excursion through $B\setminus F$ ends once $f$ has been deleted, and it does not say why an excursion of the wrong colour pair has no ends at both $p$ and $q$. A pointer at (C) does not make those steps visible. The shortcut itself is the dichotomy already in the position note: ends in $\{p,q\}$, and properness on $pq$ forces the colour pair. That dichotomy was not false. The sentence that claimed it had been recorded in (C) was false.

Revised: the pointer is gone. In its place, the paragraph that begins "Suppose the hole is a vertex $f\in F$, and write $F=\{f,p,q\}$" writes the ends of an excursion, the length-$0$ and length-$1$ replacements, both directions of the restriction, and the sentence "There is no excursion whose ends are $p$ and $q$ and whose colours are a pair other than $\{c(p),c(q)\}$." The fill target is pointed at (C) as one coloured link, which is what (C) is.

## Gluer

The sentence was: "Least order on a failure $T$ supplies $A'$ a good pair."

Least order is a property of a smallest failure. A failure of larger order may sit over a smaller failure, and then $A'$ need not have a good pair. The same paragraph defined $A'$ by deleting $f$ from the $f$-side of $(p,a,q)$ and said nothing about the three boundary degrees. Each of $p$, $a$ and $q$ is adjacent to $f$ in $A$, so each degree in $A'$ is one less than in $A$. A boundary vertex of degree $5$ in $A$ arrives in $A'$ with degree $4$. The conditional "if $A'$ has minimum degree $5$" was doing that work in silence, and the quoted sentence did not restrict $T$ to a smallest failure.

The next sentence of the same paragraph called a hole on $(p,a,q)$ "the fixed-hole case (C)". Section (C) is one colouring of one five-vertex link. It does not discharge an arbitrary hole on the inner triangle.

Revised: the completion paragraph now says that each of $p$, $a$ and $q$ falls by one in $A'$, and that least order is applied to a smallest failure. The open sentence now says that a hole on $(p,a,q)$ is a fixed-hole problem of the same shape as (C), and that (C) does not discharge every such passage.

## Connectivity

The sentence was: "$\deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 4$."

The attack tried to replace $4$ by $5$, copying the degree line on the minimal-counterexample page, on the ground that a degree-$4$ cut vertex would spoil the equivalence inside the minimum-degree-$5$ class. The attack fails. Each arc contributes at least one neighbour and the two triangle edges are counted in both induced sides, so each side degree is at least $3$ and the difference of the sum and $2$ is at least $3+3-2=4$. The triangular bipyramid attains $4$. The equivalence signed on the page is for every spherical triangulation of order at least $5$, and that bipyramid is one of them. Inside the minimum-degree-$5$ class the floor $5$ is the class hypothesis, and the page already separates that sentence from the arc count. Writing $\ge 5$ into the arc count would make the bipyramid a counterexample to a true identity.

The order-$6$ certificate was checked against the same formula: side degrees $3$ and $4$, and $3+4-2=5=\deg_T(f)$. The eight faces and the seven bichromatic components listed there were not found to mis-count. That check is why the certificate sentence stands.

## Second sitting

The director left the interior lift, the cut statement, the order-$6$ edge list, and the one-swap criterion standing. This sitting is the double lock and one sentence on the carry.

### Gluer

The sentence was: "The remaining case is the double lock: a $\{2,3\}$-path from $b_1$ to $q$ exists, and under the colouring $c'$ obtained by swapping the $\{1,3\}$-component of $b_2$, a $\{0,3\}$-path from $b_2$ to $p$ exists."

That sentence stops at the crossing vertex and never says whether the second path can be drawn. On the pentagon $(p,a,q,b_2,b_1)$ the chords $b_2p$ and $qb_1$ alternate, so they are not both edges. The order-$6$ certificate uses $qb_1$. That chord separates $b_2$ from $p$, and under $c'$ the vertices $b_1$ and $q$ have colours $1$ and $2$, so the second path does not exist in that graph. The edge $b_2p$ separates $b_1$ from $q$ in colours $\{2,3\}$, so it kills the first path. A double lock needs three interior vertices: colour $2$ and colour $3$ on the first path, and colour $0$ on the second, since the preparatory swap creates no colour $0$. With $f$ and the five link vertices the smallest order is $9$.

Revised: the paragraph that begins "On the pentagon $(p,a,q,b_2,b_1)$ the chords $b_2p$ and $qb_1$ alternate" records that exclusion. The paragraph that begins "Order $9$ realizes both locks" is the certificate. Vertices $f,p,a,q,b_1,b_2,u,v,w$, twenty-one edges, fourteen faces, $9-21+14=2$. The vertex $a$ has degree $3$. It is a certificate about the coloured link, not a failure. The first path is $(b_1,u,v,q)$. After the swap on $(b_2,b_1)$, the second path is $(b_2,w,v,p)$. They meet at $s=v$.

### Adversary

The sentence was: "No sequence starting from that observation is written here."

The attack was an attempt to keep the order-$9$ link at four colours. It fails. One swap does not fill, because $(b_1,u,v,q)$ joins $b_1$ to $q$ and the six-pair split leaves no other pair. Two swaps do. Swap $\{1,3\}$ on the singleton $(v)$: the neighbours of $v$ are $q,p,u,w$, coloured $2,0,2,0$, so $v$ is not in the component of $b_2$. Then $v$ has colour $1$, and the neighbours of $q$ are $a,p,b_2,w,v$, coloured $1,0,1,0,1$. The component $(q)$ in colours $\{2,3\}$ swaps $q$ from $2$ to $3$. The link is $(0,1,3,1,3)$.

Revised: that "no sequence" sentence is removed. The certificate paragraph ends with these two swaps. The open sentence is now one sentence: "Whether every double-locked interior, and not only this order-$9$ certificate, reaches a $3$-colour link by Kempe swaps at $f$." The universal lock did not close. This certificate did.

### Connectivity

The sentence was: "Each of $p$, $a$ and $q$ is adjacent to $f$ in $A$, and $f\notin V(A')$, so each of those three degrees falls by one in $A'$."

The fall by one was already on the page. It did not say when $A'$ meets minimum degree $5$. Each of $p$, $a$ and $q$ loses $f$, so $\deg_{A'}(x)=\deg_A(x)-1$. If any one of those three degrees in $A$ is $5$, the completion has a vertex of degree $4$. Least order does not apply, and $A'$ is not a smaller failure. The case in which least order supplies a pair is the case in which all three degrees are at least $6$. That is the special case. The unfinished carry is what remains in general, and it is still unfinished when the degrees are large enough for the pair to exist.

Revised: the completion paragraph now says $A'$ lies in the minimum-degree-$5$ class only when all three had degree at least $6$ in $A$, and that otherwise least order does not supply a good pair and $A'$ is not a smaller failure. The unfinished carry is named as the generic case. The carry itself is not closed.
