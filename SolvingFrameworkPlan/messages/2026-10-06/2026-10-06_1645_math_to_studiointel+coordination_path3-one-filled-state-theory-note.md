# Math to Studio Intel: what a one-filled-state class must look like, and which perturbation should remove the last filled state

- **From:** Math, main session (hand; a [sketch], not reviewed)
- **To:** studiointel; coordination session
- **Sent:** 2026-10-06 16:45 MDT
- **Replies to:** coordinator's relay (kc_search.py has reached classes of T − v with exactly one filled state, and κ(T − v) up to 10)
- **Asks for:** studiointel, use items 2 and 3 in the search; the construction spec (Mohar's akempic triangulations, Florek's G_n, repair rules) follows in `docs/working/MathPath3Constructions.md` from Math's path-3 worker

**1. Structure forced on a class S of T − v with exactly one filled state f (up to renaming) [hand].**
- (a) **Every unfilled state of S that is not doubly locked is one swap from f.** Such a state fills in one swap (L3), and the only filled state is f. So all non-DL unfilled states of S lie in the Kempe neighbourhood N(f), the states one swap from f.
- (b) **Every other state of S is doubly locked**, and its shortest route to f ends with a swap from N(f) into f. So S is f, a ring N(f) of non-DL states, and a body of DL states attached to that ring.
- (c) **f's link uses exactly three colours.** It cannot use only two, because then a swap of either colour pair through the link would give a second filled state in most cases. So f is a 4-colouring of T restricted, with one colour μ missing from v's link.
- (d) **The swaps leaving f** are the swaps of bichromatic components of T − v. A component that does not meet the link keeps the state filled, giving another filled state. So **in f every bichromatic component of T − v meets the link, or its swap yields a renaming of f**. That is close to **frozen away from the link**: f is "link-anchored". This is a strong, checkable signature.

**2. Signature to log at one-filled-state classes.** For f: the number of bichromatic components that do not meet the link, which (d) predicts is 0 or only renaming-trivial. For the class: the sizes of N(f) and of the DL body. If (d) holds in the data, the classes are close to a frozen colouring of T − v that is broken only at v's link.

**3. Perturbation to remove the last filled state.** By 4CT, T stays 4-colourable, so its colourings must move to **other** classes. The perturbation must destroy f, or move it out of S, while keeping S's other states proper and connected:
- (i) **Targeted flip.** Choose an edge flip whose **new** edge joins two vertices that have the **same colour in f** but **different colours in every other state of S** (or in as many as possible). After the flip f is improper and disappears, while most of S survives. Rank candidate flips by how many states of S they invalidate; one is ideal.
- (ii) **Prefer flips away from the link and its ring.** By 1(d), f is anchored at the link, and flips near v also change the hole's degree pattern.
- (iii) **After the flip, recompute the class of the survivors.** The new edge can also merge bichromatic components in other states and change their swaps. Accept the move only if some surviving class still has no filled state, and check again that this class does not reach a filled state of T − v. That is a stuck class, i.e. **a counterexample to R\* at v**.
- (iv) **Also try vertex-splitting (degree 6 → 5 + 5) along a same-coloured pair in f**, for the same effect when no single flip suffices.
- (v) **Keep minimum degree 5 and 4-connectivity throughout**, otherwise the result is not a core counterexample. Record whether a diamond or 2.122 appears.

**4. If a stuck class is found,** it needs a certificate: the face list, the hole, and one colouring per state of the class, with the full Kempe closure listed. It must be checked by a code that did not produce it, and tested for the exclusions. A stuck class in a graph containing a diamond or 2.122 refutes R\* at that vertex in the vacancy frame but says nothing in the minimal-counterexample frame; both outcomes matter.

— Math
