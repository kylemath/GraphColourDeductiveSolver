#!/usr/bin/env python3
"""[exploratory] NightSixEvent: component counts (f,g,h)=(C(alpha mu),C(alpha B),C(alpha A)) and
(C(AB),C(mu A),C(mu B)) at every state of every Gamma-cycle and of every DL run through a Hole6 window,
for the 34 hole-orientations of jobak-66dump (+ p25#668) and gentri (open control). One core."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../27-studio-positive-config/jobuv'))
sys.path.insert(0, os.path.join(HERE, '../32-nightsigmaimage'))
import uv_lib
NM = {(3, 4): 0, (1, 1): 1, (3, 3): 2, (1, 0): 3, (3, 2): 4, (1, 4): 5, (3, 1): 6, (1, 3): 7, (3, 0): 8, (1, 2): 9}
def run(rot, h, tag, fo):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False); sp = H.sp
    q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    EDG = [(sp.idx[u], sp.idx[v]) for u in range(len(rot)) for v in rot[u] if u < v and h not in (u, v)]
    def info(k):
        s = sp.states[k]; d = {'k': k, 'DL': H.DL[k]}
        lk = H.locks(k)
        if lk is None: d['pos'] = None; return d
        j, ty, hi, (al, mu, A, B) = H.frame(k)
        d['pos'] = NM.get((ty, (q - j) % 5)); d['locks'] = lk
        C = lambda a, b: len(sp.components(s, a, b))
        d['c'] = [C(al, mu), C(al, B), C(al, A), C(A, B), C(mu, A), C(mu, B)]
        d['fix'] = H.sigma(k) == k
        E = lambda a, b: sum(1 for (u, v) in EDG if {s[u], s[v]} == {a, b})
        d['E'] = [E(al, mu), E(al, B), E(al, A)]
        return d
    done = set()
    for ci, z in enumerate(H.cycles):
        if all(H.DL[x] for x in z):
            fo.write(json.dumps({'tag': tag, 'hole': h, 'kind': 'gamma', 'L': len(z), 'seq': [info(x) for x in z]}) + '\n')
            done |= set(z)
    # open DL runs containing an R3k2 state (pos 4); record maximal run plus one state either side
    for t in range(H.S):
        if t in done or not H.DL[t] or H.DL[H.pinv[t]]: continue
        seq = [H.pinv[t]]; x = t
        while H.DL[x] and len(seq) < 400: seq.append(x); x = H.pi[x]
        seq.append(x)
        I = [info(y) for y in seq]
        if any(d['pos'] == 4 for d in I[1:-1]):
            fo.write(json.dumps({'tag': tag, 'hole': h, 'kind': 'open', 'seq': I}) + '\n')
if __name__ == '__main__':
    fo = open(sys.argv[2], 'w')
    if sys.argv[1] == 'dump':
        d = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen = set()
        for r in d:
            key = (r['run'], r['name'], r['hole'])
            if key in seen: continue
            seen.add(key); run(r['rotation'], r['hole'], '%s:%s' % key[:2], fo); print(key, flush=True)
        ce = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-counterexample.json')))
        run(ce['rotation_system'], ce['hole'], 'ce:' + ce['graph'], fo)
    else:
        sys.path.insert(0, os.path.join(HERE, '../33-nightw2euler'))
        from w2e import holes6
        from kempe_py import gentri_rotation
        G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
        for n in [int(x) for x in sys.argv[1].split(',')]:
            for gi, l in enumerate(open(G % n)):
                if not l.startswith('G'): continue
                rot0 = gentri_rotation(l)
                for mir in (0, 1):
                    rot = [list(reversed(x)) for x in rot0] if mir else rot0
                    for h in holes6(rot): run(rot, h, 'g%d#%d%s' % (n, gi, 'm' if mir else ''), fo)
            print(n, flush=True)
