# completeness check (Studio, 3 Nov): Studio's own derived rule set (f2b_rulecheck.py DERIVE on the same forbidden set) must kill
# at least every letter the outside rules kill. Arrangements: each outside rule instantiated (its letters, random elsewhere,
# 3 per rule) + 3,000 random rows d = 7..9; every position and side compared (mask inclusion outside <= Studio).
import sys, os, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
src = open(os.path.join(W, 'out', 'job31', 'st21_check_f2b.py')).read()
a = src.index("F2BR = os.environ.get('F2B')"); b = src.index('# ================= 12.5: receiverR2 rows')
def matcher(path):
    os.environ['F2B'] = path; G = {'os': os, 'json': json, 'LET': (5, 6, 7, 8, 9), 'V6': False, 'FB': False, 'XO': False, 'fail': sys.exit, 'print': lambda *x, **k: None}
    exec(src[a:b], G); return G['f2b_extra'], G['F2BG']
RJ = os.path.join(HERE, 'in', 'gc', 'kill_upgraded', 'tierA', 'full2ball_extra_rules.json')
th, thG = matcher(RJ); us, usG = matcher(sys.argv[1])
print('outside rules %s; Studio rules %s' % ({k: len(v) for k, v in thG.items()}, {k: len(v) for k, v in usG.items()}))
rg = random.Random(7); cases = []; LET = (5, 6, 7, 8, 9)
for g, L in thG.items():
    d = g[1]
    for fw, fs, m in L:
        for _ in range(3):
            w = [rg.choice([l for l in LET if not (fw >> (5 * o + l - 5)) & 1]) for o in range(d)]
            s = [rg.choice([l for l in LET if not (fs >> (5 * o + l - 5)) & 1]) for o in range(d)]
            w[0] = 6 if g[0] == 'w6' else 7; cases.append((d, w, s))
for _ in range(3000):
    d = rg.choice((7, 8, 9)); cases.append((d, [rg.choice((5, 5, 6, 6, 6, 7, 7, 8)) for _ in range(d)], [rg.choice((5, 5, 6, 6, 6, 7, 7, 8)) for _ in range(d)]))
st = collections.Counter(); bad = []
for d, w, s in cases:
    for i in range(d):
        for g in ([('w6', d)] if d <= 9 else []) + ([('w7', d, 1), ('w7', d, -1)] if d in (7, 8) else []):
            x, y = th(d, w, s, i, g), us(d, w, s, i, g)
            st['cells'] += 1; st['outside nonzero'] += x != 0; st['studio nonzero'] += y != 0; st['studio kills more'] += (y & ~x) != 0
            if x & ~y: st['MISSING'] += 1; len(bad) < 10 and bad.append((g, d, ''.join(map(str, w)), ''.join(map(str, s)), i, x, y))
print('arrangements %d: %s' % (len(cases), dict(st)))
for b_ in bad: print('  outside kills a letter Studio does not:', b_)
