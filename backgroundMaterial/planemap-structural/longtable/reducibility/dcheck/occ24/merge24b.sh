#!/bin/zsh
# Append the 4 workers' results (sorted by key) to results24b.txt and write the DONE line for all 2,855 keys.
cd ${0:a:h}
until [ -f W0.DONE ] && [ -f W1.DONE ] && [ -f W2.DONE ] && [ -f W3.DONE ]; do python3 -c 'import time; time.sleep(60)'; done
sort results24b_w0.txt results24b_w1.txt results24b_w2.txt results24b_w3.txt >> results24b.txt
n=$(grep -c '^S' results24b.txt); c=$(grep -c 'D=true errors=0 sorry=0$' results24b.txt)
echo "DONE $n keys ($c clean: D=true, errors=0, sorry=0)" >> results24b.txt
