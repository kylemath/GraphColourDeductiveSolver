import json, hashlib
from pathlib import Path
BASE=Path('/Users/fulkanjou/GraphColour/backgroundMaterial/planemap-structural/icosahedron-fixture.json')
OUT=Path('/tmp/isolated-fixtures-work')
b=json.loads(BASE.read_text()); rot=[b['rotation'][str(i)] for i in range(12)]
def face_orbits(r):
 seen=set(); out=[]
 for u,ns in enumerate(r):
  for v in ns:
   if (u,v) in seen: continue
   start=(u,v); d=start; f=[]
   while d not in seen:
    seen.add(d); f.append(d[0]); a,z=d; d=(z,r[z][(r[z].index(a)+1)%len(r[z])])
   assert d==start and len(f)==3
   out.append(f)
 return out
faces=face_orbits(rot)
def keyface(f): return tuple(sorted(f))
findex={keyface(f):i for i,f in enumerate(faces)}
edges=sorted({tuple(sorted((u,v))) for u,ns in enumerate(rot) for v in ns})
eindex={e:i for i,e in enumerate(edges)}
def from_faces(n,fs):
 # face successor (a,b)->(b,c), so rotation at b maps a to c.
 successor=[{} for _ in range(n)]
 for a,b,c in fs:
  for x,y,z in [(a,b,c),(b,c,a),(c,a,b)]:
   assert x not in successor[y]; successor[y][x]=z
 r=[]
 for u,s in enumerate(successor):
  start=min(s); ns=[]; v=start
  while v not in ns: ns.append(v); v=s[v]
  assert v==start and len(ns)==len(s)
  r.append(ns)
 return r
f32=[]
dartface={(f[j],f[(j+1)%3]):i for i,f in enumerate(faces) for j in range(3)}
for u,v in edges:
 f=dartface[u,v]; g=dartface[v,u]
 f32.extend([(u,12+g,12+f),(v,12+f,12+g)])
f42=[]
for a,b,c in faces:
 ab=12+eindex[tuple(sorted((a,b)))]; bc=12+eindex[tuple(sorted((b,c)))]; ca=12+eindex[tuple(sorted((c,a)))]
 f42.extend([(a,ab,ca),(b,bc,ab),(c,ca,bc),(ab,bc,ca)])
def base_auto(target):
 mapping={}; todo=[((0,rot[0][0]),target)]
 while todo:
  (u,v),(x,y)=todo.pop()
  for a,z in [(u,x),(v,y)]:
   if a in mapping: assert mapping[a]==z
   else:
    assert z not in mapping.values(); mapping[a]=z
  # Force all cyclic neighbors; propagate newly mapped outgoing darts.
  off=(rot[x].index(y)-rot[u].index(v))%5
  for j,w in enumerate(rot[u]):
   z=rot[x][(j+off)%5]
   if w in mapping: assert mapping[w]==z
   else: todo.append(((w,u),(z,x)))
 assert len(mapping)==12
 return [mapping[i] for i in range(12)]
autos=[base_auto((u,v)) for u,ns in enumerate(rot) for v in ns]
assert len({tuple(p) for p in autos})==60
def gf2rank(rows):
 piv={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j]
   else:piv[j]=x;break
 return len(piv)
def verify(name,r,fs,perms):
 n=len(r); es=sorted({tuple(sorted((u,v))) for u,ns in enumerate(r) for v in ns}); ei={e:i for i,e in enumerate(es)}
 assert all(u not in ns and len(ns)==len(set(ns)) and all(u in r[v] for v in ns) for u,ns in enumerate(r))
 actual=face_orbits(r); assert {keyface(f) for f in actual}=={keyface(f) for f in fs}
 seen={0}; todo=[0]
 while todo:
  u=todo.pop()
  for v in r[u]:
   if v not in seen:seen.add(v);todo.append(v)
 assert len(seen)==n and n-len(es)+len(fs)==2
 incidence=[sum(1<<ei[tuple(sorted((u,v)))] for v in r[u]) for u in range(n)]
 boundaries=[sum(1<<ei[tuple(sorted((f[j],f[(j+1)%3])))] for j in range(3)) for f in fs]
 ir=gf2rank(incidence); fr=gf2rank(boundaries)
 assert ir==n-1 and fr==len(es)-n+1==len(fs)-1
 assert all(sum(((row>>ei[e])&1) for e in es if u in e)%2==0 for row in boundaries for u in range(n))
 transports=[]
 for root in range(12):
  p=next(p for p in perms if p[0]==root)
  assert sorted(p)==list(range(n))
  for u,ns in enumerate(r):
   mapped=[p[v] for v in ns]; tgt=r[p[u]]
   assert any(mapped==tgt[k:]+tgt[:k] for k in range(len(tgt)))
  assert {tuple(sorted((p[u],p[v]))) for u,v in es}==set(es)
  transports.append({'source_root':0,'target_root':root,'permutation':p})
 assert [i for i,ns in enumerate(r) if len(ns)==5]==list(range(12))
 assert all(len(ns)==6 for ns in r[12:])
 assert all(v>=12 for u in range(12) for v in r[u])
 obj={'fixture':name,'vertices':list(range(n)),'edges':[list(e) for e in es],'rotation':{str(i):ns for i,ns in enumerate(r)},'oriented_faces':[list(f) for f in fs],'orientation':'face successor (u,v) maps to (v,next(v,u))','degree_five_roots':list(range(12)),'root_transports':transports,'certificate':{'connected':True,'vertices':n,'edges':len(es),'faces':len(fs),'degree_histogram':{'5':12,'6':n-12},'incidence_rank_zmod2':ir,'face_boundary_rank_zmod2':fr,'cycle_space_dimension':len(es)-ir,'degree_five_vertices_independent':True}}
 path=OUT/(name+'.json');path.write_text(json.dumps(obj,indent=2)+'\n')
 return {'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),**obj['certificate']}
p32=[];p42=[]
for p in autos:
 p32.append(p+[12+findex[keyface([p[v] for v in f])] for f in faces])
 p42.append(p+[12+eindex[tuple(sorted((p[u],p[v])))] for u,v in edges])
report={'base_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'fixtures':[verify('F32',from_faces(32,f32),f32,p32),verify('F42',from_faces(42,f42),f42,p42)],'colourings_enumerated':0,'producer_searches_run':0}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
