"""Job 28 driver (exploratory): forbidden-pattern LP (wlp3.py) -> B-fixed configurations of the binding arrangements
(gen28.py) -> dfast18 (ring <= 16) -> cfast --search --limit 1 on the not-D ones -> add D/C as patterns -> repeat.
Stops when t* <= 1e-7, when a round writes no new configuration (every binding arrangement HARD28 or pending), or
after MAXR rounds.  Per round n: out/wlp3_j28_<n>.txt, out/job28/in_<n>.txt, out/job28/r_<n>.out, r_<n>.cfast,
out/job28/hard_<n>.txt; one summary line per round in out/job28/loop.log.
Usage: python3 loop28.py DFAST CFAST [start=1] [maxr=40] [procs=3]"""
import sys, os, subprocess, re, glob, time
HERE = os.path.dirname(os.path.abspath(__file__)); J = os.path.join(HERE, 'out', 'job28')
DFAST, CFAST = sys.argv[1], sys.argv[2]
opt = dict(a.split('=') for a in sys.argv[3:])
START, MAXR, PROCS = int(opt.get('start', 1)), int(opt.get('maxr', 40)), int(opt.get('procs', 3))
BASE = ['pat=out/pairs_D7_k2_dfast.out', 'pat=out/pairs_D8_k3_dfast.out', 'pat=out/pairs_D9_k4_dfast.out',
        'pat=out/eq_D7_dfast.out', 'pat=out/eq_D8_k3_dfast.out', 'pat=out/lp_dfast.out',
        'pat=out/pairs_D10_k5_dfast_partial.out'] + \
       ['pat=' + os.path.relpath(f, HERE) for f in sorted(glob.glob(os.path.join(HERE, 'out', 'def_*.out')))] + \
       ['cpat=' + os.path.relpath(f, HERE) for f in sorted(glob.glob(os.path.join(HERE, 'job27', '*.cfast')))] + \
       ['cpat=' + os.path.relpath(f, HERE) for f in sorted(glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')))] + ['w7plus']
def log(s):
    open(os.path.join(J, 'loop.log'), 'a').write(time.strftime('%m-%d %H:%M ') + s + '\n'); print(s, flush=True)
def par(binary, args, inp, out):
    lines = [l for l in open(inp) if l.strip()]
    if not lines: open(out, 'w').close(); return
    parts = []
    for k in range(PROCS):
        chunk = lines[k::PROCS]
        if not chunk: continue
        fn = '%s.p%d' % (inp, k); open(fn, 'w').write(''.join(chunk)); parts.append(fn)
    ps = [subprocess.Popen(['nice', '-n', '15', binary, fn] + args, stdout=open(fn + '.o', 'w'), stderr=subprocess.STDOUT)
          for fn in parts]
    for p in ps: p.wait()
    with open(out, 'w') as o:
        for fn in parts: o.write(open(fn + '.o').read()); os.remove(fn); os.remove(fn + '.o')
for n in range(START, START + MAXR):
    pats = BASE + ['pat=' + os.path.relpath(f, HERE) for f in sorted(glob.glob(os.path.join(J, 'r_*.out')))] + \
           ['cpat=' + os.path.relpath(f, HERE) for f in sorted(glob.glob(os.path.join(J, 'r_*.cfast')))]
    tight = os.path.join(J, 'tight_%d.txt' % n); allr = os.path.join(J, 'all_%d.txt' % n)
    warm = os.path.join(J, 'all_%d.txt' % (n - 1))
    cmd = [sys.executable, os.path.join(HERE, 'wlp3.py'), 'tag=j28_%d' % n, 'tight=' + tight, 'allrows=' + allr] + pats
    if os.path.exists(warm): cmd.append('warm=' + warm)
    lp = subprocess.run(['nice', '-n', '15'] + cmd, capture_output=True, text=True, cwd=HERE).stdout
    m = re.search(r't\* = (-?[\d.]+)', lp); t = float(m.group(1)) if m else None
    pm = re.search(r"patterns (\{.*?\});", lp)
    if t is None: log('round %d: LP failed\n%s' % (n, lp[-2000:])); break
    lpout = os.path.join(HERE, 'out', 'wlp3_j28_%d.txt' % n)
    if t <= 1e-7: log('round %d: t* = %.6f <= 0: LP FEASIBLE (H28 survives)' % (n, t)); break
    inp = os.path.join(J, 'in_%d.txt' % n)
    g = subprocess.run([sys.executable, os.path.join(HERE, 'gen28.py'), inp, '16', lpout, tight], capture_output=True, text=True, cwd=HERE).stdout
    open(os.path.join(J, 'hard_%d.txt' % n), 'w').write(g)
    summ = g.strip().splitlines()[-1] if g.strip() else ''
    nnew = sum(1 for l in open(inp) if l.strip())
    nhard = sum(1 for l in g.splitlines() if l.startswith('HARD28'))
    if nnew == 0:
        log('round %d: t* = %.6f; no new configuration (%s); HARD28 %d -> stop' % (n, t, summ, nhard)); break
    rout = os.path.join(J, 'r_%d.out' % n); par(DFAST, [], inp, rout)
    nd = sum(1 for l in open(rout) if 'D=true' in l)
    notd = [l for l in open(inp) if l.split()[0] not in {x.split()[0] for x in open(rout) if 'D=true' in x}]
    cin = os.path.join(J, 'cin_%d.txt' % n); open(cin, 'w').write(''.join(notd))
    cout = os.path.join(J, 'r_%d.cfast' % n); par(CFAST, ['--search', '--limit', '1'], cin, cout)
    nc = open(cout).read().count('C-REDUCIBLE')
    log('round %d: t* = %.6f; %s; tested %d: D %d, C %d, neither %d; HARD28 %d' % (n, t, summ, nnew, nd, nc, nnew - nd - nc, nhard))
