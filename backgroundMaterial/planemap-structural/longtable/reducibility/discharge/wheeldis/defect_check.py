"""Receiver-centred check of defect candidates (README §7, test G; exploratory).
For each defect line written by defect.py (sig = ring degree words), rebuild the disc and, at every vertex of degree 7,
enumerate every sender set S (|S| >= 2) of its degree-5 neighbours: the configuration u + S + links of S (gen.py type,
big link vertices free = B).  Look each one up:
  dfast registry  = every out/*.out line named e<d>_/p<d>_ (gen.py's TESTED) + out/def_*.out (this section);
  cfast registry  = job27/*.cfast + out/def_*.cfast ('C-REDUCIBLE' = C-candidate, counted reducible).
A defect SURVIVES iff every such configuration (any ring) is tested not D and has a cfast run with no C-candidate,
and every 7-wheel is tested not D.  Untested configurations are written as dfast input (ring <= 19 only).
Usage: python3 defect_check.py DEFECTS.txt NEWCFG.txt [RMAXTEST=19]"""
import sys, os, glob, re, collections, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
ARGS = sys.argv[1:]
DEFF, NEWF = ARGS[0], ARGS[1]; RT = int(ARGS[2]) if len(ARGS) > 2 else 19
# gen.py helpers (canon_key, key_of_name, ringf, build, extract, TESTED) without its main part
gsrc = open(os.path.join(HERE, 'gen.py')).read()
gsrc = gsrc[:gsrc.index('arrs = []')].replace('os.path.dirname(os.path.abspath(__file__))', repr(HERE))
sys.argv = ['gen.py', '/dev/null', str(RT)]; exec(gsrc)
_g = open(os.path.join(HERE, 'gen.py')).read(); exec(_g[_g.index('def make('):_g.index('for d, lk, sv in arrs')])
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.out')):
    for line in open(fn):
        f = line.split()
        if f and re.match(r'^[ep]\d+_', f[0]) and ('D=true' in line or 'D=false' in line):
            TESTED[key_of_name(f[0])] = 'D' if 'D=true' in line else 'notD'
CRES = {}
for fn in glob.glob(os.path.join(HERE, 'job27', '*.cfast')) + glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):
    cur = None
    for l in open(fn):
        if ' r=' in l and not l.startswith(' '):
            cur = key_of_name(l.split()[0]); CRES.setdefault(cur, 'neither')
            if 'D=true' in l: CRES[cur] = 'D'
        elif 'C-REDUCIBLE' in l and cur is not None: CRES[cur] = 'C'
# defect.py's Disc
dsrc = open(os.path.join(HERE, 'defect.py')).read()
exec(dsrc[dsrc.index('class Disc'):dsrc.index('def word')])
def canon(w):
    w = tuple(w); return min(min(s[k:] + s[:k] for k in range(len(s))) for s in (w, w[::-1]))
T7 = {}
for fn in ('bigwheels_dfast.out', 'bigwheels1516_dfast_partial.out'):
    for line in open(os.path.join(HERE, 'out', fn)):
        f = line.split()
        if f and f[0].startswith('c7_'): T7[tuple(map(int, f[0][3:]))] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.out')):
    for line in open(fn):
        f = line.split()
        if f and f[0].startswith('c7_'): T7[tuple(map(int, f[0][3:]))] = 'D' if 'D=true' in line else 'notD'

def rebuild(sig, extra=4):
    rings = sig.split('|'); d0 = int(rings[0]); D = Disc(d0)
    for k in range(1, len(rings)):
        R = D.rings[k]; assert len(R) == len(rings[k]), (k, len(R), rings[k])
        for v, ch in zip(R, rings[k]): D.deg[v] = int(ch)
        assert D.grow()
    for _ in range(extra):
        for v in D.rings[-1]: D.deg[v] = 6
        assert D.grow()
    for v in D.rings[-1]: D.deg[v] = 6
    D.index(); return D

def arrangement(D, v):
    lk = D.link(v); d = len(lk); L_ = ''.join(str(D.deg[x]) for x in lk); S_ = ''
    for i in range(d):
        x, y = lk[i], lk[(i + 1) % d]
        com = [z for z in set(D.link(x)) & set(D.link(y)) if z != v]
        assert len(com) == 1; S_ += str(D.deg[com[0]])
    return d, L_, S_

def subsets_all(d, lk, sv):
    snd = [i for i in range(d) if lk[i] == '5']; res_ = []
    for k in range(2, len(snd) + 1):
        for S in itertools.combinations(snd, k):
            wl = {(i + e) % d for i in S for e in (-1, 0, 1)}; sl = {(i + e) % d for i in S for e in (-1, 0)}
            w = [int(lk[j]) if j in wl and lk[j] in '56' else None for j in range(d)]
            s = [int(sv[j]) if j in sl and sv[j] in '56' else None for j in range(d)]
            r = ringf(d, w, s)
            L_ = ''.join(('B' if lk[j] in '789' else lk[j]) if j in wl else '.' for j in range(d))
            S_ = ''.join(('B' if sv[j] in '789' else sv[j]) if j in sl else '.' for j in range(d))
            res_.append((r, k, S, w, s, canon_key(d, L_, S_)))
    return res_

if __name__ == '__main__':
    lines = [l for l in open(DEFF) if l.startswith('c=')]
    need = {}; summary = collections.Counter(); out = []
    for line in lines:
        m = re.search(r'c=(\d+) sig=(\S+)', line); c, sig = int(m.group(1)), m.group(2)
        D = rebuild(sig)
        st = collections.Counter(); w7 = []
        for v, dv in D.deg.items():
            if dv != 7 or D.ring_of[v] >= len(D.rings) - 2: continue
            cw = canon([D.deg[x] for x in D.link(v)])
            w7.append(T7.get(cw, 'untested'))
            if T7.get(cw) is None: need.setdefault(('c7', cw), None)
            d, lk, sv = arrangement(D, v)
            for r, k, S, w, s, key in subsets_all(d, lk, sv):
                dv_ = TESTED.get(key); cv = CRES.get(key)
                if dv_ == 'D': st['D'] += 1
                elif dv_ is None: st['untestedD' if r <= RT else 'ring>%d' % RT] += 1; need.setdefault(key, (d, r, S, w, s, key))
                elif cv == 'C': st['C'] += 1
                elif cv is None: st['notD_untestedC'] += 1; need.setdefault(('C',) + key, (d, r, S, w, s, key))
                else: st['neither'] += 1
        verdict = 'killed' if st['D'] or st['C'] or 'D' in w7 or any(k.startswith('ring>') for k in st) else (
            'SURVIVES' if not st['untestedD'] and not st['notD_untestedC'] and 'untested' not in w7 else 'open')
        summary[verdict] += 1
        out.append('%s c=%d sig=%s 7wheels=%s %s' % (verdict, c, sig, ','.join(w7), dict(st)))
    print('\n'.join(out)); print('summary', dict(summary))
    lines_ = []
    for k, v in need.items():
        if v is None or k[0] == 'C': continue
        d, r, S, w, s, key = v
        if r > RT: continue
        ln = make(d, r, S, w, s, key)
        if ln: lines_.append(ln)
    open(NEWF, 'w').write('\n'.join(sorted(lines_, key=lambda x: int(x.split()[1]))) + ('\n' if lines_ else ''))
    cneed = [v for k, v in need.items() if v is not None and k[0] == 'C']
    open(NEWF + '.cneed', 'w').write('\n'.join(l for l in (make(*v) for v in cneed) if l) + '\n')
    w7need = ['c7_' + ''.join(map(str, k[1])) for k in need if k[0] == 'c7']
    open(NEWF + '.w7need', 'w').write('\n'.join(w7need) + '\n')
    print('to test: dfast', len(lines_), 'cfast', len(cneed), '7-wheels', len(w7need))
