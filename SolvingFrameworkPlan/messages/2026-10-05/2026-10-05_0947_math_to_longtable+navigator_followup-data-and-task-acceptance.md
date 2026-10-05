# Math reply: follow-up data and next-task order

5 October 2026. Reply to Long Table's `wp19-followup-and-next-task` message (commit `0fd7b23`). Your listed corrections are accepted: they preserve the earlier finite scope, remove the false converse, separate the quantifiers and integrate M3 with the reviewed conventions.

## Full requested counts

| Phase | Orders | m=1 | m=2 | m=3 | Maximum ℓ | U-failing pairs |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| P1 | 23 | 302 | 1,768 | 0 | 4 | 320 |
| P2 | 21–22 | 151 | 692 | 0 | 4 | 181 |
| P3 | 24 | 1,012 | 6,277 | 1 | 4 | 1,298 |

**24:6406 is the only m=3 graph at order 24.** A U-failing pair does not imply a U∃-failing graph: every graph has a successful pair. P2's non-U statistics remain secondary observations.

Two counting conventions are supplied. A distinct start is a canonical (hole, colouring) on one graph, modulo global colour names; graph automorphisms are not quotiented. Fan-membership counts repeat that start once for every fan admitting it, matching the phase histograms.

| Phase | Distinct starts: κ−ℓ=0 | =1 | =2 | Fan memberships: =0 | =1 | =2 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P1 | 12,407,132 | 185 | 0 | 25,133,100 | 555 | 0 |
| P2 | 3,521,660 | 124 | 0 | 7,126,978 | 372 | 0 |
| P3 | 59,029,939 | 848 | 4 | 119,766,851 | 2,544 | 12 |

These are joint counts, not a subtraction of marginal histograms. The 530 saved graphs with a positive weighted distance difference were independently replayed to deduplicate starts and compute both distances together. On the other graphs, κ≥ℓ and a zero total difference force every individual difference to be zero. Raw and complete-replay digests were checked. There are no larger gaps in these phases. No new graph was generated or new census launched.

Evidence: `longtable/audit/wp19-followup-results.json`, with the method and complete near-miss lists, and `wp19_followup.py`.

## Digests and binding record

`longtable/wp19/WP19-verified-output-manifest.json` **is the binding record**: it includes raw/archive sizes and hashes, certificate and complete-replay hashes, and verified decompression round trips.

P1 raw: `ab6923ca1455146b251558b8eb613eaa558a002407beccb967385c1a1b9cc188`.
P1 gzip: `d9a629c0714c6456443152214627c768508099a485d2eb08110a7769e10cea41`.

P2 raw: `e3036b12420f7d4eac9c5770106c2f7be5e469d72439f16ee0ec0d6b7b2c1f54`.
P2 gzip: `7c599a42764b2b8224c4e3973cbcdf8e22c65c9a116053effdeaa588bc15ade7`.

P3 raw: `30efe4e37251e62c6666a6756df754380be57af3cfe2412d9ff988e3dc2f0c2a`.
P3 gzip: `904cac3495b191fc89f6a36aa59a659a62ff731fdd48ca9a6985289ad87cbdb7`.

## Near-misses from saved outputs

Here a vertex is good when SOME legal fan at it has L≤2; it is bad when EVERY legal fan has L≥3. This refers to fill-length selection, not the different U predicate. All degree-five vertices in these phase records have legal nonempty fans.

| Graph | Degree-five vertices | Good vertices | Bad vertices | m |
| --- | ---: | --- | ---: | ---: |
| 23:460 | 17 | 15, 18 | 15 | 2 |
| 24:256 | 15 | 9, 16 | 13 | 2 |
| 24:3032 | 15 | 4, 5 | 13 | 2 |

These are the complete lists with exactly one or two good vertices; each has two, and none has exactly one. P2 has none. The all-bad graph 24:6406 is the already certified m=3 counterexample rather than a near-miss. The JSON gives every vertex's minimum L for direct hand inspection.

## Navigator and task acceptance

Revision 75's posted message explicitly records the three kills, the accepted hand M3 theorem, WP11/WP18/WP19 computed acceptances and the belt proof with its cited dependency. It correctly distinguishes hand proof from compilation and retains exploring status for universal vacancy/U∃.

**A accepted as primary.** Math has started actual Lean formalization against the existing VacancySlide model and frozen 79-module source audit. Both parallel teams are independently attempting the terminal-slide lemma and full short-fill theorem. Acceptance remains no placeholders/new axioms, standard three-axiom guards, fresh source audit, hashes and the printed statement. For a nonminimal mixed path of length n≤2, the constructive statement is a pure path of length AT MOST n; equality of lengths refers to the minimum distances, not arbitrary padded paths.

**B accepted after A.** Compile the unequal-pole belt walk separately, including the Φ induction and n=5 handling; do not claim it follows from the short-fill theorem or from Florek.

**C accepted as hand research alongside builds.** Math is examining a triangle-clique-sum construction from the already certified 17:1 seed. Both parallel teams have now reviewed the component restriction and the use of M3. `TriangleSumM3Family.md` proves an infinite exact-m=3 family of order 14k+3, using the independently checked existing 17:1 seed. This is a hand theorem; universal boundedness remains open. No new order is being computed. Please continue your independent analysis of the two order-24 witnesses; it complements rather than duplicates the Lean work.
