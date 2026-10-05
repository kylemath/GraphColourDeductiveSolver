"""Check only oldQ=17:1 for an asymmetric two-copy hand construction; never construct order31."""
from pathlib import Path
import itertools,json,hashlib
HERE=Path(__file__).resolve().parent

def main():
 seed=HERE/'triangle-sum-seed-results.json';data=json.loads(seed.read_text());word=data['ascii']
 assert hashlib.sha256(word.encode()).hexdigest()==data['ascii_sha256']
 adj=[set(ord(c)-97 for c in w) for w in word.split()[1].split(',')];n=len(adj)
 assert n==17
 assert all(v not in adj[v] and all(v in adj[w] for w in adj[v]) for v in range(n))
 degree=[len(x) for x in adj]
 faces=set()
 rot=[[ord(c)-97 for c in w] for w in word.split()[1].split(',')]
 for v,row in enumerate(rot):
  for k,u in enumerate(row):faces.add(frozenset((v,u,row[(k+1)%len(row)])))
 triangles={frozenset(x) for x in itertools.combinations(range(n),3) if all(b in adj[a] for a,b in itertools.combinations(x,2))}
 assert triangles==faces,'Seed has a nonfacial triangle'
 mapping={};used=set();autos=[];visited=0
 def candidates(v):return [w for w in range(n) if w not in used and degree[w]==degree[v] and all((u in adj[v])==(t in adj[w]) for u,t in mapping.items())]
 def visit():
  nonlocal visited
  visited+=1
  if len(mapping)==n:
   autos.append([mapping[v] for v in range(n)]);return
  options=[(candidates(v),v) for v in range(n) if v not in mapping]
  cs,v=min(options,key=lambda x:(len(x[0]),x[1]))
  for w in cs:
   mapping[v]=w;used.add(w);visit();used.remove(w);del mapping[v]
 visit();assert len(autos)==4
 fs=[(3,4,11),(1,2,7)];checks=[]
 for f in fs:
  remaining=set(range(n))-set(f);seen={min(remaining)};todo=list(seen)
  while todo:
   v=todo.pop()
   for w in adj[v]&remaining-seen:seen.add(w);todo.append(w)
  assert seen==remaining
  stabilizers=[a for a in autos if {a[v] for v in f}==set(f)]
  assert stabilizers==[list(range(n))]
  hist={str(d):sum(degree[v]==d for v in remaining) for d in sorted(set(degree))}
  checks.append({'face':f,'remaining_connected':True,'remaining_original_degree_histogram':hist,'nonidentity_image':[[a[v] for v in f] for a in autos if a!=list(range(n))],'stabilizer_size':len(stabilizers)})
 assert checks[0]['remaining_original_degree_histogram']!=checks[1]['remaining_original_degree_histogram']
 out={'scope':'old17:1 only; no new-order graph generated','seed_sha256':hashlib.sha256(seed.read_bytes()).hexdigest(),'all_triangles_facial':True,'triangles':len(triangles),'automorphisms':autos,'backtracking_nodes':visited,'faces':checks}
 (HERE/'triangle-sum-asymmetry-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
