"""EXPLORE round 37 (09:47Z): windows of w2's worst frames (round 36).  Centre w2, degree 7, link 7665575
(u, w1, s1 = 6, e = 5, e' = 5, s2 = 7, w3 = 5); s-word (s'0 = 5, p, x2, x3, x4, s'5 = 7, s'6 = 7).
Targets (x2, x3, x4): 656, 657, 666, 658, 65B (B = degree >= 9, left open).  Window = w2 + link vertices L2..L5
(round the fives e, e') + any of L0, L1, L6 + any s-slot next to an included link vertex, at the target's letter.
A window covers every target it agrees with.  Output: dfast lines (ring order) and a .cov file.
usage: python3 framewin.py OUT RMAX"""
import sys, os, itertools, collections
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
OUT, RMAX = sys.argv[1], int(sys.argv[2])
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
d, LK = 7, [7, 6, 6, 5, 5, 7, 5]
TG = {'656': (6, 5, 6), '657': (6, 5, 7), '666': (6, 6, 6), '658': (6, 5, 8), '65B': (6, 5, None)}
def sword(t): return [5, None, t[0], t[1], t[2], 7, 7]
seen, rows = {}, []
for extra in itertools.product([0, 1], repeat=3):
    inc = {2, 3, 4, 5} | {j for j, e in zip((0, 1, 6), extra) if e}
    w = [LK[j] if j in inc else None for j in range(d)]
    slots = [j for j in (0, 2, 3, 4, 5, 6) if j in inc or (j + 1) % d in inc]
    for tn, t in TG.items():
        full = sword(t)
        for k in range(len(slots) + 1):
            for SS in itertools.combinations(slots, k):
                if any(full[j] is None for j in SS): continue
                s = [full[j] if j in SS else None for j in range(d)]
                r = G['ringf'](d, w, s)
                if r > RMAX: continue
                L_ = ''.join(str(w[j]) if w[j] is not None else '.' for j in range(d))
                S_ = ''.join(str(s[j]) if s[j] is not None else '.' for j in range(d))
                key = G['canon_key'](d, L_, S_); nm = 'f%d_%s_%s' % (d, key[1], key[2])
                cov = [u for u, tt in TG.items() if all(s[j] is None or s[j] == sword(tt)[j] for j in range(d))]
                if nm in seen: seen[nm] = sorted(set(seen[nm]) | set(cov)); continue
                line = G['make'](d, r, None, w, s, nm)
                if not line or line.startswith('RING'): continue
                seen[nm] = cov; rows.append((r, nm, line))
rows.sort(key=lambda x: (x[0], -len(seen[x[1]]), x[1]))
with open(OUT, 'w') as f:
    for r, nm, line in rows: f.write(line + '\n')
with open(OUT + '.cov', 'w') as f:
    for r, nm, line in rows: f.write('%s %d %s\n' % (nm, r, ' '.join(seen[nm])))
print(len(rows), 'windows', sorted(collections.Counter(r for r, *_ in rows).items()))
