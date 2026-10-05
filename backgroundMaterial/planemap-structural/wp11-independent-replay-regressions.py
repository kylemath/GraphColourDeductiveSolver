import argparse, copy, importlib.util, itertools, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('independent_replay',str(Path(__file__).with_name('wp11-independent-replay.py')))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
base=Path(__file__).resolve().parent / 'longtable/wp11-schema-examples'
passed=json.loads((base/'pass-icosahedron-root0-q.json').read_text())
failed=json.loads((base/'existential-fail-17-1-L.json').read_text())
single=json.loads((base/'all-roots-fail-17-0-root4-q.json').read_text())
results=[]
def reject(name,cert,change):
 c=copy.deepcopy(cert);change(c)
 try:r.check(c)
 except (ValueError,KeyError,TypeError) as err:
  results.append({'case':name,'rejected':True,'reason':str(err)})
 else:raise AssertionError('accepted tampered certificate: '+name)
reject('omitted proper colouring',passed,lambda c:c['states'].pop())
reject('omitted eligible failing root',failed,lambda c:c['roots'].pop())
reject('missing macro endpoint',single,lambda c:c['failing_root']['stuck'].__setitem__('endpoints',[]))
reject('wrong feature',passed,lambda c:c['states'][0]['features'].__setitem__('hubToggles',99))
reject('wrong degree-five root list',passed,lambda c:c['degree_five_roots'].pop())
reject('invalid whole component',passed,lambda c:next(s for s in c['states'] if s['p'])['witness']['move1'].__setitem__('component',[]))
reject('out-of-domain weight',passed,lambda c:c.__setitem__('weights',[3,0,0,0,0,0,0,0]))
reject('inconsistent input rotation',single,lambda c:c['graph']['rotation'][0].reverse())
# All 24 colour permutations, complete component equivariance, on the 20 named pass states.
rot,_=r.graph_check(passed['graph']);adj,B,V=r.setup(rot,passed['root'],passed)
colour_checks=component_checks=complement_checks=0
for st in passed['states']:
 c=tuple(st['coloring']);parts=r.parts(c,adj)
 for pi in itertools.permutations(range(4)):
  renamed=tuple(pi[x] for x in c)
  assert r.features(c,adj,B)==r.features(renamed,adj,B)
  colour_checks+=1
  expected={(tuple(sorted((pi[a],pi[b]))),K) for (a,b),K in parts}
  assert expected==set(r.parts(renamed,adj))
  for pair,K in parts:
   mapped_pair=tuple(sorted(pi[x] for x in pair))
   assert tuple(pi[x] for x in r.exchange(c,pair,K))==r.exchange(renamed,mapped_pair,K)
   component_checks+=1
 for pair,K in parts:
  active=frozenset(i for i,x in enumerate(c) if x in pair)
  other=active-K
  if (pair,other) in parts:
   assert r.canonical(r.exchange(c,pair,K))==r.canonical(r.exchange(c,pair,other))
   complement_checks+=1
assert complement_checks>0
out={'scope':'pre-release checks on three declared schema examples only; no discovery', 'tamper_checks':results,'colour_permutation_feature_checks':colour_checks,'component_swap_equivariance_checks':component_checks,'complementary_component_checks':complement_checks,'root13_regression':'awaiting Long Table fixture'}
parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path); args=parser.parse_args()
if args.output: args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
