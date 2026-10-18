#!/bin/zsh
# Job 30 run A: L2 (wlp3x, xcap 3) on run29b's registry + the dropped-letter windows (out/job30/addA_dfast18.out),
# plus explore's loop/k3*/ windows that pass the two-engine filter (twoeng.py); warm from run29b's final row dump; starts on the first free core (after the first n1 win17 job ends), nice 19.
cd "$(dirname $0)/../.."
until [ -f out/job30/reg.OK ] && [ $(grep -c w17_ out/job28/n1/n1.log 2>/dev/null || echo 0) -ge 1 ]; do sleep 60; done
python3 out/job30/twoeng.py > out/job30/twoeng.log 2>&1   # explore loop/k3*/ windows, two engines
A=($(cat out/job28/j28_13.args) pat=loop/n9/win9.out pat=loop/n9/win25.out pat=loop/n9/win25b.out pat=loop/n9/win27.out pat=loop/n9/win29.out pat=loop/n9/win31.out pat=out/job30/addA_dfast18.out pat=out/job30/k3x_D.out cpat=out/job30/k3x_C.cfast)
WLP3X_DEF=1 WLP_SEPF=1 nice -n 19 python3 wlp3x.py tag=j30A warm=out/job28/j29b_final_rows.txt $A > out/job30/j30A.log 2>&1
echo done > out/job30/A.DONE
WLP3X_DEF=1 WLP_SEPF=1 SEP_NODELIMIT=0 nice -n 19 python3 feascheck.py out/wlp3x_j30A_x_sol.json $A > out/job30/j30A_feas.log 2>&1
echo done > out/job30/Afeas.DONE
