# S2-Verify report: independent verifier for the WP22 (S2) Kempe-radius search

Team S2-Verify (Long Table), 6 October 2026. Written from the specification only; no search code (wp22_*, lattack_*, astruct_*, lead_verify_L.py, ...) was read or imported. Standard library only. Nothing was git-added or committed. Longest run: 3 s, single process.

Files (in `backgroundMaterial/planemap-structural/longtable/`): `wp22v_verify.py`, `wp22v_tests.py`.

## Definitions as implemented

- State: oriented-face triangulation, hole h of degree 5, proper colouring of T-h, link with four colours. Canonical form: colours renumbered by first occurrence over increasing labels, hole skipped.
- Kempe swap: every unordered colour pair and every connected component of the induced subgraph of T-h (single vertices count), exchange the two colours on it.
- Filled: link uses at most 3 colours. Radius: least swaps to a filled state (layered BFS). Closed: BFS exhausts the class. Capped: visited states exceed the cap.
- State cap for `cert`/`census-check`: 300000 canonical states (`--cap` changes it), about 60 MB.
- Doubly locked: link in face-rotation order; repeated colour at x_j, x_{j+2}; m=x_{j+1}, a=x_{j+3}, b=x_{j+4}; m,a in one {col m, col a} component of T-h and m,b in one {col m, col b} component.
- F (used only in tests, for chain lengths): swap col x_j and col x_{j+3} on the component of x_{j+2}.
- Triangulation check: each face three distinct vertices; every directed edge in exactly one face and its reverse present; no repeated triangle; E=3n-6, F=2n-4, n-E+F=2; the rotation at every vertex is a single cycle; connected.
- A_r built from a-structure.md §1 (v=0, ring vertex (i,t)=1+5i+t, cap 5r+1; triangles listed in the docstring of `build_A`). Faces oriented by my own propagation routine.

## Commands

- `python3 wp22v_verify.py cert FILE.json [--cap N] [--orient]`: prints `RADIUS r`, `CLOSED-NO-FILLED class size N`, or `CAPPED`; prints whether the start is doubly locked; exit 0 confirmed, 1 contradicted, 2 capped or invalid (with a specific message). `--orient` repairs unoriented face lists (off by default).
- `python3 wp22v_verify.py census A_3|A_4|A_5|all [--out F.jsonl]`: all proper colourings of T-hole in canonical form (DFS enumeration), all 12 degree-5 holes, no symmetry used for the computation. The radius of every state comes from a multi-source BFS from the filled states (swaps are involutions); this is a different algorithm from the per-state BFS of `cert`, and `census-check` uses the per-state one. The 5-fold rotation is verified to be an automorphism and used only to group holes into classes, with equality of histograms inside each class checked.
- `census-check F.jsonl [--limit N]` (default 2000, evenly spaced, 0 = all): recomputes properness, canonical form, doubly-locked flag and radius per record by per-state BFS. Graph names `A_r` are rebuilt by my own construction; others are skipped.
- `planted`: target predicate "link uses at most 1 colour".
- `python3 wp22v_tests.py`: 32 checks.

## Results

Graph sanity: A_3, A_4, A_5 have orders 17, 22, 27, only degrees 5 and 6, twelve vertices of degree 5 each. My A_3 has exactly the edge set of the witness constant `A3_FACES` (data compared only).

Census (every doubly locked state, all 12 holes; DL = doubly locked states, per hole):

| graph | hole class | canonical states / 4-link / DL | radius histogram per hole |
|---|---|---|---|
| A_3 | v and cap (2 holes) | 100 / 60 / 30 | {2:20, 3:10} |
| A_3 | ring 0, ring 2 (10 holes) | 80 / 40 / 14 | {2:14} |
| A_4 | v and cap | 520 / 320 / 80 | {2:80} |
| A_4 | ring 0, ring 3 | 400 / 200 / 28 | {2:28} |
| A_5 | v and cap | 2720 / 1680 / 530 | {2:530} |
| A_5 | ring 0, ring 4 | 2080 / 1040 / 202 | {2:202} |

Totals over the 12 holes: A_3 {2:180, 3:20}, A_4 {2:440}, A_5 {2:3080}. No infinite radius anywhere; every Kempe swap stayed inside the enumerated space (completeness check). The histograms agree inside every rotation class (symmetric-consistent True). The numbers 1680 (A_5, 4-link canonical states) match the a-structure.md count 10080 / 6. Census-check on my own output: A_3 200/200, A_4 440/440, A_5 300 of 3080 (every 10th), 0 mismatches.

Regression cases (all reproduced):
- W6 (hole 16): strict orientation accepted, start doubly locked, radius 2; F-chain length 6 as stated in l-attack.md.
- A_3 centre: the witness colouring is doubly locked with radius 3; 20 canonical infinite-chain classes (as a-structure.md); the 4 with ring 0 = 01023 have radii [2,2,3,3] (3 for 2 of 4); all 20 classes have radius 2 or 3 (10 each).
- T4 (hole 4): 68 canonical states, 22 filled; histogram over all states {0:22,1:25,2:15,3:4,4:2}; over the 21 doubly locked {2:15,3:4,4:2}; nothing unreached. A radius-4 state passes through `cert`.
- Planted: with the unreachable target the class is CLOSED with size equal to an independent flood fill (A_3 centre: 100; T4: 68, the whole space); with the true target the radius is reported. The claim logic confirms a targetless claim on the planted result and contradicts it on the true one.
- Mutation tests, each with its own message: corrupted colour ("improper colouring: edge (1,5) is monochromatic"), missing colour, deleted face and reversed face and relabelled vertex ("NOT-TRIANGULATION: directed edge ..."), wrong hole degree, claim of radius 3 (true 2: "CONTRADICTED ... recomputed radius 2"), targetless claim on a class that has a filled state, a census record with a wrong radius (reported, exit 1), and a cap of 3 states (CAPPED, exit 2).

Disagreement with expected values: none. Every expected number was reproduced by code written without sight of the other implementations.

## Ambiguities in the specification and the reading taken

1. T4's face list in MathConjectureR.md is not consistently oriented (e.g. (0,1,2) and (0,1,5) both contain the directed edge 0->1), while the interface says "oriented triangles, ccw". The strict certificate check rejects it; the tests orient it with `orient_faces` (a helper; `cert --orient` exposes it). A search team that emits T4-style unoriented lists will be rejected by default. Radii do not depend on orientation, but the link order does only up to reversal, which the double-lock test is symmetric under (both locks are required).
2. `faces_sha256` in the census format has no stated definition. I define it as sha256 of repr(sorted faces, each rotated to start at its smallest label). `census-check` reports a hash difference as information only, never a failure. The two teams must agree on one definition.
3. The census labelling is not stated in the interface. I assumed the audit labelling (v=0, ring (i,t)=1+5i+t, cap 5r+1), which a-structure.md §1 states and which matches the witness. A census file with another labelling would fail `census-check` on properness or hole checks.
4. "Holes up to the 5-fold symmetry": I enumerate all 12 holes without using symmetry (4 hole classes), so a census file that lists only one hole per class is checked on the records present and nothing more. Records for the other holes are not required by `census-check`.
5. `radius` for infinite: the record format does not say how it is written; `census-check` accepts null, "inf" or -1.
6. Claim `class_size`: I read it as the number of canonical states in the Kempe class of the start state, including the start. "CLOSED-NO-FILLED" in `cert` reports the same count.
7. Whether an already-filled start has radius 0: not reachable in a state (the link must have four colours), so `cert` rejects it as invalid.
8. Filled targets with a link of 2 colours are included in "at most 3 colours".

## Not done

- No check against protected-face definitions (not part of the task).
- `census-check` for A_5 was run on every 10th record, not all (the full file takes about a few seconds, so this is an easy extension; A_3 and A_4 were checked in full).
- Only A_r with r = 3,4,5 in the census; no cross-check against a search team's census file, since none existed.
- Cap behaviour on a real large class was only tested with an artificially tiny cap; the largest class met was 2720 states.
