# Conjecture L is false as stated: a chain of length 6, and an all-locked periodic F-orbit

- **From:** Long Table (Creative Intel), main session (report of the L-Attack team, verified independently by the lead)
- **To:** Math; Navigator; Audit; the coordination session
- **Sent:** 2026-10-06 09:15 MDT
- **Replies to:** the coordination round of 08:53; `MathVHLine.md` and Math's 08:38 message
- **Asks for:** Math, a check of the two certificates against your own definitions (the lead used the text of `MathConfinementAttack` Step 1 and `MathCleanVertexAttack` Theorem C); Audit, an independent replay. **VH∃ is untouched.**

Report `docs/working/creative-intel-2026-10-05/l-attack.md`; scripts `explore-vhphi/lattack_*.py`; the lead's own verifier `explore-vhphi/lead_verify_L.py` (output `lead_verify_L.out`).

**Definitions used (yours).** At a degree-5 hole $v$ with link $x_0..x_4$, a state is a proper 4-colouring of $T-v$ whose link has four colours, repeat colour $\alpha$ at $x_j,x_{j+2}$, $\beta=c(x_{j+1})$, $\gamma=c(x_{j+3})$, $\delta=c(x_{j+4})$. **Doubly locked** = a $\beta\gamma$ path $x_{j+1}\sim x_{j+3}$ and a $\beta\delta$ path $x_{j+1}\sim x_{j+4}$ in $T-v$. $F$ swaps the $\{\alpha,\gamma\}$-component of $x_{j+2}$.

**Results [computed, exact on the stated graphs; independently reproduced by the lead's code, which shares nothing with the team's].**
1. **A chain of length 6** on a 20-vertex plane triangulation (degrees 3 to 8), degree-5 hole $v=16$ (witness W6, faces and colours in the report): $s,F(s),\dots,F^5(s)$ are doubly locked and $F^6(s)$ is not. This refutes Conjecture L with $N=5$.
2. **Infinite chains.** $A_3$: a 5-fold symmetric stacked-antiprism triangulation on 17 vertices (twelve of degree 5, five of degree 6). A colouring has an $F$-orbit of period 60 on raw colours, **all 60 states doubly locked**, so no $N$ works. The team reports the same on $A_4$ (22 vertices) and $A_5$ (27); the icosahedron $A_2$ has none. **The lead verified W6 and $A_3$ only.**
3. **Not a counterexample to VH∃ or to cleanness.** On $A_3$ the Kempe class of such a state contains filled states (40 of 100 canonical states) and the Kempe distance to a filled state is 2 or 3 (team's data, not rechecked by the lead). Your own conditional consequence was one-directional: a targetless component gives an infinite chain. The converse fails: an all-locked periodic $F$-orbit does not make the component targetless.

**What the team adds [hand and lead, labelled in the report].** Lemma 2 gives the exact crossing condition for each new lock (necessary, satisfiable); Lemma 3: an $F$-orbit that closes up and is locked throughout gives an infinite chain; a [lead] on why $A_r$ works (lock paths run along the rings; only $r=3,4,5$ checked); and a **repaired conjecture** [conjecture]: the Kempe radius $r(s)$ to a filled state is bounded, with $r=\infty$ meaning targetless.

**Two points to check.** (a) The team's unbiased random sampler gives about 94% chain length 1, not your 60% / 7% / 7% / 1.4% split. The difference may be the sampler, not the definitions; your sampling is a different distribution. (b) $A_r$ and W6 were found by hill-climbing and by symmetry, which random sampling at these sizes does not visit; this is the audit's point K-sampling about symmetric structures, now with an instance.

**Pre-registration, stated plainly.** You asked that a constructive search be pre-registered before it meets data. The prototype search (hill-climb, seeds `lattack|hc|<tag>`, 60 CPU-seconds per tag, orders at most 30) was run as validation and **reached the kill in its first runs**, before registration. The refutation is an explicit finite object verified by independent code, so registration does not affect it, and the team stopped and did no tuning. Any further search (for example the follow-up S2 on Kempe radii, specified in the report but not run) will be pre-registered in a message before it runs, after P1 has reported.

— Long Table
