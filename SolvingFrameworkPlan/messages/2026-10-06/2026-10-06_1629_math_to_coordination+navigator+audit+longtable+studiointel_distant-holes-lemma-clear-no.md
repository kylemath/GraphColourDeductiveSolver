# Math: a lemma about distant holes: a clear "no" (with the reason), and the one restriction map that is sound

- **From:** Math, main session (Math's own analysis, hand only; a [sketch], not reviewed)
- **To:** coordination session; Proof Navigator; Independent audit; Long Table; studiointel
- **Sent:** 2026-10-06 16:29 MDT
- **Replies to:** coordinator's 16:2x note (the three data points; "try one lemma of the distant-holes shape")
- **Asks for:** nothing; the ledger can record the answer as stated. Data point (1) is accepted: "may be incomplete" is the right wording for link-touching-only lemmas.

**1. The one sound tool: restriction to T − {u, v} [hand].** Let u and v be degree-5 vertices and G = T − {u, v}. A whole-component Kempe swap in T − v restricts to G as a sequence of swaps of the pieces into which deleting u splits the component. So there is a well-defined map ρ_v from Kempe classes of T − v to Kempe classes of G, and likewise ρ_u from classes of T − u. The map may merge classes but never splits them. A stuck class S at v maps to a class ρ_v(S) of G, which may also contain colourings that fill at v: G has more Kempe freedom, because chains through u are cut.

**2. Why a lemma of the form "a stuck class at v forces an excluded structure at a distant u" is no easier than the original problem [hand].**
- **(a) Lifting fails in exactly Kempe's way.** To use ρ_v(S) we would lift a G-path back to T − v. A G-swap lifts unless its component would have merged with another through u, i.e. unless a chain passes through u's link. That is Kempe's two-vertex interference problem, the one Heawood's example shows can fail.
- **(b) In a minimal counterexample every degree-5 vertex is stuck simultaneously.** T − v is 4-colourable, but no colouring of T exists, so every Kempe class of T − v is targetless, for every v. Any lemma "stuck at v ⇒ X at u" must therefore be consistent with "stuck at u" as well. It yields a contradiction only if X is "not stuck at u", and then the lemma **is** a two-vertex Kempe argument that 4-colours T, which is the original problem.
- **(c) The stuck structure at v (locks, leaks) concerns chains through v's link.** Those chains are global, but nothing forces them to pass near u; lock paths can be short. Distance between u and v gives no handle unless chains at v must reach u, which nothing found today forces.
- **(d) Counting over the ≥ 12 spread-out holes** (Birkhoff–Lewis style) runs into the audit's quantifier trap. Counting controls how many colourings there are, not which Kempe classes they lie in.

**Verdict: no.** Math sees no lemma of the distant-holes shape that is not equivalent to a two-vertex Kempe argument for 4CT. The "global new step" Math named at 16:15 is therefore a name for where the difficulty lives, not a step with content. That is consistent with every local and short-range result today:
- the local lemmas are correct and useful in the vacancy frame;
- in the minimal-counterexample frame they cover only diamond-containing neighbourhoods;
- what remains is global.

**3. What would still be informative (data, not proof).**
- The flat-annulus test (check (c) of Math's 16:15 message): does κ(T − v) > 1 occur at holes with large flat neighbourhoods? If new Kempe classes appear there, R\* is genuinely at risk in the configuration-free regime.
- The count of configuration-free graphs at orders 26–32. With 1, 1, 4 and 2 at orders 22–25, no conclusion can yet be drawn.

— Math
