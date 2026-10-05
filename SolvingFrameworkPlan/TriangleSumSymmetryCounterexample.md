# The triangle-sum family refutes the axis-symmetry conjecture as stated

Math, 5 October 2026. **[hand]** structural argument with independently checked facts about the existing 17:1 seed. No order31 graph was generated, coloured or searched. This addresses Conjecture S in Long Table's `wp19/counterexample-analysis.md`, as written without a four-connectedness restriction.

Let Q be 17:1 and let F₊={3,4,11}, F₋={1,2,7} be the two disjoint facial triangles used in `TriangleSumM3Family.md`. Let H₂ be two copies of Q glued along F₊ in the first and F₋ in the second. The already reviewed family theorem gives |V(H₂)|=31 and m(H₂)=3.

**Claim: H₂ has trivial automorphism group.** Therefore it has no half-turn of the type in Conjecture S, or any other nonidentity graph automorphism.

1. **The interface is the unique separating triangle.** The old seed has 30 triangles, all facial. No triangle in the glued graph can use vertices exclusive to both sides: there is no edge between them. Every triangle except the interface is thus an unchanged facial triangle of a seed copy. Deleting the interface leaves two connected components, since deleting either chosen face from Q leaves its remaining 14 vertices connected. The interface itself separates them.
2. **The two sides cannot be exchanged.** Outside the interface, original degrees are unchanged. The first side (Q minus F₊) has 11 degree-five and 3 degree-six vertices. The second (Q minus F₋) has 10 degree-five and 4 degree-six vertices. Their global degree histograms differ. Any automorphism must preserve the unique separating triangle and each component of its complement individually.
3. **Neither seed copy admits a nonidentity restriction.** An automorphism preserving the sides restricts to an automorphism of each induced seed copy, preserving its chosen interface face. Both chosen faces have trivial stabilizer in the full automorphism group of Q. Therefore both restrictions are identities, and so is the global automorphism.

These conclusions do not depend on which triangle bijection is used in the gluing. The face stabilizer and component-degree arguments are unchanged.

## Checked finite seed facts

`longtable/audit/triangle_sum_asymmetry_check.py` reads only the previously verified seed record and its binding. An independent adjacency-only backtracking enumeration visits 70 nodes and exhausts all vertex bijections compatible with degrees and every mapped adjacency/nonadjacency. It finds four graph automorphisms (identity, two reflections and the half-turn). Both selected face stabilizers contain only the identity. This uses the full automorphism group, rather than assuming that the identity and half-turn are its only elements.

The same script checks all triangles against the saved rotation's facial triples, connectivity after removing each chosen face, and the two degree histograms. All results and the four permutations are in `triangle-sum-asymmetry-results.json`. Team B reviewed the unique-separator/stabilizer argument against these corrected seed facts.

**Scope.** Conjecture S is false for minimum-degree-five spherical triangulations as stated. H₂ has a separating triangle. This argument says nothing about a conjecture explicitly restricted to four-connected triangulations. It does not settle boundedness of m, and it introduces no new census.
