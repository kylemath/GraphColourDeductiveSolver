"""EXPLORE round 6 (exploratory): a fast local version of Job 28's loop (loop28.py), with two changes:
  - B-fixed sender sets are tried LARGEST S FIRST (then ring), up to PER per binding arrangement per round, plus up to
    NSMALL with ring <= SMALLR (cheap; a small D configuration also forbids sibling arrangements);
  - patterns also include the explore-loop verdicts (loop/rules/cert_bf_*.out, loop/lp/r_*.out / *.cfast).
LP: loop/lp/wlp3s.py (wlp3.py + early stop: the dual of the rows found so far, a valid lower-bound certificate).  Per round n: loop/lp/wlp3_xl_<n>.txt (LP output), wlp3_<n>.log, in_<n>.txt, r_<n>.out, r_<n>.cfast, log.txt.
Usage: python3 loop/lp/loopfast.py [start=1] [maxr=3] [per=2] [procs=2] [narr=200] [stall=25] [small=14] [nsmall=12] [cmax=13: cfast only up to this ring]"""
import sys, os, subprocess, re, glob, time, shutil
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); L = os.path.join(HERE, 'loop', 'lp')
opt = dict(a.split('=') for a in sys.argv[1:])
START, MAXR, PER, PROCS, NARR, STALLN, SMALLR, NSMALL, CMAX = (int(opt.get(k, v)) for k, v in (('start', 1), ('maxr', 3), ('per', 2), ('procs', 2), ('narr', 200), ('stall', 25), ('small', 14), ('nsmall', 12), ('cmax', 13)))
DF, DF18, CF = (os.path.join(HERE, 'bin', b) for b in ('dfast', 'dfast18', 'cfast'))
rel = lambda f: os.path.relpath(f, HERE)
BASE = ['pat=out/pairs_D7_k2_dfast.out', 'pat=out/pairs_D8_k3_dfast.out', 'pat=out/pairs_D9_k4_dfast.out',
        'pat=out/eq_D7_dfast.out', 'pat=out/eq_D8_k3_dfast.out', 'pat=out/lp_dfast.out',
        'pat=out/pairs_D10_k5_dfast_partial.out'] + \
       ['pat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'out', 'def_*.out')))] + \
       ['cpat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'job27', '*.cfast')))] + \
       ['cpat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')))] + ['w7plus']
def log(s):
    open(os.path.join(L, 'log.txt'), 'a').write(time.strftime('%m-%d %H:%M ') + s + '\n'); print(s, flush=True)
# gen28 machinery (variants, make, registries) without its main body
src = open(os.path.join(HERE, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', '16']; __file__ = os.path.join(HERE, 'gen28.py'); exec(src)
def verdicts():
    DVx, CVx = {}, {}
    for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.out')) + glob.glob(os.path.join(L, 'r_*.out')) + glob.glob(os.path.join(HERE, 'loop', 'rules', 'cert_bf_*.out')):
        for line in open(fn):
            f = line.split()
            if f and f[0].startswith('f') and ('D=true' in line or 'D=false' in line): DVx[f[0]] = 'D' if 'D=true' in line else 'notD'
    for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.cfast')) + glob.glob(os.path.join(L, 'r_*.cfast')) + glob.glob(os.path.join(HERE, 'loop', 'rules', 'cert_bf*.cfast')):
        cur = None
        for line in open(fn):
            if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
            elif 'C-REDUCIBLE' in line and cur: CVx[cur] = 'C'
            elif 'search |X|' in line and cur: CVx.setdefault(cur, 'neither')
    return DVx, CVx
def par(binary, args, inp, out):
    lines = [l for l in open(inp) if l.strip()]
    if not lines: open(out, 'w').close(); return
    parts = []
    for k in range(PROCS):
        chunk = lines[k::PROCS]
        if chunk: fn = '%s.p%d' % (inp, k); open(fn, 'w').write(''.join(chunk)); parts.append(fn)
    ps = [subprocess.Popen(['nice', '-n', '5', binary, fn] + args, stdout=open(fn + '.o', 'w'), stderr=subprocess.STDOUT) for fn in parts]
    for p in ps: p.wait()
    with open(out, 'w') as o:
        for fn in parts: o.write(open(fn + '.o').read()); os.remove(fn); os.remove(fn + '.o')
for n in range(START, START + MAXR):
    pats = BASE + ['pat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'out', 'job28', 'r_*.out')))] + \
           ['cpat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'out', 'job28', 'r_*.cfast')))] + \
           ['pat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'loop', 'rules', 'cert_bf_*.out')))] + \
           ['pat=' + rel(f) for f in sorted(glob.glob(os.path.join(L, 'r_*.out')))] + \
           ['cpat=' + rel(f) for f in sorted(glob.glob(os.path.join(L, 'r_*.cfast')))] + \
           ['cpat=' + rel(f) for f in sorted(glob.glob(os.path.join(HERE, 'loop', 'rules', 'cert_bf*.cfast')))]
    tight = os.path.join(L, 'tight_%d.txt' % n); allr = os.path.join(L, 'all_%d.txt' % n); warm = os.path.join(L, 'all_%d.txt' % (n - 1))
    cmd = [sys.executable, os.path.join(L, 'wlp3s.py'), 'tag=xl_%d' % n, 'stall=%d' % STALLN, 'tight=' + tight, 'allrows=' + allr] + pats
    if os.path.exists(warm): cmd.append('warm=' + warm)
    t0 = time.time(); wl = os.path.join(L, 'wlp3_%d.log' % n)
    subprocess.run(['nice', '-n', '5'] + cmd, stdout=open(wl, 'w'), stderr=subprocess.STDOUT, cwd=HERE); lp = open(wl).read()
    m = re.search(r't\* = (-?[\d.]+)', lp); t = float(m.group(1)) if m else None
    if t is None: log('round %d: LP failed\n%s' % (n, lp[-2000:])); break
    lpout = os.path.join(L, 'wlp3_xl_%d.txt' % n)
    log('round %d: t* = %.6f (LP %.0f s)' % (n, t, time.time() - t0))
    if t <= 1e-7: log('round %d: LP FEASIBLE' % n); break
    # binding arrangements: receiver rows with positive dual weight, heaviest first
    arrs = []
    for line in open(lpout):
        mm = re.search(r'^\s*([\d.]+)\s+receiver d=(\d+) link (\d+) s (\d+)', line)
        if mm: arrs.append((float(mm.group(1)), int(mm.group(2)), mm.group(3), mm.group(4)))
    arrs.sort(reverse=True); arrs = arrs[:NARR]
    DVx, CVx = verdicts(); new = {}; killed = 0; hard = 0
    for wgt, d, lk, sv in arrs:
        vs = sorted(variants(d, lk, sv), key=lambda x: (-x[1], x[0]))
        if any(DVx.get(x[5]) == 'D' or CVx.get(x[5]) == 'C' for x in vs): killed += 1; continue
        un = [x for x in vs if x[5] not in DVx and x[5] not in new]
        if not un: hard += 1; continue
        k = 0
        for x in un:
            ln = make(d, x[0], x[2], x[3], x[4], x[5])
            if ln and not ln.startswith('RINGMISMATCH'): new[x[5]] = ln; k += 1
            if k >= PER: break
        # also the cheap ones: up to NSMALL variants with ring <= SMALLR (a small D configuration covers many siblings)
        k = 0
        for x in sorted(un, key=lambda x: (x[0], -x[1])):
            if x[0] > SMALLR or k >= NSMALL: break
            if x[5] in new: continue
            ln = make(d, x[0], x[2], x[3], x[4], x[5])
            if ln and not ln.startswith('RINGMISMATCH'): new[x[5]] = ln; k += 1
    inp = os.path.join(L, 'in_%d.txt' % n)
    open(inp, 'w').write(''.join(l + '\n' for l in sorted(new.values(), key=lambda x: int(x.split()[1]))))
    if not new: log('round %d: no new configuration (binding %d, already killed %d, all-tested %d)' % (n, len(arrs), killed, hard)); break
    rout = os.path.join(L, 'r_%d.out' % n); par(DF, [], inp, rout)
    nd = sum(1 for l in open(rout) if 'D=true' in l)
    dset = {x.split()[0] for x in open(rout) if 'D=true' in x}
    cin = os.path.join(L, 'cin_%d.txt' % n); open(cin, 'w').write(''.join(l for l in open(inp) if l.split()[0] not in dset and int(l.split()[1]) <= CMAX))
    cout = os.path.join(L, 'r_%d.cfast' % n); par(CF, ['--search', '--limit', '1'], cin, cout)
    nc = open(cout).read().count('C-REDUCIBLE')
    log('round %d: binding %d (already killed %d, all-tested %d); tested %d: D %d, C %d' % (n, len(arrs), killed, hard, len(new), nd, nc))
