#!/usr/bin/env python3
"""Job U: p27 #133619 h21, the F4 failure (k = 4 lockless exit with f = 1), both orientations."""
from uv_lib import Hole
CN = 'abcd'
def lc(H, k): return ' '.join('%s%s' % ('x%d=' % t, CN[c]) for t, c in enumerate(H.linkc(k)))
for mirror in (False, True):
    H = Hole('p27#133619', 21, mirror); print('==== p27 #133619 hole 21, %s orientation; link degrees %s; states %d; pi-cycles %d' % ('mirror' if mirror else 'plantri', [len(H.rot[x]) for x in H.L], H.S, len(H.cycles)))
    for ci, z in enumerate(H.cycles):
        if not all(H.DL[x] for x in z): continue
        print('  Gamma-cycle %d: L %d, w %d' % (ci, len(z), H.W[ci]))
        for x in z:
            j, ty, hi, roles = H.frame(x)
            if ty != 3 or hi != [4]: continue
            s = H.sigma(x); lk = H.locks(s)
            if H.filled(s) or lk is None or lk[0] or lk[1]: continue
            f = H.f_after(s)
            if f != 1: continue
            print('   SOURCE R3@k=4 state %d: repeat j=%d; link %s; roles (alpha,mu,A,B) = %s' % (x, j, lc(H, x), tuple(CN[c] for c in roles)))
            ch = [t for t in range(5) if H.linkc(x)[t] != H.linkc(s)[t]]
            print('   LANDING sigma(r) = state %d on cycle %d (w %d, L %d): link %s; link vertices recoloured: %s; locks (Lock1, Lock2) = %s; pi-move of sigma(r): %s'
                  % (s, H.cyc[s], H.W[H.cyc[s]], len(H.cycles[H.cyc[s]]), lc(H, s), ['x%d' % t for t in ch], lk, H.kind[s]))
            y = H.pi[s]; print('   excursion: sigma(r) (u = 1) -> filled state %d (link %s; its move %s, lambda %d) -> next state %d (%s; link %s)'
                               % (y, lc(H, y), H.kind[y], H.lam[y], H.pi[y], 'filled' if H.filled(H.pi[y]) else 'unfilled', lc(H, H.pi[y])))
            # why f = 1: the filled state's move is phiA (x_{i+4} not in the {Y,Z}-component of x_{i+2}) rather than tau
            c = H.linkc(y); from collections import Counter; cnt = Counter(c); i = next(i for i in range(5) if cnt[c[i]] == 1)
            print('   filled state: singleton colour at x%d; W=%s X=%s Y=%s; phiA applies since x%d is not in the {Y,Z}-component of x%d -> f = 1 (tau would need that component to reach x%d)'
                  % (i, CN[c[i]], CN[c[(i + 1) % 5]], CN[c[(i + 2) % 5]], (i + 4) % 5, (i + 2) % 5, (i + 4) % 5))

# Addendum: rotation system and full colourings (vertex -> colour, canonical labels a-d) of r, sigma(r), pi(sigma r), pi^2(sigma r); K_sigma's link vertices
import json
out = {}
for mirror in (False, True):
    H = Hole('p27#133619', 21, mirror); rec = {'rotation_system': H.rot, 'hole': 21, 'link': H.L, 'outer_w': H.w, 'cases': []}
    for ci, z in enumerate(H.cycles):
        if not all(H.DL[x] for x in z): continue
        for x in z:
            j, ty, hi, roles = H.frame(x)
            if ty != 3 or hi != [4]: continue
            s = H.sigma(x); lk = H.locks(s)
            if H.filled(s) or lk is None or lk[0] or lk[1] or H.f_after(s) != 1: continue
            st = H.sp.states[x]; al, mu = roles[0], roles[1]; m = H.sp.linki[(j + 1) % 5]
            K = next(K for K in H.sp.components(st, al, mu) if K >> m & 1)
            seq = [x, s, H.pi[s], H.pi[H.pi[s]]]
            rec['cases'].append({'gamma_cycle': ci, 'repeat_j': j, 'K_sigma_vertices': H.sp.mask_vertices(K), 'K_sigma_link_vertices': [t for t in range(5) if K >> H.sp.linki[t] & 1],
                                 'states': {nm: {str(v): 'abcd'[H.col(k, v)] for v in sorted(H.sp.order)} for nm, k in zip(('r', 'sigma_r', 'pi_sigma_r', 'pi2_sigma_r'), seq)},
                                 'moves': {nm: H.kind[k] for nm, k in zip(('r', 'sigma_r', 'pi_sigma_r', 'pi2_sigma_r'), seq)}})
    out['mirror' if mirror else 'plantri'] = rec
json.dump(out, open('jobu-p27-133619-h21.json', 'w'), indent=1)
for o, rec in out.items():
    for c in rec['cases']: print(o, 'case: K_sigma link vertices x%s' % c['K_sigma_link_vertices'], '|K_sigma| =', len(c['K_sigma_vertices']), 'moves', c['moves'])
