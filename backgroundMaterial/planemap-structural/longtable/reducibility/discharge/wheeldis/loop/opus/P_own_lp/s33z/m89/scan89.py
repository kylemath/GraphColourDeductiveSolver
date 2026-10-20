# m89: where do the 89 XRing C names occur among the A64 args files? (C-REDUCIBLE in cpat files, D=true in pat files)
import sys, os, re, collections
args = open(sys.argv[1]).read().split(); root = sys.argv[2]; names = [l.split()[0] for l in open(sys.argv[3]) if l.strip() and not l.startswith('#')]
N = set(names); assert len(N) == len(names) == 89, (len(N), len(names))
hit = collections.defaultdict(list)
for a in args:
    if not a.startswith(('pat=', 'cpat=')): continue
    fn = a.split('=', 1)[1]; allf = fn.endswith(':all'); fn = fn[:-4] if allf else fn
    p = fn if os.path.isabs(fn) else os.path.join(root, fn)
    if not os.path.exists(p): continue
    if a.startswith('pat='):
        for line in open(p):
            w = line.split()
            if w and w[0] in N and (allf or 'D=true' in line): hit[w[0]].append(('D', fn))
    else:
        cur = None
        for line in open(p):
            if ' r=' in line and not line.startswith(' '): cur = line.split()[0]
            elif 'C-REDUCIBLE' in line and cur in N: hit[cur].append(('C', fn))
c = collections.Counter()
for n in names:
    ks = hit[n]; kinds = tuple(sorted(set(k for k, _ in ks)))
    c[(kinds, len(ks))] += 1
    if len(ks) != 1: print(n, ks)
print('summary (kinds, #sources) -> count:', dict(c))
print('found', sum(1 for n in names if hit[n]), 'of 89')
