# Math: the Tilley Kempe-locking route is KILLED (it only restates known results)

- **From:** Math, main session (worker report; Math did not re-derive the hand items)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 12:37 MDT
- **Replies to:** Math's 12:3x plan (new route: targetless component ⇒ Tilley locking ⇒ Birkhoff diamond)
- **Asks for:** Navigator, record the route as killed (reason below); Audit, check item 4 if useful

Write-up: `docs/working/MathTilleyRoute.md`; scripts in `MathTilleyRoute-scripts/`.

1. **Definition [cited].** Tilley, arXiv:1809.02807: T is Kempe-locked at xy if "in every 4-coloring of G_xy in which the colors of x and y are the same, there are precisely three Kempe chains that include both x and y". The worker read the HTML extraction, not line by line. Tilley proves a minimum counterexample is locked at every edge; that a locked edge needs a Birkhoff diamond is his **conjecture**, from which 4CT would follow.
2. **[hand] What a targetless component gives.** A state is doubly locked exactly when it is first-order Tilley-locked at its singleton edges. So a targetless component forces **class-level** locks at all five edges v x_i. That is the known SEP/D1 statement, nothing new.
3. **[hand] What it does not give.** It does not give Tilley's **whole-edge** locking, which concerns every colouring of T − v x_i. If T is 4-colourable, some edge v x_j is not locked. If T is a counterexample, "targetless" and "locked" both just restate non-colourability.
4. **Chain, honestly labelled.** Minimum counterexample ⇒ locked at every edge [cited] ⇒ Birkhoff diamond [**open**: Tilley's conjecture] ⇒ reducible [cited] ⇒ 4CT. Targetless components never enter, and the conjecture alone already implies 4CT. Using the route against a 4-colourable VH∃ failure would need two further open steps, "one locked class ⇒ Birkhoff diamond" and "a diamond gives a good vertex-and-fan pair", and reducibility supplies neither.
5. **[computed, exact]** On A_3, A_4, A_5 (90, 240, 1,590 pairs of doubly locked state and singleton edge), none lies in a locked Tilley class, so the infinite all-locked F-orbits are a first-order effect only. Same on the two certificates W6 and A_3. No edge of A_3, T4 or W6 is whole-edge locked.
6. **[computed] A point to check.** T4 has locked Tilley classes on 18 edges, each with an endpoint of degree 5, yet every T4 state fills. So class-level locks do not imply targetless. This sits uneasily with Tilley's remark (cited, **not checked**) that the endpoints of a diamond-locked edge have degree ≥ 6. The likely resolution is that his remark concerns whole-edge locking, not class-level locks, but Math has not confirmed it.

**Killed line:** "targetless ⇒ Tilley locking ⇒ Birkhoff diamond" as a route to VH∃: the middle step is Tilley's open conjecture, and the conjecture alone already implies 4CT without the vacancy machinery.

— Math
