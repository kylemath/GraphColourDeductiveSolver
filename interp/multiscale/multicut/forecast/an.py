import json, sys, collections, re
def load(f):
    D = {}
    for l in open(f):
        r = json.loads(l); D[r['spec']] = r
    return list(D.values())
def cfg(spec):
    p = spec.split(':'); o = p[4] if len(p) > 4 else ''
    o = ','.join(x for x in o.split(',') if x and not x.startswith('dump') and not x.startswith('d=0') and not x.startswith('guard'))
    return p[0], int(p[1]), o or 'base'
def table(files, fams=None):
    R = []
    for f in files: R += load(f)
    T = collections.defaultdict(list)
    for r in R:
        m, s, o = cfg(r['spec'])
        if fams and m not in fams: continue
        T[(m, o)].append(r)
    rows = []
    for (m, o), L in sorted(T.items()):
        ok = sum(r['status'] == 'ok' for r in L)
        last = sum(r['status'] == 'FAIL' and (r.get('faillast') or False) for r in L)
        dead = sum(r['status'] == 'FAIL' and not r.get('faillast') and (r.get('fail_nodd') == r.get('oddtot')) for r in L)
        oth = sum(r['status'] == 'FAIL' for r in L) - last - dead
        unk = sum(r['status'] not in ('ok', 'FAIL') for r in L)
        pc = sum(r['peakcuts'] for r in L) / len(L); pt = sum(r['peakt'] for r in L) / len(L)
        tz = sum(1 for r in L if r.get('t_at_full') not in (None, 0.0))
        rows.append((m, o, len(L), ok, last, dead, oth, unk, round(pc, 1), round(pt, 1), tz))
    print('%-6s %-28s %3s %3s %4s %4s %4s %3s %5s %5s %4s' % ('map', 'config', 'N', 'ok', 'last', 'flat', 'oth', 'unk', 'pkc', 'pkt', 't!=0full'))
    for x in rows: print('%-6s %-28s %3d %3d %4d %4d %4d %3d %5.1f %5.1f %4d' % x)
    return T
if __name__ == '__main__':
    table(sys.argv[1:])
