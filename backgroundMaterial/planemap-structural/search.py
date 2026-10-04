"""Finite Plantri census of the universal-root Kempe escape kill witness."""
import argparse,collections,hashlib,itertools,json,subprocess,time
from pathlib import Path
import networkx as nx
from escape import colors,canon
P=list(itertools.combinations(range(4),2))
ARCHIVE_SOURCE='https://users.cecs.anu.edu.au/~bdm/plantri/plantri58.tar.gz'
def parse(line):
 n,code=line.strip().split(' ',1);n=int(n);rot=[[ord(c)-97 for c in row] for row in code.split(',')];assert len(rot)==n
 G=nx.Graph();G.add_nodes_from(range(n))
 for v,ns in enumerate(rot):
  assert len(set(ns))==len(ns) and v not in ns and len(ns)>=5
  for w in ns:assert v in rot[w];G.add_edge(v,w)
 assert G.number_of_edges()==3*n-6
 seen=set();faces=[]
 for v,ns in enumerate(rot):
  for w in ns:
   if (v,w) in seen:continue
   face=[];d=(v,w)
   while d not in seen:
    seen.add(d);face.append(d);a,b=d;d=(b,rot[b][(rot[b].index(a)+1)%len(rot[b])])
   assert d==face[0] and len(face)==3;faces.append(face)
 assert len(faces)==2*n-4 and nx.is_connected(G) and nx.check_planarity(G)[0]
 return G,rot

def root_check(G,rot,r):
 H=G.copy();H.remove_node(r);V=sorted(H);B=rot[r];C=colors(H,V);ix={c:i for i,c in enumerate(C)};adj=[{V.index(w) for w in H[v]} for v in V];moves=[];good=set()
 for i,c in enumerate(C):
  assert all(c[j]!=c[k] for j in range(len(V)) for k in adj[j])
  if len({c[V.index(v)] for v in B})<=3:good.add(i)
  nxt=set()
  for a,b in P:
   pending={j for j,k in enumerate(c) if k in (a,b)}
   while pending:
    seed=min(pending);K={seed};q=[seed];pending.remove(seed)
    for j in q:
     ns=adj[j]&pending;pending-=ns;K|=ns;q.extend(ns)
    swapped=canon([b if k==a and j in K else a if k==b and j in K else k for j,k in enumerate(c)]);nxt.add(ix[swapped])
  moves.append(nxt)
 assert all(i in moves[j] for i,ns in enumerate(moves) for j in ns)
 reached=set(good);q=list(good)
 for i in q:
  ns=moves[i]-reached;reached|=ns;q.extend(ns)
 remaining=set(range(len(C)));classes=0;bad=0;witness=None
 while remaining:
  seed=min(remaining);comp={seed};q=[seed];remaining.remove(seed)
  for i in q:
   ns=moves[i]&remaining;remaining-=ns;comp|=ns;q.extend(ns)
  classes+=1
  if not comp&good:bad+=1;witness={'vertex_order':V,'coloring':C[seed],'class_size':len(comp)}
 assert (bad==0)==(len(reached)==len(C))
 return {'root':r,'coloring_orbits':len(C),'kempe_classes':classes,'targetless_classes':bad,'reachable_orbits':len(reached),'bad_class_witness':witness}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--max-order',type=int,default=18)
 ap.add_argument('--plantri',default='plantri',help='Path to the compiled Plantri executable.')
 ap.add_argument('--archive',type=Path,help='Optional downloaded Plantri source archive for hashing.')
 ap.add_argument('--input-dir',type=Path,default=Path(__file__).parent,help='Directory for generated ASCII rotations.')
 ap.add_argument('--output',type=Path,default=Path(__file__).with_name('search-results.json'))
 args=ap.parse_args();out={'scope':'Finite exhaustive census only; not a uniform theorem or complexity bound.','generator':'Plantri 5.8 -am5: simple triangulations of minimum degree five','archive_source':ARCHIVE_SOURCE,'archive_sha256':hashlib.sha256(args.archive.read_bytes()).hexdigest() if args.archive else None,'orders':[],'kill_witness':None};base=args.input_dir;base.mkdir(parents=True,exist_ok=True);start=time.time()
 for n in range(12,args.max_order+1):
  path=base/f'triangulations-min5-{n}.txt';proc=subprocess.run([args.plantri,'-am5',str(n),str(path)],capture_output=True,text=True,check=True);lines=path.read_text().splitlines();rec={'order':n,'graphs':len(lines),'generator_stderr':proc.stderr.strip(),'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'graphs_checked':[]};out['orders'].append(rec)
  for gi,line in enumerate(lines):
   G,rot=parse(line);rs=[root_check(G,rot,r) for r in G if G.degree(r)==5];assert rs
   killed=all(r['targetless_classes']>0 for r in rs);rec['graphs_checked'].append({'graph_index':gi,'ascii':line,'roots':rs,'good_roots':sum(r['targetless_classes']==0 for r in rs)})
   print(n,gi+1,'/',len(lines),'roots',len(rs),'orbits',sum(r['coloring_orbits'] for r in rs),'kill',killed,flush=True)
   if killed:out['kill_witness']={'order':n,'graph_index':gi,'ascii':line};break
  out['elapsed_seconds']=time.time()-start;args.output.write_text(json.dumps(out,indent=2)+'\n')
  if out['kill_witness']:break
 if not out['kill_witness']:out['completed_through_order']=args.max_order
 out['elapsed_seconds']=time.time()-start;args.output.write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
