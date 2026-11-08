# s86: hand the lower slot from k86GL5 to k86GL6: wait for GL5's iteration-0 line and for eng_p1r/rows_k86GL5.txt to be non-empty and unchanged
# for 30 s (its separated rows), stop the GL5 LP run (its watchL86p lowerR2 on cert p1_00 keeps running), wait for 4 GB free, then launch_k86GL6.sh
# (warm = GL5's list + GL5's rows).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N
until grep -q "^iter 0" runK_k86GL5/K.log 2>/dev/null; do sleep 60; done
for i in $(seq 1 40); do s1=$(stat -c %s eng_p1r/rows_k86GL5.txt 2>/dev/null || echo 0); sleep 30; s2=$(stat -c %s eng_p1r/rows_k86GL5.txt 2>/dev/null || echo 0); [ "$s1" -gt 0 ] && [ "$s1" = "$s2" ] && break; done
echo "$(date -u +%H:%M:%SZ) [s86G] gl6gate: GL5 $(grep '^iter 0' runK_k86GL5/K.log | cut -c1-90); rows_k86GL5 $(wc -l < eng_p1r/rows_k86GL5.txt) lines; stopping GL5" >> run.log
pkill -f "runK86p.sh 200 2 k86GL5"; sleep 2; pkill -f "tag=k86GL5 "; sleep 20
until [ $(free -m | awk 'NR==2{print $7}') -ge 4000 ]; do sleep 20; done
bash launch_k86GL6.sh
echo "$(date -u +%H:%M:%SZ) [s86G] gl6gate: launched k86GL6 (keys $(md5sum < p1r/cg_keys_r13w16_16fik.txt | cut -c1-8), 240)" >> run.log
