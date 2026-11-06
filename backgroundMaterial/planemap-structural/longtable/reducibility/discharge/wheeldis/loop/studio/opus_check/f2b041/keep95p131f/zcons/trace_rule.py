"""ZCONS step 1 (Studio): trace which (Z, r, embedding) of OUR f2b_rulecheck DERIVE emits a given rule. Loads f2b_rulecheck.py's
preamble (forbidden set, frame, targets, job) without running its main block, then replays DERIVE's emission for one config."""
import sys, os, json
CFG, D, W0, SG = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
RULE = json.loads(sys.argv[5])
sys.argv = ['f2b_rulecheck.py', 'x', 'y']
M = {'__name__': 'f2b_trace', '__file__': os.path.abspath('out/job31/f2b_rulecheck.py')}
exec(open('out/job31/f2b_rulecheck.py').read(), M)
G = M['G']; cfg = [c for c in M['FORB'] if c[0] == CFG]; assert len(cfg) == 1, len(cfg); cfg = cfg[0]
want = (RULE[0], tuple(sorted((k, tuple(al)) for k, al in RULE[1])), tuple(sorted((k, v) for k, v in RULE[2])))
print('config', CFG, 'interior degrees', cfg[3])
for Z in range(0, 1 << D, 2):
    pa, pf = M['frame'](D, W0, Z)
    P = ([('u',)] if D in (7, 8) else []) + [('w', k) for k in range(D)] + [('s', k) for k in range(D)] + sorted(x for x in pa if x[0] == 'p' and x[1] == 0)
    fd = {('w', 0): W0}
    if D in (7, 8): fd[('u',)] = D
    Ps = set(P); pa2 = {x: pa[x] & Ps for x in P}; pf2 = {f for f in pf if f <= Ps}
    tt = tuple(M['targets'](D, W0, pa)[int(SG)])
    for e in G['embeddings'](cfg, P, pa2, pf2, fd):
        r = tuple(sorted((v, cfg[3][u]) for u, v in e if v not in fd)); rd = dict(r)
        if tt not in rd or any(v[0] == 'p' and v != tt for v in rd): continue
        wq = {v[1]: (g,) for v, g in r if v[0] == 'w'}; sq = {v[1]: g for v, g in r if v[0] == 's'}
        for k in range(1, D):
            if (k - 1) in sq and k in sq and k not in wq: wq[k] = (5,) if (Z >> k) & 1 else (6, 7, 8, 9)
        rule = (rd[tt], tuple(sorted(wq.items())), tuple(sorted(sq.items())))
        if rule != want: continue
        bits = ''.join(str((Z >> k) & 1) for k in range(D))
        incons = [(k, g) for (v, g) in r if v[0] == 'w' and v[1] >= 1 for k in [v[1]] if (g == 5) != bool((Z >> k) & 1)]
        emap = {v: u for u, v in e}
        used_edges = [(a, b) for a in emap for b in emap if a < b and b in pa2[a] and emap[b] in cfg[4].get(emap[a], set())]
        sep = [(('s', k - 1), ('s', k)) for k in range(1, D) if (Z >> k) & 1 and ('s', k - 1) in emap and ('s', k) in emap and emap[('s', k)] in cfg[4][emap[('s', k - 1)]]]
        faces = [sorted(f) for f in pf2 if all(x in emap for x in f) and frozenset(emap[x] for x in f) in cfg[5]]
        print('EMITTED at Z=%d (bits w_0..w_%d: %s)' % (Z, D - 1, bits))
        print('  r =', r)
        print('  r vs Z inconsistent (w_k, letter in r) where (letter==5) != bit k:', incons)
        print('  embedding (frame vertex -> cfg vertex):', sorted(emap.items()))
        print('  s_{k-1}~s_k edges used by the embedding (only present when bit k = 1):', sep)
        print('  faces of the frame used that contain an s_{k-1},s_k pair:', [f for f in faces if any(('s', k - 1) in f and ('s', k) in f for k in range(1, D))])
