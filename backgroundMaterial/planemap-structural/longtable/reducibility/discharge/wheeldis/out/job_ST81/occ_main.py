# ST-81: which of P05 (K3l5k kill), P06-P08 occur on the 2 failing K3l5j receivers. cwd wheeldis
C='out/job_ST67/chk/h05/'
src0 = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = '%s'" % C).replace("open(K + 'configs.kc')", "open(K + 'cfg.in')")
exec(src0)
H={'P05':'out/job_ST67/chk/h05/cfg.in','P06':'out/job_ST76/chk/h06/cfg.in','P07':'out/job_ST76/chk/h07/cfg.in','P08':'out/job_ST76/chk/h08/cfg.in'}
H={n:open(p).read().strip() for n,p in H.items()}
for r in ['55676676/56665666','56766765/66656665']:
    L,S=r.split('/'); print(r,[n for n,k in H.items() if occurs(k,len(L),L,S)[1]>0])
