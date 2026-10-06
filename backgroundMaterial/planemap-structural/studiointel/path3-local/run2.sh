#!/bin/sh
# Round 2: 6 workers x 15 min wall, nice 10. New seeds (Math's akempic RAK at n=32,36; tube TU(8,4); double cone CC(2,1);
# the order-26 K3 counterexample) and a random-only control on HoG 1152 (KT=0) to compare with the targeted-flip runs of round 1.
cd "$(dirname "$0")"; O=run2; mkdir -p $O; W=900
nice -n 10 python3 kc_search_local.py ../path3/seeds/K3_26_5401.json 21 8 4 $W $O 9 K3_26_5401 > $O/K3_26_5401.out 2>&1 &
nice -n 10 python3 kc_search_local.py seeds/RAK_a17_b1_s2.json 22 8 4 $W $O 9 RAK_a17_b1_s2 > $O/RAK_a17_b1_s2.out 2>&1 &
nice -n 10 python3 kc_search_local.py seeds/RAK_a19_b1_s2.json 23 8 4 $W $O 9 RAK_a19_b1_s2 > $O/RAK_a19_b1_s2.out 2>&1 &
nice -n 10 python3 kc_search_local.py seeds/TU_n8_L4.json 24 8 4 $W $O 9 TU_n8_L4 > $O/TU_n8_L4.out 2>&1 &
nice -n 10 python3 kc_search_local.py seeds/CC_R2_tw1.json 25 8 4 $W $O 9 CC_R2_tw1 > $O/CC_R2_tw1.out 2>&1 &
nice -n 10 python3 kc_search_local.py ../../longtable/historical-traps/hog1152-heawood-four-color-graph.json 26 8 0 $W $O 9 hog1152_randomonly > $O/hog1152_randomonly.out 2>&1 &
wait
