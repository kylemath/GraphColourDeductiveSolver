# s62_w5check: independent re-pricing of the W5 claim (2).  usage: python3 check62.py <engine args as in run62.sh> [q7]
# Loads the s62 engine copy (patched f2bglue) and re-derives emissions / slots / masks / matching from the raw certificate JSON.
import sys, os, json, itertools, collections
from fractions import Fraction as F
ENG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eng', 'pcheck.py')
args = [a for a in sys.argv[1:]]
sys.argv = [ENG, 'help'] + args
ns = {'__file__': ENG, '__name__': 'pcheck_s62'}
exec(compile(open(ENG).read(), ENG, 'exec'), ns)
ns['l3q_load']()
q7sig, q7keys, qkey, RBIG, L3T, canon = ns['q7sig'], ns['q7keys'], ns['qkey'], ns['RBIG'], ns['L3T'], ns['canon']
extra7 = ns['f2bm'].extra7; q7_inflow = ns['q7_inflow']; recv = ns['recv_coef_R2']; l3q_terms = ns['l3q_terms']
LET = (5, 6, 7, 8, 9)
C = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs', 'certP2full_rat.json')))
R = [(r['row'][2], r['row'][3], F(r['w'])) for r in C if r['row'][0] == 'receiverR2']
rows = [([int(c) for c in l], [int(c) for c in s]) for l, s, _ in R]; names = ['%s/%s' % (l, s) for l, s, _ in R]
# --- (a) mask function vs the engine's own lQ keys in the rows (does my mask reproduce what the cert's lQ credits use?)
def mask(w, s, j, sg):
    n = 7; c = w[(j + sg) % n]; ap, o = (s[j], s[(j - 1) % n]) if sg == 1 else (s[(j - 1) % n], s[j])
    if c > 6 or ap > 6: return None
    m = L3T[(sg, c, w[(j + 2 * sg) % n], w[(j + 3 * sg) % n], w[(j + 4 * sg) % n], ap, o)]
    return m & ~extra7(7, w, s, j, sg)
bad = 0
for (w, s), nm in zip(rows, names):
    mine = collections.Counter()
    for j in range(7):
        if w[j] != 7: continue
        for sg in (1, -1):
            m = mask(w, s, j, sg)
            if m is not None:
                c = w[(j + sg) % 7]; ap = s[j] if sg == 1 else s[(j - 1) % 7]; mine[('lQ', (c, ap, m))] += 1
    eng = collections.Counter({k: v for k, v in l3q_terms(7, w, s).items() if k[0] == 'lQ' and v > 0})
    if mine != eng: bad += 1; print('MASK MISMATCH', nm, mine, eng)
print('(a) mask function vs engine lQ credit keys: %d of %d rows mismatch' % (bad, len(rows)))
# --- (b) emissions from the engine's own q7_inflow, per row
em = []   # (row, key)  one entry per unit
for r, (w, s) in enumerate(rows):
    for k, m in q7_inflow(w).items():
        for _ in range(m): em.append((r, k))
print('(b) emissions via engine q7_inflow: %d; first letters %s' % (len(em), collections.Counter(k[0] for _, k in em)))
# --- slots: (row, pos j) with w[j]==7 ; option sets lenient (engine q7keys) and masked
def slot_sig(w, s, j): return q7sig(7, w[(j + 1) % 7], s[j], s[(j - 1) % 7], w[(j - 1) % 7])
slots = [(r, j) for r, (w, s) in enumerate(rows) for j in range(7) if w[j] == 7]
def opts(r, j, masked):
    w, s = rows[r]; a, b, c, e = w[(j + 1) % 7], s[j], s[(j - 1) % 7], w[(j - 1) % 7]
    P1, P2 = LET, LET
    if masked:
        m1, m2 = mask(w, s, j, 1), mask(w, s, j, -1)
        P1 = [l for k, l in enumerate(LET) if m1 is None or (m1 >> k) & 1]; P2 = [l for k, l in enumerate(LET) if m2 is None or (m2 >> k) & 1]
    return {qkey((7, a, b, p1, p2, c, e)) for p1 in P1 for p2 in P2 if ''.join(map(str, canon((7, a, b, p1, p2, c, e)))) not in RBIG}
def maxmatch(masked):
    O = {sl: opts(sl[0], sl[1], masked) for sl in slots}
    # sanity: unmasked options == engine q7keys(sg)
    if not masked: assert all(O[sl] == set(q7keys(slot_sig(*rows[sl[0]], sl[1]))) for sl in slots)
    adj = [[sl for sl in slots if em[e][1] in O[sl]] for e in range(len(em))]
    mt = {}
    def aug(e, seen):
        for sl in adj[e]:
            if sl in seen: continue
            seen.add(sl)
            if sl not in mt or aug(mt[sl], seen): mt[sl] = e; return True
        return False
    for e in range(len(em)): aug(e, set())
    return adj, mt
res = {}
for masked in (False, True):
    adj, mt = maxmatch(masked); un = [e for e in range(len(em)) if e not in mt.values()]
    nocompat = [e for e in range(len(em)) if not adj[e]]
    print('(c) %s: emissions %d slots %d max matching %d; emissions with NO compatible slot: %s; unmatched in this matching: %s' % (
        'MASKED' if masked else 'unmasked(engine q7keys)', len(em), len(slots), len(mt),
        [(names[em[e][0]][:7], ''.join(map(str, em[e][1]))) for e in nocompat], [(names[em[e][0]][:7], ''.join(map(str, em[e][1]))) for e in un]))
    res[masked] = (adj, mt, nocompat)
    # all maximum matchings leave unmatched count = deficiency; also report which emissions are 'inessential'
# --- (d) write mrowQ-extended certificates from the two matchings (unmasked: 18 rows; masked: the matched rows only)
base = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs', 'certP2full_rat.json')))
for masked in (False, True):
    adj, mt, _ = res[masked]; C2 = list(base)
    for sl, e in sorted(mt.items()):
        r, j = sl; w, s = rows[r]
        C2.append({'w': '-10/207', 'row': ['mrowQ', list(slot_sig(w, s, j)), list(em[e][1])]})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certs', 'cert_s62_%s.json' % ('masked' if masked else 'unmasked'))
    json.dump(C2, open(out, 'w')); print('(d) wrote', out, len(C2), 'rows')
# --- (e) raw reduced cost of an unmatched key: q column total from the receiver rows = w * (-m) summed
tot = collections.Counter()
for (l, sv, w), (wr, sr) in zip(R, rows):
    for k, m in q7_inflow(wr).items(): tot[k] += w * (-m)
print('(e) raw q totals (receiver rows only): ', {''.join(map(str, k)): str(v) for k, v in tot.items()})
