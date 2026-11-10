#!/bin/bash
# maclane v2e smoke (Opus 10 Nov): the Mac's own build of eng_p8 against the same tests the container ran on the mock Studio tree.
# One engine run at a time on K3l5n (args_A97_F_W13K3l5n.txt), flags c6le f2b7 f2b=<rules c67fa1d1 + A5 twins> rpatN=<rpatN3 rot.-justified>:
#  0 installed: eng_p8 = ENG_P8.md5, its three binaries (build_v2e.sh), the 268-key file known (keyscheck) and needing eng_p8 (keyseng)
#  1 p8reftest  (ref/keys_p8bb_test.txt = the 8 payer-8 keys + every 12th of the 260; N=1500 receivers per d = 7..10): P8REFTEST: PASS
#  2 gkwintest  (same keys, N=1500): GKWINTEST: PASS
#  3 F2B self-test on the 268 keys, point ref/sol_k86MK1_in23_p8bb_amt.json (sol_k86MK1_in23 + amounts 0.011..0.0173 on the 8 new keys),
#    f2bself=SMOKE_F2B (default 200) arrangements per d: python exact vs this Mac's C++ leaf / WIN: F2B-SELFTEST: PASS
#  4 planted control: step 3 with flag gkoplant (WIN drops the sg = -1 W5 OUT term): must end F2B-SELFTEST: FAIL
# env: SMOKE_MINMEM (MB to wait for before each run; 0 = no wait), SMOKE_THREADS (2), SMOKE_F2B (200).  About 5-15 min.
# usage: bash smoke_v2e.sh      must end "SMOKE-V2E: PASS" (writes <pack>/smoke_v2e.ok); logs <pack>/smoke_v2e*.log
R=/tmp/maclane-k86
B=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7; NN=$N
SD=$R/fs/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sD
PATH=$R/macshim:$PATH; export PATH
. $N/maclib.sh
H=$(cd "$(dirname "$0")" && pwd -P); E=$N/eng_p8; K268=$N/p1r/cg_keys_r13w16_16fikp_p8bb.txt
V2KT=$H/ref/keys_p8bb_test.txt; V2PT=$H/ref/sol_k86MK1_in23_p8bb_amt.json; NF=0; LOG=$R/smoke_v2e.log
say() { echo "$*" | tee -a $LOG; }
ok() { say "   OK   $*"; }
bad() { say "   FAIL $*"; NF=$((NF + 1)); }
: > $LOG; rm -f $R/smoke_v2e.ok
say "maclane v2e smoke, $(date -u +%Y-%m-%dT%H:%M:%SZ) on $(uname -sm)"

say "0. installed files"
D=$(python3 -c "
import sys, os, hashlib
d, mf = sys.argv[1], sys.argv[2]
want = dict(l.split()[::-1] for l in open(mf) if l.strip())
have = dict((f, hashlib.md5(open(os.path.join(d, f), 'rb').read()).hexdigest()) for f in os.listdir(d) if f.endswith(('.py', '.cpp')) and os.path.isfile(os.path.join(d, f)))
bad = [f for f in sorted(set(want) | set(have)) if want.get(f) != have.get(f)]
print('%d files, %d differ %s' % (len(want), len(bad), bad[:3])); sys.exit(1 if bad else 0)
" $E $H/ENG_P8.md5 2>&1) && ok "eng_p8 = ENG_P8.md5 ($D)" || bad "eng_p8 differs from ENG_P8.md5 ($D): bash $H/install_v2e.sh"
for b in jsepf_gk_k192 jsepf_gk jsep3; do [ -x $E/bin/$b ] || bad "eng_p8/bin/$b missing: bash $H/build_v2e.sh"; done
KC=$(cd $N && python3 k5e_lib.py keyscheck $K268) && ok "$KC" || bad "keyscheck: $KC"
[ "$(cd $N && python3 k5e_lib.py keyseng $K268)" = eng_p8 ] && ok "keyseng: the 268 keys need eng_p8" || bad "keyseng does not say eng_p8 for $K268"
for f in $V2KT $V2PT; do [ -s $f ] || bad "$f missing"; done
[ $NF = 0 ] || { say "SMOKE-V2E: FAIL ($NF)"; exit 1; }

# run <name> <pcheck command> <keys> <sol or -> <threads> [extra flags]  -> $R/smoke_v2e_<name>.log
run() {
  memgate ${SMOKE_MINMEM:-0}
  local nm=$1 cmd=$2 ky=$3 sl=$4 th=$5; shift 5
  (
    export STACK=s77 ARGS=$NN/args_A97_F_W13K3l5n.txt KEYS=$ky FAM=full KS=0; unset EGK; . $NN/env86.sh; N=$NN
    WK=$SD/v2esmoke_$nm; rm -rf $WK; mkdir -p $WK; cd $N/eng_p8
    nice -n 12 python3 pcheck.py $cmd $F $X nomax $( [ "$sl" = - ] || echo sol=$sl ) $A threads=$th work=$WK gkeys=$KEYS gkwin gkleaf \
      c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt "$@" > $R/smoke_v2e_$nm.log 2>&1
    rm -rf $WK
  )
}
verdict() { grep -E "$2" $R/smoke_v2e_$1.log | tail -1; }
TH=${SMOKE_THREADS:-2}; NS=${SMOKE_F2B:-200}

say "1. p8reftest (eng_p8 key coefficients vs W6b's p8_ref.py), $(grep -vc '^#' $V2KT) keys, N=1500"
T0=$(date +%s); run p8ref p8reftest $V2KT - 1 N=1500 seed=11; V=$(verdict p8ref 'P8REFTEST:')
case "$V" in "P8REFTEST: PASS"*) ok "$V ($(( $(date +%s) - T0 )) s)";; *) bad "${V:-no verdict} ($R/smoke_v2e_p8ref.log)";; esac

say "2. gkwintest (window IN >= exact IN, W5 OUT <= exact OUT), same keys, N=1500"
T0=$(date +%s); run gkwin gkwintest $V2KT - 1 N=1500 seed=11; V=$(verdict gkwin 'GKWINTEST:')
case "$V" in "GKWINTEST: PASS"*) ok "$V ($(( $(date +%s) - T0 )) s)";; *) bad "${V:-no verdict} ($R/smoke_v2e_gkwin.log)";; esac

say "3. F2B self-test on the 268 keys (this Mac's C++ leaf / WIN vs python exact), f2bself=$NS, $TH threads"
T0=$(date +%s); run self upperR2 $K268 $V2PT $TH f2bself=$NS seed=11; V=$(verdict self 'F2B-SELFTEST: (PASS|FAIL)')
case "$V" in "F2B-SELFTEST: PASS"*) ok "$V ($(( $(date +%s) - T0 )) s): $(grep -E '^ *F2B-SELFTEST d=' $R/smoke_v2e_self.log | sed 's/,.*worst/; worst/' | cut -c1-90 | tr '\n' ' ')";;
  *) bad "${V:-no verdict} ($R/smoke_v2e_self.log)";; esac

say "4. planted control gkoplant (must FAIL)"
T0=$(date +%s); run selfCTL upperR2 $K268 $V2PT $TH f2bself=$NS seed=11 gkoplant; V=$(verdict selfCTL 'F2B-SELFTEST: (PASS|FAIL)')
case "$V" in "F2B-SELFTEST: FAIL"*) ok "control fails as required: $V ($(( $(date +%s) - T0 )) s)";; *) bad "the planted control did not FAIL: ${V:-no verdict} ($R/smoke_v2e_selfCTL.log)";; esac

if [ $NF = 0 ]; then date -u +%Y-%m-%dT%H:%M:%SZ > $R/smoke_v2e.ok; say "SMOKE-V2E: PASS"; echo "$(date -u +%H:%M:%SZ) [maclane] smoke_v2e PASS" >> $N/run.log; exit 0
else say "SMOKE-V2E: FAIL ($NF)"; exit 1; fi
