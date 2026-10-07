"""[exploratory] NightTwoPocket: the one-period m-neighbourhood relation on OPEN runs (gentri orders given, both orientations, all Hole6).
For every DL state u at position 9 (R1k2) whose next ten pi-states are DL and the tenth is again at position 9, record deg(m), the table-frame
colours of m's far neighbours ordered from z's side to y's side (start and end), and the break flags (pocket reaches w+) at start and end.
Uses ../30-nighta34/eng.py. Output: openscan-<orders>.jsonl lines (aggregated counts) and a summary on stdout."""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../30-nighta34'))
from eng import *
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from mdata import tabcol, HN
NM={(3,4):0,(1,1):1,(3,3):2,(1,0):3,(3,2):4,(1,4):5,(3,1):6,(1,3):7,(3,0):8,(1,2):9}
def pos(Hh,c):
    f=Hh.frame(c); return None if f is None else NM.get((f[1],f[2]))
def names(Hh):
    nm={'p':Hh.P,'m':Hh.Mi,'y':Hh.Y,'z':Hh.Z}
    for t in range(5):
        r=(t-Hh.q)%5; nm[['p','xp','x2','x3','xm'][r]]=Hh.X[t]; nm[['z','wp','w2','w3','y'][r]]=Hh.W[t]
    return nm
def tframe(c, nm):
    T=tabcol(9); phi={}
    for k in HN:
        if phi.get(c[nm[k]],T[k])!=T[k]: return None
        phi[c[nm[k]]]=T[k]
    return phi
def mfar(adj, nm):
    m=nm['m']; N=adj[m]-{nm['p']}; path=[nm['z']]
    while path[-1]!=nm['y']:
        nx=[u for u in N if u in adj[path[-1]] and u not in path and (len(path)==1 or u!=nm['p'])]
        nx=[u for u in nx if u!=nm['y']] or nx
        if len(path)>1 and nm['y'] in adj[path[-1]]: nx=[nm['y']]
        path.append(nx[0])
    return path[1:-1]
def pocket(adj, col, nm):
    P={nm['m']}; st=[nm['m']]
    while st:
        u=st.pop()
        for w in adj[u]:
            if w not in P and w not in (nm['p'],nm['xp']) and col[w] in (0,2): P.add(w); st.append(w)
    return nm['wp'] in P
C=Counter(); orders=[int(x) for x in sys.argv[1].split(',')]
out=open('openscan-%s.jsonl'%sys.argv[1].replace(',','_'),'w')
for n in orders:
  for gi,rot0 in graphs(n):
    for mirror in (0,1):
      rot=[list(reversed(r)) for r in rot0] if mirror else rot0
      for h in holes6(rot):
        Hh=H(rot,h); S=Hh.sp.states; idx=Hh.sp.index; A=Hh.sp.adj; I=Hh.sp.idx
        adj={I[v]:set(I[u] for u in A[v] if u in I) for v in A if v in I}
        nm=names(Hh); far=mfar(adj,nm)
        for k,c in enumerate(S):
            if not Hh.DL(c) or pos(Hh,c)!=9: continue
            seq=[c]; ok=True
            for i in range(10):
                c=Hh.pi(c)[0]
                if not Hh.DL(c): ok=False; break
                seq.append(c)
            if not ok or pos(Hh,seq[-1])!=9: continue
            f0=tframe(seq[0],nm); f1=tframe(seq[-1],nm)
            if f0 is None or f1 is None: C['frame error']+=1; continue
            c0={v:f0[x] for v,x in enumerate(seq[0])}; c1={v:f1[x] for v,x in enumerate(seq[-1])}
            s=tuple(c0[u] for u in far); e=tuple(c1[u] for u in far); b0=pocket(adj,c0,nm); b1=pocket(adj,c1,nm)
            key=(len(far)+3, s, e, b0, b1); C[key]+=1
            if b0 and b1: out.write(json.dumps(dict(n=n,g=gi,mirror=mirror,h=h,degm=len(far)+3,s=s,e=e))+'\n')
  print('order',n,'done',flush=True)
for k,v in sorted(C.items(),key=str): print(v,k)
