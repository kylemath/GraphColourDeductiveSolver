# s84_sepaudit: run one jsepf binary directly on a kept d = 7 query (the exact argv the driver used, from logs/argv_<q>.txt),
#   with a replacement header file (threshold / K / mode edited) and the audit knobs in the environment.  1 thread, nice 15.
#   usage: [SEPA_LOOSEN=..] [SEPA_BREAK=1] bash runq.sh <query tag> <binary> <hdr file> <run name>
#   writes runs/<run name>.out (stdout), .err (stderr), .time; one line to run.log
S84=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s84_sepaudit
Q=$1; BIN=$2; HDR=$3; RN=$4; mkdir -p $S84/runs
read -r -a AV < $S84/logs/argv_$Q.txt          # AV[0] = binary, AV[1] = hdr, AV[2..] = win, threads, sym, ...
AV[0]=$BIN; AV[1]=$HDR
unset SEPA_ARGVLOG
T0=$(date +%s.%N)
nice -n 15 "${AV[@]}" > $S84/runs/$RN.out 2> $S84/runs/$RN.err; RC=$?
T1=$(date +%s.%N); echo "rc=$RC wall=$(echo "$T1 - $T0" | bc)s" > $S84/runs/$RN.time
echo "$(date -u +%H:%M:%SZ) [runq] $RN q=$Q bin=$(basename $BIN) md5 $(md5sum < $BIN | cut -c1-8) hdr=$(basename $HDR) (line1: $(head -1 $HDR)) LOOSEN=${SEPA_LOOSEN:-0} BREAK=${SEPA_BREAK:-0} rc=$RC: $(tail -1 $S84/runs/$RN.out) [$(cat $S84/runs/$RN.time)]" >> $S84/run.log
