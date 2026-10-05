exec(open('/tmp/vacancy_inquiry.py').read().split('results=[]')[0])
t=json.loads(gzip.decompress((base/'18-10-r0.json.gz').read_bytes()));rot=t['graph']['rotation'];pop=set();targets=0
for s in t['states']:
 if s['p']!=0:continue
 targets+=1;c=[-1]*len(rot)
 for v,a in zip(t['vertex_order'],s['coloring']):c[v]=a
 for a in set(range(4))-{c[v] for v in rot[0]}:
  d=list(c);d[0]=a;assert all(d[u]!=d[v] for u in range(len(rot)) for v in rot[u]);pop.add(tuple(sorted(d.count(i) for i in range(4))))
bad=[z for z in json.loads(Path('/tmp/vacancy-all-discovery-results.json').read_text()) if not z['target_found']];rows=[]
for z in bad:
 t2=json.loads(gzip.decompress((base/z['fixture']).read_bytes()));s=t2['states'][z['state_index']];cnt=[s['coloring'].count(i) for i in range(4)];possible={tuple(sorted(cnt[j]+(i==j) for j in range(4))) for i in range(4)}
 rows.append({'fixture':z['fixture'],'state_index':z['state_index'],'population':sorted(cnt),'possible_completed_populations':sorted(possible),'matches_full_colouring':bool(pop&possible)})
out={'full_colouring_populations':sorted(pop),'target_deletion_orbits_checked':targets,'failed_starts':rows,'interpretation':'Slides preserve occupied colour populations; full-colouring populations use complete previously replayed root0 deletion table. No independent new census or universal claim.'}
Path('/tmp/vacancy-population-results.json').write_text(json.dumps(out,indent=2));print({'targets':targets,'populations':sorted(pop),'all16_obstructed':all(not x['matches_full_colouring'] for x in rows)})
