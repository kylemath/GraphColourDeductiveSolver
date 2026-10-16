"""EXPLORE round 10 (exploratory): turn hash-named D configurations at a binder's centre into f<d>_ wlp3 patterns.
For each binder arrangement, builds every B-fixed variant with gen28.py's own builder (any S, |S| >= 2, ring <= 19)
and compares its canonical key (lemmaA la.ckey) with the canonical keys of the D configurations in DFILE (dfast lines
'name r m ra ia', verdicts from VFILE).  A key match means the hash-named D configuration IS that B-fixed
configuration, so 'f<d>_.. D=true' is a valid pattern line.
Usage: python3 tof.py BINDERS DLINES VERDICTS... > PATFILE"""
import sys, os
W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIND, DL, VF = sys.argv[1], sys.argv[2], sys.argv[3:]
src = open(os.path.join(W, 'gen28.py')).read(); src = src[:src.rindex('arrs = []')]
sys.argv = ['gen28.py', '/dev/null', '19']; G = {'__file__': os.path.join(W, 'gen28.py'), '__name__': 'g28'}; exec(src, G)
sys.path.insert(0, os.path.join(W, 'loop', 'lemmaA')); _a = sys.argv; sys.argv = ['x']; import la; sys.argv = _a
D = set()
for fn in VF:
    for line in open(fn):
        if 'D=true' in line: D.add(line.split()[0])
keys = {}
for line in open(DL):
    f = line.split(None, 1)
    if f[0] in D: keys[la.ckey(f[1].strip())] = f[0]
print('# %d D configurations to match' % len(keys), file=sys.stderr)
for line in open(BIND):
    f = line.split()
    if len(f) < 2: continue
    d, lk, sv = len(f[0]), f[0], f[1]
    for (r, k, S, w, s, nm) in G['variants'](d, lk, sv):
        c = G['make'](d, r, S, w, s, nm)
        if c is None or c.startswith('RING'): continue
        kk = la.ckey(c.split(None, 1)[1])
        if kk in keys: print('%s r=%d D=true via %s (binder %s/%s S=%s, defect round 10)' % (nm, r, keys[kk], lk, sv, S))
