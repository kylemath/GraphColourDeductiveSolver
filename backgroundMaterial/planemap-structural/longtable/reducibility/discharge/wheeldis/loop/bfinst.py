"""Round 1 probe P1b: per 7-instance (u of degree 7 with >= NMIN five-neighbours, in an R_opt-free patch), is some B-fixed
configuration (|S| >= 2, ring <= RMAX) D?  Tries large S first, stops at the first D.  dfast results cached in cache.txt."""
import sys, os, hashlib, itertools, collections, subprocess
W = sys.argv[1]; NMIN = int(sys.argv[2]); RMAX = int(sys.argv[3]); PATCHES = sys.argv[4].split(','); TAG = sys.argv[5]
DF = os.path.join(W, 'bin', 'dfast')
sys.argv = ['x', '/dev/null', '/dev/null']; __file__ = os.path.join(W, 'defect_check2.py')
src = open(__file__).read(); exec(src[:src.index("if __name__ == '__main__':")])
CACHE = {}
if os.path.exists('cache.txt'):
    for l in open('cache.txt'):
        k, v = l.split(); CACHE[k] = v
def dres(kb, cb):
    if kb not in CACHE:
        open('tmp_%s.txt' % TAG, 'w').write('%s %s\n' % (kb, cb))
        o = subprocess.run([DF, 'tmp_%s.txt' % TAG], capture_output=True, text=True).stdout
        CACHE[kb] = 'D' if 'D=true' in o else 'notD'
        open('cache.txt', 'a').write('%s %s\n' % (kb, CACHE[kb]))
    return CACHE[kb]
seen = set(); res = collections.Counter(); bad = []
for fn in PATCHES:
    for line in open(fn):
        sig = line.split('sig=')[1].split()[0]
        L, adj, nxt = patch(sig); deg = L.deg; outer = set(L.ring())
        for u in adj:
            if u in outer or deg.get(u) != 7: continue
            lk = rotf(nxt, u); snd = [x for x in lk if deg[x] == 5]
            if len(snd) < NMIN: continue
            cands = []
            for k in range(len(snd), 1, -1):
                for S in itertools.combinations(snd, k):
                    Ib = {u} | set(S)
                    for s in S: Ib |= adj[s]
                    if any(x in outer for x in Ib): cands = None; break
                    cb = extract_cfg(adj, deg, Ib)
                    if cb is None: continue
                    cands.append((-k, int(cb.split()[0]), 'b' + hashlib.sha1(cb.encode()).hexdigest()[:16], cb))
                if cands is None: break
            if cands is None: continue
            inst = tuple(sorted(c[2] for c in cands))
            if inst in seen: continue
            seen.add(inst)
            ok = None; skipped = 0
            for _, r, kb, cb in sorted(cands):
                if r > RMAX: skipped += 1; continue
                if dres(kb, cb) == 'D': ok = kb; break
            v = 'D' if ok else ('open' if skipped else 'notD')
            res[(len(snd), v)] += 1
            if not ok: bad.append((len(snd), sig, [deg[x] for x in lk], skipped))
            if len(seen) % 50 == 0: print(len(seen), dict(res), flush=True)
print('FINAL', dict(sorted(res.items())))
for b in bad: print('NOT-KILLED', b)
