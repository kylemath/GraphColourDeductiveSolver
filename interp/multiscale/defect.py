import sys,random,collections
src=open('/tmp/claude-0/ms/ms.py').read().split("if __name__=='__main__':")[0]; exec(src)
def flip_defects(adj,nflips,rng,maxdeg=8):
    # flip edge (a,b) with common nbrs c,d -> edge (c,d); keep degrees in [5,maxdeg]
    n=len(adj); done=0; tries=0
    while done<nflips and tries<nflips*200:
        tries+=1; a=rng.randrange(n); b=rng.choice(sorted(adj[a])); cn=adj[a]&adj[b]
        if len(cn)!=2: continue
        c,d=cn
        if d in adj[c]: continue
        if len(adj[a])-1<5 or len(adj[b])-1<5 or len(adj[c])+1>maxdeg or len(adj[d])+1>maxdeg: continue
        adj[a].discard(b); adj[b].discard(a); adj[c].add(d); adj[d].add(c); done+=1
    return adj
rng=random.Random(5)
adj=flip_defects(icosphere(17),1500,rng)
print('degrees',sorted(collections.Counter(len(a) for a in adj).items()))
import pickle; pickle.dump(adj,open('/tmp/claude-0/ms/defect_ico17.pkl','wb'))
stats=[]
for seed in range(2):
    st=run(adj,seed); byL=collections.defaultdict(list)
    for L,sz,nc,R,nf in st: byL[L].append((sz,nc,R))
    for L in sorted(byL):
        v=byL[L]; Rs=[x[2] for x in v if x[1]>0]
        print(' seed',seed,'L%2d meanSize %7.1f conflicts %4d radius %s'%(L,np.mean([x[0] for x in v]),len(Rs),dict(sorted(collections.Counter(Rs).items()))),flush=True)
