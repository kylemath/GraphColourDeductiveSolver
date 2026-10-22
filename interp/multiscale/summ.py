import sys,re,collections
for fn in sys.argv[1:]:
    prev=0; byL=collections.defaultdict(list)
    for line in open(fn):
        m=re.search(r'merge L(\d+) size (\d+) conflicts (\d+) R=(\d+) timeouts_so_far=(\d+)',line)
        if not m: continue
        L,sz,nc,R,t=map(int,m.groups())
        if nc: byL[L].append((R,t>prev,sz))
        prev=t
    print(fn)
    for L in sorted(byL):
        v=byL[L]; mx=max(v)
        print('  L%2d merges-with-conflicts %3d  maxR %2d%s  maxSize %d  R-hist %s'%(L,len(v),mx[0],' (upper bd: SAT timeouts)' if any(x[1] for x in v if x[0]==mx[0]) else '',max(x[2] for x in v),dict(sorted(collections.Counter(x[0] for x in v).items()))))
