"""s63 provenance rebuild: re-runs Studio/outside kill-table, l3q-mask and 2-ball-rule derivations on the Tier A forbidden set,
but keeps WHICH configuration produced each requirement.  Read-only on the repo; writes prov.pkl.  usage: prov_build.py WD NL51 OUT.pkl"""
import os, sys, re, glob, json, itertools, collections, pickle, time
WD, NL51, OUT = sys.argv[1:4]
os.chdir(WD)
src = open('out/job31/st16_filter.py').read()
head, rest = src.split("# ---- 1) check 4, full test ----", 1)
sys.argv = ['st16_filter.py', '/tmp/s63_st16_unused']
os.environ['K3X'] = 'out/job30/k3x_D.out,out/job30/k3x_C.cfast'
g = {'__file__': os.path.join(WD, 'out/job31/st16_filter.py'), '__name__': 'st16'}
exec(compile(head, 'st16_head', 'exec'), g)
G = g['G']; FORB = g['FORB']; ver = g['ver']
# class of each config
cls = {}
for c in FORB:
    if c[0].startswith('rsst'): cls[c[0]] = 'rsst' + ('D' if ver.get(c[0]) == 'D2' else 'C')
kD = {l.split()[0] for l in open('out/job30/k3x_D.out') if re.match(r'^[epf]\d+_\S+ r=\d+ ', l)}
for c in FORB:
    if c[0] not in cls: cls[c[0]] = 'k3xD' if c[0] in kD else 'k3xC'
EXTRA = []; cl2 = {}
for l in open(NL51).read().splitlines():
    f = l.split()
    if len(f) == 5 and f[1].isdigit() and f[2].isdigit() and ';' in f[3] + f[4]: EXTRA.append(G['kcline'](l, 'nl51')); cl2[f[0]] = 'nl51'
for fn, k in (('out/job30/k3p_D.out', 'k3pD'), ('out/job30/k3p_C.cfast', 'k3pC')):
    for l in open(fn):
        if not l.strip() or l[0].isspace(): continue
        f = l.split()
        if len(f) >= 5 and f[1].isdigit() and f[2].isdigit() and ';' in f[3] + f[4]: EXTRA.append(G['kcline'](' '.join(f[:5]), 'k3p')); cl2[f[0]] = k
have = {c[0] for c in FORB}
EXTRA = [c for c in EXTRA if c[0] not in have]
for c in EXTRA: cls[c[0]] = cl2[c[0]]
FORB += EXTRA
print('FORB', len(FORB), collections.Counter(cls[c[0]] for c in FORB), flush=True)
LET = (5, 6, 7, 8, 9)
import numpy as np
# ---- KT records with provenance ----
J = 2
KN_W = [('w', J - 2), ('w', J - 1), ('w', J + 1), ('w', J + 2)]; KN_S = [('s', J - 2), ('s', J - 1), ('s', J), ('s', J + 1)]
SLOTS = KN_W + KN_S + [('p', J, 1)]
def reqs_who(P, pa, pf, fd):
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}; who = collections.defaultdict(set)
    for c in FORB:
        for e in G['embeddings'](c, P, pa2, pf2, fd):
            who[tuple(sorted((v, c[3][u]) for u, v in e if v not in fd))].add(c[0])
    return who
def frame(D, LK, SV):
    G['D'] = D; G['LK'] = LK; G['SV'] = dict(SV)
    adj, name, faces = G['build2']({('s', j): v for j, v in SV.items()})
    pa = {x: {name[y] for y in adj[v] if y in name} for v, x in name.items()}
    pf = {frozenset(name[y] for y in f) for f in faces if all(y in name for y in f)}
    return pa, pf
KTREC = {}
for U in (7, 9):
    t0 = time.time(); Dd = U if U in (7, 8) else 9; acc = {}
    for c1, c2 in itertools.product((5, 6), repeat=2):
        LKf = [6] * Dd; LKf[J] = 6; LKf[J - 1] = c1; LKf[J + 1] = c2; LKf[J - 2] = 6; LKf[J + 2] = 6
        pa, pf = frame(Dd, LKf, {i: 6 for i in range(Dd)})
        known = ([('u',)] if U == 7 else []) + [('w', J)] + SLOTS; fd = {('w', J): 6}
        if U == 7: fd[('u',)] = U
        who = reqs_who(list(known), pa, pf, fd)
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
    KTREC[U] = list(acc.items()); print('KT U=%d: %d distinct requirement boxes, %.0fs' % (U, len(acc), time.time() - t0), flush=True)
KTREC[8] = KTREC[9]
# ---- l3q records ----
L3REC = {}
for D_val in (7, 8):
    for sig in (1, -1):
        def frame_l3(lk_fill, sv_fill):
            LK = [7] + [lk_fill] * 4 + [9] * (D_val - 5)
            return frame(D_val, LK, {i: sv_fill for i in range(D_val)})
        pa, pf = frame_l3(6, 6)
        W = lambda k: ('w', k % D_val); S = lambda k: ('s', k % D_val)
        a = S(0) if sig == 1 else S(-1); o = S(-1) if sig == 1 else S(0)
        priv = [x for x in pa if x[0] == 'p' and x[1] == 0]; a2 = [x for x in priv if a in pa[x]]; assert len(a2) == 1
        var = {'c': W(sig), 'w2': W(2 * sig), 'w3': W(3 * sig), 'w4': W(4 * sig), 'a': a, 'o': o, 'a2': a2[0]}
        inv = {v: k for k, v in var.items()}
        P = [('u',), ('w', 0)] + list(var.values()); fd = {('u',): D_val, ('w', 0): 7}
        who = reqs_who(P, pa, pf, fd)
        L3REC[(D_val, sig)] = [({inv[v]: gg for v, gg in r}, ws) for r, ws in who.items()]
        print('l3q V=%d sig=%+d: %d reqs' % (D_val, sig, len(who)), flush=True)
# ---- 2-ball rules with provenance (outside team's extract_full2ball_rules, source-sliced from build_upgraded_kills.py) ----
bsrc = open(os.environ['BUK']).read()
a_ = bsrc.index('def extract_full2ball_rules'); b_ = bsrc.index('def build_extra_rules_dict')
fsrc = bsrc[a_:b_].replace('rules_by_p[p_v].add(rule)', 'rules_by_p[p_v].add(rule); PROV.setdefault((D_val, w0, p_v, rule), set()).add(c[0])')
PROV = {}
ns = {'G': G, 'PROV': PROV, 'LET': LET, 'itertools': itertools, 'collections': collections}
exec(compile(fsrc, 'rules_src', 'exec'), ns)
t0 = time.time()
RULES = {}
for (Dv, w0, ue) in ((7, 6, True), (7, 7, True), (8, 6, True), (8, 7, True), (9, 6, False)):
    ns['extract_full2ball_rules'](Dv, w0, FORB, ue)
RULEPROV = {k: v for k, v in PROV.items()}
print('rules provenance: %d (D,w0,p,rule) entries, %.0fs' % (len(RULEPROV), time.time() - t0), flush=True)
pickle.dump({'cls': cls, 'KTREC': KTREC, 'L3REC': L3REC, 'RULEPROV': RULEPROV, 'nforb': len(FORB)}, open(OUT, 'wb'))
