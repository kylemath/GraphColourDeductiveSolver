# round 52, explore rows from 14:45Z: ring <= 16 only (STOP=0); a row with no kill there gets its ring 17-18 windows
# (not yet run) written to win52_<row>_todo.txt for Studio, since kc averages ~322 s per ring-17 window here.
# usage: sh q52r16.sh D LK SV PREFIX   -> touches R52_<PREFIX>.DONE
cd "$(dirname "$0")"
D=$1; LK=$2; SV=$3; P=$4; CAP=${CAP:-7000}
for R in 16 18; do
  [ -f win45_${D}_${LK}_${SV}_A$R.txt ] || python3 win45.py $R $D $LK $SV > /dev/null
done
W16=win45_${D}_${LK}_${SV}_A16.txt; W18=win45_${D}_${LK}_${SV}_A18.txt
date -u +%H:%MZ
STOP=0 NW=3 timeout $CAP python3 drive45.py $W16 600 > drive52_${P}_16.log 2>&1
python3 minkill47.py $W16 $LK $P; cat ${P}_kills_min.txt
if [ ! -s ${P}_kills.txt ]; then
  python3 -I -c "
import sys
done = {l.split()[0] for l in open('A_kcc.out') if l.strip() and not l.startswith(' ')}
out = [l for l in open(sys.argv[1]) if l.strip() and l.split()[0] not in done]
open(sys.argv[2], 'w').write(''.join(out)); print(len(out), 'windows left ->', sys.argv[2])" $W18 win52_${D}_${LK}_${SV}_todo.txt
fi
date -u +%H:%MZ; touch R52_$P.DONE
