import json,itertools,collections,hashlib
import networkx as nx
from pathlib import Path
import argparse
parser=argparse.ArgumentParser(description='Independent Kittell Kempe-state replay; computational research evidence only.')
parser.add_argument('--input', type=Path, default=Path(__file__).resolve().parents[2] / 'backgroundMaterial/agent1720/groups/K6_kittell.json')
parser.add_argument('--output', type=Path, default=Path(__file__).with_name('replay-results.json'))
args=parser.parse_args()
src=args.input
data=json.loads(src.read_text());G=nx.Graph();G.add_edges_from(data['edges']);ok,emb=nx.check_planarity(G); assert ok
pairs=list(itertools.combinations(range(4),2))
def canon(c):
 d={};return tuple(d.setdefault(x,len(d)) for x in c)
def enumerate_colors(H,vs):
 adj={v:set(H[v]) for v in vs}; c={};out=[]
 def rec(maxcol):
  if len(c)==len(vs):out.append(canon([c[v] for v in vs]));return
  v=max((v for v in vs if v not in c),key=lambda v:(len({c[u] for u in adj[v] if u in c}),len(adj[v]),-v))
  bad={c[u] for u in adj[v] if u in c}
  for a in range(min(3,maxcol+1)+1):
   if a not in bad:c[v]=a;rec(max(maxcol,a));del c[v]
 rec(-1);return sorted(set(out))
def comps(H,vs,c,a,b):
 return list(nx.connected_components(H.subgraph([v for v,k in zip(vs,c) if k in (a,b)])))
def signature(H,vs,c,B):
 # Normalize colour names by boundary first, then full vertex order.
 order=B+[v for v in vs if v not in B]; cd=dict(zip(vs,c));mp={};cc={v:mp.setdefault(cd[v],len(mp)) for v in order}
 parts=[]
 for a,b in pairs:
  cs=comps(H,vs,[cc[v] for v in vs],a,b)
  parts.append(tuple(sorted(tuple(i for i,v in enumerate(B) if v in C) for C in cs if any(v in C for v in B))))
 return (tuple(cc[v] for v in B),tuple(parts)),cc
allstates=[];report=[];collision=None
for root in sorted(v for v in G if G.degree(v)==5):
 H=G.copy();H.remove_node(root);vs=sorted(H);B=list(emb.neighbors_cw_order(root));B=B[B.index(min(B)):]+B[:B.index(min(B))]
 colors=enumerate_colors(H,vs);assert all(all(c[vs.index(u)]!=c[vs.index(v)] for u,v in H.edges) for c in colors);idx={c:i for i,c in enumerate(colors)};trans=[];sigs=[];actions=[]
 for c in colors:
  sig,cc=signature(H,vs,c,B);sigs.append(sig);t=set();acts={}
  for a,b in pairs:
   for C in comps(H,vs,[cc[v] for v in vs],a,b):
    swapped=canon([b if cc[v]==a and v in C else a if cc[v]==b and v in C else cc[v] for v in vs]);j=idx[swapped];t.add(j)
    boundary=tuple(i for i,v in enumerate(B) if v in C)
    if boundary:acts[(a,b,boundary)]=j
  trans.append(t);actions.append(acts)
 good={i for i,c in enumerate(colors) if len({c[vs.index(v)] for v in B})<=3};dist={i:0 for i in good};q=collections.deque(good)
 # swaps involutive modulo global colour symmetry, thus undirected.
 while q:
  i=q.popleft()
  for j in trans[i]:
   if j not in dist:dist[j]=dist[i]+1;q.append(j)
 assert len(dist)==len(colors)
 assert all(i in trans[j] for i,ts in enumerate(trans) for j in ts)
 stategraph=nx.Graph();stategraph.add_nodes_from(range(len(colors)));stategraph.add_edges_from((i,j) for i,ts in enumerate(trans) for j in ts);assert nx.number_connected_components(stategraph)==1
 groups=collections.defaultdict(list)
 for i,s in enumerate(sigs):groups[s].append(i)
 for s,ids in groups.items():
  succ=[{sigs[j] for j in trans[i]} for i in ids]
  if collision is None and len(set(s[0]))==4 and any(x!=succ[0] for x in succ[1:]):
   k=next(k for k,x in enumerate(succ) if x!=succ[0]);collision={'root':root,'boundary':B,'colorings':[list(colors[ids[0]]),list(colors[ids[k]])],'vertex_order':vs,'signature':repr(s),'successor_counts':[len(succ[0]),len(succ[k])],'difference':sorted(map(repr,succ[0]^succ[k]))}
 for i,s in enumerate(sigs):allstates.append((root,i,s,{a:sigs[j] for a,j in actions[i].items()},i in good))
 report.append({'root':root,'boundary':B,'states':len(colors),'signatures':len(groups),'max_distance':max(dist.values())})
groups=collections.defaultdict(list)
for row in allstates:groups[row[2]].append(row)
winning={s for s,rows in groups.items() if all(r[4] for r in rows)};rounds=0
while True:
 new=set()
 for s,rows in groups.items():
  if s in winning:continue
  available=set(rows[0][3])
  for r in rows[1:]:available.intersection_update(r[3])
  if any(all(r[3][a] in winning for r in rows) for a in available):new.add(s)
 if not new:break
 winning.update(new);rounds+=1
root_games=[]
for root in sorted({r[0] for r in allstates}):
 rg=collections.defaultdict(list)
 for row in allstates:
  if row[0]==root:rg[row[2]].append(row)
 win={s for s,rows in rg.items() if all(r[4] for r in rows)}
 while True:
  new=set()
  for s,rows in rg.items():
   if s in win:continue
   available=set(rows[0][3])
   for r in rows[1:]:available.intersection_update(r[3])
   if any(all(r[3][a] in win for r in rows) for a in available):new.add(s)
  if not new:break
  win.update(new)
 root_games.append({'root':root,'signatures':len(rg),'robust_losing':len(rg)-len(win)})
out={'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'graph':{'n':len(G),'m':G.number_of_edges(),'planar':ok},'per_root':report,'root_dependent_games':root_games,'combined_signatures':len(groups),'robust_winning':len(winning),'robust_losing':len(groups)-len(winning),'attractor_rounds':rounds,'collision':collision,'losing_signatures':sorted(map(repr,set(groups)-winning))}
args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('collision','losing_signatures')},indent=2));print('collision',collision and collision['root'])
