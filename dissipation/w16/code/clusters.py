# W16: defect clusters in a 6-sea. Start from the 6-regular triangular lattice torus (p x p), apply k flips whose edges lie
# near the previous flips (BFS over flip sequences, dedup by canonical code), keep every state whose rows are all admissible
# with no payee kill (degrees in 5..9). Each kept state is a zero-Euler periodic pattern (its fundamental domain = the torus).
import sys, os, time, pickle, collections, random
sys.path.insert(0, '/tmp/swarm-W16/code')
import torus as TT, w16lib as W, explore as X
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)
def state_ok(T):
    if min(T.deg) < 5 or max(T.deg) > 9: return False
    for v in range(T.n):
        if X.vstat(T, v, {5, 6, 7, 8, 9}): return False
    return True
def near_edges(T, S, rad):
    B = set(S)
    for _ in range(rad): B |= {y for x in list(B) for y in T.adj[x]}
    return sorted({(min(u, v), max(u, v)) for (u, v) in T.opp if u in B and v in B})
if __name__ == '__main__':
    out = sys.argv[1]; p = int(sys.argv[2]); kmax = int(sys.argv[3]); budget = float(sys.argv[4]); rad = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    W.init()
    found = pickle.load(open(out, 'rb')) if os.path.exists(out) else {}
    T = TT.lattice_torus(p, 0, p); T.check()
    seen = set(); frontier = [(tuple(sorted(T.faces)), ())]   # (faces, touched vertices)
    for k in range(1, kmax + 1):
        new = []; nst = 0
        for faces, touched in frontier:
            if time.time() - T0 > budget: break
            S = TT.Torus(T.n, faces)
            cand = near_edges(S, touched, rad) if touched else [min((min(u, v), max(u, v)) for (u, v) in S.opp)]
            for (u, v) in cand:
                if time.time() - T0 > budget: break
                a = S.opp[(u, v)]; b = S.opp[(v, u)]
                if not S.flip(u, v): continue
                if min(S.deg) >= 4 and max(S.deg) <= 10:
                    code = frozenset(collections.Counter(TT.canon_ws(*TT.words(S, x)[:2]) for x in range(S.n)).items())
                    if code not in seen:
                        seen.add(code); nst += 1
                        new.append((tuple(sorted(S.faces)), tuple(sorted(set(touched) | {u, v, a, b}))))
                        if state_ok(S):
                            labs, cnt = W.pattern_rows(S)
                            if any(l[0] != 'C' for l in cnt) and frozenset(cnt) not in found:
                                found[frozenset(cnt)] = dict(faces=sorted(S.faces), n=S.n, cnt=cnt, tag='cluster p%d k%d' % (p, k), degs=collections.Counter(S.deg))
                                log('FOUND k=%d degs %s (total %d)' % (k, dict(collections.Counter(S.deg)), len(found)))
                                pickle.dump(found, open(out + '.tmp', 'wb')); os.replace(out + '.tmp', out)
                S.flip(a, b)
        log('k=%d: %d new states, %d found so far' % (k, nst, len(found)))
        frontier = new
        if len(frontier) > 6000: random.seed(k); frontier = random.sample(frontier, 6000)
    pickle.dump(found, open(out + '.tmp', 'wb')); os.replace(out + '.tmp', out)
    log('done, %d found' % len(found))
