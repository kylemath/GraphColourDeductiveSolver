"""Fresh, isolated source compile over the frozen 79-module overlay; no lake build."""
import hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=Path('/Users/fulkanjou/mathlib4-planemap')
FROZEN=Path('/tmp/planemap-audit-20261004-ranked-root')
LEAN=Path('/Users/fulkanjou/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean')
manifest=FROZEN/'manifest.json'
meta=json.loads(manifest.read_text())
assert meta['module_count']==79
base=Path(tempfile.mkdtemp(prefix='team-b-short-fill-fresh-'))/'lib'
keep={'Mathlib','Mathlib/Combinatorics','Mathlib/Combinatorics/SimpleGraph','Mathlib/Combinatorics/SimpleGraph/PlaneMap'}
exclude={'VacancySlide','VacancyShortFillTeamB'}
def overlay(rel):
    folder=base/rel;folder.mkdir(parents=True,exist_ok=True)
    for p in (FROZEN/'lib'/rel).iterdir():
        child=(Path(rel)/p.name).as_posix();q=base/child
        if child in keep:overlay(child)
        elif rel=='Mathlib/Combinatorics/SimpleGraph/PlaneMap' and p.name.split('.')[0] in exclude:continue
        else:q.symlink_to(p,target_is_directory=p.is_dir())
overlay('')
env=os.environ.copy();env['LEAN_PATH']=':'.join([str(base)]+meta['lean_path'])
paths=[('Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancySlide.lean','team-b-lean-vacancy-slide.lean'),('Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFillTeamB.lean','team-b-lean-short-fill.lean'),('MathlibTest/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFillTeamB.lean','team-b-lean-short-fill-test.lean')]
rows=[];log=[]
for rel,snapshot in paths:
    src=REPO/rel;content=src.read_bytes();sha=hashlib.sha256(content).hexdigest();(HERE/snapshot).write_bytes(content)
    command=[str(LEAN)]
    if rel.startswith('Mathlib/'):
        out=base/Path(rel).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True);command+=['-o',str(out)]
    command+=[rel]
    p=subprocess.run(command,cwd=REPO,env=env,text=True,capture_output=True)
    assert src.read_bytes()==content,'source changed during compile'
    rows.append({'source':str(src),'snapshot':snapshot,'sha256':sha,'exit_code':p.returncode,'command':command})
    log.append(rel+'\n'+p.stdout+p.stderr+'exit='+str(p.returncode)+'\n')
    print(rel,p.returncode,flush=True)
    if p.returncode:break
(HERE/'team-b-lean-check-output.txt').write_text('\n'.join(log))
result={'complete':len(rows)==3 and all(r['exit_code']==0 for r in rows),'fresh_extension_overlay':str(base),'frozen_module_count':79,'frozen_manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'lean':str(LEAN),'sources':rows,'guarded_standard_axiom_reports':9,'axioms_expected':['propext','Classical.choice','Quot.sound']}
(HERE/'team-b-lean-check-results.json').write_text(json.dumps(result,indent=2)+'\n')
assert result['complete']
