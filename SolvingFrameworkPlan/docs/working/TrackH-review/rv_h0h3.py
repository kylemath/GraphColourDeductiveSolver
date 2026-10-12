"""Item 2: test Lemma H0, Lemma H3 (and H4/H5 side claims, rigid isolation off the sphere) on fresh
random triangulations of torus / RP^2 / Klein bottle / sphere.
Usage: python3 rv_h0h3.py SURFACE NGRAPHS NMIN NMAX SEED OUTJSON"""
import sys
import json
import random
from collections import Counter
import rv_core as R
import rv_surf as S


def orientable(F):
    # try to orient faces consistently
    import collections
    edge_faces = collections.defaultdict(list)
    for i, f in enumerate(F):
        for k in range(3):
            edge_faces[frozenset((f[k], f[(k + 1) % 3]))].append(i)
    ori = {0: tuple(F[0])}
    st = [0]
    while st:
        i = st.pop()
        f = ori[i]
        for k in range(3):
            u, v = f[k], f[(k + 1) % 3]
            for j in edge_faces[frozenset((u, v))]:
                if j == i:
                    continue
                g = F[j]
                # want g oriented with v->u
                cand = None
                for gg in (tuple(g), tuple(reversed(g))):
                    for m in range(3):
                        if gg[m] == v and gg[(m + 1) % 3] == u:
                            cand = gg
                if j in ori:
                    if ori[j] != cand and not any(ori[j][m:] + ori[j][:m] == cand for m in range(3)):
                        return False
                else:
                    ori[j] = cand
                    st.append(j)
    return True


def run_hole(F, chi, h, tally, ex):
    adj = S.adjacency(F)
    n = len(adj)
    x = S.link_cycle(F, h)
    assert sorted(x) == sorted(adj[h]) and len(x) == 5
    cols = R.colourings(adj, h, canonical=True)
    edges = [(u, v) for u in range(n) for v in adj[u] if u < v and u != h and v != h]
    infos = {}
    pimg = {}
    for c in cols:
        inf = R.state_info(adj, h, x, c)
        infos[c] = inf
        # ---- H3: edge balance for every state (filled or not) ----
        parts = [({0, 1}, {2, 3}), ({0, 2}, {1, 3}), ({0, 3}, {1, 2})]
        if inf is not None:
            al, mu, A, B = inf['roles']
            parts_role = [({al, mu}, {A, B}), ({al, A}, {mu, B}), ({al, B}, {mu, A})]
        else:
            parts_role = parts
        link_edges = [(x[t], x[(t + 1) % 5]) for t in range(5)]
        for k, (p1, p2) in enumerate(parts_role):
            def inpart(u, v):
                cu, cv = c[u], c[v]
                return ({cu, cv} <= p1) or ({cu, cv} <= p2)
            Ek = sum(1 for u, v in edges if inpart(u, v))
            lk = sum(1 for u, v in link_edges if inpart(u, v))
            pred2 = 2 * n - 2 * chi - 5 + lk  # = 2 E_k
            tally['H3_general_checked'] += 1
            if 2 * Ek != pred2:
                tally['H3_general_FAIL'] += 1
            if inf is not None:
                # specific form: E1=n-chi-1, E2=E3=n-chi-2; c_k-beta_k = chi, chi+1, chi+1
                tally['H3_unfilled_checked'] += 1
                want_l = (3, 1, 1)[k]
                if lk != want_l:
                    tally['H3_linkcount_FAIL'] += 1
                ck = len(R.components(adj, h, c, *sorted(p1))) + len(R.components(adj, h, c, *sorted(p2)))
                Vk = n - 1
                betak = Ek - Vk + ck
                want = chi if k == 0 else chi + 1
                if ck - betak != want:
                    tally['H3_unfilled_FAIL'] += 1
                    if len(ex['H3']) < 5:
                        ex['H3'].append(dict(k=k, Ek=Ek, ck=ck, betak=betak, chi=chi, n=n))
        if inf is not None:
            p = R.pi_map(adj, h, x, c, inf)
            pimg[c] = R.canon(p) if p is not None else None
    # ---- H0 ----
    preimg = Counter(v for v in pimg.values() if v is not None)
    for s, ps in pimg.items():
        inf = infos[s]
        if preimg[s] == 0:
            continue
        tally['pi_images'] += 1
        # proof content: a pi-image has not inB
        if inf['inB']:
            tally['H0_core_notInB_FAIL'] += 1
        if ps is None:
            continue
        tally['H0_literal_checked'] += 1  # s unfilled, pi(s) defined, s = pi(t)
        ok = inf['D1'] and inf['D2']
        if not ok:
            tally['H0_literal_FAIL(nonDL s)' if not inf['DL'] else 'H0_literal_FAIL(DL s)'] += 1
    # all-DL pi-cycles
    seen = set()
    for c0 in pimg:
        if c0 in seen:
            continue
        path = [c0]
        cur = pimg[c0]
        while cur is not None and cur not in path:
            path.append(cur)
            cur = pimg[cur]
        if cur == c0:
            seen.update(path)
            if all(infos[s]['DL'] for s in path):
                tally['allDL_cycles'] += 1
                for s in path:
                    tally['allDL_cycle_states'] += 1
                    if not (infos[s]['D1'] and infos[s]['D2']):
                        tally['H0_cycle_FAIL'] += 1
    # D-violations overall (sanity: off sphere expected; on sphere none)
    for s, inf in infos.items():
        if inf is None:
            tally['filled'] += 1
            continue
        tally['unfilled'] += 1
        if not (inf['D1'] and inf['D2']):
            tally['D_violation_states'] += 1
        if not (inf['P1'] and inf['P2'] and inf['P3']):
            tally['P_FAIL'] += 1
    # ---- H4/H5 + rigid isolation off sphere ----
    for s, inf in infos.items():
        if inf is None or not inf['DL'] or not (inf['D1'] and inf['D2']):
            continue
        cnt = R.pair_counts(adj, h, x, s, inf)
        tally['DL_with_D'] += 1
        if any(a < b for a, b in zip(cnt, R.RIGID)):
            tally['H4_lowerbound_FAIL'] += 1
        if cnt != R.RIGID:
            continue
        tally['rigid'] += 1
        # H5: every Kempe move -> renaming, pi(s), or pi^{-1}(s)
        allowed = {s}
        if pimg[s] is not None:
            allowed.add(pimg[s])
        allowed |= {t for t, v in pimg.items() if v == s}
        for _, _, d in R.kempe_neighbours(adj, h, s):
            if R.canon(d) not in allowed:
                tally['H5_FAIL'] += 1
                break
        ps = pimg[s]
        if ps is not None and R.is_rigid(adj, h, x, ps):
            tally['rigid_to_rigid'] += 1
            if len(ex['rr']) < 5:
                ex['rr'].append(dict(h=h, n=n))


def main():
    surface, ng, nmin, nmax, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    rng = random.Random(seed)
    tally = Counter()
    ex = {'H3': [], 'rr': []}
    graphs = []
    for g in range(ng):
        nv = rng.randint(nmin, nmax)
        F, chi = S.random_surface(surface, nv, rng)
        adj = S.adjacency(F)
        V = len(adj)
        E = sum(map(len, adj)) // 2
        assert V - E + len(F) == chi
        if g == 0:
            tally['orientable'] = int(orientable(F))
        holes = [v for v in range(V) if len(adj[v]) == 5]
        tally['graphs'] += 1
        tally['holes'] += len(holes)
        for h in holes:
            run_hole(F, chi, h, tally, ex)
        graphs.append(F)
    res = dict(surface=surface, seed=seed, tally=dict(tally), examples=ex)
    json.dump(dict(res, faces=graphs), open(out, 'w'))
    print(json.dumps(res))


if __name__ == '__main__':
    main()
