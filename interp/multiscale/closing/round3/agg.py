import json, collections
by = collections.defaultdict(list)
for l in open('s3.jsonl'):
    r = json.loads(l)
    if 'res' in r: by[r['F']].append(r)
for F in sorted(by):
    rs = by[F]; R = collections.Counter(x.get('R') for r in rs for x in r['res']); W = collections.Counter(x.get('W_band') for r in rs for x in r['res'])
    ch = [x.get('conf_changed', 0)/r['L'] for r in rs for x in r['res']]
    print(F, 'splits', len(rs), 'L', sorted(r['L'] for r in rs), 'N', sum(R.values()), 'R', sorted(R.items()), 'W', sorted(W.items()),
          'maxR', max(k for k in R if k is not None), 'P(R>=3)=%.3f' % (sum(v for k, v in R.items() if k and k >= 3)/sum(R.values())),
          'max chg/L %.2f' % max(ch), 'odd_d', [r['odd_d'][0] for r in rs])
