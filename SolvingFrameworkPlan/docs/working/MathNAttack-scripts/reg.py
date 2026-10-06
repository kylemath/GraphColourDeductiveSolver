import sys, subprocess
from nlab import *
P=sys.argv[1]
line=subprocess.run([P,"-m5","17","-a"],capture_output=True,text=True).stdout.splitlines()[1]
rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
for x in (5,15):
  ring=rot[x]
  for col in colourings_minus(adj,n,x):
    cl=classify(adj,x,ring,col)
    if cl is None: continue
    u,(D,al,be,ga)=cl
    pi=pair_info(adj,col,x); key=lambda p,q:(min(p,q),max(p,q))
    vec=(pi[key(D,al)],pi[key(D,be)],pi[key(D,ga)],pi[key(al,be)],pi[key(al,ga)],pi[key(be,ga)])
    if vec!=((1,0),(2,0),(2,0),(1,0),(1,0),(1,0)): continue
    if not all(not class_in_G(adj,n,x,u[j],col)[0] for j in (1,3,4)): continue
    nm={D:'D',al:'a',be:'b',ga:'g'}
    print("x",x,"u",u)
    for name,colr in (("alpha",al),("beta",be),("gamma",ga),("D",D)):
        col2={v:c for v,c in col.items() if c!=colr}
        # components of H=T-x-V_colr
        seen=set(); comps_=[]
        for s in col2:
            if s in seen: continue
            comp={s}; st=[s]
            while st:
                a=st.pop()
                for w in adj[a]:
                    if w in col2 and w not in comp: comp.add(w); st.append(w)
            seen|=comp; comps_.append(sorted(comp))
        print("  H minus class",name,":",len(comps_),"components", [ ''.join(sorted(nm[col[v]] for v in cc)) for cc in comps_])
