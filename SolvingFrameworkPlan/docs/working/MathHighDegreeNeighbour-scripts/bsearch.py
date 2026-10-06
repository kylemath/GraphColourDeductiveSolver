import sys,random,collections
from lib import *
from pat import comp,classify,canon
# hill-climb on triangulations containing hole h (deg 5) adjacent to p (deg>=7); others of link <= maxo; min deg 5; 4-connected
def valid(n,F,h,p,maxo):
    Ad=adj(n,F); d=[len(x) for x in Ad]
    if min(d)<5 or d[h]!=5 or p not in Ad[h] or d[p]<7: return False
    if max(d[x] for x in Ad[h] if x!=p)>maxo: return False
    return ntri(n,F)==2*n-4
def insert(n,F,f,rnd):
    x=n; G=[g for g in F if g!=f]+[(f[0],f[1],x),(f[1],f[2],x),(f[2],f[0],x)]
    for _ in range(2):
        opp=[(g[0],g[1]) if g[2]==x else (g[1],g[2]) if g[0]==x else (g[2],g[0]) for g in G if x in g]
        rnd.shuffle(opp)
        for (y,z) in opp:
            H=flip(G,y,z)
            if H: G=H; break
    return n+1,G
def propose(n,F,h,p,rnd,maxn,frozen):
    for _ in range(rnd.randint(1,3)):
        if rnd.random()<0.25 and n<maxn:
            f=rnd.choice(F)
            if h in f or any(t in frozen for t in f): continue
            n,F=insert(n,F,f,rnd)
        else:
            f=rnd.choice(F); i=rnd.randrange(3); x,y=f[i],f[(i+1)%3]
            if h in (x,y) or x in frozen or y in frozen: continue
            G=flip(F,x,y)
            if G: F=G
    return n,F
def score(batch,h,p):
    out=run([(n,F) for n,F in batch],extra=['--hole',str(h)],fn='b%d.txt'%id(batch))
    recs,links,dls=parse(out); res=[]
    for gi,(n,F) in enumerate(batch):
        L=links[(gi,h)]; kp=L.index(p); mx=collections.defaultdict(int)
        for j,dd,col in dls[(gi,h)]: mx[(kp-j)%5]=max(mx[(kp-j)%5],dd)
        r=[x for x in recs if x['g']==gi][0]
        res.append((r['maxdl'],dict(mx),r['unreached'],r['ncol']))
    return res
if __name__=='__main__':
    m=int(sys.argv[1]); steps=int(sys.argv[2]); seed=int(sys.argv[3]); maxo=int(sys.argv[4]); maxn=int(sys.argv[5]); mode=sys.argv[6]
    DUMP=open(f'dump_{m}_{mode}_{maxo}_{seed}.txt','w'); rnd=random.Random(seed); n,F=belt(m); h,p=2,0
    frozen={p} if mode=='free' else {0}|set(range(2,2+m))   # 'bside': keep a and all u_i; 'free': only keep a's own edges? (a not flipped)
    cur=score([(n,F)],h,p)[0]; best=(cur[0],cur[1],n,F); hist=collections.Counter()
    for it in range(steps):
        batch=[]
        for _ in range(12):
            nn,G=propose(n,F,h,p,rnd,maxn,frozen)
            if G is not F and valid(nn,G,h,p,maxo): batch.append((nn,G))
        if not batch: continue
        res=score(batch,h,p)
        for (nn,G),r in zip(batch,res):
            hist[r[0]]+=1
            DUMP.write(line(nn,G))
            if r[2]>0: print('UNREACHED', line(nn,G))
            if r[0]>best[0]: best=(r[0],r[1],nn,G); print('new best',r,'n',nn,'deg p',len(adj(nn,G)[p]),'others',sorted(len(adj(nn,G)[x]) for x in adj(nn,G)[h]),flush=True)
        i=max(range(len(res)),key=lambda i:(res[i][0],rnd.random()))
        if res[i][0]>=cur[0] or rnd.random()<0.3: n,F=batch[i]; cur=res[i]
    print('m',m,'mode',mode,'maxo',maxo,'evaluated hist of max DL radius',dict(hist),'best',best[0],best[1])
    open(f'best_{m}_{mode}_{maxo}_{seed}.txt','w').write(line(best[2],best[3]))
