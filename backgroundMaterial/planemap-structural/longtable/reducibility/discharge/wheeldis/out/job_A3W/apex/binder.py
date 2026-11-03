#!/usr/bin/env python3
"""Windows of the face binder row (d=7, w letters LK, s letters SV) built the way win45 builds them, plus windows that
also hold the face apex t (the one ring-3 neighbour of the face's s vertex) at a fixed degree. Runs kc on each and
prints ring, extendable classes, reached, D verdict, depth.  usage: python3 binder.py LK SV [kc path]"""
import sys, os, subprocess, collections
W = '/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge'
sys.path.insert(0, os.path.join(W, 'b8b')); sys.path.insert(0, W)
from rings import Layered
LK, SV = os.environ["LK"], os.environ["SV"]; D = len(LK); KC = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kc')

def adjacency(L):
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj

def build(tdeg=None):
    """2-ball of the row; if tdeg is given, ring 3 is added too with the face apex t at degree tdeg and the rest 9."""
    L = Layered(D); L.add_ring([int(c) for c in LK])
    Wr = L.rings[1]; Z = L.ring(); adj = adjacency(L)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    r2 = {('s', j): int(SV[j]) for j in range(D)}
    L.add_ring([r2.get(name[z], 9) for z in Z])
    deg = {('u',): D}; deg.update({('w', j): int(LK[j]) for j in range(D)}); deg.update({('s', j): int(SV[j]) for j in range(D)})
    adj = adjacency(L); inv = {v: x for x, v in name.items()}
    if tdeg is not None:
        # the face apex: the ring-3 neighbour of the 5,5,5 face's s vertex (the s_j with w_j = w_{j+1} = s_j = 5)
        j = next(j for j in range(D) if LK[j] == '5' and LK[(j + 1) % D] == '5' and SV[j] == '5')
        sj = inv[('s', j)]; Z3 = set(L.ring()); t = next(iter(adj[sj] & Z3))
        name[t] = ('t',); deg[('t',)] = tdeg
        L.add_ring([tdeg if z == t else 9 for z in L.ring()])
        adj = adjacency(L); inv = {v: x for x, v in name.items()}
    return L, adj, name, inv, deg

def extract(adj, I, deg):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    for x in I: assert len(adj[x]) == deg[x], (x, len(adj[x]), deg[x])
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return len(order), len(Il), f(ra), f(ia), Il, order

def line(S, tdeg=None):
    L, adj, name, inv, deg = build(tdeg)
    I = [inv[x] for x in S]; c = extract(adj, I, {inv[x]: deg[x] for x in S})
    if c is None: return None
    nm = 'b7_' + ('u' if ('u',) in S else '-') + ''.join(LK[j] if ('w', j) in S else '.' for j in range(D)) + '_' + ''.join(SV[j] if ('s', j) in S else '.' for j in range(D)) + ('_t%d' % tdeg if tdeg is not None else '')
    # ring contacts of each inside vertex, by name, for the report
    contacts = {name[x]: [name.get(y, ('r', y)) for y in sorted(adj[x]) if y not in set(I)] for x in I}
    return nm, '%s %d %d %s %s' % (nm, c[0], c[1], c[2], c[3]), contacts

def kc(lines, timeout=1800):
    p = subprocess.run([KC, '-j'], input='\n'.join(l for l in lines) + '\n', capture_output=True, text=True, timeout=timeout)
    return p.stdout.strip().splitlines()

if __name__ == '__main__':
    u, w, s = ('u',), lambda j: ('w', j), lambda j: ('s', j)
    base = {u, w(3), w(4), w(5), w(6), s(3), s(4)}
    cases = collections.OrderedDict([
        ('base (the open-case window on this row)', (base, None)),
        ('+ s5', (base | {s(5)}, None)), ('+ s6', (base | {s(6)}, None)), ('+ s5 + s6', (base | {s(5), s(6)}, None)),
        ('+ s5 + s6 + w0', (base | {s(5), s(6), w(0)}, None)), ('+ s5 + s6 + w0 + s0', (base | {s(5), s(6), w(0), s(0)}, None)),
        ('+ w2', (base | {w(2)}, None)), ('+ w2 + s2', (base | {w(2), s(2)}, None)), ('+ w2 + s2 + s5 + s6', (base | {w(2), s(2), s(5), s(6)}, None)),
        ('all u, w, s', ({u} | {w(j) for j in range(D)} | {s(j) for j in range(D)}, None)),
        ('base + apex 6', (base | {('t',)}, 6)), ('base + apex 7', (base | {('t',)}, 7)), ('base + apex 8', (base | {('t',)}, 8)),
        ('+ s5 + s6 + apex 6', (base | {s(5), s(6), ('t',)}, 6)), ('+ s5 + s6 + apex 7', (base | {s(5), s(6), ('t',)}, 7)),
        ('+ w2 + s2 + s5 + s6 + apex 6', (base | {w(2), s(2), s(5), s(6), ('t',)}, 6)),
    ])
    todo = []
    for title, (S, td) in cases.items():
        r = line(S, td)
        if r is None: print(f'{title:<40} no simple ring'); continue
        nm, ln, contacts = r; ring = int(ln.split()[1])
        far = contacts.get(('w', 6)); print(f'{title:<40} ring {ring:2d}  far-side 6 contacts: {far}', flush=True)
        todo.append((title, ln, ring))
    print('\nrunning kc (ring <= 15 now):', flush=True)
    for title, ln, ring in todo:
        if ring > 15: print(f'{title:<40} ring {ring}: skipped here (run in background)'); continue
        out = kc([ln]); print(f'{title:<40} {out[0].split(" ", 1)[1] if out else "no output"}', flush=True)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'binder_windows.txt'), 'w').write(''.join(ln + '\n' for _, ln, _ in todo))
