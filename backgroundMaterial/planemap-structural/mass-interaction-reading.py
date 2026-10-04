import argparse,hashlib,importlib.util,json,collections,itertools
from pathlib import Path
parser=argparse.ArgumentParser(description='Named-fixture component interaction diagnostics; no selector or changed macro claim.')
parser.add_argument('--input-dir',type=Path,default=Path(__file__).resolve().parent)
parser.add_argument('--output',type=Path,default=Path(__file__).with_name('mass-interaction-reading.json'))
args=parser.parse_args();folder=args.input_dir
spec=importlib.util.spec_from_file_location('mass',folder/'mass-macro.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
table=json.loads((folder/'mass-macro-results.json').read_text());g=next(g for o in table['orders'] if o['order']==17 for g in o['graphs_checked'] if g['graph_index']==0)
rot=m.parse_rotation(g['ascii']);out={}
def boundary_profile(root,c):
 V=[v for v in range(17)if v!=root];pos={v:i for i,v in enumerate(V)};B=rot[root];cd=dict(zip(V,c));names={}
 cc={v:names.setdefault(cd[v],len(names))for v in B+[v for v in V if v not in B]};parts=[];sizes=[];contributions=[]
 for a,b in m.PAIRS:
  pending={v for v in V if cc[v]in(a,b)};partition=[];descriptors=[];contribution=0
  while pending:
   K={min(pending)};pending-=K;queue=list(K)
   for v in queue:
    ns=(set(rot[v])-{root})&pending;pending-=ns;K|=ns;queue.extend(ns)
   trace=tuple(j for j,v in enumerate(B)if v in K);exterior=len(K-set(B))
   descriptors.append((trace,exterior))
   if trace:partition.append(trace);contribution+=exterior**2
  parts.append(tuple(sorted(partition)));sizes.append(sorted(descriptors));contributions.append(contribution)
 return {'sigma':(tuple(cc[v]for v in B),tuple(parts)),'component_descriptors':sizes,'pair_contributions':contributions}
for r in [4,8]:
 V=[v for v in range(17) if v!=r];pos={v:i for i,v in enumerate(V)};A=[{pos[w] for w in rot[v] if w!=r}for v in V];B={pos[w] for w in rot[r]};C=m.colourings(A);idx={c:i for i,c in enumerate(C)};D=[m.state_data(c,A,B,17)for c in C]
 S=[{idx[t] for _,_,t in moves}for s,moves in D];good={i for i,(s,moves)in enumerate(D)if s[0]==0};dist={i:0 for i in good};q=list(good)
 for i in q:
  for j in S[i]:
   if j not in dist:dist[j]=dist[i]+1;q.append(j)
 assert len(dist)==len(C)
 def profile(c):
  bypair=[]
  for a,b in m.PAIRS:
   pending={i for i,k in enumerate(c)if k in(a,b)};cs=[]
   while pending:
    k={min(pending)};pending-=k;queue=list(k)
    for i in queue:
     ns=A[i]&pending;pending-=ns;k|=ns;queue.extend(ns)
    cs.append({'vertices':[V[i] for i in sorted(k)],'boundary':[V[i] for i in sorted(k&B)],'exterior_size':len(k-B),'contribution':len(k-B)**2 if k&B else 0})
   bypair.append({'pair':[a,b],'contribution':sum(c['contribution']for c in cs),'components':cs})
  return bypair
 non=[i for i,(s,mv)in enumerate(D)if s[0]];bad=[i for i in non if not any(D[j][0][2]<D[i][0][2]for j in S[i])and not any(D[k][0][2]<D[i][0][2]for j in S[i]for k in S[j])]
 summary={'root':r,'vertex_order':V,'boundary':rot[r],'orbits':len(C),'non_target':len(non),'non_target_q_histogram':dict(sorted(collections.Counter(D[i][0][1]for i in non).items())),'stuck_states':[]}
 for i in bad:
  orig=D[i][0];row={'coloring':C[i],'rank':orig,'profile':profile(C[i]),'distinct_first_successors':[{'coloring':C[j],'rank':D[j][0],'self_mod_color':i==j,'profile':profile(C[j])}for j in sorted(S[i])],'target_distance_diagnostic':dist[i]}
  decreasing=set(k for j in S[i]for k in S[j] if D[k][0][2]<orig[2]);assert not decreasing
  reachable=[(j,k,l)for j in S[i]for k in S[j]for l in S[k] if D[l][0][2]<orig[2]]
  if reachable:
   seq=min(reachable,key=lambda z:(D[z[-1]][0][2],z));steps=[];current=C[i]
   for j in seq:
    move=next(move for move in m.state_data(current,A,B,17)[1]if move[2]==C[j])
    steps.append({'pair':move[0],'component':[V[v]for v in move[1]],'coloring':C[j],'rank':D[j][0]});current=C[j]
   row['three_move_diagnostic']=steps
  summary['stuck_states'].append(row)
 out[str(r)]=summary
 if r==8:
  c4=tuple(out['4']['stuck_states'][0]['coloring']);profile4=boundary_profile(4,c4)
  matches=[i for i,c in enumerate(C)if boundary_profile(8,c)['sigma']==profile4['sigma']]
  match=next(i for i in matches if D[i][0][1]==143);profile8=boundary_profile(8,C[match])
  move=next(move for move in D[match][1]if D[idx[move[2]]][0][2]<D[match][0][2])
  collision={'root4_coloring':c4,'root8_coloring':C[match],'root4_profile':profile4,'root8_profile':profile8,
             'same_sigma':True,'same_lex_rank':[1,143],
             'root4_color_class_sizes':[c4.count(a)for a in range(4)],'root8_color_class_sizes':[C[match].count(a)for a in range(4)],
             'root8_decreasing_move':{'pair':move[0],'component':[V[v]for v in move[1]],'successor':move[2],'rank':D[idx[move[2]]][0]}}
report={'scope':'Component interactions on order17 graph0 at roots4 and8 only. Three-move paths and target distances are diagnostics, not a new rank or proposal to lengthen the two-swap candidate. No selector, general lemma or complexity claim.',
        'order':17,'graph_index':0,'ascii':g['ascii'],'ascii_sha256':g['ascii_sha256'],
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inputs':{name:hashlib.sha256((folder/name).read_bytes()).hexdigest()for name in ['mass-macro.py','mass-macro-results.json']},'roots':out,'paired_observation_collision':collision}
args.output.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'root4_successor_ranks':[v['rank']for v in out['4']['stuck_states'][0]['distinct_first_successors']],
                  'three_move_diagnostic':[v['rank']for v in out['4']['stuck_states'][0]['three_move_diagnostic']],
                  'root8_stuck_count':len(out['8']['stuck_states'])}))
