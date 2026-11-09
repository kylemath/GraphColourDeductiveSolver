# maclane v2d1: side-lane tags k86MK<n> (on top of v2d)

**Why.** The Studio tags the 260-key test lane k86MK1, so it cannot collide with the k86MS<n> numbers that a family switch picks
(launch_upper_fam.sh names its next lane k86MS<max n + 1>). v2d's launch_msfam.sh refused any tag but k86MS<n>, and stop_fam.sh refused
to stop one.

**What changes.**
- `launch_msfam.sh`: TAG may be k86MS<n> or k86MK<n>. Nothing else differs from v2d.
- `stop_fam.sh`: stops a k86MK<n> lane by name; its last outbox pass uses the lane's own key file, as in v2d.
- `status_fam.sh`: its "NOTE: <tag> is running too" line also lists k86MK lanes.

fam_lib.py `lane` (and so launch_upper_fam.sh, and the no-argument default of status_fam.sh / stop_fam.sh) still sees only k86MS<n>.
That means a family switch never stops or moves MK1. The repair ladder names MK1's points sol_repK1MW_NN; no MS lane before MS11 uses
"K1".

**Container tests** (the v2d mock tree): with MS6 running, MK1 launches with PARALLEL=1 and the 260 keys; its in-point
(sol_k86MK1_in01) and ladder (sol_repK1MW_01) points are filed as __K3l5j_k260; `fam_lib.py lane` stays k86MS6; `stop_fam.sh k86MK1`
stops only MK1 and makes its last pass on the 260 keys; install_v2d1.sh passes dry, install and rerun, and refuses when v2d is not
installed.

**Studio commands.**
```
DRY=1 bash install_v2d1.sh; bash install_v2d1.sh      # needs v2d (k5e_lib 839623aa, fam_lib 67daca90); replaces launch_msfam 91af83c3,
                                                      #   stop_fam 8de63ed3, status_fam 31eae46f; backups *.pre_v2d1
KEYS=cg_keys_r13w16_16fikp.txt PARALLEL=1 TAG=k86MK1 PREV_TAG=k86MS6 FAM_SUFFIX=j bash $N/launch_msfam.sh <in-point json>
bash /tmp/maclane-k86/status_fam.sh k86MK1 ; bash /tmp/maclane-k86/stop_fam.sh k86MK1
```
