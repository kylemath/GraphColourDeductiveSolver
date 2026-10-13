# Two-hole game support: shelved (13 Oct 2026)

The user stopped this feature before it was finished. The bug risk across 14 skins and the app UX was not worth it,
so the game stays single-hole. These files are kept for reference only and are not used anywhere.

- `twin_map.py`: was `~/4square/tools/twin_map.py`. It glues a map to its mirror copy along a face triangle, keeping
  both holes. Checked as a planar triangulation on trap17, c30, six, r178 and ico.
- `core-js-two-holes.patch` and `core.js.two-holes`: an unfinished rewrite of `~/4square/lab/core.js`, with a list of
  holes and both win rules. Twin distances came from the base map's census table plus a bounded exact search.
  It was never tested in a browser and was reverted in `~/4square`.
