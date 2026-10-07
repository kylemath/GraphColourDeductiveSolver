"""NightStatementC: summary of cls-*.json."""
import json, sys
from collections import Counter
def q(v): v = sorted(v); return 'min %s  med %s  max %s' % tuple(round(x, 3) if isinstance(x, float) else x for x in (v[0], v[len(v) // 2], v[-1]))
for fn in sys.argv[1:]:
    R = json.load(open(fn)); print('=====', fn, 'classes with a Gamma-cycle:', len(R))
    print('class size N:', q([r['N'] for r in R]), '| #cycles:', q([r['ncyc'] for r in R]), '| #Gamma:', q([r['nGamma'] for r in R]))
    print('floor F/N:', q([r['F'] / r['N'] for r in R]), '| sumLam <= 0:', sum(r['sumLam'] <= 0 for r in R))
    print('M = most negative cycle: Lam', q([r['M']['Lam'] for r in R]), ' L', q([r['M']['L'] for r in R]))
    print('  M is the longest cycle:', sum(r['M_is_longest'] for r in R), '/', len(R))
    print('  phiN = L(M)/N:', q([r['phiN'] for r in R]))
    print('  phiU = U(M)/U:', q([r['phiU'] for r in R]))
    print('  phiF = F(M)/F:', q([r['phiF'] for r in R]), '| phiF >= 1/2:', sum(r['phiF'] >= .5 for r in R))
    print('  M share of negative mass:', q([r['Mshare_neg'] for r in R]))
    print('Star(ii) -Lam(M) >= positive mass:', sum(r['star'] for r in R), '/', len(R), '| posmass', q([r['posmass'] for r in R]), '| ratio -Lam(M)/posmass', q([-r['M']['Lam'] / r['posmass'] for r in R]))
    for t in ('20', '100', '1000'):
        print('heavy (Lam <= -%s): #cycles' % t, q([r['nheavy'][t] for r in R]), ' unfilled share', q([r['hU'][t] for r in R]))
    print('credit-free transport, all sigma-edges:', sum(r['flow_sigma'] for r in R), '/', len(R), '| only (c)-edges:', sum(r['flow_c'] for r in R))
    P = [(r, z) for r in R for z in r['pos']]; G = [(r, z) for r, z in P if z['gamma']]; NG = [(r, z) for r, z in P if not z['gamma']]
    for lab, S in (('Gamma', G), ('non-Gamma positive', NG)):
        if not S: continue
        print('--', lab, 'cycles:', len(S), ' L', dict(Counter(z['L'] for r, z in S).most_common(6)))
        print('   (c):', sum(z['c'] for r, z in S), ' (c_M) some image on M:', sum(z['cM'] for r, z in S))
        print('   #images off Z:', q([z['noff'] for r, z in S]), '| on heavy T:', q([z['heavy'] for r, z in S]), '| on M:', q([z['onM'] for r, z in S]))
        print('   heavy-image share h = heavy/noff:', q([z['heavy'] / z['noff'] for r, z in S if z['noff']]), ' vs class unfilled share on Lam<=-Lam(Z) cycles (t=20):', q([r['hU']['20'] for r, z in S]))
        print('   #distinct target cycles:', q([z['distinct'] for r, z in S]))
        # pigeonhole: expected misses if images were uniform over unfilled states
        import math
        print('   min over Z of #heavy images:', min(z['heavy'] for r, z in S), '; Z with heavy <= 3:', [(r['tag'], r['orientation'], z['L'], z['Lam'], z['heavy'], z['noff']) for r, z in S if z['heavy'] <= 3][:8])
        print('   kinds of images on M (sum):', dict(sum((Counter(z['kinds_onM']) for r, z in S), Counter())))
print('\n===== margins')
for fn in sys.argv[1:]:
    R = json.load(open(fn)); S = [(r, z) for r in R for z in r['pos']]
    m = sorted(((-z['heavy_cycles'][0] / z['Lam']) if z['heavy_cycles'] else 0, r['tag'], r['orientation'], z['L'], z['Lam'], z['heavy'], z['noff'], z['onM'], r['M']['Lam'], r['nheavy']['20']) for r, z in S)
    print(fn, 'margin m(Z) = max -Lam(T)/Lam(Z) over sigma-images: lowest five:'); [print('   ', x) for x in m[:5]]
    d = [z['heavy'] / z['noff'] - r['hU']['20'] for r, z in S if z['noff']]
    print('  paired enrichment h(Z) - hU(class): ', q(d), ' #negative:', sum(x < 0 for x in d), '/', len(d))
    print('  #light images (Lam(T) > -Lam(Z)) per Z:', q([z['noff'] - z['heavy'] for r, z in S]))
    st = sorted((-r['M']['Lam'] / r['posmass'], r['tag'], r['orientation'], r['M']['Lam'], r['posmass'], r['npos'], r['N'], r['F']) for r in R)
    print('  Star ratio lowest three:'); [print('   ', x) for x in st[:3]]
    nm = [(r['tag'], r['orientation'], z['L'], z['heavy'], z['noff'], r['M']['Lam'], r['top5'][:3]) for r, z in S if not z['cM']]
    print('  (c) without M:', len(nm)); [print('   ', x) for x in nm[:6]]
