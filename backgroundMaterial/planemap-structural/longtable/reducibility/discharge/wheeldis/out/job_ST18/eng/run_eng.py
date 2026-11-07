"""ST-15 engines per twin: D -> kc -C -s 60 -t 600 + dfast18; C -> kc -C, kc -C -x X, cfast --fixed X (Studio binaries)."""
import json, subprocess, os, re
from concurrent.futures import ThreadPoolExecutor
J='out/job_ST18/'; tw=json.load(open(J+'twins_new.json'))
P1=['_392_','_73_','_443_','_445_','_765_','_1005_','_524_','_1173_','_1128_','_1131_','_1178_','_1083_','_1133_']
order=sorted(tw, key=lambda n: (not any(p in n for p in P1), n))
def run(n):
    d=tw[n]; f=J+'eng/'+re.sub(r'[^A-Za-z0-9_.-]','_',n); line=' '.join(d['kc'].split()[:5])
    open(f+'.in','w').write(line+'\n'); o=''
    sh=lambda c: subprocess.run(['nice','-n','10']+c,capture_output=True,text=True).stdout
    o+='== kc -C\n'+sh(['loop/kc/kc','-C','-s','60','-t','600',f+'.in'])
    if d['v']=='D': o+='== dfast18\n'+sh(['out/job52/dfast18',f+'.in'])
    else:
        X=d['X'].strip('{}'); open(f+'.x','w').write('%s {%s}\n'%(n,X))
        o+='== kc -C -x X\n'+sh(['loop/kc/kc','-t','600','-C','-x',f+'.x',f+'.in'])
        o+='== cfast --fixed X\n'+sh(['../studio15/cfast',f+'.in','--fixed',X])
    open(f+'.out','w').write(o)
    if d['v']=='D': ok='D=true' in o.split('== dfast18')[0] and 'D=true' in o.split('== dfast18')[1]; v='kc:%s dfast18:%s'%('D' if 'D=true' in o.split('== dfast18')[0] else 'noD','D' if 'D=true' in o.split('== dfast18')[1] else 'noD')
    else:
        kx=o.split('== kc -C -x X')[1].split('== cfast')[0]; cf=o.split('== cfast --fixed X')[1]
        adm='adm=yes' in kx and 'leftover 0' in kx; cfo='leftover bad classes extending after contraction = 0' in cf
        kcC='C-REDUCIBLE' in o.split('== kc -C -x X')[0]; ok=adm and cfo
        v='kc-C:%s kc-x:%s cfast:%s'%('C' if kcC else 'noC','adm=yes,leftover0' if adm else 'FAIL','C' if cfo else 'noC')
    return n, d['v'], d['X'], v, ok
with ThreadPoolExecutor(6) as ex: R=list(ex.map(run, order))
with open(J+'eng/verdicts.tsv','w') as f:
    f.write('# twin\tverdict\tX\tengines\tconfirmed\n')
    for r in R: f.write('%s\t%s\t%s\t%s\t%s\n'%(r[0],r[1],r[2],r[3],'yes' if r[4] else 'NO'))
print(sum(r[4] for r in R),'/',len(R),'confirmed'); [print('NOT', r) for r in R if not r[4]]
