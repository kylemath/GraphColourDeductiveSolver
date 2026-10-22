import sys, time, collections, random
sys.path.insert(0,'/mnt/project-files/multiscale/hierarchy')
from hier import *
for f in [5,10]:
    g=G(icosphere(f)); t=time.time()
    st=build(g,L=12,seed=0,exh=12)
    print(f,g.n,'nodes',st['nodes'],'bad',len(st['bad']),st['bad'][:5],'unsplit',collections.Counter(st['unsplit']),'leaves',collections.Counter(st['leaves']).most_common(5),'maxleaf',max(st['leaves']),'depth',st['depth'],'rep',st['rep'],'minbal',round(min(st['balance']),2),'sec',round(time.time()-t,1),flush=True)
