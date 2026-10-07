#!/usr/bin/env python3
"""Job BT summary (NightImagesBoundary §4) from out/bt{hits,hitsm,25,25m,...}.jsonl (picyc.bt --jobbt).
T row: [t, n (non-fixed images), nN0, nL1, nL2, nDL, nfixed, e_T, b_T, F_T, w_T, L_T, N0, #L1, #L2, #DL, E2, tau, |DD|, f_max, #DL-sigma-partner, isZ]."""
import json, math, sys
from collections import Counter
def pearson(x, y):
    n = len(x); mx = sum(x) / n; my = sum(y) / n; sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float('nan')
for group, files in (('census orders 25-27', ['bt%d%s' % (o, s) for o in (25, 26, 27) for s in ('', 'm')]), ('AW hit graphs', ['bthits', 'bthitsm'])):
    chk = Counter(); C = Counter(); minN0 = []; minB = []; ratios = []; pfail = []; heavy = Counter(); rows = []; seen_cycles = set(); worst = None
    for f in files:
        for l in open('../out/%s.jsonl' % f):
            if '"jobbt"' not in l: continue
            r = json.loads(l)
            for Z in r['jobbt']:
                C['Gamma-cycles'] += 1; wZ = Z['w']; LZ = 5 * wZ; T = [t for t in Z['T'] if not t[21]]; Zr = [t for t in Z['T'] if t[21]][0]
                C['R3 non-fixed images that are DL or not run boundaries'] += Z['nonboundary_R3_images']; C['DL images from R3 states'] += Z['DL_images_R3']; C['DL images from R1 states'] += Z['DL_images_R1']
                for t in Z['T']:
                    key = (r['name'], r['hole'], f, t[0])
                    if key in seen_cycles: continue
                    seen_cycles.add(key); chk['cycles checked'] += 1
                    chk['Lambda = L - 4F fails'] += 5 * t[10] != t[11] - 4 * t[9]; chk['#L1 = #L2 fails'] += t[13] != t[14]; chk['Lemma N0 (2 N0 <= |DD| - Lambda) fails'] += 2 * t[12] > t[18] - 5 * t[10]
                heavyT = [t for t in T if 5 * t[10] <= -LZ]
                nN0 = sum(t[2] for t in heavyT); nB = sum(t[2] + t[3] + t[4] for t in heavyT)
                C['IB-N0 holds'] += nN0 > 0; C['IB-B holds'] += nB > 0; minN0.append((nN0, r['name'], r['hole'], f, wZ, Z['L'])); minB.append(nB)
                ll = [t for t in T if t[2] > 0]
                if ll: ratios.append((max(-t[10] for t in ll) / wZ, r['name'], r['hole'], f, wZ, Z['L']))
                # kind-matched model: h_k = share of class states of kind k on heavy cycles; P(fail) = prod over Z's non-fixed images of (1 - h_kind)
                tot = Counter(); hv = Counter()
                for t in T:
                    for k, i in (('N0', 12), ('L1', 13), ('L2', 14), ('DL', 15)):
                        tot[k] += t[i]
                        if 5 * t[10] <= -LZ: hv[k] += t[i]
                h = {k: hv[k] / tot[k] if tot[k] else 0 for k in tot}; p = 1.0
                for k, i in (('N0', 2), ('L1', 3), ('L2', 4), ('DL', 5)):
                    n = sum(t[i] for t in T) + Zr[i]; p *= (1 - h.get(k, 0)) ** n
                    heavy[(k, 'images')] += sum(t[i] for t in T) + Zr[i]; heavy[(k, 'heavy images')] += sum(t[i] for t in heavyT)
                pfail.append((p, r['name'], r['hole'], f, wZ, Z['L']))
                for t in T: rows.append((t[1], t[7], t[8], t[12], -t[10], t[2]))
    print('=' * 20, group)
    print('exact checks:', dict(chk))
    print(dict(C))
    minN0.sort(); print('IB-N0: minimum #heavy lockless images per Z %d %s; distribution of the minimum-5: %s' % (minN0[0][0], minN0[0][1:], [m[0] for m in minN0[:5]]))
    print('IB-B: minimum #heavy boundary images per Z', min(minB))
    ratios.sort(); print('best-lockless ratio -Lambda(T)/Lambda(Z) over lockless images: min', ratios[:3])
    pfail.sort(reverse=True); print('kind-matched model: sum_Z P(fail) = %.4f; max P(fail) %s' % (sum(p[0] for p in pfail), pfail[:3]))
    for x in pfail:
        if x[1] == 'p25#17650' and x[2] == 3: print('    p25#17650 h3:', x)
    print('heavy-landing by kind (images / heavy):', {k: (heavy[(k, 'images')], heavy[(k, 'heavy images')]) for k in ('N0', 'L1', 'L2', 'DL')})
    n = [x[0] for x in rows]
    print('correlation of #images on T with e_T %.3f, b_T %.3f, N0(T) %.3f, -Lambda(T) %.3f (pooled over %d rows); lockless images vs N0(T): %.3f' % (
        pearson(n, [x[1] for x in rows]), pearson(n, [x[2] for x in rows]), pearson(n, [x[3] for x in rows]), pearson(n, [x[4] for x in rows]), len(rows), pearson([x[5] for x in rows], [x[3] for x in rows])))
    tn0 = sum(x[3] for x in rows); print('images per N0 state (lockless images / N0 states, pooled): %.4f' % (sum(x[5] for x in rows) / max(1, tn0)))
