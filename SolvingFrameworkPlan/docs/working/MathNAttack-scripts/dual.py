import sys, subprocess, itertools
from nlab import *
P=sys.argv[1]; N=int(sys.argv[2]); idxs=[int(a) for a in sys.argv[3:]]
tot=0; bad=0; nonconn=0
for order,gi in [(N,i) for i in idxs]:
    line=subprocess.run([P,"-m5",str(order),"-a"],capture_output=True,text=True).stdout.splitlines()[gi]
    rot=parse(line); n=len(rot); adj=[set(r) for r in rot]
    for x in range(n):
        if len(rot[x])!=5: continue
        ring=rot[x]
        for col in colourings_minus(adj,n,x):
            for i,j in itertools.combinations(range(5),2):
                a,b=ring[i],ring[j]
                p,q=col[a],col[b]
                # pair containing both colours
                S={p,q}
                if len(S)==1:
                    S={p,(p+1)%4}   # arbitrary extension? skip same-colour
                    continue
                comp_idx=comps(adj,col,S,x)[1]
                disc = comp_idx[a]!=comp_idx[b]
                comp=set(range(4))-S
                # complement path between ring vertices s,t separating a,b
                found=False
                for k,l in itertools.combinations(range(5),2):
                    s,t=ring[k],ring[l]
                    if col[s] in comp and col[t] in comp:
                        # separation: a, b in different arcs of cycle minus {k,l}
                        def arc(m):
                            if m in (k,l): return None
                            return 0 if (k<m<l) else 1
                        if arc(i) is None or arc(j) is None or arc(i)==arc(j): continue
                        if path_in(adj,col,comp,s,t,x) is not None: found=True; break
                tot+=1
                if disc: nonconn+=1
                if disc!=found: bad+=1
print("tests",tot,"disconnected",nonconn,"mismatches",bad)
