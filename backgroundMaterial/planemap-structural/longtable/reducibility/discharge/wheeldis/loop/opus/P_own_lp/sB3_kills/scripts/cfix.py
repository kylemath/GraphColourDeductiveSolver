# B3 C recheck: lines a screener logged N with an empty leftover and an X set (kcc printed C-REDUCIBLE but the old parser
# tested 'C=true') are rerun with cfast --fixed X; writes OUT with corrected verdicts (C + cfast verdict) for those codes.
# usage: python3 cfix.py OUT.tsv res1.tsv [res2.tsv ...]
import sys, subprocess, re
O = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus'
CF = O + '/A_rsst_defects/bin/cfast'; tmp = sys.argv[1] + '.one'; n = 0
with open(sys.argv[1], 'a') as out:
    for fn in sys.argv[2:]:
        for l in open(fn):
            g = l.rstrip('\n').split('\t')
            if len(g) < 12 or g[4] != 'N' or g[5] != '' or not g[6]: continue
            open(tmp, 'w').write(g[11] + '\n')
            o = subprocess.run(['nice', '-n', '15', CF, tmp, '--fixed', g[6]], capture_output=True, text=True, timeout=1800).stdout
            g[4] = 'C'; g[10] = 'cfast:' + ('C-REDUCIBLE' if 'C-REDUCIBLE' in o else 'noC') + ' ' + re.sub(r'\s+', ' ', o.strip())[-120:]
            out.write('\t'.join(g) + '\n'); out.flush(); n += 1
            print(g[3], g[9], 'X=' + g[6], g[10][:40], flush=True)
print('rechecked', n)
