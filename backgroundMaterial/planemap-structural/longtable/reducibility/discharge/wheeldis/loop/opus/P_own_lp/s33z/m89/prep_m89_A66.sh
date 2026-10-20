# m89 on A66 (main 3d6c4f9a, the registry solved on): A66 minus the 89 CGLUE-XRING C entries (27964810 list); only k3x_C changes.
# Rebuild kill6 (U=7,8,9), killnpy, l3q tables, dcount; md5 compare against reg_A66. (A64 minus-89 build kept in m89/A64.)
set -e
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Z=$P/s33z; A=$Z/reg_A66; Q=$Z/m89/A66; mkdir -p $Q/f/kill; cd $Q
until [ -e $A/prep_done.txt ]; do sleep 60; done
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; EX=$S/ex_A66
date -u +%H:%M:%SZ > prep_start.txt
python3 - $Z/m89/CGLUE-XRING-ENTRIES_27964810.txt $A/k3x_C_A66.cfast k3x_C_A66m89.cfast > m89_build.txt <<'PY'
import sys
N=set(l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')); assert len(N)==89
out=[]; cur=None; drop=set()
for line in open(sys.argv[2]):
    if ' r=' in line and not line.startswith(' '): cur=line.split()[0]
    if cur in N: drop.add(cur); continue
    out.append(line)
open(sys.argv[3],'w').writelines(out)
print('dropped', len(drop), 'of 89; not found', sorted(N-drop), '; C entries left', sum(1 for l in out if ' r=' in l and not l.startswith(' ')))
PY
sed "s#cpat=$A/k3x_C_A66.cfast#cpat=$Q/k3x_C_A66m89.cfast#" $A/args_A66.txt > args_A66m89.txt
diff <(tr ' ' '\n' < $A/args_A66.txt) <(tr ' ' '\n' < args_A66m89.txt) >> m89_build.txt || true
cp $P/s31/f/s16_filter.py $P/s31/f/s16_killnpy.py f/
TD=$A/k3x_D_A66.out; TC=$Q/k3x_C_A66m89.cfast
{ for U in 7 8 9; do echo "cd $Q/f && nice -n 10 python3 s16_filter.py $EX $TD $TC kill/kill6_U$U.json wj=6 U=$U > kill/kill6_U$U.log 2>&1"; done
  for sg in 1 -1; do echo "cd $Q && nice -n 10 python3 $Z/l3qtab.py $EX $TD $TC tab_$sg.json $sg > tab_$sg.log 2>&1"; done
  echo "cd $Q && nice -n 10 python3 $P/s31/dcount.py args_A66m89.txt $M > dcount.txt 2>&1"; } | OMP_NUM_THREADS=1 xargs -P1 -I{} sh -c '{}'
(cd f && python3 s16_killnpy.py kill > kill/killnpy.log 2>&1)
{ echo "# m89 vs A66"; for f in f/kill/kill6_U7.npy f/kill/kill6_U8.npy f/kill/kill6_U9.npy tab_1.json tab_-1.json; do a=$(md5sum < $A/$f | cut -c1-32); b=$(md5sum < $f | cut -c1-32); [ $a = $b ] && s=SAME || s=DIFF; echo "$f A66 $a m89 $b $s"; done; } > md5_compare.txt
date -u +%H:%M:%SZ > prep_end.txt
echo DONE > prep_done.txt
