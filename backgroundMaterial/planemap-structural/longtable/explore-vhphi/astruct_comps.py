import sys,itertools; sys.path.insert(0,'.')
from astruct_core import *
r=int(sys.argv[1]); rows=sys.argv[2].split(); cap=int(sys.argv[3])
adj=build(r);L=link(r)
s={'v':None,'c':cap}
for i in range(r):
    for t in range(5): s[(i,t)]=int(rows[i][t])
def nm(u): return 'c' if u=='c' else "%d.%d"%u
for pair in itertools.combinations(range(4),2):
    seen=set()
    print("pair",pair)
    for u in sorted([u for u in s if u!='v' and s[u] in pair],key=str):
        if u in seen: continue
        K=comp(adj,s,u,set(pair)); seen|=K
        prof=[sum(1 for x in K if x!='c' and x[0]==i) for i in range(r)]+[1 if 'c' in K else 0]
        print("  size %2d ring-profile %s"%(len(K),prof), "has top(ring0):",[nm(x) for x in K if x!='c' and x[0]==0])
