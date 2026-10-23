import json, os, collections
D = '/mnt/project-files/multiscale/kempe_trace/state_test/'
VARS = ['height_row0', 'height_all', 'trace_row0', 'trace_row0+h', 'trace_roww', 'trace_rows0,w', 'trace_deep_1..w',
        'trace_all_indep', 'FULL_noparity', 'FULL']
EXPS = ['L10_A', 'L10_B', 'L11_A', 'L11_B', 'L12_A', 'L12_B', 'L13_A', 'L13_B', 'L14_A', 'L14_B', 'L15_A', 'L15_B', 'L18_A', 'L18_B', 'opus_A', 'opus_B']
out = {}
def groups(recs, var):
    g = collections.defaultdict(list)
    for i, r in enumerate(recs): g[r['keys'].get(var, ('missing', i)) if var != 'colour' else r.get('colour', i)].append(i)
    return g
lines = []
for e in EXPS:
    if not os.path.exists(D + f'pop_{e}.json'): continue
    P = json.load(open(D + f'pop_{e}.json')); recs = P['recs']
    if os.path.exists(D + f'hpop_{e}.json'): recs = recs + json.load(open(D + f'hpop_{e}.json'))['recs']
    nob = sum(r['obstructing'] for r in recs); modes = collections.Counter((r['mode'], r['obstructing']) for r in recs)
    pb = sum(r.get('parity_bad', 0) for r in recs); pt = sum(r.get('parity_tot', 0) for r in recs)
    row = dict(L=P['L'], w=P['w'], k0=P['k0'], n=len(recs), obstructing=nob, modes={f'{m}:{"ob" if o else "pass"}': c for (m, o), c in sorted(modes.items())},
               parity_bad=pb, parity_tot=pt, vars={})
    pref = sorted(k for k in recs[0]['keys'] if k.startswith('prefix_'))
    # informative FULL classes: >= 2 distinct full colourings in the class
    if 'colour' in recs[0]:
        g = groups(recs, 'FULL'); inf = [ix for ix in g.values() if len({recs[i].get('colour', ('h', i)) for i in ix}) > 1]
        row['FULL_classes_with_distinct_colourings'] = len(inf)
        row['FULL_recs_in_those'] = sum(len(x) for x in inf)
        row['FULL_those_outcomes'] = collections.Counter(tuple(sorted(collections.Counter(recs[i]['obstructing'] for i in ix).items())) for ix in inf).most_common()
        row['FULL_those_modes'] = collections.Counter(tuple(sorted({recs[i]['mode'] for i in ix})) for ix in inf).most_common()
        row['distinct_colourings'] = len({r['colour'] for r in recs if 'colour' in r})
    # where do row-0-identical pairs with different outcome first differ?
    g0 = groups(recs, 'trace_row0+h'); firstdiff = collections.Counter(); ex0 = []
    for ix in g0.values():
        obs = [i for i in ix if recs[i]['obstructing']]; ps = [i for i in ix if not recs[i]['obstructing']]
        for a in obs:
            for b in ps:
                ka, kb = recs[a]['keys'], recs[b]['keys']
                if 'prefix_0..1' not in ka or 'prefix_0..1' not in kb: firstdiff['n/a'] += 1; continue
                fd = next((p for p in pref if ka[p] != kb[p]), 'row w only')
                firstdiff[fd] += 1
                wd = [r for r in range(P['w'] + 1) if recs[a]['rows'][r] != recs[b]['rows'][r]]
                if len(ex0) < 4: ex0.append(dict(ob_mode=recs[a]['mode'], pass_mode=recs[b]['mode'], ob_rows=recs[a]['rows'], pass_rows=recs[b]['rows'],
                                                 rows_whose_word_differs=wd, ob_heights=recs[a]['heights'], pass_heights=recs[b]['heights'], first_prefix_differing=fd))
    row['row0_collisions_first_difference'] = dict(firstdiff); row['row0_collision_examples'] = ex0
    for v in VARS + pref:
        g = groups(recs, v)
        mixed = [ix for ix in g.values() if len(set(recs[i]['obstructing'] for i in ix)) > 1]
        row['vars'][v] = dict(states=len(g), states_ob=len({k for k, ix in g.items() if recs[ix[0]]['obstructing']}),
                              mixed_classes=len(mixed), recs_in_mixed=sum(len(x) for x in mixed))
        if v == 'FULL' and mixed:
            ex = []
            for ix in mixed[:3]:
                a = next(i for i in ix if recs[i]['obstructing']); b = next(i for i in ix if not recs[i]['obstructing'])
                ex.append(dict(ob=recs[a], ps=recs[b]))
            row['FULL_mixed_examples'] = [{'ob_rows': x['ob']['rows'], 'ob_mode': x['ob']['mode'], 'pass_rows': x['ps']['rows'], 'pass_mode': x['ps']['mode']} for x in ex]
    out[e] = row
    lines.append(f"{e:7s} L={P['L']} w={P['w']} k0={P['k0']} n={len(recs)} ob={nob} parity_bad={pb}/{pt} " +
                 ' '.join(f"{v}:{row['vars'][v]['states']}/{row['vars'][v]['mixed_classes']}" for v in row['vars']) + f" | infoFULL={row.get('FULL_classes_with_distinct_colourings')} {row.get('FULL_those_outcomes')} {row.get('FULL_those_modes')} | row0-collision firstdiff {dict(firstdiff)}")
json.dump(out, open(D + 'analysis.json', 'w'), indent=1)
print('per variant: distinct states / mixed classes')
print('\n'.join(lines))
