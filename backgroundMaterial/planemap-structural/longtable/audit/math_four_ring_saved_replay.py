"""Independent single-saved-member game certificate replay; no producer imports."""
import json, hashlib, itertools, time, resource
from collections import defaultdict
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(60,60))
base=Path('/Users/fulkanjou/GraphColour')
src=base/'backgroundMaterial/planemap-structural/longtable/explore-vhphi/vhphi-quad-explore-seed2-mixed0.json'
out=base/'backgroundMaterial/planemap-structural/longtable/audit/math-four-ring-saved-replay.json'
began=time.monotonic(); digest=hashlib.sha256(src.read_bytes()).hexdigest(); rec=json.loads(src.read_text()); m=rec['member']; n=m['n']; F=m['faces']; Q=set(m['phi']); hmarker=4
assert digest=='ca1c0921e24c005cf551a5c67e4876ad52319502ccea738df1aca3489015d224'
adj=[set() for _ in range(n)]; oriented=defaultdict(list); links=[{} for _ in range(n)]
for a,b,c in F:
 for x,y,z in [(a,b,c),(b,c,a),(c,a,b)]:
  adj[x].add(y); adj[y].add(x); oriented[tuple(sorted((x,y)))].append((x,y)); assert y not in links[x]; links[x][y]=z
assert all(len(x)==2 and x[0]==x[1][::-1] for x in oriented.values())
assert n-len(oriented)+len(F)==2
rotation=[]
for v in range(n):
 seq=[min(links[v])]
 while links[v][seq[-1]]!=seq[0]: seq.append(links[v][seq[-1]])
 assert len(seq)==len(adj[v]); rotation.append(seq)
s,t=m['deleted']; assert s in adj[t]; adj[s].remove(t); adj[t].remove(s)
assert [len(a) for a in adj]==m['degs']
assert all(len(adj[v])>=5 for v in range(n) if v not in Q)
assert all(len(adj[v]&Q)==2 for v in Q)
allowed=[v for v in range(n) if v not in Q]
def canon(c):
 mp={}; return tuple(hmarker if x==hmarker else mp.setdefault(x,len(mp)) for x in c)
def colourings(h):
 vs=[v for v in range(n) if v!=h]; state=[hmarker]*n; result=[]
 def dfs(i,top):
  if i==len(vs): result.append(tuple(state)); return
  v=vs[i]; blocked={state[u] for u in adj[v] if u!=h and u<v}
  for col in range(min(3,top+1)+1):
   if col not in blocked: state[v]=col; dfs(i+1,max(top,col))
  state[v]=hmarker
 dfs(0,-1); return result
states=sorted(x for h in allowed for x in colourings(h)); assert len(states)<10000
index={x:i for i,x in enumerate(states)}; assert len(index)==len(states)
def swaps(x):
 for a,b in itertools.combinations(range(4),2):
  active={v for v in range(n) if x[v] in (a,b)}; comps=[]
  while active:
   seed=min(active); active.remove(seed); stack=[seed]; comp={seed}
   while stack:
    v=stack.pop()
    for u in adj[v]&active:
     active.remove(u);comp.add(u);stack.append(u)
   comps.append(comp)
  boundary=[c for c in comps if c&Q]; assert len(boundary)<=2
  for comp in comps:
   variants=[comp]
   if comp&Q and len(boundary)==2: variants.append(comp|next(c for c in boundary if c is not comp))
   choices=[]
   for changed in variants:
    y=canon([b if v in changed and col==a else a if v in changed else col for v,col in enumerate(x)])
    assert all(y[u]!=y[v] for u in range(n) for v in adj[u] if y[u]!=4 and y[v]!=4)
    choices.append(index[y])
   yield tuple(sorted(set(choices)))
def actions(x):
 moves=list(swaps(x)); h=x.index(4); freq={k:sum(x[u]==k for u in adj[h]) for k in range(4)}
 for v in sorted(adj[h]-Q):
  if freq[x[v]]==1:
   y=list(x);y[h]=x[v];y[v]=4;moves.append((index[canon(y)],))
 return moves
moves=[actions(x) for x in states]
filled={i for i,x in enumerate(states) if len({x[u] for u in adj[x.index(4)]})<=3}
def attractor(acts):
 W=set(filled); rounds=0
 while True:
  extra={i for i in range(len(states)) if i not in W and any(all(j in W for j in move) for move in acts[i])}
  if not extra: return W,rounds
  W.update(extra);rounds+=1
winning,rounds=attractor(moves); losing=set(range(len(states)))-winning
assert all(any(j in losing for j in move) for i in losing for move in moves[i])
pure=[]
for x in states:
 actions0=[]
 for a,b in itertools.combinations(range(4),2):
  active={v for v in range(n) if x[v] in (a,b)}
  while active:
   seed=min(active); comp={seed};todo=[seed];active.remove(seed)
   while todo:
    v=todo.pop()
    for u in adj[v]&active: active.remove(u);comp.add(u);todo.append(u)
   y=canon([b if v in comp and col==a else a if v in comp else col for v,col in enumerate(x)])
   actions0.append((index[y],))
 pure.append(actions0)
purewin,purerounds=attractor(pure)
report={}; witnesses=[]
for h in m['deg5_off']:
 fans=[]; starts=[i for i,x in enumerate(states) if x[h]==4]; link=rotation[h]; assert len(link)==5
 reachable=set(starts); queue=list(starts)
 while queue:
  i=queue.pop()
  for move in moves[i]:
   for j in move:
    if j not in reachable: reachable.add(j);queue.append(j)
 assert len(reachable)==1186
 for fi in range(5):
  apex=link[fi]; p=link[(fi+2)%5]; q=link[(fi+3)%5]
  if p in adj[apex] or q in adj[apex]: continue
  admitted=[i for i in starts if states[i][apex]!=states[i][p] and states[i][apex]!=states[i][q]]
  bad=[i for i in admitted if i in losing]; assert bad
  fans.append([fi,sum(i in winning for i in admitted),len(admitted)])
  witnesses.append({'hole':h,'fan':fi,'state':states[bad[0]]})
  assert all(i in purewin for i in admitted)
 assert fans==rec['report'][str(h)]['fans']; report[str(h)]={'states':len(states),'fans':fans}
result={'input_sha256':digest,'scope':'one saved order-16 member only; independent post-hoc certificate replay','graph':{'n':n,'removed_edge':[s,t],'protected_vertices':sorted(Q),'edges':[[u,v] for u in range(n) for v in sorted(adj[u]) if u<v]},'states':len(states),'filled':len(filled),'winning':len(winning),'losing':len(losing),'attractor_rounds':rounds,'pure_winning':len(purewin),'pure_rounds':purerounds,'reports':report,'losing_kernel':[states[i] for i in sorted(losing)],'bad_start_per_fan':witnesses,'closure_certificate':'For each losing state and each player action, at least one successor is in losing_kernel; checked for all actions.','wall_seconds':round(time.monotonic()-began,3)}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['graph','reports','losing_kernel','bad_start_per_fan']},indent=2));print('output',out)
