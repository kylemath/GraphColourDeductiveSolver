#!/bin/zsh
# Job 30 A snapshot (Long Table 17:16Z): re-solve A's latest row dump once (maxit=0) on one core, then exhaustive
# feascheck (sep3xf, d = 7..15) on that solution. A itself keeps running.
cd "$(dirname $0)/../.."
cp out/wlp3x_j30A_x_rows.txt out/job30/j30A_rows_snap.txt
A=($(cat out/job28/j28_13.args) pat=loop/n9/win9.out pat=loop/n9/win25.out pat=loop/n9/win25b.out pat=loop/n9/win27.out pat=loop/n9/win29.out pat=loop/n9/win31.out pat=out/job30/addA_dfast18.out pat=out/job30/k3x_D.out cpat=out/job30/k3x_C_A.cfast)
WLP3X_DEF=1 WLP_SEPF=1 nice -n 19 python3 wlp3x.py tag=j30Asnap maxit=0 warm=out/job30/j30A_rows_snap.txt $A > out/job30/j30Asnap.log 2>&1
WLP3X_DEF=1 WLP_SEPF=1 nice -n 19 python3 feascheck.py out/wlp3x_j30Asnap_x_sol.json $A > out/job30/j30Asnap_feas.log 2>&1
echo done > out/job30/snapA.DONE
