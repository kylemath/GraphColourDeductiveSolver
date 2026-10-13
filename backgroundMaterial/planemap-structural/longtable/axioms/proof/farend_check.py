"""Lemma FE check: local matched-edge words at the five neighbours w_s of v along closed orbits / windows.
Prediction [hand]: with A5v at the visit times, w_s's word is f a b a b f b a b a ... (blocks alternate, zero
winding); with anti-A5v it is f a b a b f a b a b ... (blocks repeat, winding L/5 turns w.r.t. any fixed
cyclic order of the three edges at w_s)."""
import sys, json
sys.path.insert(0, '..')
from ax_lib import G5, parse_line

def words(g, cyc):
    L = len(cyc); out = {}
    for s in range(5):
        e = g.fv[s]; w = g.other(e, g.v)
        inc = g.inc[w]
        word = [next(x for x in inc if x in cyc[t]) for t in range(L)]
        # winding w.r.t. the cyclic order inc[0] -> inc[1] -> inc[2]
        idx = {x: i for i, x in enumerate(inc)}
        steps = [((idx[word[(t + 1) % L]] - idx[word[t]]) % 3) for t in range(L)]
        wind = sum(1 if d == 1 else -1 for d in steps) // 3
        rel = ''.join('f' if x == e else ('a' if x == min(y for y in inc if y != e) else 'b') for x in word)
        out[s] = (rel, wind)
    return out

for path in sys.argv[1:]:
    for l in open(path):
        l = l.strip()
        if l.startswith('SOL'): l = l.split(' ', 1)[1].split('{')[0]
        if not l or not l[0].isdigit(): continue
        g = G5(*parse_line(l))
        P, good, cyc = g.orbits()
        for c in cyc:
            w = g.word(c)
            if len(c) < 10: continue
            print(path.split('/')[-1], 'L', len(c), 'kH word', ''.join(map(str, w)))
            for s_, (rel, wind) in words(g, c).items():
                print('   far end of f%d:' % s_, rel, 'winding', wind)
