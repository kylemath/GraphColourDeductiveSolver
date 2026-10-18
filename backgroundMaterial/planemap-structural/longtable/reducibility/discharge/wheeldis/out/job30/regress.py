"""Job 30 regression (a): identical separation queries to the old and the new sep3x binaries; outputs must be equal.
Uses run29b's registry and the j29 one-off solution's (y, x) at threshold d - 6 + t - DELTA, d = 7..12, top 20 rows,
default node limit. The registry has no whole-arrangement patterns, so the new section is empty.
Usage: WLP3X_DEF=1 python3 out/job30/regress.py <pattern args>"""
import sys, os, json, subprocess
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SOL = json.load(open(os.path.join(HERE, 'out', 'wlp3x_j29_dump_x_sol.json'))); DELTA = 0.4
EXCL = ('hr1_or1',) if os.environ.get('WLP3X_DEF') == '1' else ('out/def_', 'hr1_or1')
PARGS = [a for a in sys.argv[1:] if not (a.startswith(('pat=', 'cpat=')) and any(e in a for e in EXCL))]
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3', 'tag=reg30'] + PARGS
exec(src[:src.index('A_ub, b_ub = [], []')])
SEP.stdin.close(); SEP.wait()
yv = [0.0] * len(roots)
for k, v in SOL['y'].items():
    u, rest = k.split('|'); yv[ix[(int(u),) + tuple(int(c) for c in rest)]] = v
xs = [(int(k), v) for k, v in SOL['x'].items()]; t = SOL['t']
Q = ''.join('q %d %.12f %d %d\n%s\nX %d %s\n' % (d, d - 6 + t - DELTA, 20, 0, ' '.join('%.12f' % x for x in yv),
            len(xs), ' '.join('%d %.12f' % kv for kv in xs)) for d in range(7, 13))
# Rule T check (MODE=T): sep3xt with flags merged (every flag var = the plain root var) and T = 0 vs sep3xf
MODE = os.environ.get('MODE', '')
SFT = SF + '.T'
if MODE == 'R':   # Job 31: sep3r with its R section (copied from a wlp3r6 static file) and y6b = 0
    rs = open(os.path.join(HERE, 'bin', 'sep3_r6chk.in')).read(); rsec = rs[rs.rindex('\nR\n') + 1:]
    open(SFT, 'w').write(open(SF).read() + rsec)
    n6b = len(rsec.split('\n')[1:]) and max(int(x) for l in rsec.split('\n')[1:] for x in l.split()) + 1
    QT = ''.join(blk + 'R %d %s\n' % (n6b, ' '.join(['0'] * n6b)) for blk in [b_ for b_ in Q.split('q ') if b_] for blk in ['q ' + blk])
elif MODE == 'TF':   # option F table, every one of the 36 flag slots = the plain root var (merged), T = 0
    tl = ['TF']
    for U in (7, 8, 9):
        for (wp, sp, wc) in states:
            for sc in L:
                for wn in L:
                    v = ix[root([U, wn, sc, sp, wp], 0)] if (wc == 5 and not isR5([U, wn, sc, sp, wp])) else -1
                    fv = [-1] * 36
                    for ca in (range(1, 6) if wn == 6 else (0,)):
                        for ce in (range(1, 6) if wp == 6 else (0,)): fv[ca * 6 + ce] = v
                    tl.append(' '.join(map(str, fv)))
    open(SFT, 'w').write(open(SF).read() + '\n'.join(tl) + '\n')
    QT = ''.join(blk + 'T 0 0 0 -1 -1 -1\n' for blk in [b_ for b_ in Q.split('q ') if b_] for blk in ['q ' + blk])
elif MODE == 'T':
    tl = ['T']
    for U in (7, 8, 9):
        for (wp, sp, wc) in states:
            for sc in L:
                for wn in L:
                    v = ix[root([U, wn, sc, sp, wp], 0)] if (wc == 5 and not isR5([U, wn, sc, sp, wp])) else -1
                    tl.append('%d %d %d %d' % (v, v if wp == 6 else -1, v if wn == 6 else -1, v if (wp == 6 and wn == 6) else -1))
    open(SFT, 'w').write(open(SF).read() + '\n'.join(tl) + '\n')
    Q = Q.replace('\nX ', '\nX ').replace('\nq ', '\nq ')
    QT = ''.join(blk + 'T 0 0 0 -1 -1 -1\n' for blk in [b_ for b_ in Q.split('q ') if b_] for blk in ['q ' + blk])
outs = {}
for b in (('sep3xf', 'sep3r') if MODE == 'R' else ('sep3xf', 'sep3xt') if MODE in ('T', 'TF') else ('sep3x_new', 'sep3xf')):
    p = subprocess.run([os.path.join(HERE, 'bin', b), SFT if b in ('sep3xt', 'sep3r') else SF], input=QT if b in ('sep3xt', 'sep3r') else Q, capture_output=True, text=True)
    outs[b] = p.stdout; open(os.path.join(HERE, 'out', 'job30', 'reg_%s.txt' % b), 'w').write(p.stdout)
    print(b, 'lines', p.stdout.count('\n'), 'END lines:', [l for l in p.stdout.splitlines() if l.startswith('END')])
k_ = list(outs); print('IDENTICAL' if outs[k_[0]] == outs[k_[1]] else 'DIFFERENT')
