"""Stage 16 sanity check: binder 7665566/6675666 one ring out. Six privates: p1, p2, p5, p6 (private of the link 6 w_j)
and q1, q2 (w0's two unseen neighbours). Kill a case if a registry item forbids it with every slot it uses known:
 - R6: the 6-wheel link of a link 6 (studio17 verdicts, as in admissibility);
 - a registry wheel pattern (k3x / job28 / addA / feascheck / rpatD, as loaded from args) centred at an exact-degree
   vertex whose arrangement contains the private: w0 (7) and s2 (7). Unknown slots must be unconstrained by the
   pattern instance. usage: python3 s16_census.py root=... args=... rpat=rpatD.txt"""
import sys, os, runpy, io, contextlib, itertools, collections, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ['pcheck.py', 'none'] + sys.argv[1:]
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(HERE, 'pcheck.py'))
lp = G['load_patterns']; g = lp.__globals__
NAME = {}
orig = g['addpat']
def addpat(nm, src):
    d, P = g['pname'](nm); NAME.setdefault((d, P), '%s:%s' % (src, nm)); orig(nm, src)
g['addpat'] = addpat
with contextlib.redirect_stdout(io.StringIO()): lp()
PATS = g['PATS']; LET = g['LET']; LI = g['LI']; isR6 = g['isR6']
# rpat names: re-parse to label RPAT patterns by file line
for fn in [f for f in g['OPT'].get('rpat', '').split(',') if f]:
    for ln, line in enumerate(open(fn), 1):
        f = line.split('#')[0].split(); cm = line.split('#')[1].strip() if '#' in line else ''
        if not f: continue
        d, k = int(f[0]), int(f[1]); slots = {}
        for j in range(k):
            i, m = int(f[2 + 2 * j]), int(f[3 + 2 * j])
            rd = [('w', (i + 1) % d), ('s', i), ('s', (i - 1) % d), ('w', (i - 1) % d)]
            ent = [(('w', i), frozenset((5,)))] + [(rd[t], frozenset(LET[b] for b in range(5) if (m >> (5 * t + b)) & 1)) for t in range(4)]
            for sl, S_ in ent: slots[sl] = slots.get(sl, frozenset(LET)) & S_
        NAME.setdefault((d, tuple(sorted(slots.items()))), 'RPAT:%s line %d # %s' % (os.path.basename(fn), ln, cm))
def placements(d, P):
    for r in range(d):
        for refl in (False, True):
            m = {}
            for (typ, i), S in P:
                j = (i + r) % d if not refl else ((r - i) % d if typ == 'w' else (r - i - 1) % d)
                sl = (typ, j); m[sl] = m.get(sl, frozenset(LET)) & S
            yield r, refl, m
def killers(d, w, s):
    """w, s: letter or None (unknown). return list of (pattern name, rotation, reflection) that surely match"""
    out = []
    for P in PATS.get(d, ()):
        for r, refl, m in placements(d, P):
            ok = True
            for (typ, j), S in m.items():
                v = w[j] if typ == 'w' else s[j]
                if S == frozenset(LET): continue
                if v is None or v not in S: ok = False; break
            if ok: out.append((NAME.get((d, P), '?'), r, refl)); break
    return out
BIN_W = [7, 6, 6, 5, 5, 6, 6]; BIN_S = [6, 6, 7, 5, 6, 6, 6]
w = BIN_W; s = BIN_S
def wheel6(j, p):   # link 6 w_j: (U, w_{j+1}, s_j, p, s_{j-1}, w_{j-1})
    return (7, w[(j + 1) % 7], s[j], p, s[(j - 1) % 7], w[(j - 1) % 7])
def frames(pr):
    p1, p2, p5, p6, q1, q2 = pr
    F = {}
    F['w0'] = ([7, w[1], s[0], q1, q2, s[6], w[6]], [w[2], p1, None, None, None, p6, w[5]])
    F['s2'] = ([p2, w[2], w[3], s[3], None, None, None], [s[1], 7, w[4], None, None, None, None])
    return F
cache = {}; surv = 0; why = collections.Counter(); log = {}
for pr in itertools.product(LET, repeat=6):
    p1, p2, p5, p6, q1, q2 = pr; reasons = []
    for j, p in ((1, p1), (2, p2), (5, p5), (6, p6)):
        if isR6(wheel6(j, p)): reasons.append('R6 at w%d: %s' % (j, ''.join(map(str, wheel6(j, p)))))
    for cen, (fw, fs) in frames(pr).items():
        key = (cen, tuple(fw), tuple(fs))
        if key not in cache: cache[key] = killers(7, fw, fs)
        for nm, r, refl in cache[key][:1]: reasons.append('%s-centred d=7 %s (rot %d refl %s)' % (cen, nm, r, refl))
    if reasons:
        why[reasons[0].split(':')[0] if reasons[0].startswith('R6') else reasons[0].split(' (')[0]] += 1; log[pr] = reasons
    else: surv += 1
print('cases 15625; survivors %d; killed %d' % (surv, 15625 - surv))
allp6 = sum(1 for pr in itertools.product(LET, repeat=6) if pr not in log and min(pr) >= 6)
print('survivors with all privates >= 6: %d ; survivors with some private = 5: %d' % (allp6, sum(1 for pr in itertools.product(LET, repeat=6) if pr not in log and min(pr) == 5)))
for k, v in why.most_common(20): print('  first reason %6d  %s' % (v, k))
for i, nm in enumerate(['p1', 'p2', 'p5', 'p6', 'q1', 'q2']):
    for l in LET:
        tot = 5 ** 5; k = sum(1 for pr in log if pr[i] == l)
        print('  %s=%d killed %d / %d' % (nm, l, k, tot), end=';')
    print()
json.dump({''.join(map(str, k)): v for k, v in log.items()}, open(os.path.join(HERE, 's16_census_kills.json'), 'w'))
