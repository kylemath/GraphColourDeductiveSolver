"""Check the named dead-end page's ring in the concrete Kempe state graph."""
import argparse,collections,hashlib,importlib.util,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=a.repo;f=r/'backgroundMaterial/planemap-structural'
spec=importlib.util.spec_from_file_location('mass',f/'mass-macro.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
js=r/'docs/deadend/data.js';text=js.read_text();D=json.loads(text[text.index('{'):].rstrip().rstrip(';'));T=D['roots']['3'];rot=m.parse_rotation(D['ascii']);V=T['V'];B={V.index(v)for v in T['B']};A=[{V.index(w)for w in rot[v]if w!=3}for v in V];C=[tuple(s['c'])for s in T['states']];idx={c:i for i,c in enumerate(C)};assert len(idx)==len(C);N=[]
for i,c in enumerate(C):
 assert all(c[v]!=c[w]for v,ns in enumerate(A)for w in ns)
 score,moves=m.state_data(c,A,B,D['order']);assert tuple(score)==(T['states'][i]['p'],T['states'][i]['q'],T['states'][i]['R']);ns={idx[t]for _,_,t in moves};assert ns-{i}==set(T['states'][i]['next']);N.append(ns)
R=[s['R']for s in T['states']];N2=[ns|set().union(*(N[j]for j in ns))for ns in N];can={}
for i in sorted(range(len(C)),key=lambda i:R[i]):can[i]=T['states'][i]['p']==0 or any(can[j]for j in N2[i]if R[j]<R[i])
region={i for i in range(len(C))if not can[i]};assert region==set(T['region']);traps={i for i in region if not any(R[j]<R[i]for j in N2[i])};assert traps==set(T['traps'])
ring=set().union(*(N[i]for i in region))-region;assert ring==set(T['ring'])
groups=[set(g)for g in T['patternGroups']];assert len(groups)==5 and set().union(*groups)==region
for g in groups:assert len(g)==2 and sorted(R[i]for i in g)==[1842,1850];i,j=sorted(g);assert j in N[i]
pit={i:k for k,g in enumerate(groups)for i in g};cross=collections.Counter();spurs=0
for j in ring:
 neighbours=N[j]&region
 assert T['states'][j]['p']==1
 if len(neighbours)==1:assert R[j]==1866;spurs+=1
 else:
  assert len(neighbours)==2 and R[j]==1873 and sorted(R[i]for i in neighbours)==[1842,1850]
  pair=tuple(sorted(pit[i]for i in neighbours));assert pair[0]!=pair[1];cross[pair]+=1
assert spurs==10 and len(cross)==5 and set(cross.values())=={2}
Q={i:set()for i in range(5)}
for i,j in cross:Q[i].add(j);Q[j].add(i)
assert all(len(v)==2 for v in Q.values());seen={0};queue=[0]
for i in queue:
 for j in Q[i]-seen:seen.add(j);queue.append(j)
assert len(seen)==5
warnings=json.loads((f/'breadcrumb-warning-traces.json').read_text());row=next(row for row in warnings['rows']if row['order']==17 and row['graph_index']==3 and row['root']==3);run=next(run for run in row['runs']if run['warning_count']==4);warn_ids=[idx[tuple(w['coloring'])]for w in run['warnings']]
assert all(i in region for i in warn_ids)
out=dict(scope='One named fixture/root. Page state ranks and complete moves independently checked against original mass implementation. Ring is in an undirected colouring graph; not a decreasing-rank cycle or a universal symmetry/warning bound.',inputs={str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [js,f/'mass-macro.py',f/'breadcrumb-warning-traces.json']},checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),root=3,graph_index=3,order=17,state_count=len(C),pits=[sorted(g)for g in groups],connectors_by_pit_pair=[dict(pits=list(k),count=v)for k,v in sorted(cross.items())],connector_count=10,spur_count=10,connector_rank=1873,spur_rank=1866,four_warning_witness=dict(start=run['start']['coloring'],warning_state_ids=warn_ids,warning_ranks=[R[i]for i in warn_ids],trap_warning_count=sum(i in traps for i in warn_ids),twin_warning_count=sum(i not in traps for i in warn_ids)))
a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['state_count','connector_count','spur_count','four_warning_witness']}))
