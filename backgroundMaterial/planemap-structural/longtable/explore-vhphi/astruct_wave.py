import sys; sys.path.insert(0,'.')
from astruct_core import *
r=int(sys.argv[1]); rows=sys.argv[2].split(); cap=int(sys.argv[3])
adj=build(r);L=link(r)
s={'v':None,'c':cap}
for i in range(r):
    for t in range(5): s[(i,t)]=int(rows[i][t])
def cr(x):
    mp={};o=[]
    for y in x:
        if y not in mp: mp[y]=len(mp)
        o.append(mp[y])
    return tuple(o)
T=20
states=[]
for n in range(T): states.append(s); s=F(adj,s,L)
ringseq=[[cr([st[(i,t)] for t in range(5)]) for st in states] for i in range(r)]
def rotc(x,k): return x[k:]+x[:k]
for i in range(r-1):
    for k in range(5):
        for d in range(T):
            if all(cr(rotc(ringseq[i+1][n],k))==ringseq[i][(n+d)%T] for n in range(T)):
                print("ring",i+1,"at time n  ==  ring",i,"at time n+%d  up to renaming and rotation %d"%(d,k))
