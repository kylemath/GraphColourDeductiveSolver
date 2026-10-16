"""Per-situation check of A(k) (engine level, exploratory).  For each situation (L s) build every K(S), |S| >= 2,
order by ring ascending (ties: larger S first), stop at the first D (dfast <= 16; dfast18 17..RMAX).
Verdicts cached by canonical configuration key (la.ckey) in vcache.txt (seeded from the round-1 cache).
Usage: python3 inst.py SITFILE RMAX TAG [cfast]   -> res_<TAG>.txt (one line per situation)"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from la import *
SITF, RMAX, TAG = sys.argv[1], int(sys.argv[2]), sys.argv[3]; DOC = 'cfast' in sys.argv[4:]
BIN = os.path.join(W, 'bin'); VC = os.path.join(HERE, 'vcache.txt')
V = {}
if os.path.exists(VC):
    for l in open(VC):
        k, v = l.split()[:2]; V[k] = v
def run(binname, args, cb, kb):
    tmp = os.path.join(HERE, 'tmp_%s.txt' % TAG); open(tmp, 'w').write('%s %s\n' % (kb, cb))
    t0 = time.time()
    o = subprocess.run(['nice', '-n', '10', os.path.join(BIN, binname), tmp] + args, capture_output=True, text=True).stdout
    return o, time.time() - t0
def dverd(kb, cb, r):
    if kb in V and V[kb] in ('D', 'notD'): return V[kb]
    if r <= 16: o, dt = run('dfast', [], cb, kb)
    else: o, dt = run('dfast18', [], cb, kb)
    v = 'D' if 'D=true' in o else ('notD' if 'D=false' in o else 'err')
    if v != 'err':
        V[kb] = v; open(VC, 'a').write('%s %s r=%d %.1fs\n' % (kb, v, r, dt))
    return v
def cverd(kb, cb):
    if V.get(kb + 'C'): return V[kb + 'C']
    o, dt = run('cfast', ['--search', '--limit', '1'], cb, kb)
    v = 'C' if 'C-REDUCIBLE' in o else ('noC' if 'search |X|' in o else 'err')
    if v != 'err':
        V[kb + 'C'] = v; open(VC, 'a').write('%sC %s %.1fs\n' % (kb, v, dt))
    return v
def cands(L, s):
    adj, deg, w, sv, known = build(L, s)
    F = [j for j in range(7) if L[j] == 5]; out = []; seen = set()
    for k in range(len(F), 1, -1):
        for S in itertools.combinations(F, k):
            cb = KS(adj, deg, w, sv, known, S)
            if cb is None: out.append((99, -k, S, None, None)); continue
            kb = ckey(cb)
            if kb is None: kb = 'h' + hashlib.sha1(cb.encode()).hexdigest()[:16]
            if kb in seen: continue
            seen.add(kb); out.append((int(cb.split()[0]), -k, S, kb, cb))
    return sorted(out)
if __name__ == '__main__':
    fo = open(os.path.join(HERE, 'res_%s.txt' % TAG), 'a'); t0 = time.time()
    for line in open(SITF):
        Ls, ss = line.split()[:2]; L = tuple(map(int, Ls)); s = tuple(map(int, ss))
        cs = cands(L, s); hit = None; tried = []; skipped = 0
        for r, mk, S, kb, cb in cs:
            if kb is None: continue
            if r > RMAX: skipped += 1; continue
            v = dverd(kb, cb, r); tried.append((r, -mk, v))
            if v == 'D': hit = (r, -mk, S, kb); break
        if hit is None and DOC:
            for r, mk, S, kb, cb in cs:
                if kb is None or r > 15: continue
                if cverd(kb, cb) == 'C': hit = (r, -mk, S, kb + 'C'); break
        rings = ','.join(str(c[0]) for c in cs)
        if hit: fo.write('%s %s HIT r=%d |S|=%d S=%s %s rings=%s\n' % (Ls, ss, hit[0], hit[1], ''.join(map(str, hit[2])), hit[3], rings))
        else: fo.write('%s %s MISS skipped=%d tried=%s rings=%s\n' % (Ls, ss, skipped, ';'.join('%d/%d/%s' % t for t in tried), rings))
        fo.flush()
    print('done %.0fs' % (time.time() - t0))
