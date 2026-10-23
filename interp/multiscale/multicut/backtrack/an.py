# analysis of runs.jsonl (bounded backtracking)
import json, sys, collections, math
import numpy as np
rs = {}
for l in open('/mnt/project-files/multiscale/multicut/backtrack/runs.jsonl'):
    r = json.loads(l); rs[r['spec']] = r
R = list(rs.values())
def fam(r):
    nm = r['name']
    if nm.startswith('ico'): return nm
    if nm == 'L18': return 'L18-' + r['spec'].split(':')[2]
    return 'ctrl'
def cfg(r):
    o = r['spec'].split(':')[4].replace('face=seam,', '').replace(',walk=1', '')
    return o
print('## completion by family x config\n')
tab = collections.defaultdict(lambda: collections.Counter())
for r in R: tab[(cfg(r), fam(r))][r['status'] + ('-last' if r.get('faillast') else '') + (('-' + r['failkind']) if r.get('failkind') else '')] += 1
fams = sorted(set(fam(r) for r in R)); cfgs = sorted(set(cfg(r) for r in R))
print('| config | ' + ' | '.join(fams) + ' |'); print('|---' * (len(fams) + 1) + '|')
for c in cfgs:
    row = []
    for f in fams:
        t = tab[(c, f)]; n = sum(t.values())
        row.append('%d/%d' % (t['ok'], n) + (' (' + ', '.join('%s %d' % (k, v) for k, v in sorted(t.items()) if k != 'ok') + ')' if n and t['ok'] < n else '') if n else '-')
    print('| %s | %s |' % (c, ' | '.join(row)))
print('\n## events: backtrack depth used\n')
for c in cfgs:
    ev = [e for r in R if cfg(r) == c for e in r['events']]
    for kind in ('F', 'D', 'G'):
        E = [e for e in ev if e['kind'] == kind]
        if not E: continue
        ok = [e for e in E if e['ok']]; dep = [e['depth'] for e in ok]
        h = collections.Counter(min(d_, 41) if d_ < 5 else (5 if d_ < 10 else (10 if d_ < 20 else 20 if d_ < 40 else 40)) for d_ in dep)
        gd = [e['gdist'] for e in ok if e.get('gdist') is not None and e['depth'] > 0]
        jv = sum(1 for e in ok if e.get('jvortex')); nonzero = [e for e in ok if e['depth'] > 0]
        print('%-34s %s events %4d resolved %4d | depth max %s mean %.1f hist %s | changed step vortex %d/%d | graph dist median %s max %s' % (
            c, kind, len(E), len(ok), max(dep, default=None), np.mean(dep) if dep else float('nan'), dict(sorted(h.items())), jv, len(nonzero),
            np.median(gd) if gd else None, max(gd, default=None)))
print('\n## peaks (all runs that ran >= 90% of steps)\n')
pk = collections.defaultdict(list)
for r in R:
    if r['steps'] < 0.9 * (r['n'] - 3): continue
    pk[(fam(r) if fam(r) == 'ctrl' else fam(r)[:3], cfg(r))].append((r['n'], r['peakcuts'], r['peakt'], r['status']))
for k in sorted(pk):
    g = pk[k]; ns = np.array([x[0] for x in g]); pc = np.array([x[1] for x in g]); pt = np.array([x[2] for x in g])
    s1 = np.polyfit(np.log(ns), np.log(np.maximum(pc, 1)), 1)[0] if len(set(ns)) > 1 else float('nan')
    s2 = np.polyfit(np.log(ns), np.log(np.maximum(pt, 1)), 1)[0] if len(set(ns)) > 1 else float('nan')
    byn = collections.defaultdict(list)
    for x in g: byn[x[0]].append(x)
    print('%-8s %-36s runs %3d  slope cuts %.2f  slope |t| %.2f  | ' % (k[0], k[1], len(g), s1, s2) +
          '  '.join('n=%d: c %.1f t %.1f' % (n_, np.mean([x[1] for x in v]), np.mean([x[2] for x in v])) for n_, v in sorted(byn.items())))
print('\n## last-vertex / dead-state analysis: steps from full enclosure to end\n')
for r in R:
    if not r['name'].startswith('ico') and r['name'] != 'L18': continue
    if cfg(r) != 'd=0,guard=0': continue
    if r['full_n']: print(r['spec'], r['status'], 'faillast', r['faillast'], 'full_n', r['full_n'], 'n-full', r['n'] - r['full_n'], 't_at_full', r['t_at_full'])
print('\n## dead-state (D) events: depth from the enclosing step, by map\n')
for r in sorted(R, key=lambda r: (r['n'], r['spec'])):
    D = [e for e in r['events'] if e['kind'] == 'D']
    if D: print(r['spec'], r['status'], [(e['k'], e.get('depth'), e['ok'], e['used'], e.get('gdist')) for e in D])
print('\n## F events resolved: (failure n, depth, graph dist, changed step is vortex, last-vertex)\n')
for r in R:
    F = [e for e in r['events'] if e['kind'] == 'F' and e['ok']]
    if F: print(r['spec'], [(e['n'], e['depth'], e.get('gdist'), e.get('jvortex'), e['last']) for e in F])
print('\n## unresolved F events: last-vertex?, used\n')
for r in R:
    F = [e for e in r['events'] if e['kind'] == 'F' and not e['ok'] and r['d'] > 0]
    if F: print(r['spec'], [(e['n'], e['last'], e['full'], e['used']) for e in F])
