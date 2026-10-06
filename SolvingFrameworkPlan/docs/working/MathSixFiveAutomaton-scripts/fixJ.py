import pickle, sys, collections
from auto import *
nodes,groups,bad0,inits=pickle.load(open('fix.pkl','rb'))
def joins(c,T,R):
    # number of outside joins = (#same-class arcs) - (#blocks), computed on ring
    cls=[c[5+i] in TYPES[T][0] for i in range(10)]
    if all(x==cls[0] for x in cls): return 0
    narcs=sum(1 for i in range(10) if cls[i]!=cls[i-1])
    return narcs-len(set(R))
def solve(J):
    allowed=lambda n: joins(*n)<=J
    bad={n for n,v in nodes.items() if not v[0] and allowed(n)}
    while True:
        gb={gk:any(n in bad for n in L) for gk,L in groups.items()}
        rem=[n for n in bad if not (all(m in bad for m in nodes[n][1]) and all((m in bad) and all(gb[g_] for g_ in gs) for m,gs in nodes[n][2]))]
        if not rem: break
        bad-=set(rem)
    win=sum(all(any(n in bad for n in per[T]) for T in range(3)) for p,per in inits)
    return bad,win
if __name__=="__main__":
  for J in range(0,6):
      bad,win=solve(J)
      print('J',J,'bad nodes',len(bad),'colourings',len({n[0] for n in bad}),'patterns trapped',win,flush=True)
      if win==74: pickle.dump(bad,open(f'badJ{J}.pkl','wb')); break
  