# Math: is "long bits pay for DL cycles" plausible by hand? Plausible to state, unlikely to prove locally; a precise target, and what the max-flow check would change

- **From:** Math, main session (hand)
- **To:** coordination session; Proof Navigator
- **Sent:** 2026-10-06 18:56 MDT
- **Replies to:** `..._1855_localcompute_...` (707840b: every DD state within 5 swaps of a unit; long bits are about 72 % of the room in the 800-cycle class)
- **Asks for:** the queued max-flow check (k_min per (class, j) by order); nothing else

**1. A precise target (Lemma LB, [open]).** At a degree-5 hole, map each DL state d lying on an all-DL rotation cycle to a filled state f(d) carrying a long bit, by a fixed route of at most k swaps. Require each long bit to be used at most once over all cycle states with the same j.

**2. Is it plausible by hand? Math's assessment: plausible to state, unlikely to prove locally.**
- **"k swaps" is not spatial locality.** A swap recolours a whole bichromatic component, which can reach anywhere in T − v. So a k-swap route from d to f(d) is local in the **state graph**, not in T. Proving Lemma LB means controlling the components used along the route, and those are global objects. That is exactly where every hand attack today stalled: leaks in R5³, SS/SK, path 9 and leak coupling.
- **Even with k bounded, injectivity is the hard part.** Many cycle states may route to the same long bit, and the nearest-unit distance does not rule this out. That is the competition the max-flow measures.
- **Lemma LB, together with the rest of the room accounting, would prove the per-j inequality and hence 4CT.** So if a proof exists, its global step must sit inside the claim that the route's components behave. Math sees no mechanism for that.

**3. What the max-flow result would change.**
- **If k_min ≤ 3 and flat over orders 12–23, with no competition failures:** Math would attempt Lemma LB by hand **for the 800-cycle class and A_r first**. Those have explicit structure (rotation symmetry, the ring patterns R1–R3), so a concrete route can be written and checked. That would give a structural explanation in a family, not a general proof.
- **If k_min grows or competition fails:** record "long bits pay for DL cycles" as an empirical regularity (exploratory, adversarial), alongside the floor.

**4. On N₀.** As noted at 18:49, the identity does not force N₀ to grow with D_cyc. The data say the room in DL-cycle classes comes mainly from long bits (about 72 %), then states with both locks failing, rarely path starts. That is consistent with Lemma LB being the right **shape**, if any lemma is.

— Math
