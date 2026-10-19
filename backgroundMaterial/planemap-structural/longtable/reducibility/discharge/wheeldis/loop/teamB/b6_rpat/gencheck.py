"""B6 self-check: patterns from rpat.kill must generalise. For random arrangements that rpat kills, re-randomise every
slot the pattern leaves free (respecting its masks) and re-run the oracle restricted to the same configuration: it
must still find an embedding."""
import random, sys, rpat
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
CF = {c[0]: c for c in rpat.CONFS}
tot = bad = 0
for trial in range(4000):
    d = random.choice([7, 7, 8, 8, 9, 10, 11])
    link = [random.choice([5, 5, 5, 6, 6, 7, 8, 9]) for _ in range(d)]
    sw = [random.choice([5, 6, 6, 7, 8, 9]) for _ in range(d)]
    k = rpat.kill(d, link, sw)
    if not k:
        continue
    name, pat = k
    for rep in range(3):
        l2, s2 = list(link), list(sw)
        P = dict(pat)
        for i in range(d):
            if i not in P: l2[i] = random.choice([5, 6, 7, 8, 9])
            else:
                l2[i] = random.choice([5 + b for b in range(5) if P[i] >> b & 1])
            if d + i not in P: s2[i] = random.choice([5, 6, 7, 8, 9])
            else:
                s2[i] = random.choice([5 + b for b in range(5) if P[d + i] >> b & 1])
        rot, deg, known, slot = rpat.disc(d, l2, s2)
        tot += 1
        if rpat.embed_map(CF[name], rot, deg, known) is None:
            bad += 1
            if bad <= 5: print('FAIL', d, link, sw, name, pat, '->', l2, s2)
print('generalisation checks', tot, 'failures', bad)
