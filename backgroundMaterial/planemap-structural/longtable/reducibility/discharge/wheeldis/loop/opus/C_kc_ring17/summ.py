"""C_kc_ring17: table of results.txt by row (from the w*.txt.rows maps) and D rate by ring."""
import re, collections, glob
res = {}
for l in open('results.txt'):
    m = re.search(r'^(w\d+) (\S+) r=(\d+) .*?\| (.*?) \| rss_MB=(\d+) wall_s=(\d+)', l)
    if not m: continue
    tag, nm, r, out, rss, wall = m.groups(); r = int(r)
    v = 'D' if 'D=true' in out else ('notD' if 'D=false' in out else 'budget')
    g = lambda k: (re.search(k + r'=(\d+)', out) or [None, '-'])[1]
    res[nm] = (tag, r, v, g('ext'), g('reached'), g('classes'), wall, rss)
print('| window | ring | verdict | ext | reached | classes | wall s | MB |'); print('|---|---|---|---|---|---|---|---|')
for nm, (tag, r, v, e, re_, c, w, mb) in sorted(res.items(), key=lambda x: x[1][0]): print('| %s `%s` | %d | %s | %s | %s | %s | %s | %s |' % (tag, nm, r, v, e, re_, c, w, mb))
byr = collections.defaultdict(collections.Counter)
for t in res.values(): byr[t[1]][t[2]] += 1
print('\nby ring:', {r: dict(c) for r, c in sorted(byr.items())})
for fn in sorted(glob.glob('w[1-4]_*.txt.rows')):
    for l in open(fn):
        f = l.split(); un = l.strip().split('=')[-1]; ws = [x for x in un.split(',') if x]
        st = [res[w][2] if w in res else 'queued' for w in ws]
        print(fn.split('.')[0], f[0], f[1], f[3][:30], 'r17-20 windows:', len(ws), dict(collections.Counter(st)))
