#!/bin/zsh
# st24b spec-only check (Long Table 17:07Z): queued behind Job 52. Starts only after a Job 52 process has exited (a slot
# freed by Job 52), with free memory >= 30 GB. One job, sequential: dcount, the lower rebuild, then the upper check.
# Never takes a dfast18/cfast heavy slot.
cd "$(dirname $0)/../.."
O=loop/studio/opus_check
n0=$(ps -axo command= | grep -cE "out/job52/(job52|row10_open).py")
while true; do
  n=$(ps -axo command= | grep -cE "out/job52/(job52|row10_open).py")
  fr=$(vm_stat | awk '/Pages free/ {gsub("\\.","",$3); print int($3*16384/1073741824)}')
  [ $n -lt $n0 ] && [ $fr -ge 30 ] && break
  [ $n -lt $n0 ] && n0=$n   # a slot freed but memory short: wait for memory
  sleep 120
done
echo "st24b started $(date -u '+%m-%d %H:%MZ') (Job 52 processes $n, free ${fr} GB)" > out/job52/st24b_gate.status
WLP3X_DEF=1 WLP_SEPF=1 nice -n 10 python3 $O/dcount.py $O/argsA59_pinned.txt > $O/studio_st24b_dcount.txt 2>&1
HAT5=1 V6=0 LOWER_ONLY=1 EXPECT_T=2/13 EXPECT_PAT=16937,1884,158 WLP3X_DEF=1 WLP_SEPF=1 nice -n 10 python3 out/job31/st18_check.py $O/sol_st24b.json $O/cert_st24bL.json $O/argsA59_pinned.txt > $O/st24bL_lower.log 2>&1
CALD=12 HAT5=1 V6=0 SKIP_LOWER=1 DMAXP=17 CAP=3000000 EXPECT_T=2/13 EXPECT_PAT=16937,1884,158 WLP3X_DEF=1 WLP_SEPF=1 nice -n 10 python3 out/job31/st18_check.py $O/sol_st24b.json $O/cert_st24bL.json $O/argsA59_pinned.txt > $O/st24b_check.log 2>&1
echo "st24b done $(date -u '+%m-%d %H:%MZ')" >> out/job52/st24b_gate.status
