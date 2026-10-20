# s43 EXPLORATORY (not built, not specified): FAN=1 adds the fan class of a link-6 spoke (n1 = 6: s_{i+1}; n4 = 6: s_{i-2}).
# price "level 2P" = fy2 + the private of a 6 spoke next to the five
# (h1 when n1 = 6, h3 when n4 = 6; a 6 has one private, adjacent to both its apexes), against cert_q39n3A74L.
# Receiver cells: face t classes (fy2_cells) x, for every 6 at w_j next to a link five, the class of its private p_j,
# restricted to the classes that filt16's amask allows for that 6 (p_j is shared by the 6's two link neighbours).
B43 = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s43'
exec(open(B43 + '/pricer43.py').read().split("C = json.load(open(CERT))")[0])
import itertools, os
c2 = G['c2']; amask = G['amask']; LET = G['LET']
FAN = int(os.environ.get('FAN', '0'))
def key2p(n, h, fa=(2, 2)):
    if FAN:
        fm = (fa[0] if n[1] == 6 else 2, fa[1] if n[4] == 6 else 2)
        show = [True, n[1] in (5, 6), (n[1] == 5 and n[2] == 5) or (n[4] == 5 and n[3] == 5), n[4] in (5, 6), True]
        m = tuple(h[k] if show[k] else 2 for k in range(5))
        return min(tuple(n) + m + fm, (n[0], n[4], n[3], n[2], n[1]) + m[::-1] + fm[::-1])
    show = [True, n[1] in (5, 6), (n[1] == 5 and n[2] == 5) or (n[4] == 5 and n[3] == 5), n[4] in (5, 6), True]
    m = tuple(h[k] if show[k] else 2 for k in range(5))
    return min(tuple(n) + m, (n[0], n[4], n[3], n[2], n[1]) + m[::-1])
def sender_z(wd, bits):
    w = [int(c) for c in wd]; Hb = [int(c) for c in bits[:5]]; z = collections.Counter()
    sixes = [k for k in range(5) if w[k] == 6]; Fn = dict(zip(sixes, bits[5:]))
    for j in range(5):
        if w[j] >= 7: z[('z', key2p(tuple(w[(j + m) % 5] for m in range(5)), tuple(Hb[(j + m) % 5] for m in range(5)), (Fn.get((j + 1) % 5, 2), Fn.get((j + 4) % 5, 2))))] += 1
    return dict(z)
ctx = collections.defaultdict(list)
for (wd, co, bt) in OLDC: ctx[wd].append((tuple(map(str, bt)), tuple(sorted(co.items(), key=str)), sender_z(wd, [int(x) for x in bt if x != '|'])))
def recv_cells(d, w, s):
    U = min(d, 9); out = []
    six = sorted({j for i in range(d) if w[i] == 5 for j in ((i + 1) % d, (i - 1) % d) if w[j] == 6})
    pa = []
    for j in six:
        mk = amask(U, w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d])
        A_ = tuple(c for c in (0, 1) if any((mk >> k) & 1 and c2(LET[k]) == c for k in range(5))) or (0, 1); pa.append(A_)
    for cl, tau in G['fy2_cells'](d, w, s):
        for pc in itertools.product(*pa):
            P = dict(zip(six, pc)); z = collections.Counter()
            for i in range(d):
                if w[i] != 5: continue
                n = (U, w[(i + 1) % d], s[i], s[(i - 1) % d], w[(i - 1) % d])
                fc = i if (n[1] == 5 and n[2] == 5) else (i - 1) % d if (n[4] == 5 and n[3] == 5) else None
                h = (c2(w[(i + 2) % d]), c2(s[(i + 1) % d]) if n[1] == 5 else P.get((i + 1) % d, 2), tau[fc] if fc is not None else 2,
                     c2(s[(i - 2) % d]) if n[4] == 5 else P.get((i - 1) % d, 2), c2(w[(i - 2) % d]))
                z[('z', key2p(n, h, (c2(s[(i + 1) % d]), c2(s[(i - 2) % d]))))] += 1
            out.append(((cl or '-') + '/p' + ''.join('%d:%d' % x for x in P.items()), dict(z)))
    return out
C = json.load(open(CERT)); FACE = {('7766556', '6567566'), ('7766556', '6566576'), ('7766556', '6576576'), ('7665566', '6675676'), ('7665566', '6775676')}
rows = []; tco = Fraction(0)
for c in C:
    w = Fraction(c['w']).limit_denominator(10 ** 7); r = c['row']
    if r[0] == 'senderR2':
        lab = tuple(map(str, r[2])); L = ctx[r[1]]; mine = [x for x in L if x[0] == lab]; same = [x for x in L if x[1] == mine[0][1]]
        rows.append(('S', '%s %s' % (r[1], ''.join(lab)), w, [(''.join(x[0]), x[2]) for x in same], False)); tco += w
    elif r[0] == 'receiverR2':
        d, lk, sv = int(r[1]), r[2], r[3]
        rows.append(('R', '%d %s %s' % (d, lk, sv), w, recv_cells(d, [int(ch) for ch in lk], [int(ch) for ch in sv]), (lk, sv) in FACE)); tco -= w
for k, lab, w, opts, fc in rows:
    if k == 'R': print('  %s %-26s w=%-9s cells=%d%s %s' % (k, lab, w, len(opts), ' FACE' if fc else '', [o[0] for o in opts]))
src2 = open(B43 + '/pricer43.py').read(); body = src2[src2.index("keys = sorted("):]
exec(body)
