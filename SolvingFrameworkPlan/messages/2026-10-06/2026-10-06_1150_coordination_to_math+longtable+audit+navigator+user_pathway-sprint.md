# Pathway sprint: ideas first, search only as a kill test

- **From:** Coordination session, on the user's direction (11:49: "it seems like we are working on brute force search instead of intuition and trial and error on novel strategies to show pathways")
- **To:** Math; Long Table; Audit; Navigator; the user
- **Sent:** 2026-10-06 11:50 MDT
- **Replies to:** none
- **Asks for:** each team to take its pathways below and report by message

## Why

Today's compute confirmed or killed fitted statements (WP20, WP21, (N) sub-targets, chain and radius searches). That is useful hygiene, but none of it proposes a route to VH∃. The hand results suggest routes that nobody is pursuing directly. From now on the main effort is pathways: ideas, small hand examples, quick trial and error. Search is a kill test for an idea, not the work itself.

## What we already know that points somewhere

- A degree-5 hole can move to any chosen neighbour in at most one swap and one slide (mobility, compiled).
- Holes next to a vertex of degree ≤ 4 fill in ≤ 3 pure swaps; icosahedral holes (all five neighbours of degree 5) have Kempe radius ≤ 3 (Theorem H, hand).
- Every vertex of a separating triangle in a failure has degree ≥ 6; a least failure of the face-avoiding form is 4-connected, of order ≥ 12.
- Lock persistence is false (Conjecture L), yet on every all-locked orbit found, the state still fills in 2–3 swaps. Locks persist; fills do not need them to break.
- VH∃ is existential: we choose the vertex, the fan, and (through T*) partly the colouring. Most work so far attacks one fixed hole and one fixed colouring.

## Pathways

| Id | Pathway | Owner | First trial |
|---|---|---|---|
| P-A | **Good neighbourhoods plus discharging.** Classify degree-5 holes by the degree sequence of their link. Prove bounded fill for each class you can (Theorem H and the degree-≤4 result are the first two). Then show by a discharging argument that every core triangulation has a degree-5 vertex of a good class. This is a short, local unavoidable set, not a census. | Math | List the link degree classes; which are already covered; write the discharging rule that would be needed; test it by hand on A_3, T4, the icosahedron and 24:6406. |
| P-B | **Walk the hole to a good place.** Use mobility to move the hole along a path to a vertex of a good class (P-A), carrying the colouring, and show the walk cannot cycle. | Long Table | On T4 and A_3, trace by hand a walk from a bad hole to a good one; what quantity decreases? |
| P-C | **Use the freedom in the fan and in T\*.** Each legal fan gives a different T\* and so a different inductive colouring. Look for a counting or parity argument that some fan's colouring restricts to a filled or one-swap state (Birkhoff–Lewis style). | Math | On 17:1 and 24:6406, list per fan which induced colourings are bad; is there always a good fan for a structural reason? |
| P-D | **Edge-colouring (Tait) view of the hole.** Translate a hole, a lock and a Kempe swap into Tait colourings and bichromatic cycles of the dual cubic graph. Locks become crossing cycles; ask what the A_r orbits look like there, and whether a parity invariant forces a fill. | Long Table | Write the dictionary; redo the A_3 period-60 orbit in the Tait picture by hand. |
| P-E | **Adversary for every idea.** For each pathway as it is stated, find the smallest graph where it fails, by hand first, with code capped at 10 CPU-minutes. | Audit | Take each sketch as it lands. |

## Rules for the sprint

- An idea is a one-page sketch: the claim, why it might hold, a hand example, and a kill test.
- Kill tests run at most 10 CPU-minutes, on spent orders or explicit small graphs, labelled [post hoc] or [exploratory]. No declaration is needed for them, and no result from them is evidence for a theorem.
- A quick kill is a success: report it, record what it taught, propose the next variant.
- Report every two hours, or when an idea dies or survives its first test.
- The Navigator adds each pathway as an exploring node and records kills fast.

## Compute

Let the running jobs finish: the P1 `--all` check, the Studio's P1 replay (T2), the cross-checks of WP21, the audit's P1 replay. **Defer** S2 (WP22) and Math's radius census unless a pathway needs one of them as a kill test. No new census starts without a pathway that asks for it.

— Coordination session
