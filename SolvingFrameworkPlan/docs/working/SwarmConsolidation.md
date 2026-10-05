# Where the math and creative inquiries stopped

4 October 2026. Both inquiries ran out of usage with the same picture and three unfinished checks. Nothing here is a navigator status.

## Killed

**Slide-only completion.** A singleton slide preserves the sorted colour counts on the coloured vertices. Order 18 graph 10, Florek's two-pole graph \(G_8\), has 16 deletion starts whose slide component has 32 states and population \((2,5,5,5)\). Every full four-colouring of that graph has population \((4,4,5,5)\). No slide path can fill them. This is a kill of slides alone, not of slides plus a Kempe swap.

**Slides as an all-roots mass proof.** On the 21 published mass traps, forbidding landings on a mass-passing root leaves a dead end. The only stuck-to-stuck slide is order 17 graph 0, roots 9 and 14, and they exchange traps. The other 19 traps have no failing-root exit.

**Slow mass continuation after a landing.** The smallest-index rule reaches a fill in at most 3 macros. The slowest greedy rule, on order 20 graph 7 root 7 orbit 180, takes a second swap that leaves a state which the first swap had already filled, and it revisits a colouring. An unguided two-swap macro is not a progress rule.

**The isolated pentagon does not force an exit.** On the 15-vertex star of either symmetric graph there is a proper colouring of the patch minus the centre, boundary pattern \(2,1,1,1\), for which every second slide onto a far pentagon is illegal. A slightly larger patch sends every remaining forward slide onto another locked pentagon. The colourings are in `backgroundMaterial/planemap-structural/longtable/swarm/isolated-local.md`. The full 32- and 42-vertex graphs were not coloured.

**Kempe preparation is not the two-step slide.** On all four locked traps the landing orbits are disjoint, and both routes still descend:

| Graph | Forward roots | Prepared roots |
|---|---|---|
| 17:0 root 4 | 1, 2, 12, 16 | 0, 11 |
| 17:0 root 6 | 0, 2, 11, 16 | 1, 12 |
| 20:7 root 7 | 0, 13 | 8, 15 |
| 20:7 root 11 | 9, 19 | 4, 12 |

No prepared landing is mass-stuck. All eight prepared slides descend in one mass swap at a passing root. The routes are not the same orbit, but each long-arc pair differs by one Kempe chain: swapping that chain and sliding onto its degree-five neighbour, or walking the vacancy two steps through the singleton, produces two colourings that agree except on that chain with the neighbour removed. The short-arc vertex sits outside the pairing. The certificate is `backgroundMaterial/planemap-structural/longtable/swarm/kempe-vs-twostep.md`. **No scored rank gets past the next colouring.** On the 21 traps, $q$, $(p,q)$, $(n_5,q)$, $(d_{\min},q)$, $\mathrm{repMass}$, and $(L,q)$ already fail to fall. $(\mathrm{shortLinks}, q)$ and $(H, q)$ fall on all 21 and refuse the $9 \leftrightarrow 14$ exchange, then stop: the first at order 17 graph 3, degree-6 vertex 11, on $(0, 96)$; the second on the first landing, root 0 colouring 37, at $(0, 111)$. Details are in `backgroundMaterial/planemap-structural/longtable/swarm/rank-kill.md`. The order-17 traps have colour counts $(4,4,4,4)$. The order-20 traps have $(4,5,5,5)$. A slide changes neither. An ionic reading of the same orbits is in `IonicCharge.md`.

## Proved as hand arguments, not yet the theorem

The equal-pole star swap: if the two poles of the antiprism suspension have the same colour, one explicit Kempe swap on the other pole's star makes a belt vacancy fillable, for every ring length. At \(n=8\) this is exactly the population repair \((2,5,5,5)\to(4,4,5,5)\). Differently coloured poles are outside the proof.

A degree-5, 6, or 7 non-target hole always has a legal slide. That does not prevent cycles. \(K_5\) with a hole has legal slides forever and no four-colouring, so any proof must use the sphere.

On a targetless slide component in a graph of maximum degree 6, the vertices that occur as holes induce a cycle. That lemma does not explain order 18 graph 10. There the hole set of the population-$(2,5,5,5)$ component is all 18 vertices, including both degree-8 poles, and it closes at 32 states. Every belt state in it has equal pole colours, and the star swap fills it. A slide onto a pole keeps the bad population.

Vacancy slides and a conditional rank-portfolio contact are reported compiled in an 83-module audit. Universal descent is not.

## Still open, and what the next swarm is for

1. Differently coloured poles on the same belt. The star proof stops there.
2. A hybrid kill: one slide component on which every single Kempe swap leads only to another targetless slide component. All 16 known population failures unlock with one swap, so this witness is not in that list.
3. A rank on the actual pair \((\text{hole}, \text{colouring})\) that falls when the star swap changes the population, and that does not consult a pass/fail label.
4. The support of the 32-state component: which vertices are holes, and whether both poles are among them.

Feasibility of the hybrid "slides, at most one Kempe swap, slides, fill" as a universal claim: **killed**. The same 21-vertex hole kills "at most two Kempe swaps": 172 of 224 ordered pairs stay frozen. A third swap unlocks the link on the 148 pairs that leave the original colouring, and on 84 of those the new hole still sees four colours. Orders 12 through 20 still unlock with one swap. Feasibility of the equal-pole star as a lemma: **High**. On $G_5-u_0$ and $G_8-u_0$, unequal poles fill by slides alone (19 of 19, and 121 of 121). Feasibility of that pattern for every $n$: **Medium**. It holds for $n=5$, $8$, and $11$ (807 unequal orbits, longest walk 6). The $A_\tau$ tile, the surviving $B$ orientation, and the cap are hand arguments. The gap $0,\rho,\tau,0$ is not a colouring. The remaining unnamed slides are the $A_\rho$ tile whose outer $u$-vertex has colour $\tau$.
