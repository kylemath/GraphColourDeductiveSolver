#!/usr/bin/env python3
"""Compare RSST-1SHOT against the spec's test vectors (results/test_vectors.json, test_vectors_ext.json).
Prints per vector MATCH or MISMATCH with the first differing field.  usage: check_vectors.py [tv|ext|both]"""
import sys, os, json, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcore as R, rows78

JOB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
IN = os.path.join(JOB, 'in')

def parse_conds(txt):
    if txt == 'always': return {}
    out = {}
    for t in txt.split(' & '):
        m = re.fullmatch(r'(p\d+\.\d+)(=|<=|>=)(\d)', t.strip())
        if not m: m2 = re.fullmatch(r'(p\d+\.\d+)in(\d)\.\.(\d)', t.strip()); out[m2.group(1)] = (int(m2.group(2)), int(m2.group(3))); continue
        nm, op, k = m.group(1), m.group(2), int(m.group(3))
        out[nm] = (k, k) if op == '=' else ((5, k) if op == '<=' else (k, 9))
    return out

def fits_key(lst):
    return collections.Counter((f['part'], f['hub'], f['target'], f.get('sure'), f.get('possible')) for f in lst)

def my_fired(fired):
    return collections.Counter((I['tag'], I['hub'], I['target'], sure, True) for I, sure in fired)

def check_filling(W, insts, reqs, privates, d, exp):
    """returns first differing field or None"""
    f = dict(privates)
    lo, hi, fired = R.ledger(d, insts, f)
    if lo != exp['lo']: return 'lo (mine %s, theirs %s)' % (lo, exp['lo'])
    if hi != exp['hi']: return 'hi (mine %s, theirs %s)' % (hi, exp['hi'])
    a, b = my_fired(fired), fits_key(exp['fits_that_fire'])
    if a != b: return 'fits_that_fire (mine-only %s; theirs-only %s)' % (list((a - b).elements())[:4], list((b - a).elements())[:4])
    mine = sorted([R.CONFIGS[c]['name'], R.CONFIGS[c]['verdict']] for c in R.contained(reqs, f))
    th = sorted([list(x) for x in exp['rsst_configs_contained']])
    if mine != th: return 'rsst_configs_contained (mine %s; theirs %s)' % (mine, th)
    return None

SUMF = ['n_fill', 'n_groups', 'relevant', 'n_inst', 'lo_max', 'hi_max', 'fills_lo_pos', 'fills_hi_pos', 'argmax_lo',
        'groups_hi_pos_killed', 'lo_max_after', 'hi_max_after', 'argmax_lo_after', 'lo_max_after_proved',
        'hi_max_after_proved', 'argmax_hi_after_proved', 'fills_hi_pos_after_proved']

def check_tv(log):
    TV = json.load(open(os.path.join(IN, 'results', 'test_vectors.json')))
    doms = {}
    nm = 0
    for v in TV:
        s = v['set']
        if s not in doms: doms[s] = json.load(open(os.path.join(IN, 'inputs', 'dom_%s.json' % s)))
        res, row = rows78.run_row(v['label'], doms[s][v['label']])
        first = None; nfield = 0; diffs = []; conv = []
        for k in SUMF:
            if k not in v['summary']: continue
            nfield += 1
            if res.get(k) != v['summary'][k]:
                diffs.append(k)
                first = first or 'summary.%s (mine %r, theirs %r)' % (k, res.get(k), v['summary'][k])
                if res.get('diag_relsites_' + k) == v['summary'][k]: conv.append(k)
        if diffs:
            log('   %s differing summary fields: %s; of which equal under the relevant-sites multiplicity convention: %s' % (v['label'], diffs, conv))
        first_strict = first
        first = None if diffs and diffs == conv else first
        extra = [k for k in v['summary'] if k not in SUMF]
        if first is None:
            mine = collections.Counter((I['tag'], I['hub'], I['target'], tuple(sorted(I['conds'].items())), I['open']) for I in row.insts)
            th = collections.Counter((f['part'], f['hub'], f['target'], tuple(sorted(parse_conds(f['conditions']).items())), False) for f in v['fits_touching_u'])
            if mine != th: first = 'fits_touching_u (mine-only %s; theirs-only %s)' % (list((mine - th).elements())[:3], list((th - mine).elements())[:3])
            txt_ok = sorted((I['tag'], I['hub'], R.cond_text(I)) for I in row.insts) == sorted((f['part'], f['hub'], f['conditions']) for f in v['fits_touching_u'])
        if first is None:
            for F in v['fillings']:
                key = F['which']
                if res.get(key) != F['filling']:
                    first = 'fillings[%s].filling (mine %r, theirs %r)' % (key, res.get(key), F['filling']); break
                fp = rows78.full_privates(row.link, {k: v2 for k, v2 in F['privates'].items()})
                if fp != F['privates']:
                    first = 'fillings[%s].privates keys' % key; break
                e = check_filling(row.W, row.insts, row.reqs, F['privates'], row.d, F)
                if e: first = 'fillings[%s].%s' % (key, e); break
        st = 'MATCH' if first is None and first_strict is None else ('MISMATCH' if first is not None else 'MISMATCH(count-convention only; all other fields match)')
        nm += (first is not None) or (first_strict is not None)
        if first is None and first_strict is not None: first = first_strict
        log('tv %s %-22s %s  (summary fields %d%s; cond text identical %s)%s' % (v['set'], v['label'], st, nfield,
            (', unchecked keys %s' % extra) if extra else '', txt_ok if first is None else '-', '' if first is None else '  first diff: ' + first))
    return len(TV), nm

def check_ext(log):
    E = json.load(open(os.path.join(IN, 'results', 'test_vectors_ext.json')))
    nm = 0
    for v in E['vectors']:
        d = v['d']; link = [int(c) for c in v['link']]; sw = [int(c) for c in v['sword']]
        W = R.Window(d, link, sw); insts = R.instances(W); reqs = R.requirements(W)
        first = None
        if len(insts) != v['n_fits_touching_u']: first = 'n_fits_touching_u (mine %d, theirs %d)' % (len(insts), v['n_fits_touching_u'])
        exp_keys = set(rows78.full_privates(link, {}))
        if first is None and set(v['privates']) != exp_keys: first = 'privates keys (mine %s theirs %s)' % (sorted(exp_keys), sorted(v['privates']))
        if first is None: first = check_filling(W, insts, reqs, v['privates'], d, v)
        nm += first is not None
        log('ext d=%-2d %-9s %s %s %s%s' % (d, v['why'], v['link'], v['sword'], 'MATCH' if first is None else 'MISMATCH',
            '' if first is None else '  first diff: ' + first))
    # all-5 at d>=9 (spec §10.2 last line)
    for d in range(9, 16):
        W = R.Window(d, [5] * d, [5] * d); insts = R.instances(W); reqs = R.requirements(W)
        lo, hi, fired = R.ledger(d, insts, {})
        c = [R.CONFIGS[i]['name'] for i in R.contained(reqs, {})]
        ok = (lo == hi == 60 - 4 * d and len(fired) == 6 * d and c == ['0.7322'])
        nm += not ok
        log('all5 d=%d lo=%d hi=%d fits=%d contains=%s %s' % (d, lo, hi, len(fired), c, 'MATCH' if ok else 'MISMATCH'))
    return len(E['vectors']) + 7, nm

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    out = open(os.path.join(JOB, 'logs', 'vectors_%s%s.log' % (which, ('_' + R.CONTROL) if R.CONTROL else '')), 'w')
    def log(s): print(s, flush=True); out.write(s + '\n'); out.flush()
    log('# RSST-1SHOT vector check, control=%r' % R.CONTROL)
    tot = []
    if which in ('ext', 'both'): tot.append(('ext', check_ext(log)))
    if which in ('tv', 'both'): tot.append(('tv', check_tv(log)))
    for k, (n, m) in tot: log('TOTAL %s: %d vectors, %d mismatches' % (k, n, m))
