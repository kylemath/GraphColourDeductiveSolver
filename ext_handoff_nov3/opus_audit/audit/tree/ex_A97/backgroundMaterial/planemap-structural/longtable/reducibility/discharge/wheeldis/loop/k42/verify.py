"""Round 42: cut every (config, image) that kills a case out of a representative 2-ball (free slots at 7) and write
it as a kc/dfast line (cut.txt), one per distinct window.  usage: python3 verify.py"""
import os, sys, collections
H = os.path.dirname(os.path.abspath(__file__))
G = {'__file__': os.path.join(H, 'grow.py'), '__name__': 'grow'}; exec(open(G['__file__']).read(), G)
P, pa, pf = G['structure'](); fd = G['fixed_deg'](); VAR = G['VAR']
C = G['rsst']() + G['explore_kills']()
rows, seen = [], {}
for c in C:
    for e in G['embeddings'](c, P, pa, pf, fd):
        req = dict((v, c[3][u]) for u, v in e if v not in fd)
        key = tuple(req.get(x, 0) for x in VAR)
        if key[0] == 5 or key[1] == 5: continue
        a, b = key[0] or 7, key[1] or 7; p = tuple(k or 7 for k in key[2:])
        img = frozenset(v for _, v in e)
        tag = 'k42_%s_%s' % (c[0].replace('.', 'o'), ''.join(str(k) if k else 'x' for k in key))
        line = G['cut'](img, a, b, p, tag)
        if line is None: print('NOT SIMPLE', c[0], key); continue
        sig = (key, ' '.join(line.split()[1:]))
        if sig in seen: continue
        seen[sig] = tag; rows.append((c[1], line))
        dg = sorted(c[3].values())
        print('%-22s %-26s ring %2s m %2s degrees %s' % (tag, c[1], line.split()[1], line.split()[2], ''.join(map(str, dg))))
open(os.path.join(H, 'cut.txt'), 'w').write(''.join(l + '\n' for _, l in sorted(rows, key=lambda x: int(x[1].split()[1]))))
print('windows', len(rows))
