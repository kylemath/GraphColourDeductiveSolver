# job P870 (Studio): configuration cover of the 870 rules + every keep95p131f kill-table cell + V7/V8 mask kill, from Studio's
# provenance (keep95p131f/rule_provenance.tsv for rules, prov_tables.json for tables/masks). Forced = sole justifier of an item;
# greedy cover (unweighted, then ring-weighted); compared with Opus's cover_final870.tsv (527).
import json, collections, glob, os, re
P = 'out/job_P870/'; F = 'loop/studio/opus_check/f2b041/'
A = json.load(open(P + 'in/final870.rules.json'))
def canon(g, r): return (g, json.dumps([int(r[0]), sorted([int(o), sorted(int(x) for x in al)] for o, al in r[1]), sorted([int(o), int(v)] for o, v in r[2])]))
want = set()
for g, v in A.items():
    for s, L in (v.items() if isinstance(v, dict) else [('0', v)]):
        for r in L: want.add(canon(g + ('' if s == '0' else '_' + s), r))
items = {}
for l in open(F + 'keep95p131f/rule_provenance.tsv'):
    if l.startswith('#'): continue
    g, rj, sg, n, names = l.rstrip('\n').split('\t'); k = canon(g + ('' if sg == '0' else '_' + sg), json.loads(rj))
    if k in want: items[('rule',) + k] = set(names.split(',')) if names else set()
print('rules matched in provenance: %d of %d' % (len(items), len(want)))
T = json.load(open(P + 'prov_tables.json'))
for U, d in T['kill'].items():
    for c, nm in d.items(): items[('kill', U, c)] = set(nm)
for kk in ('v7', 'v8'):
    for c, nm in T[kk].items(): items[(kk, c)] = set(nm)
print('items: %s' % dict(collections.Counter(k[0] for k in items)))
assert all(items.values()), 'an item without justifier'
ring = {}
for l in open('loop/k44/rsst.txt'): t = l.split(); ring[t[0].split('_')[0]] = int(t[1])
for fn in glob.glob('loop/k[0-9]*/*') + glob.glob(F + 'tierA/*') + glob.glob('out/job30/*') + glob.glob('job27/*'):
    if not os.path.isfile(fn): continue
    try: L = open(fn).read().splitlines()
    except Exception: continue
    for l in L:
        t = l.split()
        if len(t) >= 5 and t[1].isdigit() and t[2].isdigit() and ';' in t[3] + t[4]: ring.setdefault(t[0], int(t[1]))
allc = set().union(*items.values()); print('distinct justifying configurations over all items: %d; ring unknown: %d' % (len(allc), sum(1 for c in allc if c not in ring)))
forced = {next(iter(v)) for v in items.values() if len(v) == 1}
def greedy(wt):
    U = dict(items); cov = []
    for c in forced: cov.append(c)
    U = {k: v for k, v in U.items() if not (v & forced)}
    while U:
        cnt = collections.Counter(c for v in U.values() for c in v)
        c = max(cnt, key=lambda c: (cnt[c] / wt(c), c)); cov.append(c); U = {k: v for k, v in U.items() if c not in v}
    return cov
lean = {l.split()[0] for l in open(F + 'keep/keep_lean_C.txt') if l.strip() and not l.startswith('#')}
core = {l.split()[0] for l in open(F + 'keep95/core95.txt')}; r118 = {l.strip() for l in open(F + 'rsst118/names118.txt') if l.strip()}
k13 = {l.split()[0] for l in open(F + 'keep95/dropnames_cover.txt') if l.strip() and not l.startswith('#') and not l.startswith('rsst')}
ver = {}
for l in open('loop/k44/rsst_verdicts.txt'):
    if l.startswith('#') or not l.strip(): continue
    f = l.split(); v = [x for x in f if x.startswith('verdict=')]; ver[f[0].split('_')[0]] = v[0][8:] if v else None
def cls(c):
    if c.startswith('rsst'): return 'C rsst118' if c in r118 else ('C Lean531 (RSST)' if ver.get(c) == 'C2cons' else 'D RSST')
    if c in lean: return 'C Lean531'
    if c in core: return 'C core95'
    if c in k13: return 'C k3x13'
    if c.startswith('nl'): return 'D nl51'
    if c.startswith('q7'): return 'D k3p'
    return 'D k3x'
theirs = {l.split('\t')[0] for l in open(P + 'in/cover_final870.tsv') if not l.startswith('#') and l.strip()}
for nm_, wt in (('unweighted', lambda c: 1.0), ('ring-weighted (ring^4)', lambda c: float(ring.get(c, 12)) ** 4)):
    cov = set(greedy(wt)); D = [c for c in cov if cls(c).startswith('D')]; C = [c for c in cov if cls(c).startswith('C')]
    print('== greedy %s: %d configurations (%d D, %d C; forced %d)' % (nm_, len(cov), len(D), len(C), len(forced)))
    print('   D by ring: %s' % dict(sorted(collections.Counter(ring.get(c, -1) for c in D).items())))
    print('   C by source: %s' % dict(collections.Counter(cls(c) for c in C)))
    print('   vs Opus 527: common %d, theirs only %d, ours only %d' % (len(cov & theirs), len(theirs - cov), len(cov - theirs)))
    json.dump({'cover': sorted(cov), 'theirs_only': sorted(theirs - cov), 'ours_only': sorted(cov - theirs)}, open(P + 'cover_%s.json' % nm_.split()[0], 'w'), indent=0)
print('forced (sole-justifier) configurations: %d, of which in Opus\'s cover: %d; forced not in theirs: %s' % (len(forced), len(forced & theirs), sorted(forced - theirs)[:20]))
print('Opus cover names not justifying any item here: %d %s' % (len(theirs - allc), sorted(theirs - allc)[:20]))
