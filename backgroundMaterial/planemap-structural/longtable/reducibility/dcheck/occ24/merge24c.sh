#!/bin/zsh
# Merge (18 Oct): wait until every key S2703..S2854 has a result line in results24b_w*/c*.txt, then append them
# (one per key, sorted) to results24b.txt and write the DONE line for all 2,855 keys.
cd ${0:a:h}
n=$(grep -c . k1_studioD.txt)
while true; do
  got=$(cat results24b_w*.txt results24b_c*.txt 2>/dev/null | awk '{print $1}' | sort -u | grep -c '^S')
  [ $got -ge $(( n - 2703 )) ] && break; python3 -c 'import time; time.sleep(120)'
done
cat results24b_w*.txt results24b_c*.txt | sort -u -k1,1 >> results24b.txt
k=$(grep -c '^S' results24b.txt); c=$(grep -c 'D=true errors=0 sorry=0$' results24b.txt)
echo "DONE $k keys ($c clean: D=true, errors=0, sorry=0)" >> results24b.txt
