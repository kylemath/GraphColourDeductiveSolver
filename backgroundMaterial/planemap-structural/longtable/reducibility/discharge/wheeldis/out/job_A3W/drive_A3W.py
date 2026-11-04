# job A3W (Studio): window protocol on Studio engines for the ring-15/16 windows of the 14 A3 dual rows (windows_r15r16.txt):
# kc -C -s 60 -t 600; D -> dfast18; C -> cfast --fixed {kc X}. Pass 2 (CFD=1): cfast D check on the windows in CFDLIST.
import os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
KC = os.path.join(W, 'loop', 'kc', 'kc'); DF = os.path.join(W, 'out', 'job52', 'dfast18'); CF = os.path.join(W, '..', 'studio15', 'cfast')
os.makedirs(os.path.join(H, 'tmp'), exist_ok=True)
def run(c): return subprocess.run(['nice', '-n', '15'] + c, capture_output=True, text=True).stdout.strip().replace('\n', ' // ')
def one(line):
    nm = line.split()[0]; tf = os.path.join(H, 'tmp', re.sub(r'[^A-Za-z0-9_.-]', '_', nm) + '.in'); open(tf, 'w').write(line + '\n')
    if os.environ.get('CFD'): return '\t'.join([nm, run([CF, tf])])
    k = run([KC, '-C', '-s', '60', '-t', '600', tf]); d = c = ''
    if 'D=true' in k.split(' // ')[0]: d = run([DF, tf])
    m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', k)
    if m: c = run([CF, tf, '--fixed', m.group(1)])
    return '\t'.join([nm, k, d, c])
src = os.environ.get('CFDLIST', os.path.join(H, 'windows_r15r16.txt')); outf = os.environ.get('OUTF') or os.path.join(H, 'cfd.tsv' if os.environ.get('CFD') else 'kc.tsv')
done = {l.split('\t')[0] for l in open(outf)} if os.path.exists(outf) else set()
lines = [l.strip() for l in open(src) if l.strip() and l.split()[0] not in done]
with ThreadPoolExecutor(int(os.environ.get('NPAR', '6'))) as ex, open(outf, 'a') as out:
    for r in ex.map(one, lines): out.write(r + '\n'); out.flush()
