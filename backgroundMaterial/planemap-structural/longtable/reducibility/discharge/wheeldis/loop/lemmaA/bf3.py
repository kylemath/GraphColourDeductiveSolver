"""Round-1 probe P1b redone from the cache (no new dfast): every 7 with exactly NF fives in the R_opt-free K = 3
patches; per instance (distinct candidate set) is some B-fixed K(S) at ring <= RMAX D?  Also cross-checks la.py: the
abstract situation (L, s) read off the patch must give the same canonical K(S) keys as the patch itself.
Usage: python3 bf3.py LOOPDIR NF RMAX PATCHFILES(comma)  -> bf3_misses_<NF>.txt"""
import sys, os, itertools, collections, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import la
LD, NF, RMAX, PF = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4].split(',')
_s = open(os.path.join(la.W, 'defect_check2.py')).read(); _sv = sys.argv; sys.argv = ['x', '/dev/null', '/dev/null']
g = {'__file__': os.path.join(la.W, 'defect_check2.py')}; exec(_s[:_s.index("if __name__ == '__main__':")], g); sys.argv = _sv
C = dict(l.split()[:2] for l in open(os.path.join(LD, 'cache.txt')))
V = {}
for l in open(os.path.join(la.HERE, 'vcache.txt')):
    f = l.split(); V[f[0]] = f[1]
seen = set(); res = collections.Counter(); xc = collections.Counter(); miss = []
for fn in PF:
    for line in open(fn):
        sig = line.split('sig=')[1].split()[0]
        L, adj, nxt = g['patch'](sig); deg = L.deg; outer = set(L.ring())
        for u in adj:
            if u in outer or deg.get(u) != 7: continue
            lk = g['rotf'](nxt, u); F = [i for i in range(7) if deg[lk[i]] == 5]
            if len(F) != NF: continue
            sv = []
            for i in range(7):
                com = [z for z in adj[lk[i]] & adj[lk[(i + 1) % 7]] if z != u]; sv.append(com[0])
            J = set(F) | {(i - 1) % 7 for i in F}
            Lw = tuple(deg[x] for x in lk); sw = tuple(deg[sv[i]] if i in J else 0 for i in range(7))
            cands = []; bad = False
            for k in range(len(F), 1, -1):
                for S in itertools.combinations(F, k):
                    Ib = {u} | {lk[i] for i in S}
                    for i in S: Ib |= adj[lk[i]]
                    if any(x in outer for x in Ib): bad = True; break
                    cb = g['extract_cfg'](adj, deg, Ib)
                    if cb is None: continue
                    kb = 'b' + hashlib.sha1(cb.encode()).hexdigest()[:16]; ck = la.ckey(cb)
                    cands.append((int(cb.split()[0]), -k, S, kb, ck, cb))
                if bad: break
            if bad: continue
            inst = tuple(sorted(c[3] for c in cands))
            if inst in seen: continue
            seen.add(inst)
            # cross-check against the abstract builder
            adj2, deg2, w2, sv2, kn2 = la.build(Lw, sw)
            for r, mk, S, kb, ck, cb in cands:
                cb2 = la.KS(adj2, deg2, w2, sv2, kn2, S); xc['same' if cb2 and la.ckey(cb2) == ck else 'DIFF'] += 1
            hit = None; unt = 0
            for r, mk, S, kb, ck, cb in sorted(cands):
                if r > RMAX: continue
                v = C.get(kb) or V.get(ck)
                if v is None: unt += 1; continue
                if v == 'D': hit = (r, -mk); break
            v = 'D' if hit else ('untested' if unt else 'noD')
            res[v] += 1
            if not hit:
                miss.append((sig, ''.join(map(str, Lw)), ''.join(map(str, sw)),
                             [(r, -mk, ''.join(map(str, S)), C.get(kb) or V.get(ck) or '?', ck, cb) for r, mk, S, kb, ck, cb in sorted(cands)]))
print('instances', len(seen), dict(res), 'crosscheck', dict(xc))
with open(os.path.join(la.HERE, 'bf3_misses_%d.txt' % NF), 'w') as f:
    for sig, Lw, sw, cs in miss:
        f.write('MISS %s %s sig=%s\n' % (Lw, sw, sig))
        for r, k, S, v, ck, cb in cs: f.write('  r=%d |S|=%d S=%s %s %s %s\n' % (r, k, S, v, ck, cb))
