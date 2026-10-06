#!/usr/bin/env python3
"""Compare a merged WP20 phase output with the audit's own recomputation (steps 1-7 of
longtable/audit/WP20-P1-audit-replay-plan.md, commit 003c289).

usage: compare_p1.py MERGED_JSON INPUT_PLANTRI [--workers 2] [--out DIR]
       compare_p1.py --chunks CHUNK_JSON... INPUT_PLANTRI   (merge integrity by the audit's own merge)
It imports only wp20_audit.py (audit code).
"""
import argparse, hashlib, json, os, sys
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wp20_audit import parse, analyse_graph

LT = os.environ.get('LONGTABLE_DIR', '/Users/fulkanjou/GraphColour/backgroundMaterial/planemap-structural/longtable')
EXPECT = dict(declaration='8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef',
              producer='bb350d3b9579b984188a270a58d682562d170dc41c159ac4528a340fbd1fd0b5',
              checker='98c6bcf79f684fd75a1a805388763982ce7de9ce41641bf75c94d0e75d79ab12',
              input='92e482edefb9ff4c5fbb77b2121366b2c3a88cf8001fecafa1ae29025e60d989')
FIELDS = ['unfilled_total', 'states', 'no_legal_fan', 'sep_bad', 'depth', 'filled_neighbour_for_bad',
          'd1_kills', 'p_kills', 'p_capped', 'locked_classes', 'legal_fans', 'status']


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def audit_sample(i): return int(hashlib.sha256(f'AUDIT-WP20-P1-{i}'.encode()).hexdigest()[:8], 16) % 100 == 0
def declared_sample(i): return int(hashlib.sha256(f'WP20-{i}'.encode()).hexdigest()[:8], 16) % 50 == 0


def recount(args):
    i, line = args
    recs, wits = analyse_graph(parse(line))
    return i, recs, wits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('merged'); ap.add_argument('input'); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', default='.'); ap.add_argument('--phase', default='P1'); ap.add_argument('--order', type=int, default=25)
    ap.add_argument('--input-sha', default=EXPECT['input'])
    a = ap.parse_args()
    rep = dict(faults=[], notes=[])
    def fault(*m): rep['faults'].append(' '.join(map(str, m)))

    # 1. bindings
    files = dict(declaration=f'{LT}/WP20-D1-declaration.md', producer=f'{LT}/d1_confirm.py',
                 checker=f'{LT}/d1_check.py', input=a.input)
    rep['file_hashes'] = {k: sha(p) for k, p in files.items()}
    for k, h in rep['file_hashes'].items():
        if h != (a.input_sha if k == 'input' else EXPECT[k]): fault('binding', k, h)
    out = json.load(open(a.merged))
    if out.get('declaration_sha256') != EXPECT['declaration']: fault('output declaration hash', out.get('declaration_sha256'))
    if out.get('input_sha256') != a.input_sha: fault('output input hash', out.get('input_sha256'))
    if out.get('producer_sha256', {}).get('d1_confirm.py') != EXPECT['producer']: fault('output producer hash', out.get('producer_sha256'))
    if out.get('phase') != a.phase or out.get('order') != a.order: fault('phase/order', out.get('phase'), out.get('order'))

    # 2. merge integrity
    lines = [l.rstrip('\n') for l in open(a.input) if l.strip()]
    gs = out['graphs']
    if [g['index'] for g in gs] != list(range(len(lines))): fault('indices not exactly 0..N-1 in order', len(gs), len(lines))
    for g in gs:
        if g['ascii'].strip() != lines[g['index']].strip(): fault('ascii mismatch at', g['index'])

    # 3. accounting
    unresolved = []
    for g in gs:
        rot = parse(lines[g['index']])
        deg5 = [x for x in range(len(rot)) if len(rot[x]) == 5]
        if sorted(v['x'] for v in g['vertices']) != deg5: fault('vertex set', g['index'])
        if g['status'] != 'complete': unresolved.append((g['index'], g['status']))
        for v in g['vertices']:
            if v['unfilled_total'] != v['states'] + v['no_legal_fan']: fault('unfilled identity', g['index'], v['x'])
            if v['d1_kills'] != v['sep_bad'] - v['depth']['1']: fault('d1 identity', g['index'], v['x'])
            if sum(v['depth'].values()) != v['sep_bad']: fault('depth sum', g['index'], v['x'])
            if (v['status'] == 'capped') != (v['p_capped'] > 0): fault('capped identity', g['index'], v['x'])
            if v['status'] != 'complete': unresolved.append((g['index'], v['x'], v['status']))
    rep['unresolved'] = unresolved

    # 4-7. recount: flagged graphs, audit 1% sample, declared 2% sample
    W = out.get('witnesses', {})
    flagged = {w['index'] for k in ('sep_bad', 'd1_kills', 'p_kills') for w in W.get(k, [])}
    flagged |= {g['index'] for g in gs if any(v['sep_bad'] or v['d1_kills'] or v['p_kills'] or v['status'] != 'complete'
                                              for v in g['vertices']) or g['status'] != 'complete'}
    aud = {i for i in range(len(lines)) if audit_sample(i)}
    dec = {i for i in range(len(lines)) if declared_sample(i)}
    todo = sorted(flagged | aud | dec)
    rep['sets'] = dict(flagged=len(flagged), audit_sample=len(aud), declared_sample=len(dec), total=len(todo))
    byidx = {g['index']: g for g in gs}
    witset = {k: {(w['index'], w['x'], tuple(w['state'])) for w in W.get(k, [])} for k in ('sep_bad', 'd1_kills', 'p_kills')}
    mine = {k: set() for k in witset}
    with ProcessPoolExecutor(a.workers) as ex:
        for i, recs, wits in ex.map(recount, [(i, lines[i]) for i in todo], chunksize=1):
            prod = {v['x']: v for v in byidx[i]['vertices']}
            for r, w in zip(recs, wits):
                p = prod.get(r['x'])
                if p is None: fault('missing vertex', i, r['x']); continue
                if p['status'] != 'complete': continue
                for f in FIELDS:
                    if p[f] != r[f]: fault('count', i, r['x'], f, 'producer', p[f], 'audit', r[f])
                for s in w['sep_bad']: mine['sep_bad'].add((i, r['x'], tuple(s['state'])))
                for k in ('d1_kills', 'p_kills'):
                    for s in w[k]: mine[k].add((i, r['x'], tuple(s)))
    for k in witset:
        sub = {t for t in witset[k] if t[0] in set(todo)}
        if sub != mine[k]: fault('witness set', k, 'producer-only', len(sub - mine[k]), 'audit-only', len(mine[k] - sub))
    rep['witness_counts'] = {k: len(v) for k, v in witset.items()}
    rep['truncated'] = out.get('truncated')
    rep['verdict'] = 'REPLAY AGREES' if not rep['faults'] else 'FAULT'
    json.dump(rep, open(os.path.join(a.out, 'compare-result.json'), 'w'), indent=1)
    print(rep['verdict'], len(rep['faults']), rep['sets'])


if __name__ == '__main__':
    main()
