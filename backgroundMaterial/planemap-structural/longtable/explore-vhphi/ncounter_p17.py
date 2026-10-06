"""Independent reproduction at order <= 17 from plantri output (own enumeration, own lock test, own Case code).
usage: python3 ncounter_p17.py PLANTRI N   [exploratory]
For each min-degree-5 triangulation of order N, each degree-5 vertex x, each rotation/direction of the ring word
D a D b g: enumerate proper colourings of T-x with that ring, keep rigid ones (six forests, comps 1,2,2,1,1,1),
test the three fans (full Kempe class in G=T-xy), and for triply locked states classify c', c''."""
import sys, subprocess
from ncounter_lib import *

def parse_p(line):
    _, body = line.split()
    return [[ord(ch) - 97 for ch in r] for r in body.split(',')]

def states(adjl, x, ring_order):
    n = len(adjl); adj = [set(a) for a in adjl]
    out = []
    word = [D, A, D, B, G]
    for direction in (1, -1):
        ro = ring_order[::direction]
        for rot in range(5):
            ring = [ro[(rot + i) % 5] for i in range(5)]
            col = {ring[i]: word[i] for i in range(5)}
            order = []; seen = set(ring) | {x}
            q = list(ring)
            while q:
                v = q.pop(0)
                for w in adjl[v]:
                    if w not in seen: seen.add(w); order.append(w); q.append(w)
            assert len(order) + 6 == n
            def go(i):
                if i == len(order):
                    if is_rigid(adj, col, x): out.append((ring, dict(col)))
                    return
                v = order[i]
                bl = {col[w] for w in adj[v] if w in col}
                for a in range(4):
                    if a not in bl:
                        col[v] = a; go(i + 1); del col[v]
            # ring must itself be proper
            if all(col[ring[i]] != col[ring[(i + 1) % 5]] for i in range(5)):
                go(0)
    return out

def main():
    pl, N = sys.argv[1], sys.argv[2]
    lines = subprocess.run([pl, '-m5', '-a', N], capture_output=True, text=True).stdout.strip().split('\n')
    lines = [l for l in lines if l and l[0].isdigit()]
    tot = 0
    for gi, line in enumerate(lines):
        adjl = parse_p(line)
        for x in range(len(adjl)):
            if len(adjl[x]) != 5: continue
            # ring order from plantri's cyclic neighbour order
            ro = adjl[x]
            adj = [set(a) for a in adjl]
            # chords forbidden? (4-connected) -- skip graphs where ring has a chord u_i u_{i+2}
            if any(ro[(i + 2) % 5] in adj[ro[i]] for i in range(5)): continue
            S = states(adjl, x, ro)
            nr = len(S); nl = 0
            for ring, col in S:
                L = fan_locks(adj, col, x, ring, 20000)
                if any(r[0] is not False for r in L): continue
                nl += 1
                t = classify_both(adj, col, x, ring)
                K2 = comp_of(adj, col, ring[2], {D, G}, x); K0 = comp_of(adj, col, ring[0], {D, B}, x)
                s1 = kempe_class(adj, swapK(col, K2, D, G), x, ring[0], 20000)
                s2 = kempe_class(adj, swapK(col, K0, D, B), x, ring[2], 20000)
                print(f"graph {gi} x={x} ring={ring} sizes={[sum(1 for v in col if col[v]==k) for k in range(4)]} classes(fans)={[r[1] for r in L]} c'={t[0][0]} sep={s1[0]} cls={s1[1]} | c''={t[1][0]} sep={s2[0]} cls={s2[1]}")
                tot += 1
            if nr: print(f"  graph {gi} x={x}: rigid states (all rotations/directions) {nr}, triply locked {nl}")
    print('N', N, 'triply locked rigid states (labelled by ring rotation/direction):', tot)
if __name__ == "__main__":
    main()
