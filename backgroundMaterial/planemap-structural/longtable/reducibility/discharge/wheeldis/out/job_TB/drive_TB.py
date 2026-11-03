# job TB (Opus Tier B request, relay 2 Nov 22:06Z): 28 lines of tierB28.txt. Studio engines only:
# kc loop/kc/kc, dfast18 out/job52/dfast18, cfast ../studio15/cfast. Window protocol (as out/job_tw1/drive_tw1.py):
# kc -C -s 60 -t 600 + dfast18; C lines: kc -t 600 -C -x {X} and cfast --fixed {X} for every recorded X.
import os, re, subprocess, sys
WD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
KC = os.path.join(WD, 'loop', 'kc', 'kc'); DF = os.path.join(WD, 'out', 'job52', 'dfast18'); CF = os.path.join(WD, '..', 'studio15', 'cfast')
T = os.path.join(WD, 'out', 'job_TB'); TMP = os.path.join(T, 'tmp'); os.makedirs(TMP, exist_ok=True)
REC = {'loop/k34/fill.txt': ['loop/k34/fill_kcc.out'], 'loop/k38/kills.txt': ['loop/k38/kills_x.txt'],
       'loop/k37/cwin.txt': ['loop/k37/fill_kcc.out', 'loop/k37/lt_x.txt']}
def run(cmd): return subprocess.run(['nice', '-n', '10'] + cmd, capture_output=True, text=True).stdout.strip()
def recx(nm, src):   # every X recorded for this name in the named record's X files, in file order
    xs = []
    for f in REC[src]:
        L = open(os.path.join(WD, f)).read().splitlines()
        for k, l in enumerate(L):
            if l.split()[:1] == [nm]:
                for t in [l] + L[k + 1:k + 2]:
                    for m in re.findall(r'\{([^}]*)\}', t):
                        if m not in xs: xs.append(m)
    return xs
out = open(os.path.join(T, 'results.tsv'), 'a')
for i, line in enumerate(open(os.path.join(T, 'tierB28.txt'))):
    meta, cfg = [x.strip() for x in line.split(' | ', 1)]; nm = cfg.split()[0]; mt = meta.split()
    tf = os.path.join(TMP, 'l%02d.in' % i); open(tf, 'w').write(cfg + '\n')
    if mt[0] == 'E' and mt[1] == 'C':
        for x in recx(nm, mt[3]) or ['NONE']:
            if x == 'NONE': out.write('%d\t%s\tC\tnoX\t%s\n' % (i, nm, run([KC, '-C', '-s', '60', '-t', '600', tf]).replace('\n', ' // '))); continue
            open(tf + '.x', 'w').write('%s {%s}\n' % (nm, x))
            k = run([KC, '-t', '600', '-C', '-x', tf + '.x', tf]); c = run([CF, tf, '--fixed', x])
            out.write('%d\t%s\tC\t{%s}\t%s\t%s\n' % (i, nm, x, k.replace('\n', ' // '), c.replace('\n', ' // ')))
    else:
        k = run([KC, '-C', '-s', '60', '-t', '600', tf]); d = run([DF, tf])
        m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', k); c = ''
        if m: c = run([CF, tf, '--fixed', m.group(1)])
        out.write('%d\t%s\t%s\twindow\t%s\t%s\t%s\n' % (i, nm, 'D' if mt[0] == 'E' else re.search(r'tag=(\w)', meta).group(1), k.replace('\n', ' // '), d.replace('\n', ' // '), c.replace('\n', ' // ')))
    out.flush()
