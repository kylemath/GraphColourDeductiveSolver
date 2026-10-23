import json, sys, collections, math
import numpy as np
rs = [json.loads(l) for l in open('walk.jsonl')]
print('| spec | n | status | fail n | peak cuts | peak abs t | nodd at peak cuts | final nodd | maxR | top-quartile steps | with non-increasing cand (pre-SAT) | chosen increased cuts | chosen increased abs t | ...although a non-increasing cand existed |')
print('|' + '---|'*14)
fit = collections.defaultdict(list)
for r in sorted(rs, key=lambda r: (r['spec'].split(':')[0][:4], r['n'], r['spec'])):
    W = r.get('walk') or []
    if not W: continue
    nc = np.array([w[2] for w in W]); tt = np.array([w[3] for w in W])
    thr = max(1, np.percentile(nc, 75)); top = [w for w in W if w[2] >= thr and w[6] is not None]
    ex = sum(1 for w in top if w[6] > 0)
    incc = sum(1 for w in top if w[2] > w[9]); inct = sum(1 for w in top if w[3] > w[10] + 1e-9)
    incboth_ex = sum(1 for w in top if (w[2] > w[9] or w[3] > w[10] + 1e-9) and w[6] > 0)
    ip = int(np.argmax(nc))
    print('| %s | %d | %s | %s | %d | %.2f | %d | %d | %d | %d | %d | %d | %d | %d |' % (r['spec'], r['n'], r['status'], (r['diag'] or {}).get('n', ''), nc.max(), tt.max(), W[ip][1], W[-1][1], r['maxR'], len(top), ex, incc, inct, incboth_ex))
    fam = r['spec'].split(':')[0].rstrip('0123456789_')
    fam = ''.join(c for c in r['spec'].split(':')[0] if not c.isdigit() and c != '_')
    key = (fam, 'greedy' if 'greedy=1' in r['spec'] else 'keep', r['spec'].split(':')[3])
    fit[key].append((r['n'], nc.max(), tt.max(), W[-1][1], r['status'] == 'ok'))
print()
print('| family / policy / variant | runs | ok | n range | peak cuts per run | peak abs t per run | slope log(peak cuts) vs log n | peak cuts / sqrt(n) | peak cuts / final nodd |')
print('|' + '---|'*9)
for k in sorted(fit):
    g = fit[k]; ns = np.array([x[0] for x in g]); pc = np.array([x[1] for x in g]); pt = np.array([x[2] for x in g]); no = np.array([max(1, x[3]) for x in g])
    sl = np.polyfit(np.log(ns), np.log(np.maximum(pc, 1)), 1)[0] if len(set(ns)) > 1 else float('nan')
    print('| %s | %d | %d | %d-%d | %s | %s | %.2f | %s | %s |' % ('/'.join(k), len(g), sum(x[4] for x in g), ns.min(), ns.max(), list(pc), [round(x, 1) for x in pt], sl,
          [round(a / math.sqrt(b), 2) for a, b in zip(pc, ns)], [round(a / b, 3) for a, b in zip(pc, no)]))
