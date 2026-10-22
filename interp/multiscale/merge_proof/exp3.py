# Monodromy obstruction probe: two-vortex caps A, B (|t|=2 each, vortices deep). For every renaming: conflicts,
# |t_U| of the glued colouring, min R, and min w after that renaming's repair. Usage: python exp3.py map seed ncol
import sys, json, time, random, math
sys.path.insert(0, '/mnt/project-files/multiscale/merge_proof')
from mp import *
from exp1 import pairs

def tU(D, col):
    return tvec(D.whole, col)

def per_renaming(g, D, A, B, colA, colB, Rmax=4, wmax=6):
    seam = [(u, w) for (u, w) in D.edges if (u in A) != (w in A)]
    dB = multi_bfs(g.adj, list(D.bset), D.S); rows = []
    for p in PERMS:
        cc = {v: colA[v] for v in A}; cc.update({v: p[colB[v]] for v in B})
        K = set(x for e in seam if cc[e[0]] == cc[e[1]] for x in e)
        R = None
        for RR in range(Rmax+1):
            r, c2 = (0, cc) if not K else proper_repair_at(g, D.S, cc, K, RR)
            if r is not None: R = RR; break
        row = dict(perm=''.join(map(str, p)), nconf=len(K), tU_glued=tU(D, cc), R=R)
        if R is not None:
            row['tU_rep'] = tU(D, c2); zone = set(v for v in D.S if c2[v] != cc[v])
            w = None
            for ww in range(wmax+1):
                fx = {v: c2[v] for v in D.S if dB[v] > ww and v not in zone}
                r = sat2(D, D.pockets, 1.0, fixed=fx)
                if r not in (None, 'UNK'): w = ww; break
                if r == 'UNK': w = 'UNK%d' % ww; break
            row['w'] = w if w is not None else '>%d' % wmax
        rows.append(row)
    return rows

if __name__ == '__main__':
    name, seed, ncol = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    g = G(make(name)); rng = random.Random(seed)
    log = open('/mnt/project-files/multiscale/merge_proof/exp3_%s_s%d.jsonl' % (name, seed), 'a')
    for A, B in pairs(g, 'cap2big', rng, nmax=4):
        D = Disc(g, A | B); dB = multi_bfs(g.adj, list(D.bset), D.S)
        odd = [v for v in D.S if g.deg[v] % 2 and v not in D.bset]
        depths = sorted(dB[o] for o in odd)
        cA = level_cols(g, A, ncol, 'nonzero', seed0=7*seed, budget=4*10**7); cB = level_cols(g, B, ncol, 'nonzero', seed0=7*seed+3, budget=4*10**7)
        if not cA or not cB: print('no forced-nonzero colourings', len(A), len(B)); continue
        for ca in cA:
            for cb in cB:
                t0 = time.time(); rows = per_renaming(g, D, A, B, ca, cb)
                ok = [r for r in rows if r['R'] is not None]
                best = min(((r['w'] if isinstance(r['w'], int) else 99), r['R']) for r in ok) if ok else None
                rec = dict(map=name, nA=len(A), nB=len(B), mU=len(D.whole['walk']), nodd=len(odd), depths=depths, tA=tvec(Disc(g, A).whole, ca), tB=tvec(Disc(g, B).whole, cb),
                           best_w_R=best, minR=min(r['R'] for r in ok) if ok else None, rows=rows, sec=round(time.time()-t0, 1))
                log.write(json.dumps(rec)+'\n'); log.flush()
                print({k: rec[k] for k in ('nA', 'nB', 'mU', 'nodd', 'depths', 'tA', 'tB', 'best_w_R', 'minR', 'sec')}, [(r['perm'], r['nconf'], r['tU_glued'], r['R'], r.get('w')) for r in rows if r['R'] is not None][:8], flush=True)
