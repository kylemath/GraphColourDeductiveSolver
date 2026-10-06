import random, subprocess, sys, re
from real import parse, holes65
from grow import adjof, flip
random.seed(7)
def mutate(line,maxn):
    n,fs=parse(line); fs=[tuple(f) for f in fs]
    H=[h for h in holes65(n,fs) if h[0]==0]
    if not H: return None
    protect={0}|set(H[0][1]); adj=adjof(n,fs)
    for _ in range(random.randint(0,2) if n<maxn else 0):
        cand=[i for i,f in enumerate(fs) if not set(f)&protect]
        i=random.choice(cand); a,b,c=fs[i]; u=n; n+=1; adj.append(set())
        fs[i]=(a,b,u); fs.append((b,c,u)); fs.append((c,a,u))
        for x in (a,b,c): adj[u].add(x); adj[x].add(u)
        for _ in range(20):
            if len(adj[u])>=5: break
            nb=list(adj[u]); random.shuffle(nb); done=False
            for x in nb:
                for y in nb:
                    if x<y and y in adj[x] and flip(fs,adj,x,y,protect): done=True;break
                if done:break
            if not done: return None
    for _ in range(random.randint(1,6)):
        a=random.randrange(n); b=random.choice(list(adj[a])); flip(fs,adj,a,b,protect)
    if min(len(x) for x in adj)<5: return None
    if not any(h[0]==0 for h in holes65(n,fs)): return None
    return f"G {n} 0 {len(fs)} "+' '.join(f'{a} {b} {c}' for a,b,c in fs)
pop=[open('r4.txt').read().strip()]
best=None
for rnd in range(int(sys.argv[1])):
    cands=[]
    while len(cands)<int(sys.argv[2]):
        m=mutate(random.choice(pop),int(sys.argv[3]))
        if m: cands.append(m)
    open('cl.txt','w').write('\n'.join(cands)+'\n')
    out=subprocess.run(['../six/six2','cl.txt'],capture_output=True,text=True).stdout
    sc=[]
    for L in out.splitlines():
        mm=re.match(r'H g=(\d+) n=(\d+) v=0 class=66666.*maxdl=(\d+) unr=(\d+) hist=([\d,]+)',L)
        if mm:
            g,n,mx,unr,h=int(mm[1]),int(mm[2]),int(mm[3]),int(mm[4]),list(map(int,mm[5].split(',')))
            sc.append(((mx,unr,h[4]+h[5],h[3]),g,n))
    sc.sort(reverse=True)
    print('round',rnd,'top',sc[:3],flush=True)
    if sc and sc[0][0][0]>=5 or (sc and sc[0][0][1]>0):
        open('found.txt','w').write(cands[sc[0][1]]+'\n'); print('FOUND'); break
    top=[cands[g] for s,g,n in sc if s[0]>=4][:20]
    if top: pop=top
