"""exact canonical situation counts with link/s letters restricted to ALPHABET (wildcard completions still 5..9+)."""
import sys, os, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la
A = tuple(map(int, sys.argv[2])); k = int(sys.argv[1])
seen = set(); n = 0
f = open(os.path.join(la.HERE, 'sit_k%d_%s.txt' % (k, sys.argv[2])), 'w')
for F in itertools.combinations(range(7), k):
    J = sorted(set(F) | {(j - 1) % 7 for j in F}); NB = [a for a in A if a != 5]
    for rest in itertools.product(NB, repeat=7 - k):
        it = iter(rest); L = tuple(5 if j in F else next(it) for j in range(7))
        for sv in itertools.product(A, repeat=len(J)):
            s = [0] * 7
            for j, x in zip(J, sv): s[j] = x
            c = la.canon_sit(L, s)
            if c in seen: continue
            seen.add(c)
            if la.excluded(L, s): continue
            n += 1; f.write(''.join(map(str, c[:7])) + ' ' + ''.join(map(str, c[7:])) + '\n')
print('k=%d A=%s canonical non-excluded situations %d' % (k, sys.argv[2], n))
