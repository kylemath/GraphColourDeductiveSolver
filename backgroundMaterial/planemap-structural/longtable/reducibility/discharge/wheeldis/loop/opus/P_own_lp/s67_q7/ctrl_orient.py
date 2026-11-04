# s67 orientation control.  usage: python3 ctrl_orient.py OUTCERT <engine args incl. q7 q7m>
# Builds, with the s67 engine's own MASKED Q signatures, the W5 masked certificate: certP2full_rat (58 rows) + one mrowQ row (w = -10/207) per matched payer slot.
import sys, os, json, collections
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'eng', 'pcheck.py')
out = sys.argv[1]; sys.argv = [ENG, 'help'] + sys.argv[2:]
ns = {'__file__': ENG, '__name__': 'pcheck_s67o'}; exec(compile(open(ENG).read(), ENG, 'exec'), ns); ns['l3q_load']()
recv = ns['recv_coef_R2']; q7keys = ns['q7keys']; q7_inflow = ns['q7_inflow']
base = json.load(open(os.path.join(HERE, '..', 's62_w5check', 'certs', 'certP2full_rat.json')))
rows = [(r['row'][1], r['row'][2], r['row'][3]) for r in base if r['row'][0] == 'receiverR2']
em = []; slots = []
for ri, (d, lk, sv) in enumerate(rows):
    cf = recv(d, lk, sv, True, None)
    w = [int(c) for c in lk]
    for k, m in q7_inflow(w).items():
        for _ in range(m): em.append((ri, k))
    for k, v in cf.items():
        if k[0] == 'Q':
            for _ in range(int(v)): slots.append((ri, k[1]))
print('emissions %d, payer slots %d (masked sigs: %d)' % (len(em), len(slots), sum(1 for _, s in slots if len(s) == 7)))
mt = {}
def aug(e, seen):
    for si, (r, sg) in enumerate(slots):
        if em[e][1] in q7keys(sg) and si not in seen:
            seen.add(si)
            if si not in mt or aug(mt[si], seen): mt[si] = e; return True
    return False
for e in range(len(em)): aug(e, set())
un = [e for e in range(len(em)) if e not in mt.values()]
print('max matching %d of %d; unmatched keys: %s' % (len(mt), len(em), sorted(''.join(map(str, em[e][1])) for e in un)))
C2 = list(base)
for si, e in sorted(mt.items()): C2.append({'w': '-10/207', 'row': ['mrowQ', list(slots[si][1]), list(em[e][1])]})
json.dump(C2, open(out, 'w')); print('wrote', out, len(C2))
