# (a) matched-tilt seams on lattice parallelograms: min repair radius R vs seam length L and height mismatch M
import random, math, sys, itertools, collections
from tilt import build, c22, c3, height_inc, minR, PERMS
def half(L,D,side):
    return [(i,j) for i in range(L+1) for j in (range(-D,0) if side=='A' else range(0,D))]
def kempe_randomise(col,verts,nflips,rng):
    S=set(verts); vs=list(verts)
    for _ in range(nflips):
        v=rng.choice(vs); a=col[v]; b=rng.choice([c for c in range(4) if c!=a])
        comp={v}; st=[v]
        while st:
            x=st.pop()
            for d in [(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)]:
                y=(x[0]+d[0],x[1]+d[1])
                if y in S and y not in comp and col[y] in (a,b): comp.add(y); st.append(y)
        for x in comp: col[x]=a+b-col[x]
    return col
def base(kind,rng):
    p=rng.choice(PERMS); si,sj=rng.randrange(6),rng.randrange(6)
    f=c3 if kind=='flat' else c22
    return lambda v:p[f((v[0]+si,v[1]+sj))]
def rowH(colf,j,L):
    H=[(0.0,0.0)]
    for i in range(L):
        h=height_inc((i,j),(i+1,j),colf); H.append((H[-1][0]+h[0],H[-1][1]+h[1]))
    return H
def mismatch(cA,cB,L):
    HA=rowH(cA,-1,L); best=None
    for p in PERMS:
        HB=rowH(lambda v:p[cB(v)],0,L)
        Dt=[(a[0]-b[0],a[1]-b[1]) for a,b in zip(HA,HB)]
        diam=max(math.hypot(x[0]-y[0],x[1]-y[1]) for x in Dt for y in Dt)
        best=diam if best is None else min(best,diam)
    return best
def sample(L,D,kindA,kindB,nA,nB,rng):
    A=half(L,D,'A'); B=half(L,D,'B')
    fa=base(kindA,rng); fb=base(kindB,rng)
    ca=kempe_randomise({v:fa(v) for v in A},A,nA,rng)
    cb=kempe_randomise({v:fb(v) for v in B},B,nB,rng)
    cA=lambda v:ca[v]; cB=lambda v:cb[v]
    M=mismatch(cA,cB,L); R,p=minR(L,D,cA,cB,Rmax=D-2)
    return M,R
if __name__=="__main__":
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0)
    D=12
    rows=[]
    for L in [12,24,36,48]:
        for (kA,kB,nA,nB,label) in [('flat','flat',0,0,'flat|flat'),('tilt','tilt',0,0,'c22|c22'),
                                    ('flat','flat',30,30,'flat+K30'),('flat','flat',300,300,'flat+K300'),
                                    ('tilt','tilt',300,300,'c22+K300'),('flat','tilt',0,0,'flat|c22')]:
            for rep in range(4 if nA==0 else 6):
                M,R=sample(L,D,kA,kB,nA,nB,rng)
                print("L=%2d %-10s M=%6.2f R=%s"%(L,label,M,R if R is not None else '>=%d'%(D-1)),flush=True)
def height_LB(cA,cB,L,D):
    """Smallest R not excluded by the height theorem: exists renaming with diam_t(H_A row -(R+2) - H_piB row R+1) <= 4R+6."""
    import math
    for R in range(0,D-1):
        HA=rowH(cA,-(R+2),L)
        for p in PERMS:
            HB=rowH(lambda v:p[cB(v)],R+1,L)
            Dt=[(a[0]-b[0],a[1]-b[1]) for a,b in zip(HA,HB)]
            if max(math.hypot(x[0]-y[0],x[1]-y[1]) for x in Dt for y in Dt)<=4*R+6+1e-9: return R
    return None
