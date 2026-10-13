"""Do the off-sphere R0 violations survive when every state must LIFT to a primal 4-colouring?
(Long Table, r0surfaces.)

A state of an R0 sequence is an arc (M, M') of D; it is a near-Tait colouring (M -> colour 1, M' -> 2, rest -> 3
in Z2 x Z2; at v the colours sum to 1+2+3+3+3 = 0, so it is locally consistent everywhere).  In an embedding it
lifts to a face colouring (= a 4-colouring of the primal T - x) iff assigning col(F') = col(F) xor col(e) across
every edge is consistent (trivial holonomy).  On the sphere every state lifts.  For each R0 violator and each of
its RP2 / torus embeddings with the rotation at v (listed by `genus -sepP/-sepT -list`, first 400 each) we ask:
is there a closed R0 walk through the Hamiltonian arc M_0 -> M_1 using only liftable arcs?
usage: lift_test.py n [maxgraphs] [--lines FILE] [--surf RP2|T2|KB] [--nolift] [--sphere-control]"""
import sys, json, subprocess, itertools
from collections import Counter
sys.path.insert(0, '..')
from ax_lib import G5, parse_line

n = int(sys.argv[1]); maxg = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 10 ** 9
lines = ([x.strip() for x in open(sys.argv[sys.argv.index('--lines') + 1]) if x.strip()] if '--lines' in sys.argv
         else [json.loads(l)['line'] for l in open(f'out/r0enum_n{n}.jsonl')])[:maxg]
SURF = sys.argv[sys.argv.index('--surf') + 1] if '--surf' in sys.argv else 'both'
inp = ''.join(l + '\n' for l in lines)
outP = (subprocess.run(['./genus', '-sepP', '-list'], input=inp, capture_output=True, text=True).stdout.splitlines()
        if SURF in ('both', 'RP2') else ['| 0'] * len(lines))
outT = (subprocess.run(['./genus', '-sepT', '-list'], input=inp, capture_output=True, text=True).stdout.splitlines()
        if SURF in ('both', 'T2') else ['| 0'] * len(lines))
outK = (subprocess.run(['./genus', '-sepK', '-list'], input=inp, capture_output=True, text=True).stdout.splitlines()
        if SURF == 'KB' else ['| 0'] * len(lines))
if '--sphere-control' in sys.argv:
    # control: star-relabelled violators that are planar; every arc must lift on a sphere embedding
    star = []
    for l in lines:
        t = l.split(); fv = t[-5:]; star.append(' '.join(t[:-5] + [fv[0], fv[2], fv[4], fv[1], fv[3]]))
    outS = subprocess.run(['./genus', '-sepS', '-list'], input=''.join(s + '\n' for s in star), capture_output=True, text=True).stdout.splitlines()
    lines = star


def faces_of(nv, E, rot, tw):
    other = lambda e, x: E[e][1] if E[e][0] == x else E[e][0]
    pos = {u: {e: i for i, e in enumerate(rot[u])} for u in range(nv)}
    seen = set(); walks = []
    for u in range(nv):
        for e in rot[u]:
            for sg in (1, -1):
                if (u, e, sg) in seen: continue
                W = []; x, f, s = u, e, sg
                while (x, f, s) not in seen:
                    seen.add((x, f, s)); W.append((x, f))
                    y = other(f, x); s2 = s * (-1 if tw[f] else 1)
                    r = rot[y]; f = r[(pos[y][f] + s2) % len(r)]; x = y; s = s2
                walks.append(W)
    faces = []; used = set()
    for w in walks:
        key = frozenset(w); rev = frozenset((other(f, x), f) for x, f in w)
        if rev in used: continue
        used.add(key); faces.append(w)
    return faces


res = Counter(); examples = {}
for gi, line in enumerate(lines):
    nv, E, fv = parse_line(line); g = G5(nv, E, fv); m = len(E); v = g.v
    P = [frozenset(p) for p in g.pms()]; idx = {p: i for i, p in enumerate(P)}
    k = [g.kidx(p) for p in P]
    arcs = [(i, j) for i in range(len(P)) for j in range(len(P)) if not (P[i] & P[j]) and k[j] == (k[i] - 2) % 5]
    out_arcs = [[] for _ in P]
    for i, j in arcs: out_arcs[i].append(j)
    M0 = frozenset(e for e in range(nv) if e % 2 == 0); M1 = frozenset(e for e in range(nv) if e % 2 == 1)
    i0, i1 = idx[M0], idx[M1]
    inc = [[e for e in range(m) if u in E[e]] for u in range(nv)]
    pairs = (('S2', outS[gi]),) if '--sphere-control' in sys.argv else (('RP2', outP[gi]), ('T2', outT[gi]), ('KB', outK[gi]))
    for surf, out in pairs:
        codes = out.split('|')[0].split()
        if not codes: continue
        best = None
        for code in codes:
            if surf in ('RP2', 'KB'):
                tw = [(int(code, 16) >> e) & 1 for e in range(m)]
                rot = {u: list(inc[u]) for u in range(nv)}
            else:
                b = int(code, 16); tw = [0] * m
                rot = {u: (list(inc[u]) if not (b >> u) & 1 else [inc[u][0], inc[u][2], inc[u][1]]) for u in range(nv)}
            rot[v] = list(fv)
            faces = faces_of(nv, E, rot, tw)
            assert nv - m + len(faces) == {'RP2': 1, 'T2': 0, 'S2': 2, 'KB': 0}[surf]
            if surf == 'S2':
                pass
            side = [[] for _ in range(m)]
            for fi, w in enumerate(faces):
                for x, f in w: side[f].append(fi)
            def lifts(i, j):
                if '--nolift' in sys.argv: return True   # positive control of the detector
                col = [3] * m
                for e in P[i]: col[e] = 1
                for e in P[j]: col[e] = 2
                fc = [None] * len(faces); fc[0] = 0; st = [0]
                adj = [[] for _ in faces]
                for e in range(m):
                    a, b2 = side[e]; adj[a].append((b2, col[e])); adj[b2].append((a, col[e]))
                while st:
                    a = st.pop()
                    for b2, c in adj[a]:
                        if fc[b2] is None: fc[b2] = fc[a] ^ c; st.append(b2)
                        elif fc[b2] != fc[a] ^ c: return False
                return True
            if surf == 'S2':
                good = [(i, j) for (i, j) in arcs if lifts(i, j)]
                res[('S2-all-arcs-lift', len(good) == len(arcs))] += 1; best = 'control'; break
            # lazy: Hamiltonian arc first, then BFS from M_1 testing only arcs leaving reached matchings
            ham_ok = lifts(i0, i1)
            seen = {i1}
            if ham_ok:
                st = [i1]
                while st and i0 not in seen:
                    a = st.pop()
                    for b2 in out_arcs[a]:
                        if b2 not in seen and lifts(a, b2): seen.add(b2); st.append(b2)
            viol = ham_ok and i0 in seen
            # also: the same for plain arcs (sanity: must be True)
            r = ('lift-closed' if viol else ('ham-arc-not-liftable' if not ham_ok else 'no-lift-cycle'))
            rank = {'ham-arc-not-liftable': 0, 'no-lift-cycle': 1, 'lift-closed': 2}
            if best is None or rank[r] > rank[best]: best = r   # best over all embeddings
            if viol:
                examples.setdefault(surf, (line, code)); break
        res[(surf, best)] += 1
print(json.dumps(dict(n=n, graphs=len(lines), result={f'{a}:{b}': c for (a, b), c in sorted(res.items())},
                      examples=examples)), flush=True)
