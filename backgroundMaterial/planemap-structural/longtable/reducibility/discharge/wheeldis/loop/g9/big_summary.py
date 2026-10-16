"""G9 probe 2 (exploratory): summary of big-centre (9..12) K=3 leaves: ring-1 words grouped by (#fives, #lone fives)
(a lone five = ring-1 five whose neighbours other than the centre all have degree <= 6), and kill families from the
defect_check2_9 status files (first check = existing registries, second = after the ring<=12 dfast batch)."""
import sys, os, ast, collections
WD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(os.path.dirname(WD), 'b8b')); from rings import Layered
def lone(sig):
    r = sig.split('|'); L = Layered(int(r[0]))
    for k in range(1, len(r)): L.add_ring([int(c) for c in r[k]])
    L.add_ring([6] * len(L.ring()))
    adj = collections.defaultdict(set)
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj[x].add(y); adj[y].add(x)
    f = [v for v in L.rings[1] if L.deg[v] == 5]
    return len(f), sum(1 for v in f if all(L.deg.get(y, 6) <= 6 for y in adj[v] if y != 0))
for c in (9, 10, 11, 12):
    st1 = {l.split()[2]: l.split()[0] for l in open('big_chk_c%d.status' % c)}
    grp = collections.Counter(); fam = collections.Counter(); words = collections.Counter()
    for line in open('big_chk2_c%d.status' % c):
        sig = line.split()[2][4:]; st = ast.literal_eval(line[line.index('{'):])
        nf, nl = lone(sig); grp[(nf, nl)] += 1; words[sig.split('|')[1]] += 1
        rc_c = any(st.get(k) for k in ('rcD@%d' % c, 'rcC@%d' % c)); bf_c = any(st.get(k) for k in ('bfD@%d' % c, 'bfC@%d' % c))
        rc_s = any(st.get(k) for k in st if k.startswith(('rcD@', 'rcC@')) and not k.endswith('@%d' % c))
        bf_s = any(st.get(k) for k in st if k.startswith(('bfD@', 'bfC@')) and not k.endswith('@%d' % c))
        w = any(st.get(k) for k in st if k[:2] in ('W7', 'W8') or k == 'C7')
        fam['rc at centre'] += rc_c; fam['B-fixed at centre'] += bf_c; fam['rc at a 7/8'] += rc_s; fam['B-fixed at a 7/8'] += bf_s; fam['7/8-wheel'] += w
        fam['ONLY B-fixed (no rc, no wheel)'] += (bf_c or bf_s) and not (rc_c or rc_s or w)
        fam['killed only after new ring<=12 dfast'] += st1[line.split()[2]] != 'killed'
    print('centre %d: leaves %d, distinct ring-1 words %d' % (c, sum(grp.values()), len(words)))
    print('  (#fives in ring 1, #lone fives): ' + ' '.join('%s:%d' % (k, v) for k, v in sorted(grp.items())))
    print('  kills (leaves with at least one D/C in family): ' + ', '.join('%s %d' % kv for kv in fam.items()))
