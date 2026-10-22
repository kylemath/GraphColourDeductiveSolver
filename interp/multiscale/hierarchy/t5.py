import sys, time, collections, random
sys.path.insert(0,'/mnt/project-files/multiscale/hierarchy')
from hier import *
g=G(icosphere(10)); t=time.time()
st=build(g,L=12,seed=0,exh=16)
first=[b for b in st['bad'] if b['chordlessU']]
print('bad',len(st['bad']),'bad with chordless parent',len(first))
for b in first: print(b)
print('q',collections.Counter(st.get('q',[])), time.time()-t)
