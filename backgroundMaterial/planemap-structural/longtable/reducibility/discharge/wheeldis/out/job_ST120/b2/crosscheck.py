#!/usr/bin/env python3
"""ST-120 B2 cross-check: Lean (RSSTCheck.lean #eval) against the spec test vectors and the independent spec-only
Python engine out/job_RSST1SHOT/code/rcore.py.

  python3 -I crosscheck.py gen   -> cases.txt (input of RSSTCheck.lean), expected.json
  ./run.sh RSSTCheck             -> lean_out.txt, lean_parts.txt
  python3 -I crosscheck.py cmp   -> crosscheck.log (per-source totals, every mismatch listed)
  RSST_CONTROL=hatside python3 -I crosscheck.py gen|cmp   planted control: rcore with its hat read across x–xn
      (expected_hatside.json, crosscheck_hatside.log); the cases are the same, so Lean need not be re-run

Cases: every filling in the spec's vectors (§10.1 test_vectors.json fillings, §10.2 test_vectors_ext.json, the all-5
lines d = 9..15, the §13 A.4 vectors), each compared with the spec's own expected values AND with rcore; plus seeded
random 2-balls at d = 5..14 compared with rcore.  Compared per case: lo, hi, and the multiset of fired fits
(tag, hub, target, sure).  Parts: lean_parts.txt against in/inputs/parts71.txt and against rcore.PARTS."""
import os, sys, json, random, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
WHEELDIS = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
JOB = os.path.join(WHEELDIS, 'out', 'job_RSST1SHOT')
sys.path.insert(0, os.path.join(JOB, 'code'))
import rcore as R  # noqa: E402

SEED = 20261110
SUF = ('_' + R.CONTROL) if R.CONTROL else ''
NRAND = {d: 250 for d in range(5, 15)}

def npriv(L): return 0 if L == 5 else (3 if L >= 9 else L - 5)

def ref(d, link, apex, priv):
    """rcore reference: lo, hi, Counter of (tag, hub, target, sure), number of OPEN instances."""
    W = R.Window(d, link, apex)
    insts = R.instances(W)
    f = {}
    for i in range(d):
        for j in range(npriv(link[i])): f['p%d.%d' % (i, j + 1)] = priv[i][j]
    lo, hi, fired = R.ledger(d, insts, f)
    c = collections.Counter((I['tag'], I['hub'], I['target'], bool(s)) for I, s in fired)
    return lo, hi, c, sum(1 for I in insts if I['open'])

def privs_from_dict(link, pd):
    return [[int(pd.get('p%d.%d' % (i, j + 1), 9)) for j in range(npriv(link[i]))] for i in range(len(link))]

def spec_fits(lst):
    return collections.Counter((x['part'], x['hub'], x['target'], bool(x['sure'])) for x in lst)

def gen():
    cases = []   # (id, d, link, apex, priv, spec_expected or None)
    TV = json.load(open(os.path.join(JOB, 'in', 'results', 'test_vectors.json')))
    for vi, v in enumerate(TV):
        d, lk, sw = v['label'].split(); d = int(d); link = [int(c) for c in lk]; apex = [int(c) for c in sw]
        for F in v['fillings']:
            cases.append(('tv%d_%s' % (vi, F['which']), d, link, apex, privs_from_dict(link, F['privates']),
                          {'lo': F['lo'], 'hi': F['hi'], 'fits': spec_fits(F['fits_that_fire'])}))
    E = json.load(open(os.path.join(JOB, 'in', 'results', 'test_vectors_ext.json')))
    for vi, v in enumerate(E['vectors']):
        link = [int(c) for c in v['link']]; apex = [int(c) for c in v['sword']]
        cases.append(('ext%d_d%d_%s' % (vi, v['d'], v['why']), v['d'], link, apex, privs_from_dict(link, v['privates']),
                      {'lo': v['lo'], 'hi': v['hi'], 'fits': spec_fits(v['fits_that_fire'])}))
    for d in range(9, 16):   # spec §10.2 last line: lo = hi = 60 - 4d, 6d fits
        cases.append(('all5_d%d' % d, d, [5] * d, [5] * d, [[] for _ in range(d)],
                      {'lo': 60 - 4 * d, 'hi': 60 - 4 * d, 'nfits': 6 * d}))
    txt = open(os.path.join(JOB, 'in_spec_v2_a7915274.md')).read()
    sec = txt[txt.index('**Test vectors** (all of them re-evaluated'):txt.index('<!--/D9TABLES-->')]
    k = 0
    for line in sec.split('\n'):
        f = [z.strip() for z in line.strip().strip('|').split('|')]
        if len(f) != 7 or not f[0].isdigit(): continue
        d, link, apex, pv, hl = int(f[0]), [int(c) for c in f[2]], [int(c) for c in f[3]], f[4], int(f[5])
        pv = '9' * (3 * d) if pv == '9..9' else pv
        priv = [[int(pv[3 * i + j]) for j in range(npriv(link[i]))] for i in range(d)]
        exp = {'lo': hl, 'hi': hl}
        if d == 9 and f[2] == '555665566' and f[3] == '595565666':
            m = re.search(r'37 fits into u: (.*)\n', txt)
            exp['fitlist'] = collections.Counter(z.strip() for z in m.group(1).split(','))
        cases.append(('s13_%d_d%d' % (k, d), d, link, apex, priv, exp)); k += 1
    rnd = random.Random(SEED)
    for d in range(5, 15):
        for t in range(NRAND[d]):
            if t % 5 == 4: pick = lambda: rnd.randint(5, 9)                       # uniform letters
            else: pick = lambda: rnd.choices([5, 6, 7, 8, 9], [40, 25, 15, 10, 10])[0]   # biased toward fits
            link = [pick() for _ in range(d)]; apex = [pick() for _ in range(d)]
            priv = [[pick() for _ in range(npriv(L))] for L in link]
            cases.append(('rnd_d%d_%d' % (d, t), d, link, apex, priv, None))
    with open(os.path.join(HERE, 'cases.txt'), 'w') as fh:
        for cid, d, link, apex, priv, _ in cases:
            fh.write('%s;%d;%s;%s;%s\n' % (cid, d, ''.join(map(str, link)), ''.join(map(str, apex)),
                                          ','.join(''.join(map(str, p)) for p in priv)))
    exp = {}
    for cid, d, link, apex, priv, spec in cases:
        lo, hi, c, nopen = ref(d, link, apex, priv)
        e = {'ref': {'lo': lo, 'hi': hi, 'fits': [[list(k), n] for k, n in sorted(c.items())], 'nopen': nopen}}
        if spec is not None:
            s = dict(spec)
            for key in ('fits', 'fitlist'):
                if key in s: s[key] = [[list(k) if isinstance(k, tuple) else k, n] for k, n in sorted(s[key].items())]
            e['spec'] = s
        exp[cid] = e
    json.dump(exp, open(os.path.join(HERE, 'expected%s.json' % SUF), 'w'), separators=(',', ':'))
    print('wrote %d cases (%d with spec expectations)' % (len(cases), sum(1 for c in cases if c[5] is not None)))

def parse_lean():
    out = {}
    for line in open(os.path.join(HERE, 'lean_out.txt')):
        f = line.split()
        if not f: continue
        cid, lo, hi, nopen, d5, d9 = f[0], int(f[1]), int(f[2]), int(f[3]), int(f[4]), int(f[5])
        c = collections.Counter()
        for z in f[6:]:
            m = re.fullmatch(r'(.+)@(u|w\d+)>(u|w\d+):([SO])', z)
            c[(m.group(1), m.group(2), m.group(3), m.group(4) == 'S')] += 1
        out[cid] = {'lo': lo, 'hi': hi, 'fits': c, 'nopen': nopen, 'dis5': d5, 'dis9': d9}
    return out

def tocounter(lst):
    return collections.Counter({(tuple(k) if isinstance(k, list) else k): n for k, n in lst})

def cmp():
    log = open(os.path.join(HERE, 'crosscheck%s.log' % SUF), 'w')
    def P(s): print(s); log.write(s + '\n')
    P('# ST-120 B2 cross-check: Lean RSSTCheck #eval vs spec vectors and rcore (%s), rcore control %r'
      % (R.__file__.split('wheeldis/')[-1], R.CONTROL))
    # parts
    lean_parts = [l.rstrip('\n') for l in open(os.path.join(HERE, 'lean_parts.txt')) if l.strip()]
    spec_parts = [l.rstrip('\n') for l in open(os.path.join(JOB, 'in', 'inputs', 'parts71.txt')) if l.strip() and not l.startswith('#')]
    rc_parts = R.parts_text(R.PARTS)
    P('parts: lean %d, parts71.txt %d, rcore %d; lean == parts71.txt: %s; lean == rcore: %s'
      % (len(lean_parts), len(spec_parts), len(rc_parts), lean_parts == spec_parts, lean_parts == rc_parts))
    for a, b in zip(lean_parts, spec_parts):
        if a != b: P('  PART MISMATCH lean %r spec %r' % (a, b))
    exp = json.load(open(os.path.join(HERE, 'expected%s.json' % SUF)))
    L = parse_lean()
    tot = collections.Counter(); bad = collections.Counter(); nfits = collections.Counter()
    extra = collections.Counter()
    for cid, e in exp.items():
        src = cid.split('_')[0]
        src = src if src == 's13' else re.sub(r'\d+$', '', src)
        tot[src] += 1
        if cid not in L: bad[src] += 1; P('MISSING %s' % cid); continue
        m = L[cid]; nfits[src] += sum(m['fits'].values())
        errs = []
        r = e['ref']
        if (m['lo'], m['hi']) != (r['lo'], r['hi']): errs.append('ref lo/hi lean %s rcore %s' % ((m['lo'], m['hi']), (r['lo'], r['hi'])))
        rc = tocounter(r['fits'])
        if m['fits'] != rc: errs.append('ref fits lean-only %s rcore-only %s' % (list((m['fits'] - rc).elements())[:5], list((rc - m['fits']).elements())[:5]))
        if m['nopen'] != r['nopen']: errs.append('open count lean %d rcore %d' % (m['nopen'], r['nopen']))
        if m['dis5'] or m['dis9']: errs.append('bool/tri disagreement %d/%d' % (m['dis5'], m['dis9']))
        s = e.get('spec')
        if s:
            if (m['lo'], m['hi']) != (s['lo'], s['hi']): errs.append('spec lo/hi lean %s spec %s' % ((m['lo'], m['hi']), (s['lo'], s['hi'])))
            if 'fits' in s:
                sc = tocounter(s['fits'])
                if m['fits'] != sc: errs.append('spec fits lean-only %s spec-only %s' % (list((m['fits'] - sc).elements())[:5], list((sc - m['fits']).elements())[:5]))
            if 'nfits' in s and sum(m['fits'].values()) != s['nfits']: errs.append('spec nfits lean %d spec %d' % (sum(m['fits'].values()), s['nfits']))
            if 'fitlist' in s:
                mine = collections.Counter('%s@%s' % (k[0], k[1]) for k in m['fits'].elements())
                if mine != tocounter(s['fitlist']): errs.append('spec 37-fit list differs')
                else: extra['s13 37-fit list'] += 1
        if errs:
            bad[src] += 1
            P('MISMATCH %s: %s' % (cid, '; '.join(errs)))
    for src in sorted(tot):
        P('%-5s cases %5d  fits fired (Lean) %6d  mismatches %d' % (src, tot[src], nfits[src], bad[src]))
    P('TOTAL cases %d, fits fired %d, OPEN fits (Lean) %d, mismatches %d; extra checks %s'
      % (sum(tot.values()), sum(nfits.values()), sum(m['nopen'] for m in L.values()), sum(bad.values()), dict(extra)))

if __name__ == '__main__':
    {'gen': gen, 'cmp': cmp}[sys.argv[1]]()
