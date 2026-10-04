"""Frozen breadcrumb-v1 on the existing labelled corpus; finite evidence only."""
import argparse,hashlib,importlib.util,json,time
from pathlib import Path
POLICY='breadcrumb-v1-global-min-depth3-canonical-lex'
p=argparse.ArgumentParser();p.add_argument('--input-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
d=args.input_dir
spec=importlib.util.spec_from_file_location('mass',d/'mass-macro.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
table=json.loads((d/'mass-macro-results.json').read_text())
rows=[];began=time.time()
for order in table['orders']:
 for g in order['graphs_checked']:
  assert hashlib.sha256(g['ascii'].encode()).hexdigest()==g['ascii_sha256'];rot=m.parse_rotation(g['ascii']);n=len(rot)
  assert g['degree_five_roots']==[v for v in range(n)if len(rot[v])==5]
  for expected in g['roots']:
   r=expected['root'];V=[v for v in range(n)if v!=r];pos={v:i for i,v in enumerate(V)};A=[{pos[w]for w in rot[v]if w!=r}for v in V];B={pos[w]for w in rot[r]}
   C=m.colourings(A);assert C and len(C)==expected['coloring_orbits'];idx={c:i for i,c in enumerate(C)};data=[m.state_data(c,A,B,n)for c in C];R=[s[0][2]for s in data];target=[s[0][0]==0 for s in data];N=[{idx[t]for _,_,t in s[1]}for s in data]
   assert all(i in N[j]for i,ns in enumerate(N)for j in ns)
   N2=[ns|set().union(*(N[j]for j in ns))for ns in N]
   decrease=[sorted((j for j in ns if R[j]<R[i]),key=lambda j:(R[j],C[j]))for i,ns in enumerate(N2)]
   # On roots with no dead end, this dynamic calculation exactly evaluates
   # every greedy run: warnings and the second wave are never needed.
   if all(target[i]or decrease[i]for i in range(len(C))):
    lengths={}
    for i in sorted(range(len(C)),key=lambda j:(R[j],C[j])):
     lengths[i]=1 if target[i]else 1+lengths[decrease[i][0]]
    results=[dict(ok=True,warnings=0,wave2=0,steps=lengths[i])for i in range(len(C))]
   else:
    reach3={}
    def run(start):
     W=set();stack=[start];steps=0;wave=0
     while True:
      c=stack[-1];steps+=1
      if target[c]:return dict(ok=True,warnings=len(W),wave2=wave,steps=steps)
      j=next((j for j in decrease[c]if j not in W),None)
      if j is not None:stack.append(j);continue
      W.add(c)
      if len(stack)>1:stack.pop();continue
      if c not in reach3:reach3[c]=N2[c]|set().union(*(N[j]for j in N2[c]))
      candidates=[j for j in reach3[c]if R[j]<R[c]and j not in W]
      if not candidates:
       return dict(ok=False,warnings=len(W),wave2=wave,steps=steps,start_coloring=C[start],stuck_coloring=C[c],warning_colorings=[C[j]for j in sorted(W)],rank=data[c][0],all_within_three=[dict(coloring=C[j],rank=data[j][0])for j in sorted(reach3[c]|{c})])
      j=min(candidates,key=lambda j:(R[j],C[j]));assert R[j]<R[c];wave+=1;stack=[j]
    results=[run(i)for i in range(len(C))]
   failures=[s for s in results if not s['ok']]
   rows.append(dict(order=n,graph_index=g['graph_index'],ascii_sha256=g['ascii_sha256'],root=r,vertex_order=V,boundary_cyclic_order=rot[r],coloring_orbits=len(C),non_target_orbits=sum(not b for b in target),all_reach_target=not failures,max_warnings=max(s['warnings']for s in results),max_wave2_uses=max(s['wave2']for s in results),runs_using_wave2=sum(s['wave2']>0 for s in results),max_steps=max(s['steps']for s in results),failures=failures))
  print('checked',n,g['graph_index'],flush=True)
assert len(rows)==1586 and sum(r['coloring_orbits']for r in rows)==244051
out=dict(policy=POLICY,scope='All 118 existing labelled corpus graphs, every degree-five root, all deletion-colouring orbits. Wave depth chosen after previous trap observations; not holdout evidence. Canonical lex tie-break is label-dependent. No general theorem or polynomial warning bound.',inputs={f:hashlib.sha256((d/f).read_bytes()).hexdigest()for f in ['mass-macro.py','mass-macro-results.json']},checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),totals=dict(graphs=118,roots=len(rows),coloring_orbits=sum(r['coloring_orbits']for r in rows),failing_roots=sum(not r['all_reach_target']for r in rows),max_warnings=max(r['max_warnings']for r in rows),max_wave2_uses=max(r['max_wave2_uses']for r in rows),max_steps=max(r['max_steps']for r in rows)),elapsed_seconds=time.time()-began,rows=rows)
args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['totals']),flush=True)
