import gzip,json,collections
from pathlib import Path
base=Path('/Users/fulkanjou/GraphColour/backgroundMaterial/planemap-structural/longtable/wp11-discovery/tables')
def canon(c):
 d={};return tuple(-1 if a==-1 else d.setdefault(a,len(d)) for a in c)
def search(t,idx,limit=200000):
 rot=t['graph']['rotation'];r=t['root'];c=[-1]*len(rot)
 for v,a in zip(t['vertex_order'],t['states'][idx]['coloring']):c[v]=a
 start=(r,canon(c));q=collections.deque([start]);parent={start:None};target=None
 while q and len(parent)<limit:
  r,c=q.popleft();counts=collections.Counter(c[v] for v in rot[r])
  if len(counts)<4:target=(r,c);break
  for x in rot[r]:
   if counts[c[x]]!=1:continue
   d=list(c);d[r]=d[x];d[x]=-1;assert all(d[u]==-1 or d[v]==-1 or d[u]!=d[v] for u in range(len(rot)) for v in rot[u])
   z=(x,canon(d))
   if z not in parent:parent[z]=(r,c);q.append(z)
 path=[]
 if target:
  z=target
  while z is not None:path.append({'root':z[0],'degree':len(rot[z[0]]),'coloring':z[1]});z=parent[z]
  path.reverse()
 return {'graph':t['graph']['ascii'],'root':t['root'],'state_index':idx,'states_seen':len(parent),'exhausted':not q and target is None,'target_found':target is not None,'vacancy_roots':sorted({z[0] for z in parent}),'slide_path':path}
results=[]
for name,idx in [('17-0-r4.json.gz',25)]:
 t=json.loads(gzip.decompress((base/name).read_bytes()));results.append(search(t,idx))
Path('/tmp/vacancy-inquiry-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results))
