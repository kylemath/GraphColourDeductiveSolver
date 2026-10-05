"""Rebuild the accepted 97 sources and the protected all-holes lift, excluding custom caches."""
from pathlib import Path
import os,re,subprocess,hashlib,json,time
REPO=Path('/Users/fulkanjou/mathlib4-planemap')
BASE=Path('/tmp/planemap-audit-20261005-clique-lift')
ROOT=Path('/tmp/planemap-audit-20261005-protected-lift')
LEAN=Path('/Users/fulkanjou/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 start=time.monotonic();base=json.loads((BASE/'manifest.json').read_text())
 for line in (BASE/'SHA256SUMS').read_text().splitlines():
  h,p=line.split('  ',1);assert digest(REPO/p)==h,p
 names=base['modules']+['Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyProtectedLift','MathlibTest.PlaneMapVacancyProtectedLift']
 modules={m:REPO/(m.replace('.','/')+'.lean') for m in names};assert len(modules)==99
 hashes={m:digest(p) for m,p in modules.items()}
 ROOT.mkdir();lib=ROOT/'lib';lib.mkdir();old=REPO/'.lake/build/lib/lean'
 stems={m.replace('.','/') for m in names}
 stems.update(str(p.relative_to(REPO).with_suffix('')) for p in (REPO/'Mathlib/Combinatorics/SimpleGraph/PlaneMap').glob('*.lean'))
 stems.update(str(p.relative_to(REPO).with_suffix('')) for p in (REPO/'MathlibTest').glob('PlaneMap*.lean'))
 linked=excluded=0
 for directory,dirs,files in os.walk(old):
  rel=Path(directory).relative_to(old);target=lib/rel;target.mkdir(parents=True,exist_ok=True)
  for name in files:
   if str(rel/name).split('.')[0] in stems:excluded+=1;continue
   (target/name).symlink_to(Path(directory)/name);linked+=1
 deps={m:set(re.findall(r'^\s*(?:public\s+)?import\s+(\S+)',p.read_text(),re.M)) & modules.keys() for m,p in modules.items()}
 pending=dict(deps);order=[]
 while pending:
  ready=sorted(m for m,ds in pending.items() if not(ds & pending.keys()));assert ready,pending
  for m in ready:order.append(m);del pending[m]
 paths=[str(lib) if p==str(BASE/'lib') else p for p in base['lean_path']]
 assert str(old) not in paths and str(BASE/'lib') not in paths
 env=dict(os.environ,LEAN_PATH=':'.join(paths))
 meta={'module_count':99,'baseline_module_count':97,'baseline_manifest_sha256':digest(BASE/'manifest.json'),'lean_path':paths,'linked_upstream_artifacts':linked,'excluded_custom_artifacts':excluded,'modules':order,'source_hashes':hashes,'status':'running'}
 def save(): (ROOT/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
 save();(ROOT/'SHA256SUMS').write_text(''.join(hashes[m]+'  '+str(modules[m].relative_to(REPO))+'\n' for m in sorted(modules)))
 print('99 source modules; custom cached artifacts excluded:',excluded,flush=True)
 for i,m in enumerate(order,1):
  src=modules[m];out=lib/src.relative_to(REPO).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
  with (ROOT/(m+'.log')).open('w') as log:
   result=subprocess.run([str(LEAN),'-o',str(out),str(src)],cwd=REPO,env=env,stdout=log,stderr=subprocess.STDOUT)
  print(f'{i}/99 {m}: exit {result.returncode}',flush=True)
  if result.returncode:meta.update(status='failed',failed_module=m);save();raise SystemExit(result.returncode)
 assert all(digest(p)==hashes[m] for m,p in modules.items()),'Source changed during audit'
 meta.update(status='passed',seconds=round(time.monotonic()-start,3),sources_stable=True);save()
 print('ALL 99 SOURCE MODULES PASSED',flush=True)
if __name__=='__main__':main()
