#!/usr/bin/env python3
"""Track S experiment 1: alpha-orientation height along Phi.

At a rigid state u every pair graph is a forest whose 8 components each meet the link.  Root each component at a link
vertex (a 'root rule', chosen by role position), orient every forest edge towards its root, and orient the spoke
h-x_k out of x_k iff x_k roots 2 components.  If every link vertex roots 1 or 2 components (three roots 2, two roots 1),
this is an alpha-orientation of T with outdegree 3 at interior vertices, 2 at link vertices, 2 at h: the same alpha for
every rigid state.  Two alpha-orientations differ by a circulation = boundary of a face function phi (sphere).
We test whether phi(O(Phi u)) - phi(O(u)) has a fixed sign (a lattice-monotone potential would forbid periodic Phi).
usage: ts_orient.py GRAPHFILE name:hole ...
"""
import sys, itertools
from ts_lib import load_graphs, HoleData, Geo, phi_steps, pair_components

COMPS = {'am': {0, 1, 2}, 'AB': {3, 4}, 'K': {2, 3}, 'K0': {0}, 'mB': {1, 4}, 'J0': {0, 4}, 'J2': {2}, 'mA': {1, 3}}
NAMES = sorted(COMPS)


def rules():
    out = []
    for choice in itertools.product(*[sorted(COMPS[c]) for c in NAMES]):
        r = [0] * 5
        for p in choice: r[p] += 1
        if all(1 <= x <= 2 for x in r): out.append(dict(zip(NAMES, choice)))
    return out


def named_components(hd, i):
    r = hd.info[i]; col = hd.col[i]; al, mu, A, B = r['roles']; x = r['x']
    out = {}
    for nm, pr in (('am', (al, mu)), ('AB', (A, B)), ('aA', (al, A)), ('mB', (mu, B)), ('aB', (al, B)), ('mA', (mu, A))):
        cs = pair_components(hd, col, pr)
        if nm == 'aA':
            for K in cs:
                if x[2] in K: out['K'] = K
                elif x[0] in K: out['K0'] = K
                else: raise ValueError
        elif nm == 'aB':
            for K in cs:
                if x[0] in K: out['J0'] = K
                elif x[2] in K: out['J2'] = K
                else: raise ValueError
        else:
            assert len(cs) == 1; out[nm] = cs[0]
    return out


def orientation(hd, i, rule):
    """dict dart (a,b) meaning a->b, for every edge of T"""
    rot = hd.rot; h = hd.h; r = hd.info[i]; x = r['x']
    comps = named_components(hd, i)
    O = {}
    rcount = [0] * 5
    for nm, K in comps.items():
        root = x[rule[nm]]; rcount[rule[nm]] += 1
        seen = {root}; st = [root]
        while st:
            a = st.pop()
            for b in rot[a]:
                if b in K and b not in seen:
                    seen.add(b); st.append(b); O[(b, a)] = 1
        assert seen == K
    for k in range(5):
        if rcount[k] == 2: O[(x[k], h)] = 1
        else: O[(h, x[k])] = 1
    E = sum(len(q) for q in rot) // 2
    assert len(O) == E, (len(O), E)
    return O


def diff_phi(geo, O1, O2):
    circ = {}
    for (a, b) in O1:
        if (a, b) not in O2: circ[(b, a)] = 1      # reversed edge, as a unit of flow in O2's direction
    return geo.potential(circ)


def main():
    G = load_graphs(sys.argv[1])
    RU = rules()
    print('root rules', len(RU))
    stats = {k: [0, 0, 0, 0] for k in range(len(RU))}   # [steps, phi>=min at all hfaces & sign+, sign-, mixed]
    for spec in sys.argv[2:]:
        nm, h = spec.rsplit(':', 1); h = int(h)
        rot = G[nm]; hd = HoleData(rot, h); geo = Geo(rot, h)
        steps = phi_steps(hd)
        print(nm, h, 'Phi steps', len(steps), flush=True)
        for (u, c, u2) in steps:
            for k, rule in enumerate(RU):
                O1 = orientation(hd, u, rule); O2 = orientation(hd, u2, rule)
                phi = diff_phi(geo, O1, O2)
                assert phi is not None
                hv = [phi[f] for f in geo.hfaces]
                # normalise at the h-faces: sign of phi - (value at h-faces) if all h-faces agree
                st = stats[k]; st[0] += 1
                if len(set(hv)) == 1:
                    d = [p - hv[0] for p in phi]
                    if min(d) >= 0 and max(d) > 0: st[1] += 1
                    elif max(d) <= 0 and min(d) < 0: st[2] += 1
                    else: st[3] += 1
                else: st[3] += 1
    for k, rule in enumerate(RU):
        print(k, rule, stats[k])


if __name__ == '__main__':
    main()
