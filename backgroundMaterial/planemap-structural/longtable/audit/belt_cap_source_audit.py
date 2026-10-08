"""Compile immutable belt-cap sources and their actual graph dependency; full walk is not claimed."""
from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time,re
HERE=Path(__file__).resolve().parents[2];SOURCE=HERE/'belt-cap-lean';BASE=Path('/tmp/planemap-audit-20261005-short-fill')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def overlay(a,b,branches):
 b.mkdir(parents=True)
 names={x.split('/')[0] for x in branches if x}
 for p in a.iterdir():
  q=b/p.name
  if p.name in names:overlay(p,q,[x.split('/',1)[1] if '/' in x else '' for x in branches if x.split('/')[0]==p.name])
  else:q.symlink_to(p)
def main():
 start=time.monotonic();m=json.loads((BASE/'manifest.json').read_text());assert m['status']=='passed'
 root=Path(tempfile.mkdtemp(prefix='planemap-belt-caps-audit-'));lib=root/'lib';overlay(BASE/'lib',lib,['Mathlib/Combinatorics/SimpleGraph/PlaneMap','MathlibTest'])
 paths=['Mathlib/Combinatorics/SimpleGraph/PlaneMap/BeltVacancyTeamA.lean','Mathlib/Combinatorics/SimpleGraph/PlaneMap/BeltCapsMath.lean','MathlibTest/PlaneMapBeltCapsMath.lean']
 env=dict(os.environ,LEAN_PATH=':'.join(str(lib) if x==str(BASE/'lib') else x for x in m['lean_path']));hashes={p:digest(SOURCE/p) for p in paths};checks=[]
 for p in paths:
  assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',(SOURCE/p).read_text())
  out=lib/Path(p).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists()
  r=subprocess.run(['/Users/fulkanjou/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean','-o',str(out),p],cwd=SOURCE,env=env,capture_output=True,text=True)
  log=SOURCE/(Path(p).stem+'-output.txt');log.write_text(r.stdout+r.stderr);checks.append({'source':p,'sha256':hashes[p],'exit_code':r.returncode,'log':log.name});print(p,r.returncode,flush=True);assert not r.returncode,r.stdout+r.stderr
 assert all(digest(SOURCE/p)==h for p,h in hashes.items())
 (SOURCE/'source-audit.json').write_text(json.dumps({'complete':True,'scope':'Actual D/S caps and original-column preservation; full belt walk not compiled','baseline_manifest_sha256':digest(BASE/'manifest.json'),'lean_path':env['LEAN_PATH'].split(':'),'checks':checks,'sources_stable':True,'seconds':round(time.monotonic()-start,3)},indent=2)+'\n')
if __name__=='__main__':main()
