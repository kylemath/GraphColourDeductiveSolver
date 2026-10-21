import sys, os, re, glob, collections
L = sys.argv[1]; OUT = sys.argv[2]; ALLB = sys.argv[3]
sys.path.insert(0, os.path.join(L, 'k59')); from canon59 import canon, isface
logs = sorted(glob.glob(os.path.join(L, 'k47', 'q54.log')) + glob.glob(os.path.join(L, 'k5[0-9]', 'q5*.log')) + glob.glob(os.path.join(L, 'k6[0-9]', 'q6*.log')))
rows = collections.OrderedDict()
for fn in logs:
    cur = None; lg = os.path.relpath(fn, L)
    for l in open(fn).read().splitlines():
        m = re.match(r'^(\d\d:\d\dZ) row (\S+) (\d+) (\d+) (\d+) - (\d+) windows at ring <= 16, (\d+) at ring <= 15', l)
        if m:
            t, P, d, lk, sv, n16, n15 = m.groups(); cur = (lg, P)
            rows[cur] = dict(log=lg, P=P, d=d, LK=lk, SV=sv, n15=n15, start=t, kills='', minimal='', todo='', closed='')
            continue
        if not cur: continue
        r = rows[cur]
        m = re.match(r'^kills (\d+) distinct f-names (\d+) minimal (\d+)', l)
        if m: r['kills'] = m.group(1)
        m = re.match(r'^Counter\((.*)\)$', l)
        if m and r['kills'] and r['kills'] != '0': r['minimal'] = ' '.join('r%s%s:%s' % (a, b, c) for a, b, c in re.findall(r"\('(\d+)', '(\w)'\): (\d+)", m.group(1)))
        m = re.search(r'(\d+) windows left -> (\S+)', l)
        if m: r['todo'] = '%s (%s)' % m.groups()
        if l.endswith('row %s closed' % cur[1]): r['closed'] = l[:6]
W = {}
for l in open(ALLB):
    f = l.split(); W[canon(f[2], f[3])] = (f[0], f[4])
o = open(os.path.join(OUT, 'binder_rows_swept.tsv'), 'w')
o.write('queue_log\tprefix\td\tlink\tsecond_ring\tcanon_key\tface\twindows_ring_le15\tstarted\tclosed\tkills\tminimal_kills(ring,verdict:count)\tno_kill_todo_ring16_18\topus_binder_weight_most_negative\topus_certs\n')
for r in rows.values():
    k = canon(r['LK'], r['SV']); w = W.get(k, ('', ''))
    o.write('\t'.join([r['log'], r['P'], r['d'], r['LK'], r['SV'], '%s/%s' % k, 'face' if isface(r['LK'], r['SV']) else 'nonface', r['n15'], r['start'], r['closed'],
                       (r['kills'] or '0') if r['closed'] else 'stopped', r['minimal'] or '-', r['todo'] or '-', w[0] or '-', w[1] or '-']) + '\n')
o.close(); print(len(rows), 'rows from', len(logs), 'queue logs')
