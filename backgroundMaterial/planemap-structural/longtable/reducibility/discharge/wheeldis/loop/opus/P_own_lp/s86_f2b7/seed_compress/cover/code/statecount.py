#!/usr/bin/env python3
"""seed_compress Stage B, state-level counts where per-state data exists (Opus, 10 Nov 2026).

(1) d7/d8 domain sets A/B/C/T (W6r rsst_fp results/fp_{A,B,C,T}.json, K3gB5n domains): for every RSST config X, the positive
    groups (label + filling) whose kill list contains X, and how many of those have a row label that family F does NOT reject
    (engine admissible() semantics, all letters known).  Private-level kills are already in the K3gB5n domains.
(2) Full world d6/d7/d8 needs-none states (Studio RSST-1SHOT results/NEEDS_NONE.tsv.gz): for every none config X, the states
    no proved config covers that X kills, and how many family F does not reject.  Apex letters missing from the filling are
    unknown and every completion must be rejected (cover.py DFS); privates are ignored (conservative).
usage: python3 -I statecount.py <family tag> <patterns tsv> <out prefix>
"""
import sys, os, json, gzip, collections, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('cover', os.path.join(HERE, 'cover.py')); cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)
RF = '/mnt/project-files/swarm/round6/W6r-replay/rsst_fp'
tag, tsv, outp = sys.argv[1], sys.argv[2], sys.argv[3]
PATS, NAME, KIND = cv.load_family(tsv); INST = {}
LET, LI, UNK = cv.LET, cv.LI, cv.UNK

def rejected(d, link, apex):
    """apex: dict i -> letter (missing = unknown).  True if every completion is inadmissible under F."""
    w = [int(c) for c in link]
    if d == 5: return cv.isR5(w)
    if d == 6 and cv.isR6(w): return True
    lets = []
    for i in range(d): lets += [LI[min(w[i], 9)], LI[min(apex[i], 9)] if i in apex else UNK]
    if d not in INST: INST[d] = cv.Inst(PATS, d)
    ok, info, nn = cv.placement_killed(d, lets, INST[d], 20000)
    return ok
_RC = {}
def rejected_c(d, link, apex):
    k = (d, link, tuple(sorted(apex.items())))
    if k not in _RC: _RC[k] = rejected(d, link, apex)
    return _RC[k]

# (1) d7/d8 sets
S1 = collections.defaultdict(lambda: [0, 0, 0, 0]); seen = set(); trunc = []
for s in 'ABCT':
    D = json.load(open('%s/results/fp_%s.json' % (RF, s)))
    for row in D['rows']:
        if row.get('positives_truncated'): trunc.append('%s %s' % (s, row['label']))
        d, lk, sv = row['label'].split(); d = int(d)
        rej = rejected_c(d, lk, {i: int(c) for i, c in enumerate(sv)})
        for p in row['positives']:
            key = (row['label'], p['filling'])
            if key in seen: continue
            seen.add(key)
            for nm, verdict in p['configs']:
                a = S1[nm]; a[0] += 1; a[1] += p['fills']
                if not rej: a[2] += 1; a[3] += p['fills']
with open(outp + '_sets.tsv', 'w') as g:
    g.write('# %s: d7/d8 domain sets A/B/C/T, positive groups (distinct label + filling) whose kill list contains the config; rows truncated in fp json: %s\n' % (tag, '; '.join(trunc)))
    g.write('config\tgroups\tfills\tgroups_not_rejected\tfills_not_rejected\n')
    for nm, a in sorted(S1.items(), key=lambda x: -x[1][0]): g.write('%s\t%d\t%d\t%d\t%d\n' % ((nm,) + tuple(a)))
print('sets: %d configs with positive groups, %d distinct groups, truncated rows %d' % (len(S1), len(seen), len(trunc)), flush=True)

# (2) full-world needs-none states
S2 = collections.defaultdict(lambda: [0, 0, 0, 0]); n = 0
for line in gzip.open(RF + '/from_studio_RSST1SHOT/results/NEEDS_NONE.tsv.gz', 'rt'):
    f = line.rstrip('\n').split('\t')
    if len(f) < 9 or f[1] != 'fullworld': continue
    X, lab, fill, sole = f[0], f[3], f[4], f[7] == 'True'
    dd, link = lab.split(); d = int(dd[1:]); apex = {}
    for t in fill.split():   # '(all read letters 9+)': which apexes were read is not given, so all stay unknown
        if '=' not in t: continue
        k, v = t.split('=')
        if k.startswith('s') and '.' not in k: apex[int(k[1:])] = int(v)
    rej = rejected_c(d, link, apex); n += 1
    a = S2[X]; a[0] += 1; a[1] += (not rej); a[2] += sole; a[3] += (sole and not rej)
    if n % 50000 == 0: print('  needs-none %d lines, %d distinct states tested' % (n, len(_RC)), flush=True)
with open(outp + '_needsnone.tsv', 'w') as g:
    g.write('# %s: full-world d6/d7/d8 states that need a none config (RSST-1SHOT NEEDS_NONE, fullworld lines); not_rejected = family %s does not reject every apex completion\n' % (tag, tag))
    g.write('none_config\tstates\tstates_not_rejected\tsole_states\tsole_not_rejected\n')
    for X, a in sorted(S2.items(), key=lambda x: -x[1][0]): g.write('%s\t%d\t%d\t%d\t%d\n' % ((X,) + tuple(a)))
print('needs-none: %d lines, %d none configs, %d distinct states tested' % (n, len(S2), len(_RC)))
