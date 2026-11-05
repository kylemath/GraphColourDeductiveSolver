"""job P870 (Studio): provenance of the keep95p131f section 14' kill tables and V7/V8 l3q masks, on Studio's own st16_filter.py /
l3q_masks.py code (their FORB build, frame and reqs, executed unchanged up to the table loops), with the justifying configuration
names of every killed cell / mask letter. Checks the rebuilt tables equal the saved keep95p131f ones. Writes a JSON of
items -> justifiers. usage: (keep95p131f env) python3 prov_tables.py KILLDIR V7TAB(%s) V8TAB(%s) OUT.json"""
import os, sys, json, itertools, collections
import numpy as np
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
KD_, V7_, V8_, OUTF = sys.argv[1:5]
src = open(os.path.join(HERE, 'out', 'job31', 'st16_filter.py')).read()
pre = src[:src.index("D, LK, SW = 7, [7, 6, 6, 5, 5, 6, 6]")]
sys.argv = ['st16_filter.py', '/tmp/unused']; g = {'__file__': os.path.join(HERE, 'out', 'job31', 'st16_filter.py'), '__name__': 'x'}
exec(pre, g); FORB = g['FORB']; frame = g['frame']; reqs = g['reqs']; LET = g.get('LET', (5, 6, 7, 8, 9))
print('forbidden set %d' % len(FORB), flush=True)
J = 2; KN_W = [('w', J - 2), ('w', J - 1), ('w', J + 1), ('w', J + 2)]; KN_S = [('s', J - 2), ('s', J - 1), ('s', J), ('s', J + 1)]
SLOTS = KN_W + KN_S + [('p', J, 1)]
def table_prov(U):   # = st16_filter.table(U) (strict, unk=6), recording who per killed cell
    Dd = U if U in (7, 8) else 9; who = collections.defaultdict(set); K = np.zeros((5,) * 9, dtype=bool)
    for c1, c2 in itertools.product((5, 6), repeat=2):
        LKf = [6] * Dd; LKf[J] = 6; LKf[J - 1] = c1; LKf[J + 1] = c2; LKf[J - 2] = 6; LKf[J + 2] = 6
        pa, pf = frame(Dd, LKf, {i: 6 for i in range(Dd)})
        known = ([('u',)] if U == 7 else []) + [('w', J)] + SLOTS; fd = {('w', J): 6}
        if U == 7: fd[('u',)] = U
        rs, wh = reqs(list(known), pa, pf, fd)
        for r in rs:
            rd = dict(r)
            if ('p', J, 1) not in rd: continue
            w1, w2 = rd.get(('w', J - 1)), rd.get(('w', J + 1))
            if w1 is not None and (w1 == 5) != (c1 == 5): continue
            if w2 is not None and (w2 == 5) != (c2 == 5): continue
            axes = []
            for k, sl in enumerate(SLOTS):
                if sl in rd: axes.append([rd[sl] - 5])
                elif k == 1: axes.append([0] if c1 == 5 else [1, 2, 3, 4])
                elif k == 2: axes.append([0] if c2 == 5 else [1, 2, 3, 4])
                else: axes.append(range(5))
            for cell in itertools.product(*axes): K[cell] = True; who[cell] |= wh[r]
    return K, who
rep = {'kill': {}, 'v7': {}, 'v8': {}}; ok = True
for U in (7, 8, 9):
    K, who = table_prov(U); Ks = np.load(os.path.join(KD_, 'kill_U%d.npy' % U)); eq = bool((K == Ks).all()); ok &= eq
    print('kill_U%d: %d cells killed, rebuilt == saved: %s' % (U, int(K.sum()), eq), flush=True)
    rep['kill'][U] = {','.join(map(str, c)): sorted(v) for c, v in who.items()}
# l3q masks (l3q_masks.py's frame / setup / reading A), V = 7 and 8
lsrc = open(os.path.join(HERE, 'out', 'job31', 'l3q_masks.py')).read()
for V, tabf, keyname in ((7, V7_, 'v7'), (8, V8_, 'v8')):
    os.environ['L3QV'] = str(V)
    lpre = lsrc[:lsrc.index("TAB = {}; stats = collections.Counter(); REQ = {}")]
    sys.argv = ['l3q_masks.py', os.environ['K3X'].split(',')[0], os.environ['K3X'].split(',')[1], '/tmp/unused_l3q']
    lg = {'__file__': os.path.join(HERE, 'out', 'job31', 'l3q_masks.py'), '__name__': 'x'}; exec(lpre, lg)
    D = lg['D']; FB = lg['FORB']; G = lg['G']; items = {}
    for sig in (1, -1):
        pa, pf = lg['frame'](6, 6); var = lg['setup'](sig, pa); inv = {v: k for k, v in var.items()}
        P = [('u',), ('w', 0)] + list(var.values()); fd = {('u',): D, ('w', 0): 7}
        Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}; RQ = collections.defaultdict(set)
        for cfg in FB:
            for e in G['embeddings'](cfg, P, pa2, pf2, fd):
                RQ[tuple(sorted((inv[v], cfg[3][u]) for u, v in e if v not in fd))].add(cfg[0])
        saved = {tuple(r[:6]): r[6] for r in json.load(open(tabf % ('%+d' % sig)))}
        for c_, a_ in itertools.product((5, 6), repeat=2):
            for w2, w3, w4, o_ in itertools.product((5, 6, 7, 8, 9), repeat=4):
                ent = {'c': c_, 'a': a_, 'w2': w2, 'w3': w3, 'w4': w4, 'o': o_}; kill = collections.defaultdict(set)
                for r, nm in RQ.items():
                    rd = dict(r)
                    if 'a2' in rd and all(ent[k] == v for k, v in rd.items() if k != 'a2'): kill[rd['a2']] |= nm
                m = sum(1 << (L - 5) for L in (5, 6, 7, 8, 9) if L not in kill)
                if m != saved[(c_, a_, w2, w3, w4, o_)]: ok = False
                for L, nm in kill.items(): items['%+d|%d,%d,%d,%d,%d,%d|%d' % (sig, c_, a_, w2, w3, w4, o_, L)] = sorted(nm)
    rep[keyname] = items; print('%s: %d letter kills; rebuilt masks == saved: %s' % (keyname, len(items), ok), flush=True)
rep['ok'] = ok; json.dump(rep, open(OUTF, 'w')); print('ALL REBUILT EQUAL SAVED: %s' % ok)
