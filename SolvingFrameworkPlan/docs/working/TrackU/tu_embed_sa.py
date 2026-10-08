#!/usr/bin/env python3
"""Track U: simulated annealing for a polyhedral (simplicial-dual) embedding of a G5 graph, orientable
(rotations only) or non-orientable (rotations + edge signatures).  v's rotation fixed to f0..f4.
usage: tu_embed_sa.py GRAPHLINES idx iters restarts [nonor]"""
import sys, random, math


def faces_gen(n, E, rot, sig):
    """general face tracing with edge signatures (sig[e] = 1 twisted). state (x, e, dir)"""
    pos = [{e: i for i, e in enumerate(r)} for r in rot]
    seen = set(); F = []
    for x in range(n):
        for e in rot[x]:
            for s0 in (1, -1):
                if (x, e, s0) in seen: continue
                face = []; st = (x, e, s0)
                while st not in seen:
                    seen.add(st); face.append(st)
                    xx, ee, s = st
                    a, b = E[ee]; y = b if a == xx else a
                    if sig[ee]: s = -s
                    r = rot[y]; ne = r[(pos[y][ee] + s) % len(r)]
                    # the reverse traversal of this corner is (y, ne, -s) arriving ... mark it to avoid double counting
                    seen.add((y, ee, -s))
                    st = (y, ne, s)
                F.append(face)
    return F


def defects(n, E, rot, sig):
    F = faces_gen(n, E, rot, sig)
    side = {}; bad = 0
    for fi, f in enumerate(F):
        vs = [d[0] for d in f]
        if len(vs) < 3: bad += 3
        bad += len(vs) - len(set(vs))
        for d in f: side.setdefault(d[1], []).append(fi)
    pairs = {}
    for e, s in side.items():
        if len(s) != 2: bad += 5; continue
        if s[0] == s[1]: bad += 1
        else:
            k = tuple(sorted(s)); pairs[k] = pairs.get(k, 0) + 1
    bad += sum(c - 1 for c in pairs.values())
    return bad, F, side


def main():
    lines = [l for l in open(sys.argv[1]) if l.strip()]
    idx, iters, rest = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    nonor = len(sys.argv) > 5
    p = list(map(int, lines[idx].split()))
    n, m = p[0], p[1]; E = [(p[2 + 2 * i], p[3 + 2 * i]) for i in range(m)]; fv = p[2 + 2 * m: 7 + 2 * m]
    inc = [[] for _ in range(n)]
    for k, (a, b) in enumerate(E): inc[a].append(k); inc[b].append(k)
    rnd = random.Random(7); gbest = 10 ** 9
    for r in range(rest):
        rot = [list(fv)] + [rnd.sample(inc[x], 3) for x in range(1, n)]
        sig = [0] * m
        bad, F, side = defects(n, E, rot, sig); T = 2.0
        for it in range(iters):
            if bad == 0: break
            if nonor and rnd.random() < 0.4:
                e = rnd.randrange(m); sig[e] ^= 1; undo = ('s', e)
            else:
                x = rnd.randrange(1, n); rot[x] = rot[x][::-1]; undo = ('r', x)
            b2, F2, s2 = defects(n, E, rot, sig)
            if b2 <= bad or rnd.random() < math.exp((bad - b2) / T):
                bad, F, side = b2, F2, s2
            else:
                if undo[0] == 's': sig[undo[1]] ^= 1
                else: rot[undo[1]] = rot[undo[1]][::-1]
            T = max(0.15, T * 0.9995)
        gbest = min(gbest, bad)
        print('restart', r, 'defects', bad, 'faces', len(F), file=sys.stderr, flush=True)
        if bad == 0:
            chi = n - m + len(F)
            print(dict(chi=chi, nonor=nonor, rot=rot, sig=sig))
            return
    print('best', gbest)


if __name__ == '__main__':
    main()
