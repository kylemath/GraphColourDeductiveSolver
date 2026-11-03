# job R3A2 (Studio): is a configuration (kc line) already present, up to rotation/reflection (configuration isomorphism), among
# every kc line committed in the repo (loop/k*/, loop/studio/, out/), RSST 633 (loop/k44/rsst.txt) and nl51 (8,200)?
# Isomorphism = Studio's induced embedding (explore grow.py embeddings) of the query onto a same-size candidate with exact degrees
# and interior triangles onto triangles. Candidates prefiltered by (r, m, sorted degrees, sorted degree-pair edge list).
import os, sys, glob, re, collections
HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
G = {'__file__': os.path.join(HERE, 'loop', 'k42', 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
def inv(c):
    nm, tag, U, g, E, tri = c
    return (len(U), tuple(sorted(g.values())), tuple(sorted(tuple(sorted((g[a], g[b]))) for a in U for b in E[a] if a < b)))
def iso(c, d):
    if inv(c) != inv(d): return False
    P = list(d[2]); pa = {x: set(d[4][x]) for x in P}; pf = set(d[5]); fd = dict(d[3])
    return len(G['embeddings'](c, P, pa, pf, fd)) > 0
Q = [G['kcline'](open(f).read().split('\n')[0], 'q') for f in sys.argv[1:]]
for f, q in zip(sys.argv[1:], Q): q_r = open(f).read().split()[1]; print('query', q[0], 'r', q_r, 'm', len(q[2]))
qi = [(inv(q), int(open(f).read().split()[1])) for f, q in zip(sys.argv[1:], Q)]
hits = collections.defaultdict(set); nlines = 0; seen = set(); hits_key = set()
files = [f for pat in ('loop/k[0-9]*/*', 'loop/k[0-9]*/*/*', 'loop/studio/**/*', 'out/**/*', 'loop/kc/*') for f in glob.glob(os.path.join(HERE, pat), recursive=True)]
files = [f for f in files if os.path.isfile(f) and 'teamB' not in f and 'job_R3A2' not in f and os.path.getsize(f) < 200_000_000]
for fn in sorted(set(files)):
    try: lines = open(fn, errors='strict').read().splitlines()
    except Exception: continue
    for l in lines:
        t = l.split()
        if len(t) < 5 or not (t[1].isdigit() and t[2].isdigit()) or ';' not in t[3] + t[4]: continue
        key = ' '.join(t[1:5])
        try: r = int(t[1])
        except: continue
        if not any(r == qr for _, qr in qi): continue
        if key in seen:
            for k, q in enumerate(Q):
                if (k, key) in hits_key: hits[k].add((t[0], os.path.relpath(fn, HERE)))
            continue
        seen.add(key); nlines += 1
        try: c = G['kcline'](' '.join(t[:5]), 'x')
        except Exception: continue
        for k, q in enumerate(Q):
            if r == qi[k][1] and iso(q, c): hits[k].add((t[0], os.path.relpath(fn, HERE))); hits_key.add((k, key))
    if 'hits_key' not in dir(): pass
print('distinct candidate kc lines at the query rings: %d' % nlines)
for k, q in enumerate(Q):
    print('== %s: %d occurrences (name, file) of isomorphic configurations' % (q[0], len(hits[k])))
    for h in sorted(hits[k])[:60]: print('   ', h[0], h[1])
