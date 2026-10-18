"""F_free_slots: u-centred windows of the 7/27 binder R (d7 link 5675765 s 6577575) for the 16 fillings
(s1, s4) in {6,7,8,9}^2 (9 = degree >= 9, never interior).  Window = u + all 7 link vertices + subset of
{s0,s2,s3,s5,s6} at R's letters + s1 absent or at 6..8 + s4 likewise (same construction as loop/k34/fillwin.py
on origin/claude/project-thread-nh6pv2, restricted to the free fillings).  Writes OUT (dfast lines) and OUT.cov.
usage: python3 freewin.py OUT"""
import sys, os, itertools, collections
W = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
OUT = sys.argv[1]
sys.argv = ['gen28.py', '/dev/null', '24']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
d, lk, sv = 7, '5675765', '6577575'
FILL = [(a, b) for a in range(6, 10) for b in range(6, 10)]
seen, rows = {}, []
for a in [None, 6, 7, 8]:
    for b in [None, 6, 7, 8]:
        for k in range(0, 6):
            for SS in itertools.combinations([0, 2, 3, 5, 6], k):
                w = [int(c) for c in lk]
                s = [int(sv[j]) if j in SS else None for j in range(d)]
                s[1], s[4] = a, b
                r = G['ringf'](d, w, s)
                S_ = ''.join(str(s[j]) if s[j] is not None else '.' for j in range(d))
                key = G['canon_key'](d, lk, S_); nm = 'f%d_%s_%s' % (d, key[1], key[2])
                cov = [f for f in FILL if (a is None or f[0] == a) and (b is None or f[1] == b)]
                if nm in seen: seen[nm] = sorted(set(seen[nm]) | set(cov)); continue
                line = G['make'](d, r, None, w, s, nm)
                if not line or line.startswith('RING'): print('skip', nm, line); continue
                seen[nm] = cov; rows.append((r, nm, line))
rows.sort(key=lambda x: (x[0], -len(seen[x[1]]), x[1]))
with open(OUT, 'w') as f:
    for r, nm, line in rows: f.write(line + '\n')
with open(OUT + '.cov', 'w') as f:
    for r, nm, line in rows: f.write('%s %d %s\n' % (nm, r, ' '.join('%d%d' % c for c in seen[nm])))
print(len(rows), 'windows', sorted(collections.Counter(r for r, *_ in rows).items()))
