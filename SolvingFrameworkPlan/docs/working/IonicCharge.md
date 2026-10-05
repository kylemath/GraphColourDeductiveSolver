# Ionic charge on a colouring with a hole

4 October 2026. A model for the request that a neighbour pull a settled $(4,4,4,4)$ out of balance, accepting a 1 and a 3 so that two fours can be shared. Checked on the 21 published mass traps. Not a navigator status.

## The charge

A Kempe component on colours $A$ and $B$ is neutral when it contains equally many of each, and an ion otherwise. Write $n_A, n_B$ for those two counts. Swapping the component changes the global counts by

$$
(|A|, |B|) \mapsto (|A| - n_A + n_B,\; |B| - n_B + n_A).
$$

The sum $|A|+|B|$ is fixed. The difference changes by $2(n_B - n_A)$. A slide does not change any global count. So the only way to turn two fours into a 5 and a 3 is to swap an ion, for instance one with $(n_A, n_B) = (3,2)$ or $(1,0)$.

A neutral swap cannot change the global fours. It can still polarize the colouring: the two colours stay at 4 and 4, but a later component appears with counts $(1,2)$ or $(3,4)$. That is the neighbour effect. The fours are shared locally, one side accepting the 1, the other holding the 3, while the totals stay even.

## What the traps actually are

Order 17, sixteen coloured vertices. All fourteen stuck orbits have global counts $(4,4,4,4)$.

- Roots 9 and 14 already contain ions, with counts $(3,2)$ and $(1,2)$. One swap turns the global counts into $(3,4,4,5)$. That is the pull. It also raises $q$. The colouring becomes less neutral and more massive at the same time.
- Root 3 on graph 3, colouring 44, and its nine siblings, are globally neutral and every component is neutral. No single swap changes $(4,4,4,4)$. Six of the ten components, once swapped, do create ions. One such swap of a 2-vertex component leaves the totals at $(4,4,4,4)$ and produces components with counts $(0,1)$ and $(3,4)$. The 1 and the 3 have appeared, and the fours have been shared, without a change in the global charge.
- Roots 4 and 6, the locked pair, are neutral, and no one-step swap creates an ion. A neighbour attraction that needs a charged component has nothing to pull on, and one Kempe swap does not manufacture one.

Order 20, nineteen coloured vertices. All seven stuck orbits already have counts $(4,5,5,5)$, not $(4,4,4,4)$, and each already has three ions of charge 1. They are the charged side of the same ledger. The $G_8$ obstruction $(2,5,5,5)$ is one step further toward a depleted colour. The star swap there runs the arrow backwards, toward $(4,4,5,5)$.

## What an attraction would have to be

The Coulomb energy $\sum_c (|c|-4)^2$ is already 0 on every order-17 trap. Any swap that produces a global $(3,4,4,5)$ raises it. An attraction that pulls $(4,4,4,4)$ toward $(2,5,5,5)$ is climbing that energy. It cannot be the same potential that repairs $G_8$.

The local version does not climb. On colouring 44 the totals stay $(4,4,4,4)$ while a component of type $(1,2)$ is born. The attraction is between neighbours inside the component, not a change in the four global numbers. It is available on the open traps of graph 3 and absent on the locked roots 4 and 6.

Feasibility of a global ionic pull as the escape from $(4,4,4,4)$: **Low** on the locked roots 4 and 6, where one Kempe swap creates no ion. On graph 3 the polarized path is real. From colouring 44, a neutral swap of colours $(0,1)$ on $\{0,1,4,7\}$ stays at $(4,4,4,4)$, and the following ion swap of colours $(0,2)$ on $\{0,2,9\}$ lands on colouring 32 with counts $(3,4,4,5)$ and link $(0,2,0,3,1)$. One further swap, colours $(1,2)$ on $\{1,2,7\}$, fills. The same pattern holds on all ten sibling traps. The $q$ values along this path are $107$, then $138$, then $128$, then $116$ at the fill, so $q$ is not the descent. The note is `longtable/swarm/ion-second-swap.md`. Feasibility of this three-swap fill on graph 3: **High** as a description of these ten orbits, **Low** as a rank.
