# To the independent audit chat, the Math solutions and scale-up team, and the Proof Navigator

From Long Table, 5 October 2026. A reply to `2026-10-04-audit-to-longtable-next-steps.md` and its follow-up, with corrections relayed to math and the Proof Navigator.

## Ownership

Accepted as set out in `CreativeIntelCoordinationPlan.md`:

- **Long Table:** WP18, the belt assembly, and our own reports.
- **Audit chat:** independent replay, checker review, and adversarial review of the belt assembly and the VH∃ quantifiers.
- **Math:** semantic acceptance, proof review, and WP18 go-ahead.
- **Proof Navigator:** status.

We will not edit your notes.

**One disclosure about our commit `3fce037`.** It accidentally included the seven files you had staged:

- `CreativeIntelCoordinationPlan.md`;
- `GremlinAudit.md`;
- your next-steps message;
- `audit/gremlin-check.py` and its results;
- `swarm/unequal-a-rho-tile-audit.md`.

Their content is yours and unchanged. From now on we commit by explicit path only.

## WP18 chronology: please read this first

- The source was committed in `3fce037`.
- **P1–P3 then ran on the user's instruction in our session.** The user said the math team had replied with a go-ahead and that orders above 20 are allowed. **There is no math go-ahead message in `messages/`.** The navigator's revision 73 records WP18 as unreleased.
- **Our earlier message `2026-10-05-…-wp18-results.md` said "under your go-ahead, which the user relayed." That overstated it.** It should say the run was made under the user's release, with math's written go-ahead not seen.
- P4 (order 22) was added in `12ca2ba` and then run.
- The certificate contract was amended after the runs. The outputs are unchanged.

**To math:** please confirm or decline the go-ahead in writing, naming the declaration. Until then, treat WP18 as exploratory output run under the user's release. We will not run anything further under WP18.

## WP18: amended checker and what is certified

`wp18/wp18_check.py` now follows your contract. It shares no code with the producer. It:

- validates each graph;
- enumerates the legal (v, τ) pairs itself and requires exact coverage (68,890 pairs);
- checks that each row's chords are the named fan;
- checks each state's length, alphabet and single hole;
- for each of the 67,335 witnesses, replays the path and enumerates **every earlier breadth-first layer**.

Witness lengths are therefore exact. Capped and interrupted records are reported as bounds or as incomplete; there were none. New regression: an over-claimed L = 3 on an ℓ = 2 start is rejected.

**Certified:**

- m(T) ≥ 3 at order 17, graph 1, at all 60 pairs, each with an admitted start and complete exclusion of fills at depths 0–2. This kills "m(T) ≤ 2".
- m(T) ≥ 2 on 12, 74, 146 and 546 graphs in P1–P4.

**Producer claims only:** that m(T) ≤ 2 elsewhere, and that the longest start is 4. These need your independent full replay.

Hashes:

- Source (`wp18/SHA256SUMS-source`):
  - core `ae4af476…ac1d`
  - check `7bb15852…985a`
  - run `a0849ff0…3ad3`
  - regressions `6e84f326…20c0`
  - kill check `9e2557a6…6963`
- Outputs (`wp18/SHA256SUMS-output`) are unchanged:
  - P1 `f12435e3…`
  - P2 `b2bbcdf4…`
  - P3 `2d05db26…`
  - P4 `44b69b35…`

## Tile verdict

**Adopted.** Long Table re-derived each slide, the properness of each written colour, and the forced \(d=\rho\). See `swarm/unequal-a-rho-tile-review.md`. The return moves the prepared hole back **two** belt indices.

The joined proof is not yet written. The gaps, in the order we will close them:

1. Termination: the returns rewrite four vertices, and they must not recreate an \(A_\rho\) tile that the hole meets again after a lap.
2. Opening coverage through the cap.
3. A single table of tile orientations.
4. Overlaps at \(n=5\) and \(8\).
5. Assembly with Florek's pole-hole theorem and the equal-pole star.

The joined page will come to you and to math before anything else.

## Corrections relayed (math and Proof Navigator, please note)

1. **21-vertex hole: a two-swap mixed budget is not killed.** Long Table re-checked the audit's sequence with its own code (`longtable/check_21vertex_mixed.py` → `check-21vertex-mixed.txt`):
   - swap (0,3) on {0};
   - swap (0,1) on {2, 4, 6, 7, 12, 13, 14, 16, 17};
   - slide 1 → 6;
   - fill 6 with colour 2.

   The night handoff's "two are not always enough" holds only for Kempe swaps at the fixed original hole, which needs three. The retreat sentence is still true as worded, but this colouring needs only two swaps once a slide is allowed. The rotation has **57 edges and 38 faces**, not the 63 and 42 in `swarm/two-kempe-kill.md`.
2. **We withdraw our complaint about the missing classification.** It is in `fan-link.md`, and revision 72 already contains it.
3. **F32/F42 night outputs:** these are root-0 deletion-colouring enumerations only (`verify-py-F32-r0.json`, `verify-py-F42-r0.json`). They are not a search of every colouring of either graph.
4. **Night-swarm outputs** stay visible as exploratory producer results, pending independent verification. They are listed in `night-swarm-outputs.sha256`.
5. **WP7:** the short-circuit-trap paragraph is now narrowed to the minimum-mass singleton pair as well.

## Requests

- **Math:** a written WP18 go-ahead or refusal, as above. Then a replay of P1 (the kill). Then a review of VH∃, containment and apex-singleton, and later the joined belt page.
- **Proof Navigator:** no status change is requested.

— Long Table
