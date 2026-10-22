# (a') controlled mismatch: A's seam row carries a tilted (c22) segment of length m inside a flat (c3) row; B is flat.
# Is min R a function of the mismatch M only (independent of the seam length L)?
import random, sys
from pysat.solvers import Minisat22
from tilt import build, c22, c3, minR, PERMS
from matched import mismatch
DIRS=[(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]
def complete_A(L,D,pins,rng):
    V=[(i,j) for i in range(L+1) for j in range(-D,0)]; ix={v:k for k,v in enumerate(V)}
    var=lambda v,c:4*ix[v]+c+1; s=Minisat22()
    for v in V:
        s.add_clause([var(v,c) for c in range(4)])
        for d in DIRS:
            w=(v[0]+d[0],v[1]+d[1])
            if w in ix and ix[w]>ix[v]:
                for c in range(4): s.add_clause([-var(v,c),-var(w,c)])
    s.set_phases([var(v,rng.randrange(4)) for v in V])
    ok=s.solve(assumptions=[var(v,c) for v,c in pins.items()])
    if not ok: return None
    m=set(x for x in s.get_model() if x>0)
    return {v:next(c for c in range(4) if var(v,c) in m) for v in V}
if __name__=="__main__":
    rng=random.Random(1); D=11
    for m in [0,4,8,12,16]:
        for L in [24,48,72]:
            a=(L-m)//2
            pins={}
            for i in range(L+1):
                if a<=i<a+m: pins[(i,-1)]=c22((i,-1))
                elif i<a-2 or i>=a+m+2: pins[(i,-1)]=c3((i,-1))   # 2 free vertices at each junction
            ca=complete_A(L,D,pins,rng)
            if ca is None: print("m=%d L=%d unextendable pins"%(m,L)); continue
            cA=lambda v:ca[v]; cB=c3
            M=mismatch(cA,cB,L); R,p=minR(L,D,cA,cB,Rmax=D-2)
            print("m=%2d L=%2d  M=%6.2f  minR=%s"%(m,L,M,R if R is not None else '>=%d'%(D-1)),flush=True)
