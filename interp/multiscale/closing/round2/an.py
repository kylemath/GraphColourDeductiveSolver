import json, collections, sys
rows=[json.loads(l) for l in open('s1.jsonl')]
by=collections.defaultdict(list)
for r in rows:
    if 'res' in r: by[r['F']].append(r)
    else: print('ERR', r)
print('F  splits closings  L(range)  R-hist  Wband-hist  maxR maxW  conf_changed(med,max) changed/L(max) conf_maxd(max) band_maxd(max)')
for F in sorted(by):
    rs=by[F]; res=[x for r in rs for x in r['res']]
    Ls=[r['L'] for r in rs]
    Rh=collections.Counter(x['R'] for x in res); Wh=collections.Counter(x['W_band'] for x in res)
    ch=sorted(x['conf_changed'] for x in res)
    rat=max(x['conf_changed']/r['L'] for r in rs for x in r['res'])
    print(F, len(rs), len(res), (min(Ls),max(Ls)), sorted(Rh.items()), sorted(Wh.items()), max(Rh), max(Wh), (ch[len(ch)//2], ch[-1]), round(rat,2),
          max(x['conf_maxd'] for x in res), max(x['band_maxd'] for x in res))
    for r in rs: print('   ', r['kind'], r['seed'], 'L', r['L'], 'os1', r['odd_seam1'], 'oddd', r['odd_d'], 'maxR', max(x['R'] for x in r['res']), 'maxW', max(x['W_band'] for x in r['res']), r['sec'])
