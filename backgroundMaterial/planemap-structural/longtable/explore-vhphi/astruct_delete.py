import sys,collections; sys.path.insert(0,'.')
from astruct_list import listsol
from astruct_census import compat
R=8
def load(r):
    if r>=7:
        out=[]
        for l in open('/private/tmp/claude-501/x/l%d.txt'%r).read().splitlines()[1:]:
            p=l.split(); out.append((tuple(tuple(map(int,x)) for x in p[:-2]),int(p[-1])))
        return out
    return [(tuple(seq),cc) for seq,cc in listsol(r)]
S={r:load(r) for r in range(3,R+1)}
Sset={r:set(S[r]) for r in S}
for d in (1,2):
    for r in range(3+d,R+1):
        cnt=collections.Counter(); 
        for seq,cc in S[r]:
            ok=[]
            for i in range(1,r-d+0):  # delete rings i..i+d-1, keep ring0 and last ring
                new=seq[:i]+seq[i+d:]
                if len(new)==r-d and all(compat(new[k],new[k+1]) for k in range(len(new)-1)) and (new,cc) in Sset[r-d]:
                    ok.append(i)
            cnt[tuple(ok)]+=1
        print("delete",d,"ring(s): r",r,"->",r-d," positions i that give a solution:",dict(cnt))
