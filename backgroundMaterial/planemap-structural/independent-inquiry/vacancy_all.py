exec(open('/tmp/vacancy_inquiry.py').read().split('results=[]')[0])
results=[]
for p in sorted(base.glob('*.json.gz')):
 t=json.loads(gzip.decompress(p.read_bytes()))
 for idx,s in enumerate(t['states']):
  if s['p']==0:continue
  z=search(t,idx,200000);z['fixture']=p.name;results.append(z)
  if not z['target_found']:print('NO TARGET',p.name,idx,z['states_seen'],z['exhausted'],flush=True)
Path('/tmp/vacancy-all-discovery-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'starts':len(results),'targets':sum(z['target_found'] for z in results),'exhausted_without_target':sum(z['exhausted'] for z in results),'capped':sum(not z['target_found'] and not z['exhausted'] for z in results),'max_slide_length':max((len(z['slide_path'])-1 for z in results if z['target_found']),default=0),'max_states_seen':max((z['states_seen'] for z in results),default=0)}))
