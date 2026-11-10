#!/usr/bin/env python3
"""Summaries for RSST-1SHOT: results/summary_sets.tsv (spec-exact counts over all sites; both after-kill readings),
results/rows_sets.tsv (per row scalars), results/NEEDS_NONE.tsv (addendum A), results/fullworld_summary.tsv."""
import os, sys, json, glob, collections
JOB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
os.makedirs(os.path.join(JOB, 'results'), exist_ok=True)
rows = [json.loads(l) for l in open(os.path.join(JOB, 'logs', 'sets_ABCT_0of1.jsonl'))]
rows = [r for r in rows if 'label' in r]
pos = lambda v: v is not None and v > 0
mx = lambda a, b: b if a is None else (a if b is None else max(a, b))

cols = ['set', 'd', 'rows', 'not_done', 'fillings', 'pos_rows_dom', 'max_lo', 'max_hi', 'pos_fills_dom',
        'pos_rows_582', 'max_hi_582', 'pos_fills_582', 'rows_mod_adm', 'pos_rows_633', 'max_hi_633', 'pos_fills_633',
        'inexact', 'max_hi_582_allkill', 'max_hi_633_allkill', 'diag_pos_fills_dom_relsites']
agg = collections.OrderedDict()
for S in 'ABCT':
    for d in ('7', '8', 'all'):
        agg[(S, d)] = {c: 0 for c in cols}; agg[(S, d)].update({'set': S, 'd': d, 'max_lo': None, 'max_hi': None, 'max_hi_582': None,
                                                               'max_hi_633': None, 'max_hi_582_allkill': None, 'max_hi_633_allkill': None})
for r in rows:
    for key in ((r['set'], r['label'].split()[0]), (r['set'], 'all')):
        a = agg[key]; a['rows'] += 1
        if r['status'] != 'done': a['not_done'] += 1; continue
        a['fillings'] += r['n_fill']; a['pos_rows_dom'] += pos(r['hi_max']); a['pos_fills_dom'] += r['fills_hi_pos']
        a['max_lo'] = mx(a['max_lo'], r['lo_max']); a['max_hi'] = mx(a['max_hi'], r['hi_max'])
        a['pos_rows_582'] += pos(r['hi_max_after_proved']); a['pos_fills_582'] += r['fills_hi_pos_after_proved']
        a['max_hi_582'] = mx(a['max_hi_582'], r['hi_max_after_proved'])
        a['pos_rows_633'] += pos(r['hi_max_after']); a['pos_fills_633'] += r['fills_hi_pos_after']
        a['max_hi_633'] = mx(a['max_hi_633'], r['hi_max_after'])
        a['rows_mod_adm'] += pos(r['hi_max_after_proved']) and not pos(r['hi_max_after'])
        a['inexact'] += r['inexact_groups']
        a['max_hi_582_allkill'] = mx(a['max_hi_582_allkill'], r.get('hi_max_after_proved_allkill'))
        a['max_hi_633_allkill'] = mx(a['max_hi_633_allkill'], r.get('hi_max_after_allkill'))
        a['diag_pos_fills_dom_relsites'] += r['diag_relsites_fills_hi_pos']
with open(os.path.join(JOB, 'results', 'summary_sets.tsv'), 'w') as o:
    o.write('\t'.join(cols) + '\n')
    for a in agg.values():
        if a['rows']: o.write('\t'.join('-' if a[c] is None else str(a[c]) for c in cols) + '\n')
rc = ['set', 'label', 'status', 'n_fill', 'n_groups', 'relevant', 'rel_8mid', 'n_inst', 'lo_max', 'hi_max', 'fills_lo_pos', 'fills_hi_pos',
      'groups_hi_pos', 'groups_hi_pos_killed', 'groups_hi_pos_killed_proved', 'inexact_groups', 'lo_max_after', 'hi_max_after',
      'fills_hi_pos_after', 'lo_max_after_proved', 'hi_max_after_proved', 'fills_hi_pos_after_proved', 'hi_max_after_allkill',
      'hi_max_after_proved_allkill', 'argmax_hi', 'argmax_hi_after_proved']
with open(os.path.join(JOB, 'results', 'rows_sets.tsv'), 'w') as o:
    o.write('\t'.join(rc) + '\n')
    for r in rows: o.write('\t'.join(str(r.get(c)) for c in rc) + '\n')
# addendum A: per none config, rows/fillings that need it (no proved config in some minimal combination)
need = collections.defaultdict(list)
fw = []
for f in glob.glob(os.path.join(JOB, 'logs', 'fw_d*_582_0of1.jsonl')):
    for l in open(f):
        x = json.loads(l)
        if 'needs_none' in x: fw.append((f, x))
with open(os.path.join(JOB, 'results', 'NEEDS_NONE.tsv'), 'w') as o:
    o.write('# rows/fillings (positive, hi > 0) that no proved (D2/C2cons) configuration covers and that a "none" configuration kills.\n')
    o.write('# d7/8 sets: one line per (none config, positive group); sole = every uncovered minimal combination of the group contains this config\n')
    o.write('# fullworld d5/d6: one line per (none config, DFS leaf); unread apexes/privates are 9+ in the leaf\n')
    o.write('none_config\tsource\tset\tlabel\tfilling\thi\tfills\tsole\tnone_sets_of_uncovered_combinations\n')
    per = collections.Counter(); perrows = collections.defaultdict(set)
    for r in rows:
        for g in r['needs_none']:
            sets = g['none_sets_per_uncovered_combination']
            for c in sorted(set(z for s in sets for z in s)):
                sole = all(c in s for s in sets)
                o.write('%s\td78\t%s\t%s\t%s\t%d\t%d\t%s\t%s\n' % (c, r['set'], r['label'], g['filling'], g['hi'], g['fills'], sole, json.dumps(sets)))
                per[c] += g['fills']; perrows[c].add((r['set'], r['label']))
    for f, x in fw:
        for c in x['needs_none']:
            o.write('%s\tfullworld\t-\td%s %s\t%s\t%d\t-\t%s\t%s\n' % (c, os.path.basename(f).split('_')[1][1:], x['link'], x['filling'], x['hi'], len(x['needs_none']) == 1, json.dumps([x['needs_none']])))
            per[c] += 0; perrows[c].add(('fw', x['link']))
    o.write('# per none config: d78 fillings (spec-exact multiplicity) and rows\n')
    for c in sorted(perrows): o.write('# %s\tfillings %d\trows %s\n' % (c, per[c], sorted(perrows[c])))
print(open(os.path.join(JOB, 'results', 'summary_sets.tsv')).read())
