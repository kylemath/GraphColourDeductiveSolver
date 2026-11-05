"""s77 Team B2: independent check of the B1 kill6 patch (222 new U7 bits) with OUR embedding code.
Method = s63_minconf/scripts/prov_build.py KT part (Studio st16_filter spec 14' frame, grow.embeddings, strict rule),
run on the 7 new configurations only (kc lines of configs_D_kill6.txt), U = 7 and U = 9 (U = 8 uses the U = 9 frame).
No code from B1's k6patch.py is used.  Also rebuilds the base U7/U9 cells from s63 prov.pkl KTREC (keep-justified boxes,
s71 items.pkl, as s73_prune/cells/build_cells.py) and checks them against s64_keep95p131f/tab/kill.
usage: python3 k6check.py GROW_PY CONFIGS_TXT PATCHED_PREFIX OUT_PREFIX   (run from P_own_lp)"""
import sys, os, itertools, collections, pickle, hashlib
import numpy as np
GROW, CFG, PATCH, OUTP = sys.argv[1:5]
G = {'__file__': GROW, '__name__': 'grow'}
exec(open(GROW).read(), G)
LET = (5, 6, 7, 8, 9)
FORB = []
for l in open(CFG):
    if l.startswith('#') or not l.strip(): continue
    kc = l.split('|')[0].strip(); FORB.append(G['kcline'](kc, 'b1'))
print('new configurations: %d' % len(FORB), [c[0] for c in FORB], flush=True)
# ---- prov_build.py KT derivation (verbatim logic) ----
J = 2
KN_W = [('w', J - 2), ('w', J - 1), ('w', J + 1), ('w', J + 2)]; KN_S = [('s', J - 2), ('s', J - 1), ('s', J), ('s', J + 1)]
SLOTS = KN_W + KN_S + [('p', J, 1)]
def reqs_who(P, pa, pf, fd, forb):
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}; who = collections.defaultdict(set)
    for c in forb:
        for e in G['embeddings'](c, P, pa2, pf2, fd):
            who[tuple(sorted((v, c[3][u]) for u, v in e if v not in fd))].add(c[0])
    return who
def frame(D, LK, SV):
    G['D'] = D; G['LK'] = LK; G['SV'] = dict(SV)
    adj, name, faces = G['build2']({('s', j): v for j, v in SV.items()})
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in name.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    return pa, pf
def ktrec(U, forb):
    Dd = U if U in (7, 8) else 9; acc = {}
    for c1, c2 in itertools.product((5, 6), repeat=2):
        LKf = [6] * Dd; LKf[J] = 6; LKf[J - 1] = c1; LKf[J + 1] = c2; LKf[J - 2] = 6; LKf[J + 2] = 6
        pa, pf = frame(Dd, LKf, {i: 6 for i in range(Dd)})
        known = ([('u',)] if U == 7 else []) + [('w', J)] + SLOTS; fd = {('w', J): 6}
        if U == 7: fd[('u',)] = U
        who = reqs_who(list(known), pa, pf, fd, forb)
        for r, ws in who.items():
            rd = dict(r)
            if ('p', J, 1) not in rd: continue
            w1, w2 = rd.get(('w', J - 1)), rd.get(('w', J + 1))
            if w1 is not None and (w1 == 5) != (c1 == 5): continue
            if w2 is not None and (w2 == 5) != (c2 == 5): continue
            mk = []
            for k, sl in enumerate(SLOTS):
                if sl in rd: mk.append(1 << (rd[sl] - 5))
                elif k == 1: mk.append(1 if c1 == 5 else 30)
                elif k == 2: mk.append(1 if c2 == 5 else 30)
                else: mk.append(31)
            acc.setdefault(tuple(mk), set()).update(ws)
    return list(acc.items())
def build(boxes):
    K = np.zeros((5,) * 9, bool)
    for mk, ws in boxes: K[np.ix_(*[[i for i in range(5) if (m >> i) & 1] for m in mk])] = True
    return K
def pack(K):
    A = np.zeros((5,) * 8, np.uint8)
    for b in range(5): A |= K[..., b].astype(np.uint8) << b
    return A
def unpack(A): return np.stack([(A >> b) & 1 for b in range(5)], axis=-1).astype(bool)
def mirror(K): return np.transpose(K, (3, 2, 1, 0, 7, 6, 5, 4, 8))
def boxstr(mk):
    f = lambda m: '.' if m == 31 else ('^5' if m == 30 else '[' + ''.join(str(5 + i) for i in range(5) if (m >> i) & 1) + ']' if bin(m).count('1') > 1 else str(4 + m.bit_length()))
    return ''.join(f(m) for m in mk[:4]) + ' ' + ''.join(f(m) for m in mk[4:8]) + ' p=' + f(mk[8])
base = {U: np.load('s64_keep95p131f/tab/kill/kill6_U%d.npy' % U) for U in (7, 8, 9)}
pat = {U: np.load(PATCH + '_U%d.npy' % U) for U in (7, 8, 9)}
res = {}
for U in (7, 9):
    rec = ktrec(U, FORB); res[U] = rec
    print('U=%d: %d requirement boxes from the new configurations' % (U, len(rec)), flush=True)
    for mk, ws in sorted(rec, key=lambda x: sorted(x[1])): print('   box %s  <- %s' % (boxstr(mk), ','.join(sorted(ws))))
out = {}
for U in (7, 8, 9):
    Kn = build(res[9 if U == 8 else U]); Bn = unpack(base[U]); Pn = unpack(pat[U])
    new_cells = int(Kn.sum()); add = Kn & ~Bn; reb = Bn | Kn
    print('U%d: new-config cells %d (mirror exceptions %d), of which not in base %d; base %d, patched %d (patched-base %d, base-patched %d)' % (
        U, new_cells, int((Kn != mirror(Kn)).sum()), int(add.sum()), int(Bn.sum()), int(Pn.sum()), int((Pn & ~Bn).sum()), int((Bn & ~Pn).sum())))
    d1 = Pn & ~reb; d2 = reb & ~Pn
    print('U%d: rebuilt (base | ours) vs B1 patched: equal %s; in patched not ours %d; ours not in patched %d' % (U, bool((reb == Pn).all()), int(d1.sum()), int(d2.sum())), flush=True)
    for nm, D_ in (('patched-not-ours', d1), ('ours-not-patched', d2)):
        for idx in list(zip(*np.nonzero(D_)))[:20]: print('   %s %s' % (nm, ''.join(str(5 + int(i)) for i in idx[:4]) + ' ' + ''.join(str(5 + int(i)) for i in idx[4:8]) + ' p=' + str(5 + int(idx[8]))))
    A = pack(reb); out[U] = A
    fn = OUTP + '_U%d.npy' % U; np.save(fn, np.ascontiguousarray(A))
    print('U%d: rebuilt table %s file md5 %s; B1 patched file md5 %s' % (U, fn, hashlib.md5(open(fn, 'rb').read()).hexdigest(), hashlib.md5(open(PATCH + '_U%d.npy' % U, 'rb').read()).hexdigest()), flush=True)
# per-configuration contribution (U7)
Bn = unpack(base[7])
for c in FORB:
    r = ktrec(7, [c]); K = build(r)
    print('  %-28s boxes %d cells %d new over base %d' % (c[0], len(r), int(K.sum()), int((K & ~Bn).sum())))
# ---- base reproduction from s63 prov.pkl (as s73 build_cells.py) ----
P = pickle.load(open('s63_minconf/prov.pkl', 'rb')); items = pickle.load(open('s71_ruleset/items.pkl', 'rb'))
for U, tag in ((7, 'KT7'), (9, 'KT9')):
    its = {int(it[1]): it[2] for it in items if it[0] == tag}; rec = P['KTREC'][U]
    keep = [(rec[i][0], ws) for i, ws in its.items() if ws]
    K = build(keep); A = pack(K)
    print('base from prov.pkl KTREC U%d (keep-justified boxes %d): cells %d; equals s64 kill6_U%d %s (diff bits %d)' % (
        U, len(keep), int(K.sum()), U, bool((A == base[U]).all()), int((K != unpack(base[U])).sum())), flush=True)
    K2 = K | build(res[U]); print('   prov.pkl base boxes + our new boxes vs B1 patched U%d: equal %s' % (U, bool((pack(K2) == pat[U]).all())))
