"""Independent root-13 and run-manifest checks. Does not import/run search code."""
import argparse, hashlib, importlib.util, itertools, json, math
from functools import reduce
from pathlib import Path

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('replay',BASE/'wp11-independent-replay.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
LT=BASE/'longtable'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

manifest_path=LT/'wp11-run-manifest.json';m=json.loads(manifest_path.read_text())
r.need(m['schema']=='wp11-run-manifest-v1' and m['features']==r.FEATURES,'manifest schema/features')
for rel,h in m['bound_files'].items():r.need(sha(LT/rel)==h,'bound file: '+rel)
expected=[]
for i in range(8):
 w=[0]*8;w[i]=1;expected.append(('1a',w))
for i,j in itertools.combinations(range(8),2):
 for a,b in itertools.product(range(1,4),repeat=2):
  w=[0]*8;w[i]=a;w[j]=b;expected.append(('1b',w))
for bits in itertools.product(range(2),repeat=8):
 if any(bits):expected.append(('1c',list(bits)))
rows=[]
for k,(tier,w) in enumerate(expected):
 divisor=reduce(math.gcd,[x for x in w if x])
 rows.append({'id':k,'subtier':tier,'weights':w,'proportional_class':[x//divisor for x in w]})
r.need(m['weight_registry']==rows,'complete weight registry/order/membership')
r.need(m['distinct_weight_vectors']==len({tuple(x['weights']) for x in rows})==479,'distinct weights')
r.need(m['distinct_proportional_classes']==len({tuple(x['proportional_class']) for x in rows})==423,'proportional classes')
counts={}
for field,lo,hi in [('discovery_graphs',12,18),('validation_graphs',19,20)]:
 input_graphs=[]
 for n in range(lo,hi+1):
  lines=(BASE/f'triangulations-min5-{n}.txt').read_text().splitlines()
  for gi,line in enumerate(lines):
   order,text=line.split(' ',1);rot=[[ord(c)-97 for c in row] for row in text.split(',')]
   g={'order':int(order),'graph_index':gi,'ascii':line,'ascii_sha256':hashlib.sha256(line.encode()).hexdigest(),'rotation':rot}
   _,roots=r.graph_check(g)
   g.pop('rotation');g['degree_five_roots']=roots;input_graphs.append(g)
 r.need(m[field]==input_graphs,'manifest graph registry differs from raw inputs: '+field)
 counts[field]=len(input_graphs)
r.need(counts=={'discovery_graphs':22,'validation_graphs':96},'split counts')

fixture=LT/'wp11-schema-examples/regression-17-3-root13-toggles.json';j=json.loads(fixture.read_text())
r.need(j['schema']=='wp11-regression-v1' and j['features']==r.FEATURES,'regression schema')
g=dict(j['graph']);_,text=g['ascii'].split(' ',1);g['rotation']=[[ord(c)-97 for c in row] for row in text.split(',')]
rot,roots=r.graph_check(g)
r.need(g['order']==17 and g['graph_index']==3 and j['root']==13 and j['opposite_hub']==3,'named fixture identity')
r.need(g['ascii']==(BASE/'triangulations-min5-17.txt').read_text().splitlines()[3],'fixture corpus identity')
for filename,h in j['producer'].items():r.need(sha(LT/filename)==h,'fixture producer hash')
adj,B,V=r.setup(rot,13,j);states=sorted(r.enumerate_states(adj));state_index={c:i for i,c in enumerate(states)}
e1=[1,0,0,0,0,0,0,0];pit_results=[]
for pit in j['pits']:
 c=tuple(pit['trap_coloring']);pair=tuple(pit['pair'])
 r.need(c in state_index,'proper/canonical trap')
 # State numbers depend on producer enumeration; mathematical identity is the colouring.
 comps=set(r.parts(c,adj));K2=frozenset(V.index(v) for v in pit['two_vertex_component']);K6=frozenset(V.index(v) for v in pit['complementary_component'])
 r.need((pair,K2) in comps and (pair,K6) in comps,'whole components')
 active=frozenset(i for i,x in enumerate(c) if x in pair)
 r.need(K2.isdisjoint(K6) and K2|K6==active and len(K2)==2 and len(K6)==6,'complementary component sizes')
 r.need(V.index(3) in K2 and 3 not in rot[13],'opposite hub')
 c2=r.exchange(c,pair,K2);c6=r.exchange(c,pair,K6)
 r.need(tuple(pit['raw_endpoint_two_vertex_swap'])==c2 and tuple(pit['raw_endpoint_complementary_swap'])==c6,'raw endpoints')
 r.need(r.proper(c2,adj) and r.proper(c6,adj),'endpoint properness')
 perm={int(k):v for k,v in pit['global_renaming_between_raw_endpoints'].items()}
 r.need(set(perm)==set(range(4)) and set(perm.values())==set(range(4)),'colour permutation bijection')
 r.need(tuple(perm[x] for x in c2)==c6,'named endpoint renaming')
 twin=r.canonical(c2)
 r.need(twin==r.canonical(c6)==tuple(pit['canonical_endpoint']),'same canonical twin')
 r.need(r.features(c2,adj,B)==r.features(c6,adj,B),'all-feature invariance')
 r.need(pit['endpoint_features']==r.features(c2,adj,B)[1],'endpoint features')
 rank=r.score(c,adj,B,e1);twinrank=r.score(twin,adj,B,e1)
 r.need(tuple(pit['trap_rank_pq'])==rank==(1,107),'trap mass rank')
 r.need(tuple(pit['endpoint_rank_pq'])==twinrank==(1,115),'twin mass rank')
 ends=r.full_endpoints(c,adj)
 r.need(all(not r.score(e,adj,B,e1)<rank for e in ends),'trap is not two-swap stuck')
 twinends=r.full_endpoints(twin,adj)
 r.need(any(r.score(e,adj,B,e1)<twinrank for e in twinends),'twin has no decreasing macro')
 pit_results.append({'trap_coloring':list(c),'trap_state_as_published':pit['trap_state'],'twin_state_as_published':pit['twin_state'],'component_sizes':[len(K2),len(K6)],'trap_macro_endpoints':len(ends),'twin_macro_endpoints':len(twinends),'trap_rank':list(rank),'twin_rank':list(twinrank)})
r.need(len(pit_results)==5 and len({tuple(x['trap_coloring']) for x in pit_results})==5,'five distinct pits')
result={'scope':'input/manifest and named root-13 regression replay only; no WP11 search', 'manifest_sha256':sha(manifest_path),'fixture_sha256':sha(fixture),'checked_bound_files':len(m['bound_files']),'registry_entries':len(rows),'distinct_weight_vectors':479,'proportional_classes':423,**counts,'root13_proper_colouring_orbits':len(states),'root13_pits':pit_results,'checker_sha256':sha(Path(__file__))}
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
