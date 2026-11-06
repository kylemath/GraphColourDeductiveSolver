"""Round 47: per receiver and per sender context (a 5 at w_i whose link word is a cert_s9 sender), the two-engine
kills among the swept windows, and those that contain the sender wheel (u, w_i-1, w_i, w_i+1, s_i-1, s_i).
usage: python3 ctx47.py"""
import os, collections
H = os.path.dirname(os.path.abspath(__file__))
ROWS = [(7, '8655675', '5756585'), (8, '75576556', '78756665')]
SEND = {'55667', '56668', '55767', '58778'}
def canon(w):
    w = tuple(w); return min(min(s[k:] + s[:k] for k in range(len(s))) for s in (w, w[::-1]))
def verts(nm):
    _, l, s = nm.split('_')
    return ({('u',)} if l[0] == 'u' else set()) | {('w', j) for j, c in enumerate(l[1:]) if c in '5678'} | {('s', j) for j, c in enumerate(s) if c != '.'}
kill = {}
if os.path.exists(os.path.join(H, 'KILL')):
    for l in open(os.path.join(H, 'KILL')): kill.setdefault(l.split()[0], l.split()[1])
done = {l.split()[0] for l in open(os.path.join(H, 'A_kcc.out')) if l[:1] == 'a'} if os.path.exists(os.path.join(H, 'A_kcc.out')) else set()
for d, lk, sv in ROWS:
    win = {l.split()[0]: int(l.split()[1]) for l in open(os.path.join(H, 'win45_%d_%s_%s_A14.txt' % (d, lk, sv)))}
    run = [w for w in win if w in done]; k = [w for w in win if w in kill]
    print('%d %s/%s: windows run %d of %d, kills %d %s, smallest ring %s' % (d, lk, sv, len(run), len(win), len(k),
          dict(collections.Counter(kill[w] for w in k)), min((win[w] for w in k), default='-')))
    W = [int(x) for x in lk]; S = [int(x) for x in sv]
    for i in range(d):
        if W[i] != 5: continue
        cw = ''.join(map(str, canon((min(d, 9), W[(i + 1) % d], S[i], S[(i - 1) % d], W[(i - 1) % d]))))
        if cw not in SEND: continue
        wheel = {('u',), ('w', (i - 1) % d), ('w', i), ('w', (i + 1) % d), ('s', (i - 1) % d), ('s', i)}
        ww = [w for w in win if wheel <= verts(w)]; kk = [w for w in ww if w in kill]
        best = min(kk, key=lambda w: (win[w], w)) if kk else None
        print('   sender %s at w%d: wheel windows %d (run %d), kills %d, smallest %s' % (
            cw, i, len(ww), sum(1 for w in ww if w in done), len(kk), '%s ring %d %s' % (best, win[best], kill[best]) if best else '-'))
