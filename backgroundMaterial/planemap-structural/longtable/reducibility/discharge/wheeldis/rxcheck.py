"""Task B (exploratory): independent check of the `Rx` link reader of b8b/k2size_v3.py.
For every canonical K<=2 key (DMAX=8) and every first-ring x_k of degree 5/6, compare
  (a) k2size_v3's link word  [5, x_{k-1}, s_{k-1}, privs, s_k, x_{k+1}]
  (b) the word read off ball.build(key): neighbours of interior vertex 1+k, ordered as the induced cycle they form,
      degrees from the built degree list.
Also checks: x_k's neighbours are all interior (inside the 2-ball), their count is deg x_k, they induce a simple
cycle (no chord), and counts how many keys are Rx-hits under each reader.  Writes out/rxcheck.txt."""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); DIS = os.path.dirname(HERE); sys.path.insert(0, DIS)
import ball
DMAX, KMAX = 8, 2
canon = lambda w: ''.join(map(str, ball.wheel_canon([int(c) for c in w])))
C5x = {canon(w) for w in ('55558','55568','55577','55578','55588','55658','56568','56577','56578','56588','56658','66666')}
C6 = {canon(w) for w in ('555577','555677','555767','555777','556577','566577')}
degs = range(5, DMAX + 1)
blocks = []
for dx in degs:
    for privs in itertools.product(degs, repeat=dx - 5):
        for ds in degs:
            b = (dx, tuple(privs), ds); blocks.append((b, sum(1 for d in (dx,) + privs + (ds,) if d >= 7)))
bybig = collections.defaultdict(list)
for b, nb in blocks: bybig[nb].append(b)

def word_a(key, k):
    return [5, key[k-1][0], key[k-1][2]] + list(key[k][1]) + [key[k][2], key[(k+1) % 5][0]]

def word_b(cfg, k):
    r, m, D, ia, ra = cfg; x = 1 + k; N = ia[x]
    if ra[x]: return None, 'x has ring neighbours'
    if len(N) != D[x]: return None, 'degree mismatch'
    Ns = set(N)
    for y in N:
        if len(set(ia[y]) & Ns) != 2: return None, 'link not an induced cycle'
    order = [N[0]]; prev = None
    while True:
        cur = order[-1]; nb = sorted(set(ia[cur]) & Ns); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == order[0]: break
        order.append(nxt); prev = cur
    if len(order) != len(N): return None, 'link has several cycles'
    return [D[y] for y in order], 'ok'

seen = set(); stats = collections.Counter(); bad = []
def rec(prefix, nbig):
    if len(prefix) == 5:
        key = ball.canon_blocks(prefix)
        if key in seen: return
        seen.add(key); check(key); return
    for nb in range(0, KMAX - nbig + 1):
        for b in bybig[nb]: rec(prefix + [b], nbig + nb)

def check(key):
    stats['keys'] += 1
    cfg = ball.build(key)
    if cfg is None: stats['build None'] += 1; return
    hitA = hitB = False
    for k in range(5):
        dx = key[k][0]
        if dx not in (5, 6): continue
        wa = canon(word_a(key, k)); wb, why = word_b(cfg, k)
        if wb is None: bad.append((ball.key_str(key), k, why)); continue
        wb = canon(wb); stats['links checked'] += 1
        if wa != wb: bad.append((ball.key_str(key), k, 'word %s vs %s' % (wa, wb)))
        S = C5x if dx == 5 else C6
        hitA |= wa in S; hitB |= wb in S
    stats['hitA'] += hitA; stats['hitB'] += hitB

rec([], 0)
lines = ['# rxcheck: K<=%d DMAX=%d' % (KMAX, DMAX), str(dict(stats)), 'mismatches/failures: %d' % len(bad)]
lines += ['  %s k=%d %s' % b for b in bad[:50]]
os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
open(os.path.join(HERE, 'out', 'rxcheck.txt'), 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
