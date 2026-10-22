# Level rows on the straight degree-6 cylinder: structural characterisation and generator.
# Row = proper colouring of C_L with colours 0..3.  Boundary walk: H_{i+1}=H_i+e_{r(i)^r(i+1)} (constant sign, degree 6).
# Inclusive definition: r is level iff for SOME base point (rotation) the one-lap walk has tau<=1 (tm.py's tau).
# Claim [P]: r is level iff some colour c occupies a position set whose cyclic gaps are all 3 except at most one gap in {2,4}.
import sys, itertools, math
sys.path.insert(0, '/mnt/project-files/multiscale/closing/round2')
from tm import rows, tau, walk, PERMS

def rot(r, k): return r[k:] + r[:k]
def level_tm(r):
    """tm.py tau<=1 for some base point"""
    return any(tau(rot(r, k))[0] <= 1 + 1e-9 for k in range(len(r)))
def level_struct(r):
    L = len(r)
    for c in range(4):
        pos = [i for i in range(L) if r[i] == c]
        if not pos: continue
        gaps = [(pos[(j+1) % len(pos)] - pos[j]) % L or L for j in range(len(pos))]
        odd = [g for g in gaps if g != 3]
        if len(odd) == 0 or (len(odd) == 1 and odd[0] in (2, 4)): return True
    return False
def gen_level(L):
    """all level rows (inclusive) via the structure, as a sorted list of tuples"""
    out = set()
    m, res = divmod(L, 3)
    # skeleton colour c; blocks of (c, x, y), x!=y, x,y!=c; defect: gap 2 -> (c, x) ; gap 4 -> (c, x, y, z)
    for c in range(4):
        oth = [d for d in range(4) if d != c]
        if res == 0:
            blocks = [(c, x, y) for x in oth for y in oth if x != y]
            for bs in itertools.product(blocks, repeat=m):
                w = sum(bs, ())
                if all(w[i] != w[(i+1) % L] for i in range(L)):
                    for k in range(L): out.add(rot(w, k))
        else:
            blocks = [(c, x, y) for x in oth for y in oth if x != y]
            if res == 2: defs = [(c, x) for x in oth]
            else: defs = [(c, x, y, z) for x in oth for y in oth for z in oth if x != y and y != z]
            for d in defs:
                for bs in itertools.product(blocks, repeat=(L-len(d))//3):
                    w = d + sum(bs, ())
                    if all(w[i] != w[(i+1) % L] for i in range(L)):
                        for k in range(L): out.add(rot(w, k))
    return sorted(out)
if __name__ == '__main__':
    for L in range(3, 11):
        R = rows(L); A = set(r for r in R if level_tm(r)); B = set(r for r in R if level_struct(r)); G = set(gen_level(L))
        base0 = sum(1 for r in R if tau(r)[0] <= 1+1e-9)
        print('L', L, 'rows', len(R), 'level(tm,any base)', len(A), 'level(struct)', len(B), 'gen', len(G), 'tm base0 only', base0, 'EQUAL' if A == B == G else 'DIFFER', flush=True)
