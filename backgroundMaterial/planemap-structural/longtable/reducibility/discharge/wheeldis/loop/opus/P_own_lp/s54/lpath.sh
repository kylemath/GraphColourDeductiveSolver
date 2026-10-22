# s54 lpath.sh LAMBDA TAG: lasso LP on the pool (nosep, ipm first), support extraction, then the support refit with separation + upperR2
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s54
L=$1; T=$2; D=y:dict,g:dict,h:dict,x:dict,r:dict,lq:dict
while pgrep -f "tag=n_$T " > /dev/null; do sleep 30; done
[ -s runs/n_$T/sol_n_$T.json ] || NOUPPER=1 bash run1.sh n_$T $D lasso=$L lazyb nosep ipm0
python3 support.py runs/n_$T/sol_n_$T.json sup/sup_n_$T.json > sup/sup_n_$T.txt
F=$PWD/sup/sup_n_$T.json; MAXIT=400 bash run1.sh R_$T y:sup:$F,g:sup:$F,h:sup:$F,x:sup:$F,r:sup:$F,lq:sup:$F lazyb
