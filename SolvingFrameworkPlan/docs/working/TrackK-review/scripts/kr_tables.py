"""TrackK review: exhaustive check of the finite tables T1, T2, T3 of TrackK/FProof.md, written from scratch.
Colours 0..3 viewed as Z2^2 with xor.  Usage: python3 -I kr_tables.py
"""
from itertools import permutations

CYC = {(1, 2, 3), (2, 3, 1), (3, 1, 2)}

def tait_cw(a, b, c):
    return (a ^ b, b ^ c, c ^ a) in CYC

def perm_even(p):
    p = list(p); inv = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            inv += p[i] > p[j]
    return inv % 2 == 0

def positive(a, b, c):
    d = ({0, 1, 2, 3} - {a, b, c}).pop()
    return perm_even((d, a, b, c))

def sigma(a, b, c):
    return 1 if positive(a, b, c) else -1

# T1
n1 = bad1 = 0
for a, b, c in permutations(range(4), 3):
    n1 += 1; bad1 += tait_cw(a, b, c) != positive(a, b, c)
# sanity: Tait triple of a proper face is always a permutation of (1,2,3)
assert all(sorted((a ^ b, b ^ c, c ^ a)) == [1, 2, 3] for a, b, c in permutations(range(4), 3))
print('T1: cw <=> positive : %d triples, %d mismatches' % (n1, bad1))

# T2
n2 = bad2 = 0
for al, mu, A, B in permutations(range(4)):
    hand = (al ^ mu, al ^ A, al ^ B) in CYC
    for f in ((mu, al, A), (mu, A, B), (B, al, mu)):
        n2 += 1; bad2 += tait_cw(*f) != hand
print('T2: new faces cw <=> hand : %d (roles x faces), %d mismatches' % (n2, bad2))

# T3 (also: coherence of the orientation of the boundary of the tetrahedron)
n3 = bad3 = 0
for x, y in permutations(range(4), 2):
    rest = [t for t in range(4) if t not in (x, y)]
    for z in rest:
        for w in rest:
            n3 += 1; bad3 += (sigma(x, y, z) == sigma(y, x, w)) != (z != w)
print('T3: sigma equal across xy-edge <=> z != w : %d cases, %d mismatches' % (n3, bad3))

# Extra E1: the reversed-link convention flips hand (so the orientation convention is load-bearing:
# the wrong convention would make the residue odd at every state).
bad = 0
for al, mu, A, B in permutations(range(4)):
    h1 = (al ^ mu, al ^ A, al ^ B) in CYC
    h2 = (al ^ mu, al ^ B, al ^ A) in CYC   # reversed link: roles (al, mu, al, B, A)
    bad += h1 == h2
print('E1: reversing the link order flips hand on all 24 role assignments: %d exceptions' % bad)

# Extra E2: hand is invariant under the pi relabelling (al, mu, A, B) -> (al, B, mu, A) claimed in TrackC 6.4
bad = 0
for al, mu, A, B in permutations(range(4)):
    h1 = (al ^ mu, al ^ A, al ^ B) in CYC
    h2 = (al ^ B, al ^ mu, al ^ A) in CYC
    bad += h1 != h2
print('E2: hand(al,B,mu,A) == hand(al,mu,A,B): %d exceptions of 24' % bad)
print('ALL TABLES OK' if bad1 == bad2 == bad3 == 0 else 'TABLE FAILURE')
