"""EXPLORE round 44 stage 2: second-engine checks after kc -C on RSST's 633.
kc C -> cfast --fixed with kc's conservative X (kc_cf.cfast).
kc not D, not C (conservative search over |X| <= 4 exhausted) -> diagnostics, kept out of the registry:
  kc -x with RSST's own X (conservative scoring of that X, rsst_x_kc.out), kcc2 -C2 broad search (rsst_C2.out),
  cfast --fixed RSST's X (rsst_C2_cf.cfast), and last cfast --search --limit 1 (rsst_C2_cfsearch.cfast, 900 s cap).  usage: NW=2 python3 cf44.py"""
import os, re, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(H, '..', '..', 'bin'); KC = os.path.join(H, '..', 'kc')
line = {l.split()[0]: l.rstrip('\n') for l in open(os.path.join(H, 'rsst.txt')) if l.strip()}
rx = dict(l.split() for l in open(os.path.join(H, 'rsst_x.txt')) if l.strip())
kc = {}; cur = None
for fn in ('s0_kcc.out', 's1_kcc.out'):
    for l in open(os.path.join(H, fn)):
        if l.startswith('rsst'): cur = l.split()[0]; kc[cur] = ['D' if 'D=true' in l else 'notD', None]
        m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', l)
        if m and cur: kc[cur] = ['C', m.group(1)]
assert len(kc) == 633
def run(cmd, inp=None): return subprocess.run(cmd, input=inp, capture_output=True, text=True).stdout.rstrip('\n')
def cfast(nm, *a):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as t: t.write(line[nm] + '\n')
    o = run([os.path.join(B, 'cfast'), t.name] + list(a)); os.unlink(t.name); return o
def job(nm):
    v, x = kc[nm]
    if v == 'C': return ('kc_cf.cfast', cfast(nm, '--fixed', x))
    if v == 'D': return None
    out = []
    if rx[nm] != '-':
        with tempfile.NamedTemporaryFile('w', suffix='.x', delete=False) as t: t.write('%s %s\n' % (nm, rx[nm]))
        out.append(('rsst_x_kc.out', run([os.path.join(KC, 'kcc'), '-x', t.name], line[nm] + '\n'))); os.unlink(t.name)
        out.append(('rsst_C2_cf.cfast', cfast(nm, '--fixed', rx[nm].strip('{}'))))
    out.append(('rsst_C2.out', run([os.path.join(KC, 'kcc2'), '-C2', '-s', '60', '-t', '1200'], line[nm] + '\n')))
    out.append(('rsst_C2_cf.cfast', cfast(nm, '--search', '--limit', '1')))
    return out
fh = {}
def emit(r):
    for fn, o in ([r] if isinstance(r, tuple) else r):
        if fn not in fh: fh[fn] = open(os.path.join(H, fn), 'w')
        fh[fn].write(o + '\n'); fh[fn].flush()
def diag(nm):          # fast diagnostics first; cfast --search (slow) last, 900 s cap each
    out = []
    if rx[nm] != '-':
        with tempfile.NamedTemporaryFile('w', suffix='.x', delete=False) as t: t.write('%s %s\n' % (nm, rx[nm]))
        out.append(('rsst_x_kc.out', run([os.path.join(KC, 'kcc'), '-x', t.name], line[nm] + '\n'))); os.unlink(t.name)
        out.append(('rsst_C2_cf.cfast', cfast(nm, '--fixed', rx[nm].strip('{}'))))
    out.append(('rsst_C2.out', run([os.path.join(KC, 'kcc2'), '-C2', '-s', '60', '-t', '1200'], line[nm] + '\n')))
    return out
def search(nm):
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as t: t.write(line[nm] + '\n')
    try: o = subprocess.run(['timeout', '900', os.path.join(B, 'cfast'), t.name, '--search', '--limit', '1'], capture_output=True, text=True).stdout.rstrip('\n')
    finally: os.unlink(t.name)
    return ('rsst_C2_cfsearch.cfast', o or (nm + ' cfast --search: no output within 900 s'))
NW = int(os.environ.get('NW', '2'))
C_ = sorted(n for n in kc if kc[n][0] == 'C'); N_ = sorted(n for n in kc if kc[n][0] == 'notD')
with ThreadPoolExecutor(NW) as ex:
    for r in ex.map(job, C_): emit(r)
open(os.path.join(H, 'cfC.DONE'), 'w').write('')
with ThreadPoolExecutor(NW) as ex:
    for r in ex.map(diag, N_): emit(r)
open(os.path.join(H, 'diag.DONE'), 'w').write('')
with ThreadPoolExecutor(NW) as ex:
    for r in ex.map(search, N_): emit(r)
open(os.path.join(H, 'cf.DONE'), 'w').write('')
