"""Independent replay of shared WP11 tables and indexed rank certificates.
Reads existing outputs only; never imports/runs the producer or search.
"""
import argparse, gzip, hashlib, importlib.util, json
from pathlib import Path

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('replay',BASE/'wp11-independent-replay.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def safe_file(base,rel):
 p=(base/rel).resolve();r.need(p.is_relative_to(base.resolve()),'indexed path escapes output directory');return p

def check_output(outdir,manifest):
 result=json.loads((outdir/'results.json').read_text())
 manifest_sha=sha(manifest);m=json.loads(manifest.read_text());lt=manifest.parent
 for rel,digest in m['bound_files'].items():r.need(sha(lt/rel)==digest,'changed bound file: '+rel)
 r.need(result['manifest_sha256']==manifest_sha,'results manifest hash')
 cpath=safe_file(outdir,result['certificates']['path'])
 r.need(sha(cpath)==result['certificates']['sha256'],'certificate file hash')
 cert=json.loads(cpath.read_text())
 r.need(cert['schema']=='wp11-cert-v1-indexed' and cert['stage']==result['stage'],'indexed schema/stage')
 r.need(cert['manifest_sha256']==manifest_sha and cert['features']==r.FEATURES and cert['macro_bound']==2,'indexed model')
 r.need(hashlib.sha256(json.dumps(cert['tables'],sort_keys=True).encode()).hexdigest()==result['tables_index_sha256'],'table index hash')
 registry={}
 for entry in m['weight_registry']:
  registry.setdefault(tuple(entry['weights']),[]).append({'id':entry['id'],'subtier':entry['subtier']})
 stage=result['stage'];input_graphs={}
 if stage=='smoke':
  expected_weights={(1,0,0,0,0,0,0,0),(0,0,1,0,0,0,0,0)}
  ico=json.loads((lt/'wp11-schema-examples/pass-icosahedron-root0-q.json').read_text())['graph']
  input_graphs[(12,None)]=ico
  for g in m['discovery_graphs']:
   if g['order']==17 and g['graph_index'] in (0,1,3):input_graphs[(17,g['graph_index'])]=g
  r.need(result['frozen_discovery'] is None,'smoke discovery reference')
 elif stage=='discovery':
  expected_weights=set(registry);input_graphs={(g['order'],g['graph_index']):g for g in m['discovery_graphs']}
  r.need(result['frozen_discovery'] is None,'discovery frozen reference')
 elif stage=='validation':
  frozen=result['frozen_discovery'];path=safe_file(lt,frozen['path'])
  r.need(sha(path)==frozen['sha256'],'frozen discovery digest')
  disc=json.loads(path.read_text());r.need(disc['stage']=='discovery' and disc['manifest_sha256']==manifest_sha,'frozen discovery identity')
  for k in ['existential_survivors','all_roots_survivors']:r.need(frozen[k]==disc[k],'frozen survivor list')
  expected_weights={tuple(x['weights']) for x in frozen['existential_survivors']}
  input_graphs={(g['order'],g['graph_index']):g for g in m['validation_graphs']}
 else:raise ValueError('unknown stage')

 tables={};graph_roots={};seen_pairs=set();state_total=target_macros=hard_total=endpoint_records=0
 for tid,index in cert['tables'].items():
  path=safe_file(outdir,index['path']);r.need(sha(path)==index['sha256'],'table file hash')
  table=json.loads(gzip.decompress(path.read_bytes()))
  r.need(table['schema']=='wp11-table-v1' and table['features']==r.FEATURES,'shared table schema')
  g=table['graph'];key=(g['order'],g['graph_index']);root=table['root']
  r.need(key in input_graphs,'unexpected graph table');expected=input_graphs[key]
  for k in ['order','graph_index','ascii']:r.need(g[k]==expected[k],'wrong graph input identity')
  if key==(12,None):r.need(g['rotation']==expected['rotation'],'icosahedron input rotation')
  rot,roots=r.graph_check(g);r.need(table['degree_five_roots']==roots,'table eligible roots')
  graph_roots[key]=roots
  r.need((key,root) not in seen_pairs,'duplicate graph/root table');seen_pairs.add((key,root))
  r.need(index['order']==key[0] and index['graph_index']==key[1] and index['root']==root,'index coordinates')
  adj,B,V=r.setup(rot,root,table);states=table['states'];listed=[tuple(s['coloring']) for s in states]
  exact=r.enumerate_states(adj)
  r.need(len(listed)==len(set(listed)) and set(listed)==exact,'omitted/duplicated proper state')
  r.need(table['state_count']==index['state_count']==len(exact),'state count')
  hard=[]
  for i,(s,c) in enumerate(zip(states,listed)):
   p,f=r.features(c,adj,B);r.need(s['p']==p and s['features']==f,'table feature calculation')
   if not p:
    r.need('target_macro' not in s and 'endpoints' not in s,'target carries non-target record');continue
   if 'target_macro' in s:
    r.need('endpoints' not in s,'ambiguous target/hard classification')
    end=r.macro(c,s['target_macro'],adj,V)
    r.need(r.features(end,adj,B)[0]==0,'macro misses target');target_macros+=1
   else:
    r.need('endpoints' in s,'non-target missing certificate');hard.append(i)
    supplied={c}
    for ep in s['endpoints']:
     end=r.macro(c,ep,adj,V);p2,f2=r.features(end,adj,B)
     r.need(ep['endpoint_p']==p2 and ep['endpoint_features']==f2,'indexed endpoint features')
     r.need(p2==1,'hard state actually has target macro');supplied.add(end);endpoint_records+=1
    actual=r.full_endpoints(c,adj)
    r.need(supplied==actual,'incomplete hard-state macro endpoint set')
    r.need(all(r.features(e,adj,B)[0]==1 for e in actual),'hidden target endpoint')
  r.need(table['hard_states']==hard and index['hard_states']==len(hard),'hard-state index')
  state_total+=len(states);hard_total+=len(hard)
  tables[tid]=(table,adj,B,V,key,root)
 r.need(set(graph_roots)==set(input_graphs),'omitted graph')
 r.need(seen_pairs=={(key,root) for key,roots in graph_roots.items() for root in roots},'missing root table')

 outcomes=[];weights=[];decreases=stuck_count=0
 for wc in cert['certificates']:
  w=tuple(wc['weights']);weights.append(w)
  r.need(w in expected_weights and wc['registry']==registry[w],'weight/tier membership')
  per_graph=[];seen_graphs=set();first_ex=first_all=None
  for gcert in wc['per_graph']:
   key=(gcert['order'],gcert['graph_index']);r.need(key in graph_roots and key not in seen_graphs,'certificate graph duplicate/unknown');seen_graphs.add(key)
   good=gcert['good_roots'];bad=gcert['bad_roots'];want={str(x) for x in graph_roots[key]}
   r.need(set(good).isdisjoint(bad) and set(good)|set(bad)==want,'root proof partition incomplete')
   for root_str,proof in good.items():
    table,adj,B,V,tkey,troot=tables[proof['table']]
    r.need(tkey==key and str(troot)==root_str,'good table belongs to other root')
    indices=proof['decreasing_endpoint'];r.need(len(indices)==len(table['hard_states']),'good proof omits hard state')
    for si,ei in zip(table['hard_states'],indices):
     s=table['states'][si];r.need(type(ei) is int and 0<=ei<len(s['endpoints']),'endpoint index')
     c=tuple(s['coloring']);end=tuple(s['endpoints'][ei]['endpoint'])
     r.need(r.score(end,adj,B,w)<r.score(c,adj,B,w),'claimed good endpoint does not decrease');decreases+=1
   for root_str,proof in bad.items():
    table,adj,B,V,tkey,troot=tables[proof['table']]
    r.need(tkey==key and str(troot)==root_str,'bad table belongs to other root')
    si=proof['stuck_state'];r.need(type(si) is int and si in table['hard_states'],'stuck index not hard')
    s=table['states'][si];c=tuple(s['coloring']);rank=r.score(c,adj,B,w)
    r.need(all(not r.score(tuple(ep['endpoint']),adj,B,w)<rank for ep in s['endpoints']),'bad proof has a decreasing endpoint');stuck_count+=1
   if not good and first_ex is None:first_ex={'order':key[0],'graph_index':key[1],'roots':bad}
   if bad and first_all is None:
    rr=min(bad,key=int);first_all={'order':key[0],'graph_index':key[1],'root':int(rr),**bad[rr]}
   per_graph.append({'order':key[0],'graph_index':key[1],'good_roots':sorted(map(int,good)),'bad_roots':sorted(map(int,bad))})
  r.need(seen_graphs==set(input_graphs),'weight omitted graphs')
  r.need(wc['existential_fail_witness']==first_ex and wc['all_roots_fail_witness']==first_all,'wrong failure-witness quantifier/index')
  outcomes.append({'weights':list(w),'registry':registry[w],'existential_pass':first_ex is None,'all_roots_pass':first_all is None,'per_graph':per_graph})
 r.need(len(weights)==len(set(weights)) and set(weights)==expected_weights,'weight registry evaluation incomplete')
 r.need(result['weight_count']==len(weights) and result['results']==outcomes,'summary differs from certificate proofs')
 for k,pred in [('existential_survivors','existential_pass'),('all_roots_survivors','all_roots_pass')]:
  expected=[{'weights':x['weights'],'registry':x['registry']} for x in outcomes if x[pred]]
  r.need(result[k]==expected,'survivor summary mismatch')
 for line in (outdir/'SHA256SUMS').read_text().splitlines():
  digest,rel=line.split(None,1);r.need(sha(safe_file(outdir,rel))==digest,'stage checksum mismatch')
 return {'stage':stage,'manifest_sha256':manifest_sha,'results_sha256':sha(outdir/'results.json'),'certificates_sha256':sha(cpath),'tables':len(tables),'proper_state_orbits':state_total,'target_macros':target_macros,'hard_states':hard_total,'serialized_endpoint_records_checked':endpoint_records,'decreasing_indices_checked':decreases,'stuck_witnesses_checked':stuck_count,'weight_vectors':len(weights),'existential_survivors':[x['weights'] for x in outcomes if x['existential_pass']],'all_roots_survivors':[x['weights'] for x in outcomes if x['all_roots_pass']]}

def main():
 p=argparse.ArgumentParser();p.add_argument('output_directory',type=Path);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path);args=p.parse_args()
 checked=check_output(args.output_directory,args.manifest)
 checked.update(scope='replay of existing output only; no search',checker_sha256=sha(Path(__file__)))
 if args.output:args.output.write_text(json.dumps(checked,indent=2)+'\n')
 print(json.dumps(checked))
if __name__=='__main__':main()
