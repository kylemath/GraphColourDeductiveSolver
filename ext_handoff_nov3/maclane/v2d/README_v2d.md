# maclane v2d: key-file override and a parallel upper lane (k86MS7 = K3l5j + 260 keys beside k86MS6)

**Why.** Studio ask (9 Nov): run MS7 on K3l5j with the 260-key file (0470c459 = the 240 keys + W6b-16p's 20, the keys of the
container's k86GS12) as a test, with MS6 (240 keys) as the control, without stopping MS6. Before v2d the 240-key path was fixed in
launch_msfam.sh (line 53), recheck_fam.sh (line 31) and k5e_lib.py (K240, the verified-point check), and a running PREV_TAG was refused.

**What changes** (5 files replaced, one added; on the 240 keys every command behaves as before).
- `launch_msfam.sh`: `KEYS=<key file>` (a path, or a name in p1r/; default the 240 keys). The file must be a known one with its md5
  (`k5e_lib.py keyscheck`: cg_keys_r13w16_16fik.txt 3d996dbb, cg_keys_r13w16_16fikp.txt 0470c459; `KEYS_UNLISTED=1` accepts another).
  The K run, in-point watch, ladder (REPL_KEYS) and tightening all get it. The in-point must be FEASIBLE on K3l5x **+ that key file**
  (a 240-key check does not count for a 260-key lane). `PARALLEL=1` starts the lane while PREV_TAG runs (warm = PREV_TAG's warm list +
  a snapshot of its rows, as for a switch); without it a running PREV_TAG is refused as before. A tag keeps its key file: relaunching
  a tag on another key file is refused (`KEYS_SWITCH=1` overrides).
- `recheck_fam.sh`: `KEYS=` as above. On a non-240 key file the default tag and outbox family carry the key label, so the 240-key
  check of the same point is kept: tag `F_<name>_K3l5j_k260`, family `K3l5j_k260`.
- `k5e_lib.py`: known key files (KNOWN, KLABEL), `keyscheck`, `lanekeys <tag>` (the key file of the tag's newest launch line in
  run.log), `verified <json> [keys]`; `state` takes keys; `base_name` strips a labelled family.
- `fam_lib.py`: `verified / state / pick <..> [keys basename]`; `outpass` files a lane's points on its own key file (from its launch
  line) under `K3l5<x><label>` / `K3gB5<x><label>`; `file` uses the key file of the check it files; a 240-key `pick` never offers a
  labelled point. New: `lanekeys <tag>`.
- `outbox86_fam.py`: passes the lane's key file to outpass; its log lines name the labelled families and the key file.
- `p1r/cg_keys_r13w16_16fikp.txt` (new, 0470c459, 260 keys, 93 payer-7: eng_p1r uses bin/jsepf_gk_k192 as for the 240).

**Labels.** Points of a 260-key lane are filed as `<name>__K3l5j_k260` (or `__K3gB5j_k260`), family column `K3l5j_k260`. They are
uppers for K3l5j **with the 260 keys**; quote them with the key file (0470c459), never as plain K3l5j.

**Container tests** (a mock pack tree, dummy engine and U86e.sh writing real-format run.log lines): keyscheck accepts both files and
refuses an edited copy or an unlisted name; recheck on 240 and on 260 keeps both checks and files both points; a 260 lane refuses an
in-point checked only on 240 keys; without PARALLEL a running MS6 is refused (exit 3), with it MS7 starts and every child gets KEYS
(K run, watch86, tightwatch, repladder REPL_KEYS); the MS7 outbox files its 260-checked points as `_k260` (in-point, ladder K3gB5j_k260),
ignores a 240-only check, and the MS6 pass files 240 points as K3l5j; 240 / 260 picks stay separate; restart guards hold.
install_v2d.sh checked on a tree with the k5e / k5g / v2c files: dry, install, idempotent rerun, refusal on a wrong md5.

**Studio commands.** H = this folder on the Mac; R = ~/maclane/maclane-k86 path the pack uses (/tmp/maclane-k86); N = R/fs/.../s86_f2b7.
```
DRY=1 bash H/install_v2d.sh        # checks the pack and the installed md5s (launch_msfam 41bbab63 v2c or 74a41d8a k5g, recheck_fam
bash H/install_v2d.sh              #   a2716a38, k5e_lib 69bb7d60, fam_lib 60e58489, outbox86_fam ac5e8991); backups *.pre_v2d
KEYS=cg_keys_r13w16_16fikp.txt bash R/recheck_fam.sh j <MS6's in-point> 2       # ~5 min: FEASIBLE on K3l5j + 260 keys here
DRY=1 KEYS=cg_keys_r13w16_16fikp.txt PARALLEL=1 TAG=k86MS7 PREV_TAG=k86MS6 FAM_SUFFIX=j bash N/launch_msfam.sh <in-point json>
KEYS=cg_keys_r13w16_16fikp.txt PARALLEL=1 TAG=k86MS7 PREV_TAG=k86MS6 FAM_SUFFIX=j bash N/launch_msfam.sh <in-point json>
bash R/status_fam.sh k86MS7 ; bash R/status_fam.sh k86MS6        # name the tag: the default is the newest lane
bash R/stop_fam.sh k86MS7                                         # stops only MS7; its last outbox pass is on the 260 keys
```
Knobs for MS7 as before (UPPER_THREADS, MAXIT, REPL_PAR, REPL_MINMEM, TIGHTWATCH); the defaults copy MS6's from run.log, so two lanes
double the Mac's load unless you lower them. Do not use launch_upper_fam.sh while both lanes run: it moves only the newest lane
(MS7). Running MS6 processes keep the code they loaded; the install does not touch them.
