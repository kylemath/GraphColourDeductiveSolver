# s86: mrow summary of a dualexport JSON: |w| by mrow type, by signature (summed over keys), top signatures with their top keys.
# usage: python3 -I mrowsum.py <dual_rows.json> [top]
import json, sys, collections
J = json.load(open(sys.argv[1])); R = J['rows']; top = int(sys.argv[2]) if len(sys.argv) > 2 else 25
tot = sum(abs(r['w']) for r in R)
by_t = collections.defaultdict(lambda: [0.0, 0]); by_s = collections.defaultdict(lambda: [0.0, 0, []])
for r in R:
    if not r['type'].startswith('mrow'): continue
    by_t[r['type']][0] += abs(r['w']); by_t[r['type']][1] += 1
    k = (r['type'], tuple(r['sig'])); by_s[k][0] += abs(r['w']); by_s[k][1] += 1; by_s[k][2].append((abs(r['w']), r['key']))
print('# MROWS of %s (total |w| %.6f)' % (sys.argv[1].split('/')[-1], tot))
print('# stamp: %s' % J.get('stamp', '')[:200])
for t, (w, n) in sorted(by_t.items(), key=lambda kv: -kv[1][0]): print('# %-7s %5d rows  |w| %.6f (%.1f%%)  %d signatures' % (t, n, w, 100 * w / tot, sum(1 for k in by_s if k[0] == t)))
print('# rank  type    signature                      keys  sum|w|    %%tot  top keys (|w|)')
cum = 0.0
for i, ((t, sg), (w, n, ks)) in enumerate(sorted(by_s.items(), key=lambda kv: -kv[1][0])[:top]):
    cum += w; ks.sort(key=lambda x: -x[0])
    print('%4d  %-7s %-30s %4d  %.6f  %5.1f  %s' % (i + 1, t, list(sg), n, w, 100 * w / tot, '; '.join('%s %.4f' % (k, a) for a, k in ks[:3])))
