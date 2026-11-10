#!/usr/bin/env python3
"""ST-120 B2 follow-up: cross-check of the 79 parts (71 + N2 of RSSTFP_SPEC_v2.md 122da06a §16.2).

Reference = rcore.py (out/job_RSST1SHOT/code, spec-only engine) extended here by N2, written independently of
gen_rules_n2.py from the §16.2 table grammar (`spoke[hat]`, `=k`, `*`), mirrored with rcore.mirror / rcore.psub.
No W6r code is read or run.

  python3 -I crosscheck_n2.py gen    -> cases_n2.txt, expected_n2.json
  ./run.sh RSSTCheckN2               -> lean_out_n2.txt, lean_parts_n2.txt
  python3 -I crosscheck_n2.py cmp    -> crosscheck_n2.log
  python3 -I crosscheck_n2.py cplus  -> cplus_n2.log: §16.4 tail table (max c+ per hub letter, Karp max mean),
                                        71 vs 79 parts, at d >= 9 (u reads 9)

Cases: the 2,576 windows of cases.txt (re-run with 79 parts), plus N2 plants (each of the 8 parts planted at hub u
(d = 7) and at a hub w_i with target u (d = 8 for g2 = 8, d = 9..12 for g2 = 9) on random backgrounds), plus near
misses (one constrained letter of a plant moved by 1, or u's degree moved across g2)."""
import os, sys, json, random, re, collections, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
WHEELDIS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(WHEELDIS, 'out', 'job_RSST1SHOT', 'code'))
import rcore as R  # noqa: E402

FULL = R.FULL
SEED = 20261111
PAIRS = [(9, 7), (9, 8), (9, 9), (8, 8)]
N2_ROW = '=6 =5[=5] g2 =6 =6[=5] g5 =5'      # §16.2, hub 7, target position 2

def tok_range(t):
    if t == '*': return FULL
    m = re.fullmatch(r'=([5-9])', t)
    if m: return (int(m.group(1)),) * 2
    m = re.fullmatch(r'>=([5-9])', t)
    if m: return (int(m.group(1)), 9)
    raise ValueError(t)

def parse_row(row):
    subs = []
    for t in row.split():
        m = re.fullmatch(r'([^\[\]]+)(?:\[([^\]]+)\])?', t)
        sp = tok_range(m.group(1)); hat = tok_range(m.group(2)) if m.group(2) else FULL
        fans = (FULL,) * (sp[0] - 5) if sp[0] == sp[1] and 6 <= sp[0] <= 8 else ()   # §3.1 padding
        subs.append((sp, hat, fans))
    return subs

def n2_parts():
    out = []
    for g2, g5 in PAIRS:
        p = parse_row(N2_ROW.replace('g2', '=%d' % g2).replace('g5', '=%d' % g5))
        tag = 'N2_%d%d' % (g2, g5)
        out.append((tag, p))
        mp = R.mirror(p)
        if not R.psub(mp, p): out.append((tag + 'm', mp))
    return out

N2 = n2_parts()
assert len(N2) == 8
R.PARTS.extend(N2)                 # rcore.instances reads R.PARTS at call time
N2TAGS = {t for t, _ in N2}

def npriv(L): return R.npriv(L)

def ref(d, link, apex, priv):
    W = R.Window(d, link, apex); insts = R.instances(W)
    f = {'p%d.%d' % (i, j + 1): priv[i][j] for i in range(d) for j in range(npriv(link[i]))}
    lo, hi, fired = R.ledger(d, insts, f)
    return lo, hi, collections.Counter((I['tag'], I['hub'], I['target'], bool(s)) for I, s in fired), \
        sum(1 for I in insts if I['open'])

# ------------------------------------------------------------------ plants
def pick(rnd): return rnd.choices([5, 6, 7, 8, 9], [40, 25, 15, 10, 10])[0]

def resize(link, priv, rnd):
    for i, L in enumerate(link):
        k = npriv(L); priv[i] = (priv[i] + [pick(rnd) for _ in range(k)])[:k]

def constrained_vertices(d, link, apex, hub, a, part):
    """[(vertex, required letter)] for an all-exact part at hub h, anchor a (rcore geometry)."""
    W = R.Window(d, link, apex); S = W.rot[hub]; n = len(part); out = []
    assert len(S) == n
    for j, (sp, hat, fans) in enumerate(part):
        x, xp = S[(a + j) % n], S[(a + j - 1) % n]
        if sp != FULL: out.append((x, sp[0]))
        if hat != FULL: out.append((W.succ(x, xp), hat[0]))
        assert all(f == FULL for f in fans)
    return out

def setv(d, link, apex, priv, v, L):
    if v == 'u': return min(d, 9) == L
    if v[0] == 'w': link[v[1]] = L
    elif v[0] == 's': apex[v[1]] = L
    elif v[0] == 'p': priv[v[1]][v[2] - 1] = L
    else: raise ValueError(v)
    return True

def plant(rnd, part, where):
    tag, p = part; g2 = p[2][0][0]
    if where == 'u':
        d = 7; hub = 'u'; a = rnd.randrange(7)
    else:
        d = 8 if g2 == 8 else rnd.randint(9, 12)
        i = rnd.randrange(d); hub = ('w', i); a = 5
    link = [pick(rnd) for _ in range(d)]; apex = [pick(rnd) for _ in range(d)]
    if hub != 'u': link[hub[1]] = 7
    priv = [[] for _ in range(d)]; resize(link, priv, rnd)
    for _ in range(4):
        for v, L in constrained_vertices(d, link, apex, hub, a, p):
            assert setv(d, link, apex, priv, v, L), (tag, v, L)
        resize(link, priv, rnd)
    cons = constrained_vertices(d, link, apex, hub, a, p)
    W = R.Window(d, link, apex)
    f = {'p%d.%d' % (i, j + 1): priv[i][j] for i in range(d) for j in range(npriv(link[i]))}
    ok = [I for I in R.instances(W) if I['tag'] == tag and I['hub'] == ('u' if hub == 'u' else 'w%d' % hub[1])
          and I['anchor'] == a and R.holds(I, f) and not I['open']]
    assert ok, (tag, where, d, link, apex, priv)
    return d, link, apex, priv, hub, a, cons

def gen():
    rnd = random.Random(SEED)
    cases = []
    for line in open(os.path.join(HERE, 'cases.txt')):
        cid, d, lk, ap, pv = line.rstrip('\n').split(';')
        cases.append((cid, int(d), [int(c) for c in lk], [int(c) for c in ap], [[int(c) for c in z] for z in pv.split(',')], 'old'))
    for part in N2:
        for where in ('u', 'w'):
            for t in range(15):
                d, link, apex, priv, hub, a, cons = plant(rnd, part, where)
                base = 'n2p_%s_%s_%d' % (part[0], where, t)
                cases.append((base, d, link, apex, priv, 'plant'))
                movable = [(v, L) for v, L in cons if v != 'u']
                for k, (v, L) in enumerate(rnd.sample(movable, 2)):
                    L2 = L + rnd.choice([-1, 1])
                    if not 5 <= L2 <= 9: L2 = L - (L2 - L)
                    lk2, ap2, pv2 = list(link), list(apex), [list(z) for z in priv]
                    setv(d, lk2, ap2, pv2, v, L2); resize(lk2, pv2, rnd)
                    cases.append(('n2m_%s_%s_%d_%d' % (part[0], where, t, k), d, lk2, ap2, pv2, 'near'))
                if where == 'w':                 # u's letter moved across g2: 8 <-> 9+
                    g2 = part[1][2][0][0]; d2 = 9 if g2 == 8 else 8
                    i = hub[1] % d2
                    lk2 = (link + [pick(rnd) for _ in range(d2)])[:d2]; ap2 = (apex + [pick(rnd) for _ in range(d2)])[:d2]
                    pv2 = ([list(z) for z in priv] + [[] for _ in range(d2)])[:d2]; resize(lk2, pv2, rnd)
                    cases.append(('n2d_%s_%d' % (part[0], t), d2, lk2, ap2, pv2, 'near'))
    with open(os.path.join(HERE, 'cases_n2.txt'), 'w') as fh:
        for cid, d, link, apex, priv, _ in cases:
            fh.write('%s;%d;%s;%s;%s\n' % (cid, d, ''.join(map(str, link)), ''.join(map(str, apex)),
                                          ','.join(''.join(map(str, z)) for z in priv)))
    exp = {}
    for cid, d, link, apex, priv, kind in cases:
        lo, hi, c, nopen = ref(d, link, apex, priv)
        exp[cid] = {'kind': kind, 'lo': lo, 'hi': hi, 'nopen': nopen, 'fits': [[list(k), n] for k, n in sorted(c.items())]}
    json.dump(exp, open(os.path.join(HERE, 'expected_n2.json'), 'w'), separators=(',', ':'))
    print('wrote %d cases (%s)' % (len(cases), dict(collections.Counter(c[5] for c in cases))))

def parse_out(fn):
    out = {}
    for line in open(os.path.join(HERE, fn)):
        f = line.split()
        if not f: continue
        c = collections.Counter()
        for z in f[6:]:
            m = re.fullmatch(r'(.+)@(u|w\d+)>(u|w\d+):([SO])', z)
            c[(m.group(1), m.group(2), m.group(3), m.group(4) == 'S')] += 1
        out[f[0]] = {'lo': int(f[1]), 'hi': int(f[2]), 'nopen': int(f[3]), 'dis5': int(f[4]), 'dis9': int(f[5]), 'fits': c}
    return out

def cmp():
    log = open(os.path.join(HERE, 'crosscheck_n2.log'), 'w')
    def P(s): print(s); log.write(s + '\n')
    P('# ST-120 B2 N2 cross-check: Lean RSSTCheckN2 (rsstParts79) vs rcore + independent N2 (RSSTFP_SPEC_v2 122da06a §16.2)')
    lp = [l.rstrip('\n') for l in open(os.path.join(HERE, 'lean_parts_n2.txt')) if l.strip()]
    rp = R.parts_text(N2)
    P('N2 parts: lean %d, reference %d, identical %s' % (len(lp), len(rp), lp == rp))
    for a, b in zip(lp, rp):
        P('  %s%s' % (a, '' if a == b else '   <> reference ' + b))
    exp = json.load(open(os.path.join(HERE, 'expected_n2.json')))
    L = parse_out('lean_out_n2.txt'); OLD = parse_out('lean_out.txt')
    tot = collections.Counter(); bad = collections.Counter(); n2f = collections.Counter(); casesn2 = collections.Counter()
    oldbad = 0; changed = 0
    for cid, e in exp.items():
        k = e['kind']; tot[k] += 1
        m = L.get(cid)
        if m is None: bad[k] += 1; P('MISSING %s' % cid); continue
        errs = []
        rc = collections.Counter({tuple(a): n for a, n in e['fits']})
        if (m['lo'], m['hi']) != (e['lo'], e['hi']): errs.append('lo/hi lean %s ref %s' % ((m['lo'], m['hi']), (e['lo'], e['hi'])))
        if m['fits'] != rc: errs.append('fits lean-only %s ref-only %s' % (list((m['fits'] - rc).elements())[:5], list((rc - m['fits']).elements())[:5]))
        if m['nopen'] != e['nopen']: errs.append('open lean %d ref %d' % (m['nopen'], e['nopen']))
        if m['dis5'] or m['dis9']: errs.append('bool/tri disagreement %d/%d' % (m['dis5'], m['dis9']))
        nn = sum(v for (t, *_), v in m['fits'].items() if t in N2TAGS)
        n2f[k] += nn; casesn2[k] += nn > 0
        if k == 'old':          # 79-part run = 71-part run + N2 fits only
            o = OLD[cid]; non = collections.Counter({kk: v for kk, v in m['fits'].items() if kk[0] not in N2TAGS})
            delta_lo = sum(v * (1 if kk[2] == 'u' else -1) for kk, v in m['fits'].items() if kk[0] in N2TAGS and kk[3])
            delta_hi = sum(v * (1 if kk[2] == 'u' else -1) for kk, v in m['fits'].items() if kk[0] in N2TAGS)
            if non != o['fits'] or (m['lo'] - o['lo'], m['hi'] - o['hi']) != (delta_lo, delta_hi):
                errs.append('differs from the 71-part run outside N2'); oldbad += 1
            changed += (m['lo'], m['hi']) != (o['lo'], o['hi'])
        if errs: bad[k] += 1; P('MISMATCH %s: %s' % (cid, '; '.join(errs)))
    pl = [cid for cid, e in exp.items() if e['kind'] == 'plant']
    planted_hit = sum(1 for cid in pl if any(kk[0] == re.match(r'n2p_(N2_\d\dm?)_', cid).group(1) and v for kk, v in L[cid]['fits'].items()))
    for k in ('old', 'plant', 'near'):
        P('%-5s cases %5d  cases with an N2 fit %4d  N2 fits %4d  mismatches %d' % (k, tot[k], casesn2[k], n2f[k], bad[k]))
    P('old windows: 79-part output = 71-part lean_out.txt + N2 fits only: %d differ; lo/hi changed in %d' % (oldbad, changed))
    P('plants: %d of %d fire their planted part (Lean)' % (planted_hit, len(pl)))
    P('TOTAL cases %d, mismatches %d' % (sum(tot.values()), sum(bad.values())))

# ------------------------------------------------------------------ §16.4 tail table: c+ and Karp
def cplus_window(Lw, parts_filter):
    """c+ at hub w_2 of a d = 9 window with link letters L_0..L_4 = Lw (others 5), apexes and privates free:
    max over the variables of the number of possible fits from w_2 into u."""
    d = 9; link = list(Lw) + [5] * 4
    if link[2] > 8: return 0
    W = R.Window(d, link, None)
    ins = [I for I in R.instances(W) if I['hub'] == 'w2' and parts_filter(I['tag'])]
    if not ins: return 0
    vs = sorted({v for I in ins for v in I['conds']})
    best = 0
    def dfs(k, alive):
        nonlocal best
        if len(alive) <= best: return
        if k == len(vs): best = len(alive); return
        v = vs[k]
        for x in (9, 5, 6, 7, 8):
            nxt = [I for I in alive if v not in I['conds'] or I['conds'][v][0] <= x <= I['conds'][v][1]]
            dfs(k + 1, nxt)
    dfs(0, ins)
    return best

def karp(c):
    """max cycle mean of c[(L0..L4)] over the de Bruijn graph on 4-tuples (step appends L4)."""
    nodes = list(itertools.product(range(5, 10), repeat=4)); idx = {v: i for i, v in enumerate(nodes)}; N = len(nodes)
    NEG = float('-inf'); D = [[NEG] * N for _ in range(N + 1)]
    for i in range(N): D[0][i] = 0.0
    for k in range(1, N + 1):
        Dk, Dp = D[k], D[k - 1]
        for v in nodes:
            pv = Dp[idx[v]]
            if pv == NEG: continue
            for x in range(5, 10):
                w = v[1:] + (x,); val = pv + c[v + (x,)]
                j = idx[w]
                if val > Dk[j]: Dk[j] = val
    best = NEG
    for i in range(N):
        if D[N][i] == NEG: continue
        best = max(best, min((D[N][i] - D[k][i]) / (N - k) for k in range(N) if D[k][i] != NEG))
    return best

def cplus():
    log = open(os.path.join(HERE, 'cplus_n2.log'), 'w')
    def P(s): print(s, flush=True); log.write(s + '\n'); log.flush()
    P('# c+ (max possible fits from hub w_i into u, d >= 9, apexes/privates free) and Karp max mean, 71 vs 79 parts')
    cs = []
    for name, flt in (('71 parts', lambda t: t not in N2TAGS), ('79 parts (71 + N2)', lambda t: True)):
        c = {}; cs.append(c)
        for Lw in itertools.product(range(5, 10), repeat=5):
            c[Lw] = cplus_window(Lw, flt)
        mx = {h: max(v for k, v in c.items() if k[2] == h) for h in range(5, 10)}
        P('%s: max c+ by hub letter 5..9+ %s' % (name, [mx[h] for h in range(5, 10)]))
        # Karp on 4-tuples is O(N^2 * 5) with N = 625: fine
        P('%s: max mean c+ per link edge %.4f' % (name, karp(c)))
    up = [k for k in cs[0] if cs[1][k] != cs[0][k]]
    P('link windows (L_{i-2}..L_{i+2}) whose c+ changes with N2: %d of %d; increases %s' % (len(up), len(cs[0]),
      collections.Counter(cs[1][k] - cs[0][k] for k in up)))

if __name__ == '__main__':
    {'gen': gen, 'cmp': cmp, 'cplus': cplus}[sys.argv[1]]()
