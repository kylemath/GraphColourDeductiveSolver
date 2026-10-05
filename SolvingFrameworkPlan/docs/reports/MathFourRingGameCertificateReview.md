# Math review: one saved free-adversary four-ring counterexample

Math triangle-carry research team, 5 October 2026. **[computed: independently checked saved exploratory counterexample]** and **[hand: interface review]**. This is an independent Math implementation, not a statement that the separate Audit team has completed its review. No graph generation, census, random sampling, new order, or exploratory search was performed.

## Frozen input and limits

The only input is Long Table's `explore-vhphi/vhphi-quad-explore-seed2-mixed0.json`.

- Input SHA-256: `ca1c0921e24c005cf551a5c67e4876ad52319502ccea738df1aca3489015d224`.
- Independent checker: `longtable/audit/math_four_ring_saved_replay.py`.
- Checker SHA-256: `72cd4803e0b8a4362e0542df18b13fa11de960d4c86b2a4f18a9bda7b0a27719`.
- Output: `longtable/audit/math-four-ring-saved-replay.json`.
- Output SHA-256: `2b77aa77d2f3e164407daa58b1581f13dd548f9e60c0bb931cfd0dce74321dd6`.

The scope and limits were sent to root before running: one saved order-16 graph, fewer than 10,000 states, 60 CPU seconds, output under 10 MB. Final run completed in 0.243 seconds. Short reruns after removing redundant work and adding an explicit per-root closure assertion changed no mathematical counts.

## Independent graph and game reconstruction

The checker imports no producer module. It reconstructs adjacency and vertex rotations from the stored oriented face list. It verifies that every original edge has exactly two oppositely oriented face incidences, every vertex link is a single cycle, Euler characteristic is two, the degrees match the saved record, and the four protected vertices induce a cycle after deleting edge (0,9). The protected set is {0,1,9,14}; vertices outside it have degree at least five.

For every permitted hole outside the protected cycle, the checker independently enumerates every proper four-colouring modulo global colour permutation by restricted-growth backtracking. This gives 1186 states. Quotienting by colour permutation is valid because the game, its legal moves, and its fill target are invariant under such a permutation; no boundary colour is frozen.

For each colour pair it constructs actual whole components. A selected boundary-touching component has two possible outcomes precisely when a second component of the same pair touches the protected cycle: swap the selected component alone, or both components. All generated successors are independently checked proper and belong to the exhaustively enumerated state set. Singleton slides are allowed only when their destination is outside the protected set. Each root's deletion starts generate the full same 1186-state outcome closure.

The finite-game winning attractor is calculated with the correct quantifiers: a state enters the attractor if there exists a player action all of whose adversarial outcomes are already winning. This is not existential reachability over the outcomes.

## Exact result and counterexample certificate

The full mixed game has:

- 1186 states;
- 432 already filled states;
- 1076 winning states;
- 110 losing states;
- two nonterminal attractor layers.

There are ten degree-five vertices outside the protected cycle and five legal fans at each. Every one of these 50 pairs has an admitted losing start. All per-fan counts match the saved report exactly; the best count is 44 winning starts out of 46 admitted starts.

The output stores the entire 110-state losing kernel and one explicit admitted losing start for every candidate pair. For every state in that kernel and every player action, the checker verifies that at least one outcome stays in the kernel. None of its states is filled. This supplies a memoryless adversarial strategy that avoids the target forever, and certifies that no candidate pair wins every start.

With the adversary removed and only pure Kempe swaps retained, every one of the 1186 states reaches a fill. Thus the obstruction is specifically the free adversary, not ordinary pure reachability on this member.

## Hand interface review and scope

The four-cycle component restriction lemma is sound: a global component restricts to one side component or the union of two boundary-touching components at opposite boundary vertices. A colour pair meeting three or four cycle vertices already connects them along the cycle; only two opposite active vertices can supply an additional merge. The interior slide lift also remains valid because the source neighbourhood agrees with the side neighbourhood.

The proposed game intentionally allows the adversary to choose a different merge outcome at each turn without remembering a real exterior graph or exterior colouring. Its finite losing kernel therefore refutes the game hypothesis as stated. It supplies no counterexample to VH_C, VH∃, or a four-cut theorem with a fixed evolving far side.

The hand closure argument has the appropriate scope: a genuinely winning side strategy tolerates every possible extra boundary-component merge, so it can be followed under an actual exterior. Across a triangular interface there is at most one boundary-touching side component for any pair, so an additional exterior component cannot introduce another side component. Across a quadrilateral interface the total restriction still consists of the chosen component with at most its one boundary partner. This establishes the described strategy lift; it does not repair the now-false universal free-game hypothesis.

**Review outcome:** accept this single saved member as an independently checked finite counterexample to the unrestricted free-adversary game. The triangle reduction is unaffected. A constrained far-side model must track realizable, evolving connection information rather than grant arbitrary independent choices.
