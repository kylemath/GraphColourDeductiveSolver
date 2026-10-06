# Tilley separability at degree-5 apex fans

Long Table (Creative Intel), 5 October 2026, 18:08 MDT. A conjecture page with an exploratory reading. The first conjecture, TS, turned out to be the known refuted item 13 (U at every pair). Nothing here is proved except the bridge in §1. Literature: `literature-check.md`.

## 1. The bridge [hand]

Let $x$ have degree $5$ with link $(y,a,s,t,b)$, and let the apex-$y$ fan $\tau_y=\{ys,yt\}$ be legal. Then $T^\ast_{\tau_y}=T/xy$. So the starts $S(x,\tau_y)$ are the colourings of $G=T-xy$ with $c(x)=c(y)$, read with $x$ uncoloured. A colouring with $c(x)\ne c(y)$ is proper on $T$, so its link at $x$ misses $c(x)$. Any Kempe change on $G$ becomes one or more successive pure swaps at the hole $x$:
- a change whose component avoids $x$ is the same swap;
- a change through $x$ splits, once $x$ is deleted, into components of $(T-x)[a,b]$, which are swapped one after another (containment Lemma 3.1).

**So a start that Kempe changes on $G$ can move to $c(x)\ne c(y)$ has a pure fill at $x$.** Call such a start **Tilley-separable**.

**Locking.** A start is not separable exactly when its whole $G$-Kempe class keeps $c(x)=c(y)$. Equivalently, every colouring in the class has the three chains $\{1,2\},\{1,3\},\{1,4\}$ joining $x$ to $y$, where $c(x)=c(y)=1$. This is Tilley's lock, read one colouring class at a time. Tilley calls $T$ Kempe-locked at $xy$ when **every** class is locked, and proves that a minimum counterexample is Kempe-locked at every edge.

## 2. Conjectures

Every fan at a degree-5 vertex is an apex fan, because its apex is a neighbour. So "every apex pair" means every pair.

> **TS (every pair). REFUTED** [computed, exploratory]. It fails at $10$ pairs of $17{:}0$ and $22$ pairs of $17{:}1$, in `plantri -m5` order. These are **exactly the pairs where U fails** in `swarm/vh-exists-check.txt` (item 13 of `vh-exists.md`, already refuted at $41$ pairs on $17{:}0$, $17{:}1$, $20{:}12$ and $20{:}24$). **TS is U at every pair, stated in Tilley's language.** It is not new.

> **TS∃ (open).** Every minimum-degree-5 triangulation has an edge $xy$ at a degree-5 vertex $x$, with legal apex fan, such that **no** Kempe class of $T/xy$ is locked in $T-xy$. TS∃ implies pure VH at that pair, and so VH∃.

On the order-17 data, per-pair Tilley separability and U coincide pair for pair. A hand proof of the equivalence is not written. The two differ in principle: Kempe classes of $T/xy$ against classes in $T-xy$, and "unlocked member" against "reaches separation". I would expect it to reduce to Lemma 3.1 together with the merge at the contracted vertex.

**Tilley's frame.** His theorem says a minimum counterexample has **every** class locked at **every** edge. TS∃ asks for **one** edge at a degree-5 vertex with **no** class locked. The whole question is the gap between these. Tilley's data (no 5-connected locked triangulation to order $24$; every locked one contains a Birkhoff diamond) is about entire edges being locked, so it is weaker than what TS∃ needs.

## 3. Exploratory reading [computed, post hoc, undeclared]

Code: `longtable/explore-vhphi/tilley_apex.py`. All legal apex pairs at degree-5 vertices.

| Family | Orders | Apex pairs | Pairs with a locked start |
|---|---|---|---|
| `plantri -m5` (minimum degree 5) | 12, 14, 15, 16 | 370 | 0 |
| `plantri -c4m4` (4-connected, degree 4 allowed) | 10–14 | 35,710 | 1 |

The single locked pair is $14{:}5$ in `-c4m4` order, with $x=12$ and $y=7$ ($\deg y=7$); $6$ of its $8$ starts are locked.
- $x$ has **two degree-4 neighbours**, so the graph is outside the minimum-degree-5 class.
- Every fan at $x$ is still pure-good, by Math's degree-4-neighbour lemma. The richer moves at the hole succeed where Tilley's Kempe changes do not.
- $y$ lies on the rings of six Birkhoff diamonds.

Orders 17–18 of `-m5`, and order 15 of `-c4m4`: see §5.

## 4. What would make TS a proof route

- **A hand proof of TS∃.** This is the Wernicke situation, now with a precise classical statement: three $\{1,k\}$-chains from $x$ to $y$ in $T-xy$, for every colouring in a Kempe class.
- **The Heawood check.** In Heawood's 1890 example, Kempe's two simultaneous swaps fail. The question is whether the class is TS-locked, or only that particular two-swap argument fails. Per-class locks at degree-5 endpoints do occur in minimum degree $5$: $17{:}0$ and $17{:}1$, §5. So TS∃, not TS, is the target. The locked classes on $17{:}1$ are natural objects to study by hand.
- **Adversarial fixtures (needs a WP).** Tilley's locked triangulations, Birkhoff diamonds with $x$ a diamond vertex, and graphs with degree-5 $x$ next to degree-$\ge7$ $y$.

## 5. Larger orders [computed, exploratory]

| Family | Order | Apex pairs | Pairs with a locked start |
|---|---|---|---|
| `-m5` | 17 | 245 | 32 (17:0 has 10, 17:1 has 22; 192 locked starts), matching U |
| `-m5` | 18 | 780 | 0 |
| `-c4m4` | 15 | 133,270 | 2 |

**Reading.** Per-pair separability is false in general and rare. Every graph tested still has separable pairs. That is the known U∃ evidence, now in Tilley's vocabulary.

**What this means for the brainstorm.** The diamond-lemma test did not isolate the Birkhoff diamond. The loose "diamond-near" flag is set on most pairs: $680$ of $780$ at order $18$. A sharper test would match Tilley's exact $K_{xy}$ (the diamond with $x,y$ as its specified endpoints), which needs his figure.

## 6. Structure of the locks on $17{:}0$ and $17{:}1$ (18:10, exploratory, post hoc)

- **No radius-1 degree signature separates locked pairs from separable ones.** The signature is (degree of $y$, number of degree-6 neighbours of $x$, degrees of the two chord ends). Every signature that occurs locked also occurs separable. The locks are not determined by local degrees, so a Wernicke-style lemma must use information beyond radius $1$.
- **Every degree-5 vertex keeps a fully separable fan.**
  - $17{:}0$: vertices $2,8,9,14,15,16$ have all fans separable, vertices $0,1,4,6,11,12$ are mixed, and none has all fans locked.
  - $17{:}1$: vertices $7,13$ have all fans separable, the other ten are mixed, and none has all fans locked.
  - At every other `-m5` order $\le18$ there are no locks at all.

> **TS$_v$ (post hoc, open).** In a minimum-degree-5 triangulation, every degree-5 vertex $x$ has a neighbour $y$ with legal apex fan such that no Kempe class of $T/xy$ is locked in $T-xy$.

TS$_v$ sits between TS (refuted) and TS∃ (open, equivalent on the data to U∃). It implies that every degree-5 vertex carries a pure-good pair. Tilley's theorem puts every edge of a minimum counterexample under a whole-edge lock. TS$_v$ says that, class by class, every degree-5 vertex has an incident edge that escapes. It was formulated after the data, so a fair test needs a declaration and fresh orders.

## 7. How the locks are escaped (18:41, exploratory, post hoc, undeclared)

Code: `longtable/explore-vhphi/` — `lock_anatomy.py`, `lock_escape.py`, `fan_switch.py`, `sep_any.py`, `sep_depth.py`. Orders $\le18$ for `-m5`, $10$–$14$ for `-c4m4`.

**Anatomy of a lock (17:1, $22$ pairs).** Each locked pair has exactly **one** locked class, of size $6$. Its three bichromatic chains $\{1,k\}$ through $x$ and $y$ are the same connected sets (size $9$ in most cases; two pairs, $(x,y)=(10,15)$ and $(15,10)$, have a size-$7$ chain). **Every locked class still has a pure fill at the hole $x$**, reached by swaps in $T-x$ that Tilley's changes in $T-xy$ cannot make.

**The escape always leaves $S$ through exactly one chord.** On $17{:}0$ ($10$ locked classes) and $17{:}1$ ($22$), the shortest pure escape takes $2$ swaps for $24$ classes and $3$ swaps for $8$, and **the first swap always makes exactly one fan chord monochromatic**, never both and never none. This is the observation recorded in `vh-exists.md` ("every path to $F$ must break a chord"), now with a count.

**Fan switching.** After the first swap, the state is admitted by exactly $3$ fans. This is automatic: an unfilled link has pattern $(2,1,1,1)$, and each singleton colour picks one fan. In $32$ of $32$ locked classes it is **separable for at least two of those three fans** ($27$ for all three).

**SEP (the fan-free statement).** *Every unfilled state at a degree-5 hole is Tilley-separable for at least one of its admitting fans.*
- Holds with **no exception** on: all `-m5` triangulations of orders $12,14,15,16,18$ ($9{,}568$ states), and all `-c4m4` triangulations of orders $10$–$14$ ($173{,}000$ states).
- **Fails only on $17{:}0$ and $17{:}1$**: $8$ states at $4$ vertices (two states each at $17{:}0$ vertices $4$ and $6$ and $17{:}1$ vertices $5$ and $15$), locked for all three admitting fans.
- **Every one of those $8$ has separation depth exactly $1$.** One pure swap at the hole reaches a state separable for some admitting fan.

**D1 (conjecture, post hoc).** *Every unfilled state at a degree-5 hole is separable for some admitting fan, or is one pure Kempe swap away from such a state.* True on all data above, hence a state-level, fan-free refinement of U∃. By the bridge in §1, D1 implies a pure fill at every degree-5 hole for every deletion colouring, with the sequence "one swap, then a Tilley sequence in the contraction $T/xy_j$, then fill". That is the strong pure form at degree-5 holes, which `vh-exists-check.txt` already reports as `deg5_KD_bad=0`. D1 explains it in terms of a statement about contractions.

**What this does and does not buy.**
- It localises the whole difficulty. A hand proof of D1 would need to show that no state is locked for all three admitting fans **and** all of its one-swap neighbours. The observed exceptions are all at $17{:}0$ and $17{:}1$, the two graphs that already carry every U failure, and nothing in the data says they are sporadic.
- It is stated for deletion states of $T$ alone, not for the induced $T^\ast$ starts that the induction supplies. The two coincide, because the starts of fan $j$ are exactly the colourings admitted by $\tau_j$.
- It uses only pure swaps at a fixed degree-5 hole. Slides, mobility and the protected face play no part, so it complements Math's route and does not depend on it.
- It was formulated after the data. A fair test needs a declaration and fresh orders. It is **not** evidence.

**Next (Long Table).**
1. Hand-analyse one doubly-locked state at $17{:}1$ vertex $5$: write out its link word, the three admitting fans, the three chain systems, and the swap that escapes. That is the smallest concrete object a proof of D1 must handle.
2. Test D1 on `-c4m4` order $15$ and on rare 4-connected shapes, to see whether depth $1$ survives.
