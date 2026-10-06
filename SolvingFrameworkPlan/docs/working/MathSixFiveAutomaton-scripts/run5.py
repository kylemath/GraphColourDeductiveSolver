from auto import *
import time
for k in (4,5):
    t=time.time()
    bad=[p for p in pats if radius_bound(init(p),k) is None]
    print('k',k,'unresolved',len(bad),round(time.time()-t,1),'cache',g.cache_info().currsize,flush=True)
