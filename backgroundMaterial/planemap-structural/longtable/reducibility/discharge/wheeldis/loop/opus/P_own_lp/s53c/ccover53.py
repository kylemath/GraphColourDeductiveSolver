"""s53c copy of s52c/ccover52.py (unchanged). s52c copy of s46c/ccover46.py (unchanged logic; A83 inputs come from the command line).
s46c copy of s41c/ccover41.py (+ EXNAME: C entries held out by name, as the engine's exname=, are not cover candidates).
s41c: copy of s33z/ccover/ccover.py (+ ring size r= per entry, Lean status from CXRing/CXInt entry lists, per-row cover lists to OUTDIR/vrows_cover.txt.gz).
s33z C-cover analysis (Long Table request). For the violated receiver rows of a solution checked with ALL C removed (upperR2 noC noCw,
kill6 / l3q tables built D-only; rows from vfile=, exhaustive), find which C entries cover (= kill) each row:
  - cpat C entries (every cpat= file of ARGS, name-level, same pattern semantics as pcheck.pname / instances: 2d rotations/reflections),
  - C 7-wheels of ROOT/out/def_*.cfast (link word in the C RBIG set; d = 7 rows only).
Sole-cover set = entries that are the only cover of >= 1 row. Then a greedy cover of the rows not covered by the sole set.
usage: python3 ccover52.py VFILE ARGS ROOT XRING_LIST OUTDIR LEAN1[,LEAN2..] EXNAME"""
import gzip
import sys, os, re, glob, collections, json, time
import numpy as np
VF, ARGS, ROOT, XR, OUT = sys.argv[1:6]
EXN = set(l.split()[0] for l in open(sys.argv[7]) if l.strip() and not l.startswith('#')); EXHIT = set()
LEAN = {}
for fn in sys.argv[6].split(','):
    tag = 'CXRing' if 'Ring' in fn else 'CXInt'
    for l in open(fn):
        f = l.split()
        if len(f) >= 3: LEAN[f[2]] = tag
RING = {}
os.makedirs(OUT, exist_ok=True)
if os.path.exists(os.path.join(OUT, 'vrows_cover.txt.gz')): os.remove(os.path.join(OUT, 'vrows_cover.txt.gz'))
LET = (5, 6, 7, 8, 9); LI = {l: i for i, l in enumerate(LET)}
SETS = {'5': (5,), '6': (6,), '7': (7,), '8': (8,), 'B': (7, 8, 9)}
def pname(name):   # = pcheck.pname
    f = name.split('_'); kind = f[0][0]; d = int(f[0][1:]); lk, sv = f[1], f[2]
    assert len(lk) == d and len(sv) == d, name
    out = []
    for typ, word in (('w', lk), ('s', sv)):
        for i, ch in enumerate(word):
            if ch == '.': continue
            if kind == 'p' and ((typ == 'w' and ch == '9') or (typ == 's' and ch == '0')): continue
            assert ch in SETS, name
            if kind != 'f': assert ch in '56B', name
            out.append(((typ, i), frozenset(SETS[ch])))
    return d, tuple(sorted(out))
def insts(d, P):   # = pcheck._instances for one pattern
    out = set()
    for r in range(d):
        for refl in (False, True):
            m = {}
            for (typ, i), S in P:
                j = (i + r) % d if not refl else ((r - i) % d if typ == 'w' else (r - i - 1) % d)
                sl = 2 * j + (0 if typ == 'w' else 1); m[sl] = m.get(sl, 31) & sum(1 << LI[x] for x in S)
            out.add(tuple(sorted(m.items())))
    return sorted(out)
def canon(w):
    w = tuple(w); n = len(w)
    return min(min(s[k:] + s[:k] for k in range(n)) for s in (w, w[::-1]))
t0 = time.time()
# ---- C entries
ENT = []   # (id, kind, name, file, d, insts or wordset)
seen = {}
for a in open(ARGS).read().split():
    if not a.startswith('cpat='): continue
    fn = a.split('=', 1)[1]; fn = fn[:-4] if fn.endswith(':all') else fn
    p = fn if os.path.isabs(fn) else os.path.join(ROOT, fn)
    if not os.path.exists(p): continue
    cur = None
    for line in open(p):
        if ' r=' in line and not line.startswith(' '):
            cur = line.split()[0]; m_ = re.search(r' r=(\d+)', line)
            if m_ and cur not in RING: RING[cur] = int(m_.group(1))
        elif 'C-REDUCIBLE' in line and cur and re.match(r'^[epf]\d+_', cur):
            if cur in EXN: EXHIT.add(cur); continue   # s46c: held out (exname)
            if cur in seen: continue   # one entry per name (first cpat file listed); same name = same pattern
            d, P = pname(cur); seen[cur] = len(ENT); ENT.append(('cpat', cur, fn, d, insts(d, P)))
CW = {}
for fn in glob.glob(os.path.join(ROOT, 'out', 'def_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '):
            m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = m.group(1) if m else None
            m_ = re.search(r' r=(\d+)', line)
            if cur and m_: RING.setdefault('c7_' + ''.join(map(str, canon(map(int, cur)))), int(m_.group(1)))
        elif 'C-REDUCIBLE' in line and cur:
            w = ''.join(map(str, canon(map(int, cur)))); CW.setdefault(w, os.path.relpath(fn, ROOT))
for w, fn in sorted(CW.items()): ENT.append(('cwheel', 'c7_' + w, fn, 7, w))
XRN = set(l.split()[0] for l in open(XR) if l.strip() and not l.startswith('#'))
print('exname: %d names held out, %d of them met in cpat files' % (len(EXN), len(EXHIT)))
print('C entries: %d cpat (%d distinct names, %d files), %d C 7-wheels; %.1fs' % (
    sum(e[0] == 'cpat' for e in ENT), len({e[1] for e in ENT if e[0] == 'cpat'}), len({e[2] for e in ENT if e[0] == 'cpat'}), len(CW), time.time() - t0))
# ---- rows
RW = collections.defaultdict(list)
for line in open(VF):
    f = line.split()
    if len(f) < 5: continue
    RW[int(f[0])].append((f[3], f[4], float(f[2])))
print('violated rows: %d; by d %s' % (sum(len(v) for v in RW.values()), {d: len(v) for d, v in sorted(RW.items())}))
# ---- cover vectors
cnt = {}; first = {}; byent = collections.Counter(); bitsd = {}
for d, rows in sorted(RW.items()):
    n = len(rows)
    L = np.zeros((n, 2 * d), np.uint8)
    for k, (lk, sv, ex) in enumerate(rows):
        for i, c in enumerate(lk): L[k, 2 * i] = LI[int(c)]
        for i, c in enumerate(sv): L[k, 2 * i + 1] = LI[int(c)]
    cache = {}
    def sm(s, m):
        if (s, m) not in cache: cache[(s, m)] = ((m >> L[:, s].astype(np.int64)) & 1).astype(bool)
        return cache[(s, m)]
    links = None
    C = np.zeros(n, np.int32); F = np.full(n, -1, np.int64); vecs = {}
    for ei, e in enumerate(ENT):
        if e[3] != d: continue
        if e[0] == 'cpat':
            v = np.zeros(n, bool)
            for I in e[4]:
                u = np.ones(n, bool)
                for s, m in I: u &= sm(s, m)
                v |= u
        else:
            if links is None: links = np.array([''.join(map(str, canon(map(int, lk)))) for lk, sv, ex in rows])
            v = links == e[4]
        k = int(v.sum())
        if not k: continue
        byent[ei] = k; C += v; F[v & (F < 0)] = ei; vecs[ei] = np.packbits(v)
    cnt[d] = C; first[d] = F; bitsd[d] = vecs
    if n:
        M_ = np.zeros((n, len(vecs)), bool); ks = sorted(vecs)
        for j, ei in enumerate(ks): M_[:, j] = np.unpackbits(vecs[ei], count=n).astype(bool)
        with gzip.open(os.path.join(OUT, 'vrows_cover.txt.gz'), 'at') as zf:
            for k, (lk, sv, ex) in enumerate(rows):
                zf.write('%d %s %s %.6g | %s\n' % (d, lk, sv, ex, ' '.join(ENT[ks[j]][1] for j in np.nonzero(M_[k])[0])))
        del M_
    print('d=%d: %d rows, covered %d, uncovered %d, max covers %d; %.1fs' % (d, n, int((C > 0).sum()), int((C == 0).sum()), int(C.max()) if n else 0, time.time() - t0))
# ---- sole covers
sole = collections.Counter()
for d in cnt:
    C, F, vecs = cnt[d], first[d], bitsd[d]
    one = C == 1
    if not one.any(): continue
    # the sole cover of a count-1 row is the only entry covering it -> F (first cover) is that entry
    for ei, c in collections.Counter(F[one].tolist()).items(): sole[ei] = c
S = set(sole)
# rows left: count >= 2 and not covered by any sole entry
left = {}; nleft = 0
for d in cnt:
    n = len(cnt[d]); cov = np.zeros(n, bool)
    for ei in S:
        if ei in bitsd[d]: cov |= np.unpackbits(bitsd[d][ei], count=n).astype(bool)
    lm = (~cov) & (cnt[d] > 0); left[d] = lm; nleft += int(lm.sum())
print('sole-cover entries: %d (covering %d count-1 rows); rows with >= 2 covers not covered by the sole set: %d' % (len(S), sum(sole.values()), nleft))
# greedy on the left rows only: per entry, its cover restricted to the left rows (bool vectors over the left rows of each d)
G = []; sub = collections.defaultdict(dict); rem = {}
for d in left:
    idx = np.nonzero(left[d])[0]; rem[d] = np.ones(len(idx), bool)
    if not len(idx): continue
    for ei, pv in bitsd[d].items():
        u = np.unpackbits(pv, count=len(left[d])).astype(bool)[idx]
        if u.any(): sub[d][ei] = u
while sum(int(r.sum()) for r in rem.values()):
    tot = collections.Counter()
    for d in rem:
        if not rem[d].any(): continue
        for ei, u in sub[d].items():
            k = int((u & rem[d]).sum())
            if k: tot[ei] += k
    ei, k = max(tot.items(), key=lambda x: (x[1], -x[0]))
    G.append((ei, k))
    for d in rem:
        if ei in sub[d]: rem[d] &= ~sub[d][ei]
unc = sum(int((cnt[d] == 0).sum()) for d in cnt)
def lab(ei): e = ENT[ei]; return '%s r=%s %s [%s]' % (e[1], RING.get(e[1], '?'), LEAN.get(e[1], 'notLean'), os.path.basename(e[2]))
def isx(ei): return ENT[ei][1] in XRN
with open(os.path.join(OUT, 'ccover_summary.txt'), 'w') as f:
    f.write('# C-cover analysis: VFILE %s\n# ARGS %s\n# EXNAME %s (%d names; %d met in cpat files, not candidates)\n' % (VF, ARGS, sys.argv[7], len(EXN), len(EXHIT)))
    f.write('violated rows (all C out): %d; by d %s\n' % (sum(len(v) for v in RW.values()), {d: len(v) for d, v in sorted(RW.items())}))
    f.write('rows with no cpat / C 7-wheel cover: %d\n' % unc)
    f.write('sole-cover set: %d entries; greedy cover of the rest: %d entries; total %d\n' % (len(S), len(G), len(S) + len(G)))
    f.write('overlap with the 89 XRing entries: sole %d, greedy %d\n' % (sum(isx(e) for e in S), sum(isx(e) for e, k in G)))
    f.write('## sole-cover set (entry, #rows it alone covers, #rows it covers)\n')
    for ei in sorted(S, key=lambda e: (-sole[e], ENT[e][1])): f.write('S %s sole=%d cov=%d%s\n' % (lab(ei), sole[ei], byent[ei], ' XRING' if isx(ei) else ''))
    f.write('## greedy cover (order, entry, #new rows)\n')
    for i, (ei, k) in enumerate(G): f.write('G%d %s new=%d cov=%d%s\n' % (i + 1, lab(ei), k, byent[ei], ' XRING' if isx(ei) else ''))
    f.write('## XRing entries covering >= 1 violated row: %d of 89\n' % len({ENT[e][1] for e in byent if isx(e)}))
json.dump({'sole': [lab(e) for e in sorted(S)], 'greedy': [lab(e) for e, k in G],
           'cover_count_by_entry': {lab(e): c for e, c in byent.items()}}, open(os.path.join(OUT, 'ccover.json'), 'w'), indent=0)
with open(os.path.join(OUT, 'cover_list.txt'), 'w') as f:
    f.write('# name ring lean role(S=sole,G=greedy) file\n')
    for ei in sorted(S, key=lambda e: (-sole[e], ENT[e][1])): f.write('%s %s %s S %s\n' % (ENT[ei][1], RING.get(ENT[ei][1], '?'), LEAN.get(ENT[ei][1], 'notLean'), os.path.basename(ENT[ei][2])))
    for ei, k in G: f.write('%s %s %s G %s\n' % (ENT[ei][1], RING.get(ENT[ei][1], '?'), LEAN.get(ENT[ei][1], 'notLean'), os.path.basename(ENT[ei][2])))
with open(os.path.join(OUT, 'entries_used.txt'), 'w') as f:
    f.write('# every C entry covering >= 1 violated row: name ring lean #rows-covered #rows-sole file\n')
    for ei in sorted(byent, key=lambda e: -byent[e]): f.write('%s %s %s %d %d %s\n' % (ENT[ei][1], RING.get(ENT[ei][1], '?'), LEAN.get(ENT[ei][1], 'notLean'), byent[ei], sole.get(ei, 0), os.path.basename(ENT[ei][2])))
print(open(os.path.join(OUT, 'ccover_summary.txt')).read()[:4000])
print('done %.1fs' % (time.time() - t0))
