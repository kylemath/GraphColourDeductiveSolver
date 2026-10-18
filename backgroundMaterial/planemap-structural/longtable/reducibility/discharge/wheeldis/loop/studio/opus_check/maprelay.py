"""Map an Opus relay solution's g/h keys onto wlp3r6's y56/y6b keys, by key only (no Opus code read).
h: 6-tuples [b, ...] rooted at a big b -> wlp3r6 y6b key root(Lw, j) over the non-R6 six link words W6.
g: 5-tuples -> wlp3r6 y56 keys root([6, wn, sc, sp, wp], 0) over sender fives (reported as-is; flag-bit keys have no
wlp3r6 counterpart). Usage: python3 maprelay.py SOL.json <args>"""
import sys, os, json, itertools, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SOL = json.load(open(sys.argv[1]))
src = open(os.path.join(HERE, 'wlp3.py')).read().replace('os.path.abspath(__file__)', repr(os.path.join(HERE, 'wlp3.py')), 1)
sys.argv = ['wlp3'] + sys.argv[2:]
exec(src[:src.index('A_ub, b_ub = [], []')])
SEP.stdin.close(); SEP.wait()
R56 = sorted({root(list(w), j) for w in senders for j in range(5) if w[j] == 6})
def canon6(w):
    w = tuple(w); return min(min(s_[k:] + s_[:k] for k in range(6)) for s_ in (w, w[::-1]))
W6 = sorted({canon6(w) for w in itertools.product(L, repeat=6) if not isR6(list(w))})
R6B = set(root(list(w), j) for w in W6 for j in range(6) if w[j] >= 7)
print('wlp3r6: %d y56 keys, %d y6b keys' % (len(R56), len(R6B)))
hk = [tuple(k) for k, v in SOL['h']]; hv = {tuple(k): v for k, v in SOL['h']}
direct = [k for k in hk if k in R6B]
viaroot = [k for k in hk if k not in R6B and tuple(root(list(k), 0)) in R6B]
rootkeys = collections.Counter(tuple(root(list(k), 0)) for k in hk)
isr6 = [k for k in hk if isR6(list(k))]
print('h: %d keys; %d are wlp3r6 y6b keys as written, %d more after wlp3r6 root(); %d unmapped; %d are R6 words'
      % (len(hk), len(direct), len(viaroot), len(hk) - len(direct) - len(viaroot), len(isr6)))
print('h -> y6b collisions (several h keys on one y6b key): %d y6b keys hit by >1 h key' % sum(1 for c in rootkeys.values() if c > 1))
gk = [tuple(k) for k, v in SOL['g']]
g56 = [k for k in gk if k in set(map(tuple, R56))]
print('g: %d keys, %d are wlp3r6 y56 keys; key shape (letter, 3 flag bits, letter), first letters %s, last letters %s'
      % (len(gk), len(g56), sorted(set(k[0] for k in gk)), sorted(set(k[-1] for k in gk))))
print('y: %d keys, %d not wlp3r6 y roots' % (len(SOL['y']), sum(1 for k in SOL['y'] if (int(k.split('|')[0]),) + tuple(int(c) for c in k.split('|')[1]) not in ix)))
