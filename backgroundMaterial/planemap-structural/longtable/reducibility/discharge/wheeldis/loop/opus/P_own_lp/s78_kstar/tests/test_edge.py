# s78 test 0 for the generic EDGE family (orientation / semantics against W6's grammar.py + gext.py, as test_orient.py does for K*):
# per key, on d = 7 pictures (W6's certpics.recv_pic: link + apexes exact, 6-privates amask & ~extra6, 7-privates L3T & ~extra7) and d = 8
# pictures (6-privates amask & ~extra6, 7-privates free): engine payer count == grammar 'out' SURE count (exact), engine payee credit (the
# window bound) >= grammar 'in' POSSIBLE count on every row (the bound may only over-credit), equality rate reported; the grammar's MIRROR of
# each key must give the same columns; a deliberately mis-oriented control (one + position flipped to -) must differ.
# Also KG (= K* as a generic key) vs the K* family: payer identical, generic payee >= exact K* payee.   usage: python3 test_edge.py [N] [stack]
import sys, os, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'w6'))
import numpy as np
from loadeng import load
import grammar as G, gext as X
NARR = int(sys.argv[1]) if len(sys.argv) > 1 else 6000; STACK = sys.argv[2] if len(sys.argv) > 2 else 's75'
HERE = os.path.dirname(os.path.abspath(__file__))
ns = load(STACK, 'full', ['kstar', 'edgekeys=' + os.path.join(HERE, 'edgekeys_test.txt')]); ns['l3q_load'](); ns['kt_load']()
KEYS = {k['name']: k for k in ns['EGKEYS']}
def pic(d, w, s):
    priv = []
    for j in range(d):
        pv = [G.ALL] * (w[j] - 5) if w[j] <= 9 else []
        if w[j] == 6:
            am = ns['amask'](min(d, 9), w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d])
            pv = [am & ~ns['f2bm'].extra6(d, w, s, j)]
        if w[j] == 7 and d == 7:
            for sg, slot in ((1, 1), (-1, 0)):
                c = w[(j + sg) % d]; ap, o = (s[j], s[(j - 1) % d]) if sg == 1 else (s[(j - 1) % d], s[j])
                if c <= 6 and ap <= 6:
                    pv[slot] = ns['L3T'][(sg, c, w[(j + 2 * sg) % d], w[(j + 3 * sg) % d], w[(j + 4 * sg) % d], ap, o)] & ~ns['f2bm'].extra7(d, w, s, j, sg)
        priv.append(pv)
    return G.build('R', 'r', d, list(w), [G.BIT[x] for x in s], priv)
def ctx_of(key, mirror=False, flip=None):
    cx = {}
    for p_, m_ in key['conds']:
        i_ = X.EPOS.index(p_)
        if mirror: i_ = X.EMIRROR[i_]
        if flip == p_: i_ = X.EPOS.index(p_.replace('+', '#').replace('-', '+').replace('#', '-'))
        cx[i_] = m_
    return cx
def gcols(T, key, cx, n):
    sure, poss = G.match(T, G.SYM['7'], key['vm'], cx)
    pay = np.bincount(T['rid'][T['out'] & sure], minlength=n); rec = np.bincount(T['rid'][(~T['out']) & poss], minlength=n)
    return pay, rec
rng = random.Random(7803); res = {}; allok = True
for d in (7, 8):
    arrs = []
    while len(arrs) < NARR:
        if len(arrs) % 2: w, s = ns['eg_force'](rng, d)
        else: w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
        if rng.random() < 0.5 or ns['admissible'](d, ''.join(map(str, w)), ''.join(map(str, s))) is None: arrs.append((w, s))
    items = [(rid, sl) for rid, (w, s) in enumerate(arrs) for sl in X.slots(pic(d, w, s)) if sl[0] == 'EDGE']
    T = G.SlotTable(items).G['EDGE']; n = len(arrs)
    for nm, key in KEYS.items():
        epay = np.array([ns['eg_payer_count'](key, w, s) if d == 7 else 0 for w, s in arrs])
        etot = np.array([ns['eg_terms'](d, w, s).get(('ks', nm), 0) for w, s in arrs]); erec = etot + epay
        gp, gr = gcols(T, key, ctx_of(key), n); mp, mr = gcols(T, key, ctx_of(key, mirror=True), n)
        flipc = [p_ for p_, _ in key['conds'] if '+' in p_][0] if any('+' in p_ for p_, _ in key['conds']) else key['conds'][0][0]
        wp, wr = gcols(T, key, ctx_of(key, flip=flipc), n)
        ok = (epay == gp).all() and (erec >= gr).all() and (gp == mp).all() and (gr == mr).all()
        live = bool(gp.any() or gr.any() or wp.any() or wr.any() or epay.any() or erec.any())
        ctl = bool((wp != epay).any() or (wr != gr).any()) if live else 'n/a (no slot of this key at d=%d)' % d
        allok &= ok and (ctl is not False)
        print('d=%d %s %s: payer slots on %d rows (engine == grammar SURE: %s), payee: grammar POSSIBLE on %d rows, engine bound >= grammar on all: %s, equal on %d/%d rows (bound > grammar on %d); mirror identical: %s; control (%s flipped) differs: %s'
              % (d, nm, key['spec'], int((epay > 0).sum()), bool((epay == gp).all()), int((gr > 0).sum()), bool((erec >= gr).all()), int((erec == gr).sum()), n, int((erec > gr).sum()),
                 bool((gp == mp).all() and (gr == mr).all()), flipc, ctl))
        if not ok:
            bad = np.nonzero((epay != gp) | (erec < gr))[0][:3]
            print('   e.g. %s' % [(''.join(map(str, arrs[i][0])), ''.join(map(str, arrs[i][1])), int(epay[i]), int(gp[i]), int(erec[i]), int(gr[i])) for i in bad])
        if nm == 'KG' and d == 7:
            kp = np.array([sum(ns['kstar_payer_slot'](w, s, i, e) for i in range(7) for e in (1, -1)) for w, s in arrs])
            kr = np.array([sum(ns['kstar_payee_slot'](w, s, i, e) for i in range(7) for e in (1, -1)) for w, s in arrs])
            okk = (kp == epay).all() and (erec >= kr).all(); allok &= okk
            print('   KG vs the K* family: payer identical %s; generic payee bound >= exact K* payee on all rows %s (equal on %d/%d)' % (bool((kp == epay).all()), bool((erec >= kr).all()), int((erec == kr).sum()), n))
print('EDGE-ORIENT-TEST: %s' % ('PASS' if allok else 'FAIL'))
