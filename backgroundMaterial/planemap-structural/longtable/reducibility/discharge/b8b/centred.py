"""B8b (exploratory): size of the receiver-centred family.  For a centre u of degree d, count the u-centred 2-balls
(link and second-ring degrees 5/6, the block model of maxsend.py) with more than d - 6 relaxed K = 1 lone-u
senders, up to rotation and reflection, by ring size (ring = third ring of u in the free completion
= sum over second-ring y of (deg y - in y - 3)).  These are the u-centred configurations that R would have to
contain (or a rule of another shape would have to handle) for the K <= 1 receiver rows to close."""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from maxsend import BLOCKS, count


def ring(S):
    r = 0
    for dw, p, s in S:
        if p is not None: r += p - 1 - 3
        r += s - 2 - 3
    return r


def canon(seq):
    n = len(seq); best = None
    rev = [None] * n
    for k in range(n):                      # reflection: block order reversed, privates fine, s shifts
        rev[k] = (seq[(-k) % n][0], seq[(-k) % n][1], seq[(-k - 1) % n][2])
    for S in (list(seq), rev):
        for k in range(n):
            t = tuple(S[k:] + S[:k]); best = t if best is None or t < best else best
    return best


if __name__ == '__main__':
    for d in map(int, sys.argv[1:]):
        seen = set(); C = collections.Counter(); R = collections.defaultdict(collections.Counter)
        for seq in itertools.product(range(6), repeat=d):
            S = [BLOCKS[b] for b in seq]; c = canon(S)
            if c in seen: continue
            seen.add(c); k, who = count(list(c), d)
            C[k] += 1
            if k > d - 6: R[k][ring(c)] += 1
        tot = sum(v for k, v in C.items() if k > d - 6)
        print('d=%d canonical 2-balls %d; by sender count %s; with > d-6 senders: %d' % (d, len(seen), dict(sorted(C.items())), tot))
        allr = collections.Counter()
        for k in R: allr.update(R[k])
        print('    rings of those:', dict(sorted(allr.items())))

    # case (b) refinement for d = 8: the only non-R K = 1 keys with a lone 8 are 66666 holes with the 8 at a PRIVATE
    # position (165 J9-notD), so count only p-senders.
    if os.environ.get('PONLY'):
        for d in map(int, os.environ['PONLY'].split(',')):
            seen = set(); C = collections.Counter(); allr = collections.Counter()
            for seq in itertools.product(range(6), repeat=d):
                S = [BLOCKS[b] for b in seq]; c = canon(S)
                if c in seen: continue
                seen.add(c); k, who = count(list(c), d); kp = sum(1 for w in who if w[0] == 'p')
                C[kp] += 1
                if kp > d - 6: allr[ring(c)] += 1
            print('PONLY d=%d by p-sender count %s; with > d-6: %d; rings %s' % (d, dict(sorted(C.items())),
                  sum(allr.values()), dict(sorted(allr.items()))))
