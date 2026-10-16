"""Isolated positive defects (README §7, test G; exploratory).
A defect = a disc built ring by ring around a centre (b8b/rings.py conventions): rings 0..K-1 carry degrees in
{5, 6, 7}, ring K and every later ring is all 6 (the sea).  Charge c = sum over rings < K of (6 - deg).
DFS over ring degrees; a vertex is checked as soon as its link is complete:
  5: not isR5 (Job 17 D/C 5-wheels incl. the certified C, D fans incl. diamond);
  6: not isR6 (Job 17 D/C 6-wheels, 2.122) and not one of the six 565xxx C-candidates (R_opt counts them);
  7: not a D 7-wheel (bigwheels*_dfast.out); untested 7-wheels are flagged for testing at the leaf.
Leaves (c >= CMIN) are written with every 7's arrangement (link word, s word) for the receiver-centred check
(defect_check.py).
Usage: python3 defect.py CENTRE K CMIN OUT [maxleaves]"""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
src = open(os.path.join(HERE, 'wlp.py')).read().replace('__file__', repr(os.path.join(HERE, 'wlp.py')))
sys.argv = ['wlp']; exec(src[:src.index('# sender rows')]); sys.argv = [sys.argv[0]] + ARGS
UNC6 = {tuple(map(int, w)) for w in UNCERT}
def bad6(w):
    return isR6(w) or canon(w) in UNC6
D7 = set(); T7 = set()
for fn in ('bigwheels_dfast.out', 'bigwheels1516_dfast_partial.out'):
    for line in open(os.path.join(HERE, 'out', fn)):
        f = line.split()
        if not f or not f[0].startswith('c7_'): continue
        w = tuple(map(int, f[0][3:])); T7.add(w)
        if 'D=true' in line: D7.add(w)
# README §7.3 (R_opt+): 7-wheels that cfast flags as C-candidates also count as reducible; ring-16 7-wheels from
# out/def_w7_r16.out count as tested.
import glob as _glob, re as _re
C7 = set(); NC7 = set()
for fn in _glob.glob(os.path.join(HERE, 'out', 'def_*.cfast')):
    cur = None
    for line in open(fn):
        if ' r=' in line and not line.startswith(' '):
            m = _re.match(r'^(?:c7_|\S*_w7_\d+_)(\d{7}) ', line); cur = canon(tuple(map(int, m.group(1)))) if m else None
            if cur is not None: NC7.add(cur)
        elif 'C-REDUCIBLE' in line and cur is not None: C7.add(cur)
NC7 -= C7
_p = os.path.join(HERE, 'out', 'def_w7_r16.out')
if os.path.exists(_p):
    for line in open(_p):
        f = line.split()
        if f and f[0].startswith('c7_') and ('D=true' in line or 'D=false' in line):
            w = tuple(map(int, f[0][3:])); T7.add(w)
            if 'D=true' in line: D7.add(w)
if 'strict7' in ARGS: D7 |= C7
def bad(deg, w):
    if deg == 5: return isR5(w)
    if deg == 6: return bad6(w)
    if deg == 7: return canon(w) in D7
    return True

CENTRE, K, CMIN, OUT = int(ARGS[0]), int(ARGS[1]), int(ARGS[2]), ARGS[3]
MAXLEAVES = int(ARGS[4]) if len(ARGS) > 4 else 10 ** 9
DEGS = (5, 6, 7)


class Disc:
    """rings[k] = list of vertex ids; inb[v] = in-block (previous ring, cyclic order); outb[v] = out-block."""
    def __init__(self, d0):
        self.deg = {0: d0}; self.rings = [[0]]; self.inb = {0: []}; self.outb = {}; self.n = 1
        z = list(range(1, d0 + 1)); self.n += d0
        for v in z: self.inb[v] = [0]
        self.outb[0] = z; self.rings.append(z)

    def grow(self):
        """create the next ring from the degrees of the current outer ring; returns False if impossible."""
        R = self.rings[-1]; a = len(R)
        out = [self.deg[R[j]] - len(self.inb[R[j]]) - 2 for j in range(a)]
        if min(out) < 1: return False
        b = sum(o - 1 for o in out)
        if b < 3: return False
        Z = list(range(self.n, self.n + b)); self.n += b
        inb = {z: [] for z in Z}; t = 0
        for j in range(a):
            blk = [Z[(t + i) % b] for i in range(out[j])]
            self.outb[R[j]] = blk
            for z in blk: inb[z].append(R[j])
            t += out[j] - 1
        # cyclic order of each in-block: the wrap vertex Z[0] sees R[a-1] first
        for z in Z:
            js = inb[z]
            if z == Z[0] and R[a - 1] in js:
                js = [R[a - 1]] + [x for x in js if x != R[a - 1]]
            self.inb[z] = js
        self.rings.append(Z)
        return True

    def link(self, v):
        """cyclic neighbour order of v (ring k >= 1): R[j-1], in-block, R[j+1], out-block reversed."""
        if v == 0: return list(self.outb[0])
        k = self.ring_of[v]; R = self.rings[k]; j = self.pos[v]; a = len(R)
        return [R[(j - 1) % a]] + list(self.inb[v]) + [R[(j + 1) % a]] + list(reversed(self.outb[v]))

    def index(self):
        self.ring_of = {}; self.pos = {}
        for k, R in enumerate(self.rings):
            for j, v in enumerate(R): self.ring_of[v] = k; self.pos[v] = j


def word(D, v): return [D.deg[x] for x in D.link(v)]


leaves = []; stats = {'nodes': 0, 'leaves': 0}
def ring_dfs(D, k):
    """assign degrees to ring k (k >= 1); ring k-1 wheels are checked as their out-blocks complete."""
    if len(leaves) >= MAXLEAVES: return
    R = D.rings[k]; a = len(R); prev = D.rings[k - 1]
    # for each position t of ring k, the vertices of ring k-1 whose out-block is complete once R[0..t] is assigned
    done_at = {t: [] for t in range(a)}
    for v in prev:
        blk = D.outb[v]; idx = [D.pos[z] for z in blk]
        last = a - 1 if idx[-1] == 0 and len(idx) > 1 and idx[0] != 0 else max(idx)
        done_at[last].append(v)
    # ring-k vertices with in >= 2 need degree >= in + 3 (out >= 1)
    choices = []
    for v in R:
        lo = len(D.inb[v]) + 3
        choices.append([d for d in (DEGS if k < K else (6,)) if d >= lo])
    def rec(t):
        if len(leaves) >= MAXLEAVES: return
        stats['nodes'] += 1
        if t == a:
            finish(D, k); return
        for d in choices[t]:
            D.deg[R[t]] = d
            ok = True
            for v in done_at[t]:
                if bad(D.deg[v], word(D, v)): ok = False; break
            if ok: rec(t + 1)
        D.deg.pop(R[t], None)
    rec(0)


def finish(D, k):
    """ring k fully assigned (and ring k-1 checked)."""
    if k < K:
        import copy
        E = copy.deepcopy(D)
        if not E.grow(): return
        E.index(); ring_dfs(E, k + 1); return
    # k == K: ring K is all 6; grow ring K+1 (all 6) to check ring K, then a few more rings for validity
    import copy
    E = copy.deepcopy(D)
    for extra in range(4):
        if not E.grow(): return
        E.index()
        for v in E.rings[-1]: E.deg[v] = 6
        if extra == 0:
            for v in E.rings[K]:
                if bad(6, word(E, v)): return
    c = sum(6 - D.deg[v] for kk in range(K) for v in D.rings[kk])
    if c < CMIN: return
    stats['leaves'] += 1
    leaves.append((c, E))


D = Disc(CENTRE); D.index()
# ring 1: choose degrees; centre wheel checked when ring 1 is complete (centre's out-block = ring 1)
def ring1():
    R = D.rings[1]; a = len(R); seen = set()
    for degs in itertools.product(DEGS if K > 1 else (6,), repeat=a):
        if canon(degs) != tuple(degs) or degs in seen: continue
        seen.add(degs)
        if bad(CENTRE, list(degs)): continue
        for j, v in enumerate(R): D.deg[v] = degs[j]
        E = D
        import copy
        F = copy.deepcopy(E)
        if not F.grow(): continue
        F.index(); ring_dfs(F, 2)
        if len(leaves) >= MAXLEAVES: break
ring1()
print('centre', CENTRE, 'K', K, 'stats', stats, 'leaves', len(leaves), flush=True)
with open(OUT, 'w') as f:
    for c, E in leaves:
        sig = '|'.join(''.join(str(E.deg[v]) for v in E.rings[kk]) for kk in range(K))
        sevens = []
        for v, dv in E.deg.items():
            if dv != 7: continue
            lk = E.link(v); L_ = ''.join(str(E.deg[x]) for x in lk); d = len(lk)
            # s_i = common neighbour of w_i, w_{i+1} other than v
            S_ = ''
            for i in range(d):
                x, y = lk[i], lk[(i + 1) % d]
                com = [z for z in set(E.link(x)) & set(E.link(y)) if z != v]
                S_ += str(E.deg[com[0]]) if len(com) == 1 and com[0] in E.deg else '?'
            sevens.append('%d:%s:%s:%s' % (v, L_, S_, ''.join(str(E.deg[x]) for x in lk)))
        unt7 = sorted({''.join(map(str, canon(word(E, v)))) for v, dv in E.deg.items() if dv == 7 and canon(word(E, v)) not in T7})
        f.write('c=%d sig=%s n7=%d sevens=%s unt7=%s\n' % (c, sig, sum(1 for v in E.deg if E.deg[v] == 7), ' '.join(sevens), ','.join(unt7) or '-'))
