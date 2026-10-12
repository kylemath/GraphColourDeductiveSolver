# Covering spaces, monodromy, and the locked pentagon

4 October 2026. Variability seed 23. Local colourings only. The 32-vertex pentakis dodecahedron and the 42-vertex frequency-2 icosahedron were not coloured. No Four Colour proof is claimed.

**Verdict: KILL ALL.** On the exhibit colouring the monodromy is the identity permutation of the bridge link $(0,1,0,2,3)$.

The object is a proper $4$-colouring of the $15$-vertex star with the centre deleted, boundary $(0,1,0,2,3)$ on the five bridges, as in `isolated-local.md`. The frequency-2 colouring is the one on which every far pentagon is an illegal second slide:

$$
\gamma(m)=(0,1,0,2,3),\qquad \gamma(p)=(1,0,1,0,0),\qquad \gamma(q)=(2,2,3,1,2).
$$

Colours are $\{0,1,2,3\}$. Indices are modulo $5$. The centre $c$ is the hole. Its link, in rotation order, is $(m_0,m_1,m_2,m_3,m_4)$.

## The monodromy that was computed

A state is a hole together with a proper colouring of every other vertex that the state uses. A singleton slide along an edge $h\to x$ writes the colour of $x$ onto $h$ and moves the hole to $x$. It is legal when that colour appears once on the link of $h$. A closed walk based at $c$ returns a colouring of the same five bridges. The monodromy is the resulting permutation of the ordered $5$-tuple. The identity tuple is $(0,1,0,2,3)$.

The bridge $5$-cycle does not lift to a legal slide walk. From $c$ the repeated colour $0$ sits on $m_0$ and $m_2$, so the only legal first steps are $m_1$, $m_3$ and $m_4$. On each of those bridges the two cycle-neighbours are duplicated colours, so the hole cannot take either edge of the $5$-cycle.

- At $m_1$, after $c\to m_1$, the link in rotation order is $(q_1,m_2,c,m_0,q_0,p_1)$ with colours $(2,0,1,0,2,0)$. Colour $0$ appears three times. The only legal slide is back to $c$.
- At $m_3$, after $c\to m_3$, the link is $(q_3,m_4,c,m_2,q_2,p_3)$ with colours $(1,3,2,0,3,0)$. The cycle-neighbours $m_4$ and $m_2$ carry colours $3$ and $0$, each twice. The legal slides are back to $c$ and on to $q_3$.
- At $m_4$, after $c\to m_4$, the link is $(p_4,q_4,m_0,c,m_3,q_3)$ with colours $(0,2,0,3,2,1)$. The cycle-neighbours $m_0$ and $m_3$ are duplicated. The legal slides are back to $c$ and on to $q_3$.

Each return $c\to m_i\to c$ restores $(0,1,0,2,3)$. These three walks are involutions.

The only other slide the star determines is the step onto $q_3$. The full link of $q_3$ is $(p_3,o_{35},o_{33},p_4,m_4,m_3)$, where $o_{35}$ and $o_{33}$ are the two degree-$6$ vertices outside the star. They are adjacent to each other. In the exhibit, $o_{35}$ meets $q_3$ in colour $1$ and $p_3$ in colour $0$, and $o_{33}$ meets $q_3$ in colour $1$ and $p_4$ in colour $0$. The only proper pairs are therefore

$$
(\gamma(o_{35}),\gamma(o_{33}))\in\{(2,3),(3,2)\}.
$$

Both pairs block the crossing that would have joined the two spurs.

- Arrive by $c\to m_3\to q_3$. Then $c$ has colour $2$, $m_3$ has colour $1$, and $m_4$ still has colour $3$. The link colours are $(0,\,2\text{ or }3,\,3\text{ or }2,\,0,\,3,\,1)$. Colour $3$ appears twice, so the slide $q_3\to m_4$ is illegal. Colour $1$ appears once, on $m_3$, so the slide back to $m_3$ is legal and undoes the step.
- Arrive by $c\to m_4\to q_3$. Then $m_3$ still has colour $2$ and the link colours are $(0,\,2\text{ or }3,\,3\text{ or }2,\,0,\,1,\,2)$. Colour $2$ appears twice, so $q_3\to m_3$ is illegal. The slide back to $m_4$ undoes the step.

The two outer vertices of colour $2$ are legal exits, and each has three neighbours outside the coloured set. Any walk through those neighbours is invisible to the exhibit. Within the moves the colouring decides, the slide graph is a tree of involutions: three spurs from $c$, two of them extended by an out-and-back through $q_3$. Every closed walk returns the tuple $(0,1,0,2,3)$. The monodromy is the identity in $S_5$ on the bridges and the identity in $S_4$ on the colours.

The same boundary on the pentakis star has the same visible monodromy. The document's three singleton links give out-and-back slides to $f_1$, and out-and-back slides through $g_3$ and through $g_4$, and no cycle whose link lies entirely in the coloured star.

## Two transports that are not monodromies

Reading uniqueness only on the four neighbours of $q_3$ inside the star makes $q_3\to m_4$ and $q_3\to m_3$ look legal. Carrying those steps around and back to $c$ replaces the link by $(0,1,0,2,1)$ or by $(0,1,0,1,3)$. Each of those tuples uses three colours, so the centre would accept the missing colour at once. Both steps are illegal in the two proper colourings of $(o_{35},o_{33})$ above. The three-colour returns are not monodromies of the exhibit.

On the pentakis colouring a five-step walk $c\to f_4\to g_4\to e_4\to f_0\to c$ returns the different tuple $(3,1,0,2,1)$, with the repeated colour moved from $\{f_0,f_2\}$ to $\{f_1,f_4\}$, and the returned colouring has legal slides onto far pentagons. The middle step $g_4\to e_4$ uses the link $(o_{10},e_4,f_4,e_3,o_{16},o_{29})$. Exactly one of the five proper colourings of those three outer vertices by colours in $\{0,1,2,3\}$, namely $(3,3,0)$, makes every step legal. The other four proper colourings stop the walk. Those three colours are not in the exhibit, so this permutation is invisible to the colouring.

## Mappings

A mapping names an object on the pair $(\text{hole},\text{colouring})$ and a computation that can kill it. Seed 23 is used as the icosahedral reading: the frequency-2 star sits on the icosahedron, whose rotational symmetry is $A_5$.

### 1. Deck transformation of the slide cover

The legal slide graph covers the set of hole positions. Based at $(c,\gamma)$, a closed walk acts on the fibre of link tuples. The object is that permutation representation $\rho$.

On the exhibit the determined component is a tree of involutions, so the fundamental group is trivial and $\rho$ is the identity on $(0,1,0,2,3)$. The identity does not create a legal far-pentagon slide. The identification that a deck transformation rewrites the locked boundary dies on this colouring. The monodromy is visible, and it is trivial.

### 2. Klein holonomy of the bridge plaquette

Write the colours as elements of $\mathbb{Z}_2\times\mathbb{Z}_2$ by $0=(0,0)$, $1=(1,0)$, $2=(0,1)$, $3=(1,1)$, and assign to each oriented edge the sum of its endpoint colours. The object is the sum of those values around the bridge $5$-cycle.

The edge sums on $(m_0m_1m_2m_3m_4)$ are $(1,1,2,1,3)$, and $1+1+2+1+3=0$. The same cancellation holds for every closed walk of every vertex colouring, because the sum telescopes. The holonomy does not read the tuple $(0,1,0,2,3)$. This mapping is killed because its monodromy is invisible to the colouring.

The developing map of the equilateral triangulation gives the same death in another group. Five triangles around $c$ leave an angle deficit of $60^\circ$, so the geometric holonomy is a rotation by $60^\circ$. That rotation is fixed by the degree. It is the same rotation for every colouring of every degree-$5$ link, and it does not permute $\{0,1,2,3\}$.

### 3. Braid of the hole with a degree-$5$ defect

The configuration space of the hole and one far pentagon, as two distinct points of the sphere, has fundamental group $\mathbb{Z}/2\mathbb{Z}$. The object is the image of the generator, a single circuit of the hole about that pentagon, in the colourings of the link of $c$.

In the exhibit every far pentagon fails uniqueness on the link of its bridge, so the hole has no legal slide onto the defect. The short circuit $c\to m_3\to q_3\to m_4\to c$ is the walk killed in the computation above: colour $3$ is duplicated by the forced outer pair. The generator has no image in the determined slide graph. The representation of the subgroup that does lift is the identity.

The pentakis five-step walk would have been a nontrivial braid, and on the one outer colouring $(3,3,0)$ it even opens legal far-pentagon slides. It is invisible to the $15$-vertex colouring, so it is not a monodromy of the exhibit.

Separately, the rotational symmetry group of the icosahedron is $A_5$. A colour permutation would be an element of $S_4$. The only homomorphism $A_5\to S_4$ is the trivial one, since $A_5$ is simple and $60$ does not divide $24$. Geometric icosahedral monodromy therefore supplies no colour permutation, on this boundary or on any other.

### 4. Fundamental group of the one-hole configuration space

The configuration space of a single hole on the spherical triangulation is the sphere itself. Its fundamental group is trivial. The object would have been a colour permutation produced by that group.

A trivial group has only the identity representation, for every colouring. The group does not see $(0,1,0,2,3)$. This mapping is killed because its monodromy is invisible to the colouring. The permutations that do depend on the colouring live in the slide graph of §1, and there the representation is the identity for a different reason: the legal loops are contractible.

### 5. Descent against gauge

A returned tuple is a gauge when a global permutation of $\{0,1,2,3\}$ carries it onto $(0,1,0,2,3)$, and a descent when the return makes a far pentagon legal or drops the link to three colours so that $c$ extends. The object is that comparison for $\rho(c,\gamma)$.

The only determined return is $(0,1,0,2,3)$ itself, the trivial gauge. The two three-colour tuples produced by the illegal crossing at $q_3$ would have extended $c$ immediately. That reading reduces to the hole being extendible, and the extension is not a legal slide of this colouring. The mapping is killed.

The invisible pentakis return $(3,1,0,2,1)$ is not a gauge either: a global colour permutation preserves which bridges share the repeated colour, and here the repeated pair moves from $\{f_0,f_2\}$ to $\{f_1,f_4\}$. It remains a four-colour link. It is killed by invisibility, not by being a gauge.

## Conclusion

KILL ALL. The monodromy of the exhibit is the identity on $(0,1,0,2,3)$. The bridge $5$-cycle does not lift. The Klein sum around it is $0$ for every colouring. The braid generator about a far pentagon does not lift. The one-hole configuration space contributes only the identity, independently of the colouring. The only transports that would extend the centre, or that would move the repeated colour, use vertices the exhibit does not colour, or a crossing the forced outer pair forbids.

Feasibility that a monodromy of this colouring descends, or that it produces a gauge other than the identity: **Low**. The determined loops were enumerated by hand from the links above, and each returns the same tuple.

Next step: leave the $32$-vertex and $42$-vertex graphs uncoloured. A rank on the pair $(\text{hole},\text{colouring})$ has to read something other than the link permutation, which on this boundary is the identity. Walks that exit through $o_{35}$ or $o_{33}$ are not invariants of the exhibit.
