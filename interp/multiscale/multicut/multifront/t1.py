import sys, time; sys.dont_write_bytecode=True; sys.path.insert(0,'.')
import mf
for spec in sys.argv[1:]:
    t=time.time(); r=mf.job(spec)
    print({k:r[k] for k in ('spec','n','diam','mind','status','err','steps','colored','maxR','Rhist','nskip','sec')}, r.get('proper'))
    from collections import Counter
    print(Counter(x[3] for x in r['recs']), 'maxcuts', max(max([w[1] for w in x[6]],default=0) for x in r['recs']), 'maxt', max(max([w[2] for w in x[6]],default=0) for x in r['recs']))
    print(r['fails'][:3]); print(r['dual']['edges'][:10], r['dual']['triangles'][:10])
