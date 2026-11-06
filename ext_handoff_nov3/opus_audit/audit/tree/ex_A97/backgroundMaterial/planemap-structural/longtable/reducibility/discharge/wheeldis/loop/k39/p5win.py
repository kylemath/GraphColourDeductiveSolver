"""EXPLORE round 39: windows of R* with w5's private p5 at 7 (Opus's fourth floor arrangement: w6's sender row with
z-letters (w4, p5) = (7, 7)).  R = d7 link 5675765 s 6577575 at u; p5 = ('p', 5, 1), w5's second-ring neighbour
between s4 and s5.  Window = u + all seven link vertices + any subset of {s0, s2, s3, s5, s6} at R's letters + s1, s4
each absent or at a letter 6..8 + p5 = 7.  Covers every open filling (s1, s4 >= 6) it agrees with.
Output: dfast lines (ring order) and .cov.  usage: python3 p5win.py OUT RMAX"""
import sys, os, itertools, collections
HERE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT, RMAX = sys.argv[1], int(sys.argv[2])
src = open(os.path.join(HERE, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', '30']; G = {'__file__': os.path.join(HERE, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
sys.path.insert(0, os.path.join(HERE, 'loop', 'lemmaA')); _a = sys.argv; sys.argv = ['x']; import la; sys.argv = _a
d, lk, sv = 7, [5, 6, 7, 5, 7, 6, 5], [6, 5, 7, 7, 5, 7, 5]
OPEN = ['%d%d' % (a, b) for a in range(6, 10) for b in range(6, 10)]
lines, cov, rc = {}, collections.defaultdict(set), collections.Counter()
for a in [None, 6, 7, 8]:
    for b in [None, 6, 7, 8]:
        for k in range(6):
            for SS in itertools.combinations([0, 2, 3, 5, 6], k):
                r2 = {('s', j): sv[j] for j in SS}
                if a is not None: r2[('s', 1)] = a
                if b is not None: r2[('s', 4)] = b
                r2[('p', 5, 1)] = 7
                adj, name = G['build'](d, lk, r2)
                inv = {v: x for x, v in name.items()}
                I = [inv[('u',)]] + [inv[('w', j)] for j in range(d)] + [inv[x] for x in r2]
                deg = {inv[('u',)]: d}; deg.update({inv[('w', j)]: lk[j] for j in range(d)}); deg.update({inv[x]: v for x, v in r2.items()})
                c = G['extract'](adj, I, deg)
                if c is None or c[0] > RMAX: continue
                cb = '%d %d %s %s' % c; nm = 'q' + la.ckey(cb)[1:]
                cv = {f for f in OPEN if (a is None or int(f[0]) == a) and (b is None or int(f[1]) == b)}
                cov[nm] |= cv
                if nm not in lines: lines[nm] = (c[0], '%s %s' % (nm, cb)); rc[c[0]] += 1
rows = sorted(lines.items(), key=lambda x: (x[1][0], -len(cov[x[0]]), x[0]))
with open(OUT, 'w') as f:
    for nm, (r, line) in rows: f.write(line + '\n')
with open(OUT + '.cov', 'w') as f:
    for nm, (r, line) in rows: f.write('%s %d %s\n' % (nm, r, ' '.join(sorted(cov[nm]))))
print(len(rows), 'windows', sorted(rc.items()))
