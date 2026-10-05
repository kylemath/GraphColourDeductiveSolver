# Math acceptance of WP19

5 October 2026. All released phases under frozen package `e7172ca` completed and independently reproduced. Order 24 kills M2, C1 and C3: the saved certificates and complete independent replay agree. Orders 23 and the U∃-only order-21/22 phase have no kills. There were no interrupted graphs, unresolved pairs, truncated records, capped distances or admitted starts in Kempe classes without a fill in any phase. These are finite results; the unrestricted vacancy hypothesis and U∃ remain open.

## Exact scope

| Phase | Graphs | Legal vertex/fan pairs | m=1 | m=2 | m=3 | U∃ true | Largest ℓ / κ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| P1 | 2,070 | 155,593 | 302 | 1,768 | 0 | 2,070 | 4 / 5 |
| P2 | 843 | 60,960 | 151 | 692 | 0 | 843 | 4 / 5 |
| P3 | 7,290 | 564,852 | 1,012 | 6,277 | 1 | 7,290 | 4 / 5 |

P1 tests all seven statements on all 2,070 order-23 graphs. P3 tests them on all 7,290 order-24 graphs. P2 tests **U∃ only** on all 192 order-21 and 651 order-22 graphs; its other measurements are secondary data. Every graph has m≤2 except 24:6406, whose exact m is 3. This does not mean every vertex/fan pair or every start fills in two moves. Histograms count fan memberships, which can count one deletion colouring in several fans; independently reconstructed distinct-start counts are supplied in the final summary JSON.

## Seven fixed statements

| Statement | P1 | P3 |
| --- | --- | --- |
| M1 | 2,070 passed | 7,290 passed |
| M2 | 2,070 passed | **Killed on 24:7228**; 7,289 passed |
| M3 | 2,070 passed | 7,290 passed |
| C1 | 2,070 passed | **Killed on 24:6406**; 7,289 passed |
| C2 | 2,070 passed | 7,290 passed |
| C3 | 2,025 passed; 45 labelled not applicable | **Killed on 24:6406**; 7,200 passed; 89 labelled not applicable |
| U∃ | 2,070 passed | 7,290 passed |

Every row has zero unresolved cases. The producer labels C3 not applicable when all degrees are already 5 or 6. C1 and C3 are false on 24:6406; M2 is false on 24:7228. M3 additionally has a general hand proof in `MathShortFillTheorem.md`, independently reviewed by both parallel teams. That proof is separate from the unchanged experimental test. M2, C1 and C3 are disproved by finite counterexamples. M1/C2/U∃ passed on the tested graphs and remain universal conjectures.

## Counterexamples

**24:6406 kills C1 and C3.** Every one of its 70 legal vertex/fan pairs has a start with no mixed fill in zero, one or two moves. At least one pair has maximum exactly three, so m=3. The degree multiset is fourteen 5s, eight 6s and two 7s: this simultaneously refutes m≤2 at order≥18 and the implication m≥3⇒all degrees 5/6. All these are exhaustive finite certificates; U∃ nevertheless holds.

**24:7228 kills M2.** At vertex 17, fan 0, the certified start has exact ℓ=3 and κ=5. The mixed path is slide to 8, K(1,2,seed 1), K(0,1,seed 0), in canonical labels after each move. The certificate excludes every pure Kempe fill through depth four; the complete independent replay establishes the exact distance five. Thus κ−ℓ=2, contradicting the proposed allowance of one extra Kempe swap. This graph still has m=1: its good choice of vertex/fan does not prevent a harder individual start elsewhere.

Full ASCII rotations, starts, all-pair lower witnesses and the mixed path are preserved in the complete P3 archive. Graph indices and vertices are zero-based. Both parallel teams separately rechecked all 70 lower certificates and the complete best-pair upper bound, and reconstructed the exact 3/5 witness. Team B also independently rebuilt a successful U∃ pair on each graph. The isolated readable exhibit is MathWP19Counterexamples.md; the accompanying extraction JSON also retains both full graph records. These kills do not refute VH∃ or U∃.

## Independent verification

The released certificate checker re-parsed every graph, verified pair coverage, replayed every saved path and reconstructed every listed all-locked T* class. It explicitly does not certify positive U verdicts, start counts or distance histograms. Math therefore used a separate implementation importing only its own old audit move code: it enumerated every deletion colouring at every hole, rebuilt mixed and Kempe distances, filtered every legal fan family, reconstructed every T* class and re-derived all graph and phase summaries. P3 was replayed as records completed, with final checks binding those records to the finished file, frozen sources, declaration and entire raw input. No replay findings were fed back into the producer.

| Phase | Producer seconds | Replay seconds | Peak producer worker KiB | Saved paths checked | All-locked classes checked |
| --- | ---: | ---: | ---: | ---: | ---: |
| P1 | 420.8 | 445.57 | 27,824 | 23,340 | 320 |
| P2 | 350.9 | 287.35 | 25,904 | 9,805 | 181 |
| P3 | 3558.5 | 3163.11 | 37,920 | 109,162 | 1,298 |

P3 replay time includes waiting for producer records; it overlaps the producer and is not an additional sequential cost. P1 used 12 producer workers and P2 used four. P3 used 12 producer and 12 replay workers concurrently. The declaration’s 30-minute per-graph, 12-hour per-phase, 8-GiB per-worker and 1-GB output limits were not reached.

## Integrity and release

Written Math releases were `8dffb45` (P1/P2) and `81b2bf7` (P3 after the verified P1 cost checkpoint), under the user’s existing autonomous release. Declaration digest: `56d1c97b8b913822822fe0ce5c8b4f2d05827c9845a1810c61037619e4b85a9e`. Producer/checker regressions and the independent replay corruption regressions passed. Frozen sources and imported dependencies were hash-checked; none was tuned between phases.

Each full phase output is preserved as deterministic lossless gzip in `longtable/wp19/wp19-P*.json.gz`; raw JSON also remains in the workspace. `WP19-verified-output-manifest.json` binds raw and archive sizes/digests to certificate and complete-replay files, and records decompression round-trip verification. Exact input hashes and every graph-level record are preserved. To inspect an archive, decompress it to a fresh path and verify its raw digest against that manifest.

Order-23/24 graph sets had already appeared in the night swarm’s exploratory q/lin rank sweeps. These move/class statistics are fresh; the graph sets are not pristine holdouts. No graph beyond these released phases was run. WP12 remains withdrawn.

## Next session

Long Table owns corrections to its source proof pages: promote M3 with its precise move conventions, remove the false converse after Lemma F, and distinguish uniform all-start bounds from existential VH∃. Navigator can record accepted finite results, the reviewed belt theorem with its Florek dependency, the conditional VH∃ induction route and the short-fill theorem. Universal vacancy remains exploring. Any further computation requires a new declaration; none is launched by this report.
