cd /tmp/swarm-R3A2/tw
python3 -c "
import json
for d,cl,w,s,y in json.load(open('/mnt/project-files/swarm/teamA/A3-diamond/a3_rows.json')): print(w,s)
" > rows.txt
for t in 6 5 7 8; do
while read LK SV; do
  f=g_${t}_${LK}_${SV}
  [ -s $f.txt ] || LK=$LK SV=$SV timeout 600 nice -n 10 python3 gen.py 16 $t > $f.txt 2>$f.err
  timeout 600 python3 kcrun.py $f.txt $f.res 15 stop1
done < rows.txt
done
echo SWEEPDONE > sweep.flag
