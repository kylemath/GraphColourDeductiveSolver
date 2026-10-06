import sys,random,json,collections
from lib import *
T4F=[(0,1,2),(0,1,5),(0,2,3),(0,3,4),(0,4,5),(1,2,6),(1,5,10),(1,6,10),(2,3,7),(2,6,11),(2,7,11),(3,4,8),(3,7,8),(4,5,9),(4,8,9),(5,9,10),(6,10,15),(6,11,15),(7,8,12),(7,11,12),(8,9,13),(8,12,13),(9,10,14),(9,13,14),(10,14,15),(11,12,16),(11,15,16),(12,13,16),(13,14,16),(14,15,16)]
def linkof(n,F,h):
    Ad=adj(n,F); return Ad
def ok(n,F,h,p,need4c=True):
    Ad=adj(n,F); d=[len(x) for x in Ad]
    if min(d)<5 or d[h]!=5 or p not in Ad[h]: return False
    if need4c and ntri(n,F)!=2*n-4: return False
    return True
def cls(n,F,h,p):
    Ad=adj(n,F); d=[len(x) for x in Ad]
    o=sorted(d[x] for x in Ad[h] if x!=p)
    return d[p], max(o)
def evaluate(batch):
    # batch: list of (n,F,h,p)
    out=run([(n,F) for n,F,h,p in batch],fn='s.txt')
    recs,links,dls=parse(out)
    res=[]
    for gi,(n,F,h,p) in enumerate(batch):
        L=links[(gi,h)]; kp=L.index(p)
        mx=collections.defaultdict(int); ndl=0
        for j,d,col in dls[(gi,h)]:
            mx[(kp-j)%5]=max(mx[(kp-j)%5],d); ndl+=1
        r=[x for x in recs if x['g']==gi and x['v']==h][0]
        res.append((r.get('maxdl',-1),dict(mx),r.get('unreached',0),ndl))
    return res
def walk(name,n,F,h,p,steps,seed,pre=0,maxp=99):
    rnd=random.Random(seed)
    # pre-phase: raise deg p
    Ad=adj(n,F)
    while len(Ad[p])<pre:
        cand=[]
        for f in F:
            if p in f:
                x,y=[t for t in f if t!=p]
                if h in (x,y): continue
                G=flip(F,x,y)
                if G and ok(n,G,h,p,False): cand.append(G)
        if not cand: break
        F=rnd.choice(cand); Ad=adj(n,F)
    cur=evaluate([(n,F,h,p)])[0]; best=collections.defaultdict(lambda:(-1,None))
    E=lambda F:[(f[i],f[(i+1)%3]) for f in F for i in range(3) if f[i]<f[(i+1)%3]]
    for it in range(steps):
        batch=[]
        for _ in range(8):
            G=F
            for _ in range(rnd.randint(1,2)):
                x,y=rnd.choice(E(G))
                if h in (x,y): continue
                H=flip(G,x,y)
                if H: G=H
            if G is not F and ok(n,G,h,p) and len(adj(n,G)[p])>=7 and len(adj(n,G)[p])<=maxp: batch.append((n,G,h,p))
        if not batch: continue
        res=evaluate(batch)
        for (nn,G,hh,pp),r in zip(batch,res):
            c=cls(nn,G,hh,pp); key=('o<=5' if c[1]<=5 else 'o<=6' if c[1]<=6 else 'o<=11' if c[1]<=11 else 'o>11')
            if r[2]>0: print('UNREACHED!',name,line(nn,G)); 
            if r[0]>best[key][0]: best[key]=(r[0],r[1],c,line(nn,G))
        i=max(range(len(res)),key=lambda i:(res[i][0],rnd.random()))
        if res[i][0]>=cur[0] or rnd.random()<0.3: F=batch[i][1]; cur=res[i]
    for k,v in best.items(): print(name,k,'maxDL',v[0],'by k',v[1],'(deg p, max other)',v[2]); 
    return best
if __name__=='__main__':
    which=sys.argv[1]; steps=int(sys.argv[2]); seed=int(sys.argv[3])
    if which.startswith('belt'):
        m=int(which[4:]); n,F=belt(m); walk(which,n,F,2,0,steps,seed)
    elif which.startswith('A'):
        r=int(which[1:]); n,F=A(r); walk(which,n,F,0,1,steps,seed,pre=7)
    elif which=='pent':
        n,F=pentakis(); Ad=adj(n,F); h=[x for x in range(n) if len(Ad[x])==5][0]; p=min(Ad[h]); walk(which,n,F,h,p,steps,seed,pre=7)
    elif which=='T4':
        walk(which,17,T4F,4,0,steps,seed,pre=7)
