import sys; sys.path.insert(0,'.')
from astruct_list import listsol
R=7
sols={r:listsol(r) for r in range(3,R+1)}
S={r:{tuple(seq):cc for seq,cc in sols[r]} for r in sols}
for r in range(4,R+1):
    full=set(tuple(seq) for seq,cc in sols[r])
    p1=[s for s in full if tuple(s[:-1]) in S[r-1]]
    p2=[s for s in full if r-2>=3 and tuple(s[:-2]) in S[r-2]]
    print("r",r,"solutions",len(full),"with (r-1)-prefix a solution:",len(p1),"with (r-2)-prefix a solution:",len(p2),"both",len([s for s in p1 if s in p2]))
    # prefixes of full solutions (any cap)
for r in range(3,R+1):
    cores=set(tuple(seq[:-1]) for seq,cc in sols[r])
    print("r",r,"distinct (r-1)-prefix cores",len(cores),"solutions",len(sols[r]))
# print the last ring + cap options per prefix
import collections
for r in (6,):
    d=collections.defaultdict(list)
    for seq,cc in sols[r]: d[tuple(seq[:-1])].append((seq[-1],cc))
    for k,v in d.items(): print(" ".join("".join(map(str,x)) for x in k),"->",[ "".join(map(str,a))+"/"+str(b) for a,b in v])
