#!/bin/bash
# maclane k5g add-on: recheck an upper point on the check family of suffix x (K3l5x) + the 240-key file with the eng_p1r engine: the
# exhaustive upperR2 (gkwin gkleaf; flags c6le f2b7 f2b=<rules c67fa1d1> rpatN=<rpatN3 rotation-justified>), as recheck_k5e.sh does for
# K3l5e.  About 5 min and ~1.6 GB on 1 thread.  The family must pass fam_lib.py famcheck (FAMILIES.txt line, md5s, chain).
# usage: bash recheck_fam.sh <suffix> <point> [threads, default 1]
#   point: a name in cand/ (repS2MW_03 or sol_repS2MW_03), in outbox/upper/ (also <name>__K3l5e), or the path of a sol json
# env: RECHECK_TAG (default F_<name>_K3l5<x>), RECHECK_UPPER (1; 0 = do not file into outbox/upper)
# v2d (Opus 9 Nov): KEYS=<key file> (a path, or a name in p1r/; default the 240 keys p1r/cg_keys_r13w16_16fik.txt) checks on that key
#   file; it must be a known one (k5e_lib.py keyscheck).  On another key file than the 240 keys the default tag and the outbox family
#   carry its label (260 keys: tag F_<name>_K3l5<x>_k260, family K3l5<x>_k260), so the 240-key check of the same point is kept.
# Result: logs/upper_<tag>.log, a run.log line; in outbox/fam/: the log and one line in RECHECK.txt (name  md5 (8)  family  verdict  log
# checked-at); when FEASIBLE: outbox/upper/sol_<name>__K3l5<x>.json + .log and a POINTS.txt line with family K3l5<x>.  Exit status 0 =
# FEASIBLE, 1 = not FEASIBLE, 2 = could not run.  A killed check leaves its work dir; it is cleared before a new check of the same tag.
R=/tmp/maclane-k86
N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
SD=$R/fs/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sD
PATH=$R/macshim:$PATH; export PATH
X=$1; P=$2; TH=${3:-1}
[ -n "$X" ] && [ -n "$P" ] || { echo "usage: bash recheck_fam.sh <suffix> <cand name, outbox/upper name or sol json> [threads]" >&2; exit 2; }
FC=$(python3 $N/fam_lib.py famcheck $X quiet) || { echo "recheck_fam: family $X: $FC" >&2; exit 2; }
KEYS=${KEYS:-$N/p1r/cg_keys_r13w16_16fik.txt}
case "$KEYS" in */*) ;; *) KEYS=$N/p1r/$KEYS ;; esac
[ "${KEYS#/}" != "$KEYS" ] || { [ -f "$KEYS" ] && KEYS=$(cd "$(dirname "$KEYS")" && pwd -P)/$(basename "$KEYS"); }
KC=$(python3 $N/k5e_lib.py keyscheck $KEYS) || { echo "recheck_fam: keys: $KC" >&2; exit 2; }
KL=$(echo "$KC" | awk '{print $4}'); [ "$KL" = - ] && KL=""
ARG=$(echo "$FC" | sed -n 's/.* l=\([^ ]*\) .*/\1/p'); FAMN=K3l5$X$KL
if [ -f "$P" ]; then SOL=$(cd "$(dirname "$P")" && pwd -P)/$(basename "$P")
elif [ -f $N/cand/$P.json ]; then SOL=$N/cand/$P.json
elif [ -f $N/cand/sol_$P.json ]; then SOL=$N/cand/sol_$P.json
elif [ -f $R/outbox/upper/$P.json ]; then SOL=$R/outbox/upper/$P.json
elif [ -f $R/outbox/upper/sol_$P.json ]; then SOL=$R/outbox/upper/sol_$P.json
else echo "recheck_fam: no point $P (looked for it as a file, cand/$P.json, cand/sol_$P.json and in outbox/upper/)" >&2; exit 2; fi
NAME=$(basename $SOL .json); NAME=${NAME#sol_}; NAME=$(echo $NAME | sed -E 's/__K3[A-Za-z0-9]*(_[A-Za-z0-9]+)?$//')
TAG=${RECHECK_TAG:-F_${NAME}_$FAMN}
for f in $N/eng_p1r/bin/jsepf_gk_k192 $N/eng_p1r/bin/jsepf_gk $N/eng_p1r/bin/jsep3; do [ -x $f ] || { echo "recheck_fam: $f missing (bash build.sh)" >&2; exit 2; }; done
pgrep -f "work=$SD/wr86r_$TAG " > /dev/null && { echo "recheck_fam: a check with tag $TAG is running already" >&2; exit 2; }
rm -rf $SD/wr86r_$TAG
echo "recheck_fam: $NAME on $(basename $ARG) + $(basename $KEYS) ($(echo "$KC" | awk '{print $3}')), engine eng_p1r, $TH thread(s): log $N/logs/upper_$TAG.log"
E86OVR=$N/eng_p1r STACK=s77 ARGS=$ARG KEYS=$KEYS bash $N/U86e.sh $TAG $SOL $TH \
  c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt
V=$(grep '^UPPER-R2' $N/logs/upper_$TAG.log | tail -1); [ -n "$V" ] || V="no verdict ($(grep -c Traceback $N/logs/upper_$TAG.log) tracebacks)"
O=$R/outbox/fam; mkdir -p $O; cp $N/logs/upper_$TAG.log $O/
echo "$NAME    $(md5sum < $SOL | cut -c1-8)    $FAMN    $V    upper_$TAG.log    $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $O/RECHECK.txt
echo "recheck_fam: $NAME: $V"
case "$V" in "UPPER-R2: FEASIBLE"*) ;; "UPPER-R2: "*) exit 1;; *) exit 2;; esac
if [ "${RECHECK_UPPER:-1}" != 0 ]; then echo "recheck_fam: outbox/upper: $(python3 $N/fam_lib.py file $X sol_$NAME $SOL $TAG)"; fi
exit 0
