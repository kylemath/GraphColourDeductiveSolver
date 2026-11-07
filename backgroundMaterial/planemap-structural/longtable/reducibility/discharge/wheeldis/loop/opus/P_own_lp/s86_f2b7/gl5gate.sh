# s86: hand the lower slot from k86GL4 to k86GL5: wait for GL4's iteration-0 line (its separated rows are then in eng_p1r/rows_k86GL4.txt),
# stop the GL4 LP run (its watchL86p lowerR2 on cert p1_00 keeps running), wait for 4 GB free, then launch_k86GL5.sh (warm = GL4's list + GL4's rows).
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; cd $N
until grep -q "^iter 0" runK_k86GL4/K.log 2>/dev/null; do sleep 60; done
for i in $(seq 1 20); do [ -s eng_p1r/rows_k86GL4.txt ] && break; sleep 15; done
echo "$(date -u +%H:%M:%SZ) [s86G] gl5gate: GL4 $(grep '^iter 0' runK_k86GL4/K.log | cut -c1-90); rows_k86GL4 $(wc -l < eng_p1r/rows_k86GL4.txt) lines; stopping GL4" >> run.log
pkill -f "runK86p.sh 200 2 k86GL4"; sleep 2; pkill -f "tag=k86GL4 "; sleep 20
until [ $(free -m | awk 'NR==2{print $7}') -ge 4000 ]; do sleep 20; done
bash launch_k86GL5.sh
echo "$(date -u +%H:%M:%SZ) [s86G] gl5gate: launched k86GL5 (keys $(md5sum < p1r/cg_keys_r13w16_16fi.txt | cut -c1-8), 220)" >> run.log
