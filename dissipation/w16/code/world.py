# W16: "world" LPs. A world = a set of letters (degrees). Rows: every admissible receiverR2 arrangement of the given degrees whose
# link and second ring use only world letters (2-ball admissibility exactly as st21 admissible()), every senderR2 row whose word uses
# only world letters, every cons2 row of a non-R6 world 6-word (all ap apex-class words), + mrow closure.
# The world rows are a subset of the full LP's rows, so min t over them is a lower bound on t* (same families).
# Any doubly periodic triangulation with degrees in the world whose vertices all have admissible rows gives a dual certificate of value 0.
# usage: python3 -I world.py WORLD(e.g. 567) DEGS(e.g. 7 or 7,8) OUT.pkl
import sys, os, time, pickle, itertools, collections
sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT
T0 = time.time()
def log(*a): print(*a, '[%.0fs]' % (time.time() - T0), flush=True)

def bracelets(letters, d):
    out = []
    for w in itertools.product(letters, repeat=d):
        if W.NS['canon'](w) == w: out.append(w)
    return out

def receivers(world, d):
    ns = W.NS; U = min(d, 9); isR5, isR6, RBIG = ns['isR5'], ns['isR6'], ns['RBIG']; L = sorted(world)
    rows = []; stats = collections.Counter()
    for w in bracelets(L, d):
        if d in (7, 8) and ns['canon'](w) in RBIG: stats['RBIG'] += 1; continue
        # backtracking over s with R5 / R6 checks at link positions as soon as s_{i-1}, s_i are set
        s = [None] * d
        def ok_at(i):   # check link position i (needs s[i-1], s[i])
            a, b = s[i], s[(i - 1) % d]
            if a is None or b is None: return True
            if w[i] == 5: return not isR5((U, w[(i + 1) % d], a, b, w[(i - 1) % d]))
            if w[i] == 6: return not all(isR6((U, w[(i + 1) % d], a, p, b, w[(i - 1) % d])) for p in ns['LET'])
            return True
        def rec(k):
            if k == d:
                if not ok_at(0): return
                ss = tuple(s)
                if TT.canon_ws(w, ss) != (w, ss): return
                stats['cand'] += 1
                if W.patmatch_fast(d, w, ss): stats['PAT'] += 1; return
                rows.append(('R', d, w, ss)); return
            for x in L:
                s[k] = x
                if ok_at(k): rec(k + 1)
                else: stats['R56'] += 1
                s[k] = None
        rec(0)
    return rows, stats

def world_rows(world, degs):
    world = set(world); labs = []
    for d in degs:
        r, st = receivers(world, d); log('d=%d world %s: %d admissible receivers %s' % (d, ''.join(map(str, sorted(world))), len(r), dict(st))); labs += r
    import joint
    S = [l for l in joint.all_sender_labels() if set(l[1]) <= world]; log('senders with world words: %d' % len(S)); labs += S
    if 6 in world:
        C = []; seen = set()
        for L6 in itertools.product(sorted(world), repeat=6):
            if W.NS['canon'](L6) != L6 or W.NS['isR6'](L6): continue
            for sc in itertools.product((5, 7), repeat=6):
                lab = ('C', L6, sc); key = tuple(sorted(W.cons_coef(lab).items()))
                if key in seen or not key: continue
                seen.add(key); C.append(lab)
        log('cons2 rows: %d' % len(C)); labs += C
    return labs

if __name__ == '__main__':
    ARGV = list(sys.argv); W.init()
    world = tuple(int(c) for c in ARGV[1]); degs = [int(x) for x in ARGV[2].split(',')]; out = ARGV[3]
    labs = world_rows(world, degs)
    pickle.dump(labs, open(out, 'wb')); log('saved %d labels to %s' % (len(labs), out))
