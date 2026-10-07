#!/usr/bin/env python3
"""Job Y: full sigma-group accounting at p27 #68456 h19 (plantri) and p27m #166916 h19 (the two Lemma R failure types at order 27).
For each cycle of the sigma-group of the positive cycles: w, L, Lambda, its excursions (unfilled run u + following filled run f; lambda-mass u - 3f; a Gamma-cycle has none)
marked hit / unhit by exits; exits = R3 DD-endpoint states of positive cycles with lockless sigma-image on another cycle (NightF6Flow 1.1)."""
from uv_lib import Hole
from collections import defaultdict
def run(name, h, mirror):
    H = Hole(name, h, mirror); print('==== %s hole %d, %s orientation: link degrees %s, states %d, pi-cycles %d, class sum w %d'
                                      % (name, h, 'mirror' if mirror else 'plantri', [len(H.rot[x]) for x in H.L], H.S, len(H.cycles), sum(H.W)))
    up = list(range(len(H.cycles)))
    def f(x):
        while up[x] != x: up[x] = up[up[x]]; x = up[x]
        return x
    exits = []
    for k in range(H.S):
        if not H.isDDend(k): continue
        s = H.sigma(k)
        if H.cyc[s] != H.cyc[k]: up[f(H.cyc[k])] = f(H.cyc[s])
        if H.W[H.cyc[k]] > 0:
            j, ty, hi, roles = H.frame(k); lk = H.locks(s)
            if ty == 3 and not H.filled(s) and not lk[0] and not lk[1] and H.cyc[s] != H.cyc[k]: exits.append((k, s, H.f_after(s)))
    pos = [c for c in range(len(H.cycles)) if H.W[c] > 0]
    groups = {f(c) for c in pos}
    hit = {s: (k, ff) for k, s, ff in exits}
    for g in groups:
        mem = [c for c in range(len(H.cycles)) if f(c) == g]; print('  sigma-group: %d cycles, sum lambda %d' % (len(mem), 5 * sum(H.W[c] for c in mem)))
        for c in mem:
            z = H.cycles[c]; L = len(z); print('   cycle %d: w %d, L %d, Lambda %d%s' % (c, H.W[c], L, 5 * H.W[c], ' (POSITIVE)' if H.W[c] > 0 else ''))
            if all(not H.filled(x) for x in z): print('      all unfilled (no excursions)'); continue
            s0 = next(i for i in range(L) if H.filled(z[i - 1]) and not H.filled(z[i]))
            zz = z[s0:] + z[:s0]; i = 0; exc = []
            while i < L:
                u = 0
                while i < L and not H.filled(zz[i]): u += 1; i += 1
                ff = 0
                while i < L and H.filled(zz[i]): ff += 1; i += 1
                start = zz[i - u - ff]; exc.append((u, ff, u - 3 * ff, start))
            for u, ff, mass, st in exc:
                tag = ('HIT by exit from state %d (cycle %d), f %d, credit %d' % (hit[st][0], H.cyc[hit[st][0]], hit[st][1], 3 * hit[st][1] - 1)) if (u == 1 and st in hit) else 'unhit'
                print('      excursion u %d f %d lambda-mass %d  %s' % (u, ff, mass, tag))
            hm = sum(u - 3 * ff for u, ff, _, st in exc if u == 1 and st in hit)
            print('      Lambda %d = hit mass %d + unhit mass %d -> rem %d' % (5 * H.W[c], hm, 5 * H.W[c] - hm, 5 * H.W[c] - hm))
        for c in pos:
            if f(c) != g: continue
            ex = [(k, s, ff) for k, s, ff in exits if H.cyc[k] == c]
            print('   exits of positive cycle %d (Lambda %d): %s; Cr_N = %d' % (c, 5 * H.W[c], [('src', k, 'f', ff, 'credit', 3 * ff - 1, 'target', H.cyc[s], 'w', H.W[H.cyc[s]]) for k, s, ff in ex],
                                                                         sum(3 * ff - 1 for k, s, ff in ex if H.W[H.cyc[s]] <= 0)))
run('p27#68456', 19, False)
run('p27#166916', 19, True)
