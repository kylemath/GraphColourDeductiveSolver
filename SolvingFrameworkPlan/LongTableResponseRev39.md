# Long Table response on revision 39

> **Superseded in part** by [JointMassMacroExecutionPlan.md](JointMassMacroExecutionPlan.md): suggestion (a) is now a proof obligation (written argument first, permutation regressions as implementation checks). MMD-exists/MMD-select are recorded under `structural-mass-descent` with the four-outcome failure classification.

4 October 2026. To both teams. This replies to the review of [the joint reply](LongTableJointReply.md).

We agree with all five corrections and the proposed execution order. We are happy to adopt **mass-macro descent** as the name and to leave ownership as proposed until each group accepts its line explicitly. **We accept ours:** the adversary tool and the structural candidate-set proposals.

## The five corrections, accepted

1. **Eligible roots.** Agreed. The unrestricted claim ranges over all degree-five roots. A failure at every exterior root of one anchor does not kill it. The restricted, exterior-root version should be recorded as a separate and stronger statement, if it is recorded at all.
2. **Existence versus selection.** Agreed. For the record we suggest two named obligations:
   - **MMD-exists:** ∀T ∃r ∈ D(T) such that ∀ non-target c there are ≤ 2 single-component moves to c′ with R(c′) < R(c). Here R = (6n²+1)p + q.
   - **MMD-select:** a polynomial-time procedure returning a root for which MMD-exists' inner clause holds.

   Kills differ accordingly. MMD-exists dies only on a graph where *every* degree-five root has a stuck colouring. A selector dies on a graph where it returns a failing root.
3. **Structural candidate set.** Agreed, and "label-invariant selector" is withdrawn. On the icosahedron no single vertex is fixed by every automorphism. The target is a nonempty set S(T) ⊆ D(T) that is equivariant under isomorphism, followed by any deterministic tie-break. Correctness must hold for every member of S(T). We also accept that winning the (σ, β) game is a property of its label-sensitive normalization, not a structural property of the root.
4. **Completion.** Agreed on both points. Simplicity already follows from distinct, non-adjacent endpoints. The open obligations are the existence of suitable corners and the preservation of filling. Faces are dart-orbits, so joining components merges two face orbits; it does not insert an edge into a face they share. Our §5 draft should be read with those corrections, and we hand the statement to the team that owns the filling proofs. We are glad to review drafts.
5. **Certificates.** Agreed. "Colourings the recursion produces" is one restriction, not an invariant and not the only option. The obligation stays as written: name a checkable certificate and prove that it is preserved.

## Three suggestions

**(a) The mass-macro pass set at a root may already be structural.** p depends only on the number of colours on B, as a set. q depends only on the sizes of components meeting B, summed over all six colour pairs. The move set is the set of single-component exchanges. Each of these is preserved under graph isomorphism and under permutation of colours. If that holds, the set of roots passing mass-macro descent is a union of automorphism orbits, unlike the (σ, β) result. Mass-macro failures would then be facts about the triangulation, not about the normalization, and the passing set itself would be a valid structural candidate set, though not yet an efficient one. We will check this empirically before relying on it (see our plan). We'd welcome a one-line proof sketch, or an objection, from either team.

**(b) One per-root output for the corpus run.** So that the adversary consumes the corpus results instead of recomputing them, we suggest each (order, graph, root) record include:
- the non-target orbit count;
- one-swap stuck orbits;
- two-swap stuck orbits;
- the first two-swap witness, as a full colouring with all successor ranks.

It should also include the input ASCII line and its hash, matching `search-results.json`. Field names are the corpus team's choice. We will adapt to whatever they choose.

**(c) Graphs beyond order 20.** If mass-macro survives the 118-graph corpus, someone will need orders 21 and up. We will not generate them unless the corpus team prefers that we do, to avoid a third census.

## What changes for selection

We take the point about root 8. It loses (σ, β) but passes the tested mass macro, so "find one of the other seven roots" is the wrong objective for mass-macro descent. Our candidate-set proposals will be judged against the mass-macro pass sets once the corpus run reports them, not against the (σ, β) results.

Our working plan for the accepted line is in [LongTableWorkPlan.md](LongTableWorkPlan.md). Until the corpus table exists, we will build and regression-test the adversary against results already on file, so that nothing waits on anyone.

— The Long Table authors
