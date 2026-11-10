#!/usr/bin/env python3
"""Per-degree 'only cover' table (coordinator item 3): for every RSST 'none' configuration, the number of positive
states/fillings that the 582 proved configurations leave and that contain it, and the number where it is the ONLY
none configuration contained (so the state needs exactly that config's admissibility).
Sources: d7/8 sets (logs/sets_ABCT_0of1.jsonl; positive groups, spec-exact multiplicity; a group counts as
'only c' when every minimal combination that no proved config covers contains c and no other none config);
full world d5/d6/d7 (logs/fw_d*_582_0of1.jsonl) and d9..14 (logs/d9_d*_582_0of1.jsonl): dominance-reduced
DFS leaves.  Output results/ONLY_COVER.tsv and results/needs_none_sets.tsv."""
import os, json, glob, collections
JOB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
cont = collections.defaultdict(collections.Counter); only = collections.defaultdict(collections.Counter)
fills = collections.defaultdict(collections.Counter); fills_only = collections.defaultdict(collections.Counter)
sets_ = collections.defaultdict(collections.Counter); surv = collections.Counter(); tot = collections.Counter()
for l in open(os.path.join(JOB, 'logs', 'sets_ABCT_0of1.jsonl')):
    r = json.loads(l)
    if 'label' not in r: continue
    dk = 'd%s-sets' % r['label'].split()[0]
    for g in r['needs_none']:
        S = g['none_sets_per_uncovered_combination']; tot[dk] += 1
        allc = set(z for s in S for z in s)
        for c in allc: cont[dk][c] += 1; fills[dk][c] += g['fills']
        if len(allc) == 1 and all(len(s) == 1 for s in S):
            c = next(iter(allc)); only[dk][c] += 1; fills_only[dk][c] += g['fills']
        for s in S: sets_[dk][tuple(s)] += 1
for pat, lab in (('fw_d*_582_0of1.jsonl', 'fullworld'), ('d9_d*_582_0of1.jsonl', 'd9plus')):
    for f in sorted(glob.glob(os.path.join(JOB, 'logs', pat))):
        d = os.path.basename(f).split('_')[1]
        dk = '%s-%s' % (d, lab)
        for l in open(f):
            x = json.loads(l)
            if 'summary' in x: continue
            if x.get('survivor'): surv[dk] += 1; continue
            S = x['needs_none']; tot[dk] += 1
            for c in S: cont[dk][c] += 1
            if len(S) == 1: only[dk][S[0]] += 1
            sets_[dk][tuple(S)] += 1
with open(os.path.join(JOB, 'results', 'ONLY_COVER.tsv'), 'w') as o:
    o.write('# degree-source\tnone_config\tstates_containing\tstates_only_this_none\tfillings_containing(sets only)\tfillings_only(sets only)\n')
    for dk in sorted(cont):
        o.write('# %s: states needing a none config %d, genuine survivors %d, configs involved %d, configs that are a sole killer %d\n'
                % (dk, tot[dk], surv[dk], len(cont[dk]), len(only[dk])))
        for c, n in cont[dk].most_common():
            o.write('%s\t%s\t%d\t%d\t%s\t%s\n' % (dk, c, n, only[dk][c], fills[dk].get(c, '-'), fills_only[dk].get(c, '-')))
with open(os.path.join(JOB, 'results', 'needs_none_sets.tsv'), 'w') as o:
    o.write('# degree-source\tnone_set\tstates\n')
    for dk in sorted(sets_):
        for s, n in sets_[dk].most_common(): o.write('%s\t%s\t%d\n' % (dk, ','.join(s), n))
for dk in sorted(cont):
    print(dk, 'states', tot[dk], 'survivors', surv[dk], 'sole-killers', dict(only[dk]))
