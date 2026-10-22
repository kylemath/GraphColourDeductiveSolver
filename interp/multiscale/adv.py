import sys; src=open('/tmp/claude-0/ms/msadv.py').read().split("if __name__=='__main__':")[0]; ADV=True; exec(src)
import collections,numpy as np
tot=collections.Counter(); byscale=collections.defaultdict(collections.Counter)
for name,adj in [('sphere%d'%s,sphere_tri(3000,s+10)) for s in range(2)]+[('ico17',icosphere(17))]:
    for seed in range(2):
        st=run(adj,seed)
        for L,sz,nc,R,nf in st:
            if nc: tot[R]+=1; byscale[int(np.log2(sz))][R]+=1
        print(name,seed,'adversarial radius so far',dict(sorted(tot.items())),flush=True)
for k in sorted(byscale): print('cluster size ~2^%d'%k,dict(sorted(byscale[k].items())))
