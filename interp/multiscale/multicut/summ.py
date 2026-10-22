# summary table over runs*.jsonl; vortex diagnostic: failure step encloses a new odd vertex? cut created at a non-vortex step?
import json, sys, glob, pickle, collections
for fn in sys.argv[1:]:
    print('==', fn)
    for l in open(fn):
        r = json.loads(l); fv = None
        if r['status'] != 'ok':
            try:
                D = pickle.load(open('/mnt/project-files/multiscale/multicut/fail_%s.pkl' % r['spec'].replace(':', '_'), 'rb'))
                prev = D['recs'][-1]['nodd'] if D['recs'] else 0; fv = (D['fail'] or {}).get('nodd', None)
                fv = None if fv is None else fv > prev
            except Exception: fv = '?'
        tr = r['trace']; nonv = 0; vinc = 0
        for a, b in zip(tr, tr[1:]):
            if b[2] > a[2]:
                if b[1] == a[1]: nonv += 1
                else: vinc += 1
        print('%-36s %-7s n=%-4d steps=%-4d maxR=%d maxcuts=%d after=%s nodd=%-3d fail_n=%s fail_at_vortex=%s cut+@vortex=%d cut+@nonvortex=%d nrep=%s %ds' % (
            r['spec'], r['status'], r['n'], r['steps'], r['maxR'], r['maxcuts'], r.get('maxcuts_after'), r['maxnodd'], (r.get('fail_step') or {}).get('n'), fv, vinc, nonv, r.get('nrep'), r['sec']))
