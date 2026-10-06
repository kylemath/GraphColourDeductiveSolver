import pickle, random, sys, collections
from real import parse, holes65
random.seed(int(sys.argv[1])); NOUT=int(sys.argv[2]); TARGET=int(sys.argv[3])
src=[]
for fn in ('real2_g23.txt.pkl','real2_g22.txt.pkl'):
    for f,line,res in pickle.load(open(fn,'rb')):
        mx=max(r[2] for r in res); src.append((mx,line,res[0][0]))
src.sort(key=lambda t:-t[0])
src=[s for s in src if s[0]==3]
def adjof(n,fs):
    adj=[set() for _ in range(n)]
    for f in fs:
        for k in range(3): adj[f[k]].add(f[(k+1)%3]); adj[f[(k+1)%3]].add(f[k])
    return adj
def flip(fs,adj,a,b,protect):
    F=[i for i,f in enumerate(fs) if a in f and b in f]
    if len(F)!=2: return False
    c=[x for x in fs[F[0]] if x not in (a,b)][0]; d=[x for x in fs[F[1]] if x not in (a,b)][0]
    if d in adj[c] or c==d: return False
    if {a,b,c,d}&protect: return False
    if len(adj[a])<=5 or len(adj[b])<=5: return False
    fs[F[0]]=(a,c,d); fs[F[1]]=(b,c,d)
    adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c)
    return True
out=[]
tries=0
while len(out)<NOUT and tries<NOUT*200:
    tries+=1
    mx,line,v=random.choice(src)
    n,fs=parse(line); fs=[tuple(f) for f in fs]
    H=[h for h in holes65(n,fs) if h[0]==v][0]
    protect={v}|set(H[1])
    adj=adjof(n,fs)
    ok=True
    while n<TARGET and ok:
        # insert vertex into random face avoiding protect
        cand=[i for i,f in enumerate(fs) if not set(f)&protect]
        i=random.choice(cand); a,b,c=fs[i]; u=n; n+=1; adj.append(set())
        fs[i]=(a,b,u); fs.append((b,c,u)); fs.append((c,a,u))
        for x in (a,b,c): adj[u].add(x); adj[x].add(u)
        # raise deg(u) to >=5 by flipping opposite edges
        for _ in range(20):
            if len(adj[u])>=5: break
            nb=list(adj[u]); random.shuffle(nb)
            done=False
            for x in nb:
                for y in nb:
                    if x<y and y in adj[x] and flip(fs,adj,x,y,protect): done=True;break
                if done: break
            if not done: ok=False;break
    if not ok: continue
    for _ in range(random.randint(0,15)):
        a=random.randrange(n); 
        if not adj[a]: continue
        b=random.choice(list(adj[a])); flip(fs,adj,a,b,protect)
    if min(len(x) for x in adj)<5: continue
    if not any(h[0]==v for h in holes65(n,fs)): continue
    out.append(f"G {n} 0 {len(fs)} "+' '.join(f'{a} {b} {c}' for a,b,c in fs))
open(f'grow_{sys.argv[1]}_{TARGET}.txt','w').write('\n'.join(out)+'\n')
print(len(out),'graphs',tries,'tries')
