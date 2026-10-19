# usage: python3 binders.py CERT [FORBIDFILE]  -> receiver binders, classified (face-7 / d10 / other), canonical form
import json, sys
def canon_arr(lk, sv):
    w = lk; s = sv; d = len(w); best = None
    for k in range(d):
        for refl in (False, True):
            if not refl: c = (''.join(w[(i + k) % d] for i in range(d)), ''.join(s[(i + k) % d] for i in range(d)))
            else: c = (''.join(w[(k - i) % d] for i in range(d)), ''.join(s[(k - i - 1) % d] for i in range(d)))
            if best is None or c < best: best = c
    return best
def faces(lk, sv):
    d = len(lk); return [i for i in range(d) if lk[i] == '5' and lk[(i + 1) % d] == '5' and sv[i] == '5']
def shape(d, lk, sv):
    if d == 10: return 'd10' + ('(5-5-5 face)' if faces(lk, sv) else '')
    if faces(lk, sv): return 'face-%d' % d
    return 'other-d%d' % d
C = json.load(open(sys.argv[1]))
F = set()
if len(sys.argv) > 2:
    for line in open(sys.argv[2]):
        f = line.split('#')[0].split()
        if f: F.add((int(f[0]),) + canon_arr(f[1], f[2]))
rec = [(c['w'], c['row']) for c in C if c['row'][0] == 'receiverR2']
snd = [(c['w'], c['row']) for c in C if c['row'][0] == 'senderR2']
print('receivers %d, senders %d, total dual on receivers %.6f' % (len(rec), len(snd), -sum(w for w, _ in rec)))
for w, r in sorted(rec):
    d, lk, sv = r[1], r[2], r[3]; cn = canon_arr(lk, sv)
    print('  %.6f d=%d %s/%s  canon %s/%s  %s faces@%s %s' % (-w, d, lk, sv, cn[0], cn[1], shape(d, lk, sv), faces(lk, sv), 'ALREADY-FORBIDDEN?!' if (d,) + cn in F else ''))
