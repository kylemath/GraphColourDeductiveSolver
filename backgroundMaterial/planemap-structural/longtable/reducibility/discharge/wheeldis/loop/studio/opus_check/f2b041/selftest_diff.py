# f2b041 self-test diff (Studio, 3 Nov): rule-match masks of Opus's f2b.py (imported unchanged from opus_f2b_impl/, 0f78e528)
# vs Studio's f2b_extra (exec'd from out/job31/st21_check_f2b.py), at EVERY position and side of every arrangement:
# Studio's 6,000 (seed 41) + Opus's self-test cases (their _gen / Random(12345) sequence, replayed).
import sys, os, json, random, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
RJ = os.path.join(HERE, 'in', 'gc', 'kill_upgraded', 'tierA', 'full2ball_extra_rules.json')
sys.path.insert(0, os.path.join(HERE, 'opus_f2b_impl')); import f2b
print('opus f2b.load:', f2b.load(RJ))
src = open(os.path.join(W, 'out', 'job31', 'st21_check_f2b.py')).read()
a = src.index("F2BR = os.environ.get('F2B')"); b = src.index('# ================= 12.5: receiverR2 rows')
os.environ['F2B'] = RJ; os.environ.pop('F2BHALF', None)
G = {'os': os, 'json': json, 'LET': (5, 6, 7, 8, 9), 'V6': False, 'FB': False, 'XO': False, 'fail': lambda m: sys.exit('FAIL ' + m)}
exec(src[a:b], G); f2b_extra = G['f2b_extra']; F2BG = G['F2BG']
print('studio groups:', {k: len(v) for k, v in F2BG.items()})
cases = []
# (1) Studio's 6,000 (same code as st21_check_f2b.py's self-test generator, seed 41)
_rr = random.Random(41); _gl = [(g_, r_) for g_, L_ in F2BG.items() for r_ in L_]; LET = (5, 6, 7, 8, 9)
for _ in range(6000):
    g_, (fw_, fs_, m_) = _gl[_rr.randrange(len(_gl))] if _gl and _rr.random() < 0.85 else (None, (0, 0, 0))
    d = g_[1] if g_ else _rr.choice((7, 8, 9))
    w_ = [_rr.choice([l_ for l_ in LET if not (fw_ >> (5 * o_ + l_ - 5)) & 1]) for o_ in range(d)]
    s_ = [_rr.choice([l_ for l_ in LET if not (fs_ >> (5 * o_ + l_ - 5)) & 1]) for o_ in range(d)]
    if g_: w_[0] = 6 if g_[0] == 'w6' else 7
    if _rr.random() < 0.3: w_[_rr.randrange(1, d)] = _rr.choice(LET)
    k_ = _rr.randrange(d); cases.append(('studio', d, w_[k_:] + w_[:k_], s_[k_:] + s_[:k_]))
# (2) Opus's self-test cases: their _gen and sampling order (f2b_selftest.py, 7fb0a323), replayed
_rg = random.Random(12345)
def _gen(g, rule):
    d = int(g[1]); p, wr, sr = rule; sg = int(g.split('_')[-1]) if g.count('_') == 2 else 0
    w = [_rg.choice('56789') for _ in range(d)]; s = [_rg.choice('56789') for _ in range(d)]
    if 'w7' in g: w[0] = '7'
    if 'w6' in g: w[0] = '6'
    for o, al in wr: w[o % d] = str(_rg.choice(sorted(al)))
    for o, v in sr: s[o % d] = str(v)
    if 'w7' in g:
        c = sg % d; a = 0 if sg == 1 else d - 1
        if w[c] not in '56': w[c] = _rg.choice('56')
        if s[a] not in '56': s[a] = _rg.choice('56')
    return d, ''.join(w), ''.join(s)
for g in f2b.GROUPS:
    rl = f2b._R[g]
    if not rl: continue
    for rule in _rg.sample(rl, min(len(rl), 400)): d, lk, sv = _gen(g, rule); cases.append(('opus:' + g, d, [int(c) for c in lk], [int(c) for c in sv]))
for _ in range(1500):
    d = _rg.choice((7, 8, 9, 10)); cases.append(('opus:random', d, [int(_rg.choice('55666778')) for _ in range(d)], [int(_rg.choice('55666778')) for _ in range(d)]))
st = collections.defaultdict(lambda: [0, 0, 0, 0]); bad = []
for kind, d, w, s in cases:
    k = kind.split(':')[0] if kind.startswith('studio') else kind
    for i in range(d):
        cells = []
        if 7 <= d <= 9: cells.append(('w6', f2b.extra6(d, w, s, i), f2b_extra(d, w, s, i, ('w6', d))))
        if d in (7, 8):
            for sg in (1, -1): cells.append(('w7%+d' % sg, f2b.extra7(d, w, s, i, sg), f2b_extra(d, w, s, i, ('w7', d, sg))))
        for nm, o_, s_ in cells:
            x = st[k]; x[0] += 1; x[1] += o_ != 0; x[2] += o_ != s_
            if o_ != s_: bad.append((kind, d, ''.join(map(str, w)), ''.join(map(str, s)), i, nm, o_, s_))
    st[k][3] += 1
print('arrangements: %d (studio 6000, opus %d)' % (len(cases), len(cases) - 6000))
for k, v in sorted(st.items()): print('  %-14s arrangements %5d  cells %7d  nonzero %6d  differing %d' % (k, v[3], v[0], v[1], v[2]))
print('TOTAL differing cells: %d' % len(bad))
for b_ in bad[:20]: print('  DIFF', b_)
