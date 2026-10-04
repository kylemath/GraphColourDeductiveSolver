import argparse,json,itertools,collections,hashlib
from pathlib import Path
import networkx as nx
P=list(itertools.combinations(range(4),2))
def canon(c):
 d={};return tuple(d.setdefault(x,len(d)) for x in c)
def colors(H,V):
 adj={v:set(H[v]) for v in V}; c={};out=[]
 def go(m):
  if len(c)==len(V):out.append(canon([c[v] for v in V]));return
  v=max((v for v in V if v not in c),key=lambda v:(len({c[u] for u in adj[v] if u in c}),len(adj[v]),-v));bad={c[u] for u in adj[v] if u in c}
  for a in range(min(3,m+1)+1):
   if a not in bad:c[v]=a;go(max(m,a));del c[v]
 go(-1);return sorted(set(out))
def sig(H,V,c,B):
 mp={};cd=dict(zip(V,c));cc={v:mp.setdefault(cd[v],len(mp)) for v in B+[v for v in V if v not in B]};cs={p:list(nx.connected_components(H.subgraph([v for v in V if cc[v] in p]))) for p in P}
 parts=tuple(tuple(sorted(tuple(i for i,v in enumerate(B) if v in C) for C in cs[p] if C.intersection(B))) for p in P)
 return (tuple(cc[v] for v in B),parts),cc,cs

def attractor(S,A,good,key=None):
 if key is None:key=lambda i:S[i]
 gr=collections.defaultdict(list)
 for i in range(len(S)):gr[key(i)].append(i)
 win={s for s,ids in gr.items() if all(i in good for i in ids)};r=0
 while True:
  new=set()
  for s,ids in gr.items():
   if s in win:continue
   common=set(A[ids[0]])
   for i in ids[1:]:common.intersection_update(A[i])
   if any(all(key(A[i][a]) in win for i in ids) for a in common):new.add(s)
  if not new:break
  win|=new;r+=1
 return win,gr,r

def policy_certificate(keys,actions,good):
 gr=collections.defaultdict(list)
 for i,k in enumerate(keys):gr[k].append(i)
 rank={k:0 for k,ids in gr.items() if all(i in good for i in ids)};chosen={};layer=0
 while True:
  nxt={}
  for k,ids in gr.items():
   if k in rank:continue
   common=set(actions[ids[0]])
   for i in ids[1:]:common.intersection_update(actions[i])
   winning=[a for a in common if all(keys[actions[i][a]] in rank for i in ids)]
   if winning:nxt[k]=min(winning,key=repr)
  if not nxt:break
  layer+=1
  for k,a in nxt.items():rank[k]=layer;chosen[k]=a
 for k,a in chosen.items():
  assert all(a in actions[i] and rank[keys[actions[i][a]]] < rank[k] for i in gr[k])
 entries=[{'observation':repr(k),'rank':rank.get(k),'action':chosen.get(k),'states':len(ids)} for k,ids in sorted(gr.items(),key=lambda item:repr(item[0]))]
 # Same old signature, different bit, distinct chosen boundary actions.
 distinct=[]
 for k in rank:
  if (k[0],not k[1]) in rank and k[1] is False and chosen.get(k)!=chosen.get((k[0],True)):
   if chosen.get(k) is not None and chosen.get((k[0],True)) is not None:
    distinct.append({'signature':repr(k[0]),'bit0_action':chosen[k],'bit1_action':chosen[(k[0],True)],'bit0_coloring_index':gr[k][0],'bit1_coloring_index':gr[(k[0],True)][0]})
 return {'groups':len(gr),'losing_groups':len(gr)-len(rank),'max_rank':max(rank.values(),default=0),'entries':entries,'different_actions_by_bit':distinct}

def analyze(G,name):
 planar,E=nx.check_planarity(G);assert planar
 results=[];pooled_keys=[];pooled_actions=[];pooled_good=set()
 for root in sorted(v for v in G if G.degree(v)==5):
  H=G.copy();H.remove_node(root);V=sorted(H);B=list(E.neighbors_cw_order(root));B=B[B.index(min(B)):]+B[:B.index(min(B))]
  C=colors(H,V);idx={c:i for i,c in enumerate(C)};S=[];A=[];interior=[];full=[];ccs=[];components=[]
  for c in C:
   s,cc,cs=sig(H,V,c,B);S.append(s);ccs.append(cc);components.append(cs);aa={};ii={};ff={}
   assert all(c[V.index(u)] != c[V.index(v)] for u,v in H.edges)
   for a,b in P:
    for K in cs[(a,b)]:
     j=idx[canon([b if cc[v]==a and v in K else a if cc[v]==b and v in K else cc[v] for v in V])];bb=tuple(k for k,v in enumerate(B) if v in K)
     if bb:aa[(a,b,bb)]=j
     else:
      for seed in K:ii[(a,b,seed)]=j
     for seed in K:ff[(a,b,seed)]=j
   A.append(aa);interior.append(ii);full.append(ff)
  good={i for i,s in enumerate(S) if len(set(s[0]))<=3};win,gr,rounds=attractor(S,A,good)
  ST=nx.Graph();ST.add_nodes_from(range(len(C)));ST.add_edges_from((i,j) for i,aa in enumerate(full) for j in aa.values());
  assert all(i in full[j].values() for i,aa in enumerate(full) for j in aa.values())
  dist={i:0 for i in good};q=collections.deque(good)
  while q:
   i=q.popleft()
   for j in ST[i]:
    if j not in dist:dist[j]=dist[i]+1;q.append(j)
  detail=[]
  for s in sorted(set(gr)-win):
   ids=gr[s];rep=next(k for k in range(4) if s[0].count(k)==2)
   common=set(interior[ids[0]])
   for i in ids[1:]:common.intersection_update(interior[i])
   interior_winners=[a for a in sorted(common) if all(S[interior[i][a]] in win for i in ids)]
   repcommon=set(A[ids[0]])
   for i in ids[1:]:repcommon.intersection_update(A[i])
   repeated_winners=[a for a in sorted(repcommon) if rep in a[:2] and all(S[A[i][a]] in win for i in ids)]
   detail.append({'signature':repr(s),'boundary_colors':s[0],'states':len(ids),'repeated_color':rep,'common_interior_actions_to_old_winning':interior_winners,'common_repeated_color_actions_to_old_winning':repeated_winners,'states_with_some_interior_escape':sum(any(S[j] in win for j in interior[i].values()) for i in ids),'states_with_some_repeated_color_escape':sum(any(rep in a[:2] and S[j] in win for a,j in A[i].items()) for i in ids),'representative_colors':C[ids[0]]})
  extended=[dict(a)|{('interior',)+p:j for p,j in ii.items()} for a,ii in zip(A,interior)];ew,eg,er=attractor(S,extended,good)
  # Search directly evaluable single bits: seed component for a named pair meets boundary.
  named_bits=[any(min(V) in K and bool(K.intersection(B)) for K in cs[(1,3)]) for cs in components]
  nw,ng,nr=attractor(S,A,good,lambda i:(S[i],named_bits[i]))
  named_losing=sum(1 for i in range(len(S)) if (S[i],named_bits[i]) not in nw)
  named_keys=[(S[i],named_bits[i]) for i in range(len(S))]
  certificate=policy_certificate(named_keys,A,good)
  for witness in certificate['different_actions_by_bit']:
   witness['bit0_colors']=C[witness['bit0_coloring_index']];witness['bit1_colors']=C[witness['bit1_coloring_index']]
  offset=len(pooled_keys);pooled_keys.extend(named_keys);pooled_actions.extend({a:j+offset for a,j in aa.items()} for aa in A);pooled_good.update(i+offset for i in good)
  refinements=[]
  for p in P:
   for v in V:
    bits=[any(v in K and bool(K.intersection(B)) for K in cs[p]) for cs in components]
    w,g,r=attractor(S,A,good,lambda i:(S[i],bits[i]))
    losing=sum(1 for i in range(len(S)) if (S[i],bits[i]) not in w)
    if losing==0 and len(win)<len(gr):refinements.append({'pair':p,'seed':v,'bit':'the seed belongs to a bichromatic component meeting the boundary','groups':len(g),'rounds':r})
  results.append({'root':root,'vertex_order':V,'boundary':B,'states':len(C),'kempe_components':nx.number_connected_components(ST),'targetless_components':sum(not(set(k)&good) for k in nx.connected_components(ST)),'reachable_states':len(dist),'max_target_distance':max(dist.values(),default=None),'boundary_signatures':len(gr),'old_losing':len(gr)-len(win),'interior_augmented_losing':len(eg)-len(ew),'losing_details':detail,'named_min_vertex_13_bit':{'seed':min(V),'groups':len(ng),'losing_states':named_losing,'attractor_rounds':nr,'certificate':certificate},'successful_single_bit_boundary_refinements':refinements})
  print(name,root,len(C),'old losing',len(gr)-len(win),'extended',len(eg)-len(ew),'bits',len(refinements),flush=True)
 return {'graph':name,'vertices':len(G),'edges':G.number_of_edges(),'planar':planar,'degrees':dict(G.degree),'roots':results,'pooled_min_vertex_13_bit':policy_certificate(pooled_keys,pooled_actions,pooled_good),'kill_witness_found':all(r['targetless_components']>0 for r in results)}
if __name__=='__main__':
 parser=argparse.ArgumentParser(description='Finite Kittell/icosahedron Kempe observation experiments.')
 parser.add_argument('--input',type=Path,default=Path(__file__).resolve().parent.parent/'agent1720/groups/K6_kittell.json')
 parser.add_argument('--output',type=Path,default=Path(__file__).with_name('results.json'))
 args=parser.parse_args();path=args.input;d=json.loads(path.read_text());G=nx.Graph(d['edges'])
 out={'scope':'Finite computational research; not a proof of a uniform theorem or polynomial complexity.','kittell_source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kittell':analyze(G,'Kittell'),'icosahedron':analyze(nx.icosahedral_graph(),'Icosahedron')}
 args.output.write_text(json.dumps(out,indent=2)+'\n')
