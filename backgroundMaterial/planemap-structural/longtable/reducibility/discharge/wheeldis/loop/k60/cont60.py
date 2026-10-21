"""EXPLORE round 60: registry containment inside the interior of each window of a kc-line file (another thread's data,
read as data).  Faces: the interior triangles, after checking that no interior vertex has a chord in its link (so every
interior triangle is a face).  Registry = RSST 582 + twoeng names of TD/TC; 2026 set = XKC.
usage: python3 cont60.py TD TC XKC FILE"""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'k59'))
TD, TC, XKC, FN = sys.argv[1:5]; sys.argv = sys.argv[:1]
import chain59 as C, grow
REG, miss = C.F.registry(TD, TC)
XR = [grow.kcline(l, 'xreg') for l in open(XKC) if l.strip()]
print('# cont60: registry %d (%d names not found), 2026 set %d, file %s' % (len(REG), miss, len(XR), FN))
for line in open(FN):
    if not line.strip() or line.startswith('#'): continue
    f = line.split(); r, m = int(f[1]), int(f[2]); ra = f[3].split(';'); ia = f[4].split(';')
    adj = {('i', v): set() for v in range(m)}
    for i in range(r): adj.setdefault(('r', i), set())
    for i in range(r): adj[('r', i)].add(('r', (i + 1) % r)); adj[('r', (i + 1) % r)].add(('r', i))
    for v in range(m):
        for x in ([] if ra[v] == '-' else ra[v].split(',')): adj[('i', v)].add(('r', int(x))); adj[('r', int(x))].add(('i', v))
        for x in ([] if ia[v] == '-' else ia[v].split(',')): adj[('i', v)].add(('i', int(x)))
    chord = [v for v in range(m) if sum(len(adj[a] & adj[('i', v)]) for a in adj[('i', v)]) // 2 != len(adj[('i', v)])]
    c = grow.kcline(line, 'win'); P = c[2]; pa = c[4]; pf = c[5]; fd = c[3]
    def inside(CONF):
        return sorted({k[0] for k in CONF if len(k[2]) <= len(P) and grow.embeddings(k, P, pa, pf, fd)})
    hr = inside(REG); hx = inside(XR)
    print('%s r%d m%d%s | registry: %s | 2026 set: %s' % (f[0], r, m, ' (link chord at %s)' % chord if chord else '',
          ' '.join(hr) or '-', ' '.join(hx) or '-'), flush=True)
