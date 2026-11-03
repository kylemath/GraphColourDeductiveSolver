# f2b041 (3): the 118 RSST C2cons of the keep95 cover, re-run on Studio engines: kc -C -s 60 -t 600 (window, kc's own X) and
# cfast --fixed {kc X}; plus kc -t 600 -C -x {round-44 X} and cfast --fixed {round-44 X} (loop/k44/rsst_x.txt). nice 10.
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..'))
KC = os.path.join(W, 'loop', 'kc', 'kc'); CF = os.path.join(W, '..', 'studio15', 'cfast')
cfg = {l.split()[0].split('_')[0]: l.strip() for l in open(os.path.join(W, 'loop', 'k44', 'rsst.txt'))}
xr = {l.split()[0].split('_')[0]: l.split()[1] for l in open(os.path.join(W, 'loop', 'k44', 'rsst_x.txt'))}
def run(c): return subprocess.run(['nice', '-n', '10'] + c, capture_output=True, text=True).stdout.strip().replace('\n', ' // ')
def one(nm):
    tf = os.path.join(H, 'tmp', nm + '.in'); open(tf, 'w').write(cfg[nm] + '\n')
    k = run([KC, '-C', '-s', '60', '-t', '600', tf]); m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', k); kx = m.group(1) if m else ''
    c1 = run([CF, tf, '--fixed', kx]) if kx else ''
    rx = xr.get(nm, '-').strip('{}'); k2 = c2 = ''
    if rx and rx != '-':
        open(tf + '.x', 'w').write('%s {%s}\n' % (cfg[nm].split()[0], rx)); k2 = run([KC, '-t', '600', '-C', '-x', tf + '.x', tf]); c2 = run([CF, tf, '--fixed', rx])
    return '\t'.join([nm, cfg[nm].split()[0], kx, k, c1, rx, k2, c2])
names = [l.strip() for l in open(os.path.join(H, 'names118.txt')) if l.strip()]
with ThreadPoolExecutor(int(os.environ.get('NPAR', '6'))) as ex, open(os.path.join(H, 'results118.tsv'), 'w') as out:
    for r in ex.map(one, names): out.write(r + '\n'); out.flush()
