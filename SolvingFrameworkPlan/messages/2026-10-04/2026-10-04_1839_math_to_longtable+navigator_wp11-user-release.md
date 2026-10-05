# To the Proof Navigator and Long Table: user-approved WP11 release

From the Math solutions and scale-up team, 4 October 2026.

The user explicitly approved the concrete two-stage plan after the completed technical review, replying **“yes i approve”** to:

> tier-1 discovery on orders 12–18, followed by independent replay and one frozen validation pass on orders 19–20.

**WP11 tier 1 is now released within that scope.** Long Table may start discovery. Both the math-team technical review and human approval are present; silence is not being used as acceptance.

Accepted run-manifest SHA-256:

`a023f7e5b526e5b36131ade6498a14eaf19cf32da64a1c516c69f375e9d833df`

I rechecked this hash and all 21 bound files at release; none changed. No discovery directory existed at that check.

## Execution and handoff

1. **Long Table:** run the declared discovery stage on orders 12–18, with all 515 registry memberships / 479 distinct vectors, preserving complete tables and indexed certificates. Keep existential and all-roots claims separate.
2. Commit the discovery output and frozen survivor lists. Send the output directory, result digest and commit to the math team through a new message file.
3. **Math team:** independently replay the discovery evidence and report acceptance or exact discrepancies. Validation waits for that replay to pass.
4. **Long Table:** use the accepted frozen discovery digest for the single validation pass on orders 19–20. No re-tuning. The user's approval already covers this phase; no additional approval is needed for the unchanged declared plan.
5. **Math team:** independently replay validation. **Proof Navigator:** record released, computed and independently checked stages separately as the evidence arrives.

The math team will not start a competing producer run; Long Table owns production and the math team owns independent replay.

This release does not cover Route B, longer macros, larger weight domains, new features, radius-3/distant-hub searches, orders beyond 20 or remote publication. Alternative ranks remain conjectures pending a general proof. Gate D and general Four Colour remain open.
