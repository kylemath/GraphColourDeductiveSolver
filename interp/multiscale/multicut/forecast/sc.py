import json, sys, collections, statistics as st
R = collections.defaultdict(list)
for l in open(sys.argv[1]):
    r = json.loads(l)
    if 'flog' not in r: continue
    fl = r['flog']; wt = r['walkt']   # walkt: (n, nodd, |t|, dn)
    Lmap = {x['n']: x for x in fl}
    # distance of the remaining odd vertices to the boundary
    dm = [x['dmin'] for x in fl if x['dmin'] is not None]
    # d_last: dmin when exactly one odd vertex remains outside (first such step)
    one = [x for x in fl if x['nout'] == 1]
    dlast = one[0]['dmin'] if one else None
    # steps between penultimate and last enclosure, and |t| when the last odd vertex is enclosed
    full = [x for x in fl if x['nodd'] == r['oddtot']]
    tfull = full[0]['t'] if full else None
    # first r at which the oracle forecast differs from |t| (P_r != P_0) at the step just before full enclosure
    pre = [x for x in fl if x['nout'] >= 1]
    Lb = [w for w in wt]
    R[r['name']].append(dict(seed=r['spec'].split(':')[1], status=r['status'], last=r['faillast'], tfull=tfull, dlast=dlast,
                             dmed=st.median(dm) if dm else None, dmax=max(dm) if dm else None, n=r['n'],
                             Lmed=None))
for m, L in sorted(R.items(), key=lambda kv: kv[1][0]['n']):
    n = L[0]['n']; dl = [x['dlast'] for x in L if x['dlast'] is not None]; dmed = [x['dmed'] for x in L if x['dmed'] is not None]
    dmx = [x['dmax'] for x in L if x['dmax'] is not None]
    print('%-6s n=%5d runs=%2d ok=%2d lastfail=%2d tfull!=0=%2d | d_last median %s (range %s-%s) | median dmin over run %s | max dmin %s' % (
        m, n, len(L), sum(x['status'] == 'ok' for x in L), sum(bool(x['last']) for x in L), sum(1 for x in L if x['tfull'] not in (None, 0.0)),
        st.median(dl) if dl else None, min(dl) if dl else None, max(dl) if dl else None, st.median(dmed) if dmed else None, st.median(dmx) if dmx else None))
