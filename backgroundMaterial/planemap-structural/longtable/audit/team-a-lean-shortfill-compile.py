"""Source-compile the real short-fill theorem against the frozen 79-module audit overlay."""
import hashlib,json,os,subprocess,tempfile,time
from pathlib import Path
REPO=Path('/Users/fulkanjou/mathlib4-planemap')
AUDIT=Path(__file__).resolve().parent
FROZEN=Path('/tmp/planemap-audit-20261004-ranked-root')
LEAN=Path('/Users/fulkanjou/.elan/toolchains/leanprover--lean4---v4.35.0-rc3/bin/lean')

def overlay(src,dst,branches):
    dst.mkdir(parents=True,exist_ok=True)
    names={b.split('/')[0] for b in branches if b}
    for child in src.iterdir():
        d=dst/child.name
        if child.name in names:
            overlay(child,d,[b.split('/',1)[1] if '/' in b else '' for b in branches if b.split('/')[0]==child.name])
        else:d.symlink_to(child)

def main():
    start=time.monotonic();temp=Path(tempfile.mkdtemp(prefix='planemap-team-a-lean-shortfill-'));lib=temp/'lib'
    overlay(FROZEN/'lib',lib,['Mathlib/Combinatorics/SimpleGraph/PlaneMap','MathlibTest'])
    manifest=json.loads((FROZEN/'manifest.json').read_text());env=dict(os.environ)
    env['LEAN_PATH']=':'.join([str(lib)]+manifest['lean_path'])
    sources=['Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancySlide.lean',
        'Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFillTeamA.lean',
        'MathlibTest/PlaneMapVacancyShortFillTeamA.lean']
    checks=[]
    for src in sources:
        source=REPO/src;out=lib/Path(src).with_suffix('.olean');out.parent.mkdir(parents=True,exist_ok=True)
        if out.is_symlink():out.unlink()
        text=source.read_text()
        if src!=sources[0]:
            import re
            assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b',text)
        result=subprocess.run([str(LEAN),'-o',str(out),src],cwd=REPO,env=env,text=True,capture_output=True)
        log=result.stdout+result.stderr
        logfile=AUDIT/('team-a-lean-'+source.stem+'-compile.txt');logfile.write_text(log)
        checks.append({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'exit_code':result.returncode,'log':str(logfile),'olean_sha256':hashlib.sha256(out.read_bytes()).hexdigest() if result.returncode==0 else None})
        print(src,result.returncode,flush=True)
        assert result.returncode==0,log
    (AUDIT/'team-a-lean-shortfill.lean').write_bytes((REPO/sources[1]).read_bytes())
    (AUDIT/'team-a-lean-shortfill-test.lean').write_bytes((REPO/sources[2]).read_bytes())
    result={'scope':'Fresh source compilation of baseline VacancySlide, actual whole-component short-fill theorem and kernel-checking tests; frozen 79 dependencies only','frozen_manifest':str(FROZEN/'manifest.json'),'frozen_manifest_sha256':hashlib.sha256((FROZEN/'manifest.json').read_bytes()).hexdigest(),'extension_overlay':str(lib),'lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'checks':checks,'seconds':round(time.monotonic()-start,3),'complete':True}
    (AUDIT/'team-a-lean-shortfill-results.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
