"""Graph-based receiver-centred check of defect candidates (README §7, test G; exploratory).  Replaces defect_check.py,
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
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(DIS, 'b8b'))
from rings import Layered
ARGS = sys.argv[1:]
BF = 'bf' in ARGS; S7 = 'strict7' in ARGS; ARGS = [a for a in ARGS if a not in ('bf', 'strict7')]
CAND, NEWF = ARGS[0], ARGS[1]; LIMIT = int(ARGS[2]) if len(ARGS) > 2 else 10 ** 9
gsrc = open(os.path.join(HERE, 'gen.py')).read()
gsrc = gsrc[:gsrc.index('arrs = []')].replace('os.path.dirname(os.path.abspath(__file__))', repr(HERE))
sys.argv = ['gen.py', '/dev/null', '30']; exec(gsrc)
DRES = {}; CRES = {}
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.out')):
    for line in open(fn):
        f = line.split()
        if not f or ('D=true' not in line and 'D=false' not in line): continue
        v = 'D' if 'D=true' in line else 'notD'
        if re.match(r'^[ep]\d+_', f[0]): TESTED[key_of_name(f[0])] = v
        else: DRES[f[0]] = v
for fn in glob.glob(os.path.join(HERE, 'job27', '*.cfast')) + glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):
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
for fn in glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '):
            m = re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = canon(tuple(map(int, m.group(1)))) if m else None
        elif 'C-REDUCIBLE' in line and cur is not None: C7.add(cur)
        elif 'search |X|' in line and cur is not None: NC7.add(cur)
NC7 -= C7
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
        if u in outer or deg.get(u) != 7: continue
        lk = rotf(nxt, u); d = len(lk)
        cw = canon([deg[x] for x in lk]); w7 = T7.get(cw)
        if w7 == 'D': st['D'] += 1
        elif w7 is None: st['untested7'] += 1; need.append(('w7', cw))
        elif STRICT7 and cw in C7: st['C7'] += 1
        elif STRICT7 and cw not in NC7: st['untested7C'] += 1; need.append(('w7c', cw))
        L_ = ''.join(str(deg[x]) for x in lk); S_ = ''
        for i in range(d):
            com = [z for z in adj[lk[i]] & adj[lk[(i + 1) % d]] if z != u]; assert len(com) == 1; S_ += str(deg[com[0]])
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
                    if cfg is None: st['nosimple'] += 1; continue
                    key = 'g' + hashlib.sha1(cfg.encode()).hexdigest()[:16]; nm = key; r = int(cfg.split()[0])
                if BF:
                    Ib = {u} | {lk[i] for i in S}
                    for i in S: Ib |= adj[lk[i]]
                    cb = extract_cfg(adj, deg, Ib)
                    if cb is None:                     # pinched in G: move enclosed ring vertices inside, as above
                        RSb = set(y for x in Ib for y in adj[x]) - Ib
                        Ib2 = Ib | {y for y in RSb if adj[y] <= (Ib | RSb)}
                        cb = extract_cfg(adj, deg, Ib2) if Ib2 != Ib else None
                    if cb is None: st['bf_nosimple'] += 1
                    else:
                        kb = 'b' + hashlib.sha1(cb.encode()).hexdigest()[:16]; db = DRES.get(kb); cbv = CRES.get(kb)
                        if db == 'D': st['bfD'] += 1
                        elif db is None: st['bf_untestedD'] += 1; need.append(('d', kb, cb, int(cb.split()[0])))
                        elif cbv == 'C': st['bfC'] += 1
                        elif cbv is None: st['bf_untestedC'] += 1; need.append(('c', kb, cb, int(cb.split()[0])))
                        else: st['bf_neither'] += 1
                dv = TESTED.get(key) if not isinstance(key, str) else DRES.get(key)
                cv = CRES.get(key)
                if dv == 'D': st['D'] += 1
                elif dv is None: st['untestedD'] += 1; need.append(('d', nm, cfg, r))
                elif cv == 'C': st['C'] += 1
                elif cv is None: st['untestedC'] += 1; need.append(('c', nm, cfg, r))
                else: st['neither'] += 1
    # an unrepaired non-simple ring is open, not killed (loop/appears/FINDINGS.md Q1; never fired on the 418,551 K <= 4
    # candidates, EXPLORE-LOG round 6)
    if st['D'] or st['C'] or st['C7'] or st['bfD'] or st['bfC']: v = 'killed'
    elif st['untestedD'] or st['untestedC'] or st['untested7'] or st['untested7C'] or st['bf_untestedD'] or st['bf_untestedC'] or st['nosimple'] or st['bf_nosimple']: v = 'open'
    else: v = 'SURVIVES'
    return v, st, need

if __name__ == '__main__':
    summ = collections.Counter(); needD = {}; needC = {}; need7 = set(); out = []
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
                else: need7.add(x[1])
        out.append('%s c=%s sig=%s %s' % (v, m.group(1), m.group(2), dict(st)))
    open(NEWF + '.status', 'w').write('\n'.join(out) + '\n')
    for x in out:
        if not x.startswith('killed'): print(x)
    print('summary', dict(summ))
    open(NEWF + '.d', 'w').write(''.join('%s %s\n' % (x[1], x[2]) for x in sorted(needD.values(), key=lambda x: x[3])))
    open(NEWF + '.c', 'w').write(''.join('%s %s\n' % (x[1], x[2]) for x in sorted(needC.values(), key=lambda x: x[3])))
    open(NEWF + '.w7', 'w').write(''.join('c7_%s\n' % ''.join(map(str, w)) for w in sorted(need7)))
    print('to test (from candidates not yet killed): dfast %d, cfast %d, 7-wheels %d' % (len(needD), len(needC), len(need7)))
