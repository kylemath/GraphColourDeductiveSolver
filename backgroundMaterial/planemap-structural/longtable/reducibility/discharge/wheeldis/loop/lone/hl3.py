"""EXPLORE round 8 (exploratory): probe of H-L3 ("the remaining lone-five arrangements cannot be killed from distance-2
data").  Geometry: for a lone five w_i, x = s_i (letter 6) has neighbours w_i, w_i+1, s_i-1 (when w_i has degree 5),
p = the second-ring neighbour of w_i+1 between s_i and s_i+1 when w_i+1 has degree 6 (gen.py name ('p', i+1, 1);
distance 2 from u, NOT fixed by the (w, s) letters), and third-ring vertices.  Symmetrically for x = s_i-1 with w_i-1.
For each lone five i, each such (x, p) and each S (a set of lone fives containing i, |S| <= 3), the configuration is
the B-fixed one (u + S + N(S) at exact degree) plus p at exact degree delta in {5, 6, 7, 8}.
Prints the geometry check, writes OUT (dfast lines with ring <= RMAX, deduplicated by canonical key) and OUT.map
(name -> arrangement, i, x, S, delta).
Usage: python3 loop/lone/hl3.py OUT RMAX 'd link s' ['d link s' ...]"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOUT, HRMAX, HARRS = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
src = open(os.path.join(HERE, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', '30']; __file__ = os.path.join(HERE, 'gen28.py'); exec(src)
sys.path.insert(0, os.path.join(HERE, 'loop', 'lemmaA')); _a = sys.argv; sys.argv = ['x']; import la; sys.argv = _a
lone = lambda d, lk, sv, i: lk[i] == '5' and lk[(i - 1) % d] in '56' and lk[(i + 1) % d] in '56' and sv[i] in '56' and sv[(i - 1) % d] in '56'
lines = {}; mp = []; rc = collections.Counter(); geo = 0
for a in HARRS:
    d, lk, sv = a.split(); d = int(d)
    Lp = [i for i in range(d) if lone(d, lk, sv, i)]
    for i in Lp:
        xs = []
        if sv[i] == '6' and lk[(i + 1) % d] == '6': xs.append((('s', i), ('p', (i + 1) % d, 1)))
        if sv[(i - 1) % d] == '6' and lk[(i - 1) % d] == '6': xs.append((('s', (i - 1) % d), ('p', (i - 1) % d, 1)))
        for xname, pname in xs:
            for k in (1, 2, 3):
                for S in itertools.combinations(Lp, k):
                    if i not in S: continue
                    wl = {(j + e) % d for j in S for e in (-1, 0, 1)}; sl = {(j + e) % d for j in S for e in (-1, 0)}
                    for delta in (5, 6, 7, 8):
                        link = [int(lk[j]) if j in wl else 9 for j in range(d)]
                        r2 = {('s', j): int(sv[j]) for j in sl}; r2[pname] = delta
                        adj, name = build(d, link, r2)
                        inv = {v: x for x, v in name.items()}
                        if geo < 2 and delta == 6 and k == 1:   # geometry check: neighbours of x, by name
                            X = inv[xname]; print('arr %s i=%d x=%s nbrs:' % (a, i, xname), sorted(str(name.get(y, '3rd ring')) for y in adj[X])); geo += 1
                        I = [inv[('u',)]] + [inv[('w', j)] for j in wl] + [inv[('s', j)] for j in sl] + [inv[pname]]
                        deg = {inv[('u',)]: d}; deg.update({inv[('w', j)]: int(lk[j]) for j in wl})
                        deg.update({inv[('s', j)]: int(sv[j]) for j in sl}); deg[inv[pname]] = delta
                        c = extract(adj, I, deg)
                        if c is None or c[0] > HRMAX: continue
                        cb = '%d %d %s %s' % c; kb = la.ckey(cb)
                        nm = 'h%s' % kb[1:]
                        mp.append('%s %s i=%d x=%s S=%s p=%d r=%d' % (nm, a.replace(' ', '/'), i, xname[1], S, delta, c[0]))
                        if nm not in lines: lines[nm] = '%s %s' % (nm, cb); rc[(delta, c[0])] += 1
open(HOUT, 'w').write(''.join(l + '\n' for l in sorted(lines.values(), key=lambda x: (int(x.split()[1]), x))))
open(HOUT + '.map', 'w').write('\n'.join(mp) + '\n')
print('configurations', len(lines), 'by (p degree, ring):', sorted(rc.items()))
