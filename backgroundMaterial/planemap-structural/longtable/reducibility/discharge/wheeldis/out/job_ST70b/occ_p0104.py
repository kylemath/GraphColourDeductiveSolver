# ST-70b: which of P01-P04 (K3CHK occurs, rotation-preserving) occur on each failing receiver row. cwd wheeldis
C='out/job_ST67/chk/h01/'
src0 = open('out/job_K3CHK/rowcheck.py').read().split("out = open(K + 'per_row.tsv'")[0].replace("K = 'out/job_K3CHK/'", "K = '%s'" % C).replace("open(K + 'configs.kc')", "open(K + 'cfg.in')")
exec(src0)
H={n:open('out/job_ST67/chk/h%s/cfg.in'%n).read().strip() for n in ['01','02','03','04']}
for l in open('out/job_ST70b/main_receiver_violators.txt'):
    d,L,S,v=l.split()
    r=[n for n,k in H.items() if occurs(k,len(L),L,S)[1]>0]
    print(L+'/'+S,v,'P'+',P'.join(r) if r else 'NONE')
