# Opus LP ladder: stopped state (11 Nov 2026 08:16Z)

k, 11 Nov 08:15Z: "ok lets stop everything for now while i regroup". Nothing is running in this
container (checked 08:16Z: no lane, check, watcher or launcher process). Nothing was deleted.
The lanes were already stopped at 05:00Z on k's reorientation note. Do not relaunch until k says so.

## Where each run stands

| run | family | state | resume from |
|---|---|---|---|
| k86GS23 (upper, eng_p8h) | K3gB5r b0ce409f + 365 keys 2485a27d + 14 HATBB b9ff66bd | killed 04:59Z after in02 | `warm/rows_k86GS23_snap_stop.txt` (223 lines) + `runK_k86GS22/warmlist.txt` + `warm/rows_k86GS22_snap_GS23.txt` |
| k86GL29 (lower, eng_p8l) | K3gB5n 1e1f35e8 + 357 keys 449bf4dd + p1r + consempty | ended, t1 = 0 on every pass; GL30 relaunch cancelled | `warm/rows_k86GL29_snap_GL30.txt` (1,396 lines), `launch_k86GL30.sh` |

## Bounds on K3gB5r + 365 keys + 14 HATBB

- Sound upper: t* <= 0.013046941 [E2] (GS23 in01, md5 cd2351e9, Studio ST-128).
- GS23 in02: 0.012893151 [P] (md5 57cb3529, filed in from_opus/s86_k86GS23/, no second check asked).
- Lower: no positive lower on this family (GL20..GL29 phase-1 t1 = 0).

## How to resume (only when k asks)

- Upper: copy `launch23.sh` to a new tag (never edit a used script), add
  `warm/rows_k86GS23_snap_stop.txt` to `WARM`, start from FEAS = `cand/sol_k86GS23_in02.json`
  (or in01 for an [E2] start). About 7.3 to 8.3 GB.
- Lower: `launch_k86GL30.sh` as written (about 4.7 GB). Pause it for each U86 check
  (`glswap86.py CAND OLDNUM`); the memcg limit is 14.3 GB and a check needs 2.5 GB free.
- `warmcache/` (18 files, 1.9 GB) is local only and not in git; if the container is reclaimed the
  first relaunch rebuilds it (slower, same result).

## Other Opus work, all parked

- beat_633 super-killer scan (read-only): `beat633_superkiller_scan/`. Merge sizing parked by the Lead.
- No third engine (Lead 05:30Z). Route (i) 2.126 glue pack delivered and built (`route_i_2o126/`).
