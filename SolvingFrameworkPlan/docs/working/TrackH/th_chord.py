#!/usr/bin/env python3
"""Track H: exhaustive check of 'rigid DL state => pi(state) is not rigid' in the planar chord model (sphere).

Model (dual Tait picture of a state whose {2,3}-subgraph is one cycle H through the hole vertex v, i.e. whose
{alpha,mu} and {A,B} graphs are trees): H = v, u_1, ..., u_N, v (N odd), H-edges coloured 2,3,2,...,3
(v-u_1 = e2 colour 2, u_N-v = e4 colour 3); colour-1 edges are chords: a non-crossing perfect matching inside H on the
cyclic sequence (u_1..u_N, e3) and one outside H on (u_1..u_N, e0, e1) (rotation e0,e1,e2,e3,e4 at v), every u_i in
exactly one chord.  Unfilled link pattern (1,1,2,1,3).  DL (sphere) <=> {1,2}-pairing at v is (e0,e3)(e1,e2) and
{1,3}-pairing is (e1,e3)(e0,e4).  Rigid <=> the {1,2}- and {1,3}-subgraphs are connected (all six pair graphs forests
with minimum component counts).  pi = swap colours 1<->3 along the {1,3}-trail of v through e1, e3.
For every rigid DL instance with N <= NMAX: is pi(state) rigid?  (Rigid is colour-symmetric: all three bicoloured
subgraphs connected.)  Every rigid DL sphere state is an instance (with a simple dual); instances may be multigraphs.
usage: th_chord.py NMAX"""
import sys
sys.setrecursionlimit(10000)

def ncm(points):
    """all non-crossing perfect matchings of a list of points in cyclic order"""
    if not points: yield []; return
    a = points[0]
    for k in range(1, len(points), 2):
        b = points[k]
        for m1 in ncm(points[1:k]):
            for m2 in ncm(points[k + 1:]):
                yield [(a, b)] + m1 + m2

def components(nv, edges):
    par = list(range(nv))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in edges: par[f(a)] = f(b)
    return len({f(x) for x in range(nv) if any(x in e for e in edges)})

def run(N):
    U = list(range(1, N + 1)); V0 = 0
    # half-edge labels at v: 'e0','e1','e2','e3','e4'
    Hedges = []  # (x, y, colour, label)
    Hedges.append((V0, 1, 2, 'e2'))
    for i in range(1, N): Hedges.append((i, i + 1, 3 if i % 2 == 1 else 2, None))
    Hedges.append((N, V0, 3, 'e4'))
    stats = dict(inst=0, dl=0, rigid=0, img_rigid=0, img_dl=0, img_rigidDL=0)
    examples = []
    for mask in range(1 << N):
        I = [u for u in U if mask >> (u - 1) & 1]; O = [u for u in U if not mask >> (u - 1) & 1]
        if (len(I) + 1) % 2 or (len(O) + 2) % 2: continue
        for mi in ncm(I + ['e3']):
            for mo in ncm(O + ['e0', 'e1']):
                chords = mi + mo
                if any(isinstance(a, str) and isinstance(b, str) for a, b in chords): continue  # loop at v
                stats['inst'] += 1
                # build edge list with colours; v's half-edges distinguished
                E = [(a, b, c, l) for (a, b, c, l) in Hedges]
                for a, b in chords:
                    if isinstance(a, str): a, b = b, a
                    if isinstance(b, str): E.append((a, V0, 1, b))
                    else: E.append((a, b, 1, None))
                res = analyse(N, E)
                if res is None: continue
                dl, rigid, img = res
                stats['dl'] += dl
                if dl and rigid:
                    stats['rigid'] += 1
                    stats['img_rigid'] += img[0]; stats['img_dl'] += img[1]; stats['img_rigidDL'] += img[0] and img[1]
                    if img[0] and img[1] and len(examples) < 5: examples.append(chords)
    return stats, examples

def trails(E, cols):
    """bicoloured subgraph on colours cols: return (#components, pairing at v as frozenset of label pairs)."""
    sub = [(i, e) for i, e in enumerate(E) if e[2] in cols]
    adj = {}
    for i, (a, b, c, l) in sub:
        adj.setdefault(a, []).append(i); adj.setdefault(b, []).append(i)
    comp = components(max(max(e[0], e[1]) for e in E) + 1, [(e[0], e[1]) for _, e in sub])
    # pairing at v: walk from each v-half-edge
    pair = set(); used = set()
    vh = [i for i, e in sub if e[3] is not None]
    for i0 in vh:
        if i0 in used: continue
        used.add(i0); i = i0; x = E[i0][0] if E[i0][1] == 0 else E[i0][1]
        steps = 0
        while True:
            nxt = [k for k in adj[x] if k != i]
            if x == 0: break
            i = nxt[0]; e = E[i]
            if e[3] is not None and (e[0] == 0 or e[1] == 0) and x != 0:
                used.add(i); pair.add(frozenset((E[i0][3], e[3]))); break
            x = e[0] if e[1] == x else e[1]; steps += 1
            if steps > 10 * len(E): return None
    return comp, frozenset(pair)

def analyse(N, E):
    t12 = trails(E, (1, 2)); t13 = trails(E, (1, 3)); t23 = trails(E, (2, 3))
    if None in (t12, t13, t23): return None
    dl = t12[1] == frozenset({frozenset(('e0', 'e3')), frozenset(('e1', 'e2'))}) and \
         t13[1] == frozenset({frozenset(('e1', 'e3')), frozenset(('e0', 'e4'))})
    rigid = t12[0] == 1 and t13[0] == 1 and t23[0] == 1
    if not (dl and rigid): return dl, rigid, None
    # pi: swap 1<->3 along the {1,3}-trail through e1 (it returns via e3 by DL)
    sub = [i for i, e in enumerate(E) if e[2] in (1, 3)]
    adj = {}
    for i in sub:
        a, b = E[i][0], E[i][1]; adj.setdefault(a, []).append(i); adj.setdefault(b, []).append(i)
    i0 = next(i for i in sub if E[i][3] == 'e1'); trail = {i0}; i = i0; x = E[i0][0] if E[i0][1] == 0 else E[i0][1]
    while x != 0:
        i = next(k for k in adj[x] if k != i); trail.add(i)
        x = E[i][0] if E[i][1] == x else E[i][1]
    E2 = [(a, b, ({1: 3, 3: 1}[c] if k in trail else c), l) for k, (a, b, c, l) in enumerate(E)]
    s12 = trails(E2, (1, 2)); s13 = trails(E2, (1, 3)); s23 = trails(E2, (2, 3))
    img_rigid = s12[0] == 1 and s13[0] == 1 and s23[0] == 1
    # new link colours: e0..e4 -> majority colour is 3; image DL iff pairings in the new frame (j' = j+3) match
    lab = {E2[k][3]: E2[k][2] for k in range(len(E2)) if E2[k][3]}
    assert [lab[x] for x in ('e0', 'e1', 'e2', 'e3', 'e4')] == [1, 3, 2, 3, 3], lab
    # new frame: e'_t = e_{t+3}: (e3,e4,e0,e1,e2) colours (3,3,1,3,2); new roles 1'=3, 2'=1, 3'=2
    ren = {'e3': 'e0', 'e4': 'e1', 'e0': 'e2', 'e1': 'e3', 'e2': 'e4'}
    p12 = frozenset(frozenset(ren[x] for x in pr) for pr in s13[1])   # {1',2'} = {3,1}
    p13 = frozenset(frozenset(ren[x] for x in pr) for pr in s23[1])   # {1',3'} = {3,2}
    img_dl = p12 == frozenset({frozenset(('e0', 'e3')), frozenset(('e1', 'e2'))}) and \
             p13 == frozenset({frozenset(('e1', 'e3')), frozenset(('e0', 'e4'))})
    return dl, rigid, (img_rigid, img_dl)

if __name__ == '__main__':
    for N in range(1, int(sys.argv[1]) + 1, 2):
        st, ex = run(N)
        print('N', N, st, ('EXAMPLE ' + str(ex[0])) if ex else '', flush=True)
