#!/bin/bash
# code_gk8 (9 Nov 2026): default code dir code_gk8 (payer-8/9 GK keys, PAYER8SPEC W5); run17.sh there defaults SEPBIN=sep3r_gk8.
# code_gk9 (10 Nov 2026): default code dir code_gk9 (code_gk8 + HATBB keys, HATBB_SPEC a36ce8d2); the stamp also covers hbfam.py and hb_blocks.py.
# W17 one-command Studio-path upper check: W15's w15_upper.sh (rr / z / zr / q7 masked, any kill-table stack, NOCLAMP, NECK, parts)
# plus K* and the generic EDGE(7->P) family (st21_w17.py + ksfam.py rows, bin/sep3r_w17 window bound + exact leaf).
# usage: [KS=1] [EGK=<keys file>] [ARGSF=<pattern args>] [EXPECT_PAT=D,C,RPAT] bash /tmp/swarm-W17/code_c6/w17_upper.sh SOL.json KILLDIR [TAG]
#   KS=1: K* (= K1 EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]); EGK: one 'NAME EDGE(7->P)[POS=SYM ...]' per line
#   (code/edgekeys_r4.txt = A1, C1, E1). Amounts from SOL['ks'] = [[NAME, value], ...]; a nonzero amount of a family that is off,
#   or an amount outside [0, 3], is a FAIL. KSA10=amask (default) | grammar (6-private of S.A+-1 at d >= 10 free, as certpics).
#   Every other env as w15_upper.sh: DMAXP=20, DLIST, NOCLAMP=1, NPROC (<= 2), PARTS, NECK, FAMILIES=off. Separator jobs run at
#   nice 15 (W17NICE). The Python step also runs the W17 self-test (C++ leaf vs Python rows with planted K* / EDGE slots, d = 7..12)
#   and the window-bound check; both are hard FAILs.
# Team D's stack (A97 + route F + exname + rpatD): ARGSF=/tmp/swarm-W17/args_A97F_x_studio.txt EXPECT_PAT=18101,598,158 (the args name
#   the exname-filtered cfast copies in pat/A97x, built by code/exname_filter17.py, and drop the 2 cfast files Opus's run lacks).
#   EXNAME=<list> is optional there, as a check: any held-out C entry still in the args is a FAIL (wlp3 has no exname).
# code_c6 (W17 round 2, 5 Nov): C6LE=1 checks cons2 as 'the 6 ends <= t' (in - out - t <= 0 for every non-R6 6-link x apex class
#   word, the same 1,424 x 729 enumeration) instead of the equation |in - out| <= 1e-9 (Opus flag c6le, s83). The separator never
#   reads cons2 (its rows use h through M / V6B only), so nothing else changes.
set -u
B=/tmp/swarm-W17; C=${W17CODE:-$B/code_gk9}; export W17CODE=$C   # code_c6: run17.sh runs $C/st21_w17.py
SOLF=$(readlink -f "$1"); KD=$(readlink -f "$2"); TAG=${3:-u$(date +%H%M%S)}
L=$B/logs/$TAG; Q=$B/q/$TAG; mkdir -p $L $Q
DMAXP=${DMAXP:-20}; DLIST=${DLIST:-$(seq -s, 7 $DMAXP)}; NPROC=${NPROC:-2}; NPROCMAX=${NPROCMAX:-2}; [ $NPROC -gt $NPROCMAX ] && NPROC=$NPROCMAX   # round 6: NPROCMAX (macpack: 16)
PARTS=${PARTS:-7:2,8:6,9:8,10:2}; NECK=${NECK:-1}
echo "== W17 upper check $TAG: $SOLF (md5 $(md5sum < $SOLF | cut -c1-8)), kill $KD, d = $DLIST (DMAXP $DMAXP), $NPROC processes, parts $PARTS, neck $NECK, noclamp ${NOCLAMP:-0}, cons2 mode $([ "${C6LE:-0}" = 1 ] && echo c6le || echo equality), f2b7 ${F2B7:-0}, rules ${F2BRULES:-default (run17.sh: tab/rules_zcons_minus_W18rejects.json 2b362955)}, rpatN ${RPATN:-off (default)}, GK ${GK:-none}, code $C"
python3 -I $C/killmd5.py $KD | tee $L/killmd5.log; [ ${PIPESTATUS[0]} = 0 ] || { echo "RESULT: NOT RUN (kill table md5 check failed)"; exit 2; }
T=$(python3 -I -c "import json,sys; print(repr(json.load(open(sys.argv[1]))['t']))" $SOLF)
python3 -I $C/estimate15.py $T $DLIST $NPROC 2>/dev/null
# W17 round 6: RESUME=1 continues a run of the same TAG that was killed (container restart): step 1 is kept if p0.log has its VERDICT,
# the solution md5 and the code/args stamp are unchanged and the query dump is complete; a separator part is kept iff sep.log has its
# drive17 line with rc=0 and an END and its viol file exists; every other part (stale .claim) is rerun from the start.
# bash 3.2 (macOS /bin/bash) mis-parses an unparenthesised case arm inside $( ); compute the rpatN stamp first (lead fix 7 Nov)
case ${RPATN:-off} in
  off|none) _RPSTAMP=off;;
  *) _RPSTAMP=$(cd $B/wd && md5sum < $RPATN | cut -c1-8);;
esac
STAMP="$(md5sum < $SOLF | cut -c1-32) $(cat $C/st21_w17.py $C/f2b7_blocks.py $C/gk_blocks.py $C/gkfam.py $C/hbfam.py $C/hb_blocks.py $C/w17_blocks.py $C/sep3r_gk.cpp | md5sum | cut -c1-32) $(env | grep -E '^(GK|F2B7|F2BRULES|C6LE|NOCLAMP|ARGSF|EXPECT_PAT|EXNAME|DMAXP|PARTS|NECK|FAMILIES|RPATN)=' | sort | md5sum | cut -c1-32) $DLIST rpatN:$_RPSTAMP rules:$(md5sum < ${F2BRULES:-$B/tab/rules_zcons_minus_W18rejects.json} | cut -c1-8)"
KEEP1=0
if [ "${RESUME:-0}" = 1 ] && grep -q "^VERDICT" $L/p0.log 2>/dev/null && [ "$(cat $L/stamp.txt 2>/dev/null)" = "$STAMP" ] && [ -f $Q/env.json ] && [ -f $Q/sf.in ]; then
  KEEP1=1; for d in ${DLIST//,/ }; do [ -f $Q/q_d$d.txt ] || KEEP1=0; done
fi
if [ $KEEP1 = 1 ]; then
  echo "$(date -u +%H:%M:%SZ) step 1: RESUME: kept (p0.log VERDICT, stamp unchanged): $(grep -h '^VERDICT' $L/p0.log | cut -c1-200)"
else
  [ "${RESUME:-0}" = 1 ] && echo "$(date -u +%H:%M:%SZ) RESUME requested but step 1 is not reusable (stamp or dump differs / missing): fresh run"
  RESUME=0; rm -f $L/viol_d*_p*.txt $L/viol_d*_p*.txt.claim; echo "$STAMP" > $L/stamp.txt
  echo "$(date -u +%H:%M:%SZ) step 1: Python checks + query dump"
  env SOL=$SOLF TAG=$TAG KILLDIR=$KD EXPECT_T=$T DMAXP=$DMAXP DLIST=$DLIST QDUMP_ONLY=1 SEPQDUMP=$Q W10ST=1 W10STN=1000 CALD=6 bash $C/run17.sh > $L/p0.log 2>&1
fi
grep -q "^VERDICT" $L/p0.log || { echo "Python step did not finish:"; tail -5 $L/p0.log; echo "RESULT: NOT ESTABLISHED"; exit 3; }
echo "$(date -u +%H:%M:%SZ) step 2: separator jobs"
: > $L/jobs.txt
for d in ${DLIST//,/ }; do
  n=1; for pd in ${PARTS//,/ }; do [ "${pd%%:*}" = "$d" ] && n=${pd#*:}; done
  for ((k = 0; k < n; k++)); do echo "$d $k/$n" >> $L/jobs.txt; done
done
sort -k1,1nr -s $L/jobs.txt | awk '{print ($1==9||$1==8)?0:1, $0}' | sort -k1,1n -s | cut -d' ' -f2- > $L/jobs_sorted.txt
if [ "${RESUME:-0}" = 1 ]; then   # keep the finished parts, rerun the others
  : > $L/jobs_todo.txt; nk=0
  while read d pk; do p=${pk/\//of}; f=$L/viol_d${d}_p$p.txt
    if [ -f $f ] && grep -E "^drive17 d=$d part=$pk .* rc=0 " $L/sep.log 2>/dev/null | grep -v NO-END | grep -q "end=\[END"; then nk=$((nk + 1)); else rm -f $f $f.claim; echo "$d $pk" >> $L/jobs_todo.txt; fi
  done < $L/jobs_sorted.txt
  cp $L/sep.log $L/sep.log.prev_$(date -u +%H%M%S) 2>/dev/null; touch $L/sep.log
  grep -v -E "^drive17 d=($(awk '{print $1" part="$2" "}' $L/jobs_todo.txt | paste -sd'|' -))" $L/sep.log > $L/sep.log.k 2>/dev/null; [ -s $L/jobs_todo.txt ] || cp $L/sep.log $L/sep.log.k; mv $L/sep.log.k $L/sep.log
  echo "$(date -u +%H:%M:%SZ) RESUME: $nk separator parts kept, $(wc -l < $L/jobs_todo.txt) to run"; echo "== RESUME $(date -u +%H:%M:%SZ): $nk parts kept" >> $L/sep.log
else cp $L/jobs_sorted.txt $L/jobs_todo.txt; : > $L/sep.log; fi
cat $L/jobs_todo.txt | xargs -P $NPROC -L 1 bash -c 'p=${1/\//of}; python3 -I '$C'/drive17.py '$Q' $0 '$L'/viol_d$0_p$p.txt part=$1 neck='$NECK' >> '$L'/sep.log 2>&1'
echo "$(date -u +%H:%M:%SZ) step 3: exact re-check of reported arrangements"
cat $L/viol_d*_p*.txt 2>/dev/null | awk '{print $1, $4, $2, $3}' | sort -u -k1,1n -k3,4 > $L/reported.txt
if [ -s $L/reported.txt ]; then
  head -n 20000 $L/reported.txt > $L/reported_cut.txt
  env SOL=$SOLF TAG=${TAG}_rp KILLDIR=$KD EXPECT_T=$T DMAXP=$DMAXP REPLAY=$L/reported_cut.txt REPLAY_OUT=$L/replay.jsonl bash $C/run17.sh > $L/replay.log 2>&1
fi
echo "$(date -u +%H:%M:%SZ) step 4: summary"
python3 -I $C/summarize17.py $L $DLIST $DMAXP | tee $L/summary.txt
