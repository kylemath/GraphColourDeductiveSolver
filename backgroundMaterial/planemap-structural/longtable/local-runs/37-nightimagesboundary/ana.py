#!/usr/bin/env python3
"""[exploratory] NightImagesBoundary analysis of ib-*.json. Usage: ana.py ib-census.json [ib-hits.json]"""
import sys, json, math
from collections import Counter, defaultdict
KS = ('N0', 'L1', 'L2', 'DL')
def q(xs, ps=(0, .1, .5, .9, 1)):
    xs = sorted(xs); return [round(xs[min(len(xs) - 1, int(p * (len(xs) - 1) + .5))], 3) for p in ps] if xs else []
for fn in sys.argv[1:]:
    R = json.load(open(fn)); print('=' * 30, fn, 'classes', len(R))
    chk = Counter(); smat = Counter(); fmax = Counter(); umax_exc = []
    agg_img = Counter(); agg_heavy = Counter(); agg_exp2 = defaultdict(float); agg_exp1 = 0.0
    perZ = []; dens = []
    for r in R:
        cy = r['cycles']; G = set(r['gamma'])
        for k, v in r['smat'].items(): smat[k] += v
        for (L, Lam, F, n0, l1, l2, dl, e, um, fm, pdl) in cy:
            chk['Lam=L-4F'] += (Lam == L - 4 * F); chk['L1=L2'] += (l1 == l2); chk['cycles'] += 1
            if e: fmax[fm] += 1; chk['-Lam<=(3fmax-1)e'] += (-Lam <= (3 * fm - 1) * e); chk['exc cycles'] += 1
            if e: chk['-Lam<=3F-e'] += (-Lam <= 3 * F - e)
            dens.append((Lam / L, e / L, (n0 + l1 + l2) / max(1, L - F) if L > F else 0, L))
        # sigma pair structure, conditioned: states of kind k (on cycle T) whose sigma-image is a non-fixed DL state
        # (recomputed from smat is impossible per cycle; use image lists of Gamma-cycles only)
        for g in G:
            Lz = cy[g][0]; others = [t for t in range(len(cy)) if t != g]
            H = {t for t in others if cy[t][1] <= -Lz}
            tot = {k: sum(cy[t][3 + i] for t in others) for i, k in enumerate(KS)}
            hk = {k: (sum(cy[t][3 + i] for t in H) / tot[k] if tot[k] else 0) for i, k in enumerate(KS)}
            U = lambda t: cy[t][0] - cy[t][2]
            hU = sum(U(t) for t in H) / sum(U(t) for t in others)
            hE = sum(cy[t][7] for t in H) / max(1, sum(cy[t][7] for t in others))
            ims = r['imgs'][str(g)]; off = [(t, k) for t, k, gg in ims if k != 'fixed' and t != g]
            kc = Counter(k for t, k, gg in ims); onG = sum(1 for t, k, gg in ims if k != 'fixed' and gg)
            onself = sum(1 for t, k, gg in ims if k != 'fixed' and t == g)
            heavy = sum(1 for t, k in off if t in H)
            best = max([-cy[t][1] / Lz for t, k in off] + [0])
            for t, k in off:
                agg_img[k] += 1; agg_heavy[k] += (t in H); agg_exp2[k] += hk[k]
            agg_exp1 += hU * len(off)
            pf2 = math.prod(1 - hk[k] for t, k in off); pf1 = (1 - hU) ** len(off); pfE = (1 - hE) ** len([1 for t, k in off if k != 'DL'])
            n0h = sum(1 for t, k in off if k == 'N0' and t in H); bh = sum(1 for t, k in off if k != 'DL' and t in H)
            minN0 = min([-cy[t][1] / Lz for t, k in off if k == 'N0'] + [99999])
            bestN0 = max([-cy[t][1] / Lz for t, k in off if k == 'N0'] + [0]); bestB = max([-cy[t][1] / Lz for t, k in off if k != 'DL'] + [0])
            nfix = kc['fixed']; poolL = sum(cy[t][10] for t in range(len(cy)) if t not in H)
            # kind-matched model: median best ratio
            thr = sorted({-cy[t][1] for t in others if cy[t][1] < 0}, reverse=True); med = 0
            for x in thr:
                Hx = [t for t in others if -cy[t][1] >= x]
                p = 1 - math.prod(1 - (sum(cy[t][3 + KS.index(k)] for t in Hx) / tot[k] if tot[k] else 0) for t0, k in off)
                if p >= .5: med = x / Lz; break
            perZ.append(dict(n0=kc['N0'], n0h=n0h, bh=bh, minN0=minN0, bestN0=bestN0, bestB=bestB, poolslack=poolL - (Lz - nfix), med=med, tag=r['tag'] + ':' + r['orientation'][0], L=Lz, n=len(off), heavy=heavy, best=best, hU=hU, hE=hE, hk=hk,
                             kinds=dict(kc), onG=onG, onself=onself, pf1=pf1, pf2=pf2, pfE=pfE, exp2=sum(hk[k] for t, k in off)))
    print('checks', dict(chk)); print('fmax on cycles with excursions', dict(sorted(fmax.items())))
    print('sigma kind matrix (all unfilled states of the classes):')
    for a in KS:
        print('  %s ->' % a, {b: smat['%s>%s' % (a, b)] for b in KS + ('fixed',)})
    print('  involution symmetry a>b == b>a:', all(smat['%s>%s' % (a, b)] == smat['%s>%s' % (b, a)] for a in KS for b in KS))
    print('Gamma-cycles', len(perZ))
    print('image kinds (all L states):', dict(sum((Counter(z['kinds']) for z in perZ), Counter())))
    print('non-fixed images on a Gamma-cycle: total', sum(z['onG'] for z in perZ), ' of which on Z itself', sum(z['onself'] for z in perZ),
          ' Z with an image on another Gamma-cycle', sum(1 for z in perZ if z['onG'] > z['onself']))
    print('off-Z non-fixed images by kind and heavy landing (obs heavy / kind-matched expectation):')
    for k in KS: print('  %s: n=%d heavy=%d exp=%.1f obs-share=%.3f' % (k, agg_img[k], agg_heavy[k], agg_exp2[k], agg_heavy[k] / max(1, agg_img[k])))
    print('  all: n=%d heavy=%d exp(uniform-U)=%.1f exp(kind)=%.1f' % (sum(agg_img.values()), sum(agg_heavy.values()), agg_exp1, sum(agg_exp2.values())))
    print('per Z: heavy-share hU', q([z['hU'] for z in perZ]), ' excursion-share hE', q([z['hE'] for z in perZ]))
    for k in KS: print('   kind share h_%s' % k, q([z['hk'][k] for z in perZ]))
    print('per Z: #heavy images', q([z['heavy'] for z in perZ]), ' kind-matched expectation', q([z['exp2'] for z in perZ]))
    print('per Z: P_fail uniform-U', q([z['pf1'] for z in perZ]), ' kind-matched', q([z['pf2'] for z in perZ]), ' excursion (boundary images)', q([z['pfE'] for z in perZ]))
    print('   sum P_fail (expected # (c)-failures): U %.1e kind %.1e exc %.1e ; observed 0; max per-Z: U %.1e kind %.1e exc %.1e' % (sum(z['pf1'] for z in perZ), sum(z['pf2'] for z in perZ), sum(z['pfE'] for z in perZ), max(z['pf1'] for z in perZ), max(z['pf2'] for z in perZ), max(z['pfE'] for z in perZ)))
    print('per Z: #lockless images', q([z['n0'] for z in perZ]), ' #lockless on heavy', q([z['n0h'] for z in perZ]), ' Z with none', sum(1 for z in perZ if z['n0h'] == 0))
    print('per Z: #boundary (N0/L1/L2) images on heavy', q([z['bh'] for z in perZ]), ' Z with none', sum(1 for z in perZ if z['bh'] == 0))
    print('per Z: min ratio over lockless images', q([z['minN0'] for z in perZ if z['n0']]), ' best lockless ratio', q([z['bestN0'] for z in perZ]), ' best boundary ratio', q([z['bestB'] for z in perZ]))
    print('lockless images with ratio < 1 (all Z):', sum(z['n0'] - z['n0h'] for z in perZ), 'of', sum(z['n0'] for z in perZ))
    print('pool slack |D* minus H| - |Z minus Fix| (forcing needs < 0):', q([z['poolslack'] for z in perZ]), ' forced Z', sum(1 for z in perZ if z['poolslack'] < 0), [(z['tag'], z['poolslack']) for z in perZ if z['poolslack'] < 0][:8])
    print('kind-matched model median best ratio', q([z['med'] for z in perZ]), ' observed/model', q([z['best'] / z['med'] if z['med'] else 0 for z in perZ]))
    print('per Z best ratio', q([z['best'] for z in perZ]))
    w = sorted(perZ, key=lambda z: -z['pf2'])[:6]
    for z in w: print('   worst', z['tag'], 'L', z['L'], 'n', z['n'], 'heavy', z['heavy'], 'best', round(z['best'], 2), 'hU %.2f hE %.2f' % (z['hU'], z['hE']), {k: round(v, 2) for k, v in z['hk'].items()}, z['kinds'])
    # excursion density vs mass density over cycles (weighted by length)
    bins = defaultdict(lambda: [0, 0.0, 0.0])
    for ld, ed, bd, L in dens:
        b = ('Lam/L<=-0.5' if ld <= -.5 else '-0.5<Lam/L<=-0.2' if ld <= -.2 else '-0.2<Lam/L<0' if ld < 0 else 'Lam/L=0' if ld == 0 else 'Lam>0')
        bins[b][0] += L; bins[b][1] += ed * L; bins[b][2] += bd * L
    print('length-weighted excursion density e/L and boundary share of unfilled (N0+L1+L2)/U by mass density:')
    for b, (L, e, bd) in bins.items(): print('   %-18s states %7d  e/L %.3f  boundary/U %.3f' % (b, L, e / L, bd / L))
