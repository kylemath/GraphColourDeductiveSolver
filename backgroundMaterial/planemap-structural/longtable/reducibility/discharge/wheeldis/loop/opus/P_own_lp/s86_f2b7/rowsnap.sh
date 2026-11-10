# s86 (10 Nov 03:25Z, Lead: "a row snapshot each pass so a restart is cheap"): usage: bash rowsnap.sh <engine dir name> <tag>
# On each new pass line in runK_<tag>/K.log ('^iter ' or 'lext it N: phase 1'), copy <eng>/rows_<tag>.txt (whole lines) to
# warm/rows_<tag>_snap_live.txt atomically.  Exits when the run is gone.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
E=$1; T=$2; P="${T%?}[${T: -1}]"; n0=0
while pgrep -f "pcheck.py solveR2.*tag=$P " > /dev/null; do
  n=$(grep -cE '^iter |lext it [0-9]+: phase 1' $N/runK_$T/K.log 2>/dev/null); n=${n:-0}
  if [ "$n" -gt "$n0" ]; then
    python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/$E/rows_$T.txt $N/warm/rows_${T}_snap_live.txt.tmp 2>/dev/null && mv $N/warm/rows_${T}_snap_live.txt.tmp $N/warm/rows_${T}_snap_live.txt
    n0=$n
  fi
  sleep 60
done
