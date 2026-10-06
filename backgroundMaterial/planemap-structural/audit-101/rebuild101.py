# Fixed-list variant of mathlib4-planemap/scripts/rebuild-planemap-source.py (same overlay method).
# Module list = the 99-module baseline manifest (/tmp/planemap-audit-20261005-protected-lift) + 6 added modules.
from pathlib import Path
import os,re,subprocess,hashlib,json,time,sys
repo=Path('/Users/fulkanjou/mathlib4-planemap'); out=Path(sys.argv[1]); overlayroot=Path(sys.argv[2])
base=json.load(open('/tmp/planemap-audit-20261005-protected-lift/manifest.json'))['modules']
add=['Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobility','Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityGeneral','Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyMobilityTriangulated','MathlibTest.PlaneMapVacancyMobility','MathlibTest.PlaneMapVacancyMobilityGeneral','MathlibTest.PlaneMapVacancyMobilityTriangulated']
mods=list(dict.fromkeys(base+add))
modules={m:repo/(m.replace('.','/')+'.lean') for m in mods}
stems={m.replace('.','/') for m in mods}
overlay=overlayroot/'lib'; overlay.mkdir(parents=True)
old=repo/'.lake/build/lib/lean'; linked=excluded=0
for d,_,files in os.walk(old):
    rel=Path(d).relative_to(old); t=overlay/rel; t.mkdir(parents=True,exist_ok=True)
    for n in files:
        if str(rel/n).split('.')[0] in stems: excluded+=1; continue
        (t/n).symlink_to(Path(d)/n); linked+=1
imports={m:set(re.findall(r'^\s*(?:public\s+)?import\s+(\S+)',p.read_text(),re.M))&modules.keys() for m,p in modules.items()}
order=[];pending=dict(imports)
while pending:
    ready=sorted(m for m,dp in pending.items() if not(dp&pending.keys()))
    if not ready: raise RuntimeError('cycle')
    for m in ready: order.append(m);del pending[m]
(out/'SHA256SUMS-sources').write_text(''.join(hashlib.sha256(modules[m].read_bytes()).hexdigest()+'  '+str(modules[m].relative_to(repo))+'\n' for m in sorted(mods)))
paths=os.environ['LEAN_PATH'].split(':'); assert str(old) in paths
os.environ['LEAN_PATH']=':'.join(str(overlay) if p==str(old) else p for p in paths)
meta={'module_count':len(order),'excluded_custom_artifacts':excluded,'linked':linked,'overlay':str(overlay),'modules':order,'status':'running'}
(out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
print(len(order),'modules',excluded,linked,flush=True)
for i,m in enumerate(order,1):
    p=modules[m];o=overlay/p.relative_to(repo).with_suffix('.olean');o.parent.mkdir(parents=True,exist_ok=True)
    t=time.time()
    with (out/'logs'/(m+'.log')).open('w') as log: r=subprocess.run(['lean','-o',str(o),str(p)],cwd=repo,stdout=log,stderr=subprocess.STDOUT)
    print(f'{i}/{len(order)} {m}: exit {r.returncode} ({time.time()-t:.1f}s)',flush=True)
    if r.returncode: meta['status']='failed';meta['failed']=m;(out/'manifest.json').write_text(json.dumps(meta,indent=2));raise SystemExit(1)
meta['status']='passed';(out/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n');print('ALL PASSED')
