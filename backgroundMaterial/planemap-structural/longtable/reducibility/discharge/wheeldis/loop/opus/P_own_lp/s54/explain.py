# s54 explain.py SOL [tol]: the nonzero thetas of a parametric sol in words, with small-denominator approximations.
import sys, json, collections
from fractions import Fraction
S = json.load(open(sys.argv[1])); tol = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-9
L = {5: '5', 6: '6', 7: '7', 8: '8', 9: '9+'}
def cl(c): return {0: 'small', 1: 'big', 5: 'small', 7: 'big'}.get(c, str(c))
def fr(v): q = Fraction(v).limit_denominator(240); return '%s (%.6f)' % (q, v) if abs(float(q) - v) < 1e-7 else '%.6f' % v
def say(fam, f):
    MT = ('D', 'addD', 'pairD', 'full', 'const', 'add', 'pair', 'FT', 'side', 'sideFT', 'type', 'nf', 'cnt', 'cntD')
    g = f[1:] if (isinstance(f[0], str) and f[0] in MT and len(f) > 1 and isinstance(f[1], str)) else f   # strip a dict model tag
    k = g[0]; a = g[1:]
    if fam == 'y':
        pre = 'five -> big' if k in ('c', 'K') else None
        if k == 'c': return 'five -> each big neighbour: base'
        if k == 'D': return 'five -> big of degree %s: base' % L[a[0]]
        if k == 'K': return 'five -> big %s with link (from the big) %s' % (L[a[0]], ' '.join(L[x] for x in a[1:]))
        n = {'F': 1, 'N': 1, 'L': 1, 'FN': 2, 'NN': 2, 'FF': 2}[k]; D = 'big %s' % L[a[0]] if len(a) > n else 'any big'
        v = a[-n:]
        txt = {'F': 'per flank (common nbr of the five and the big) = %s', 'N': 'per far nbr (five nbr not adjacent to the big) = %s',
               'L': 'per other nbr = %s', 'FN': 'per flank %s next to far nbr %s', 'NN': 'if the far pair is {%s, %s}', 'FF': 'if the flank pair is {%s, %s}'}[k]
        return 'five -> %s: + %s' % (D, txt % tuple(L[x] for x in v))
    if fam == 'g':
        if k == 'c': return 'five -> 6: base'
        if k == 'S': return 'five -> 6: + per spoke (common nbr of the five and the 6) = %s' % L[a[0]]
        if k == 'H': return 'five -> 6: + per hat = %s' % cl(a[0])
        if k == 'F': return 'five -> 6: + if the fan is %s' % cl(a[0])
        if k == 'A': return 'five -> 6: + per apex = %s' % cl(a[0])
        if k == 'AS': return 'five -> 6: + per apex %s beside spoke %s' % (cl(a[0]), L[a[1]])
        if k == 'SH': return 'five -> 6: + per spoke %s beside hat %s' % (L[a[0]], cl(a[1]))
        if k == 'HF': return 'five -> 6: + per hat %s beside fan %s' % (cl(a[0]), cl(a[1]))
        if k == 'SS': return 'five -> 6: + if the spokes are {%s, %s}' % (L[a[0]], L[a[1]])
        if k == 'K': return 'five -> 6, key %s' % (a,)
    if fam == 'h':
        if k == 'c': return '6 -> each big neighbour: base'
        if k == 'D' and len(a) == 1: return '6 -> big %s: base' % L[a[0]]
        if k == 'D': return '6 -> big %s: + if the 6 has %d fives' % (L[a[0]], a[1])
        nm = {'S': 'first link nbr (common nbr of the 6 and the big)', 'T': 'second link nbr', 'O': 'opposite nbr', 'A': 'apex at the big'}
        if k in nm: return '6 -> %s: + per %s = %s' % ('big %s' % L[a[0]] if len(a) == 2 else 'any big', nm[k], (cl if k == 'A' else L.get)(a[-1]))
        if k == 'AS': return '6 -> big: + per apex %s beside first link nbr %s' % (cl(a[0]), L[a[1]])
        if k == 'ST': return '6 -> big: + per first link nbr %s followed by second nbr %s' % (L[a[0]], L[a[1]])
        if k == 'TO': return '6 -> big: + per second link nbr %s followed by opposite %s' % (L[a[0]], L[a[1]])
        if k == 'K': return '6 -> big, key %s' % (a,)
    if fam == 'x':
        if k == 'c': return 'big -> adjacent big: base'
        if k == 'FT': return 'big %s -> big %s: base' % (L[a[0]], L[a[1]])
        if k in ('C', 'A', 'B'): return 'big -> big: + per side whose %s = %s' % ({'C': 'common nbr', 'A': 'sender-side nbr', 'B': 'receiver-side nbr'}[k], L[a[0]])
        if k == 's' and len(a) == 3: return 'big -> big: + per side (common nbr %s, its other nbr on the sender side %s, on the receiver side %s)' % tuple(L[x] for x in a)
        if k == 's': return 'big %s -> big %s: + per side (common nbr %s, sender side %s, receiver side %s)' % tuple(L[x] for x in a)
        if k == 'K': return 'big -> big, tau %s' % (a,)
    if fam == 'r':
        if k == 'c': return 'big hat -> five: base'
        if k == 'T': return 'big hat -> five: by the two shared spokes %s / %s' % (L[a[0]], L[a[1]])
        if k == 's': return 'big hat -> five: + per shared-spoke side %s' % (a,)
        if k == 'K': return 'big hat -> five, key %s' % (a,)
    if fam == 'lq':
        if k == 'c': return 'l3q payer, key length %d: base' % a[0]
        if k == 'K': return 'l3q key %s' % (a,)
    return '%s %s' % (fam, f)
by = collections.defaultdict(list)
for fam, f, v in S['theta']:
    if abs(v) > tol: by[fam].append((eval(f), v))
print('t = %.12f   pm %s   nonzero thetas %d' % (S['t'], S.get('pm'), sum(len(v) for v in by.values())))
for fam in ('y', 'g', 'h', 'x', 'r', 'lq'):
    for f, v in sorted(by.get(fam, []), key=lambda z: str(z[0])): print('  %-3s %-14s %s' % (fam, fr(v), say(fam, f)))
