#!/usr/bin/env python3
"""routeb/onestar.py -- [exploratory] one-star partial 2-balls (MathRstarUnavoidable.md sec.7.1): pattern of 5 cyclic link entries,
exactly one '*' (free link vertex p, on the ring; its other neighbours are outside, adversarial). K = faces incident to v or to a
specified link vertex. Ring = p, outer neighbours of the specified link vertices, back to p; length = (sum of specified) - 14.
Game: kred.py (joint, full adversary), unchanged."""
import sys, json, time
import kred

def onestar_faces(pat):
    k = pat.index('*'); pat = pat[k:] + pat[:k]                 # rotate so that x0 = p
    v = 0; X = [1, 2, 3, 4, 5]; nxt = [6]
    def new():
        nxt[0] += 1; return nxt[0] - 1
    W = [new() for _ in range(5)]
    faces = []
    for i in range(5):
        faces.append((v, X[i], X[(i + 1) % 5]))
        faces.append((X[(i + 1) % 5], X[i], W[i]))
    for i in range(1, 5):                                       # fans of the specified x1..x4 only
        kk = pat[i] - 5; assert kk >= 0
        seq = [W[(i - 1) % 5]] + [new() for _ in range(kk)] + [W[i]]
        for a, b in zip(seq, seq[1:]): faces.append((X[i], a, b))
    return faces, v

def parse(s): return [x if x == '*' else int(x) for x in s.strip('()').split(',')]

def run(s, mode='joint', mx=5000000):
    pat = parse(s); f, v = onestar_faces(pat); t = time.time()
    cfg = kred.Config(f, v)
    try:
        r = kred.Game(cfg, mode, max_nodes=mx).solve(); r.pop('startval')
    except OverflowError as e: r = {'capped': str(e)}
    return {'pattern': s, 'ring': cfg.m, 'expected_ring': sum(x for x in pat if x != '*') - 14, 'mode': mode, **r, 'secs': round(time.time() - t, 1)}

if __name__ == '__main__':
    for s in sys.argv[1].split(';'):
        print(json.dumps(run(s, sys.argv[2] if len(sys.argv) > 2 else 'joint', int(sys.argv[3]) if len(sys.argv) > 3 else 5000000)), flush=True)
