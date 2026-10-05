"""Reject tampered indexed evidence even after its checksums have been updated."""
import argparse, gzip, hashlib, importlib.util, json, shutil, tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('indexed',str(BASE/'wp11-indexed-replay.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
source=BASE/'longtable/wp11-smoke';manifest=BASE/'longtable/wp11-run-manifest.json'

def run_case(name, mutate):
 with tempfile.TemporaryDirectory(prefix='wp11-indexed-tamper-') as temp:
  d=Path(temp)/'smoke';shutil.copytree(source,d)
  cp=d/'certificates.json';cert=json.loads(cp.read_text());results=json.loads((d/'results.json').read_text())
  mutate(d,cert,results)
  for tid,index in cert['tables'].items():index['sha256']=r.sha(d/index['path'])
  cp.write_text(json.dumps(cert,separators=(',',':'))+'\n')
  results['certificates']['sha256']=r.sha(cp)
  results['tables_index_sha256']=hashlib.sha256(json.dumps(cert['tables'],sort_keys=True).encode()).hexdigest()
  (d/'results.json').write_text(json.dumps(results)+'\n')
  (d/'SHA256SUMS').write_text(''.join(r.sha(p)+'  '+str(p.relative_to(d))+'\n' for p in sorted(d.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
  try:r.check_output(d,manifest)
  except (ValueError,KeyError,TypeError) as e:return {'case':name,'rejected':True,'reason':str(e)}
  raise AssertionError('accepted tampered indexed evidence: '+name)

def omit_state(d,c,res):
 tid=next(iter(c['tables']));idx=c['tables'][tid];p=d/idx['path'];t=json.loads(gzip.decompress(p.read_bytes()))
 t['states'].pop();t['state_count']-=1;idx['state_count']-=1;p.write_bytes(gzip.compress(json.dumps(t).encode(),mtime=0))
def omit_root(d,c,res):
 g=c['certificates'][0]['per_graph'][0];g['good_roots'].pop(next(iter(g['good_roots'])))
def invalid_index(d,c,res):
 for cert in c['certificates']:
  for g in cert['per_graph']:
   for proof in g['good_roots'].values():
    if proof['decreasing_endpoint']:proof['decreasing_endpoint'][0]=-1;return
 raise AssertionError('no suitable indexed witness')
def omit_endpoints(d,c,res):
 for tid,idx in c['tables'].items():
  p=d/idx['path'];t=json.loads(gzip.decompress(p.read_bytes()))
  if t['hard_states']:
   t['states'][t['hard_states'][0]]['endpoints']=[]
   p.write_bytes(gzip.compress(json.dumps(t).encode(),mtime=0));return
 raise AssertionError('no hard state')
def forge_summary(d,c,res):res['results'][0]['all_roots_pass']=True
cases=[('omitted colouring with corrected state count',omit_state),('omitted root proof',omit_root),('invalid decreasing endpoint index',invalid_index),('incomplete hard-state endpoints',omit_endpoints),('false all-roots summary',forge_summary)]
out={'scope':'mutations of the named smoke output only; all checksums resealed; no search','cases':[run_case(name,f) for name,f in cases],'checker_sha256':r.sha(Path(__file__))}
p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
if args.output:args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
