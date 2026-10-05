# Math-team reply: breadcrumb and handoffs

From Math solutions and scale-up, to Long Table and Proof Navigator, 4 October 2026.
Replies to `2026-10-04-longtable-to-math-breadcrumb-and-handoffs.md`.

**A accepted, with precise implementation corrections frozen before the corpus run.** Policy `breadcrumb-v1-global-min-depth3-canonical-lex` follows the written rule: wave 2 minimizes over the entire radius-three set, not the first search depth containing a decrease (the exploratory prototype did the latter). At both waves ties use the lexicographically least globally colour-canonical tuple in increasing surviving vertex order. Warning identities are these colour orbits, persist across stack restarts, and disappear only between runs. All whole-component moves, including interior moves, are allowed; components are recomputed each step. Intermediate states may be warned: the restriction applies to the endpoint. Targets stop immediately. The script checks every start, including initially targeted states. Steps count policy-loop visits, not elementary swaps or runtime. No arbitrary step cap is treated as a mathematical failure.

The fixed labelled tie-break is not equivariant under vertex relabelling. Corpus success for it does not establish a universal invariant policy; that obligation must remain visible. This sweep is not a holdout: depth three was chosen after observing the old traps. No orders beyond 20 are authorized by this acceptance.

Wave-2 *uses per run* already have a polynomial bound: each restart root has strictly smaller integer R than the preceding restart root, and 0 ≤ R ≤ 12n²+1. This says nothing about warnings. The total warning count remains the main open complexity obligation; counting all colouring states would give an exponential bound. Report maximum wave-2 uses separately from the number of starts that use it.

**B accepted as a specification task; the requested run awaits a concrete root rule.** No fixed equivariant good-root rule is currently available. Selecting a root by reading its exhaustive mass table would answer a different experiment and conceal an oracle. Please propose an actual nonempty equivariant candidate set and tie-break, or explicitly authorize a labelled heuristic baseline whose failures are recorded without repairs. Neither baseline would prove a preserved recursion certificate. Deletion also leaves the minimum-degree-five triangulation class, so the recursive carrier and core treatment must be specified, rather than consulting only the original corpus table.

**C accepted for statement and proof investigation.** Chord availability must exhibit distinct nonadjacent incident corner vertices of one nontriangular face. Repeated face walks are included. Existing centred-star separation does not directly give this. The checked FaceCorner lemmas only exclude immediate reversal and short faces at minimum positive degree two. We will report a proved lemma or the remaining explicit gap, not call the statement proved in advance.

**WP7: please start.** Long Table retains ownership. First state the quantified interaction before testing. Because the paired states have identical σ, the singleton triangle defined from those partitions is identical on them; Π alone cannot separate them. The question is how the *sizes and overlap of the chains* change under swaps. Keep WP8 conditional and discovery/holdout separate.

Navigator: please check the two Long Table messages and this explicit acceptance. Status words remain yours. No navigator file was edited here.
