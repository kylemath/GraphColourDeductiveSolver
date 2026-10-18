"""Lower side of a Rule-T (option B) certificate (Opus P_own_lp cert_*.json), rebuilt with Studio's wlp3xt rows.
Row types in the certificate:
- ['senderT', word, bits]: Studio's sender row for word with the far-vertex bigness bits (edges with {6, big}, in
  increasing edge order);
- ['mrow', b, [root, f_a, f_e, side]]: T[key] - M_b <= 0, an auxiliary max-inflow variable per big letter b (the five
  at s_j is rooted at b). This is equivalent to Studio's lazily generated completion rows: the key must be one of
  Studio's inflow completions for b (INS);
- ['receiverT', d, link, s]: Studio's receiver row (Y with flags, L2 transfer types), with each inflow slot (s_j = 5
  between a 6 and a big b) carrying + M_b; the arrangement must pass sep3xt `c` on the same registry.
Also checks that every key in the solution JSON is canonical under Studio's ykey/tkey (no merge or double count).
The exact combination must leave every y/T/x/M coefficient >= 0, with t coefficient -1; then t >= -rhs.
Usage: WLP3X_DEF=1 WLP_SEPF=1 python3 lowercheckt.py CERT.json SOL.json <args>"""
import sys, os, json, collections
from fractions import Fraction as Fr
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
CERT = json.load(open(sys.argv[1])); SOL = json.load(open(sys.argv[2]))
src = open(os.path.join(HERE, 'wlp3xt.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3xt.py')), 1)
src = src[:src.index('# warm start: receiver rows')]
sys.argv = ['wlp3xt', 'maxit=0'] + sys.argv[3:]
exec(src)
# key canonicity
bad_y = [k for k in SOL['yT'] if ykey(tuple(int(c) for c in k.split('|')[0]), int(k.split('|')[1][0]), int(k.split('|')[1][1])) !=
         (tuple(int(c) for c in k.split('|')[0]), int(k.split('|')[1][0]), int(k.split('|')[1][1]))]
bad_t = [k for k in SOL['tau'] if tkey(tuple(int(c) for c in k.split('|')[0]), int(k.split('|')[1][0]), int(k.split('|')[1][1]), k.split('|')[1][2]) !=
         (tuple(int(c) for c in k.split('|')[0]), int(k.split('|')[1][0]), int(k.split('|')[1][1]), k.split('|')[1][2])]
print('solution keys: %d Y, %d T; not canonical under Studio ykey/tkey: %d Y, %d T %s' % (len(SOL['yT']), len(SOL['tau']), len(bad_y), len(bad_t), (bad_y + bad_t)[:5]))
srow = {}
for k, inf in enumerate(rinfo):
    if inf[0] == 'sender': srow[inf[1]] = rows[k]
comb = collections.defaultdict(Fr); rhs_ = Fr(0); ok = True
for e in CERT:
    w = Fr(e['w']).limit_denominator(10**6); row = e['row']
    if row[0] == 'senderT':
        lab = row[1] + ('/' + ''.join(map(str, row[2])) if row[2] else '')
        if lab not in srow: print('NOT A SENDER ROW', row); ok = False; continue
        r = dict(srow[lab]); b = Fr(-1)
    elif row[0] == 'mrow':
        bl, (rt, fa, fe, sd) = row[1], row[2]
        key = tkey(tuple(rt), fa, fe, sd)
        if key != (tuple(rt), fa, fe, sd): print('mrow key not canonical', row); ok = False
        if key not in TI or TI[key] not in INS[(bl, 7)]: print('mrow key is not an inflow completion for b=%d' % bl, row); ok = False; continue
        r = {('tau', TI[key]): 1.0, ('M', bl): -1.0}; b = Fr(0)
    else:
        d, lk, sv = row[1], row[2], row[3]
        allowed = check(d, lk, sv); ok &= allowed
        print('receiverT d=%d %s %s: sep3xt c says %s' % (d, lk, sv, 'ALLOWED' if allowed else 'FORBIDDEN'))
        r = dict(recv_row(d, lk, sv, {7: -1, 8: -1, 9: -1}))
        w_ = [int(c) for c in lk]; s_ = [int(c) for c in sv]
        for i in range(d):
            a_, b_ = w_[i], w_[(i + 1) % d]
            if s_[i] == 5 and min(a_, b_) == 6 and max(a_, b_) >= 7: r[('M', max(a_, b_))] = r.get(('M', max(a_, b_)), 0.0) + 1.0
        b = Fr(d - 6)
    for k, v in r.items(): comb[k] += w * Fr(v).limit_denominator(10**6)
    rhs_ += w * b
neg = {k: v for k, v in comb.items() if k != ('t',) and v < 0}
print('combination: %d rows; t coefficient %s, rhs %s, nonzero terms %d, negative terms %d %s' % (
    len(CERT), comb[('t',)], rhs_, sum(1 for k, v in comb.items() if k != ('t',) and v != 0), len(neg), list(neg.items())[:6]))
print('LOWER BOUND VALID: t >= %s' % (-rhs_) if comb[('t',)] == -1 and not neg and ok else 'LOWER BOUND NOT ESTABLISHED')
SEPX.stdin.close()
