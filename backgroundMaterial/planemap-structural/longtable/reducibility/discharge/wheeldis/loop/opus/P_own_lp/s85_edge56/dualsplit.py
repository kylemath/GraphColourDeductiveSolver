# s85: split an LP dual (cert json: [{'w', 'row'}]) by row type; d = 7 receivers by whether the link / apex ring has a letter >= 8; top rows.
# usage: python3 -I dualsplit.py <cert.json> [topN]
import sys, json, collections
from fractions import Fraction
fw = lambda x: float(Fraction(x)) if isinstance(x, str) else float(x)
C = json.load(open(sys.argv[1])); N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
tot = collections.Counter(); cnt = collections.Counter(); d7 = collections.Counter(); d7n = collections.Counter()
def lab(r):
    k = r[0]
    if k == 'receiverR2': return 'R%d %s/%s' % (int(r[1]), r[2], r[3])
    if k == 'senderR2': return 'S %s %s' % (r[1], ''.join(map(str, r[2])) if isinstance(r[2], list) else r[2])
    if k == 'cons2': return 'C %s/%s' % (''.join(map(str, r[1])), ''.join(map(str, r[2])))
    return ' '.join(map(str, r))[:120]
for c in C:
    r = c['row']; w = abs(fw(c['w'])); k = r[0]
    key = 'receiver d=%d' % int(r[1]) if k == 'receiverR2' else k
    tot[key] += w; cnt[key] += 1
    if k == 'receiverR2' and int(r[1]) == 7:
        big_l = any(int(ch) >= 8 for ch in r[2]); big_s = any(int(ch) >= 8 for ch in r[3])
        cls = 'link has 8+' if big_l else ('apex ring has 8+ (link 5/6/7 only)' if big_s else '5/6/7 only (link and apex ring)')
        d7[cls] += w; d7n[cls] += 1
T = sum(tot.values())
print('dual rows %d, total |w| %.6f' % (len(C), T))
for k, v in sorted(tot.items(), key=lambda x: -x[1]): print('  %-28s %8d rows  |w| %.6f  (%.1f%%)' % (k, cnt[k], v, 100 * v / T))
print('d = 7 receivers:')
for k, v in sorted(d7.items(), key=lambda x: -x[1]): print('  %-40s %8d rows  |w| %.6f' % (k, d7n[k], v))
print('top %d rows by |w|:' % N)
for c in sorted(C, key=lambda c: -abs(fw(c['w'])))[:N]: print('  %+.6f  %s' % (fw(c['w']), lab(c['row'])))
