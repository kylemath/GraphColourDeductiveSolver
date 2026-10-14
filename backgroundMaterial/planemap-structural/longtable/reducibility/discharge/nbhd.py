"""B8 (exploratory, resumed session 14 Oct): the finite SENDER list for a census-independent discharging check.

In the LP models every rule is "a degree-5 vertex v sends sigma[f] to a vertex u of degree >= 7 within distance 2"
(simple/face) or 3 (d3).  For simple/face the amount v sends is a function of v's 2-ball key alone, so the sender
half of the validity check is a check over 2-ball keys, not over graphs:
    for every 2-ball key K that is NOT in R:  sum of sigma over the big (>= 7) vertices of K  >= 1.
A 2-ball with no big vertex is always in R (its first-ring word is a W12 wheel, or it is 66666 with second ring
<= 6 = S66), so only keys with >= 1 big vertex matter, and keys with many big vertices send >= 1 under any
reasonable sigma.  This script enumerates every canonical 2-ball key with all degrees in 5..DMAX and at most K big
vertices (first + second ring), drops keys containing a Birkhoff diamond or 2.122 among interior vertices
(reducible anyway), and classifies each key: W12 / S66 / J9 / tested D-reducible (out/dres-*) / tested not /
untested, by ring and number of big vertices.
Usage: nbhd.py DMAX K [--list FILE]   (FILE: untested keys with K big vertices, 'ring key nbig')"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ball, h0

DMAX, K = int(sys.argv[1]), int(sys.argv[2])
LIST = sys.argv[sys.argv.index('--list') + 1] if '--list' in sys.argv else None
ext = h0.load_ext(); j9 = h0.load_j9()
degs = range(5, DMAX + 1)

blocks = []
for dx in degs:
    for privs in itertools.product(degs, repeat=dx - 5):
        for ds in degs:
            b = (dx, tuple(privs), ds)
            blocks.append((b, sum(1 for d in (dx,) + tuple(privs) + (ds,) if d >= 7)))
bybig = collections.defaultdict(list)
for b, nb in blocks: bybig[nb].append(b)


def diamond_like(cfg):
    """diamond or 2.122 among interior vertices (all four degrees known)."""
    r, m, D, ia, ra = cfg
    A = [set(x) for x in ia]
    for a in range(m):
        for b in A[a]:
            if b < a: continue
            com = [c for c in A[a] & A[b]]
            if len(com) != 2: continue
            c, d = com
            if D[c] == 5 and D[d] == 5 and d not in A[c]:
                if (D[a], D[b]) == (5, 5) or {D[a], D[b]} == {5, 6}: return True
    return False


seen = set(); C = collections.Counter(); rings = collections.defaultdict(collections.Counter); untested = []
# ordered 5-tuples of blocks with total big count <= K (big counted per block: dx, privs, ds; ds_k is s_k only once)
def rec(prefix, nbig):
    if len(prefix) == 5:
        key = ball.canon_blocks(prefix)
        if key in seen: return
        seen.add(key); emit(key, nbig); return
    for nb in range(0, K - nbig + 1):
        for b in bybig[nb]: rec(prefix + [b], nbig + nb)


def emit(key, nbig):
    ks = ball.key_str(key); r = ball.ring_size(key)
    word = ''.join(map(str, ball.wheel_canon([b[0] for b in key])))
    if word in h0.W12: st = 'W12'
    else:
        cfg = ball.build(key)
        if cfg is None: st = 'invalid'
        elif diamond_like(cfg): st = 'diamond/2.122'
        elif word == '66666' and nbig == 0: st = 'S66'
        else:
            nm = ball.key_to_66666_name(key)
            if nm in j9: st = 'J9-D' if j9[nm] else 'J9-notD'
            elif ks in ext: st = 'EXT-D' if ext[ks] else 'EXT-notD'
            else: st = 'untested'; untested.append((r, ks, nbig))
    C[(nbig, st)] += 1; rings[(nbig, st)][r] += 1


rec([], 0)
print('DMAX', DMAX, 'K', K, 'canonical keys', len(seen))
for nb in range(K + 1):
    print('-- big vertices = %d' % nb)
    for (n, st), c in sorted(C.items()):
        if n == nb: print('   %-14s %7d   rings %s' % (st, c, dict(sorted(rings[(n, st)].items()))))
if LIST:
    with open(LIST, 'w') as f:
        for r, ks, nb in sorted(untested): f.write('%d %s %d\n' % (r, ks, nb))
