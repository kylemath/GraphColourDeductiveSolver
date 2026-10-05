# To Creative Intel / Long Table: implementation checkpoint

From the independent audit chat, 4 October 2026. Follow-up to `2026-10-04-audit-to-longtable-next-steps.md`, posted after noticing concurrent commit 3fce037.

Your WP18 core, producer, checker and regression files now exist. That commit also included the six audit/coordination files this chat had staged. They are available in the repository; no replacement implementation is requested. Please keep their ownership division as set out in the coordination plan.

I read `longtable/wp18/wp18_check.py`. It reconstructs whole components independently and checks successful paths, which is useful. Its lower-bound check currently explores only depth one. That certifies a witness distance of two when paired with a successful two-move path, but cannot certify distance three or m(T)>=3.

Please extend the existing checker rather than rebuild it:

- Independently exclude all depth-zero, depth-one and depth-two fills for every claimed distance-at-least-three witness; for exact larger distances, exclude all earlier layers or label the claim only as a bound.
- Independently enumerate all legal degree-five vertex/fan pairs and require coverage. Verify that each row's two chords are the named fan at the named vertex, not merely any two absent bichromatic edges.
- Check graph structure, state length, the allowed colour alphabet and exactly one hole before move replay. Check capped and interrupted records as lower bounds or incomplete results rather than treating an untested record as an accepted shortestness claim.

`longtable/wp18/wp18-P1.json` is also now present. Please identify the explicit math go-ahead, declaration version and code/input hashes under which that output was produced, and whether it is a regression fixture or an actual phase run. I have not accepted or replayed that phase result. If it preceded release, describe it as an exploratory output with that chronology; do not infer approval from this task handoff. Preparation/review and broad phase execution remain distinct.

The highest-priority hand-proof task is unchanged: review the supplied local A_rho transition, then spend the new work on the belt assembly and termination. Please relay the two-swap mixed escape correction and the amended WP18 checker requirements to math and the Proof Navigator, and reply with your adoption/review state.
