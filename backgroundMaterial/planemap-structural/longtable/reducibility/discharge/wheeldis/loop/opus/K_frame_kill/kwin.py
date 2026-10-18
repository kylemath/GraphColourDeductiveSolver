"""K_frame_kill: every window of w2's frame (centre w2 d=7, link 7696575, s-word 5555977; L2 = s1 and slot 4 = x4
are degree >= 9, so ring-only).  Known vertices: w2, L0,L1,L3..L6, s0..s3,s5,s6 (13).  A window = any subset I of
them (w2 in or out) whose neighbourhood ring is a simple induced cycle (gen.py's extract).  Built on one layered
disc (gen.py build; unknown second-ring vertices at 9 = ring only).  Dedup by lemmaA's canonical key.
Names: f7_<L>_<S> with '.' for absent, 'c'/'n' prefix flag = w2 in/out: e.g. fc7_7.96.75_5555.77 (frame coords, not
canonical).  Output dfast lines sorted by (ring, -m).  usage: python3 kwin.py OUT RMIN RMAX"""
import sys, os, itertools, collections
HERE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
OUT, RMIN, RMAX = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
src = open(os.path.join(HERE, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', '30']; G = {'__file__': os.path.join(HERE, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
sys.path.insert(0, os.path.join(HERE, 'loop', 'lemmaA')); _a = sys.argv; sys.argv = ['x']; import la; sys.argv = _a
d, LK, SW = 7, [7, 6, 9, 6, 5, 7, 5], [5, 5, 5, 5, 9, 7, 7]
r2 = {('s', j): SW[j] for j in range(d) if SW[j] != 9}
adj, name = G['build'](d, LK, r2); inv = {v: x for x, v in name.items()}
K = [('u',)] + [('w', j) for j in range(d) if LK[j] != 9] + [('s', j) for j in range(d) if SW[j] != 9]
DEG = {('u',): d}; DEG.update({('w', j): LK[j] for j in range(d)}); DEG.update({('s', j): SW[j] for j in range(d)})
def conn(S):
    S = set(S); st = [next(iter(S))]; seen = {st[0]}
    while st:
        x = st.pop()
        for y in adj[x]:
            if y in S and y not in seen: seen.add(y); st.append(y)
    return len(seen) == len(S)
lines, rc = {}, collections.Counter()
for k in range(2, len(K) + 1):
    for T in itertools.combinations(K, k):
        I = [inv[x] for x in T]
        if not conn(I): continue
        Ts = set(T)
        # quick ring estimate skip: extract is cheap enough
        c = G['extract'](adj, I, {inv[x]: DEG[x] for x in T})
        if c is None or not (RMIN <= c[0] <= RMAX): continue
        cb = '%d %d %s %s' % c; ck = la.ckey(cb) or ('raw' + cb)
        L_ = ''.join(str(LK[j]) if ('w', j) in Ts else '.' for j in range(d))
        S_ = ''.join(str(SW[j]) if ('s', j) in Ts else '.' for j in range(d))
        nm = 'f%s7_%s_%s' % ('c' if ('u',) in Ts else 'n', L_, S_)
        if ck in lines and lines[ck][2] >= 0: continue
        lines[ck] = (c[0], c[1], 0, '%s %s' % (nm, cb)); rc[c[0]] += 1
rows = sorted(lines.values(), key=lambda x: (x[0], -x[1], x[3]))
open(OUT, 'w').write(''.join(r[3] + '\n' for r in rows))
print(len(rows), 'windows', sorted(rc.items()))
print('by (ring, m):', sorted(collections.Counter((r[0], r[1]) for r in rows).items()))
