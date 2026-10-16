"""Test loop for defect candidates (README §7.3; exploratory).  Repeats until nothing is left to test:
  1. defect_check2.py CANDS strict7  -> candidates surviving R_opt (strict 7-wheels) / open ones and their needs;
  2. dfast on the needed configurations (smallest ring first), then re-check; then cfast (first hit) on what is left;
  3. the R_opt survivors are checked with option bf (R_opt+), and their B-fixed configurations tested the same way.
Outputs: out/def_loop_<tag>_<round>.out / .cfast (verdicts), and <work>.strict.status, <work>.bf.status.
Usage: python3 defect_loop.py CANDS WORKPREFIX TAG [maxrounds=20] [maxring=16]"""
import sys, os, subprocess, re
HERE = os.path.dirname(os.path.abspath(__file__))
CANDS, WORK, TAG = sys.argv[1], sys.argv[2], sys.argv[3]
MAXR = int(sys.argv[4]) if len(sys.argv) > 4 else 20; RMAX = int(sys.argv[5]) if len(sys.argv) > 5 else 16
env = dict(os.environ, CFAST_FIRST='1')
def check(cands, work, opt):
    out = subprocess.run([sys.executable, os.path.join(HERE, 'defect_check2.py'), cands, work, opt], capture_output=True, text=True).stdout
    print(out.strip().splitlines()[-2:], flush=True)
    return [l for l in open(work + '.status') if not l.startswith('killed')]
def run(kind, src, n):
    lines = [l for l in open(src) if l.strip() and int(l.split()[1]) <= RMAX]
    if not lines: return 0
    fn = '%s.%s%d.in' % (WORK, kind, n); open(fn, 'w').write(''.join(lines))
    of = os.path.join(HERE, 'out', 'def_loop_%s_%d.%s' % (TAG, n, 'out' if kind == 'd' else 'cfast'))
    cmd = [os.path.join(HERE, 'bin', 'dfast'), fn] if kind == 'd' else [os.path.join(HERE, 'bin', 'cfastf'), fn, '--search', '--limit', '1']
    with open(of, 'w') as f: subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env=env)
    return len(lines)
n = 0
for stage, opt, cands in (('strict', 'strict7', CANDS), ('bf', 'bf', None)):
    if cands is None:
        cands = WORK + '.strict.surv'
        open(cands, 'w').write(''.join(l.split(' ', 1)[1] for l in open(WORK + '.strict.status') if l.startswith('SURVIVES')))
    work = WORK + '.' + stage
    for rnd in range(MAXR):
        live = check(cands, work, opt)
        n += 1; nd = run('d', work + '.d', n)
        if nd: live = check(cands, work, opt)
        n += 1; nc = run('c', work + '.c', n)
        print('stage %s round %d: %d not killed, dfast %d, cfast %d' % (stage, rnd, len(live), nd, nc), flush=True)
        if not nd and not nc: break
    live = check(cands, work, opt)
    print('stage %s final:' % stage, ''.join(live), flush=True)
