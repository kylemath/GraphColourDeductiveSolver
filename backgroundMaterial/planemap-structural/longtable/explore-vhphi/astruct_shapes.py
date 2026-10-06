import sys,itertools; sys.path.insert(0,'.')
def canon_ring(c):
    best=None
    for k in range(5):
        x=c[k:]+c[:k]; mp={};o=[]
        for y in x:
            if y not in mp: mp[y]=len(mp)
            o.append(mp[y])
        o=tuple(o)
        if best is None or o<best: best=o
    return "".join(map(str,best))
rows=[l.split() for l in open(sys.argv[1]).read().splitlines()[1:]]
import collections
sh=collections.Counter()
for l in rows:
    rg=[tuple(map(int,x)) for x in l[:-2]]
    shapes=[canon_ring(x) for x in rg]
    sh[tuple(shapes)]+=1
for k,v in sorted(sh.items()): print(" ".join(k),v)
