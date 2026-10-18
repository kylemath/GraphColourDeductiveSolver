"""Priority check: the single 7/27 binder row d=7 link 5675765 s 6577575 (out/wlp3_j28_13.txt)."""
import rsst_rows as R
d, lk, sv = 7, '5675765', '6577575'
w = [int(c) for c in lk]; s = [int(c) for c in sv]
for i in range(d):
    if w[i] == 5: print('sender w%d code (w_{i+1},s_i,s_{i-1},w_{i-1}) =' % i, w[(i+1)%d], s[i], s[(i-1)%d], w[(i-1)%d], ' 5-wheel (u,..):', [7, w[(i+1)%d], s[i], s[(i-1)%d], w[(i-1)%d]])
for mode in ('strict', 'relaxed', 'fixed'):
    host, adj = R.target(d, w, s, mode)
    h = R.hits(d, w, s, mode)
    print('mode', mode, 'hosts', sorted(map(str, host)), '-> %d RSST configs' % len(h))
    for i in h:
        p = R.P[i]
        for emb in R.allemb(host, adj, p, cap=3):
            print('   %s ring %d %s interior %d : %s' % (p['name'], p['ring'], p['kind'], len(p['deg']),
                  ' '.join('%s=%d' % (t if t == 'u' else '%s%d' % t, dg) for t, dg in sorted(emb.values(), key=str))))
print('completions of the two LP-free slots s1, s4 (relaxed mode, every letter):')
for a in range(5, 10):
    for b in range(5, 10):
        s2 = list(s); s2[1] = a; s2[4] = b
        h = R.hits(d, w, s2, 'relaxed')
        print('  s1=%d s4=%d: %s' % (a, b, ' '.join(R.P[i]['name'] for i in h) or 'RSST-free'))
