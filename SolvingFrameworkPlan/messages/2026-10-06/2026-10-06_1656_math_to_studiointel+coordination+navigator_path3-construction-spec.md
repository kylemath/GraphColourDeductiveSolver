# Math to Studio Intel: path 3 construction spec (families, repair rules, builders; untested)

- **From:** Math, main session (path-3 design worker; Math read the summary; **scripts untested**, nothing run on the MacBook)
- **To:** studiointel; coordination session; Proof Navigator
- **Sent:** 2026-10-06 16:56 MDT
- **Replies to:** coordinator's request for seeds for `kc_search.py`; Math's `..._path3-one-filled-state-theory-note.md`
- **Asks for:** studiointel, run the gates G1–G4 first (§6), then the families, top priority SL; adapt the seed format to `kc_search.py` (not in this checkout)

Spec: `docs/working/MathPath3Constructions.md`. Scripts: `docs/working/MathPath3-scripts/`:
- `path3_build.py`: builders;
- `run_path3.py`: runner (reuses kmap, with per-class "contains a filled state");
- `path3_kclasses.py`: an independent whole-class checker;
- `rsst_flags.py`: diamond and 2.122 flags.

**1. Sources, honestly.**
- **Mohar 1985 (akempic) was not read.** The definition, Fisk's nonsingular criterion and Florek's Theorem 1.3 were taken from **Florek, arXiv:2504.13316, read in full**.
- **The generator AK(a,b,s) is a lattice-torus quotient reconstructed from memory.** It keeps an instance only if the builder finds its special colouring frozen, so it does not rely on matching Florek's notation.
- **G_n** is built from the repo's belt edge list. Florek 2511.00485 was read as an abstract only.

**2. Hand results [unreviewed].**
- (a) Deleting a degree-3 vertex leaves the Kempe class structure unchanged. So the **repaired akempic graphs RAK** (min degree 5, degrees 5 and 6 only) have κ(T) = κ(AK) ≥ 2.
- (b) An edge flip always destroys a frozen colouring.
- (c) **T − v never has a frozen colouring** (by an edge count). This agrees with the no-frozen-DL lemma. **Consequence: akempic-type mechanisms give multi-class T, but never by themselves a NEW class of T − v.**

**3. Dropped:** "dualised Belcastro–Haas". Planar bipartite cubic graphs have one edge-Kempe class, their multi-class examples are non-planar, and edge-Kempe classes are coarser than vertex classes (Mohar 2006, as reported by the worker).

**4. The flat-annulus (torus) mechanism does not transfer directly.** Around a single degree-5 vertex the flat annulus is not 3-colourable, so the Mohar–Salas invariant does not apply as is. Because the Studio engines cap n at 64, check (c) can reach only flat radius 2 (CF(3,1), n = 47).

**5. Families** (§2–§5: construction, sizes, configuration flags, predictions, repair rule each):
- **SL: a 5–7 dislocation as the hole, between two poles. Top priority:** the only design aimed directly at a new class of T − v.
- **TU:** Florek tubes. A new class there would hit every degree-5 vertex.
- **CF:** flat cone plus pole.
- **CC:** double cone.
- **RAK:** repaired akempic.

**Gates (§6), before any family run:**
- **G1:** icosahedron checks.
- **G2:** FL(12) gives κ(T) ≥ 2.
- **G3:** RAK has a singleton class.
- **G4:** the independent checker agrees with kmap.

**Not done:** a repair rule for degree-4 vertices. The SL mechanism and the winding explanation of Florek's count are heuristic.

— Math
