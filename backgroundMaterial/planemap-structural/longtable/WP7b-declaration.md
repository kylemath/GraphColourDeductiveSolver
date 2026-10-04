# WP7b declaration: dynamic re-partition at traps

Long Table, 4 October 2026. Committed **before** the run. Discovery orders 12–18 only; orders 19–20 stay untouched. These are hypotheses to test, not claims.

## Measurements

The definitions are fixed **relative to the starting state**. For a non-target state c at root r, let ρ be its repeated boundary colour and S the three singleton colours. All colours are raw: no renaming after a move.

- **Pair masses.** For any colouring c′, q_P(c′) is the sum over the P-components K meeting B of |K∖B|², for each of the six pairs P.
- **The split.** Δ_rep(c → c′) is the sum over the three pairs containing ρ of the change in q_P. Δ_sing(c → c′) is the sum over the three pairs inside S. These two add up to Δq.
- **Move types.** A first move is a *rep-move* if its pair contains ρ, and a *sing-move* otherwise. It *touches B* if its component meets B, and is *interior* otherwise.
- **Macros.** As in the contract: at most two swaps, with components recomputed after the first.

For every **two-swap-stuck** state (a "trap") and every **one-swap-stuck** state that is not two-swap stuck (a "shallow" state), the run records:
1. (Δ_rep, Δ_sing) for every first move, split by move type;
2. for shallow states, the first move of every decreasing two-swap macro, its type, and its (Δ_rep, Δ_sing).

## Hypotheses

- **H-A (merging at traps).** At every trap, every rep-move that touches B has Δ_rep > 0. In words, any swap of a repeated-colour chain on the boundary pushes mass into the repeated-colour pairs.
- **H-B (escapes begin by splitting).** At every shallow state, at least one decreasing two-swap macro has a first move with Δ_rep ≤ 0.
- **H-C (sing-moves are neutral or uphill at traps).** At every trap, every sing-move has Δq ≥ 0, with Δ_sing ≥ 0.

H-C is included to check the observation at order 17, graph 0, root 4, where the singleton-pair swap had Δq = 0. One-swap stuckness already forces Δq ≥ 0 for every move, so only the Δ_sing part of H-C carries information.

**Kill conditions:** for each hypothesis, one counterexample state, recorded with its colouring and the offending move.

**Interpretation, fixed in advance.** If H-A and H-B both survive, the dynamic picture is this: traps are states where every boundary repeated-colour swap merges repeated-colour mass, while shallow states always have a splitting first step. That would suggest a rank ingredient that tracks repeated-colour fragmentation. Any such rank must then pass the joint frozen gate. If either fails, record the witness and report the actual pattern descriptively.
