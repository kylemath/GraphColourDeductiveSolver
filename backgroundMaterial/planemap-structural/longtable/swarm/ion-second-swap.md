# Second swap of an ion

4 October 2026. Counted with `mass_core.RootState` on the published two-swap-stuck orbits. A component is neutral when its two colours occur equally often, and an ion otherwise. The script is `swarm/ion_second_swap.py`.

**OPEN.** The witness is order 17, graph 3, root 3, colouring 32. It is reached from colouring 44 by a neutral swap and then one ion swap. `descent(32, 2)` returns `None`: swapping colours $(1,2)$ on $\{1,2,7\}$ fills the link.

## The count

Order 17, graph 3, root 3. The link is $(0,2,9,10,4)$, every vertex of degree 5. Colouring 44, in vertex order $(0,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16)$, is

$$(0,1,2,1,3,2,0,3,1,3,2,0,3,2,0,1).$$

The population is $(4,4,4,4)$, the link colours are $(0,2,1,3,1)$, so the multiplicities are $(2,1,1,1)$, and $p=1$, $q=107$, $R=1842$. The state is two-swap stuck: `descent(44, 2)` returns a witness. All ten bichromatic components are neutral, so one swap keeps the population at $(4,4,4,4)$.

Six of the ten components create ions. The other four do not, so they have no ion to swap: colours $(0,3)$ on the whole class and colours $(2,3)$ on the whole class both return to 44, and the two components of colours $(1,3)$ both land on colouring 43, still ion-free, at $q=115$.

| First colours | Component | Image | $q$ | Ions created |
| --- | --- | ---: | ---: | --- |
| $(0,2)$ | $\{0,2\}$ | 37 | 131 | $(0,1)$, $(0,1)$, $(3,4)$, $(3,4)$ |
| $(0,2)$ | $\{6,7,11,12,14,15\}$ | 37 | 131 | same |
| $(0,1)$ | $\{0,1,4,7\}$ | 42 | 138 | $(1,2)$, $(2,3)$ |
| $(0,1)$ | $\{9,12,15,16\}$ | 42 | 138 | same |
| $(1,2)$ | $\{1,2,6,9\}$ | 75 | 138 | $(1,2)$, $(2,3)$ |
| $(1,2)$ | $\{4,11,14,16\}$ | 75 | 138 | same |

The swap of colours $(0,2)$ on the 2-vertex component is the one recorded in `SolvingFrameworkPlan/docs/working/IonicCharge.md`. The image is colouring 37, population still $(4,4,4,4)$, link still $(0,2,1,3,1)$. Its ions are colours $(0,1)$ with counts $(4,3)$ on $\{0,1,4,6,11,14,16\}$ and $(0,1)$ on $\{9\}$, and colours $(1,2)$ with counts $(3,4)$ on $\{1,2,7,9,12,15,16\}$ and $(1,0)$ on $\{4\}$.

## The sixteen second swaps

Each ion of each image was swapped once. Complements canonicalise together, so the sixteen swaps land on four colourings. Every landing has sorted population $(3,4,4,5)$ and link multiplicities $(2,1,1,1)$. The link keeps four colours. It keeps a colour of multiplicity one; that multiplicity was already present on colouring 44. No landing drops to three colours, so none of these swaps fills. Against $q=107$, every landing raises $q$. Against the ion colouring, $q$ falls on the two landings at 128 and rises on the two at 146.

| Ion swapped | Landing | Population | Link colours | $q$ | `descent` | One-step fill |
| --- | ---: | --- | --- | ---: | --- | --- |
| $(0,2)$ counts $(2,1)$ on $\{0,2,9\}$, from 42 | 32 | $(5,4,3,4)$ | $(0,2,0,3,1)$ | 128 | `None` | $(1,2)$ on $\{1,2,7\}$ to 62, $q=116$ |
| $(0,2)$ counts $(1,2)$ on $\{0,2,4\}$, from 75 | 70 | $(3,4,5,4)$ | $(0,2,1,3,2)$ | 128 | `None` | $(0,1)$ on $\{0,1,6\}$ to 62, $q=116$ |
| $(0,1)$ counts $(0,1)$ on $\{9\}$, from 37 | 35 | $(5,3,4,4)$ | $(0,2,0,3,1)$ | 146 | `None` | $(1,2)$ on $\{4\}$ to 62, $q=116$ |
| $(1,2)$ counts $(3,4)$ on $\{1,2,7,9,12,15,16\}$, from 37 | 68 | $(4,3,5,4)$ | $(0,2,1,3,2)$ | 146 | `None` | $(0,1)$ on $\{9\}$ to 62, $q=116$ |

Each row is reached by four of the sixteen swaps. Populations are the raw colour counts in order $(|0|,|1|,|2|,|3|)$; each sorts to $(3,4,4,5)$. Colourings are the canonical representatives.

The witness path is the first row. From colouring 44, swap colours $(0,1)$ on $\{0,1,4,7\}$. The canonical image is colouring 42,

$$(0,1,2,1,3,2,0,3,0,3,2,1,3,2,1,0),$$

with $q=138$ and ions of colours $(0,2)$: counts $(2,1)$ on $\{0,2,9\}$ and $(2,3)$ on $\{6,7,11,14,16\}$. Swap the first of those. The canonical image is colouring 32,

$$(0,1,2,1,3,0,2,3,0,3,0,1,3,0,1,2),$$

with population $(5,4,3,4)$, link $(0,2,0,3,1)$, $p=1$, $q=128$, $R=1863$. Then swap colours $(1,2)$ on $\{1,2,7\}$. The image is colouring 62, $p=0$, $q=116$, link colours $(0,2,0,3,2)$. That is a fill, and it is why `descent(32, 2)` returns `None`. The same holds for 35, 68 and 70: each has a one-step Kempe swap to $p=0$, and none of those four meets the stuck set in one swap.

`descent(44, 2)` still returns a witness. Colouring 42 has $R=1873$ and colouring 32 has $R=1863$, both above the trap's $1842$. The fill is a third Kempe swap.

## The same pattern on the ten orbits

The first-swap signature of colouring 44 is uniform across the ten stuck orbits. Each has ten neutral components and population $(4,4,4,4)$. Six components create ions, with the same sorted count-pairs, the same link multiplicities $(2,1,1,1)$, and image $q\in\{131,138\}$. The second swaps were therefore run for root 3 colourings 47, 77, 91 and 93, and for root 13 colourings 19, 29, 52, 76 and 96.

Each of the ten gives sixteen ion swaps, four landings, sorted population $(3,4,4,5)$, link multiplicities $(2,1,1,1)$, two landings at $q=128$ and two at $q=146$. Every landing has `descent` returning `None` and a one-step swap to $p=0$.

| Root | Colouring | Landings ($q=128$, $q=146$) |
| ---: | ---: | --- |
| 3 | 44 | 32, 70 and 35, 68 |
| 3 | 47 | 3, 33 and 8, 22 |
| 3 | 77 | 18, 21 and 46, 95 |
| 3 | 91 | 12, 85 and 13, 16 |
| 3 | 93 | 69, 78 and 53, 84 |
| 13 | 19 | 13, 20 and 1, 14 |
| 13 | 29 | 4, 22 and 25, 32 |
| 13 | 52 | 61, 63 and 53, 64 |
| 13 | 76 | 73, 94 and 72, 77 |
| 13 | 96 | 69, 91 and 84, 88 |

## Locked roots

Order 17, graph 0, root 4 state 25 and root 6 state 27 were recomputed. Both are stuck, both have population $(4,4,4,4)$ and $q=143$, and both have nine components, all neutral. No one-step image contains an ion. The ionic pull has no first step on these two traps.

## Feasibility and next step

Feasibility that an ion swap on these ten orbits reaches a colouring with a one-step fill: **High**. The forty landings above all do. Feasibility that the same swap fills the link or lowers $q$ below the trap: **Low**, on colouring 44, where every landing has $q\in\{128,146\}$ and four link colours. Feasibility on the locked roots: **Low**, because no swap creates an ion.

Next step: the fill from colouring 32 is the third Kempe swap, outside the two-swap macro. Name a rank that may rise once along an ion and then accepts the fill, and test it on a trap whose one-swap neighbourhood does not already contain $p=0$.
