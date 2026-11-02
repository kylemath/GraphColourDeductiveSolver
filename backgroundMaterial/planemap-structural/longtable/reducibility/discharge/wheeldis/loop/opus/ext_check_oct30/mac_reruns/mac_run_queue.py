#!/usr/bin/env python3
# Mac Studio runner. usage: python3 mac_run_queue.py KC_BIN CFAST_BIN JOBS CONFIGS XFILE OUT.tsv [shard k of n]
# build: c++ -O2 -std=c++17 -o kc loop/kc/kc.cpp ; c++ -O2 -std=c++17 -o cfast studio15/cfast.cpp  (wheeldis dir / studio15 dir of origin/main)
import sys, subprocess, os, time
kc,cf,jobf,cfgf,xf,resf=sys.argv[1:7]; k,n=(int(sys.argv[7]),int(sys.argv[8])) if len(sys.argv)>8 else (0,1)
L={l.split()[0]:l.strip() for l in open(cfgf)}; X=dict(l.split() for l in open(xf)) if os.path.exists(xf) else {}
done=set(tuple(l.split('\t')[:2]) for l in open(resf)) if os.path.exists(resf) else set()
for i,l in enumerate(open(jobf)):
    if i%n!=k: continue
    nm,eng=l.split()
    if (nm,eng) in done: continue
    tmp=resf+'.in%d'%k; open(tmp,'w').write(L[nm]+'\n'); t0=time.time()
    if eng=='kcD': cmd=[kc,tmp]
    elif eng=='cfD': cmd=[cf,tmp]
    elif eng=='kcC': open(tmp+'.x','w').write(nm+' '+X[nm]+'\n'); cmd=[kc,'-C','-x',tmp+'.x',tmp]
    else: cmd=[cf,tmp,'--fixed',X[nm].strip('{}')]
    o=subprocess.run(cmd,capture_output=True,text=True).stdout
    open(resf,'a').write('%s\t%s\t%.1f\t%s\n'%(nm,eng,time.time()-t0,' // '.join(x.strip() for x in o.splitlines())))
