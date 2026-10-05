"""Fresh source-compile two belt helpers and their exact axiom guards against the accepted83-module overlay."""
from pathlib import Path
import os,json,hashlib,subprocess,tempfile,time
REPO=Path('/Users/fulkanjou/mathlib4-planemap');BASE=Path('/tmp/planemap-audit-20261005-short-fill')
DEST=Path(__file__).resolve().parents[2]/'belt-lean-preparation'
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
 root=Path(tempfile.mkdtemp(prefix='planemap-belt-preparation-audit-'));lib=root/'lib';overlay(BASE/'lib',lib,['Mathlib/Combinatorics/SimpleGraph/PlaneMap','MathlibTest'])
 env=dict(os.environ,LEAN_PATH=':'.join(str(lib) if x==str(BASE/'lib') else x for x in m['lean_path']))
 DEST.mkdir(parents=True,exist_ok=True);records=[]
 paths=['Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyPotential.lean','Mathlib/Combinatorics/SimpleGraph/PlaneMap/BeltOpeningWords.lean','MathlibTest/PlaneMapBeltPreparation.lean']
 hashes={p:digest(REPO/p) for p in paths}
 for p in paths:
  output=lib/Path(p).with_suffix('.olean');output.parent.mkdir(parents=True,exist_ok=True)
  assert not output.exists(),'Cached helper present'
  run=subprocess.run(['/Users/fulkanjou/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean','-o',str(output),p],cwd=REPO,env=env,text=True,capture_output=True)
  log=DEST/(Path(p).stem+'.log');log.write_text(run.stdout+run.stderr)
  records.append({'source':p,'sha256':hashes[p],'exit_code':run.returncode,'log':log.name});print(p,run.returncode,flush=True)
  assert run.returncode==0,run.stdout+run.stderr
  snapshot=DEST/p;snapshot.parent.mkdir(parents=True,exist_ok=True);snapshot.write_bytes((REPO/p).read_bytes())
 assert all(digest(REPO/p)==h for p,h in hashes.items())
 (DEST/'source-audit.json').write_text(json.dumps({'complete':True,'scope':'Two helpers only, not the unequal-pole belt theorem','base_manifest_sha256':digest(BASE/'manifest.json'),'lean_path':env['LEAN_PATH'].split(':'),'checks':records,'sources_stable':True,'seconds':round(time.monotonic()-start,3)},indent=2)+'\n')
if __name__=='__main__':main()
