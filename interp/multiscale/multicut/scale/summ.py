import json, sys, collections, re
def load(fn): return [json.loads(l) for l in open(fn)]
def fam(spec):
    m = spec.split(':')[0]; return re.sub(r'\d+(_\d+)?$', '', m) if m != 'L18' else 'L18'
def table(rs, key=lambda r: (fam(r['spec']), r['spec'].split(':')[2] if r['spec'].split(':')[2] in ('left','right','prioA','prioB') else 'rand', r['spec'].split(':')[3], ':'.join(r['spec'].split(':')[4:]) or '-')):
    G = collections.defaultdict(list)
    for r in rs: G[key(r)].append(r)
    print('| group | runs | ok | FAIL last vertex | FAIL earlier (flat remainder, t!=0) | FAIL earlier (other) | UNK/timeout | max R (ok runs) | R hist of maxR | max cuts | max cuts/nodd | nonvortex creations |')
    print('|' + '---|'*12)
    for k in sorted(G):
        g = G[k]; ok = [r for r in g if r['status'] == 'ok']
        fl = [r for r in g if r['status'] == 'FAIL' and r['diag'] and r['diag']['last']]
        ff = [r for r in g if r['status'] == 'FAIL' and r['diag'] and not r['diag']['last'] and r['diag']['nodd'] == r['oddtot'] and (r['t_at_full'] or 0) > 0]
        fo = [r for r in g if r['status'] == 'FAIL' and r not in fl and r not in ff]
        un = [r for r in g if r['status'] not in ('ok', 'FAIL')]
        h = collections.Counter(r['maxR'] for r in g)
        print('| %s | %d | %d | %d | %d | %d | %d | %s | %s | %d | %.2f | %d |' % ('/'.join(k), len(g), len(ok), len(fl), len(ff), len(fo), len(un),
              max([r['maxR'] for r in ok], default='-'), dict(sorted(h.items())), max(r['maxcuts'] for r in g), max(r['maxratio'] for r in g), sum(r['newcut_nonvortex'] for r in g)))
if __name__ == '__main__':
    rs = sum((load(f) for f in sys.argv[1:]), [])
    table(rs)
    bad = [r for r in rs if r['status'] == 'ok' and not r.get('proper')]
    print('ok but improper:', len(bad))
