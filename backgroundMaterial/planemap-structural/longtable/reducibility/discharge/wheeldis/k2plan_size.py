"""Sizing for the 24 Oct K = 2 plan (README §7.4-7.5; exploratory, counts only, no dfast).
(A) 'B fixed' refinement of the receiver-centred overloads that are not reducible with B free:
    every B of a not-D (and not C-candidate) minimal overload at a 7 (job27/notD.txt minus Job 27 C hits) and at an 8
    (out/eq_D8_k3_dfast.out D=false) is set to 7, 8 (exact, inside the configuration) or left free (= degree >= 9);
    variants = 3^b - 1.  Ring by gen.py's Euler formula (ringf), validated against the layered build on a sample.
(B) Fallback, exact-degree 2-balls of the §6.1 HARD 7-arrangements (out/hard_rows_d7.txt): every private second-ring
    vertex gets a degree in {5,6,7,8} (so 4^p completions); ring = third ring of u (layered build).
(C) Fallback, 3-balls (vertices to distance 3, exact degrees; ring = fourth ring): ring sizes from random completions
    (third-ring degrees iid from {5:0.25, 6:0.5, 7:0.2, 8:0.05}); count = 4^|third ring| per (B) configuration.
CPU-h from the Job 22 dfast18 per-ring means; rings >= 20 have no engine.
Usage: python3 k2plan_size.py"""
import sys, os, re, gzip, random, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(DIS, 'b8b'))
from rings import Layered
gsrc = open(os.path.join(HERE, 'gen.py')).read()
gsrc = gsrc[:gsrc.index('arrs = []')].replace('os.path.dirname(os.path.abspath(__file__))', repr(HERE))
sys.argv = ['gen.py', '/dev/null', '30']; exec(gsrc)
_g = open(os.path.join(HERE, 'gen.py')).read(); exec(_g[_g.index('def make('):_g.index('for d, lk, sv in arrs')])
SEC = {13: 1, 14: 4, 15: 18, 16: 103, 17: 621, 18: 3967, 19: 19736}
def sec(r): return 0.2 if r <= 12 else SEC.get(r, float('inf'))
def summ(tag, rings):
    c = collections.Counter(rings); tot = sum(c.values())
    h = sum(n * sec(r) for r, n in c.items() if r <= 19) / 3600.0
    print('%s: %d configurations; rings %s' % (tag, tot, sorted(c.items())))
    print('   ring <= 16: %d (%.1f CPU-h); ring 17-19: %d (%.0f CPU-h); ring >= 20 (no engine): %d' % (
        sum(n for r, n in c.items() if r <= 16), sum(n * sec(r) for r, n in c.items() if r <= 16) / 3600.0,
        sum(n for r, n in c.items() if 17 <= r <= 19), sum(n * sec(r) for r, n in c.items() if 17 <= r <= 19) / 3600.0,
        sum(n for r, n in c.items() if r >= 20)))

# ---------------- (A)
Chit = set()
for fn in ('k2a.cfast', 'k2b.cfast', 'part00.cfast', 'part01.cfast'):
    cur = None
    for l in open(os.path.join(HERE, 'job27', fn)):
        if ' r=' in l and not l.startswith(' '): cur = l.split()[0]
        elif 'C-REDUCIBLE' in l: Chit.add(cur)
names7 = [l.split()[0] for l in open(os.path.join(HERE, 'job27', 'notD.txt'))]
names8 = [l.split()[0] for l in open(os.path.join(HERE, 'out', 'eq_D8_k3_dfast.out')) if 'D=false' in l]
def variants(nm):
    f = nm.split('_'); d = int(f[0][1:]); lk, sv = f[1], f[2]
    bpos = [('w', j) for j in range(d) if lk[j] == 'B'] + [('s', j) for j in range(d) if sv[j] == 'B']
    out = []
    for ch in itertools.product((7, 8, None), repeat=len(bpos)):
        if all(c is None for c in ch): continue
        w = [int(lk[j]) if lk[j] in '56' else None for j in range(d)]
        s = [int(sv[j]) if sv[j] in '56' else None for j in range(d)]
        for (k, j), c in zip(bpos, ch):
            if c is None: continue
            (w if k == 'w' else s)[j] = c
        out.append((d, w, s))
    return out
rng = random.Random(7)
for tag, names in (('d=7', [n for n in names7 if n not in Chit]), ('d=8', names8)):
    rings = []; chk = [0, 0, 0]
    for nm in names:
        for d, w, s in variants(nm):
            r = ringf(d, w, s); rings.append(r)
            if rng.random() < 0.01 and chk[0] < 300:        # validate ringf against the layered build
                link = [w[j] if w[j] is not None else 9 for j in range(d)]
                adj, name = build(d, link, {('s', j): s[j] for j in range(d) if s[j] is not None})
                inv = {v: x for x, v in name.items()}
                I = [inv[('u',)]] + [inv[('w', j)] for j in range(d) if w[j] is not None] + [inv[('s', j)] for j in range(d) if s[j] is not None]
                deg = {inv[('u',)]: d}; deg.update({inv[('w', j)]: w[j] for j in range(d) if w[j] is not None})
                deg.update({inv[('s', j)]: s[j] for j in range(d) if s[j] is not None})
                try:
                    c = extract(adj, I, deg); chk[0] += 1
                    if c is None: chk[2] += 1
                    elif c[0] == r: chk[1] += 1
                except AssertionError: chk[2] += 1
    summ('(A) B-fixed variants of the %d not-reducible B-free overloads at %s' % (len(names), tag), rings)
    print('   ringf validation on a sample: %d built, %d agree, %d not a simple ring in the free build' % tuple(chk))

# ---------------- (B), (C)
rows = []
for line in open(os.path.join(HERE, 'out', 'hard_rows_d7.txt')):
    m = re.search(r'HARD d=(\d+) link (\d+) s (\d+)', line)
    if m: rows.append((int(m.group(1)), m.group(2), m.group(3)))
def ring2_layered(d, lk, sv):
    L = Layered(d); L.add_ring([int(c) for c in lk]); W = L.rings[1]; Z = L.ring()
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    Wi = {w: i for i, w in enumerate(W)}; kinds = []
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2: i, j = ws; kinds.append(('s', j if (i, j) == (0, d - 1) else i))
        else: kinds.append(('p', ws[0]))
    return L, kinds
cnt2 = 0; rings2 = collections.Counter(); rings6 = collections.Counter(); rings3 = collections.Counter(); n3log = []
with9 = 0; import copy
for d, lk, sv in rows:
    if '9' in lk or '9' in sv: with9 += 1; continue        # a letter 9 (degree >= 9) has no exact 2-ball
    L, kinds = ring2_layered(d, lk, sv); p = sum(1 for k in kinds if k[0] == 'p')
    cnt2 += 4 ** p
    M = copy.deepcopy(L); M.add_ring([int(sv[k[1]]) if k[0] == 's' else 6 for k in kinds]); r6 = len(M.ring()); rings6[r6] += 1
    for _ in range(4):
        pr = iter([rng.choice((5, 6, 7, 8)) for _ in range(p)])
        M = copy.deepcopy(L)
        try: M.add_ring([int(sv[k[1]]) if k[0] == 's' else next(pr) for k in kinds])
        except AssertionError: continue
        r3 = len(M.ring()); rings2[r3] += 4 ** p / 4.0
        third = [rng.choices((5, 6, 7, 8), (0.25, 0.5, 0.2, 0.05))[0] for _ in range(r3)]
        try: M.add_ring(third); rings3[len(M.ring())] += 1; n3log.append(r3)
        except AssertionError: pass
print('(B) exact-degree 2-balls of the %d HARD 7-arrangements of §6.1 (ring = third ring of u):' % len(rows))
print('   %d arrangements contain a letter 9 (degree >= 9: no exact 2-ball); the other %d have %d completions (privates in 5..8)' % (with9, len(rows) - with9, cnt2))
print('   one completion per arrangement (privates all 6): rings %s' % sorted(rings6.items()))
print('   all completions (weighted sample): ring <= 16: %d (%.0f CPU-h); 17-19: %d (%.0f CPU-h); >= 20: %d (no engine)' % (
    sum(n for r, n in rings2.items() if r <= 16), sum(n * sec(r) for r, n in rings2.items() if r <= 16) / 3600.0,
    sum(n for r, n in rings2.items() if 17 <= r <= 19), sum(n * sec(r) for r, n in rings2.items() if 17 <= r <= 19) / 3600.0,
    sum(n for r, n in rings2.items() if r >= 20)))
q = sorted(rings3.elements())
print('(C) 3-balls (ring = fourth ring), %d random completions: ring min %d, median %d, max %d; ring <= 19 in %.2f%%; the third ring has %d-%d vertices, so 4^%d-4^%d completions per (B) configuration' % (
    len(q), q[0], q[len(q) // 2], q[-1], 100.0 * sum(1 for x in q if x <= 19) / len(q), min(n3log), max(n3log), min(n3log), max(n3log)))
