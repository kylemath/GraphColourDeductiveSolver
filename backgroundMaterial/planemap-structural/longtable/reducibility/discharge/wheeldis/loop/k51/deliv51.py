"""EXPLORE round 51: Studio delivery of the sender-window kills (Studio, 11:49Z).  Renames p5_ -> s5_ (p means
something else in the receiver registry), and writes, per two-engine kill (twoeng on loop/k51/F_*), the kc line under
the new name and the frame map: for each interior vertex of the kc line, in kc-line vertex order, its sender slot
(v, w_k, s_k, f_k).  The windows are regenerated from family.json exactly as fam51 builds them, and each regenerated
kc line is checked against the run's (F_res.txt).
usage: python3 deliv51.py FAMILY TWOENG_D   -> sender_kills51.txt"""
import sys, os, itertools
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import fam51 as F
FAM, TD = sys.argv[1], sys.argv[2]
want = {l.split()[0] for l in open(TD) if l.startswith('p5_') and 'D=true' in l}
res = {}
for l in open(os.path.join(H, 'F_res.txt')):
    f = l.rstrip('\n').split(' ', 2)
    if len(f) == 3: res.setdefault(f[0], (f[1], f[2]))
slot = lambda x: 'v' if x == ('u',) else 'w%d' % x[1] if x[0] == 'w' else 's%d' % x[1] if x[0] == 's' else 'f%d' % x[1]
got = {}
for m in F.load(FAM):
    slots, cs = F.cases(m)
    for deg in cs:
        r2 = {x: v for x, v in deg.items() if x[0] in 'sp'}
        adj, name, _ = F.build(m['word'], r2); inv = {v: x for x, v in name.items()}
        for w in F.windows(m['word'], deg, 18, {}):
            nm = w[3]
            if nm not in want or nm in got: continue
            got[nm] = (w[4], m, deg)
out = []
for nm in sorted(want):
    line, m, deg = got[nm]
    assert res[nm][1] == line.split(' ', 1)[1], nm
    r2 = {x: v for x, v in deg.items() if x[0] in 'sp'}
    adj, name, _ = F.build(m['word'], r2); inv = {v: x for x, v in name.items()}
    # the interior: the vertex set whose name is nm (names are injective on vertex sets)
    V = sorted(deg, key=lambda x: inv[x]); hit = None
    for k in range(2, len(V) + 1):
        for S in itertools.combinations(V, k):
            if F.wname(frozenset(S), deg, m['word']) == nm: hit = S; break
        if hit: break
    fm = [slot(x) for x in sorted(hit, key=lambda x: inv[x])]
    assert len(fm) == int(line.split()[2]), nm
    out.append('%s %s | frame %s | dfast+kc D | first seen in context %s' % ('s5_' + nm[3:], line.split(' ', 1)[1], ','.join(fm), m['id'].replace(' ', ':')))
open(os.path.join(H, 'sender_kills51.txt'), 'w').write(
    '# round 51 sender-window kills (two-engine D), s5_ names; frame = sender slot of each interior vertex in kc order\n' +
    ''.join(l + '\n' for l in out))
print(len(out), 'of', len(want))
