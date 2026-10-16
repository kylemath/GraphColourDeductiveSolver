"""[G9 probe-2 copy (mk_check9.py): receivers of degree >= 7, f-name lookup for B-fixed]
[G9 copy, see loop/g9/mk_check8.py: receivers of degree 7 and 8, 8-wheels, loop/g9 verdicts]
Graph-based receiver-centred check of defect candidates (README §7, test G; exploratory).  Replaces defect_check.py,
which looked every sender set up by its abstract key and so missed sender sets whose free big vertices B are the SAME
vertex in the patch (two senders sharing one 7): there the ring of u + S + links is pinched in G, and the configuration
that actually appears is the one with that B inside at its exact degree.
For each candidate (ring signature) the patch is built with b8b/rings.py; at every 7 u and every set S (|S| >= 2) of its
degree-5 neighbours, I = u + S + the degree-5/6 neighbours of S:
  - ring of I simple and induced in G: the configuration is the gen.py/pairs2 one; look its key up (dfast registry:
    out/*.out; cfast registry: job27/*.cfast, out/def_*.cfast);
  - otherwise: move every ring vertex whose neighbourhood lies in I + ring inside (exact degree) and use that
    configuration (written for dfast/cfast; verdicts read back by name from out/def_*.out / out/def_*.cfast; names are
    'g<hash>' of the dfast line).
Status per candidate: killed (some configuration D or C, or a 7-wheel D), SURVIVES (all tested, none D or C), open.
Option bf: also every 'B fixed' configuration u + S + all link vertices of S at exact degree (|S| >= 2), named
'b<hash>' (R_opt+ of README §7.3).
Usage: python3 defect_check2.py CANDIDATES.txt NEWCFG.txt [limit] [bf]"""
import sys, os, glob, re, collections, itertools, hashlib
HERE = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'; DIS = os.path.dirname(HERE); G9 = os.path.join(HERE, 'loop', 'g9')
sys.path.insert(0, os.path.join(DIS, 'b8b'))
from rings import Layered
ARGS = sys.argv[1:]
BF = 'bf' in ARGS; S7 = 'strict7' in ARGS; ARGS = [a for a in ARGS if a not in ('bf', 'strict7')]
CAND, NEWF = ARGS[0], ARGS[1]; LIMIT = int(ARGS[2]) if len(ARGS) > 2 else 10 ** 9
gsrc = open(os.path.join(HERE, 'gen.py')).read()
gsrc = gsrc[:gsrc.index('arrs = []')].replace('os.path.dirname(os.path.abspath(__file__))', repr(HERE))
sys.argv = ['gen.py', '/dev/null', '30']; exec(gsrc)
DRES = {}; CRES = {}
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.out')) + glob.glob(os.path.join(G9, 'g9_*.dfast.out')):
    for line in open(fn):
        f = line.split()
        if not f or ('D=true' not in line and 'D=false' not in line): continue
        v = 'D' if 'D=true' in line else 'notD'
        if re.match(r'^[ep]\d+_', f[0]): TESTED[key_of_name(f[0])] = v
        else: DRES[f[0]] = v
for fn in glob.glob(os.path.join(HERE, 'job27', '*.cfast')) + glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')) + glob.glob(os.path.join(G9, 'g9_*.cfast')):
    cur = None
    for l in open(fn):
        if ' r=' in l and not l.startswith(' '):
            nm = l.split()[0]; cur = key_of_name(nm) if re.match(r'^[ep]\d+_', nm) else nm
            if 'D=true' in l: CRES.setdefault(cur, 'neither')
        elif 'C-REDUCIBLE' in l and cur is not None: CRES[cur] = 'C'
        elif 'search |X|' in l and cur is not None: CRES.setdefault(cur, 'neither')   # tested only once its search ended
def canon(w):
    w = tuple(w); return min(min(s[k:] + s[:k] for k in range(len(s))) for s in (w, w[::-1]))
T7 = {}
for fn in ('bigwheels_dfast.out', 'bigwheels1516_dfast_partial.out') + tuple(os.path.basename(x) for x in glob.glob(os.path.join(HERE, 'out', 'def_*.out'))):
    for line in open(os.path.join(HERE, 'out', fn)):
        f = line.split()
        if f and f[0].startswith('c7_'): T7[tuple(map(int, f[0][3:]))] = 'D' if 'D=true' in line else 'notD'

# 7-wheel C status (README §7.3, R_opt+): C-candidates count as reducible; with 'strict7' a 7-wheel must also be
# C-tested (on demand, named c7_<canonical word>)
STRICT7 = S7 or BF
C7 = set(); NC7 = set()
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')) + glob.glob(os.path.join(G9, 'g9_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '):
            m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = canon(tuple(map(int, m.group(1)))) if m else None
        elif 'C-REDUCIBLE' in line and cur is not None: C7.add(cur)
        elif 'search |X|' in line and cur is not None: NC7.add(cur)
NC7 -= C7
for fn in glob.glob(os.path.join(G9, 'g9_*.dfast.out')):
    for line in open(fn):
        f = line.split()
        if f and re.match(r'^[ep]\d+_', f[0]) and ('D=true' in line or 'D=false' in line):
            TESTED[key_of_name(f[0])] = 'D' if 'D=true' in line else 'notD'
T8 = {}
DVF, CVF = {}, {}
for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.out')) + glob.glob(os.path.join(HERE, 'loop', 'lp', '*.out')) + glob.glob(os.path.join(G9, 'g9_*.dfast.out')):
    for line in open(fn):
        f = line.split()
        if not f or ('D=true' not in line and 'D=false' not in line): continue
        if re.match(r'^f\d+_', f[0]): DVF[f[0]] = 'D' if 'D=true' in line else 'notD'
        elif re.match(r'^[ep]\d+_', f[0]) and 'loop' in fn: TESTED[key_of_name(f[0])] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(HERE, 'out', 'job28', '*.cfast')) + glob.glob(os.path.join(HERE, 'loop', 'lp', '*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
        elif 'C-REDUCIBLE' in line and cur: CVF[cur] = 'C'
        elif 'search |X|' in line and cur: CVF.setdefault(cur, 'neither')
for fn in ['bigwheels_dfast.out', 'bigwheels1516_dfast_partial.out']:
    for line in open(os.path.join(HERE, 'out', fn)):
        f = line.split()
        if f and f[0].startswith('c8_') and ('D=true' in line or 'D=false' in line): T8[tuple(map(int, f[0][3:]))] = 'D' if 'D=true' in line else 'notD'
for fn in glob.glob(os.path.join(G9, 'g9_*.dfast.out')):
    for line in open(fn):
        f = line.split()
        if f and f[0][:3] in ('c7_', 'c8_') and ('D=true' in line or 'D=false' in line):
            (T7 if f[0][:3] == 'c7_' else T8)[tuple(map(int, f[0][3:]))] = 'D' if 'D=true' in line else 'notD'
# wheels with a letter 8 that the search counted not reducible: tested sets
R5W = {}; 
for line in open(os.path.join(DIS, 'studio17', 'wheels17_verdicts.txt')):
    if line.startswith('#'): continue
    f = line.split(); R5W[tuple(map(int, f[0].split('_')[1]))] = f[2]
_bw = open(os.path.join(HERE, 'bigwheels.py')).read(); exec(_bw[_bw.index('def wheel('):_bw.index('fmt = lambda')])
def patch(sig, sea=5):
    rings = sig.split('|'); L = Layered(int(rings[0]))
    for k in range(1, len(rings)): L.add_ring([int(c) for c in rings[k]])
    for _ in range(sea): L.add_ring([6] * len(L.ring()))
    adj = collections.defaultdict(set); nxt = collections.defaultdict(dict)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
        nxt[a][b] = c; nxt[b][c] = a; nxt[c][a] = b
    return L, adj, nxt
def rotf(nxt, x):
    s0 = min(nxt[x]); r = [s0]; y = nxt[x][s0]
    while y != s0: r.append(y); y = nxt[x][y]
    return r
def extract_cfg(adj, deg, I):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nx = nb[0] if nb[0] != prev else nb[1]
        if nx == start: break
        order.append(nx); prev = cur
    if len(order) != len(RS): return None
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return '%d %d %s %s' % (len(order), len(Il), f(ra), f(ia))

def check(sig):
    L, adj, nxt = patch(sig); deg = L.deg; outer = set(L.ring())
    st = collections.Counter(); need = []
    for u in list(adj):
        if u in outer: continue
        lkw_ = [deg.get(x) for x in rotf(nxt, u)]
        if deg.get(u) in (5, 6) and None not in lkw_ and 8 in lkw_:
            cw = canon(lkw_)
            if deg[u] == 6 or cw not in R5W: st['unt8_%d_%s' % (deg[u], ''.join(map(str, cw)))] += 1
        if deg.get(u) is None or deg[u] < 7: continue
        lk = rotf(nxt, u); d = len(lk)
        cw = canon([deg[x] for x in lk]); w7 = (T7 if d == 7 else T8 if d == 8 else {}).get(cw)
        if d == 8 or 8 in cw:
            if w7 is None: st['unt8_%d_%s' % (d, ''.join(map(str, cw)))] += 1
        if d >= 9: st['bigcentre_wheel_untested'] += 1
        elif w7 == 'D': st['D'] += 1; st['W%dD' % d] += 1
        elif w7 is None and d == 8: st['untested8'] += 1; need.append(('w8', cw))
        elif w7 is None: st['untested7'] += 1; need.append(('w7', cw))
        elif d == 8: pass
        elif STRICT7 and cw in C7: st['C7'] += 1; st['W7C'] += 1
        elif STRICT7 and cw not in NC7: st['untested7C'] += 1; need.append(('w7c', cw))
        L_ = ''.join(str(min(deg[x], 9)) for x in lk); S_ = ''
        for i in range(d):
            com = [z for z in adj[lk[i]] & adj[lk[(i + 1) % d]] if z != u]; assert len(com) == 1; S_ += str(min(deg[com[0]], 9))
        snd = [i for i in range(d) if L_[i] == '5']
        for k in range(2, len(snd) + 1):
            for S in itertools.combinations(snd, k):
                I = {u} | {lk[i] for i in S}
                for i in S: I |= {y for y in adj[lk[i]] if deg[y] <= 6}
                cfg = extract_cfg(adj, deg, I)
                if cfg is not None:
                    wl = {(i + e) % d for i in S for e in (-1, 0, 1)}; sl = {(i + e) % d for i in S for e in (-1, 0)}
                    Lk = ''.join(('B' if L_[j] in '789' else L_[j]) if j in wl else '.' for j in range(d))
                    Sk = ''.join(('B' if S_[j] in '789' else S_[j]) if j in sl else '.' for j in range(d))
                    key = canon_key(d, Lk, Sk); r = int(cfg.split()[0])
                    nm = 'e%d_%s_%s_%s' % (d, key[1], key[2], ''.join('1' if ch != '.' else '0' for ch in key[1]))
                else:
                    RS = set(y for x in I for y in adj[x]) - I
                    I2 = I | {y for y in RS if adj[y] <= (I | RS)}
                    cfg = extract_cfg(adj, deg, I2) if I2 != I else None
                    if cfg is None: st['nosimple'] += 1; st['nosimple@%d' % d] += 1; continue
                    key = 'g' + hashlib.sha1(cfg.encode()).hexdigest()[:16]; nm = key; r = int(cfg.split()[0])
                if BF:
                    Ib = {u} | {lk[i] for i in S}
                    for i in S: Ib |= adj[lk[i]]
                    cb = extract_cfg(adj, deg, Ib); fnm = None
                    if cb is not None:
                        wl_ = {(i + e) % d for i in S for e in (-1, 0, 1)}; sl_ = {(i + e) % d for i in S for e in (-1, 0)}
                        if all(L_[j] != '9' for j in wl_) and all(S_[j] != '9' for j in sl_):
                            kf = canon_key(d, ''.join(L_[j] if j in wl_ else '.' for j in range(d)), ''.join(S_[j] if j in sl_ else '.' for j in range(d)))
                            fnm = 'f%d_%s_%s' % (d, kf[1], kf[2])
                    if cb is None:                     # pinched in G: move enclosed ring vertices inside, as above
                        RSb = set(y for x in Ib for y in adj[x]) - Ib
                        Ib2 = Ib | {y for y in RSb if adj[y] <= (Ib | RSb)}
                        cb = extract_cfg(adj, deg, Ib2) if Ib2 != Ib else None
                    if cb is None: st['bf_nosimple'] += 1; st['bf_nosimple@%d' % d] += 1
                    else:
                        kb = 'b' + hashlib.sha1(cb.encode()).hexdigest()[:16]; db = DRES.get(kb); cbv = CRES.get(kb)
                        if fnm and DVF.get(fnm) == 'D': db = 'D'
                        elif fnm and db is None and fnm in DVF: db = DVF[fnm]
                        if fnm and CVF.get(fnm) == 'C': cbv = 'C'
                        elif fnm and cbv is None and fnm in CVF: cbv = CVF[fnm]
                        if db == 'D': st['bfD'] += 1; st['bfD@%d' % d] += 1
                        elif db is None: st['bf_untestedD'] += 1; need.append(('d', kb, cb, int(cb.split()[0])))
                        elif cbv == 'C': st['bfC'] += 1; st['bfC@%d' % d] += 1
                        elif cbv is None: st['bf_untestedC'] += 1; need.append(('c', kb, cb, int(cb.split()[0])))
                        else: st['bf_neither'] += 1
                dv = TESTED.get(key) if not isinstance(key, str) else DRES.get(key)
                cv = CRES.get(key)
                if dv == 'D': st['D'] += 1; st['rcD@%d' % d] += 1
                elif dv is None: st['untestedD'] += 1; need.append(('d', nm, cfg, r))
                elif cv == 'C': st['C'] += 1; st['rcC@%d' % d] += 1
                elif cv is None: st['untestedC'] += 1; need.append(('c', nm, cfg, r))
                else: st['neither'] += 1
    if st['D'] or st['C'] or st['C7'] or st['nosimple'] or st['bfD'] or st['bfC'] or st['bf_nosimple']: v = 'killed'
    elif st['untestedD'] or st['untestedC'] or st['untested7'] or st['untested8'] or st['untested7C'] or st['bf_untestedD'] or st['bf_untestedC']: v = 'open'
    else: v = 'SURVIVES'
    return v, st, need

if __name__ == '__main__':
    summ = collections.Counter(); needD = {}; needC = {}; need7 = set(); need8 = set(); out = []
    for n, line in enumerate(open(CAND)):
        if n >= LIMIT: break
        m = re.search(r'c=(-?\d+) sig=(\S+)', line)
        if not m: continue
        v, st, need = check(m.group(2)); summ[v] += 1
        if v != 'killed':
            for x in need:
                if x[0] == 'd': needD[x[1]] = x
                elif x[0] == 'c': needC[x[1]] = x
                elif x[0] == 'w7c':
                    r_, m_, ra_, ia_ = wheel(list(x[1])); f_ = lambda L: ';'.join(','.join(map(str, v)) if v else '-' for v in L)
                    nm_ = 'c7_' + ''.join(map(str, x[1])); needC[nm_] = ('c', nm_, '%d %d %s %s' % (r_, m_, f_(ra_), f_(ia_)), r_)
                elif x[0] == 'w8': need8.add(x[1])
                else: need7.add(x[1])
        out.append('%s c=%s sig=%s %s' % (v, m.group(1), m.group(2), dict(st)))
    open(NEWF + '.status', 'w').write('\n'.join(out) + '\n')
    for x in out:
        if not x.startswith('killed'): print(x)
    print('summary', dict(summ))
    open(NEWF + '.d', 'w').write(''.join('%s %s\n' % (x[1], x[2]) for x in sorted(needD.values(), key=lambda x: x[3])))
    open(NEWF + '.c', 'w').write(''.join('%s %s\n' % (x[1], x[2]) for x in sorted(needC.values(), key=lambda x: x[3])))
    open(NEWF + '.w7', 'w').write(''.join('c7_%s\n' % ''.join(map(str, w)) for w in sorted(need7)))
    fmt_ = lambda L: ';'.join(','.join(map(str, v)) if v else '-' for v in L)
    with open(NEWF + '.w78', 'w') as fo:
        for nm_, ws in (('c7_', need7), ('c8_', need8)):
            for w_ in sorted(ws):
                r_, m_, ra_, ia_ = wheel(list(w_)); fo.write('%s%s %d %d %s %s\n' % (nm_, ''.join(map(str, w_)), r_, m_, fmt_(ra_), fmt_(ia_)))
    print('to test (from candidates not yet killed): dfast %d, cfast %d, 7-wheels %d, 8-wheels %d' % (len(needD), len(needC), len(need7), len(need8)))
