"""EXPLORE round 14 (exploratory): small B-fixed windows over the d = 7 tight family (H-W2).
A small window is gen28's B-fixed configuration with |S| = 2 or 3: u at exact degree 7, S a set of link fives, every
neighbour of S at its exact letter (9 -> B, a free ring vertex).  Its f7_ name has '.' outside, so one D verdict
forbids every d = 7 arrangement that contains it (wlp3 matches f-patterns on the rooted words of S).
  build OUT RMAX FAMILY...  write the untested |S| <= 3 windows with ring <= RMAX (dfast lines) to OUT
  build8 OUT RMAX FAMILY... round 15: the same windows with every 8 made free (B = 7/8/9), rows with an 8 only
  cover FAMILY...           per arrangement: forbidden by a registry D/C pattern (any f/e/p name, any S), or not
Family files: any lines with 'd=<d> link L s S', d in DS (default 7; 'ds=8,9' for round 16).  Registry: every *.out / *.cfast under out/, job27/, loop/ (oracle
files are .pat, never read), plus loop/lone/u*.pat (receiver-free D windows, as in Job 28's pattern list)."""
import sys, os, glob, re, itertools, collections
W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
mode, argv = sys.argv[1], sys.argv[2:]
DS = {7}   # receiver degrees to read from the family files; 'ds=8,9' changes it (round 16)
for a in [a for a in argv if a.startswith('ds=')]: DS = {int(x) for x in a[3:].split(',')}; argv.remove(a)
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
RM = argv[1] if mode in ('build', 'build8') else (argv[2] if mode == 'buildall' else '14')
sys.argv = ['gen28.py', '/dev/null', RM, 'small']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)

def family(files):
    seen, out = set(), []
    for fn in files:
        for line in open(fn):
            m = re.search(r'd=(\d+) link (\d+) s (\d+)', line)
            if not m or int(m.group(1)) not in DS: continue
            k = (int(m.group(1)),) + canon(m.group(2), m.group(3))
            if k not in seen: seen.add(k); out.append((m.group(2), m.group(3), os.path.basename(fn)))
    return out
def images(lk, sv):
    d = len(lk)
    for r in range(d):
        a, b = lk[r:] + lk[:r], sv[r:] + sv[:r]; yield a, b
        yield ''.join(a[-i % d] for i in range(d)), ''.join(b[(-i - 1) % d] for i in range(d))
def canon(lk, sv): return min(images(lk, sv))
# (family keys carry d, so rows of different degree never merge)

# registry: name -> 'D' / 'notD' (dfast), C from cfast
DV, CV = {}, {}
for fn in glob.glob(os.path.join(W, 'out', '**', '*.out'), recursive=True) + glob.glob(os.path.join(W, 'loop', '**', '*.out'), recursive=True) + glob.glob(os.path.join(W, 'loop', 'lone', 'u*.pat')):
    for line in open(fn):
        f = line.split()
        if f and re.match(r'^[epfg]\d*', f[0]) and ('D=true' in line or 'D=false' in line):
            if DV.get(f[0]) != 'D': DV[f[0]] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(W, '**', '*.cfast'), recursive=True):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'C-REDUCIBLE' in line and cur: CV[cur] = 'C'
PEND = set()
for fn in glob.glob(os.path.join(W, 'out', 'job28', 'in_*.txt')):
    for line in open(fn): PEND.add(line.split()[0])
PEND -= set(DV)

SETS = {'5': '5', '6': '6', '7': '7', '8': '8', 'B': '789'}
def parse(nm):
    f = nm.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]; k0 = f[0][0]
    def L(ch, kind):
        if ch == '.' or (k0 == 'p' and ((kind == 'w' and ch == '9') or (kind == 's' and ch == '0'))): return None
        return SETS[ch]
    w = [L(c, 'w') for c in lk]; s = [L(c, 's') for c in sv]; P = []
    for i in range(d):
        if w[i] != '5': continue
        r = (w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
        if None not in r: P.append((i, r))
    return d, P
def hits(P, lk, sv):
    d = len(lk); word = lambda q: (lk[(q + 1) % d], sv[q], sv[(q - 1) % d], lk[(q - 1) % d])
    for refl in (0, 1):
        for r in range(d):
            ok = True
            for p, m in P:
                q = ((-p if refl else p) + r) % d; mm = m[::-1] if refl else m
                if lk[q] != '5' or any(c not in ms for c, ms in zip(word(q), mm)): ok = False; break
            if ok: return True
    return False
PATS = {}
for nm in list(DV) + list(CV):
    if re.match(r'^[epf]\d+_', nm) and int(nm.split('_')[0][1:]) in DS and (DV.get(nm) == 'D' or CV.get(nm) == 'C'):
        d, P = parse(nm)
        if P: PATS[nm] = (d, P)

if mode == 'buildall':
    # C_kc_ring17: every B-fixed S (any |S| >= 2) with RMIN <= ring <= RMAX; per-row report; untested windows out
    OUT, RMIN, RMAX, FAM = argv[0], int(argv[1]), int(argv[2]), family(argv[3:])
    new = {}; rep = open(OUT + '.rows', 'w')
    for lk, sv, src_ in FAM:
        vs = G['variants'](len(lk), lk, sv)
        hit = [nm for nm, (d, P) in PATS.items() if d == len(lk) and hits(P, lk, sv)]
        cnt = collections.Counter()
        mine = []
        for (r, k, S, w, s, nm) in vs:
            st_ = 'D' if DV.get(nm) == 'D' else ('C' if CV.get(nm) == 'C' else ('notD' if nm in DV else 'untested'))
            cnt[(r, st_)] += 1
            if st_ == 'untested' and RMIN <= r <= RMAX:
                mine.append(nm)
                if nm not in new:
                    line = G['make'](len(lk), r, S, w, s, nm)
                    if line is None or line.startswith('RING'): cnt['notext'] += 1; continue
                    new[nm] = line
        rep.write('%s %s %s %s windows=%d %s untested_r%d-%d=%s\n' % (lk, sv, src_, 'FORBIDDEN:' + hit[0] if hit else 'free', len(vs),
                  ' '.join('r%d:%s=%d' % (r, t, c) for (r, t), c in sorted((k_, v) for k_, v in cnt.items() if isinstance(k_, tuple))), RMIN, RMAX, ','.join(mine)))
    lines = sorted(new.values(), key=lambda x: (int(x.split()[1]), x))
    open(OUT, 'w').write(''.join(l + '\n' for l in lines))
    print('family', len(FAM), 'new', len(lines), sorted(collections.Counter(int(l.split()[1]) for l in lines).items()))
elif mode in ('build', 'build8'):
    OUT, RMAX, FAM = argv[0], int(argv[1]), family(argv[2:])
    st = collections.Counter(); new = {}
    for lk, sv, src_ in FAM:
        if mode == 'build8':
            if '8' not in lk + sv: continue
            lk, sv = lk.replace('8', '9'), sv.replace('8', '9')
        vs = [x for x in G['variants'](len(lk), lk, sv) if x[1] <= 3]
        st['windows'] += len(vs)
        for (r, k, S, w, s, nm) in vs:
            if nm in DV or nm in CV: st['tested'] += 1; continue
            if nm in PEND: st['pending_studio'] += 1; continue
            if nm in new: continue
            line = G['make'](len(lk), r, S, w, s, nm)
            if line is None or line.startswith('RING'): st['notext'] += 1; continue
            new[nm] = line
    lines = sorted(new.values(), key=lambda x: (int(x.split()[1]), x))
    open(OUT, 'w').write(''.join(l + '\n' for l in lines))
    print('family', len(FAM), dict(st), 'new', len(lines), sorted(collections.Counter(int(l.split()[1]) for l in lines).items()))
else:
    FAM = family(argv)
    bysrc = collections.defaultdict(collections.Counter); why = collections.Counter()
    for lk, sv, src_ in FAM:
        hit = [nm for nm, (d, P) in PATS.items() if d == len(lk) and hits(P, lk, sv)]
        key = 'forbidden' if hit else 'free'
        bysrc[src_ if len(lk) == 7 else '%s:d%d' % (src_, len(lk))][key] += 1
        print('%s %s %s %s %s' % (lk, sv, src_ if len(lk) == 7 else '%s:d%d' % (src_, len(lk)), key, ' '.join(sorted(hit, key=len)[:3])))
    for k, v in bysrc.items(): print('#', k, dict(v))
    tot = sum(sum(v.values()) for v in bysrc.values()); fb = sum(v['forbidden'] for v in bysrc.values())
    print('# total %d forbidden %d (%.1f%%); patterns %d' % (tot, fb, 100.0 * fb / max(tot, 1), len(PATS)))
