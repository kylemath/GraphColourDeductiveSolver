"""Track K: finite tables behind the proof of Conjecture F (exhaustive, no randomness).
T1  For distinct colours a,b,c in {0,1,2,3} (= Z2^2 via xor), the Tait triple (a^b, b^c, c^a)
    is a cyclic shift of (1,2,3)  <=>  (a,b,c) is a positively oriented face of the tetrahedron
    with vertex order (0,1,2,3), i.e. the permutation (d,a,b,c) is even (d the fourth colour).
T2  For distinct al,mu,A,B: hand := [(al^mu, al^A, al^B) cyclic of (1,2,3)] equals the Tait
    cw-indicator of each of the three fan faces (x1,x2,x3)=(mu,al,A), (x1,x3,x4)=(mu,A,B),
    (x4,x0,x1)=(B,al,mu).
T3  Adjacent faces across an edge coloured xy: (x,y,z) and (y,x,w) have equal sign iff z != w.
Usage: python3 -I tk_tables.py
"""
from itertools import permutations
CYC = {(1, 2, 3), (2, 3, 1), (3, 1, 2)}
def tait_cw(a, b, c): return (a ^ b, b ^ c, c ^ a) in CYC
def parity(p):
    p = list(p); s = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            s += p[i] > p[j]
    return s % 2
def pos(a, b, c):
    (d,) = set(range(4)) - {a, b, c}
    return parity((d, a, b, c)) == 0
bad1 = [t for t in permutations(range(4), 3) if tait_cw(*t) != pos(*t)]
print('T1 ordered triples', len(list(permutations(range(4), 3))), 'mismatches', len(bad1))
bad2 = 0
for al, mu, A, B in permutations(range(4)):
    hand = (al ^ mu, al ^ A, al ^ B) in CYC
    for f in ((mu, al, A), (mu, A, B), (B, al, mu)):
        bad2 += tait_cw(*f) != hand
print('T2 role assignments 24, fan faces 72, mismatches', bad2)
bad3 = 0; n3 = 0
for x, y, z, w in permutations(range(4)):
    for zz in (z, w):
        n3 += 1
        bad3 += (pos(x, y, z) == pos(y, x, zz)) != (zz != z)
print('T3 cases', n3, 'mismatches', bad3)
