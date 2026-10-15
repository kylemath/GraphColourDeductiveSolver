"""Job 22 (Studio, exploratory): K <= 1 / K <= 2 key lists with R extended by the Lean-certified C wheels.
Enumeration as k1keys.py (degrees 5..DMAX, canonical 2-ball keys) but with at most KMAX vertices of degree >= 7.
New status of a key:
  R    old R (W12 / diamond / S66 / J9-D / EXT-D), or centre word 66666 (Job 16), or D in a Studio dfast18 run
       (Job 14, Job 13, studio14b);
  Rc   centre word is one of the 11 Lean-certified C 5-wheels (Job 21, dcheck/CWheels.lean);
  Rx   centre not in R, but some first-ring vertex x_k of degree 5 or 6 has its whole link inside the ball and the
       link word is a certified C wheel (66666 or the 11 5-wheels; the 6 certified 6-wheels).  Sub-configuration;
  notD tested, not D (and not caught above);  U untested.
The six 565xxx 6-wheels are not certified (studio17/UNCERTIFIED.md) and are not used.
dfast18 timings are read from studio1*/part*.out under this directory and under $STUDIO_OUT_ROOT (if set).
Writes b8b/out/k2size_v3.txt.  Usage: python3 k2size_v3.py [DMAX=8] [KMAX=2]"""
import sys, os, glob, itertools, collections, re
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.join(os.path.dirname(HERE), ""); sys.path.insert(0, DIS)
import ball, h0

DMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 2
canon = lambda w: ''.join(map(str, ball.wheel_canon([int(c) for c in w])))
C5 = {canon(w) for w in ('55558', '55568', '55577', '55578', '55588', '55658', '56568', '56577', '56578', '56588',
                         '56658')}
C6 = {canon(w) for w in ('555577', '555677', '555767', '555777', '556577', '566577')}
C5x = C5 | {'66666'}
if os.environ.get('NOC'): C5, C6, C5x = set(), set(), set()   # sanity run: C wheels off
OUT = 'k2size_v3%s.txt' % ('_noC' if os.environ.get('NOC') else '')

ext = h0.load_ext(); j9 = h0.load_j9()
dres = {}
for fn in ('out/dres-K1-studio.txt', 'studio13/dres-r15-16-studio.txt'):
    for line in open(os.path.join(DIS, fn)):
        if line.startswith('#'): continue
        f = line.split(); dres[f[0]] = f[2]
for fn in glob.glob(os.path.join(DIS, 'studio14b', 'part*.out')):
    for line in open(fn):
        if line.startswith('k') and ' D=' in line:
            dres[line.split()[0][1:]] = 'D' if 'D=true' in line else 'notD'

tsum = collections.defaultdict(list)
roots = [DIS] + ([os.environ['STUDIO_OUT_ROOT']] if os.environ.get('STUDIO_OUT_ROOT') else [])
for fn in {f for r in roots for f in glob.glob(os.path.join(r, 'studio1*', 'part*.out'))}:
    for line in open(fn):
        m = re.search(r' r=(\d+) .* (\d+)ms$', line.strip())
        if m and line.startswith('k'): tsum[int(m.group(1))].append(int(m.group(2)) / 1000)

degs = range(5, DMAX + 1)
blocks = []
for dx in degs:
    for privs in itertools.product(degs, repeat=dx - 5):
        for ds in degs:
            b = (dx, tuple(privs), ds)
            blocks.append((b, sum(1 for d in (dx,) + tuple(privs) + (ds,) if d >= 7)))
bybig = collections.defaultdict(list)
for b, nb in blocks: bybig[nb].append(b)

def diamond_like(cfg):   # as k1keys.py / nbhd.py
    r, m, D, ia, ra = cfg
    A = [set(x) for x in ia]
    for a in range(m):
        for b in A[a]:
            if b < a: continue
            com = [c for c in A[a] & A[b]]
            if len(com) != 2: continue
            c, d = com
            if D[c] == 5 and D[d] == 5 and d not in A[c]:
                if (D[a], D[b]) == (5, 5) or {D[a], D[b]} == {5, 6}: return True
    return False

def link_hit(key):
    """A first-ring x_k of degree 5/6 whose link word (5, x_{k-1}, s_{k-1}, privates, s_k, x_{k+1}) is certified C."""
    for k in range(5):
        dx = key[k][0]
        if dx not in (5, 6): continue
        w = [5, key[k - 1][0], key[k - 1][2]] + list(key[k][1]) + [key[k][2], key[(k + 1) % 5][0]]
        cw = ''.join(map(str, ball.wheel_canon(w)))
        if (dx == 5 and cw in C5x) or (dx == 6 and cw in C6): return cw
    return None

seen = set(); out = []
def rec(prefix, nbig):
    if len(prefix) == 5:
        key = ball.canon_blocks(prefix)
        if key in seen: return
        seen.add(key); emit(key, nbig); return
    for nb in range(0, KMAX - nbig + 1):
        for b in bybig[nb]: rec(prefix + [b], nbig + nb)

def emit(key, nbig):
    ks = ball.key_str(key); r = ball.ring_size(key)
    word = ''.join(map(str, ball.wheel_canon([b[0] for b in key])))
    if word in h0.W12: st = 'R'
    else:
        cfg = ball.build(key)
        if cfg is None: return
        if diamond_like(cfg) or word == '66666': st = 'R'
        else:
            nm = ball.key_to_66666_name(key)
            if nm in j9: st = 'R' if j9[nm] else 'notD'
            elif ks in ext: st = 'R' if ext[ks] else 'notD'
            elif ks in dres and not os.environ.get('NODRES'): st = 'R' if dres[ks] == 'D' else 'notD'
            else: st = 'U'
    if st != 'R':
        if word in C5: st = 'Rc'
        elif link_hit(key): st = 'Rx'
    out.append((ks, r, nbig, st))

rec([], 0)
lines = []
P = lambda *a: lines.append(' '.join(str(x) for x in a))
P('# Job 22 (Studio): K<=%d key sizes, DMAX=%d, R extended by Lean-certified C wheels (11 C5 + 66666, 6 C6)' % (KMAX, DMAX))
for K in range(KMAX + 1):
    C = collections.Counter(t[3] for t in out if t[2] == K)
    P('K=%d keys %d' % (K, sum(C.values())), dict(sorted(C.items())))
for K in range(1, KMAX + 1):
    U = [t for t in out if t[2] == K and t[3] in ('U', 'notD')]
    byr = collections.Counter((t[1], t[3]) for t in U)
    P('K=%d non-R (U + notD) %d; by (ring, status):' % (K, len(U)), dict(sorted(byr.items())))
    if K == 1:
        for t in U: P('   ', t[0], 'ring', t[1], t[3])
    cpu = 0.0; miss = set()
    for t in U:
        if t[3] != 'U': continue
        ts = tsum.get(t[1])
        if ts: cpu += sum(ts) / len(ts)
        else: miss.add(t[1])
    nU = sum(1 for t in U if t[3] == 'U'); le16 = sum(1 for t in U if t[3] == 'U' and t[1] <= 16)
    P('   untested %d (ring <= 16: %d, ring >= 17: %d); dfast18 CPU-h at measured per-ring means: %.0f%s' % (
        nU, le16, nU - le16, cpu / 3600, ' (no timing for rings %s)' % sorted(miss) if miss else ''))
P('dfast18 mean s per key by ring:', {r: round(sum(v) / len(v)) for r, v in sorted(tsum.items())})
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
open(os.path.join(HERE, 'out', OUT), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
