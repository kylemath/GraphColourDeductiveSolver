#!/bin/zsh
# Studio Job 4 (13 Oct 2026, exploratory): Conjecture R0 at larger n, by cubes (depth 2), nice 10.
# Starts when Job 3 (run_job3c.sh) has written ALLDONE.  Power controls (non-planar) stop at the first SAT cube.
cd "$(dirname $0)"
W4=${W4:-8}
until grep -q ALLDONE out/progress.txt 2>/dev/null; do sleep 60; done
mkdir -p out/r0
run() { echo "START r0 $* $(date)" >> out/progress4.txt
        nice -n 10 python3 r0_cubes.py $@ >> out/progress4.txt 2>&1
        echo "END r0 $* $(date)" >> out/progress4.txt; }
for spec in "28 10" "24 20" "30 10" "26 20" "28 20"; do
  set -- ${=spec}
  STOP_AFTER_SAT=1 run $1 $2 0 2 $W4 out/r0/n$1_L$2_nonplanar      # power control: must be SAT
  run $1 $2 1 2 $W4 out/r0/n$1_L$2_planar                           # R0: expected UNSAT in every cube
done
echo ALLDONE >> out/progress4.txt
