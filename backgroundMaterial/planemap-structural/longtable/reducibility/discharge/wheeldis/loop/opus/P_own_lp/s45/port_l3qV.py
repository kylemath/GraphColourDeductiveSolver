"""s45: patch s45/eng/prelay2.py (a copy of s44/eng) with the l3qV option (RELAY_SPEC_s45).  Run once on the fresh copy.
Default l3qV=7: every changed function returns exactly what it did before (new code only runs when 8 or 9 is in l3qV)."""
import sys
fn = sys.argv[1]; src = open(fn).read()
def rep(old, new):
    global src
    assert src.count(old) == 1, old[:80]
    src = src.replace(old, new)
# 1. option, V-tables, refusal of solve/upper
rep("""LQCAP = float(OPT.get('lqcap', '3')); L3T = {}; L3FILE = [None]
""", """LQCAP = float(OPT.get('lqcap', '3')); L3T = {}; L3FILE = [None]
LQVS = tuple(sorted({int(x) for x in OPT.get('l3qV', '7').split(',')}))   # s45 (RELAY_SPEC_s45): payee letters; default 7 = s44
assert 7 in LQVS and set(LQVS) <= {7, 8, 9}, LQVS
LQVX = tuple(V for V in LQVS if V >= 8) if L3Q else ()                    # the new payee letters (empty by default)
L3TV = {}
def l3q_loadV(V):
    if V not in L3TV:
        T = {}
        for fn in OPT['l3qtab%d' % V].split(','):
            for k, v in json.load(open(fn)).items():
                sg, wd, ao = k.split(); T[(int(sg),) + tuple(int(ch) for ch in wd) + tuple(int(ch) for ch in ao)] = v[0]
        if 'l3qpartial' not in FLAGS: assert len(T) == 2 * 2500, (V, len(T))
        L3TV[V] = T; log('l3qV: V = %d table %d masks (%s)' % (V, len(T), 'partial' if len(T) != 5000 else 'full'))
    return L3TV[V]
if LQVX and CMD in ('solveR2', 'upperR2'):
    log('l3qV=%s: separation / upper check for V >= 8 not built (RELAY_SPEC_s45 45.5); refusing %s' % (OPT['l3qV'], CMD)); sys.exit(7)
""")
# 2. row terms
rep("""                m = L3T[(sg, c, a, a2, w[(i + 4 * sg) % n], ap, o)]
                cf[('lQ', (c, ap, m))] += 1
    return cf
""", """                m = L3T[(sg, c, a, a2, w[(i + 4 * sg) % n], ap, o)]
                cf[('lQ', (c, ap, m))] += 1
    if LQVX:   # s45: the d = 7 centre also pays its link 8s / 9s, key (V, c, a, a2)
        for i in range(n):
            if w[i] not in LQVX: continue
            for sg in (1, -1):
                c, a, a2 = w[(i + sg) % n], w[(i + 2 * sg) % n], w[(i + 3 * sg) % n]
                if c <= 6 and a <= 6: cf[('lq', (w[i], c, a, a2))] -= 1
    return cf
def l3q_terms_payeeV(d, w, s):
    \"\"\"RELAY_SPEC_s45 45.2: a centre with V = min(d, 9) in l3qV, V >= 8, credits +1 lQ (V, c, a', mask) at every link 7, both sides\"\"\"
    cf = collections.Counter(); V = min(d, 9)
    if V not in LQVX: return cf
    T = l3q_loadV(V); n = d
    for i in range(n):
        if w[i] != 7: continue
        for sg in (1, -1):
            c, w2, w3, w4 = (w[(i + k * sg) % n] for k in (1, 2, 3, 4))
            ap, o = (s[i], s[(i - 1) % n]) if sg == 1 else (s[(i - 1) % n], s[i])
            if c <= 6 and ap <= 6: cf[('lQ', (V, c, ap, T[(sg, c, w2, w3, w4, ap, o)]))] += 1
    return cf
""")
rep("""    if L3Q: cf.update(l3q_terms(d, w, s))
""", """    if L3Q: cf.update(l3q_terms(d, w, s))
    if LQVX: cf.update(l3q_terms_payeeV(d, w, s))
""")
# 3. mrowL generation (solve path; unreachable while solveR2 refuses, kept consistent)
rep("""                lsig.add(k[1]); c_, a_, m_ = k[1]
                for a2 in l3q_mask_letters(m_): addrow({('lq', (c_, a_, a2)): 1.0, ('lQ', k[1]): -1.0}, -inf, 0.0, ('mrowL', list(k[1]), [c_, a_, a2]))
""", """                lsig.add(k[1]); c_, a_, m_ = k[1][-3:]; V_ = k[1][:-3]
                for a2 in l3q_mask_letters(m_): addrow({('lq', V_ + (c_, a_, a2)): 1.0, ('lQ', k[1]): -1.0}, -inf, 0.0, ('mrowL', list(k[1]), list(V_ + (c_, a_, a2))))
""")
# 4. lowerR2 mrowL check
rep("""            if not L3Q or len(sg) != 3 or sg[0] > 6 or sg[1] > 6 or k[:2] != sg[:2] or k[2] not in l3q_mask_letters(sg[2]): log('  BAD MROWL', row); ok = False; continue
""", """            if len(sg) == 4 and sg[0] in LQVX and len(k) == 4 and k[0] == sg[0]: sg_, k_ = sg[1:], k[1:]   # s45: V >= 8 label
            else: sg_, k_ = sg, k
            if not L3Q or len(sg_) != 3 or sg_[0] > 6 or sg_[1] > 6 or k_[:2] != sg_[:2] or k_[2] not in l3q_mask_letters(sg_[2]): log('  BAD MROWL', row); ok = False; continue
""")
open(fn, 'w').write(src); print('patched', fn)
