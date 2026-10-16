"""EXPLORE round 14 (exploratory): small B-fixed windows over the d = 7 tight family (H-W2).
A small window is gen28's B-fixed configuration with |S| = 2 or 3: u at exact degree 7, S a set of link fives, every
neighbour of S at its exact letter (9 -> B, a free ring vertex).  Its f7_ name has '.' outside, so one D verdict
forbids every d = 7 arrangement that contains it (wlp3 matches f-patterns on the rooted words of S).
  build OUT RMAX FAMILY...  write the untested |S| <= 3 windows with ring <= RMAX (dfast lines) to OUT
  build8 OUT RMAX FAMILY... round 15: the same windows with every 8 made free (B = 7/8/9), rows with an 8 only
  cover FAMILY...           per arrangement: forbidden by a registry D/C pattern (any f/e/p name, any S), or not
Family files: any lines with 'd=7 link L s S'.  Registry: every *.out / *.cfast under out/, job27/, loop/ (oracle
files are .pat, never read), plus loop/lone/u*.pat (receiver-free D windows, as in Job 28's pattern list)."""
import sys, os, glob, re, itertools, collections
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
mode, argv = sys.argv[1], sys.argv[2:]
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
RM = argv[1] if mode in ('build', 'build8') else '14'
sys.argv = ['gen28.py', '/dev/null', RM, 'small']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)

def family(files):
    seen, out = set(), []
    for fn in files:
        for line in open(fn):
            m = re.search(r'd=7 link (\d{7}) s (\d{7})', line)
            if not m: continue
            k = canon(m.group(1), m.group(2))
            if k not in seen: seen.add(k); out.append((m.group(1), m.group(2), os.path.basename(fn)))
    return out
def images(lk, sv):
    d = len(lk)
    for r in range(d):
        a, b = lk[r:] + lk[:r], sv[r:] + sv[:r]; yield a, b
        yield ''.join(a[-i % d] for i in range(d)), ''.join(b[(-i - 1) % d] for i in range(d))
def canon(lk, sv): return min(images(lk, sv))

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
    if nm[0] in 'epf' and re.match(r'^[epf]7_', nm) and (DV.get(nm) == 'D' or CV.get(nm) == 'C'):
        d, P = parse(nm)
        if P: PATS[nm] = P

if mode in ('build', 'build8'):
    OUT, RMAX, FAM = argv[0], int(argv[1]), family(argv[2:])
    st = collections.Counter(); new = {}
    for lk, sv, src_ in FAM:
        if mode == 'build8':
            if '8' not in lk + sv: continue
            lk, sv = lk.replace('8', '9'), sv.replace('8', '9')
        vs = [x for x in G['variants'](7, lk, sv) if x[1] <= 3]
        st['windows'] += len(vs)
        for (r, k, S, w, s, nm) in vs:
            if nm in DV or nm in CV: st['tested'] += 1; continue
            if nm in PEND: st['pending_studio'] += 1; continue
            if nm in new: continue
            line = G['make'](7, r, S, w, s, nm)
            if line is None or line.startswith('RING'): st['notext'] += 1; continue
            new[nm] = line
    lines = sorted(new.values(), key=lambda x: (int(x.split()[1]), x))
    open(OUT, 'w').write(''.join(l + '\n' for l in lines))
    print('family', len(FAM), dict(st), 'new', len(lines), sorted(collections.Counter(int(l.split()[1]) for l in lines).items()))
else:
    FAM = family(argv)
    bysrc = collections.defaultdict(collections.Counter); why = collections.Counter()
    for lk, sv, src_ in FAM:
        hit = [nm for nm, P in PATS.items() if hits(P, lk, sv)]
        small = [nm for nm in hit if sum(c != '.' for c in nm.split('_')[1]) and len(parse(nm)[1]) <= 3]
        key = 'forbidden' if hit else 'free'
        bysrc[src_][key] += 1
        print('%s %s %s %s %s' % (lk, sv, src_, key, ' '.join(sorted(hit, key=len)[:3])))
    for k, v in bysrc.items(): print('#', k, dict(v))
    tot = sum(sum(v.values()) for v in bysrc.values()); fb = sum(v['forbidden'] for v in bysrc.values())
    print('# total %d forbidden %d (%.1f%%); patterns %d' % (tot, fb, 100.0 * fb / max(tot, 1), len(PATS)))
