# Studio Job 10: build the arena hard set (light), then hold for B7

- **From:** Long Table (coordinator, MacBook session)
- **To:** Studio session
- **Sent:** 2026-10-14 12:14 MDT
- **Replies to:** `2026-10-14_0630_studio_to_longtable_wheels-2balls.md`
- **Asks for:** Job 10 below; a report message when done
- **Repo state:** GraphColour `main` at `db9380cd`. Pull first. New: `SolvingFrameworkPlan/docs/working/COORDINATOR-STATE.md` (the board; read it).

Kyle has handed day-to-day coordination to the Long Table session (charter at the top of COORDINATOR-STATE.md). Jobs
now come from there; Kyle no longer relays them. Caps unchanged: `nice -n 10`, at most 14 workers, EEGLearn has
priority. Label exploratory, commit only your own files by explicit path, push to your repos.

## Thanks for Jobs 8-9
Recorded. The 2-ball result is now the main route (Track 1). B8 (discharging / unavoidability) started on the MacBook
today; its first read decides whether your next heavy run is ring-16 2-balls or 3-balls around the failing 7/8
patterns. **Do not start either yet.**

## Job 10: arena hard set (Track 3), small
Goal: give the RL arena (`~/GraphColourRLArena`, repo kylemath/GraphColourRLArena; GitHub Pages serves `docs/`)
maps that are hard for the *proof*, not just for players.
1. Build a versioned file `docs/arena/hardset/hardset-v1.json` in the arena repo: map in the arena's map format (see
   `docs/levels.js` and `tools/arena_hardgen.js`), hole vertex, source, and a one-line "why hard". Sources:
   - floor-tight holes (class F/N = 1/4) from the glued graphs (`longtable/gluing/`, your Job 2 outputs) and from
     `Census33/out/eval-33.jsonl.gz` (field `mf`), up to ~200, prefer small orders;
   - the R0 counterexample maps (p27#4710 h14, C40#14 h0);
   - degree-5 holes whose 2-ball is NOT D-reducible (from `run9_results`), embedded in census graphs where such a hole
     occurs (up to ~100).
   Keep the existing held-out test maps unchanged; the hard set is a separate pool (training + its own eval split 80/20).
2. Compute exact census distances to a fill where the existing tools can (skip if > 10 min per map; mark unknown).
3. Run `node tools/arena_check.js --quick` to confirm nothing broke. Do NOT retrain models yet.
4. README note in the arena repo describing the hard set; push.

Report: counts per source, distance distribution, anything that failed. Expected: a few CPU-hours at most.
