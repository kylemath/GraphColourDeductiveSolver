import sys,pickle,collections,glob,os
sys.path.insert(0,'/mnt/project-files/multiscale/binder_maps')
import build
from binder import canon,canon_link
HARD={'5566776','5566767','5566766'}
for f in sorted(glob.glob('/mnt/project-files/multiscale/binder_maps/*.pkl')):
    name=os.path.basename(f)[:-4]
    if name.startswith('case'): continue
    adj=pickle.load(open(f,'rb'))
    if not isinstance(adj,list): continue
    deg,full,lo=build.census(adj); st,c4=build.sep_checks(adj)
    rows=collections.Counter(); hardfull=0; hardlink=0
    for u in full+lo:
        o,sv,L,S=build.words(adj,u); k=canon(L,S)
        if u in set(full): rows[k]+=1
        if canon_link(L) in HARD:
            hardlink+=1; hardfull+= (k in build.ROWS)
    fs=set(full); near=len(build.ball(adj,full,1)) if full else 0
    print('| %s | %d | %s | %d | %d | %d | %d/%d | %d | %d/%d |'%(name,len(adj),' '.join('%d:%d'%kv for kv in sorted(deg.items())),len(full),len(rows),len(lo),hardfull,hardlink,near,st,c4))
    if rows: print('   top rows:',', '.join('%s/%s x%d'%(k[0],k[1],c) for k,c in rows.most_common(6)))
