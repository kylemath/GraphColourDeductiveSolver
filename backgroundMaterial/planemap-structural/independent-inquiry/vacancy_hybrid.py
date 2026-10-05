exec(open('/tmp/vacancy_inquiry.py').read().split('results=[]')[0])
def closure(rot,start):
 q=collections.deque([start]);seen={start};parent={start:None}
 while q:
  r,c=q.popleft();cnt=collections.Counter(c[v] for v in rot[r])
  if len(cnt)<4:return seen,(r,c),parent
  for x in rot[r]:
   if cnt[c[x]]==1:
    d=list(c);d[r]=d[x];d[x]=-1;z=(x,canon(d))
    if z not in seen:seen.add(z);q.append(z);parent[z]=(r,c)
 return seen,None,parent
bad=[z for z in json.loads(Path('/tmp/vacancy-all-discovery-results.json').read_text()) if not z['target_found']]
results=[]
for z in bad:
 t=json.loads(gzip.decompress((base/z['fixture']).read_bytes()));rot=t['graph']['rotation'];c=[-1]*len(rot)
 for v,a in zip(t['vertex_order'],t['states'][z['state_index']]['coloring']):c[v]=a
 start=(t['root'],canon(c));seen,_,par=closure(rot,start);win=None;tried=0
 for r,c in sorted(seen):
  for a in range(4):
   for b in range(a+1,4):
    remaining={v for v in range(len(rot)) if c[v] in (a,b)}
    while remaining:
     component={min(remaining)};stack=list(component)
     while stack:
      v=stack.pop()
      for w in rot[v]:
       if w in remaining and w not in component:component.add(w);stack.append(w)
     remaining-=component;d=list(c)
     for v in component:d[v]=b if c[v]==a else a
     assert all(d[u]==-1 or d[v]==-1 or d[u]!=d[v] for u in range(len(rot)) for v in rot[u])
     tried+=1;_,target,after=closure(rot,(r,canon(d)))
     if target:
      beforepath=[];p=(r,c)
      while p is not None:beforepath.append(p);p=par[p]
      afterpath=[];p=target
      while p is not None:afterpath.append(p);p=after[p]
      win={'pair':[a,b],'component':sorted(component),'before_slide_path':beforepath[::-1],'after_slide_path':afterpath[::-1]};break
    if win:break
   if win:break
  if win:break
 results.append({'fixture':z['fixture'],'index':z['state_index'],'slide_component_size':len(seen),'population':[c.count(i) for i in range(4)],'one_switch_escape':win,'switches_tried':tried})
Path('/tmp/vacancy-hybrid-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'slide_only_failures':len(bad),'one_switch_escapes':sum(z['one_switch_escape'] is not None for z in results),'fixtures':sorted({z['fixture'] for z in results})}))
