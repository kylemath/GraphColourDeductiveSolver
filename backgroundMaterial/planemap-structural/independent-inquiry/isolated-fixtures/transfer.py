import itertools,json
from pathlib import Path
canon=lambda a:tuple(dict((x,i) for i,x in enumerate(dict.fromkeys(a)))[x] for x in a)
rings=[a for a in itertools.product(range(4),repeat=5) if all(a[j]!=a[(j+1)%5] for j in range(5))]
patterns=sorted(set(map(canon,rings)))
def compatible(a,b):return all(a[j]!=b[j] and a[(j+1)%5]!=b[j] for j in range(5))
trans={a:sorted(set(canon(b) for b in rings if compatible(a,b))) for a in patterns}
for a in patterns:print(a,'->',trans[a])
# search named periodic alternating ring templates, independent samepair comps per length
for a in rings:
 for b in rings:
  if compatible(a,b) and compatible(b,a) and len(set(a))==len(set(b))==3:
   print('period2',a,b);break
 else:continue
 break
out={'ring_colourings':len(rings),'patterns':[list(a) for a in patterns], 'transitions':[{'source':a,'targets':bs}for a,bs in trans.items()]}
Path('/tmp/isolated-fixtures-work/transfer.json').write_text(json.dumps(out,indent=2)+'\n')
a=(0,1,0,1,2);pi=(2,3,1,0)
assert compatible(a,tuple(pi[x]for x in a))
def cylinder(m):
 cs=[];ring=a
 for i in range(m):cs.extend(ring);ring=tuple(pi[x]for x in ring)
 adj=[set()for _ in range(5*m+2)]
 def edge(u,v):adj[u].add(v);adj[v].add(u)
 for i in range(m):
  for j in range(5):
   edge(5*i+j,5*i+(j+1)%5)
   if i<m-1:
    edge(5*i+j,5*(i+1)+j);edge(5*i+j,5*(i+1)+(j-1)%5)
 for j in range(5):edge(5*m,j);edge(5*m+1,5*(m-1)+j)
 cs.extend([next(iter(set(range(4))-set(cs[:5]))),next(iter(set(range(4))-set(cs[-5:])))])
 assert all(cs[u]!=cs[v]for u,ns in enumerate(adj)for v in ns)
 paircomps={}
 for x,y in itertools.combinations(range(4),2):
  rem={u for u,c in enumerate(cs)if c in (x,y)};comps=[]
  while rem:
   seed=min(rem);stack=[seed];comp=set();rem.remove(seed)
   while stack:
    u=stack.pop();comp.add(u)
    for v in adj[u]&rem:rem.remove(v);stack.append(v)
   comps.append(sorted(comp))
  paircomps[str((x,y))]=comps
 return cs,paircomps
for m in [2,3,4,8,12,20]:
 cs,pcs=cylinder(m)
 print('construct',m,'component sizes',{k:[len(c)for c in cs]for k,cs in pcs.items()})
Path('/tmp/isolated-fixtures-work/cylinder20-components.json').write_text(json.dumps({'colours':cylinder(20)[0],'components':cylinder(20)[1]},indent=2)+'\n')
# All template colour permutations; fixed base ring must use three colours for caps.
best=[]
for aa in patterns:
 if len(set(aa))!=3:continue
 for pp in itertools.permutations(range(4)):
  if not compatible(aa,tuple(pp[x]for x in aa)):continue
  a,pi=aa,pp
  _,pcs=cylinder(20)
  interior={pair:[comp for comp in comps if all(5<=v<95 for v in comp)]for pair,comps in pcs.items()}
  count=max(map(len,interior.values()))
  best.append((count,aa,pp,{pair:[len(c)for c in cs]for pair,cs in interior.items()}))
print('interior switches best',max(best))
# shortest quotient path lengths show compression; reachability doesn't fix named end colours.
for src in patterns:
 dist={src:0};todo=[src]
 for u in todo:
  for v in trans[u]:
   if v not in dist:dist[v]=dist[u]+1;todo.append(v)
 assert len(dist)==10
 print('diameter from',src,max(dist.values()))
