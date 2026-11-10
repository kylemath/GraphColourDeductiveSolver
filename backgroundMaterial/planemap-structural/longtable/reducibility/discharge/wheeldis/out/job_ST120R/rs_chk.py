"""ST-120 R own-engine re-check of the 403 RSST configs (Studio, 10 Nov). usage (cwd wheeldis): python3 out/job_ST119/st119_chk.py NPAR
D entries (the 107 nl configs of D_st119.tsv, and the D window): kc -t 600 -C + dfast18, PASS iff both say D=true.
C windows (windows13.tsv): kc -t 600 -C -x X (adm=yes leftover 0 C-REDUCIBLE) + cfast --fixed X (C-REDUCIBLE leftover 0).
Writes out/job_ST119/chk/<name>.{in,x,out} and out/job_ST119/verdicts.tsv (name, kind, ring, verdict, detail). Resumable."""
import sys, os, subprocess
from concurrent.futures import ThreadPoolExecutor
J = 'out/job_ST120R/'; C = J + 'chk/'; os.makedirs(C, exist_ok=True); NP = int(sys.argv[1])
items = []
for l in open(J + 'items.tsv'):
    n, v, X, kc = l.rstrip('\n').split('\t'); items.append((n, v, kc, X))
done = {l.split('\t')[0] for l in open(J + 'verdicts.tsv')} if os.path.exists(J + 'verdicts.tsv') else set()
def run(it):
    n, v, kc, X = it
    if n in done: return None
    open(C + n + '.in', 'w').write(kc + '\n'); r = kc.split()[1]
    sh = lambda c: subprocess.run(['nice', '-n', '15'] + c, capture_output=True, text=True).stdout
    if v == 'D':
        a = sh(['loop/kc/kc', '-t', '600', '-C', C + n + '.in']); b = sh(['out/job52/dfast18', C + n + '.in'])
        ok = 'D=true' in a and 'D=true' in b
        det = 'kc %s dfast18 %s' % ('D' if 'D=true' in a else 'notD', 'D' if 'D=true' in b else 'notD')
    else:
        open(C + n + '.x', 'w').write('%s {%s}\n' % (n, X))
        a = sh(['loop/kc/kc', '-t', '600', '-C', '-x', C + n + '.x', C + n + '.in']); b = sh(['../studio15/cfast', C + n + '.in', '--fixed', X])
        ka = 'adm=yes leftover 0' in a and 'C-REDUCIBLE' in a; cb = 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in b
        ok = ka and cb; det = 'kc -C -x %s cfast --fixed %s X={%s} rim=%s' % ('OK' if ka else 'FAIL', 'OK' if cb else 'FAIL', X, 'yes' if 'R' in X else 'no')
    open(C + n + '.out', 'w').write('== kc\n' + a + '== second engine\n' + b)
    return '%s\t%s\t%s\t%s\t%s\n' % (n, v, r, 'PASS' if ok else 'FAIL', det)
with ThreadPoolExecutor(NP) as ex, open(J + 'verdicts.tsv', 'a') as out:
    for res in ex.map(run, items):
        if res: out.write(res); out.flush()
print('RSCHKDONE')
