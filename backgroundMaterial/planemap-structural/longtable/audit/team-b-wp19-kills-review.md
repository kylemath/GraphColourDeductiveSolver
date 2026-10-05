# Team B: independent interpretation and certificates for the WP19 P3 kills

5 October 2026. Targeted audit of two already saved graphs, not a new census. `team-b-wp19-kills-check.py` implements its own colour canonicalisation, bichromatic-component traversal, move replay, legal-pair enumeration, and breadth-first search. It imports only the audit's graph validator and deletion-colouring enumerator, not the producer, its core, or its checker. Output: `team-b-wp19-kills-results.json`.

The raw phase input SHA256 is `30efe4e37251e62c6666a6756df754380be57af3cfe2412d9ff988e3dc2f0c2a`. Graph indices and vertex labels below use the stored zero-based numbering. A fill itself is not counted as a move.

## Graph 24:6406 kills C1 and C3, with exact m=3

The independent graph validator accepts the saved spherical triangulation. Its degree counts are fourteen degree-5 vertices, eight degree-6 vertices, and two degree-7 vertices. Independently enumerating every legal fan gives exactly 70 pairs, matching both the report and the C1 certificate's pair set, with no omissions or duplicates.

For every pair, we verify that its certificate start is a proper deletion colouring with the specified hole and distinct colours across both fan chords. We then enumerate every mixed reachable state through depth 2, including every whole-component Kempe swap and every legal singleton slide. None is a target. There are 35 distinct certificate starts across the 70 pairs; memoising repeated starts does not identify different holes. Consequently each legal pair has a start requiring at least three moves, which establishes m>=3.

For the matching upper bound, choose pair (0,0). We independently enumerate its entire admitted family of 134 colour-renaming orbits. Its exact mixed-distance histogram is

| Distance | Starts |
|---|---:|
| 0 | 22 |
| 1 | 81 |
| 2 | 28 |
| 3 | 3 |

Every start at that one pair reaches a target within three moves. Together with the all-pairs lower certificate, this proves exact m=3 without needing to accept all other reported upper histograms.

C1 states m(T)<=2 for every graph of order at least 18. This order-24 graph refutes it. C3 states that m(T)>=3 implies every vertex has degree 5 or 6. The verified antecedent m=3 and the two degree-7 vertices refute C3. The degree-7 fact alone would not refute C3; the all-pairs lower certificate is essential.

This graph does not refute C2 (m<=3): its exact value is 3. Nor is it a failure of vacancy reachability: pair (0,0) has a finite successful path for every start. It is a failure of the proposed two-move bound.

## Graph 24:7228 kills M2: exact ell=3, exact kappa=5

At pair (17,0), the root link is (7,16,23,18,8), with colours (3,1,0,1,2). The legal fan has apex 7 and added chords (7,23),(7,18). The supplied start is proper, has its only hole at 17, and is proper across both chords:

    [0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,4,1,0,2,1,3,0]

The supplied mixed path is

    S(8), K(1,2,seed=1), K(0,1,seed=0).

We replay it with canonicalisation after every move, as the certificate format requires. The initial slide transfers the unique link colour 2 and moves the hole from degree-5 vertex 17 to degree-6 vertex 8. Its successive hole-link colour lists are

    (1,3,2,1,0,3)
    (1,3,1,2,0,3)
    (1,3,1,2,1,3).

The last link omits colour 0 and fills at vertex 8. The two Kempe components and every intermediate state pass independent properness checks.

Independent shortest-path layers from this start are:

| Depth | New mixed states | Mixed targets | New Kempe-only states | Kempe-only targets |
|---|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 | 0 |
| 1 | 7 | 0 | 4 | 0 |
| 2 | 27 | 0 | 8 | 0 |
| 3 | 82 | 1 | 10 | 0 |
| 4 | — | — | 13 | 0 |
| 5 | — | — | 26 | 6 |

Thus the mixed distance is exactly 3, and the Kempe-only distance at the original hole 17 is exactly 5. An independently generated five-Kempe path is

    K(1,2,1), K(0,2,0), K(0,3,0), K(2,3,2), K(0,3,0).

It replays successfully and finishes with the original hole 17 still in place.

The raw kill certificate labels kappa as `lower`, with `kappa_lower=5`; by itself that establishes kappa>=5, not exact equality. This audit's five-swap path supplies the missing upper witness and makes kappa=5 exact.

M2 states kappa<=ell+1. Here 5>3+1, so M2 is refuted. A three-move mixed upper witness and absence of pure targets through depth 4 already suffice for the kill; exactness of both distances strengthens the interpretation. This does not contradict M3 or its reviewed theorem, whose condition is ell<=2. It supplies a separation beginning at mixed distance 3.

## Neither graph refutes U-exists or VH-exists

We additionally checked a successful U pair independently on each named graph. Add the fan chords and enumerate its complete colouring family and all Kempe classes in that augmented deletion graph. At each class, test for an unlocked member using target status or a one-Kempe target in the original deletion graph. Every generated augmented-graph swap remains in the independently enumerated start family, so class closure is checked rather than assumed.

* On 24:6406, pair (0,0) has 134 starts, eight augmented-graph Kempe classes, and zero wholly locked classes. Their class sizes are 92,36,1,1,1,1,1,1; every class has an unlocked member.
* On 24:7228, pair (17,0) has 188 starts, eight augmented-graph Kempe classes, and zero wholly locked classes. Their class sizes are 66,52,44,1,2,20,1,2; every class has an unlocked member.

Thus each graph actually satisfies U-exists at the explicitly checked pair, and therefore supplies no U-exists counterexample. Through the reviewed containment and unlocked-to-fill arguments, these successful pairs also satisfy the unbounded vacancy hypothesis for these individual graphs. A pure distance of five is finite; it is not a disconnected no-fill Kempe class. These are two finite verified exhibits, not proofs of U-exists or VH-exists for every triangulation.

## Audit scope

This check verifies the three kills and exact numbers on the two named graphs. It does not independently reproduce the entire 7,290-graph phase, establish minimal order for these phenomena beyond the earlier audited data, or alter any release/acceptance status. No new graphs were generated and no next-order computation was run.
