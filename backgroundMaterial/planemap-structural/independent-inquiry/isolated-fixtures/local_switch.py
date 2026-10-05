exec(open('/tmp/isolated-fixtures-work/transfer.py').read().split('for a in patterns:print')[0])
# Named rings are retained: compatibility is not quotient compatibility.
adj={a:[b for b in rings if compatible(a,b)]for a in rings}
found=None
for a in patterns:
 for b in adj[a]:
  for c in adj[b]:
   if not compatible(c,a):continue
   for j in range(5):
    neighbours={b[(j-1)%5],b[(j+1)%5],a[j],a[(j+1)%5],c[j],c[(j-1)%5]}
    missing=set(range(4))-neighbours-{b[j]}
    if missing:
     found=(a,b,c,j,b[j],min(missing));break
   if found:break
  if found:break
 if found:break
print('period3 isolated singlevertex pair component',found)
def bfs(start,pred):
 todo=[start];parent={start:None}
 for u in todo:
  if pred(u):
   path=[]
   while u is not None:path.append(u);u=parent[u]
   return path[::-1]
  for v in adj[u]:
   if v not in parent:parent[v]=u;todo.append(v)
a,b,c,j,x,y=found
prefix=bfs((0,1,0,1,2),lambda t:t==a)
suffix=bfs(c,lambda t:len(set(t))==3)
print('prefix',prefix,'suffix',suffix)
assert prefix and suffix
import json
from pathlib import Path
Path('/tmp/isolated-fixtures-work/independent-switch-motif.json').write_text(json.dumps({'motif':[a,b,c],'vertex_column':j,'switch_colours':[x,y],'prefix':prefix,'suffix':suffix},indent=2)+'\n')
