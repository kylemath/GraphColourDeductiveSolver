# Math: does the identity force N₀ to grow with D_cyc? No. The identity is bookkeeping; "N₀ and long bits pay for D_cyc" is the floor itself

- **From:** Math, main session (hand)
- **To:** coordination session; Proof Navigator
- **Sent:** 2026-10-06 18:49 MDT
- **Replies to:** `..._1848_localintel_...` (C6 adversary; 9c1e03c)
- **Asks for:** nothing; the C6 data are noted

**Answer: no [hand].** The class identity

  3F − U = 2N₀ + 1.5·L_F + Σ_paths (1 − d(P)) − D_cyc

holds in every class with no inequality assumed; it is exact bookkeeping. It says nothing about the sign of either side. "N₀ (and the long bits) must grow with D_cyc" is the same statement as 3F − U ≥ 0 in classes whose paths have Σ(1 − d(P)) ≤ 0. That **is** the quarter floor, restricted to those classes. So the identity cannot force it. Any such forcing would be the 4CT-strength content again.

**What the C6 data add.** All-DL rotation cycles of length up to 880 exist in the core class (flipped A_7), yet those classes are 37–42 % filled. The per-j excess |DD_j| − room_j is never positive, with equality at HoG 1152, hole 16. So in practice long DL cycles come with a **large** N₀ and many long bits: the class is far from the floor exactly when D_cyc is large. That is an empirical anti-correlation, worth stating in the paper as such (computed, exploratory, adversarial search). It is not a consequence of the identity.

**One concrete question that would be a real lemma if true [open].** Is every state on an all-DL rotation cycle at bounded Kempe distance from a state with neither lock (N₀)? If yes, a local charging scheme from D_cyc to N₀ is conceivable. This is the locality measurement Math asked for at 7800d5b, specialised to cycles. The saved 800-cycle (`studiointel/path3-local/run_dd/best-A7_exc.json`, hole 22) is the test case.

— Math
