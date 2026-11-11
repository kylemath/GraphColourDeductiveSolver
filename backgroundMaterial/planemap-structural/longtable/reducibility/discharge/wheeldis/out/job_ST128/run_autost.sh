#!/bin/bash
# usage: autost_gs9r.sh NN POINT_JSON KEYFILE : W17 gk9 (check9.sh, HATBB; default flags = the in02 / ST-108 reading) main + tneg of a GS
# point on K3gB5r (a84966df, EXPECT 18244,781,158) with the point's nonzero keys of KEYFILE + the 14 HATBB keys (b9ff66bd, ST-108 in/).
# Writes out/job_STNN/ and commits with md5 -r MD5SUMS. Stops (no check) if a nonzero key is refused or missing from the files.
NN=$1; PJ=$2; KF=$3; W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
J=$W/out/job_ST$NN; B=/tmp/swarm-W17; P=$(basename $PJ .json); HB=$W/out/job_ST108/in/cg_keys_w6b16x_hatbb.txt
mkdir -p $J/in; [ -f $J/in/$P.json ] || cp $PJ $J/in/; cp $J/in/$P.json $B/sol/
python3 -I - $J/in/$P.json $KF $HB $J/in/keys_nonzero.txt $B/sol/${P}_tneg.json <<'PY' || { echo "ST-$NN: key filter refused"; exit 1; }
import json, re, sys
pt, kf, hb, out, tn = sys.argv[1:6]; s = open(pt).read(); d = json.loads(s); ks = dict((n, a) for n, a in d['ks'])
L = [l for f in (kf, hb) for l in open(f) if l.strip() and not l.startswith('#')]
names = [l.split()[0] for l in L]
keep = [l for l in L if ks.get(l.split()[0], 0) != 0]
miss = [n for n in ks if ks[n] != 0 and n not in names]
sys.path.insert(0, '/tmp/swarm-W17/code_gk9'); import gkfam, hbfam; bad = []
for l in keep:
    body = l.split('#')[0].strip()
    try:
        if hbfam.is_hat_line(body): hbfam.parse_key(body)
        else: gkfam.parse_key(body)
    except Exception as e: bad.append(l.strip()[:150] + '  :: ' + str(e)[:100])
print('keys in files %d, nonzero kept %d (HAT %d, payer-8/9 %d), dropped %d, nonzero missing-from-files %d, refused %d'
      % (len(L), len(keep), sum('HAT(' in l for l in keep), sum(1 for l in keep if re.search(r'EDGE\([89]', l)), len(L) - len(keep), len(miss), len(bad)))
for b in bad: print('REFUSED', b)
for m in miss[:10]: print('MISSING', m)
if bad or miss: sys.exit(1)
open(out, 'w').write('# nonzero keys of %s + HATBB b9ff66bd in %s\n' % (kf.split('/')[-1], pt.split('/')[-1]) + ''.join(keep))
m = re.match(r'\{"t": ([0-9.eE+-]+)', s); t = float(m.group(1)); open(tn, 'w').write('{"t": ' + repr(t - 5e-6) + s[m.end():]); print('t', t)
PY
cp $J/in/keys_nonzero.txt $B/tab/keys_ST$NN.txt
C="GK=$B/tab/keys_ST$NN.txt RPATN=$B/tab/rpatN3_rotation_justified.txt F2BRULES=$B/tab/rules_A5final_2db75746.json W17NICE=20 ARGSF=$B/args_A97F_W13K3gB5r_x_studio.txt EXPECT_PAT=18244,781,158"
cd $B; env $C TAG=${P}_zK3gB5r_gk9 nice -n 15 bash $B/check9.sh $B/sol/$P.json 6 > $J/main.out 2>&1
env $C TAG=${P}_tneg_zK3gB5r_gk9 nice -n 15 bash $B/check9.sh $B/sol/${P}_tneg.json 6 > $J/tneg.out 2>&1
cat $B/logs/${P}_tneg_zK3gB5r_gk9/viol_d*.txt 2>/dev/null | grep -v '^#' | sort -u > $J/tneg_receiver_violators.txt
for f in main tneg; do echo "--$f"; grep -E "^RESULT|senderR2 rows|patterns distinct|DP margin|Karp|exact violated [1-9]|GK keys|HATBB|HB keys" $J/$f.out | cut -c1-150; grep -E '^cons2' $J/$f.out | grep -oE 'max [0-9.]+ \([0-9/]+\)'; done
echo "--tneg loads"; awk '{print $1, $4}' $J/tneg_receiver_violators.txt | sort | uniq -c | sort -k3,3gr | head -6; sort -k4,4gr $J/tneg_receiver_violators.txt | head -8
cp $W/out/maclane/$(basename $0) $J/run_autost.sh; cd $J; F=$(find . -type f ! -name MD5SUMS | sed 's#^\./##' | sort); md5 -r $F > MD5SUMS; echo "MD5SUMS md5 $(md5 -q MD5SUMS)"
cd $W; git add -f $(for f in $F MD5SUMS; do echo out/job_ST$NN/$f; done) && git commit -q -m "ST-$NN (auto, GS point $P): W17 gk9 (HATBB) main + tneg on K3gB5r + nonzero keys

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && for i in 1 2 3 4 5; do git fetch -q origin main && git merge -q --no-edit origin/main && git push -q origin HEAD:main && { echo "commit $(git log -1 --format=%h --grep="ST-$NN (auto")"; break; }; sleep $((2**i)); done
