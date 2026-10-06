"""Independent exact trace-game solver on one saved member; no producer imports."""
import json, hashlib, itertools, time, resource
from pathlib import Path
from functools import lru_cache
resource.setrlimit(resource.RLIMIT_CPU,(600,600))
ROOT=Path('/Users/fulkanjou/GraphColour'); D=ROOT/'backgroundMaterial/planemap-structural/longtable'
source=D/'explore-vhphi/vhphi-quad-explore-seed2-mixed0.json'; expected=D/'explore-vhphi/trace-game-order16.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(source)=='ca1c0921e24c005cf551a5c67e4876ad52319502ccea738df1aca3489015d224'
assert sha(expected)=='e61b0ef59039b006f4f3bc720499d8edd24729ed2fe983dd3664480d7f127962'
member=json.loads(source.read_text())['member']; want=json.loads(expected.read_text()); n=member['n']; adj=[set() for _ in range(n)]; nextedge=[{} for _ in range(n)]
for a,b,c in member['faces']:
 for v,u,w in [(a,b,c),(b,c,a),(c,a,b)]: adj[v].add(u);adj[u].add(v);nextedge[v][u]=w
rot=[]
for h in range(n):
 link=[min(nextedge[h])]
 while nextedge[h][link[-1]]!=link[0]: link.append(nextedge[h][link[-1]])
 assert len(link)==len(adj[h]);rot.append(link)
s,t=member['deleted'];adj[s].remove(t);adj[t].remove(s)
quad=[s,nextedge[t][s],t,nextedge[s][t]]; assert set(quad)==set(member['phi'])
pairs=list(itertools.combinations(range(4),2)); masks=[(1<<a)|(1<<b) for a,b in pairs]; complements=[masks.index(15^m) for m in masks]; boundary=set(quad); began=time.monotonic()
def starts(h):
 vs=[v for v in range(n) if v!=h]; c=[4]*n; result=[]
 def rec(i,largest):
  if i==len(vs): result.append(tuple(c));return
  v=vs[i]; banned={c[u] for u in adj[v] if u<v and u!=h}
  for col in range(min(3,largest+1)+1):
   if col not in banned:c[v]=col;rec(i+1,max(largest,col))
  c[v]=4
 rec(0,-1);return result
@lru_cache(None)
def bit_options(word):
 rel={}
 for p,m in enumerate(masks):
  hit=tuple(i for i,col in enumerate(word) if m&(1<<col))
  if hit==(0,2):rel[p]=0
  elif hit==(1,3):rel[p]=1
 options=[]; keys=list(rel)
 for subset in range(1<<len(keys)):
  on=[keys[i] for i in range(len(keys)) if subset&(1<<i)]
  if all(rel[p]==rel[r] or masks[p]&masks[r] for p,r in itertools.combinations(on,2)): options.append(sum(1<<p for p in on))
 return rel,tuple(options)
def opts(c):return bit_options(tuple(c[v] for v in quad))
def comps(c,p):
 a,b=pairs[p]; unused={v for v in range(n) if c[v] in (a,b)}; result=[]
 while unused:
  seed=min(unused);unused.remove(seed); todo=[seed]; comp={seed}
  while todo:
   v=todo.pop()
   for u in adj[v]&unused:unused.remove(u);todo.append(u);comp.add(u)
  result.append(comp)
 return result
summary={}; total=0
for hole in member['deg5_off']:
 begun=time.monotonic(); cs=starts(hole); initial=[(c,b) for c in cs for b in opts(c)[1]]; nodes=list(dict.fromkeys(initial)); lookup={x:i for i,x in enumerate(nodes)}; actions=[]; terminal=set(); cursor=0
 while cursor<len(nodes):
  c,bits=nodes[cursor]
  if len({c[u] for u in adj[hole]})<=3:terminal.add(cursor);actions.append([]);cursor+=1;continue
  rel,_=opts(c); player=[]
  for p,(a,b) in enumerate(pairs):
   parts=comps(c,p); touching=[K for K in parts if K&boundary]
   for K in parts:
    change=K
    if p in rel and bits&(1<<p) and K&boundary:
     change=set().union(*touching)
    nxt=tuple(b if col==a and v in change else a if v in change else col for v,col in enumerate(c))
    assert all(nxt[u]!=nxt[v] for u in range(n) for v in adj[u] if nxt[u]!=4 and nxt[v]!=4)
    rel2,allnew=opts(nxt); assert (p in rel)==(p in rel2); complement=complements[p];assert (complement in rel)==(complement in rel2)
    frozen=(1<<p)|(1<<complement); outcomes=[]
    for newbits in allnew:
     if newbits&frozen != bits&frozen:continue
     node=(nxt,newbits)
     if node not in lookup:lookup[node]=len(nodes);nodes.append(node)
     outcomes.append(lookup[node])
    assert outcomes;player.append(tuple(outcomes))
  actions.append(player);cursor+=1
  if len(nodes)>100000:raise RuntimeError('inconclusive: 100000-state cap reached')
 W=set(terminal);rounds=0
 while True:
  added={i for i,A in enumerate(actions) if i not in W and any(all(j in W for j in O) for O in A)}
  if not added:break
  W.update(added);rounds+=1
 fanreport=[]; witness=[]; link=rot[hole]
 for fi in range(5):
  apex=link[fi];u=link[(fi+2)%5];v=link[(fi+3)%5]
  if u in adj[apex] or v in adj[apex]:continue
  admitted=[lookup[(c,b)] for c,b in initial if c[apex]!=c[u] and c[apex]!=c[v]]
  fanreport.append([fi,sum(i in W for i in admitted),len(admitted)])
  if any(i not in W for i in admitted):witness.append(next(nodes[i] for i in admitted if i not in W))
 assert fanreport==want[str(hole)],(hole,fanreport,want[str(hole)])
 summary[str(hole)]={'positions':len(nodes),'initial_positions':len(initial),'terminal':len(terminal),'winning':len(W),'losing':len(nodes)-len(W),'attractor_rounds':rounds,'fans':fanreport,'seconds':round(time.monotonic()-begun,3)};total+=len(nodes);print(hole,summary[str(hole)],flush=True)
output={'scope':'one saved order-16 member, exact PURE trace game, independently rebuilt; no new graph enumeration','input_sha256':sha(source),'expected_sha256':sha(expected),'quadrilateral':quad,'reports':summary,'total_positions':total,'all_fan_counts_matched':True,'all_admitted_start_bit_positions_winning':all(all(w==a for _,w,a in R['fans']) for R in summary.values()),'seconds':round(time.monotonic()-began,3),'broader_claims':{'435_triangle_members':'not replayed: saved summaries omit graph inputs','4004_quad_members':'not replayed: saved summaries omit nonfailure graph inputs','2146_gluings':'not replayed: saved report omits far-side graph inputs'}}
path=D/'audit/math-trace-saved-replay.json'; data=json.dumps(output,indent=2)+'\n';assert len(data)<100000000;path.write_text(data);print('OUTPUT',path,'TOTAL',output['seconds'],flush=True)
