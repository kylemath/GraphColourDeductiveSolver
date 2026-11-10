#!/usr/bin/env python3
"""seed_compress Stage B cover test (Opus, 10 Nov 2026).

For each RSST configuration C (unavoidable.conf, 633) and each kill family F (a pattern list in mkfamlist.py TSV form, plus the
engine's wheel kills R5 / R6 / RBIG), decide whether every triangulation that contains C also contains a kill of F, using only C.

Placement test.  For an interior vertex z of C of degree d, the row label of z (link letters w_i, apex letters s_i, letters
5,6,7,8,9 with 9 = degree >= 9, as the LP engine reads them) is fixed at the slots that C determines (an interior vertex of C)
and unknown elsewhere (a ring vertex of C, or an apex that C does not draw).  z is KILLED if every completion of the unknown
slots is inadmissible under F with the engine's own admissible() semantics:
  * a pattern of F (any of its 2d rotations / reflections) matches, or
  * a link 5 has an R5 word (U, w+1, s, s-1, w-1), U = min(d, 9), or
  * a link 6 has an R6 word for every private letter p (the row does not know p), or
  * d in {7, 8} and the link word is in RBIG.
For an interior 5- or 6-vertex z, z is KILLED if every completion of its wheel word is R5 (resp. R6).
C is COVERED by F if some interior vertex of C is KILLED.  Then every state C kills (in any engine, at any degree, on any
centre) contains a kill of F, because the completions range over every degree the unknown vertices can have.  The test is
sound but not complete: a state can also be killed by an F-config that uses vertices outside C, which this test never sees.

DFS: completions are searched depth first (letter order 6, 9, 8, 7, 5 to find an uncovered completion fast), pruned by the
patterns still compatible with the assigned letters; a placement that needs more than CAP nodes counts as NOT killed.

usage: python3 -I cover.py <family tag> <patterns tsv> <out tsv> [cap]
"""
import sys, os, re, json, itertools, collections, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
ENG = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7/eng_p8/pcheck.py'
ROOT = SP + '/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
DIS = os.path.dirname(ROOT)
CONF = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/studiointel/routeb/rsst/unavoidable.conf'

LET = (5, 6, 7, 8, 9); LI = {l: i for i, l in enumerate(LET)}; UNK = 5
SETS = {'5': (5,), '6': (6,), '7': (7,), '8': (8,), 'B': (7, 8, 9)}

def pname(name):   # = pcheck.py pname
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

def rpat_slots(line):   # = pcheck.py rpat= decoding
    f = line.split(); d, k = int(f[0]), int(f[1]); slots = {}
    for j in range(k):
        i, m = int(f[2 + 2 * j]), int(f[3 + 2 * j])
        rd = [('w', (i + 1) % d), ('s', i), ('s', (i - 1) % d), ('w', (i - 1) % d)]
        ent = [(('w', i), frozenset((5,)))] + [(rd[t], frozenset(LET[b] for b in range(5) if (m >> (5 * t + b)) & 1)) for t in range(4)]
        for sl, S_ in ent: slots[sl] = slots.get(sl, frozenset(LET)) & S_
    return d, tuple(sorted(slots.items()))

def rpatn_slots(line):   # = pcheck.py rpatN= decoding
    f = line.split(); d, lk, sv = int(f[0]), f[1], f[2]
    return d, tuple(sorted(((typ, i), frozenset((6, 7, 8, 9)) if ch == 'N' else frozenset((int(ch),)))
                           for typ, word in (('w', lk), ('s', sv)) for i, ch in enumerate(word) if ch != '.'))

def load_family(tsv):
    PATS = collections.defaultdict(list); NAME = {}; KIND = {}; seen = set()
    for line in open(tsv):
        if line.startswith('#') or line.startswith('kind\t') or not line.strip(): continue
        kind, name, d_, src, nd = line.rstrip('\n').split('\t')
        if kind in ('D', 'C'): d, P = pname(name)
        elif kind == 'RPAT': d, P = rpat_slots(name)
        elif kind == 'RPATN': d, P = rpatn_slots(name)
        else: raise SystemExit('unknown kind ' + kind)
        assert d == int(d_), line
        if (d, P) in seen: continue
        seen.add((d, P)); PATS[d].append(P); NAME[(d, P)] = name; KIND[(d, P)] = (kind, src)
    return PATS, NAME, KIND

# wheel kills: the engine's own block, exec'd verbatim
_src = open(ENG).read()
_blk = _src[_src.index('# ---------------- reducible wheels ----------------'):_src.index('# ---------------- variables ----------------')]
G = {'os': os, 're': re, 'LET': LET, 'ROOT': ROOT, 'DIS': DIS, 'FLAGS': set(), 'OPT': {}}
exec(compile(_blk, 'pcheck.py:wheels', 'exec'), G)
isR5, isR6, RBIG, canon = G['isR5'], G['isR6'], G['RBIG'], G['canon']

class Inst:
    """all rotations / reflections of the patterns at degree d, as numpy arrays over 2d+1 slots (slot 2d = dummy, always ok);
    mask bit b = letter LET[b] allowed, bit 5 = unknown allowed (only for an unconstrained slot)"""
    def __init__(self, PATS, d):
        rows = []; src = []
        for P in PATS.get(d, ()):
            for r in range(d):
                for refl in (False, True):
                    m = {}
                    for (typ, i), S in P:
                        j = (i + r) % d if not refl else ((r - i) % d if typ == 'w' else (r - i - 1) % d)
                        slot = 2 * j + (0 if typ == 'w' else 1)
                        m[slot] = m.get(slot, 31) & sum(1 << LI[x] for x in S)
                    rows.append(tuple(sorted(m.items()))); src.append(P)
        u = {}
        for x, P in zip(rows, src): u.setdefault(x, P)
        self.keys = list(u.keys()); self.src = [u[k] for k in self.keys]
        mm = max((len(x) for x in self.keys), default=1)
        self.SL = np.full((len(self.keys), mm), 2 * d, dtype=np.int64); self.MK = np.full((len(self.keys), mm), 63, dtype=np.int64)
        for n, x in enumerate(self.keys):
            for j, (sl, k) in enumerate(x):
                self.SL[n, j] = sl; self.MK[n, j] = (k | 32) if k == 31 else k

class Undecided(Exception): pass

def placement_killed(d, lets0, inst, cap):
    """lets0: list of 2d letter indices (UNK = unknown), slot 2j = w_j, 2j+1 = s_j.  Returns (killed, info)."""
    U = min(d, 9); nodes = [0]; leaf = [None]
    def lv(lets, slot): return lets[slot]
    def wheel_kill(lets):
        w = lambda j: lets[2 * (j % d)]; s = lambda j: lets[2 * (j % d) + 1]
        for i in range(d):
            if w(i) == LI[5]:
                wd = [w(i + 1), s(i), s(i - 1), w(i - 1)]
                if UNK not in wd and isR5([U] + [LET[x] for x in wd]): return 'R5 at w%d' % i
            elif w(i) == LI[6]:
                wd = [w(i + 1), s(i), s(i - 1), w(i - 1)]
                if UNK not in wd:
                    a, b, c, e = [LET[x] for x in wd]
                    if all(isR6([U, a, b, p, c, e]) for p in LET): return 'R6 at w%d' % i
        if d in (7, 8):
            ww = [w(i) for i in range(d)]
            if UNK not in ww and ''.join(map(str, canon([LET[x] for x in ww]))) in RBIG: return 'RBIG link'
        return None
    def rec(lets, comp):
        nodes[0] += 1
        if nodes[0] > cap: raise Undecided()
        L = np.array(lets + [0], dtype=np.int64)
        if len(comp):
            sub = L[inst.SL[comp]]; mk = inst.MK[comp]
            ok = (mk >> sub) & 1
            hit = np.all(ok, axis=1)
            if hit.any(): return 'pattern'
            compat = np.all(ok | (sub == UNK), axis=1)
            comp = comp[compat]
        wk = wheel_kill(lets)
        if wk: return wk
        unk = [k for k in range(2 * d) if lets[k] == UNK]
        if not unk:
            leaf[0] = list(lets); return None
        # branch on the unknown slot used most by the compatible patterns (ties: link before apex)
        if len(comp):
            sl = inst.SL[comp]; cnt = collections.Counter(sl[(L[sl] == UNK)].tolist())
            slot = max(unk, key=lambda k: (cnt.get(k, 0), -k))
        else: slot = unk[0]
        for x in (6, 9, 8, 7, 5):
            l2 = list(lets); l2[slot] = LI[x]
            if not rec(l2, comp): return None
        return 'completion'
    try:
        r = rec(list(lets0), np.arange(len(inst.keys)))
    except Undecided:
        return False, 'undecided (cap %d)' % cap, nodes[0]
    LEAF[0] = leaf[0]
    return (r is not None), r, nodes[0]
LEAF = [None]

def wheel_killed(dz, word0, cap):
    """interior 5 / 6 vertex with neighbour letters word0 (None = unknown): every completion R5 / R6?"""
    unk = [k for k, x in enumerate(word0) if x is None]
    if len(unk) > 6: return False, 'too many unknowns'
    n = 0
    for comb in itertools.product(LET, repeat=len(unk)):
        w = list(word0)
        for k, x in zip(unk, comb): w[k] = x
        n += 1
        if not (isR5(w) if dz == 5 else isR6(w)): return False, 'completion %s not R%d' % (''.join(map(str, w)), dz)
    return True, 'R%d wheel (%d completions)' % (dz, n)

def parse_conf(path):
    blocks, cur = [], []
    for line in open(path):
        if line.strip() == '':
            if cur: blocks.append(cur); cur = []
        else: cur.append(line.split())
    if cur: blocks.append(cur)
    out = []
    for b in blocks:
        name = b[0][0]; n, r = int(b[1][0]), int(b[1][1]); k = int(b[2][0]); adj = {}
        for row in b[3:3 + n]:
            i, dg = int(row[0]), int(row[1]); adj[i] = [int(x) for x in row[2:2 + dg]]
            assert len(adj[i]) == dg, (name, i)
        out.append(dict(name=name, n=n, r=r, k=k, adj=adj))
    return out

def letter(c, v):
    if v is None or v <= c['r']: return None
    return min(len(c['adj'][v]), 9)

def apex(c, z, a, b):
    """third vertex of the face on edge a-b away from z (z, a, b consecutive around z), if C determines it"""
    adj = c['adj']; res = set()
    for x, y in ((a, b), (b, a)):
        if x <= c['r']: continue   # ring vertex: partial rotation
        R = adj[x]; n = len(R); p = R.index(z)
        for e in (1, -1):
            if R[(p + e) % n] == y: res.add(R[(p + 2 * e) % n])
    if len(res) > 1: raise ValueError('inconsistent apex %s %s %s %s' % (c['name'], z, a, b))
    return res.pop() if res else None

def main():
    tag, tsv, outf = sys.argv[1], sys.argv[2], sys.argv[3]; cap = int(sys.argv[4]) if len(sys.argv) > 4 else 20000
    PATS, NAME, KIND = load_family(tsv)
    print('%s: %s patterns by d %s; R5 %d R6 %d RBIG %d FANS %d' % (tag, sum(len(v) for v in PATS.values()), {d: len(v) for d, v in sorted(PATS.items())},
          len(G['R5']), len(G['R6']), len(RBIG), len(G['FANS'])), flush=True)
    INST = {}
    confs = parse_conf(CONF); t0 = time.time(); global LV; LV = open(outf + '.leaves', 'w')
    with open(outf, 'w') as g:
        g.write('# cover.py %s on %s (cap %d): idx\tname\tcovered\tkilled_vertices\twitness\tdetail\n' % (tag, os.path.basename(tsv), cap))
        g.write('idx\tname\tcovered\tn_killed_vertices\twitness_vertex\twitness_kind\twitness_detail\tundecided_placements\n')
        for idx, c in enumerate(confs):
            adj = c['adj']; kills = []; und = 0
            for z in range(c['r'] + 1, c['n'] + 1):
                dz = len(adj[z]); L = adj[z]
                if dz in (5, 6):
                    ok, info = wheel_killed(dz, [letter(c, v) for v in L], cap)
                    if ok: kills.append((z, 'wheel', info))
                    continue
                if dz not in PATS and dz not in (7, 8): continue
                if dz not in INST: INST[dz] = Inst(PATS, dz)
                lets = []
                for i in range(dz):
                    wl = letter(c, L[i]); sv = apex(c, z, L[i], L[(i + 1) % dz]); sl = letter(c, sv)
                    lets += [UNK if wl is None else LI[wl], UNK if sl is None else LI[sl]]
                ok, info, nn = placement_killed(dz, lets, INST[dz], cap)
                if not ok and LEAF[0] is not None:   # an admissible completion: engine cross-check input
                    lf = LEAF[0]; LV.write('%d\t%s\t%d\tadm\t%d %s %s\n' % (idx, c['name'], z, dz, ''.join(str(LET[lf[2 * i]]) for i in range(dz)), ''.join(str(LET[lf[2 * i + 1]]) for i in range(dz))))
                if ok:   # killed: a few random completions for the engine cross-check (all must be rejected)
                    import random; rnd = random.Random(idx * 1000 + z)
                    for _ in range(3):
                        lf = [LI[rnd.choice(LET)] if x == UNK else x for x in lets]
                        LV.write('%d\t%s\t%d\tkill\t%d %s %s\n' % (idx, c['name'], z, dz, ''.join(str(LET[lf[2 * i]]) for i in range(dz)), ''.join(str(LET[lf[2 * i + 1]]) for i in range(dz))))
                if info and str(info).startswith('undecided'): und += 1
                if ok:
                    det = info
                    if info == 'pattern':   # name the first matching pattern
                        Lr = np.array(lets + [0]); I = INST[dz]
                        hit = np.all((I.MK >> Lr[I.SL]) & 1, axis=1); P = I.src[int(np.argmax(hit))]
                        det = 'pattern %s %s (%s)' % (KIND[(dz, P)][0], NAME[(dz, P)], KIND[(dz, P)][1])
                    elif info == 'completion': det = 'completion cover, %d DFS nodes' % nn
                    kills.append((z, 'd%d label' % dz, det))
            word = lambda z: ''.join(str(letter(c, v) or '.') for v in adj[z])
            if kills:
                z, kd, det = kills[0]
                g.write('%d\t%s\tyes\t%d\t%d (deg %d, nbrs %s)\t%s\t%s\t%d\n' % (idx, c['name'], len(kills), z, len(adj[z]), word(z), kd, det, und))
            else:
                g.write('%d\t%s\tno\t0\t-\t-\t-\t%d\n' % (idx, c['name'], und))
            if idx % 50 == 0: print('  %d configs, %.0f s' % (idx, time.time() - t0), flush=True)
    print('done %d configs %.0f s' % (len(confs), time.time() - t0))

if __name__ == '__main__':
    main()
