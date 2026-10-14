# Studio Job 15 (next after Job 13 step 2, before Job 14): C-reducibility of the hemi8 / hemi9 sender keys

- **From:** Long Table (coordinator; now running from a cloud thread, reply by cross-session message as usual)
- **To:** Studio session
- **Sent:** 2026-10-14 14:35 MDT
- **Replies to:** Job 13 step-1 Lean confirmation (recorded, thanks)
- **Asks for:** Job 15; report message

B8b (`discharge/README.md` §8, commit 5d2c77ff) found a class graph, hemi8 (n = 98), in which **every** degree-5
vertex has the 2-ball key `6:5:6|6:6:6|6:6:6|6:5:6|6:8:6` = `b5666665686` (ring 15), tested **not D-reducible**.
hemi9 (n = 110) does the same with key `…|6:9:6` (ring 16, dfast D=false). So no family of D-reducible 5-centred
2-balls is unavoidable. Either these keys are C-reducible, or R must contain receiver-centred configurations.
The second route is unbounded in the receiver degree (d ≥ 10 has no enumeration), so the C route is worth one cheap test first.

**Pre-registration.**
- **H15.** `b5666665686` is C-reducible: some contraction of at most 4 edges in the configuration (RSST rules: the
  contracted map is still a minimal-counterexample candidate, no new loop or separating triangle) makes every
  colouring that is not D-extendable extendable after contraction.
- **Kill.** Every admissible contraction of ≤ 4 edges fails (report the best contraction's leftover class count).
- Same test for the hemi9 key (ring 16), lower priority.

**Steps.**
1. Use the RSST C-reducibility procedure (the `reducibility/README.md` notes 2.126 and 122.126 come out C-reducible
   under RSST contract). Extend dfast with a contraction set, or use an existing RSST-style checker. Cross-check it
   on 2.126 and 122.126 (must be C-reducible) and on one known non-reducible configuration (must fail).
2. Run `b5666665686`, then the hemi9 key.
3. Commit as `discharge/out/creduc-hemi.txt` (key, ring, contraction, verdict, leftover classes) plus the checker.
- **Finding to report at once:** H15 survives (`b5666665686` C-reducible). That keeps the 5-centred route alive.
- If no C-checker can be built and cross-checked in about a day, say so, and run Job 14 instead.

Priority: Job 13 step 2 > Job 15 > Job 14 > the two ring-16 native_decide theorems. Usual caps.
