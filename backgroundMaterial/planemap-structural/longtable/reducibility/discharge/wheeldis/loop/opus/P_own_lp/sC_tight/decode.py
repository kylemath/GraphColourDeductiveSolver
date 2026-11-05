# decode a solveR2/lowerR2 certificate (method of B1 decodeB1.py): |w| by row type, sender contexts and words, receiver motifs, top receivers, coupling.
# usage: python3 decode.py cert.json [top=N] [base=W7cert,b77cert]
import json, collections, sys
from fractions import Fraction as F
def W(e): return abs(F(e['w'])) if isinstance(e['w'], str) else abs(F(e['w']))
C = json.load(open(sys.argv[1])); TOP = int(dict(a.split('=') for a in sys.argv[2:] if '=' in a).get('top', '30'))
def canon(w):
    w = tuple(w); n = len(w); return min(min(s[k:] + s[:k] for k in range(n)) for s in (w, w[::-1]))
def canon_row(d, lk, sv):
    out = []
    for r in range(d):
        for refl in (False, True):
            W_ = [None] * d; S_ = [None] * d
            for i in range(d):
                j = (i + r) % d if not refl else (r - i) % d; W_[j] = lk[i]
                j = (i + r) % d if not refl else (r - i - 1) % d; S_[j] = sv[i]
            out.append((''.join(W_), ''.join(S_)))
    return min(out)
base = {}
for tag, fn in (('W7', '/mnt/project-files/swarm/round6/W7-lower-k95f/certs/cert_k95f_best_0.0256781.json'), ('b77', '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/runL_b77b/cert_unpatched_exact.json')):
    B = json.load(open(fn)); rec = [(W(e), e['row']) for e in B if e['row'][0] == 'receiverR2']; S = sum(w for w, _ in rec)
    for w, r in rec: base.setdefault((r[1],) + canon_row(r[1], r[2], r[3]), {})[tag] = float(w / S)
tot = sum(W(e) for e in C)
kinds = collections.defaultdict(F); kn = collections.Counter()
for e in C: kinds[e['row'][0]] += W(e); kn[e['row'][0]] += 1
print('cert %s: %d rows' % (sys.argv[1], len(C)))
print('rows and |w| mass by type (share of total |w|):')
for k in sorted(kinds, key=lambda k: -kinds[k]): print('  %-11s %5d rows  %.3f' % (k, kn[k], kinds[k] / tot))
send = [(W(e), e['row']) for e in C if e['row'][0] == 'senderR2']; S = sum(w for w, _ in send) or 1
recv = [(W(e), e['row']) for e in C if e['row'][0] == 'receiverR2']; R = sum(w for w, _ in recv) or 1
print('\nSENDER contexts (word, hat bits | six-private bits), share of sender mass, top 15:')
for w, r in sorted(send, key=lambda x: -x[0])[:15]: print('  %.3f  %s  %s' % (w / S, r[1], ''.join(map(str, r[2]))))
bw = collections.defaultdict(F)
for w, r in send: bw[r[1]] += w
print('SENDER words (share): ' + ', '.join('%s %.3f' % (k, v / S) for k, v in sorted(bw.items(), key=lambda x: -x[1])[:12]))
allzero = sum(w for w, r in send if all(b == 0 for b in r[2] if b != '|'))
print('sender mass in contexts with every hat small (bits all 0): %.3f' % (allzero / S))
def feats(d, w, s):
    f = []
    if any(w[i] == '5' and w[(i + 1) % d] == '5' and s[i] == '5' for i in range(d)): f.append('555-face')
    elif any(w[i] == '5' and w[(i + 1) % d] == '5' for i in range(d)): f.append('55-pair')
    n5 = w.count('5')
    if n5 == 0: f.append('relay(no 5)')
    elif set(w) <= {'5', '7'} and n5 >= 3 and not f: f.append('5-7 mesh')
    elif n5 == 1: f.append('lone-5')
    return ','.join(f) or 'mixed 5-6-7'
bf = collections.defaultdict(F); bfn = collections.Counter()
for w, r in recv: k = (r[1], feats(r[1], r[2], r[3])); bf[k] += w; bfn[k] += 1
print('\nRECEIVER motifs (d, feature): rows, share of receiver mass')
for k, v in sorted(bf.items(), key=lambda x: -x[1]): print('  d=%d %-14s %4d  %.3f' % (k[0], k[1], bfn[k], v / R))
big = sum(w for w, r in recv if any(c in '89' for c in r[2]))
print('receiver mass in rows with an 8 or 9 in the link: %.3f; with a 6 in the link: %.3f; no 6 in the link: %.3f' % (big / R, sum(w for w, r in recv if '6' in r[2]) / R, sum(w for w, r in recv if '6' not in r[2]) / R))
cpl = collections.defaultdict(F)
for w, r in recv:
    d, L, s = r[1], [int(c) for c in r[2]], [int(c) for c in r[3]]
    ws = set(''.join(map(str, canon((min(d, 9), L[(i + 1) % d], s[i], s[(i - 1) % d], L[(i - 1) % d])))) for i in range(d) if L[i] == 5)
    for x in ws: cpl[x] += w
print('COUPLING: receiver mass share of rows that hold a link five of word X: ' + ', '.join('%s %.3f' % (k, v / R) for k, v in sorted(cpl.items(), key=lambda x: -x[1])[:10]))
# receivers grouped by canonical class
cls = collections.defaultdict(F); rep = {}
for w, r in recv:
    k = (r[1],) + canon_row(r[1], r[2], r[3]); cls[k] += w; rep.setdefault(k, r)
print('\nRECEIVER rows, top %d (share of receiver mass, cumulative; base-cert shares W7 / b77 of the same class):' % TOP)
cum = F(0)
for k, w in sorted(cls.items(), key=lambda x: -x[1])[:TOP]:
    r = rep[k]; cum += w; b = base.get(k, {})
    print('  %.4f %.3f d=%d %s/%s  %-12s W7 %s b77 %s' % (w / R, cum / R, r[1], r[2], r[3], feats(r[1], r[2], r[3]), '%.3f' % b['W7'] if 'W7' in b else '-', '%.3f' % b['b77'] if 'b77' in b else '-'))
json.dump([[float(w / R), rep[k][1], rep[k][2], rep[k][3]] for k, w in sorted(cls.items(), key=lambda x: -x[1])], open(sys.argv[1].replace('.json', '_recv.json'), 'w'))
