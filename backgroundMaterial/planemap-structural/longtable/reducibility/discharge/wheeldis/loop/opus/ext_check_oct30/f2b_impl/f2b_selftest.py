# exec'd inside st21's namespace (after SEPX with SEP_F2B is running).  Self-test of the 2-ball exclusion.
import random as _rn, collections as _co
def _cdelta(d, lk, sv):
    SEPX.stdin.write('f %d %s %s\n' % (d, lk, sv)); SEPX.stdin.flush(); return float(SEPX.stdout.readline())
def _pydelta(d, lk, sv):
    f2b.ACTIVE = True; a = spec_val(d, lk, sv); f2b.ACTIVE = False
    try: b = spec_val(d, lk, sv)
    finally: f2b.ACTIVE = True
    return a - b
_rg = _rn.Random(12345)
def _gen(g, rule):
    d = int(g[1]); p, wr, sr = rule; sg = int(g.split('_')[-1]) if g.count('_') == 2 else 0
    w = [_rg.choice('56789') for _ in range(d)]; s = [_rg.choice('56789') for _ in range(d)]
    if 'w7' in g: w[0] = '7'
    if 'w6' in g: w[0] = '6'
    for o, al in wr: w[o % d] = str(_rg.choice(sorted(al)))
    for o, v in sr: s[o % d] = str(v)
    if 'w7' in g:   # c = w_{i+sg}, a = s_i (sg = 1) / s_{i-1} (sg = -1) must be in {5,6} for the l3q row to exist
        c = sg % d; a = 0 if sg == 1 else d - 1
        if w[c] not in '56': w[c] = _rg.choice('56')
        if s[a] not in '56': s[a] = _rg.choice('56')
    return d, ''.join(w), ''.join(s)
_cases = []   # (kind, d, lk, sv)
for g in f2b.GROUPS:
    rl = f2b._R[g]
    if not rl: continue
    for rule in _rg.sample(rl, min(len(rl), 400)): _cases.append((g,) + _gen(g, rule))
for _ in range(1500):
    d = _rg.choice((7, 8, 9, 10)); _cases.append(('random', d, ''.join(_rg.choice('55666778') for _ in range(d)), ''.join(_rg.choice('55666778') for _ in range(d))))
_st = _co.defaultdict(lambda: [0, 0, 0.0, 0.0]); _bad = 0
for kind, d, lk, sv in _cases:
    pd, cd = _pydelta(d, lk, sv), _cdelta(d, lk, sv)
    st = _st[kind]; st[0] += 1; st[1] += abs(pd) > 1e-12; st[2] = max(st[2], abs(pd - cd)); st[3] = min(st[3], pd)
    if abs(pd - cd) > 1e-9: _bad += 1; _bad <= 5 and print('F2B-SELFTEST MISMATCH', kind, d, lk, sv, pd, cd)
print('F2B-SELFTEST python-vs-C++ correction on %d arrangements (kind: n, n with nonzero value change, max |py-C++|, most negative change):' % len(_cases))
for k, v in sorted(_st.items()): print('  %-9s n=%4d changed=%4d max|py-cpp|=%.2e min change=%.6f' % (k, v[0], v[1], v[2], v[3]))
print('F2B-SELFTEST mismatches: %d' % _bad, flush=True)
if _bad: fail('f2b selftest: C++ leaf correction differs from the python rows')
# explicit should / should-not match demonstration on single rules
def _show(g, k):
    rule = f2b._R[g][k]; p, wr, sr = rule; d, lk, sv = _gen(g, rule); w = [int(c) for c in lk]; s = [int(c) for c in sv]
    print('F2B-SELFTEST rule %s#%d: p_deg=%d w_req=%s s_req=%s' % (g, k, p, [(o, sorted(al)) for o, al in wr], list(sr)))
    ex = lambda ww, ss: (f2b.extra6(d, ww, ss, 0) if 'w6' in g else f2b.extra7(d, ww, ss, 0, int(g.split('_')[-1])))
    e1 = ex(w, s)
    m0 = pmask(min(d, 9), w[-2 % d], w[-1 % d], w[1], w[2 % d], s[-2 % d], s[-1 % d], s[0], s[1]) if 'w6' in g else None
    print('   matching arrangement  d=%d link %s s %s: extra mask %s (has p bit: %s); pmask %s -> %s' % (d, lk, sv, bin(e1), bool(e1 >> (p - 5) & 1), bin(m0) if m0 is not None else '-', bin(m0 & ~e1) if m0 is not None else '-'))
    print('   row value change (masked - unmasked) py %.9f, C++ %.9f' % (_pydelta(d, lk, sv), _cdelta(d, lk, sv)))
    # break the match: change one constrained letter to one not allowed
    for o, al in wr:
        bad = [x for x in range(5, 10) if x not in al]
        if not bad: continue
        w2 = list(w); w2[o % d] = bad[0]; e2 = ex(w2, s)
        print('   w_req offset %d changed to %d (not allowed): this rule no longer matches; extra mask %s (p bit still set by another rule: %s)' % (o, bad[0], bin(e2), bool(e2 >> (p - 5) & 1)))
        lk2 = ''.join(map(str, w2)); print('      value change py %.9f C++ %.9f' % (_pydelta(d, lk2, sv), _cdelta(d, lk2, sv))); break
    for o, v in sr:
        if o in (0, -1) : continue
        s2 = list(s); s2[o % d] = 5 if v != 5 else 6; e2 = ex(w, s2)
        print('   s_req offset %d changed %d -> %d: extra mask %s' % (o, v, s2[o % d], bin(e2))); break
for _g, _k in (('d7_w6', 0), ('d7_w6', 700), ('d8_w6', 300), ('d9_w6', 5), ('d7_w7_1', 3), ('d8_w7_-1', 3)):
    if len(f2b._R[_g]) > _k: _show(_g, _k)
