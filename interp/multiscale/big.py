import sys; sys.argv=['x']; exec(open('ms.py').read().split("if __name__=='__main__':")[0])
import collections,numpy as np
for name,adj in [('sphere12k',sphere_tri(12000,7)),('ico40',icosphere(40))]:
    st=run(adj,0); byL=collections.defaultdict(list)
    for L,sz,nc,R,nf in st: byL[L].append((sz,nc,R,nf))
    print(name,len(adj),flush=True)
    for L in sorted(byL):
        v=byL[L]; Rs=[x[2] for x in v if x[1]>0]
        print('  L%2d clusters %5d meanSize %8.1f withConflicts %4d radius %s'%(L,len(v),np.mean([x[0] for x in v]),len(Rs),dict(sorted(collections.Counter(Rs).items()))),flush=True)
