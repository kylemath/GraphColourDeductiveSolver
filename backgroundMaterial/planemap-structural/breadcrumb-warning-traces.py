"""Warning traces for the frozen breadcrumb policy at its twelve warning roots."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=a.input_dir
spec=importlib.util.spec_from_file_location('mass',d/'mass-macro.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
corpus=json.loads((d/'mass-macro-results.json').read_text());published=json.loads((d/'breadcrumb-corpus-results.json').read_text());lookup={(r['order'],r['graph_index'],r['root']):r for r in published['rows']};rows=[]
for o in corpus['orders']:
 for g in o['graphs_checked']:
  for root in g['failing_roots']:
   n=o['order'];rot=m.parse_rotation(g['ascii']);V=[v for v in range(n)if v!=root];pos={v:i for i,v in enumerate(V)};A=[{pos[w]for w in rot[v]if w!=root}for v in V];B={pos[w]for w in rot[root]};C=m.colourings(A);idx={c:i for i,c in enumerate(C)};D=[m.state_data(c,A,B,n)for c in C];R=[s[0][2]for s in D];N=[{idx[t]for _,_,t in s[1]}for s in D];cache={}
   def ball(c,k):
    if (c,k)not in cache:
     seen={c};front={c}
     for _ in range(k):front=(set().union(*(N[j]for j in front))if front else set())-seen;seen|=front
     cache[c,k]=seen
    return cache[c,k]
   def record(i):return dict(coloring=C[i],rank=D[i][0])
   runs=[]
   for start in range(len(C)):
    W=set();stack=[start];events=[];steps=0;wave=0
    while True:
     c=stack[-1];steps+=1
     if D[c][0][0]==0:break
     low=[j for j in ball(c,2)-W if R[j]<R[c]]
     if low:stack.append(min(low,key=lambda j:(R[j],C[j])));continue
     assert c not in W;W.add(c);events.append(dict(step=steps,stack=[record(j)for j in stack],warned=record(c)))
     if len(stack)>1:stack.pop();continue
     low=[j for j in ball(c,3)-W if R[j]<R[c]];assert low
     stack=[min(low,key=lambda j:(R[j],C[j]))];wave+=1
    runs.append(dict(start=record(start),target=record(c),warnings=[record(j)for j in sorted(W)],warning_events=events,warning_count=len(W),wave2_uses=wave,steps=steps))
   old=lookup[n,g['graph_index'],root]
   assert len(C)==old['coloring_orbits'] and sum(D[i][0][0]>0 for i in range(len(C)))==old['non_target_orbits']
   assert max(x['warning_count']for x in runs)==old['max_warnings']
   assert max(x['wave2_uses']for x in runs)==old['max_wave2_uses']
   assert max(x['steps']for x in runs)==old['max_steps']
   assert sum(x['wave2_uses']>0 for x in runs)==old['runs_using_wave2']
   rows.append(dict(order=n,graph_index=g['graph_index'],ascii=g['ascii'],ascii_sha256=g['ascii_sha256'],root=root,vertex_order=V,boundary_cyclic_order=rot[root],coloring_orbits=len(C),non_target_orbits=old['non_target_orbits'],runs=runs))
total=dict(roots=len(rows),starts=sum(x['coloring_orbits']for x in rows),non_target_starts=sum(x['non_target_orbits']for x in rows),runs_with_warnings=sum(run['warning_count']>0 for x in rows for run in x['runs']))
out=dict(scope='All starts at the twelve mass-failing roots, including empty warning lists. The other 1574 roots have zero warnings in the frozen corpus output. Canonical colour tuples on increasing surviving labels. Diagnostic traces, not basin enumeration or a warning-bound proof.',policy=published['policy'],inputs={f:hashlib.sha256((d/f).read_bytes()).hexdigest()for f in ['mass-macro.py','mass-macro-results.json','breadcrumb-corpus-results.json']},checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),totals=total,rows=rows)
a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(total))
