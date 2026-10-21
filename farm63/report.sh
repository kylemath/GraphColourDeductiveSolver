#!/bin/bash
# usage: report.sh OUTDIR TAG -> writes farm63/results/TAG.txt (progress + kill lines) and pushes to branch farm63-results-TAG (best effort)
cd "$(dirname "$0")/.."; mkdir -p farm63/results; bash farm63/summ.sh $1 > farm63/results/$2.txt
git checkout -q -B farm63-results-$2; git add farm63/results/$2.txt
git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "farm63 results $2" && git push -q -f origin farm63-results-$2 2>&1 | tail -1
