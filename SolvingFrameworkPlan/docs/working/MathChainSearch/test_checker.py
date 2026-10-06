#!/usr/bin/env python3
"""Regression + mutation tests for checker.py (does not import or read searcher.py). Run: python3 test_checker.py [certificate_dir_of_runs]"""
import glob, itertools, json, os, random, sys
import checker as C

HERE = os.path.dirname(os.path.abspath(__file__))

def find_valid_ico():
    """Icosahedron from its 20 faces; each vertex's link cycle is read off the faces, then orientations are fixed by trying all 2^12 flips."""
    U = lambda i: 1 + (i % 5); L = lambda i: 6 + (i % 5)
    faces = []
    for i in range(5):
        faces += [(0, U(i), U(i + 1)), (U(i), L(i), U(i + 1)), (U(i), L(i - 1), L(i)), (11, L(i), L(i + 1))]
    cyc = {}
    for u in range(12):
        fs = [tuple(x for x in f if x != u) for f in faces if u in f]   # edges of the link cycle
        nxt = {}
        for a, b in fs: nxt.setdefault(a, []).append(b); nxt.setdefault(b, []).append(a)
        start = fs[0][0]; order = [start]; prev = None; cur = start
        while True:
            nb = [x for x in nxt[cur] if x != prev]
            nx = nb[0] if prev is not None else nxt[cur][0]
            if nx == start: break
            order.append(nx); prev, cur = cur, nx
        cyc[u] = order
    for mask in range(1 << 12):
        rot = {u: (cyc[u][::-1] if mask >> u & 1 else cyc[u]) for u in range(12)}
        if C.check_triangulation(12, rot) is None: return rot
    raise SystemExit('could not build icosahedron')

def ref_locked_bruteforce(adj, col, a, b, c1, c2):
    """Reference path test: DFS over simple paths in the {c1,c2}-induced subgraph (independent of checker's BFS)."""
    sys.setrecursionlimit(5000)
    def dfs(u, seen):
        if u == b: return True
        for w in adj[u]:
            if w not in seen and col[w] in (c1, c2):
                seen.add(w)
                if dfs(w, seen): return True
        return False
    return dfs(a, {a})

def all_colourings(adj, order):
    col = {}
    def rec(k):
        if k == len(order): yield dict(col); return
        u = order[k]
        used = {col[w] for w in adj[u] if w in col}
        for c in range(4):
            if c not in used:
                col[u] = c; yield from rec(k + 1); del col[u]
    yield from rec(0)

def test_icosahedron_regression():
    rot = find_valid_ico()
    assert C.check_triangulation(12, rot) is None
    v = 0; link = rot[v]
    adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
    order = sorted(adj, key=lambda u: -len(adj[u]))
    # colour link vertices and others: enumerate colourings with x0 coloured 0 (colour symmetry)
    stats = {}; n_states = 0; shifts_ok = True; prop1_ok = True
    for col in all_colourings(adj, [u for u in range(12) if u != v]):
        if col[link[0]] != 0: continue
        if len({col[x] for x in link}) != 4: continue
        n_states += 1
        cert = dict(n=12, v=v, link=link, rot={str(u): rot[u] for u in rot}, colour=[col.get(u, 0) for u in range(12)])
        ok, msg, L, out = C.verify(cert)
        assert ok, msg
        # reference chain length via brute-force path search + the F definition re-derived here
        cur = dict(col); Lr = 0
        for _ in range(12):
            cs = [cur[x] for x in link]
            if len(set(cs)) != 4: break
            j = [k for k in range(5) if cs[k] == cs[(k + 2) % 5]][0]
            b_, g_, d_, a_ = cs[(j + 1) % 5], cs[(j + 3) % 5], cs[(j + 4) % 5], cs[j]
            if not (ref_locked_bruteforce(adj, cur, link[(j + 1) % 5], link[(j + 3) % 5], b_, g_) and
                    ref_locked_bruteforce(adj, cur, link[(j + 1) % 5], link[(j + 4) % 5], b_, d_)): break
            Lr += 1
            # component of x_{j+2} in colours {a_, g_}
            comp = {link[(j + 2) % 5]}; st = list(comp)
            while st:
                u = st.pop()
                for w in adj[u]:
                    if w not in comp and cur[w] in (a_, g_): comp.add(w); st.append(w)
            cur = {u: ((g_ if cur[u] == a_ else a_) if u in comp else cur[u]) for u in cur}
        assert Lr == L, (Lr, L)
        stats[L] = stats.get(L, 0) + 1
        # Theorem A: index advances by 3 and swapped component misses x_j on locked steps; Proposition 1 link patterns
        locked_recs = [r for r in out if r.get('doubly_locked')]
        for r1, r2 in zip(locked_recs, locked_recs[1:]):
            shifts_ok &= (r2['repeat_index'] - r1['repeat_index']) % 5 == 3
        for r in locked_recs:
            if 'F_component_contains_xj' in r: shifts_ok &= not r['F_component_contains_xj']
        if len(locked_recs) >= 2:
            # Prop. 1: step k link, written as canonical pattern relative to x_j: s0 (a,b,a,g,d) -> s1 (a,b,g,a,d)
            r0, r1 = locked_recs[0], locked_recs[1]
            j0 = r0['repeat_index']; cs0 = r0['link_colours']; a0, b0, g0, d0 = cs0[j0], cs0[(j0+1)%5], cs0[(j0+3)%5], cs0[(j0+4)%5]
            expect = [None] * 5
            for k, val in enumerate(cs0): expect[k] = val
            expect[(j0 + 2) % 5] = g0; expect[(j0 + 3) % 5] = a0   # s1 = (a,b,g,a,d) relative to old j
            prop1_ok &= r1['link_colours'] == expect
    print('icosahedron: %d states, chain-length histogram %s; Theorem A shifts ok=%s; Prop 1 step ok=%s' % (n_states, dict(sorted(stats.items())), shifts_ok, prop1_ok))
    assert shifts_ok and prop1_ok and n_states > 0

def test_hand_cases():
    rot = find_valid_ico(); v = 0; link = rot[v]
    # hand case 1: colour lower ring and bottom so that x1 cannot reach x3 in colours beta,gamma:
    # link colours a,b,a,g,d = 0,1,0,2,3 ; the BETA-GAMMA path needs colours {1,2}; give every other vertex colour 0 or 3 where legal -> not locked, length 0
    col = [0] * 12
    for k, c in enumerate([0, 1, 0, 2, 3]): col[link[k]] = c
    # lower ring/bottom: choose a proper colouring avoiding colours 1 and 2 if possible, else skip
    adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
    for colr in all_colourings({u: adj[u] for u in adj}, [u for u in range(12) if u != v]):
        if [colr[x] for x in link] == [0, 1, 0, 2, 3] and all(colr[u] in (0, 3) for u in range(1, 12) if u not in link):
            c2 = [colr.get(u, 0) for u in range(12)]
            cert = dict(n=12, v=v, link=link, rot={str(u): rot[u] for u in rot}, colour=c2, claimed_length=0)
            ok, msg, L, out = C.verify(cert)
            assert ok and L == 0, (ok, msg, L)
            # beta=1 vertex is x1 whose only coloured neighbours in {1,2}: x3 is not adjacent to x1 (non-consecutive link vertices);
            # a bichromatic path would need an intermediate vertex of colour 1/2 outside the link, none exist, so no lock: length 0 by hand.
            print('hand case (no 1/2 vertices off the link -> no beta-gamma lock): length 0 as predicted')
            break
    else:
        print('hand case: no such colouring exists (skipped)')

def cert_files():
    return sorted(glob.glob(os.path.join(HERE, 'runs', 'band_*', 'recert_seed_*.json')))

def best_certs(minlen):
    res = []
    for f in cert_files():
        r = json.load(open(f))
        if r.get('certificate') and r['certificate']['claimed_length'] >= minlen: res.append((f, r['certificate']))
    return res

def test_mutations():
    certs = best_certs(3)
    if not certs:
        print('mutation tests: no certificates with length>=3 in runs/ (skipped)'); return
    rnd = random.Random(12345)
    rejected = accepted_same = total = 0
    for f, cert in certs[:40]:
        ok, msg, L, _ = C.verify(cert); assert ok, (f, msg)
        # claimed length +1 and -1
        for d in (1, -1):
            c = dict(cert); c['claimed_length'] = cert['claimed_length'] + d
            assert not C.verify(c)[0]
        # improper colouring: give an edge's ends the same colour
        n, v = cert['n'], cert['v']
        rot = {int(u): ns for u, ns in cert['rot'].items()}
        for _ in range(5):
            u = rnd.choice([x for x in range(n) if x != v]); w = rnd.choice([x for x in rot[u] if x != v])
            c = json.loads(json.dumps(cert)); c['colour'][w] = c['colour'][u]
            assert not C.verify(c)[0]; rejected += 1; total += 1
        # random single-vertex recolouring: accepted only if the recomputed length still equals the claim
        for _ in range(30):
            u = rnd.choice([x for x in range(n) if x != v])
            c = json.loads(json.dumps(cert)); c['colour'][u] = rnd.randrange(4)
            ok2, msg2, L2, _ = C.verify(c); total += 1
            if ok2: assert L2 == cert['claimed_length']; accepted_same += 1
            else: rejected += 1
        # corrupt the triangulation: swap two neighbours in a rotation, drop an edge
        c = json.loads(json.dumps(cert)); k = str(rnd.choice([x for x in range(n)])); ns = c['rot'][k]
        ns[0], ns[2] = ns[2], ns[0]; r2 = C.verify(c)[0]; total += 1; rejected += (not r2)
        c = json.loads(json.dumps(cert)); u = str(rnd.randrange(n)); w = c['rot'][u].pop(0); c['rot'][str(w)].remove(int(u))
        assert not C.verify(c)[0]; rejected += 1; total += 1
        # wrong link orientation/order
        c = json.loads(json.dumps(cert)); c['link'] = [cert['link'][i] for i in (0, 2, 1, 3, 4)]
        assert not C.verify(c)[0]; rejected += 1; total += 1
    print('mutation tests: %d certificates (length>=3), %d mutations, %d rejected, %d benign recolourings accepted with unchanged length' % (min(40, len(certs)), total, rejected, accepted_same))

def test_reference_on_certs():
    # compare the checker's chain length with the brute-force reference (explicit simple-path DFS) on regenerated certificates
    fs = sorted(glob.glob(os.path.join(HERE, 'runs', 'band_*', 'recert_seed_*.json')))[:300]
    n = 0
    for f in fs:
        cert = json.load(open(f))['certificate']
        rot = {int(u): ns for u, ns in cert['rot'].items()}; v = cert['v']; link = cert['link']
        adj = {u: [w for w in rot[u] if w != v] for u in rot if u != v}
        cur = {u: cert['colour'][u] for u in adj}; Lr = 0
        for _ in range(45):
            cs = [cur[x] for x in link]
            if len(set(cs)) != 4: break
            j = [k for k in range(5) if cs[k] == cs[(k + 2) % 5]][0]
            b_, g_, d_, a_ = cs[(j + 1) % 5], cs[(j + 3) % 5], cs[(j + 4) % 5], cs[j]
            if not (ref_locked_bruteforce(adj, cur, link[(j + 1) % 5], link[(j + 3) % 5], b_, g_) and
                    ref_locked_bruteforce(adj, cur, link[(j + 1) % 5], link[(j + 4) % 5], b_, d_)): break
            Lr += 1
            comp = {link[(j + 2) % 5]}; st = list(comp)
            while st:
                u = st.pop()
                for w in adj[u]:
                    if w not in comp and cur[w] in (a_, g_): comp.add(w); st.append(w)
            cur = {u: ((g_ if cur[u] == a_ else a_) if u in comp else cur[u]) for u in cur}
        ok, msg, L, _ = C.verify(cert)
        assert ok and L == Lr == cert['claimed_length'], (f, ok, msg, L, Lr)
        n += 1
    print('reference (DFS) agrees with checker on %d regenerated certificates' % n)

if __name__ == '__main__':
    test_icosahedron_regression(); test_hand_cases(); test_reference_on_certs(); test_mutations()
    print('ALL TESTS PASSED')
