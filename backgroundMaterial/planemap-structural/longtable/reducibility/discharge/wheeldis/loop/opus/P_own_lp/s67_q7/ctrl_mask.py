# s67: engine's masked Q signatures (recv_coef_R2, q7 q7m) vs the independent mask function of s62_w5check/check62.py, on random d=7 arrangements.  usage: python3 ctrl_mask.py N <engine args>
import sys, os, random, collections
N = int(sys.argv[1]); ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng', 'pcheck.py'); sys.argv = [ENG, 'help'] + sys.argv[2:]
ns = {'__file__': ENG, '__name__': 'pcheck_s67m'}; exec(compile(open(ENG).read(), ENG, 'exec'), ns); ns['l3q_load']()
L3T, extra7, q7keys, qkey, canon, RBIG, recv, adm = ns['L3T'], ns['f2bm'].extra7, ns['q7keys'], ns['qkey'], ns['canon'], ns['RBIG'], ns['recv_coef_R2'], ns['admissible']
LET = (5, 6, 7, 8, 9); rnd = random.Random(11); n = nb = nslot = nmask = 0
def mask(w, s, j, sg):
    c = w[(j + sg) % 7]; ap, o = (s[j], s[(j - 1) % 7]) if sg == 1 else (s[(j - 1) % 7], s[j])
    if c > 6 or ap > 6: return None
    return L3T[(sg, c, w[(j + 2 * sg) % 7], w[(j + 3 * sg) % 7], w[(j + 4 * sg) % 7], ap, o)] & ~extra7(7, w, s, j, sg)
while n < N:
    w = [rnd.choice((5, 5, 6, 6, 7, 7, 8, 9)) for _ in range(7)]; s = [rnd.choice((5, 5, 6, 6, 7, 8, 9)) for _ in range(7)]
    if ns['admissible'](7, ''.join(map(str, w)), ''.join(map(str, s))) is not None: continue
    n += 1
    cf = recv(7, ''.join(map(str, w)), ''.join(map(str, s)), True, None)
    eng = collections.Counter({k[1]: v for k, v in cf.items() if k[0] == 'Q'})   # sig -> multiplicity (union of key sets compared as multiset of key-sets)
    engsets = collections.Counter()
    for sg, v in eng.items(): engsets[tuple(q7keys(sg))] += v
    mine = collections.Counter()
    for j in range(7):
        if w[j] != 7: continue
        P = []
        for sg in (1, -1):
            m = mask(w, s, j, sg); P.append([l for k, l in enumerate(LET) if m is None or (m >> k) & 1]); nmask += (m is not None and m != 31)
        a, b, c, e = w[(j + 1) % 7], s[j], s[(j - 1) % 7], w[(j - 1) % 7]
        ks = tuple(sorted({qkey((7, a, b, p1, p2, c, e)) for p1 in P[0] for p2 in P[1] if ''.join(map(str, canon((7, a, b, p1, p2, c, e)))) not in RBIG}))
        if ks: mine[ks] += 1; nslot += 1
    if mine != engsets: nb += 1; print('MISMATCH', w, s)
print('masked Q key sets: %d random d=7 arrangements, %d payer slots, %d slot-sides with a restricting mask, %d arrangements where the engine differs from the independent derivation' % (n, nslot, nmask, nb))
