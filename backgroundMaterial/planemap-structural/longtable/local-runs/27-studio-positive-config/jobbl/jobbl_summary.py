#!/usr/bin/env python3
"""Job BL summary from out/bl{adv,c12,c24..c27}{,m}.jsonl (picyc.bl --jobbl). Key = 'R<type> <degree word from x_j> <fixed|DL|notDL>'."""
import json, itertools, sys
from collections import Counter, defaultdict
def canon(w):
    d = [int(c) for c in w]; return ''.join(map(str, min(tuple(s[r:] + s[:r]) for s in (d, d[::-1]) for r in range(5))))
for group, tags in (('census orders 12-27', ['c12', 'c24', 'c25', 'c26', 'c27']), ('adversarial (61 AW hits, AS, AQ)', ['adv'])):
    S = Counter(); G = []
    for t in tags:
        for suf in ('', 'm'):
            try: fh = open('../out/bl%s%s.jsonl' % (t, suf))
            except FileNotFoundError: print('missing', t, suf); continue
            for l in fh:
                if '"jobbl"' not in l: continue
                r = json.loads(l); b = r['jobbl']
                for k, v in b['states'].items(): S[tuple(k.split())] += v
                for w, L, nd, vis in b['gamma']: G.append((r['name'], r['hole'], suf or 'plantri', r['pattern'], w, L, nd, vis))
    print('=' * 30, group)
    for ty in ('R3', 'R1', 'R2', 'R0'):
        tot = Counter(); bypat = defaultdict(Counter)
        for (t, wd, oc), v in S.items():
            if t != ty: continue
            tot[oc] += v; bypat[canon(wd)][(wd, oc)] += v
        if not tot: continue
        print('%s DL states: %s' % (ty, dict(tot)))
        print('  (1) per pattern and degree word (x_j..x_{j+4}): DL-image count / states  [words with DL images only, plus pattern totals]')
        for p in sorted(bypat):
            words = sorted({wd for wd, _ in bypat[p]}); tdl = sum(v for (wd, oc), v in bypat[p].items() if oc == 'DL'); tn = sum(bypat[p].values())
            line = ' '.join('%s:%d/%d' % (wd, bypat[p][(wd, 'DL')], sum(bypat[p][(wd, o)] for o in ('DL', 'notDL', 'fixed'))) for wd in words if bypat[p][(wd, 'DL')])
            print('    %-6s DL images %7d of %9d   %s' % (p, tdl, tn, line[:400]))
        # (3) minimal degree-5 conditions guaranteeing a non-DL (or fixed) image
        best = []
        for k in range(0, 6):
            for sub in itertools.combinations(range(5), k):
                dl = sum(v for (t, wd, oc), v in S.items() if t == ty and oc == 'DL' and all(wd[i] == '5' for i in sub))
                cov = sum(v for (t, wd, oc), v in S.items() if t == ty and all(wd[i] == '5' for i in sub))
                if dl == 0 and not any(set(b[0]) <= set(sub) for b in best): best.append((sub, cov))
        print('  (3) minimal sets S of positions i with "deg x_{j+i} = 5 for i in S" giving 0 DL images (S, states covered):', best[:12])
    nd0 = [g for g in G if g[6] == 0]
    print('(2) all-DL pi-orbits: %d; with no non-DL sigma-image: %d %s' % (len(G), len(nd0), nd0[:10]))
    print('    min #non-DL images per orbit by pattern:', {p: min(g[6] for g in G if g[3] == p) for p in sorted({g[3] for g in G})})
