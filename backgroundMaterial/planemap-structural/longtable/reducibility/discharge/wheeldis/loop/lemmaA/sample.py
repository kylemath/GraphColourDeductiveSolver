"""Uniform random labelled situations (L, s) with exactly k fives over alphabet A, rejection of R_opt-excluded ones;
estimates the number of canonical situations (accepted fraction x labelled total / 14) and writes N canonical
samples.  Usage: python3 sample.py k ALPHABET(e.g. 567 or 56789) N SEED"""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from la import *
k, A, N, seed = int(sys.argv[1]), tuple(map(int, sys.argv[2])), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed); NB = [a for a in A if a != 5]
pos = []; wts = []
for F in itertools.combinations(range(7), k):
    J = {j for j in F} | {(j - 1) % 7 for j in F}; pos.append((F, sorted(J))); wts.append(len(NB) ** (7 - k) * len(A) ** len(J))
NLAB = sum(wts); acc = tries = 0; out = {}
while len(out) < N and tries < 200 * N:
    tries += 1; F, J = rng.choices(pos, weights=wts)[0]
    L = tuple(5 if j in F else rng.choice(NB) for j in range(7)); s = [0] * 7
    for j in J: s[j] = rng.choice(A)
    if excluded(L, s): continue
    acc += 1; out[canon_sit(L, s)] = 1
fn = os.path.join(HERE, 'samp_k%d_%s.txt' % (k, sys.argv[2]))
with open(fn, 'w') as f:
    for c in out: f.write(''.join(map(str, c[:7])) + ' ' + ''.join(map(str, c[7:])) + '\n')
print('k=%d A=%s labelled %d accepted %d/%d -> est canonical situations %.3g; wrote %d' % (k, sys.argv[2], NLAB, acc, tries, acc / tries * NLAB / 14, len(out)))
