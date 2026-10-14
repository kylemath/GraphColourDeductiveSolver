"""Job 9 family analysis: which local second-ring patterns force D-reducibility among the tested 2-balls (rings <= 15)?
A window = consecutive y-degrees starting at a p or an s position (y_{2i} = p_i, y_{2i+1} = s_i), read in both
directions.  A window 'forces' if every tested 2-ball containing it is D-reducible.  Reports the minimal forcing
windows (no forcing sub-window) of length <= 5 with their support, and simple counts."""
import glob, collections, json
R = {}
for f in glob.glob('run9/part*.out'):
    for l in open(f):
        p = l.split()
        if 'D=' in l: R[p[0][1:]] = (int(p[1][2:]), p[6] == 'D=true')
def windows(w, L):
    out = set()
    for st in range(10):
        for d in (1, -1):
            seq = tuple(w[(st + d * k) % 10] for k in range(L))
            typ = 'p' if st % 2 == 0 else 's'
            # reading backwards from an s position starts at s, its predecessor is p: type sequence alternates anyway
            out.add((typ, ''.join(seq)))
    return out
stats = {}
for L in range(1, 6):
    cnt = collections.defaultdict(lambda: [0, 0])
    for w, (r, D) in R.items():
        for win in windows(w, L): cnt[win][0] += 1; cnt[win][1] += D
    stats[L] = cnt
forcing = {}
for L in range(1, 6):
    for win, (n, d) in stats[L].items():
        if n == d and n >= 5:
            typ, s = win
            # minimal: no proper sub-window (prefix/suffix) already forcing
            subs = [(typ, s[:-1]), ((('s' if typ == 'p' else 'p') if True else typ), s[1:])]
            if any(x in forcing for x in subs): continue
            forcing[win] = n
print('tested', len(R), 'D-reducible', sum(D for r, D in R.values()))
print('minimal forcing windows (type of first vertex, degrees), support >= 5:')
for (t, s), n in sorted(forcing.items(), key=lambda x: (len(x[0][1]), -x[1])):
    print('  %s:%s  in %d tested 2-balls, all D-reducible' % (t, s, n))
# single-letter info
for L in (1, 2):
    for win, (n, d) in sorted(stats[L].items()):
        print('  window', win, 'tested', n, 'D-red', d, '(%.0f%%)' % (100 * d / n))
json.dump({'%s:%s' % k: v for k, v in forcing.items()}, open('forcing_windows.json', 'w'))
