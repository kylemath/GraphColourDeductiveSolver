"""A5v bit pattern on every closed orbit (any word, law or not) of the graphs in the given files
(TrackU line format or JSON records with edges/fv).  Usage: orbit_bits.py files..."""
import sys, json
from collections import Counter
from ax_lib import G5, parse_line, from_json, law_ok
from feat import a5bit
C = Counter(); seen = set(); ex = []
for p in sys.argv[1:]:
    for l in open(p):
        l = l.strip()
        if not l: continue
        if l.startswith('{'):
            d = json.loads(l)
            if 'edges' not in d or not d.get('ncyc', 1): continue
            n, E, fv = from_json(d)
        else:
            n, E, fv = parse_line(l)
        key = (n, tuple(sorted(tuple(sorted(e)) for e in E)), tuple(tuple(sorted(E[f])) for f in fv))
        if key in seen: continue
        seen.add(key)
        g = G5(n, E, fv); P, good, cyc = g.orbits()
        for c in cyc:
            w = g.word(c); bits = [a5bit(g, M) for M in c]
            law = law_ok(w) == 0
            typ = 'const1' if all(bits) else 'const0' if not any(bits) else 'MIXED'
            C[(p.split('/')[-1], 'law' if law else 'nolaw', len(c), typ)] += 1
            L = len(c)
            C[('A5v pattern 5-periodic', all(bits[t] == bits[(t + 5) % L] for t in range(L)))] += 1
            C[('word 5-periodic', 'law' if law else 'nolaw', all(w[t] == w[(t + 5) % L] for t in range(L)))] += 1
            if typ == 'MIXED' and len(ex) < 5: ex.append((p.split('/')[-1], n, ''.join(map(str, w)), ''.join(map(str, bits))))
for k in sorted(C): print(k, C[k])
print('mixed examples:', ex)
