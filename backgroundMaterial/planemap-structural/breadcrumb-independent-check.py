import argparse,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input-dir',type=Path,required=True);p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.input_dir/'longtable'))
from mass_core import RootState,parse_ascii
mass=json.loads((a.input_dir/'mass-macro-results.json').read_text());published=json.loads(a.results.read_text());lookup={(r['order'],r['graph_index'],r['root']):r for r in published['rows']};checked=[]
for order in mass['orders']:
 for g in order['graphs_checked']:
  for root in g['failing_roots']:
   s=RootState(parse_ascii(g['ascii']),root);nxt=[{j for _,_,j in row['moves']}for row in s.info];R=[row['R']for row in s.info]
   cache={}
   def ball(c,depth):
    key=c,depth
    if key not in cache:
     seen={c};front={c}
     for _ in range(depth):front=set().union(*(nxt[i]for i in front))-seen if front else set();seen|=front
     cache[key]=seen
    return cache[key]
   def run(start):
    warnings=set();history=[start];waves=0;steps=0
    while True:
     c=history[-1];steps+=1
     if s.info[c]['p']==0:return len(warnings),waves,steps
     candidates=ball(c,2)-warnings;lower=[j for j in candidates if R[j]<R[c]]
     if lower:history.append(min(lower,key=lambda j:(R[j],s.C[j])));continue
     warnings.add(c)
     if len(history)>1:history.pop();continue
     lower=[j for j in ball(c,3)-warnings if R[j]<R[c]]
     assert lower,('failure',root,start,c)
     history=[min(lower,key=lambda j:(R[j],s.C[j]))];waves+=1
   runs=[run(i)for i in range(len(s.C))];key=(order['order'],g['graph_index'],root);row=lookup[key]
   assert row['max_warnings']==max(t[0]for t in runs)
   assert row['max_wave2_uses']==max(t[1]for t in runs)
   assert row['max_steps']==max(t[2]for t in runs)
   assert row['runs_using_wave2']==sum(t[1]>0 for t in runs)
   checked.append(dict(order=key[0],graph_index=key[1],root=root,coloring_orbits=len(runs),matched=True))
a.output.write_text(json.dumps(dict(scope='Separate Long Table component/colouring implementation; all starts at the 12 previously mass-failing roots only, not all passing roots.',results_sha256=hashlib.sha256(a.results.read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),mass_core_sha256=hashlib.sha256((a.input_dir/'longtable/mass_core.py').read_bytes()).hexdigest(),rows=checked),indent=2)+'\n');print('Matched',len(checked),'roots',sum(x['coloring_orbits']for x in checked),'starts')
