#!/usr/bin/env python3
"""[exploratory] NightP1: charge-back P1 and its structure on the picyc.p1 outputs (gentri orders 17, 20-24, both orientations, every link pattern).
Exits (Job S sense): DD endpoint r of positive Z, R-type 3, sigma(r) unfilled with neither lock, on T != Z, T nonpositive; credit 3f - 1. Variant 'all': any R-type.
rem(T) = Lambda(T) - sum over hits (1 - 3f); rem > 0 charged back to the sources in proportion to credit; def' = Lambda(Z) - CrN(Z) + charge.
P1: each def' > 0 assigned to ONE nonpositive sigma-neighbour T (sigma-image of a DD endpoint of Z) with rem(T) < 0, no T over-assigned (exhaustive).
Also: link kind into the best neighbour T*, the excursion of T* containing the image, the shape of deficit cycles, and transport T's Hall ratio at the same hole.
Output: p1-struct.txt. One core, a few seconds."""
import json, sys, os, itertools
from fractions import Fraction
from collections import defaultdict, Counter
here = os.path.dirname(os.path.abspath(__file__))
runs = ['17', '20', '21', '22', '23', '24']
out = []; P = out.append
def kindname(kd, l1, l2, f):
    if kd == 0: return 'filled'
    if kd == 2: return 'DL'
    if f >= 0: return 'lockless'
    return 'lock1only' if l1 and not l2 else 'lock2only' if l2 and not l1 else 'unf?'
for variant in ['R3', 'all']:
    C = Counter(); rows = []; fails = []; posrem = []; fails_relay = []; nonb = []; fails_und = []
    for o in runs:
        for m in ['', 'm']:
            for l in open(os.path.join(here, 'out%s%s.jsonl' % (o, m))):
                if '"p1"' not in l: continue
                r = json.loads(l); p = r['p1']; C['holes'] += 1
                cyc = {int(k): v for k, v in p['cyc'].items()}; grp = {int(k): v for k, v in p['grp'].items()}
                links = {int(k): v for k, v in p['links'].items()}
                hits = defaultdict(list)   # T -> [(Z, credit, exc)]
                for Z, ls in links.items():
                    for i, T, ty, kd, l1, l2, f, e in ls:
                        if f < 0 or T == Z or cyc[T][0] > 0: continue
                        if variant == 'R3' and ty != 3: continue
                        hits[T].append((Z, 3 * f - 1, e))
                rem = {T: v[0] for T, v in cyc.items() if v[0] <= 0}
                for T, hs in hits.items(): rem[T] = cyc[T][0] + sum(c for _, c, _ in hs)
                # sanity: distinct excursions
                for T, hs in hits.items():
                    if len(set(e for _, _, e in hs)) != len(hs): C['double_hit'] += 1
                charge = defaultdict(Fraction)
                for T, hs in hits.items():
                    if rem[T] > 0:
                        tot = sum(c for _, c, _ in hs); posrem.append((o + m, r['name'], r['hole'], T, cyc[T][0], cyc[T][1], rem[T], sorted(set(z for z, _, _ in hs))))
                        for z, c, _ in hs: charge[z] += Fraction(rem[T] * c, tot)
                defs = []
                for Z, ls in links.items():
                    lam = cyc[Z][0]; C['pos'] += 1
                    cr = sum(3 * f - 1 for i, T, ty, kd, l1, l2, f, e in ls if f >= 0 and T != Z and cyc[T][0] <= 0 and (variant == 'all' or ty == 3))
                    dp = lam - cr + charge[Z]
                    nb = sorted(set(T for i, T, ty, kd, l1, l2, f, e in ls if T != Z and cyc[T][0] <= 0 and rem[T] < 0))
                    if dp > 0: defs.append((Z, dp, nb))
                    # strong one-hop: some nonpositive sigma-neighbour with -rem >= Lambda(Z)
                    if nb and max(-rem[t] for t in nb) >= lam: C['strong_ok'] += 1
                    elif not cyc[Z][2]: C['strong_fail_nonGamma'] += 1
                    else: C['strong_fail_Gamma'] += 1
                # alternative neighbour sets: (i) zero relays: sigma-paths through nonpositive cycles with rem = 0; (ii) sigma + transport-T edges (link-free DL swaps)
                adj = defaultdict(set)
                for a, b in p.get('edges', []): adj[a].add(b); adj[b].add(a)
                tE = {int(k): v for k, v in p.get('tedges', {}).items()}
                for Z, dp, nb in [(Z, None, None) for Z in links]:
                    pass
                def relay_nb(Z):
                    seen = {Z}; st = [Z]; res = set()
                    while st:
                        x = st.pop()
                        for y in adj[x]:
                            if y in seen or cyc[y][0] > 0: continue
                            seen.add(y)
                            if rem[y] < 0: res.add(y)
                            elif rem[y] == 0: st.append(y)
                    return sorted(res)
                def union_nb(Z, nb):
                    s = set(nb)
                    for T, lamT, lb, ing in tE.get(Z, []):
                        if T != Z and rem.get(T, lamT) < 0: s.add(T)
                    return sorted(s)
                for T, lamT, lb, ing in [e for v in tE.values() for e in v]:
                    if T not in rem: rem[T] = lamT
                def p1ok(dl):
                    if not all(nb for _, _, nb in dl): return False
                    capx = {T: Fraction(-v) for T, v in rem.items() if v < 0}
                    for ch in itertools.product(*[nb for _, _, nb in dl]):
                        used = defaultdict(Fraction)
                        for (Z, dp, nb), t in zip(dl, ch): used[t] += dp
                        if all(capx[t] >= used[t] for t in used): return True
                    return False
                def und_nb(Z): return sorted(y for y in adj[Z] if cyc[y][0] <= 0 and rem[y] < 0)
                if defs:
                    if not p1ok([(Z, dp, und_nb(Z)) for Z, dp, nb in defs]): C['und_fail'] += 1; fails_und.append((o + m, r['name'], r['hole']))
                    for Z, dp, nb in defs:
                        u = und_nb(Z)
                        if u: C['und_rho_min'] = min(C.get('und_rho_min', 10**9), float(max(-rem[t] for t in u) / dp))
                    C['relay_fail'] += 0 if p1ok([(Z, dp, relay_nb(Z)) for Z, dp, nb in defs]) else 1
                    C['union_fail'] += 0 if p1ok([(Z, dp, union_nb(Z, nb)) for Z, dp, nb in defs]) else 1
                    if not p1ok([(Z, dp, relay_nb(Z)) for Z, dp, nb in defs]): C['relayfails'] = C.get('relayfails', 0) + 0; fails_relay.append((o + m, r['name'], r['hole']))
                    for Z, dp, nb in defs:
                        if not nb: C['no_sigma_nb'] += 1; nonb.append((o + m, r['name'], r['hole'], r.get('pattern'), Z, cyc[Z][0], cyc[Z][1], cyc[Z][3], sorted((T, cyc[T][0], cyc[T][1]) for T in adj[Z]), relay_nb(Z), union_nb(Z, nb), [e[:2] for e in tE.get(Z, [])][:6]))
                if not defs: continue
                C['holes_def'] += 1
                cap = {T: Fraction(-v) for T, v in rem.items() if v < 0}
                bestmin = None
                if all(nb for _, _, nb in defs):
                    for ch in itertools.product(*[nb for _, _, nb in defs]):
                        used = defaultdict(Fraction)
                        for (Z, dp, nb), t in zip(defs, ch): used[t] += dp
                        mn = min(cap[t] - used[t] for t in used)
                        if bestmin is None or mn > bestmin: bestmin = mn
                if bestmin is None or bestmin < 0: fails.append((o + m, r['name'], r['hole'], [(z, str(d), nb) for z, d, nb in defs]))
                tr = r.get('transport', [{}])
                hall_T = min((t.get('a_DL_allpairs', {}).get('hall_ratio', 1e9) for t in tr), default=None)
                for Z, dp, nb in defs:
                    best = max(nb, key=lambda t: -rem[t]) if nb else None
                    lk = Counter(kindname(kd, l1, l2, f) for i, T, ty, kd, l1, l2, f, e in links[Z] if T == best)
                    landexc = [cyc[best][3][e] for i, T, ty, kd, l1, l2, f, e in links[Z] if T == best and e >= 0] if best is not None else []
                    gsum = sum(cyc[c][0] for c in cyc if grp[c] == grp[Z])
                    grpmin = min(cyc[c][0] for c in cyc if grp[c] == grp[Z])
                    rows.append(dict(run=o + m, name=r['name'], hole=r['hole'], pat=r.get('pattern'), Z=Z, Lam=cyc[Z][0], L=cyc[Z][1], gamma=cyc[Z][2], exc=cyc[Z][3], dp=dp,
                                     best=best, remb=rem.get(best), Lamb=cyc[best][0] if best is not None else None, Lb=cyc[best][1] if best is not None else None,
                                     hitb=len(hits.get(best, [])), lk=dict(lk), land=landexc, rho=Fraction(-rem[best]) / dp if best is not None else 0,
                                     minslack=bestmin, hallT=hall_T, gsum=gsum, isgrpmin=(best is not None and cyc[best][0] == grpmin)))
    P('==== variant %s (exits from %s DD endpoints)' % (variant, 'R3' if variant == 'R3' else 'all R-type'))
    P('holes with a positive cycle %d; positive cycles %d; double hits %d' % (C['holes'], C['pos'], C['double_hit']))
    P('targets with rem > 0: %d  %s' % (len(posrem), posrem[:12]))
    P('holes with def\' > 0: %d; deficit cycles %d; charge-back P1 FAILS at %d holes %s' % (C['holes_def'], len(rows), len(fails), fails[:5]))
    P('deficit cycles with NO nonpositive sigma-neighbour of rem < 0: %d' % C['no_sigma_nb'])
    for x in nonb: P('   %s' % (x,))
    P('P1 with UNDIRECTED one-hop sigma-neighbours (Z-T sigma-link from a DD endpoint of either cycle) FAILS at %d holes %s; min best-neighbour ratio %.3f' % (C['und_fail'], fails_und[:5], C.get('und_rho_min', 0)))
    P('P1 with zero relays (sigma-paths through nonpositive rem = 0 cycles) FAILS at %d holes %s; P1 on sigma + transport-T edges FAILS at %d holes' % (C['relay_fail'], fails_relay[:5], C['union_fail']))
    P('strong one-hop form (some nonpositive sigma-neighbour T with -rem(T) >= Lambda(Z)), over ALL positive cycles: ok %d, fail non-Gamma %d, fail Gamma %d' % (
        C['strong_ok'], C['strong_fail_nonGamma'], C['strong_fail_Gamma']))
    if rows:
        P('min rho = |rem(T*)|/def\' = %.3f; min optimal residual slack = %s; T* = most negative cycle of the sigma-group in %d/%d; T* hit by a lockless exit in %d/%d' % (
            float(min(x['rho'] for x in rows)), min(x['minslack'] for x in rows if x['minslack'] is not None), sum(x['isgrpmin'] for x in rows), len(rows),
            sum(1 for x in rows if x['hitb']), len(rows)))
        P('link kinds from Z into T* (counts of DD endpoints): %s' % dict(sum((Counter(x['lk']) for x in rows), Counter())))
        P('deficit cycles: Gamma %d; def\' = Lambda %d; Lambda distribution %s; L distribution %s' % (sum(1 for x in rows if x['gamma']), sum(1 for x in rows if x['dp'] == x['Lam']),
            sorted(Counter(x['Lam'] for x in rows).items()), sorted(Counter(x['L'] for x in rows).items())))
        P('positive-mass excursions of deficit cycles (u, f): %s' % sorted(Counter((u, f) for x in rows for u, f in x['exc'] if u - 3 * f > 0).items()))
        P('excursions of T* hit by sigma-images from Z (u, f): %s' % sorted(Counter(tuple(e) for x in rows for e in x['land']).items()))
        P('ratio rho vs transport Hall ratio at the same hole (rho is in lambda units for one Z; Hall in w units over all Z):')
        for x in sorted(rows, key=lambda x: x['rho'])[:12]:
            P('  %-4s %-9s h%-2d %-11s Z%-3d Lam=%-3d L=%-3d gamma=%d def\'=%-4s exc=%s  T*=%s Lam=%s L=%s rem=%s hits=%d links=%s landing=%s rho=%.2f slack=%s hallT=%s gsum=%s' % (
                x['run'], x['name'], x['hole'], x['pat'], x['Z'], x['Lam'], x['L'], x['gamma'], x['dp'], x['exc'] if len(x['exc']) <= 6 else str(x['exc'][:6]) + '...',
                x['best'], x['Lamb'], x['Lb'], x['remb'], x['hitb'], x['lk'], x['land'][:4], float(x['rho']), x['minslack'], x['hallT'], x['gsum']))
    P('')
open(os.path.join(here, 'p1-struct.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
