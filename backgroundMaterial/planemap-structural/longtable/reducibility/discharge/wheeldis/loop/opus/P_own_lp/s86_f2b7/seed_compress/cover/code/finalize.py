#!/usr/bin/env python3
"""Stage B: add the Lean evidence columns to the cover table and write the deliverable files (Opus, 10 Nov 2026).
usage: python3 -I finalize.py <in dir (mktable out)> <out dir>"""
import sys, os, collections, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); IN, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
mem = collections.defaultdict(list)
for l in open(os.path.join(HERE, 'leanlists', 'W_job_JCOV_coverage_lean_membership.tsv')):
    if l.startswith('#'): continue
    f = l.rstrip('\n').split('\t')
    if len(f) >= 3 and not f[2].startswith('-') and 'agreesRSST' not in f[1]: mem[f[0]].append('%s: %s' % (f[1], f[2].split(' (')[0]))
iso = {}
for l in open(os.path.join(HERE, 'leaniso.tsv')):
    if l.startswith('#') or l.startswith('rsst_id'): continue
    a, b = l.rstrip('\n').split('\t'); iso[a] = b
rows = []; H = None
for l in open(os.path.join(IN, 'cover_table.tsv')):
    if l.startswith('#'): continue
    f = l.rstrip('\n').split('\t')
    if f[0] == 'idx': H = f; continue
    rows.append(f)
H2 = H[:15] + ['lean_copy_evidence', 'queue_note'] + H[15:]
tab = collections.Counter(); out = []
for f in rows:
    ev = []
    wn = f[11].split()[2] if f[11].startswith('pattern') else None
    if wn and wn in mem: ev.append('witness %s has %s' % (wn, '; '.join(mem[wn])))
    if iso[f[1]] != '-':
        for m in iso[f[1]].split(','):
            nm, fl = m.split('@')
            if 'HDC502_D_todo' in fl: ev.append('isomorphic to %s in job_HDC502/D_todo.tsv (HDC502 hD, 370/370 built per ST-113)' % nm)
            elif 'HDC502_D_rsst5' in fl or 'HD0' in fl or 'r5' in fl: ev.append('isomorphic to %s in %s' % (nm, fl.replace('W_', '').replace('_', '/', 1)))
            else: ev.append('isomorphic to %s listed in %s (Lean job input; build status to confirm)' % (nm, fl.replace('W_', '').replace('_', '/', 1)))
    q = f[6]
    if q.startswith('to prove'):
        if wn and wn in mem: note = 'can leave the queue: our copy (same config, our X) has an hC theorem'
        elif any('HDC502/D_todo' in e for e in ev): note = 'can leave the queue: isomorphic copy proved in HDC502'
        elif ev: note = 'check: isomorphic copy listed in a Lean job input'
        else: note = 'stays in the queue'
    else: note = '-'
    tab[(q, f[3], 'covered' if f[7] == 'yes' else 'not covered', note)] += 1
    out.append(f[:15] + [' | '.join(ev) if ev else '-', note] + f[15:])
with open(os.path.join(OUT, 'cover_table.tsv'), 'w') as g:
    g.write('# Stage B cover test, all 633 RSST configs (unavoidable.conf 26aeba66). u = K3l5u + K3gB5u kill patterns + engine wheel kills; r = K3l5r + K3gB5r likewise. See README.md.\n')
    g.write('\t'.join(H2) + '\n')
    for r in out: g.write('\t'.join(r) + '\n')
for fn, sel in (('queue403_can_leave.tsv', lambda r: r[16].startswith('can leave')),
                ('queue403_check.tsv', lambda r: r[16].startswith('check')),
                ('queue403_stays.tsv', lambda r: r[16].startswith('stays'))):
    with open(os.path.join(OUT, fn), 'w') as g:
        g.write('\t'.join(H2) + '\n')
        for r in out:
            if sel(r): g.write('\t'.join(r) + '\n')
with open(os.path.join(OUT, 'summary.tsv'), 'w') as g:
    g.write('lean_queue\tverdict\tcover_u (= cover_r)\tqueue_note\tconfigs\n')
    for k, n in sorted(tab.items()): g.write('\t'.join(k) + '\t%d\n' % n)
for k, n in sorted(tab.items()): print(k, n)
shutil.copy(os.path.join(IN, 'witness_patterns.tsv'), os.path.join(OUT, 'witness_patterns.tsv'))
