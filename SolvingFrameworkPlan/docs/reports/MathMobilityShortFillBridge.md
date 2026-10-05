# A degree-five hole adjacent to degree four fills by three pure swaps

Math / high_degree_landings, 5 October 2026. **[hand argument for review]**. No computation. This combines the mobility alternative in `MathCyclicTrapResearch.md` (independently reviewed by this team) with the compiled short-fill theorem M3. It strengthens the fan-specific theorem in `MathBoundaryFourResearch.md`.

**Theorem.** Let T be a finite simple spherical triangulation. If x has degree five and has a neighbour a of degree at most four, then every proper four-colouring of T−x fills the fixed hole x within at most three whole-component Kempe swaps.

If x has a zero- or one-swap fill, stop. Otherwise the local mobility alternative supplies a path to the chosen neighbour a consisting of at most one Kempe swap followed by one singleton slide. If a initially carries a singleton on N(x), the preparatory swap is unnecessary.

After the slide the hole a has its actual global degree at most four. If its degree is at most three it is already filled. If its degree is four, the opposite-lock Jordan argument fills it by at most one Kempe swap. Thus there is a path

    optional K at x, then S from x to a, then optional K at a, then fill.

Apply M3 to the suffix after the optional preparatory swap. This suffix has mixed length at most two and starts with its hole at x. M3 replaces it with at most two pure Kempe swaps filling that same original hole x. Prepend the optional first swap. The resulting pure path has length at most three and never moves its hole.

All component swaps in this argument refer to the colouring on which they act. The last degree-four swap need not avoid boundary vertices, and no boundary colours are frozen. The conclusion is a pure fill at x, not a permission to retain the auxiliary slide onto a.

**Protected-face consequence.** If x is outside a protected face phi and a is on it, the resulting pure path is permitted because its only hole is x. Every legal fan at x is therefore phi-good, since the theorem covers every proper deletion start, not merely fan-admitted starts. For starts admitted by the fan with apex a, a is already singleton and the stronger bound of two applies.

**Degree-five region consequence.** In the four-connected face-avoiding class, let W be a connected component of the graph induced by off-face degree-five vertices. If W contains a vertex adjacent to a degree-four boundary vertex, then every state at every root in W fills by a phi-avoiding path. Given such a state, follow a fixed path in W towards the known fillable vertex. At each current degree-five hole the mobility alternative either gives an immediate fill or supplies a path of at most one swap and one slide to the next off-face vertex. On reaching the last vertex, use its pure three-swap fill. Hence every legal fan at every root of W is phi-good. This is a genuine fill transfer, so no unproved transport of fan marks is used.

This is not a general conversion of three mixed moves into three pure swaps. It works because the only possible extra first move is a Kempe swap, leaving a suffix of length at most two to which M3 applies. A three-move path starting with a slide may lack such a conversion.
