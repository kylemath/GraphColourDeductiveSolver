# Round 52 (Long Table, 12:41Z): ring 17-18 reducibility of a surviving face receiver row, one row per job.
# Windows at ring <= 16 run first with STOP=0 (all kills recorded); if none is a two-engine kill, the ring 17-18
# windows run with STOP=1 (the first two-engine kill closes the row).  Cap: CAP seconds per row (default 7000).
# usage: sh q52row.sh D LK SV PREFIX   -> touches R52_<PREFIX>.DONE
cd "$(dirname "$0")"
D=$1; LK=$2; SV=$3; P=$4; CAP=${CAP:-7000}; T0=$(date +%s)
for R in 16 18; do
  [ -f win45_${D}_${LK}_${SV}_A$R.txt ] || python3 win45.py $R $D $LK $SV > /dev/null
done
W16=win45_${D}_${LK}_${SV}_A16.txt; W18=win45_${D}_${LK}_${SV}_A18.txt
date -u +%H:%MZ
STOP=0 NW=3 timeout $CAP python3 drive45.py $W16 600 > drive52_${P}_16.log 2>&1
python3 minkill47.py $W16 $LK $P; cat ${P}_kills_min.txt
if [ ! -s ${P}_kills.txt ]; then
  LEFT=$(( CAP - ($(date +%s) - T0) ))
  date -u +%H:%MZ
  [ $LEFT -gt 60 ] && STOP=1 NW=3 timeout $LEFT python3 drive45.py $W18 600 > drive52_${P}_18.log 2>&1
  python3 minkill47.py $W18 $LK $P; cat ${P}_kills_min.txt
fi
date -u +%H:%MZ; touch R52_$P.DONE
