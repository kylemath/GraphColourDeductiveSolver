"""EXPLORE round 21 (H-A', exploratory): can a HARD28-like row be forbidden through a neighbouring exact 7?
For each row (u = 7) and each link 7 v of u, v's arrangement is fixed by u at 5 link and 2-4 s letters (pairs.py
view).  Every filling of the free letters over 5-9 (9 = 9+, matched only by B) is checked for a kill at v:
a registered D/C window centred at v (w2.py registry and matching, d = 7 names), or a reducible wheel at v or at
one of its link fives/sixes (R5, R6 for every p, RBIG).  A view is closed if every filling is killed.
Usage: python3 ap.py SEEDS"""
import sys, os, re, glob, itertools, time, collections
import numpy as np
APD = HERE = os.path.dirname(os.path.abspath(__file__)); LOOP = os.path.dirname(HERE); W = os.path.dirname(LOOP)
SEEDS = sys.argv[1]; T0 = time.time()
src = open(os.path.join(LOOP, 'av', 'pairs.py')).read(); exec(src[:src.index('arrs = [')])
view_ = view
src = open(os.path.join(W, 'wlp.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(W, 'wlp.py')), 1)
sys.argv = ['wlp']; exec(src[:src.index('# receiver DP')])
RBIG = set()
for fn in [os.path.join(W, 'out', 'bigwheels_dfast.out'), os.path.join(W, 'out', 'bigwheels1516_dfast_partial.out')] + glob.glob(os.path.join(W, 'out', 'def_*.out')):
    if not os.path.exists(fn): continue
    for line in open(fn):
        f = line.split()
        if f and 'D=true' in line:
            if re.match(r'^c[78]_\d+$', f[0]): RBIG.add(f[0][3:])
            elif fn.endswith('bigwheels_dfast.out'): RBIG.add(f[0].split('_')[1])
for fn in glob.glob(os.path.join(W, 'out', 'def_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '):
            m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = m.group(1) if m else None
        elif 'C-REDUCIBLE' in line and cur: RBIG.add(cur)
RBIG7 = {canon(tuple(map(int, w))) for w in RBIG if len(w) == 7}
src = open(os.path.join(LOOP, 'w2', 'w2.py')).read()
G = {'__file__': os.path.join(LOOP, 'w2', 'w2.py'), '__name__': 'w2'}
sys.argv = ['w2.py', 'cover']; exec(src[:src.index("\nif mode in ('build', 'build8')")], G)
PATS = [(nm, P) for nm, (d, P) in G['PATS'].items() if d == 7]
print('patterns d=7: %d; RBIG 7-wheels %d (%.0fs)' % (len(PATS), len(RBIG7), time.time() - T0), flush=True)
DIG = '56789'
def run_view(L, S):
    d = 7; fixed = list(L) + list(S); free = [j for j, c in enumerate(fixed) if c == '?']
    N = 5 ** len(free); F = np.zeros((N, 14), dtype=np.int8)
    for j, c in enumerate(fixed):
        if c != '?': F[:, j] = int(c) - 5
    for t, j in enumerate(free): F[:, j] = (np.arange(N) // 5 ** t) % 5
    Lc = lambda q: q % d; Sc = lambda q: 7 + q % d
    killed = np.zeros(N, dtype=bool); why = collections.Counter()
    # wheels: R5 at link fives of v, R6 (every p) at link sixes, RBIG at v
    R5T = {};
    for q in range(d):
        a = F[:, Lc(q + 1)].astype(int); b = F[:, Sc(q)].astype(int); c = F[:, Sc(q - 1)].astype(int); e = F[:, Lc(q - 1)].astype(int)
        code = ((a * 5 + b) * 5 + c) * 5 + e
        r5 = np.array([isR5([7, x // 125 + 5, x // 25 % 5 + 5, x // 5 % 5 + 5, x % 5 + 5]) for x in range(625)])
        r6 = np.array([all(isR6([7, x // 125 + 5, x // 25 % 5 + 5, p, x // 5 % 5 + 5, x % 5 + 5]) for p in L_) for x in range(625)])
        k5 = (F[:, Lc(q)] == 0) & r5[code]; k6 = (F[:, Lc(q)] == 1) & r6[code]
        why['R5'] += int((k5 & ~killed).sum()); killed |= k5
        why['R6'] += int((k6 & ~killed).sum()); killed |= k6
    lw = [''.join(str(x + 5) for x in F[n, :7]) for n in range(N)]
    kb = np.array([canon(tuple(map(int, w))) in RBIG7 for w in lw])
    why['RBIG'] += int((kb & ~killed).sum()); killed |= kb
    # windows centred at v
    OK = {s: np.array([str(x + 5) in s for x in range(5)]) for s in ('5', '6', '7', '8', '789')}
    nalign = 0; hitnames = collections.Counter()
    for nm, P in PATS:
        for refl in (0, 1):
            for r in range(d):
                cons = []; ok = True
                for p, m in P:
                    q = ((-p if refl else p) + r) % d; mm = m[::-1] if refl else m
                    cols = [Lc(q), Lc(q + 1), Sc(q), Sc(q - 1), Lc(q - 1)]; sets = ['5'] + list(mm)
                    for col, st in zip(cols, sets):
                        if fixed[col] != '?':
                            if fixed[col] not in st: ok = False; break
                        else: cons.append((col, st))
                    if not ok: break
                if not ok: continue
                nalign += 1
                h = np.ones(N, dtype=bool)
                for col, st in cons: h &= OK[st][F[:, col]]
                new = h & ~killed
                if new.any(): hitnames[nm] += int(new.sum()); killed |= h
                why['window'] += int(new.sum())
    miss = ~killed
    has8 = (F == 3).any(axis=1)
    ex = [(''.join(str(x + 5) for x in F[n, :7]), ''.join(str(x + 5) for x in F[n, 7:])) for n in np.nonzero(miss)[0][:3]]
    return N, int(miss.sum()), int((miss & has8).sum()), dict(why), nalign, hitnames.most_common(3), ex
L_ = (5, 6, 7, 8, 9)
rows = [l.split() for l in open(SEEDS) if l.strip()]
closed_rows = []; nrow7 = 0; out = []
for lk, sv, lab in rows:
    vs = [i for i, ch in enumerate(lk) if ch == '7']
    if vs: nrow7 += 1
    cl = False
    for i in vs:
        t = time.time(); L, S = view_(lk, sv, i)
        N, miss, miss8, why, nal, top, ex = run_view(L, S)
        cl |= miss == 0
        out.append('%s/%s %s v=w%d view %s/%s: fillings %d, killed %d (%s), MISS %d (with an 8: %d), aligns %d, %.1fs; top %s; misses e.g. %s' % (
            lk, sv, lab, i, L, S, N, N - miss, why, miss, miss8, nal, time.time() - t, top, ex))
        print(out[-1], flush=True)
    if cl: closed_rows.append((lk, sv, lab))
summ = ['# ap.py: %d rows, %d with an exact link 7, %d views; closed rows %d (%s); %.0fs' % (
    len(rows), nrow7, len(out), len(closed_rows), ' '.join('%s/%s' % r[:2] for r in closed_rows), time.time() - T0)]
summ.append('H-A\' bars: lives >= %.1f rows (1/3), dies < %.1f (1/6)' % (len(rows) / 3, len(rows) / 6))
open(os.path.join(APD, 'ap.txt'), 'w').write('\n'.join(summ + out) + '\n')
print('\n'.join(summ))
