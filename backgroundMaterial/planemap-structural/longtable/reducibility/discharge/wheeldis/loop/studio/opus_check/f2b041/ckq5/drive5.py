# f2b041 CKQ5 (Studio): the 5 q7- k3p C entries that leaked into the keep tables (names.txt,
# several lines -> name#a, #b): kc -C -s 60 -t 600 (kc's X), then cfast --fixed {kc X}. Studio engines, nice 10.
import os, re, subprocess
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..'))
KC = os.path.join(W, 'loop', 'kc', 'kc'); CF = os.path.join(W, '..', 'studio15', 'cfast')
def run(c): return subprocess.run(['nice', '-n', '10'] + c, capture_output=True, text=True).stdout.strip().replace('\n', ' // ')
jobs = []
for l in open(os.path.join(H, 'names.txt')):
    n, tag, lines = l.rstrip('\n').split('\t'); L = [x.split(' @ ') for x in lines.split('|')]
    for k, (kcl, src) in enumerate(L): jobs.append((n if len(L) == 1 else '%s#%s' % (n, 'ab'[k]), n, tag, kcl, src))
def one(j):
    nm, n, tag, kcl, src = j; tf = os.path.join(H, 'tmp', re.sub(r'[^A-Za-z0-9_.-]', '_', nm) + '.in'); open(tf, 'w').write('%s %s\n' % (n, kcl))
    k = run([KC, '-C', '-s', '60', '-t', '600', tf]); m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', k); x = m.group(1) if m else ''
    c = run([CF, tf, '--fixed', x]) if x else ''
    return '\t'.join([nm, tag, src, kcl, x, k, c])
with ThreadPoolExecutor(int(os.environ.get('NPAR', '4'))) as ex, open(os.path.join(H, 'results5.tsv'), 'w') as out:
    for r in ex.map(one, jobs): out.write(r + '\n'); out.flush()
