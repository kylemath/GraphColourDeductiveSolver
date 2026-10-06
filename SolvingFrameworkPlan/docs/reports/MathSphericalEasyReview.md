# Independent hand review of the native spherical easy-neighbour bridge

Math / high_degree_landings, 5 October 2026. I reviewed root's complete `SphericalVacancyEasy.lean`, including `vacancy_gap_easy`, together with the definitions and native geometric wrapper in `VacancyMobility.lean`. No source was edited and no additional compilation was run. Root's fresh full audit remains the compilation check for the integrated package.

Reviewed source SHA-256: `61eea0094b13a5db59e6fe21ccc9c506939127931f8065b813c0cfc77f5f8c04` for `SphericalVacancyEasy.lean`. Mobility source at review: `5780a996567dfc0d5c2aee7408f68c2abdc0e8e977c420958e752c3e56f9d74c`.

**Verdict: the mathematical argument and stated premises are sound.** No error was found in the actual-component, properness, or protected-path handling. The integrated three-swap theorem is explicitly normalized; it does not yet prove transport from every arbitrary colour word into that normalized statement.

## Actual degree-four extension

`vacancy_easy_degree_four` quantifies over every proper four-colouring with its hole at a vertex of degree at most four and derives `EasyAt`, namely a fill already present or one actual `KempeStep` producing a fill.

The small-image branch correctly chooses a colour outside the neighbour-colour image. In the remaining branch, image cardinality exceeds three while neighbour cardinality is at most four. Both are therefore exactly four. Equality of the finite-set cardinalities gives injectivity of the colouring on the actual neighbour set. Composing this with the native degree-four cyclic equivalence supplies an injective colour map on the four actual ports. Surjectivity of that equivalence establishes the required singleton assertions for every neighbour, not just the displayed ports.

`pair_reach_induce` maps a walk of the deletion's actual pair graph to the induced graph of active vertices. Each edge carries activity of its endpoints, and the initial active seed covers the zero-length case. Only this forward implication is needed: it permits the native `four_colour_hopposite` theorem to rule out both opposite locks in the actual pair graphs. No unproved converse equivalence is used.

The unlocked branch calls `one_swap_target`. That existing theorem constructs the whole component seeded at the selected neighbour and swaps exactly it, with properness inherited from the supplied `ProperOff` premise. The output is an actual move and target, not merely an assertion that some colouring exists. The stored colour at the vacant vertex is irrelevant throughout.

## Prefix and protection

`vacancy_singleton_easy` applies the actual two-move suffix conversion to the established degree-four ease theorem. `vacancy_approach_easy` unpacks `Approach` into either no initial swap or one genuine original-hole component swap, followed by a singleton witness. In the swap branch it derives current properness using `kempe_proper`, obtains the two-swap suffix replacement at the original hole, and prepends the actual first swap. Thus the three-swap bound is justified by K-prefix plus a suffix of mixed length at most two. It does not rely on a false universal conversion of arbitrary three-move paths.

`vacancy_singleton_easy_protected` constructs both the actual `PurePath` and the existing `ProtectedPath` invariant at every intermediate hole, with a proper filled endpoint. Its only protection premise is that the original hole lies outside Z. The auxiliary easy neighbour may lie inside Z; its temporary slide has been removed. Colours on Z may change, as the permitted move conventions require.

## Exact normalized geometric integration

`vacancy_gap_easy` requires:

- an actual `FiveLink` comprising all five distinct neighbours of the original hole;
- properness of the supplied deletion colouring;
- its displayed colour pattern `(0,1,0,2,3)` on those ports;
- agreement of the port order with the actual native spherical rotation;
- adjacency of the chosen neighbour and its global degree at most four.

The native `vacancy_mobility_normalized` theorem discharges its alternating-connectivity implications from the existing rotation/face-sum intersection theorem. Its two conclusions are an original-hole pure fill within one swap or an actual `Approach` to each selected neighbour. The former is included in the three-swap bound directly; the latter is passed to `vacancy_approach_easy`.

I checked the four port-index uses in `vacancy_alternation`: the disjoint colour pairs and directed/symmetric reachability arguments agree with the requested opposite locks. The pair-walk support lemma excludes the hole and supplies the colour disjointness needed at the native intersection vertex. There is no new Jordan axiom or extra separation premise in the normalized spherical theorem.

The outstanding scope boundary is **word normalization and colour-renaming transport**. The source correctly retains the `Pattern` and actual-rotation premises rather than claiming they are automatic for every deletion start. The degree-four easy theorem itself has no normalized-word restriction.
