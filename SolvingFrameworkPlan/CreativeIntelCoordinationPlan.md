# Next steps with Creative Intel / Long Table

4 October 2026. User-requested coordination following Long Table commit 833e0f7 and `GremlinAudit.md`. This plan divides preparation and review work. It does not release WP18 experiments or change navigator statuses. Creative Intel is the Long Table team in the existing message protocol.

## First objective

Finish a reviewable belt-family argument while making WP18 capable of certifying its claimed bounds. Preserve the gremlin team's useful exploratory work, with exact domains and independent checks. Keep fixed-hole swaps, moving-hole paths and chosen-fan bounds distinct.

## Work division

| Owner | Work | Concrete deliverable | Completion condition |
|---|---|---|---|
| Creative Intel / Long Table | Adopt or challenge the independently checked A_rho transition; assemble the belt argument | One hand-proof page for every hole of G_(3k+2), linking each component lemma | Explicit pole-hole, equal-pole belt-hole and unequal-pole belt-hole cases; opening coverage, tile coverage, monotone traversal, cap termination and small-ring overlap cases all accounted for |
| Creative Intel / Long Table | Amend WP18 and implement its producer and certificate output | Revised declaration, bounded BFS producer, regressions, manifest and checker interface | Exact start/pair coverage; lower-bound evidence as well as successful paths; cap and interruption reporting specified; no experiment before math's explicit go-ahead |
| Creative Intel / Long Table | Reconcile its own reports and inventory existing exploratory evidence | Short correction reply and evidence inventory | WP7's remaining broad short-circuit sentence narrowed; stale classification complaint withdrawn; F32/F42 scope described as root-zero deletion enumeration; saved sweeps labelled exploratory |
| This chat: independent audit | Maintain a separately implemented replay checker | `longtable/audit/gremlin-check.py` and `gremlin-check-results.json`; later a separate WP18 certificate checker | No imports of producer move code; validate input graph, start, whole components, slides, fill, pair coverage and lower-bound completeness |
| This chat: proof review | Review the joined belt argument and exact VH-exists quantifiers | Adversarial review with named gaps or checked arguments | Establish what is a local lemma, what terminates globally, and what suffices for induction; no proof status inferred from a finite pass |
| Math team, by relayed request | Independently replay WP11; review belt proof, VH-exists and amended WP18 | Explicit acceptance or corrections; experimental go-ahead if appropriate | Integrity hashes alone do not count as semantic acceptance; experimental approval identifies the revised declaration/version |
| Proof Navigator, by relayed request | Reconcile handoff and evidence references | Corrected report/ledger references | Separate two-swap mixed escape from three-swap fixed-hole escape; preserve the vacancy branch as open unless math supplies a proof |

This is the proposed division to be acknowledged by an explicit Long Table reply. A posted message or silence is not team acceptance. This chat owns the audit, new local tile note and coordination files; Long Table owns its declaration, producer, assembly and reports. Avoid editing another team's current files concurrently.

## Immediate handoff: reuse work already done

Creative Intel should read `GremlinAudit.md` and `longtable/swarm/unequal-a-rho-tile-audit.md` before writing a replacement tile. The local transition is:

    v_i -> u_i -> u_{i-1}.

If the unchanged colour of u_{i-2} is rho, the new link is (0,1,rho,0,rho), and the hole fills. If it is tau, continue

    u_{i-1} -> v_{i-1} -> v_{i-2},

returning the prepared shape (1,rho,tau,rho,0). Review this lemma, then spend the remaining hand work on global coverage and termination. A checked local transition does not by itself finish the belt theorem. Florek's pole-hole result needs its exact hypotheses and a properly sourced target restriction; avoid claiming historical novelty without a literature check.

The independent checker already reproduces the icosahedron's 60 fan cases, the order-14 start's exact distance two and 36 successful sequences, the 21-vertex escape and the order-17 graph-1 fixed-hole distance four. Reuse these as named regressions rather than duplicating a census.

## WP18 certificate contract to agree before a run

1. Graph identity: full rotation, source index, input hash and a checked simple spherical triangulation. Enumerate every degree-five vertex and every legal fan, recording even empty start families explicitly. Explain their treatment rather than taking an unexplained vacuous maximum.
2. Start identity: hole plus a proper colouring, its vertex order, the two fan chords and confirmation they are bichromatic. Added fan chords constrain the starts only; moves run in the current deletion of the original graph.
3. Move identity: colour pair and the complete component vertex set for a swap; old/new hole and transferred colour for a slide. Check properness and target conditions independently. Canonical state keys must include the hole.
4. Successful-path certificates prove upper bounds. Exact distances also need completeness of all earlier BFS layers. A failure of m(T)<=2 requires, for every legal pair, a specific admitted start and a complete exclusion of fills at depths zero, one and two. A length-three path alone is insufficient.
5. Capped distances are lower bounds, possibly infinite. A complete depth-six search without a target excludes length at most two; it does not refute VH-exists. A resource interruption that leaves a required layer incomplete is inconclusive. Do not require a successful shortest-path witness where no path has been found.
6. For exact m(T), distinguish resolved pair values from unresolved pair lower bounds. Report an exact minimum only when those lower bounds cannot beat the best resolved pair. Do not turn omitted or interrupted pairs into passes.
7. Before asking for release, commit regressions for the icosahedron, published order-14 start, malformed witnesses, high-degree landing holes, colour-renaming invariance, fan-chord handling and cap/interruption distinctions. Freeze the producer/checker input contract and code hashes.

This chat will independently check the certificate contract and fixture outputs before broad runs. Creative Intel should send the revised declaration to math and obtain an explicit response before P1. Order 21 remains the declared held-out statistic check; existing rank sweeps on that order must remain disclosed. Nothing in this plan broadens the approved experiment scope.

## Corrections to relay

- The 21-vertex colouring needs two Kempe swaps when slides are allowed. Its original fixed-hole target requires three. The 172 frozen pairs among 224 do not kill a two-swap mixed strategy. The graph has 57 edges and 38 faces, not 63 and 42.
- Revision 72 already links the fan-word classification. The older missing-file complaint is stale.
- F32/F42 output scope is deletion colouring at root zero; do not conflate it with full-graph enumeration or a proof of a slide bridge.
- Existing q/lin sweeps report an existential passing root on every checked graph through order 26. Their whole-census conclusions are still producer reports, not independently accepted results. A failed root does not kill an existential root theorem.
- The WP11 manifest has been checked for integrity here; math's independent semantic replay is still its own acceptance step.

## Order of work and next checkpoint

First, Creative Intel acknowledges the division and returns any conflicts with its current work. Then belt assembly and WP18 preparation proceed independently. This chat reviews each submitted artifact; math reviews the resulting proof and declaration. Broad WP18 runs follow only its explicit go-ahead and stay inside the declared resource limits.

The next checkpoint is a reply containing: the adopted or rejected tile lemma; the joined belt-proof path and remaining gaps; amended WP18 declaration/code hashes and regression output; any math acceptance/go-ahead received; and a list of corrections relayed. Preserve WP12's withdrawal. Navigator statuses, play edits and new rank fitting are not tasks in this handoff.
