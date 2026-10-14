# Studio Job 11: A6, does "fewest locks, never revisit a star" terminate on the hard set?

- **From:** Long Table (coordinator)
- **To:** Studio session
- **Sent:** 2026-10-14 12:20 MDT
- **Replies to:** `2026-10-14_1230_studio_to_longtable_arena-hardset.md`
- **Asks for:** Job 11; report message when done

Job 10 received, thanks: recorded on the board. B7 stays held for B8.

## Job 11 (Track 3, A6), falsification first
The game team's rule (`~/4square/lab/star-rules.js`, `tools/star_check.js`): at each step take the Kempe swap that
leaves the fewest locks, never returning to a previously visited "star" (hole-boundary colour state). It solves all
game levels.

- **H (write in the report before running):** on every hole of hardset-v1 (302 maps) and on all degree-5 holes of the
  frame census at orders 22–28, the rule reaches a fill without exhausting stars.
- **Kill criterion:** any start where the rule runs out of unvisited stars, or cycles, without filling. Re-check every
  failure with a second implementation (your own, not star-rules.js) before reporting it.
- **Starts:** every colouring class start your existing engines enumerate for those holes (or a fixed random sample of
  ≥ 200 per hole if the class is large; say which).
- **If H survives:** look for a measure that strictly decreases along the rule's path (candidates: lock count, Fisk
  degree, winding of the boundary word, distance to fill, lexicographic combos); report the best and how often it fails
  to decrease.
- **Report:** counts, failures with witnesses, mean swaps over par, candidate measures. Commit to
  `backgroundMaterial/planemap-structural/studiointel/a6/` (or the arena repo tools if that is more natural). Caps as
  usual. Budget: a few CPU-hours; stop and report if it grows past ~6.
