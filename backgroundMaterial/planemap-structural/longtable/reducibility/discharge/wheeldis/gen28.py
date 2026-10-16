"""Job 28 (exploratory): B-fixed receiver-centred configurations for the binding arrangements of a wlp3 run.
For a receiver arrangement (d, link w_0.., s word s_i between w_i and w_i+1) and a sender set S (|S| >= 2) of its
degree-5 link vertices, the B-fixed configuration is u (exact degree d) + S + every link vertex of S at its exact
degree from the arrangement; a letter 9 (degree >= 9) stays free (ring vertex, 'B').  Built with gen.py's builder
(pairs.py layered build); the ring must be a simple induced cycle.  Named f<d>_<link>_<s> (canonical up to the
dihedral group; letters 5..8 exact, B free, '.' outside), which wlp3.py reads as a pattern.
Greedy (as gen.py): an arrangement is killed if some B-fixed S is already D/C (should not happen after the LP);
otherwise its cheapest untested S (ring <= RMAX) is written.  HARD28: every S with ring <= RMAX tested, none D/C.
Registry: out/job28/*.out (dfast18) and out/job28/*.cfast.
Usage: python3 gen28.py OUTFILE RMAX ARRFILE [ARRFILE ...] [all] [small] [maxper=3]  (default order: largest S first)"""
import sys, os, glob, itertools, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[1:]; ALL = 'all' in argv; SMALL = 'small' in argv
MAXPER = int(next((a[7:] for a in argv if a.startswith('maxper=')), '3'))
argv = [a for a in argv if a not in ('all', 'small') and not a.startswith('maxper=')]
OUT, RMAX, FILES = argv[0], int(argv[1]), argv[2:]
gsrc = open(os.path.join(HERE, 'gen.py')).read()
gsrc = gsrc[:gsrc.index('arrs = []')].replace('os.path.dirname(os.path.abspath(__file__))', repr(HERE))
sys.argv = ['gen.py', '/dev/null', '30']; exec(gsrc)
OUT, RMAX, FILES = argv[0], int(argv[1]), argv[2:]   # gen.py's header overwrote them

DV, CV = {}, {}
for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.out')) + glob.glob(os.path.join(HERE, 'loop', '**', '*.out'), recursive=True):
    for line in open(fn):
        f = line.split()
        if f and f[0].startswith('f') and ('D=true' in line or 'D=false' in line):
            DV[f[0]] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.cfast')) + glob.glob(os.path.join(HERE, 'loop', '**', '*.cfast'), recursive=True):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'C-REDUCIBLE' in line and cur: CV[cur] = 'C'
        elif 'search |X|' in line and cur: CV.setdefault(cur, 'neither')

def variants(d, lk, sv):
    snd = [i for i in range(d) if lk[i] == '5']; res = []
    for k in range(2, len(snd) + 1):
        for S in itertools.combinations(snd, k):
            wl = {(i + e) % d for i in S for e in (-1, 0, 1)}; sl = {(i + e) % d for i in S for e in (-1, 0)}
            w = [int(lk[j]) if j in wl and lk[j] != '9' else None for j in range(d)]
            s = [int(sv[j]) if j in sl and sv[j] != '9' else None for j in range(d)]
            r = ringf(d, w, s)
            if r > RMAX: continue
            L_ = ''.join((lk[j] if lk[j] != '9' else 'B') if j in wl else '.' for j in range(d))
            S_ = ''.join((sv[j] if sv[j] != '9' else 'B') if j in sl else '.' for j in range(d))
            key = canon_key(d, L_, S_); nm = 'f%d_%s_%s' % (d, key[1], key[2])
            res.append((r, k, S, w, s, nm))
    # default (Long Table, 16 Oct): largest S first, then smallest ring; 'small' = the round-1 order (ring, |S|)
    return sorted(res, key=(lambda x: (x[0], x[1])) if SMALL else (lambda x: (-x[1], x[0])))
def make(d, r, S, w, s, nm):
    link = [w[j] if w[j] is not None else 9 for j in range(d)]
    adj, name = build(d, link, {('s', j): s[j] for j in range(d) if s[j] is not None})
    inv = {v: x for x, v in name.items()}
    I = [inv[('u',)]] + [inv[('w', j)] for j in range(d) if w[j] is not None] + [inv[('s', j)] for j in range(d) if s[j] is not None]
    deg = {inv[('u',)]: d}; deg.update({inv[('w', j)]: w[j] for j in range(d) if w[j] is not None})
    deg.update({inv[('s', j)]: s[j] for j in range(d) if s[j] is not None})
    c = extract(adj, I, deg)
    if c is None: return None
    if c[0] != r: return 'RINGMISMATCH %s %d %d' % (nm, c[0], r)
    return '%s %d %d %s %s' % ((nm,) + c)

arrs = []
for fn in FILES:
    for line in open(fn):
        m = re.search(r'receiver d=(\d+) link (\d+) s (\d+)', line)
        if m: arrs.append((int(m.group(1)), m.group(2), m.group(3)))
arrs = list(dict.fromkeys(arrs))
new = {}; st = collections.Counter(); hard = []; NOTEXT = set(); bad = []
for d, lk, sv in arrs:
    vs = variants(d, lk, sv)
    if any(DV.get(x[5]) == 'D' or CV.get(x[5]) == 'C' for x in vs): st['killed'] += 1; continue
    if any(DV.get(x[5]) == 'notD' and x[5] not in CV for x in vs): st['pendingC'] += 1; continue
    un = [x for x in vs if x[5] not in DV and x[5] not in NOTEXT]
    if not ALL and any(x[5] in new for x in un): st['pending'] += 1; continue
    got = 0
    for x in un:
        if x[5] in new: continue
        line = make(d, x[0], x[2], x[3], x[4], x[5]); st['built'] += 1
        if line is None: st['notext'] += 1; NOTEXT.add(x[5]); continue
        if line.startswith('RINGMISMATCH'): bad.append(line); NOTEXT.add(x[5]); continue
        new[x[5]] = line; got += 1
        if not ALL and got >= MAXPER: break
    if got or any(x[5] in new for x in un): st['pending'] += 1
    else: st['hard'] += 1; hard.append((d, lk, sv, len(vs)))
lines = sorted(new.values(), key=lambda x: int(x.split()[1]))
open(OUT, 'w').write('\n'.join(lines) + ('\n' if lines else ''))
for h in hard: print('HARD28 d=%d link %s s %s (%d B-fixed sender sets with ring <= RMAX, all tested, none D/C)' % h)
for b in bad: print(b)
print('arrangements', len(arrs), dict(st), 'new configs', len(lines),
      'rings', sorted(collections.Counter(int(x.split()[1]) for x in lines).items()))
