import sys,collections; sys.path.insert(0,'.')
from astruct_delete import S
r=8
sols=S[r]
layer=[collections.OrderedDict() for _ in range(r)]
for seq,cc in sols:
    for i in range(r): layer[i].setdefault(seq[i],len(layer[i]))
for i in range(r):
    print("depth",i,[ "".join(map(str,x)) for x in layer[i]])
for i in range(r-1):
    tr=collections.defaultdict(set)
    for seq,cc in sols: tr[seq[i]].add(seq[i+1])
    print("trans",i,"->",i+1,{ "".join(map(str,a)):sorted("".join(map(str,b)) for b in bs) for a,bs in tr.items()})
