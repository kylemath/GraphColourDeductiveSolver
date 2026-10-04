"""Cheap component-mass potential falsification; no reachability/attractor rank."""
import argparse,itertools,json,hashlib
from pathlib import Path
ASCII='20 bcdef,afghic,abijd,acjkle,adlmf,aemgb,bfmnoh,bgopqi,bhqjc,ciqrkd,djrsl,dksme,elsngf,gmsto,gntph,hotrq,hprji,jqptsk,krtnml,nsrpo'
def canon(c):
 d={};return tuple(d.setdefault(x,len(d)) for x in c)
def colors(H,V):
 c={};out=[]
 def go(m):
  if len(c)==len(V):out.append(canon([c[v] for v in V]));return
  v=max((v for v in V if v not in c),key=lambda v:(len({c[u] for u in H[v] if u in c}),len(H[v]),-v));bad={c[u] for u in H[v] if u in c}
  for a in range(min(3,m+1)+1):
   if a not in bad:c[v]=a;go(max(m,a));del c[v]
 go(-1);return sorted(set(out))
r=8;rot=[[ord(c)-97 for c in row] for row in ASCII.split(' ',1)[1].split(',')]
assert len(rot)==20 and all(v in rot[w] for v in range(20) for w in rot[v])
V=[v for v in range(20) if v!=r];H={v:set(rot[v])-{r} for v in V};B=rot[r];Bset=set(B);C=colors(H,V)
def data(c):
 cd=dict(zip(V,c));moves=[];q=0
 assert all(cd[v]!=cd[w] for v in V for w in H[v])
 for a,b in itertools.combinations(range(4),2):
  pending={v for v in V if cd[v] in (a,b)}
  while pending:
   seed=min(pending);K={seed};stack=[seed];pending.remove(seed)
   for v in stack:
    ns=H[v]&pending;pending-=ns;K|=ns;stack.extend(ns)
   if K&Bset:q+=len(K-Bset)**2
   swapped=canon([b if cd[v]==a and v in K else a if cd[v]==b and v in K else cd[v] for v in V])
   moves.append(((a,b,tuple(sorted(K))),swapped))
 return (max(0,len({cd[v] for v in B})-3),q),moves
D={c:data(c) for c in C};bad=[]
for c,(score,moves) in D.items():
 assert all(t in D for _,t in moves)
 assert all(c in [z for _,z in D[t][1]] for _,t in moves)
 if score[0] and not any(D[t][0]<score for _,t in moves):bad.append(c)
assert len(C)==198 and len(bad)==3
out={'scope':'Finite falsification of this explicit strict-descent formula only; no general escape theorem is refuted.','formula':'lex(p,q), p=max(0, distinct boundary colours-3), q=sum over six colour pairs and boundary-touching components K of |K minus B| squared','ascii':ASCII,'ascii_sha256':hashlib.sha256(ASCII.encode()).hexdigest(),'root':r,'states':len(C),'non_target':sum(s[0]>0 for s,m in D.values()),'local_minima':len(bad),'vertex_order':V,'boundary_cyclic_order':B,'all_local_minimum_colorings':bad}
c=bad[0];score,moves=D[c]
out['witness']={'coloring':c,'potential':score,'successor_potentials':sorted(set(D[t][0] for _,t in moves)),'moves':[{'pair':a[:2],'component':a[2],'successor':t,'potential':D[t][0]} for a,t in moves]}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('component-mass-results.json'))
args=parser.parse_args()
args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'states':len(C),'non_target':out['non_target'],'local_minima':len(bad),'first_local_minimum_potential':score,'successor_potentials':out['witness']['successor_potentials']}))
