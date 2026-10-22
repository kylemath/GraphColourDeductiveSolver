# generate closing instances (ico10/ico20 balanced splits, level sides) and save those with R in {0,1,2}
import sys
sys.path.insert(0,'/mnt/project-files/multiscale/closing/round2'); sys.path.insert(0,'/mnt/project-files/multiscale/closing')
from band import *
import e1util
OUT='/mnt/project-files/multiscale/sphere/twist/inst/'
def run(F, seed, k=3):
    rng=random.Random(500+F*31+seed); adj=e1util.base('ico%d'%F); T=Tri(adj); n=len(adj)
    for att in range(40):
        A0=grow(T, rng.choice([v for v in range(n) if T.deg[v]==5]) if EUL else rng.randrange(n), n//2+(rng.randint(-n//25,n//25) if EUL else 0), rng, wiggle=0.0)
        A,r=smooth(T,A0,rng)
        if A is None: continue
        cA,cB=r
        if cA.parity_odd or cB.parity_odd: continue
        if EUL:
            sv=set(x for e in seam_edges(T,A) for x in e)
            if len(odd_near(T,sv,1))>1: continue
        break
    else: return []
    B=cB.S; dA,dB=depth(T,cA),depth(T,cB); got=[]
    tA=[None]; 
    tt=(0,0) if T0 else None
    ca=[c for c in (band_level_col(T,cA,rng,dep=dA,t=tt) for _ in range(k)) if isinstance(c,dict)]
    cb=[c for c in (band_level_col(T,cB,rng,dep=dB,t=tt) for _ in range(k)) if isinstance(c,dict)]
    if not ca or not cb: return []
    for i,a in enumerate(ca):
        for j,b in enumerate(cb):
            R,p,nk=closing_R(T,A,B,a,b,Rmax=6)
            fn=OUT+'ico%d_%ss%d_%d_%d_R%s.pkl'%(F,('e' if EUL else '')+('t0' if T0 else ''),seed,i,j,R)
            pickle.dump(dict(map='ico%d'%F,adj=T.adj,A=A,colA=a,colB=b,R=R,tA=cA.tau(a),tB=cB.tau(b)),open(fn,'wb'))
            print(fn, R, nk, cA.tau(a), cB.tau(b), flush=True); got.append(R)
    return got
T0=len(sys.argv)>4
EUL=len(sys.argv)>5
if __name__=='__main__':
    F=int(sys.argv[1]); 
    for s in range(int(sys.argv[2]), int(sys.argv[3])): run(F,s)
