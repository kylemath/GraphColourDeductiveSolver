# Math handoff: WP19 complete, three conjectures killed, M3 proved

5 October 2026. All released phases under package `e7172ca` are finished. The certificate checker and complete independent replay passed for P1/P2/P3, with no interrupted graphs, unresolved pairs or truncated output. Full results: `SolvingFrameworkPlan/MathWP19Results.md`. Readable counterexamples: `MathWP19Counterexamples.md`.

## What changed

- **C1 and C3 are killed by 24:6406.** Its exact m is 3: every one of its 70 legal pairs has a start needing at least three mixed moves; 58 pairs have maximum 3 and 12 have maximum 4. It has two degree-seven vertices (1 and 21), so the proposed fullerene restriction on m>=3 is false too.
- **M2 is killed by 24:7228.** At vertex 17, fan 0, the exhibited start has exact mixed distance 3 and Kempe-only distance 5. A slide followed by two swaps fills; complete layers exclude every four-swap fill, and an explicit five-swap path establishes the upper bound. The graph still has m=1. This is a real saving of two Kempe swaps by a slide, not just one.
- **M3 is now a general hand theorem.** On any finite simple graph, finite palette and initial hole degree, ℓ<=2 implies κ=ℓ. Both parallel teams independently accepted the component argument in `MathShortFillTheorem.md`. WP19's frozen statements and sources were not amended mid-run.
- **M1/C2/U∃ passed on these graphs.** Every admitted start in the phases fills within four mixed moves; every graph has m<=3; U∃ holds on all 10,203 WP19 graphs. These passes establish no universal bound or vacancy hypothesis.
- **WP11 validation is independently accepted.** The separate acceptance message verifies all 1,307 tables and 221,249 colouring orbits, 259 existential survivors and 38 all-root survivors on orders 19–20. The late validation report is closed.

P1: all 2,070 order-23 graphs, no kills. P2: U∃ only as a fresh test on 843 order-21/22 graphs; other measurements are secondary. P3: all 7,290 order-24 graphs, three kills on two graphs. The order-23/24 graph sets had been exposed in the night swarm's rank sweeps; these move/class statistics are fresh, not the graph sets themselves.

Both parallel teams separately audited BOTH counterexamples. Each checked all 70 fan-admitted lower witnesses for 24:6406 and independently re-enumerated a complete 134-start best pair to prove m=3. Each reconstructed ℓ=3/κ=5 on 24:7228 with separate layer/path checks. Team A delivered the first complete counterexample review and receives lead-review credit; Team B supplied its own move/BFS implementation. Their files are in `longtable/audit/team-{a,b}-wp19-kills-*`.

## Preserved evidence

`longtable/wp19/wp19-P1.json.gz`, `wp19-P2.json.gz`, `wp19-P3.json.gz` are deterministic lossless archives. Raw JSON remains in the workspace. `WP19-verified-output-manifest.json` binds raw/archive sizes and digests to the certificate and full independent-replay records; decompression digests were checked. P3 raw digest is `30efe4e37251e62c6666a6756df754380be57af3cfe2412d9ff988e3dc2f0c2a`. Named graph records and compact paths/layers are also extracted in `audit/wp19-counterexamples.json` and `wp19-named-kills-results.json`.

## Tasks for Long Table's next session

1. Integrate the M3 theorem with its precise singleton-slide and whole-component conventions; retain the distinction between hand proof and finite observations.
2. Withdraw M2/C1/C3 as universal candidates and update mechanism/17:1 discussions so they no longer imply a one-swap slide saving or a fullerene-only m>=3 obstruction. Preserve the killed statements and certificates in the WP19 historical report, and retain the earlier finite observations with their original order scopes.
3. Study the two named counterexamples by hand: explain why 24:6406 makes every pair bad for a two-move allowance, and why the slide in 24:7228 saves two swaps. This is structural analysis of saved graphs, not a request for a new census or fitted replacement bound.
4. Apply the earlier source corrections: remove the false converse after Lemma F, and distinguish uniform all-start bounds from existential VH∃.

Navigator: record the three kills, accepted M3 hand theorem, completed WP11/WP18/WP19 finite reviews, and the belt proof with its stated Florek dependency. The unbounded vacancy/U∃ hypotheses remain exploring. WP12 stays withdrawn; any further phase or order needs a new declaration. Math has completed the released work; no new run is launched by this handoff.
