"""Lower side of Opus's t* = 1/4 (P_own_lp/cert_s2x.json): rebuild the certificate's rows with Studio's own code
(wlp3x's sender rows and recv_row with L2 transfer types), check that each row is one our LP generates (sender word
is a non-R sender; the receiver arrangement passes sep3xf `c` on the same registry), and that the weighted combination
proves t >= 1/4: all y and x coefficients >= 0 after combination, t coefficient -1, right-hand side -1/4.
Usage: WLP3X_DEF=1 WLP_SEPF=1 python3 lowercheck.py CERT.json <args>"""
import sys, os, json, collections
from fractions import Fraction as Fr
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
CERT = json.load(open(sys.argv[1]))
src = open(os.path.join(HERE, 'wlp3x.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3x.py')), 1)
src = src[:src.index('# warm start: receiver rows')]
sys.argv = ['wlp3x'] + sys.argv[2:]
exec(src)
comb = collections.defaultdict(Fr); rhs_ = Fr(0); ok = True
sendrow = {''.join(map(str, inf[1])) if not isinstance(inf[1], str) else inf[1]: rows[k] for k, inf in enumerate(rinfo) if inf[0] == 'sender'}
for e in CERT:
    w = Fr(e['w']).limit_denominator(10**6); row = e['row']
    if row[0] == 'sender':
        if row[1] not in sendrow: print('NOT A SENDER ROW', row); ok = False; continue
        r = sendrow[row[1]]; b = Fr(-1)
    else:
        d, lk, sv = row[1], row[2], row[3]
        allowed = check(d, lk, sv)
        print('receiver d=%d %s %s: sep3xf c says %s' % (d, lk, sv, 'ALLOWED' if allowed else 'FORBIDDEN'))
        ok &= allowed
        r = recv_row(d, lk, sv); b = Fr(d - 6)
    for k, v in r.items(): comb[k] += w * Fr(v).limit_denominator(10**6)
    rhs_ += w * b
neg = {k: v for k, v in comb.items() if k != ('t',) and v < 0}
print('combination: t coefficient %s, rhs %s, nonzero y/x terms %d, negative terms %d %s' % (
    comb[('t',)], rhs_, sum(1 for k, v in comb.items() if k != ('t',) and v != 0), len(neg), list(neg.items())[:5]))
if comb[('t',)] == -1 and not neg and ok: print('LOWER BOUND VALID: t >= %s' % (-rhs_))
else: print('LOWER BOUND NOT ESTABLISHED')
SEPX.stdin.close()
