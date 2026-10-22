"""Q2: spin-budget test on ring-colouring classes of dataset windows.
For each sampled window: sample canonical ring colourings, decide direct extension (SAT), and for the
non-extending ones test whether the disc-Stokes identity alone already forbids them (MILP relaxations)."""
import sys, csv, random, collections, json, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from pysat.solvers import Minisat22
sys.path.insert(0, '/mnt/project-files/multiscale/spin_windows')
from spinlib import *

def spins_allowed(d):  return [s for s in range(-(d // 3), d // 3 + 1) if (s - d) % 2 == 0]
def label_at(l0, p):    return (l0 - 1 + p) % 3 + 1
def turns_allowed(k, l0, l1):
    D = (l1 - l0) % 3
    return [t for t in range(-k, k + 1) if (t - k) % 2 == 0 and t % 3 == D]
def net_cross(l0, t, e):   # net signed crossings of label-edge e (frozenset) by lifted walk 0->t
    if t >= 0: return sum(1 for p in range(t) if frozenset((label_at(l0, p), label_at(l0, p + 1))) == e)
    return -sum(1 for p in range(t, 0) if frozenset((label_at(l0, p), label_at(l0, p + 1))) == e)
FACES = [tuple(x for x in range(4) if x != o) for o in range(4)]   # face opposite colour o

class Window:
    def __init__(self, row):
        self.name = row['name']; r, m = int(row['ring']), int(row['m']); self.r, self.m = r, m
        self.adj = parse_window(r, m, row['ring_adj'], row['int_adj'])
        self.rot, self.succ = embed_disc(self.adj, r)
        self.word = ring_word(self.succ, r)
        self.deg = [len(self.adj[v]) for v in range(r + m)]
        self.T = r + 2 * m - 2
        # incremental SAT for extension
        n = r + m; self.var = lambda v, c: 4 * v + c + 1; var = self.var
        s = Minisat22()
        for v in range(n):
            s.add_clause([var(v, c) for c in range(4)])
            for c in range(4):
                for c2 in range(c + 1, 4): s.add_clause([-var(v, c), -var(v, c2)])
            for u in self.adj[v]:
                if u > v:
                    for c in range(4): s.add_clause([-var(v, c), -var(u, c)])
        self.sat = s
    def extend(self, ring):
        if not self.sat.solve(assumptions=[self.var(v, ring[v]) for v in range(self.r)]): return None
        ms = set(x for x in self.sat.get_model() if x > 0)
        return [next(c for c in range(4) if self.var(v, c) in ms) for v in range(self.r + self.m)]

    def ac_refutes(self, ring):
        """Local baseline: domains = colours not on ring neighbours; propagate singleton domains to interior
        neighbours (forward checking to fixpoint). True if some domain becomes empty."""
        r, m, adj = self.r, self.m, self.adj
        dom = {v: set(range(4)) - {ring[u] for u in adj[v] if u < r} for v in range(r, r + m)}
        done = set(); changed = True
        while changed:
            changed = False
            for v in dom:
                if not dom[v]: return True
                if len(dom[v]) == 1 and v not in done:
                    done.add(v); a = next(iter(dom[v]))
                    for u in adj[v]:
                        if u >= r and a in dom[u]: dom[u].discard(a); changed = True
        return any(not d for d in dom.values())

    def budget(self, ring, odd_proper=False, per_face=False, mode='bounded'):
        """True if the spin identities admit a solution (necessary for extension)."""
        r, m, adj, rot = self.r, self.m, self.adj, self.rot
        cols = []; idx = {}
        def nv(key): idx[key] = len(cols); cols.append(key); return idx[key]
        integ = []; lo = []; hi = []
        for v in range(r, r + m):
            forb = {ring[u] for u in adj[v] if u < r}
            for a in range(4):
                if a in forb: continue
                if mode == 'bounded':
                    for s in spins_allowed(self.deg[v]): nv(('z', v, a, s))
                else: nv(('z', v, a, self.deg[v] % 2))   # parity mode: value = parity, slack via y_a
        tinfo = {}
        for v in range(r):
            k = len(rot[v]) - 1; l0 = ring[v] ^ ring[rot[v][0]]; l1 = ring[v] ^ ring[rot[v][-1]]
            ts = turns_allowed(k, l0, l1); tinfo[v] = (l0, ts)
            for t in ts: nv(('y', v, t))
        iy = [nv(('yy', a)) for a in range(4)] if mode == 'parity' else None
        ie = nv(('e',)); iN = [nv(('N', f)) for f in range(4)] if per_face else None
        nvar = len(cols); A = []; bl = []; bu = []
        def row(): return np.zeros(nvar)
        for v in range(r, r + m):
            a_ = row()
            for j, key in enumerate(cols):
                if key[0] == 'z' and key[1] == v: a_[j] = 1
            if not a_.any(): return False        # no colour avoids the ring neighbours
            A.append(a_); bl.append(1); bu.append(1)
        for v in range(r):
            a_ = row()
            for t in tinfo[v][1]: a_[idx[('y', v, t)]] = 1
            if not a_.any(): return False
            A.append(a_); bl.append(1); bu.append(1)
        if odd_proper:
            for v in range(r, r + m):
                for u in adj[v]:
                    if u > v and u >= r and self.deg[u] % 2 and self.deg[v] % 2:
                        for a in range(4):
                            a_ = row()
                            for j, key in enumerate(cols):
                                if key[0] == 'z' and key[1] in (u, v) and key[2] == a: a_[j] = 1
                            A.append(a_); bl.append(-np.inf); bu.append(1)
        par = self.T % 2; P = Psi12([ring[v] for v in self.word])
        # E = 2e+par ; 12 S_a + 4 sum t - 3E = 12 Psi_a  ->  ... - 6e = P_a + 3 par
        for a in (range(4) if mode != 'none' else []):
            a_ = row()
            if mode == 'parity': a_[iy[a]] = 24
            for j, key in enumerate(cols):
                if key[0] == 'z' and key[2] == a: a_[j] = 12 * key[3]
                if key[0] == 'y' and ring[key[1]] == a: a_[j] = 4 * key[2]
            a_[ie] = -6; A.append(a_); bl.append(P[a] + 3 * par); bu.append(P[a] + 3 * par)
        if per_face and mode == 'bounded':
            for f, F in enumerate(FACES):
                for a in F:
                    e = frozenset(a ^ x for x in F if x != a)
                    a_ = row()
                    for j, key in enumerate(cols):
                        if key[0] == 'z' and key[2] == a: a_[j] = key[3]
                        if key[0] == 'y' and ring[key[1]] == a: a_[j] = net_cross(tinfo[key[1]][0], key[2], e)
                    a_[iN[f]] = -1; A.append(a_); bl.append(0); bu.append(0)
            a_ = row(); a_[ie] = 2
            for f in range(4): a_[iN[f]] = -1
            A.append(a_); bl.append(-par); bu.append(-par)
        lb = np.zeros(nvar); ub = np.ones(nvar)
        lb[ie] = -(self.T + par) // 2 - 1; ub[ie] = (self.T - par) // 2 + 1
        if iy:
            for i in iy: lb[i] = -100; ub[i] = 100
        if per_face:
            for i in iN: lb[i] = -self.T; ub[i] = self.T
        res = milp(np.zeros(nvar), constraints=LinearConstraint(np.array(A), bl, bu),
                   integrality=np.ones(nvar), bounds=Bounds(lb, ub))
        return res.status == 0

def canon(c):
    mp = {}; return tuple(mp.setdefault(x, len(mp)) for x in c)
def random_ring(r, rng):
    while True:
        c = [rng.randrange(4)]
        for i in range(1, r): c.append(rng.choice([x for x in range(4) if x != c[-1]]))
        if c[-1] != c[0]: return canon(c)
def all_rings(r):
    out = []
    def rec(c, used):
        if len(c) == r:
            if c[-1] != c[0]: out.append(tuple(c))
            return
        for x in range(min(used + 1, 4)):
            if x != c[-1]: rec(c + [x], max(used, x + 1))
    rec([0], 1); return out

if __name__ == '__main__':
    rows = list(csv.DictReader(open('/mnt/project-files/explore/dataset/windows_judged.tsv'), delimiter='\t'))
    rng = random.Random(2026)
    groups = {
      'a7_D':    [x for x in rows if x['name'].startswith('a7_') and x['two_engine'] == 'D'],
      'a7_notD': [x for x in rows if x['name'].startswith('a7_') and x['kc_D'] == 'false' and 10 <= int(x['ring']) <= 15],
      'a9_D':    [x for x in rows if x['name'].startswith('a9_') and x['two_engine'] == 'D'],
      'a9_notD': [x for x in rows if x['name'].startswith('a9_') and x['kc_D'] == 'false' and 10 <= int(x['ring']) <= 15],
    }
    NW = int(sys.argv[1]) if len(sys.argv) > 1 else 12; NS = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    out = open('/mnt/project-files/multiscale/spin_windows/q2_results_'+(sys.argv[3] if len(sys.argv)>3 else 'x')+'.tsv', 'w')
    KEYS = ['ac', 'blocked', 'oddcol', 'A', 'A_odd', 'A_only_spin', 'Aodd_only_spin', 'A_beyond_ac', 'Aodd_beyond_ac', 'ac_or_A_odd', 'P_tested', 'P_same', 'F_tested', 'F_extra']
    out.write('group\tname\tring\tm\tdegs\tclasses_sampled\text\tbad\t' + '\t'.join(KEYS) + '\tgood_pass_check\n')
    summary = {}
    for g, pool in groups.items():
        if len(sys.argv) > 4 and g != sys.argv[4]: continue
        rng.shuffle(pool); tot = collections.Counter()
        for row in pool[:NW]:
            W = Window(row); r = W.r
            rings = all_rings(r) if r <= 9 else list({random_ring(r, rng) for _ in range(NS)})
            ext = bad = 0; kills = collections.Counter(); gp = 0; gtested = 0; fcheck = 0; fcheck2 = 0
            for ring in rings:
                col = W.extend(ring)
                if col is not None:
                    ext += 1
                    if gtested < 5:   # soundness check: good classes must pass all variants
                        gtested += 1; gp += W.budget(ring, True, True) and W.budget(ring, True, mode='parity')
                    continue
                bad += 1
                ac = W.ac_refutes(ring)
                b0 = not W.budget(ring, mode='none'); b0o = not W.budget(ring, odd_proper=True, mode='none')
                kA = b0 or not W.budget(ring); kAo = b0o or kA or not W.budget(ring, odd_proper=True)
                kills['ac'] += ac; kills['blocked'] += b0; kills['oddcol'] += b0o
                kills['A'] += kA; kills['A_odd'] += kAo
                kills['A_only_spin'] += kA and not b0; kills['Aodd_only_spin'] += kAo and not b0o
                kills['A_beyond_ac'] += kA and not ac; kills['Aodd_beyond_ac'] += kAo and not ac
                kills['ac_or_A_odd'] += ac or kAo
                if kA and not b0 and fcheck < 10:
                    fcheck += 1; kills['P_tested'] += 1; kills['P_same'] += (not W.budget(ring, mode='parity'))
                if not kA and fcheck2 < 5:
                    fcheck2 += 1; kills['F_tested'] += 1; kills['F_extra'] += not W.budget(ring, per_face=True)
            degs = collections.Counter(W.deg[W.r:]); ds = ','.join('%d:%d' % kv for kv in sorted(degs.items()))
            out.write('%s\t%s\t%d\t%d\t%s\t%d\t%d\t%d\t' % (g, W.name, r, W.m, ds, len(rings), ext, bad)
                      + '\t'.join(str(kills[k]) for k in KEYS) + '\t%d/%d\n' % (gp, gtested)); out.flush()
            tot['classes'] += len(rings); tot['ext'] += ext; tot['bad'] += bad
            for k, v in kills.items(): tot[k] += v
            print(g, W.name, r, W.m, ds, len(rings), ext, bad, dict(kills), '%d/%d' % (gp, gtested), flush=True)
        summary[g] = dict(tot); print(g, dict(tot), flush=True)
    json.dump(summary, open('/mnt/project-files/multiscale/spin_windows/q2_summary_'+(sys.argv[3] if len(sys.argv)>3 else 'x')+'.json', 'w'), indent=1)
