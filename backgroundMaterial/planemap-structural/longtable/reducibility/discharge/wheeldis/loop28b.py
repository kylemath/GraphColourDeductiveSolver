"""Job 28, certificate-attack loop (Long Table, 16 Oct; exploratory).  Each round: solve the forbidden-pattern LP
(wlp3.py) with every D/C verdict so far; take the arrangements of the DUAL CERTIFICATE (positive weight); build ALL their
B-fixed sender sets with ring <= 16 not yet tested (gen28.py 'all', largest S first); dfast18, then cfast on the not-D
ones; add the D/C ones as patterns; repeat.  Patterns also include the explore thread's verdicts under loop/ (any
f/e/p-named .out/.cfast).  One line per solve in out/job28/loop.log.  Usage: python3 loop28b.py DFAST CFAST [start=3]"""
import sys, os, subprocess, re, glob, time
HERE = os.path.dirname(os.path.abspath(__file__)); J = os.path.join(HERE, 'out', 'job28')
DFAST, CFAST = sys.argv[1], sys.argv[2]
opt = dict(a.split('=') for a in sys.argv[3:]); START = int(opt.get('start', 3)); PROCS = int(opt.get('procs', 3))
src = open(os.path.join(HERE, 'loop28.py')).read()
exec(src[src.index('BASE = '):src.index('for n in range(START')])   # BASE, log(), par()
rel = lambda f: os.path.relpath(f, HERE)
for n in range(START, START + 60):
    pats = BASE + ['pat=' + rel(f) for f in sorted(glob.glob(os.path.join(J, 'r_*.out')))] + \
           ['cpat=' + rel(f) for f in sorted(glob.glob(os.path.join(J, 'r_*.cfast')))] + \
           ['pat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'loop', '**', '*.out'), recursive=True))] + \
           ['cpat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'loop', '**', '*.cfast'), recursive=True))] + \
           ['pat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'loop', 'lone', 'u*.pat')))]   # lone-five killers (patterns only)
    allr = os.path.join(J, 'all_%d.txt' % n); warm = sorted(glob.glob(os.path.join(J, 'all_*.txt')))
    cmd = [sys.executable, os.path.join(HERE, 'wlp3.py'), 'tag=j28_%d' % n, 'allrows=' + allr] + pats
    if warm: cmd.append('warm=' + warm[-1])
    lp = subprocess.run(['nice', '-n', '19'] + cmd, capture_output=True, text=True, cwd=HERE).stdout
    m = re.search(r't\* = (-?[\d.]+)', lp); t = float(m.group(1)) if m else None
    if t is None: log('round %d: LP failed\n%s' % (n, lp[-2000:])); break
    lpout = os.path.join(HERE, 'out', 'wlp3_j28_%d.txt' % n)
    ncert = sum(1 for l in open(lpout) if re.search(r'^\s+[\d.]+\s+receiver d=', l))
    if t <= 1e-7: log('round %d: t* = %.6f <= 0: LP FEASIBLE (H28 survives)' % (n, t)); break
    inp = os.path.join(J, 'in_%d.txt' % n)
    g = subprocess.run([sys.executable, os.path.join(HERE, 'gen28.py'), inp, '16', lpout, 'all'],
                       capture_output=True, text=True, cwd=HERE).stdout
    open(os.path.join(J, 'hard_%d.txt' % n), 'w').write(g)
    summ = g.strip().splitlines()[-1] if g.strip() else ''
    nnew = sum(1 for l in open(inp) if l.strip()); nhard = sum(1 for l in g.splitlines() if l.startswith('HARD28'))
    if nnew == 0:
        log('round %d (cert): t* = %.6f; %d certificate receivers; no new configuration (%s); HARD28 %d -> stop' % (n, t, ncert, summ, nhard)); break
    rout = os.path.join(J, 'r_%d.out' % n); par(DFAST, [], inp, rout)
    dset = {x.split()[0] for x in open(rout) if 'D=true' in x}
    cin = os.path.join(J, 'cin_%d.txt' % n); open(cin, 'w').write(''.join(l for l in open(inp) if l.split()[0] not in dset))
    cout = os.path.join(J, 'r_%d.cfast' % n); par(CFAST, ['--search', '--limit', '1'], cin, cout)
    nc = open(cout).read().count('C-REDUCIBLE')
    log('round %d (cert): t* = %.6f; %d certificate receivers; %s; tested %d: D %d, C %d, neither %d; HARD28 %d' % (
        n, t, ncert, summ, nnew, len(dset), nc, nnew - len(dset) - nc, nhard))
