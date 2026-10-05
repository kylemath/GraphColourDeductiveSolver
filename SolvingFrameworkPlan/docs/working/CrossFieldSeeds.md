# Barriers, and the fields the next swarm is reading them as

4 October 2026. The barriers below are the ones the sweeps actually hit. Each seed is a foreign technique aimed at one barrier. A mapping is useful only if it names an object we can define on $(hole, colouring)$ and a computation that would kill it.

## The barriers

1. **A conserved charge.** A singleton slide preserves the sorted colour counts. On $G_8$ the charge $(2,5,5,5)$ cannot be filled, because every full colouring has counts $(4,4,5,5)$ (Florek, Lemmas 2.2–2.3). The star swap is the move that changes the charge.

2. **Reversible moves, no Lyapunov function.** Slides undo themselves. The pairs $(f,q)$ that fall on all 21 mass traps die on the next colouring of order 17 graph 3. $(H,q)$ stops at $(0,111)$.

3. **The one-hole restriction.** Meyniel's theorem and the polynomial 5-colour bound allow many vertices of a fifth colour. A vacancy slide keeps exactly one. Single-vertex recolouring can freeze a colouring that larger Kempe chains still connect (Ito–Iwamasa–Kobayashi–Maezawa–Nozaki–Okamoto–Ozeki, arXiv:2210.17105). $K_5$ with a hole has legal slides and no 4-colouring.

4. **A local colouring with no forward exit.** On the 15-vertex pentagon star, a proper colouring makes every second slide onto a far pentagon illegal. Geometry does not force the bridge.

5. **Equal poles need the star. Unequal poles, on $G_5$ and $G_8$, do not.** Every unequal-pole colouring of $G_n-u_0$ for those two $n$ fills by slides alone. The star swap is the equal-pole tool. Florek's Theorem 3.1 still moves a hole that is already a pole, and does not start from a belt vertex. A proof for every $n$ is open.

6. **Many Kempe classes.** $G_n$ has at least $\lfloor n/6 \rfloor$ classes, and $2n$ constant colourings when $n \equiv 2 \pmod 3$. Existence of a colouring is not a path to one prescribed colouring.

## Seeds

The swarm is one agent per seed. High temperature means a risky identification is allowed. Each agent has to say how that identification dies.

| Seed | Barrier it is aimed at |
|---|---|
| Height functions, dimers, Potts | charge, and the pentagon monodromy. Killed: the Conway–Lagarias height is the sorted colour count, frozen at $(4,4,4,4)$ on colouring 44, and the other four heights are either colour-blind, undefined off the Eulerian case, or already zero on a non-target state. |
| Chip-firing and sandpiles | the star swap as a firing. Killed: the swap changes the degree of the colour-label divisor by $-6$, so it is not a firing, and the sandpile group does not see the charge. |
| Lyapunov certificates | a rank that is not another $(f,q)$ |
| Covering spaces and monodromy | the vacancy walking around a pentagon. Killed on the exhibit link $(0,1,0,2,3)$: every closed walk the colouring allows is an out-and-back, and the monodromy is the identity. |
| Nowhere-zero flows | the classical equivalent of the theorem, read against the charge |
| Rewriting and confluence | the 9–14 exchange and the greedy walk that leaves a filled state |
