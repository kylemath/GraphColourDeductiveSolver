"""B8b (exploratory): the complete K <= 1 sender key list with status and big-vertex position.
Same enumeration as nbhd.py (degrees 5..DMAX, canonical 2-ball keys, at most one vertex of degree >= 7), plus for
each key: position of the big vertex ('x' first ring, 'p' private second-ring, 's' shared second-ring), its degree,
and status class: R (W12 / S66 / J9-D / EXT-D / diamond-2.122), notD (tested, not D-reducible), U (untested).
Writes b8b/out/k1keys.tsv: key  ring  nbig  pos  bigdeg  status  detail"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import ball, h0
import importlib.util

DMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
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

# diamond_like copied from nbhd.py (identical logic)
def diamond_like(cfg):
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

def bigpos(key):
    for b in key:
        if b[0] >= 7: return 'x', b[0]
        for d in b[1]:
            if d >= 7: return 'p', d
        if b[2] >= 7: return 's', b[2]
    return '-', 0

seen = set(); out = []
def rec(prefix, nbig):
    if len(prefix) == 5:
        key = ball.canon_blocks(prefix)
        if key in seen: return
        seen.add(key); emit(key, nbig); return
    for nb in range(0, 1 - nbig + 1):
        for b in bybig[nb]: rec(prefix + [b], nbig + nb)

def emit(key, nbig):
    ks = ball.key_str(key); r = ball.ring_size(key)
    word = ''.join(map(str, ball.wheel_canon([b[0] for b in key])))
    pos, bd = bigpos(key)
    if word in h0.W12: st, det = 'R', 'W12'
    else:
        cfg = ball.build(key)
        if cfg is None: st, det = 'X', 'invalid'
        elif diamond_like(cfg): st, det = 'R', 'diamond'
        elif word == '66666' and nbig == 0: st, det = 'R', 'S66'
        else:
            nm = ball.key_to_66666_name(key)
            if nm in j9: st, det = ('R', 'J9-D') if j9[nm] else ('notD', 'J9-notD')
            elif ks in ext: st, det = ('R', 'EXT-D') if ext[ks] else ('notD', 'EXT-notD')
            else: st, det = 'U', 'untested'
    out.append((ks, r, nbig, pos, bd, st, det))

rec([], 0)
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
with open(os.path.join(HERE, 'out', 'k1keys.tsv'), 'w') as f:
    for t in out: f.write('\t'.join(map(str, t)) + '\n')
C = collections.Counter((t[2], t[3], t[4], t[5]) for t in out)
for k in sorted(C): print(k, C[k])
