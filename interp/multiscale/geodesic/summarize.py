import json, collections, sys
R = [json.loads(l) for l in open('res.jsonl')]
def agg(rs, k):
    c = collections.Counter()
    for r in rs: c.update({int(a): b for a, b in (r.get(k) or {}).items()})
    return dict(sorted(c.items()))
def q(h, p):
    tot = sum(h.values()); acc = 0
    for k in sorted(h):
        acc += h[k]
        if acc >= p*tot: return k
by = collections.defaultdict(list)
for r in R:
    if 'err' in r: print('ERR', r['name'], r['mode'], r['err'][-200:]); continue
    by[(r['name'], r['mode'])].append(r)
print('map mode | n | splitsCL fullyCL/splitsCL | chords/child from CL | chord d<=2 share (fromCL) | types fromCL | S0 nonroot max | j median/p90 | rootj | leafmax')
for (nm, mo), rs in sorted(by.items()):
    jh = agg(rs, 'j_hist'); cc = agg(rs, 'chords_child_fromCL'); dd = agg(rs, 'chord_d_fromCL')
    ty = collections.Counter();
    for r in rs: ty.update(r.get('chord_type_fromCL') or {})
    near = sum(v for k, v in dd.items() if k <= 2); tot = sum(dd.values())
    print(nm, mo, '|', rs[0]['n'], '|', sum(r.get('splits_from_CL') or 0 for r in rs), sum(r.get('fully_CL_from_CL') or 0 for r in rs), '/', sum(r.get('splits') or 0 for r in rs),
          '|', cc, '| %d/%d' % (near, tot), '|', dict(ty), '|', [r['S0_nonroot'] for r in rs], '|', q(jh, .5), q(jh, .9), '|', [r['root_j'] for r in rs], '|', [r['leafmax'] for r in rs],
          '| jsize', [r['j_by_size'] for r in rs][0], '| kidch', max(r['kid_chords_max'] for r in rs))
