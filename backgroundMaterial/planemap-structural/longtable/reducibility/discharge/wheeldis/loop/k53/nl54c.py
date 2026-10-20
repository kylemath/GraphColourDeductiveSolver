"""EXPLORE round 54c (coordinator 03:56Z, the user's literature point 1): shapes in the published 2026 set
(github.com/near-linear-4ct/reducible-configurations, MIT; round 51's kc lines, loop/k51/nl51_kc.txt).  For each
configuration: its 7s, whether two 7s are adjacent (7-7 edge), whether three 7s are pairwise adjacent (7-7-7
triangle), the size of its biggest connected cluster of 7s, and whether it has a 7-5-5 / 5-5-5 kite (a 7 next to a
face of three 5s: x a b and a b c faces, x = 7, a = b = c = 5; round 51's face_kite).  Prints counts by ring size and
writes nl54c_shapes.txt (one line per configuration with any of the shapes: name ring 7s cluster edge77 tri777 kite).
usage: python3 -I nl54c.py"""
import os, sys, collections
H = os.path.dirname(os.path.abspath(__file__)); LOOP = os.path.join(H, '..')
sys.path.insert(0, os.path.join(LOOP, 'k42'))
import grow

def shapes(c):
    nm, tag, U, g, E, tri = c
    sev = [u for u in U if g[u] == 7]
    e77 = any(v in sev for u in sev for v in E[u])
    t777 = any(all(g[x] == 7 for x in t) for t in tri)
    seen = set(); big = 0
    for s in sev:
        if s in seen: continue
        st = [s]; seen.add(s); n = 0
        while st:
            x = st.pop(); n += 1
            for y in E[x]:
                if g[y] == 7 and y not in seen: seen.add(y); st.append(y)
        big = max(big, n)
    kite = False
    for t in tri:
        for x in t:
            a, b = sorted(t - {x})
            if g[x] == 7 and g[a] == 5 and g[b] == 5 and any(g[y] == 5 for t2 in tri if {a, b} <= t2 for y in t2 - {a, b} if y != x):
                kite = True
    return len(sev), big, e77, t777, kite

if __name__ == '__main__':
    NL = [grow.kcline(l, 'NL') for l in open(os.path.join(LOOP, 'k51', 'nl51_kc.txt')) if l.strip()]
    ring = {c[0]: int(c[0].split('_r')[1]) for c in NL}
    rows = []; tab = collections.defaultdict(collections.Counter)
    for c in NL:
        n7, big, e77, t777, kite = shapes(c); r = ring[c[0]]
        tab['all'][r] += 1
        if n7: tab['has a 7'][r] += 1
        if e77: tab['7-7 edge'][r] += 1
        if t777: tab['7-7-7 triangle'][r] += 1
        if big >= 4: tab['cluster of >= 4 sevens'][r] += 1
        if kite: tab['7 next to a 5-5-5 face'][r] += 1
        if e77 and kite: tab['7-7 edge and the kite'][r] += 1
        if e77 or t777 or kite: rows.append('%s %d %d %d %d %d %d' % (c[0], r, n7, big, e77, t777, kite))
    R = sorted(tab['all'])
    print('%-26s %6s  ' % ('shape', 'total') + ' '.join('r%-4d' % r for r in R))
    for k in ('all', 'has a 7', '7-7 edge', '7-7-7 triangle', 'cluster of >= 4 sevens', '7 next to a 5-5-5 face', '7-7 edge and the kite'):
        print('%-26s %6d  ' % (k, sum(tab[k].values())) + ' '.join('%-5d' % tab[k][r] for r in R))
    open(os.path.join(H, 'nl54c_shapes.txt'), 'w').write('# name ring sevens biggest-7-cluster edge77 tri777 kite\n' + '\n'.join(rows) + '\n')
