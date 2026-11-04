"""s71 ruleset cover: greedy set cover over kill boxes + l3q boxes + keep95p131f rules. usage: cover.py SP_DIR OUT_DIR
SP_DIR holds prov131.tsv (Studio rule_provenance.tsv of keep95p131, from origin/main) and keepC.txt (keep95p131_C.txt)."""
import pickle, json, sys, re, collections, os
SP, OUT = sys.argv[1:3]
P0 = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
os.chdir(P0 + 's63_minconf')
P = pickle.load(open('prov.pkl', 'rb')); cls = P['cls']
keepC = {l.split()[0] for l in open(SP + '/keepC.txt') if not l.startswith('#')}
kC1 = {k.split('_')[0] for k in keepC}
def is_keep(n):
    c = cls[n]
    if c.endswith('D') or c == 'nl51': return True
    if c == 'rsstC': return n.split('_')[0] in kC1
    return n in keepC
LEAK = {'q7-_....556_...756._::::::5_p3R1/s3=5', 'q7-_....556_...756._::::::5_s3#2=5', 'q7-_...5566_...56.._:::::5:5',
        'q7-_....556_....567_5*::::::5', 'q7-_...5566_...567._:::::5:5'}
keep = {n for n in cls if is_keep(n)}
print('keep', len(keep), 'leaked in keep', len(LEAK & keep), 'leaked in cls', len(LEAK & set(cls)))
cand = keep - LEAK
E0 = {l.strip() for l in open('E0_S_configs.txt') if l.strip()}
print('E0 not in cand', len(E0 - cand), list(E0 - cand)[:5])
# rules: keep95p131f file
rf = json.load(open(P0 + 's64_keep95p131f/tab/rules_studio_keep95p131f.json'))
def N(r): return json.dumps(r, sort_keys=True, separators=(',', ':'))
F = set()
for g in ('d7_w6', 'd8_w6', 'd9_w6'):
    for r in rf[g]: F.add((g, '0', N(r)))
for g in ('d7_w7', 'd8_w7'):
    for sd in ('1', '-1'):
        for r in rf[g][sd]: F.add((g, sd, N(r)))
print('rules file', len(F))
rules = {}
tot = 0
for l in open(SP + '/prov131.tsv'):
    if l.startswith('#'): continue
    g, r, sd, n, names = l.rstrip('\n').split('\t'); tot += 1
    k = (g, sd, N(json.loads(r)))
    rules[k] = set(names.split(','))
print('tsv rules', tot, 'distinct', len(rules))
inF = {k: v for k, v in rules.items() if k in F}
print('tsv rules in f file', len(inF), 'file rules not in tsv', len(F - set(rules)), 'dropped', len(rules) - len(inF))
# check the dropped are exactly those justified only by LEAK
dr = [v for k, v in rules.items() if k not in F]
print('dropped justified only by leaked:', sum(1 for v in dr if v <= LEAK), 'of', len(dr))
# name coverage
allj = set().union(*inF.values())
print('rule justifier names not in cls:', len(allj - set(cls)), list(allj - set(cls))[:5], ' not in keep:', len(allj - keep))
# items
items = []  # (kind, id, justifier set within cand)
for U in (7, 9):
    for i, (mk, ws) in enumerate(P['KTREC'][U]): items.append(('KT%d' % U, i, frozenset(ws & cand)))
for (V, s), rec in P['L3REC'].items():
    for i, (r, ws) in enumerate(rec):
        if 'a2' in r: items.append(('L3Q%d%+d' % (V, s), i, frozenset(ws & cand)))
for k, ws in inF.items(): items.append(('R_' + k[0] + '_' + k[1], k[2], frozenset(ws & cand)))
bad = [it for it in items if not it[2]]
print('items', len(items), 'uncoverable (no non-leaked justifier)', len(bad), collections.Counter(b[0] for b in bad))
assert all(b[0].startswith('KT') for b in bad)  # boxes whose justifiers are all outside the keep set are not keep-table boxes
items = [it for it in items if it[2]]
NBAD = len(bad)
pickle.dump(items, open(OUT + '/items.pkl', 'wb'))
def greedy(items, seed=set(), pref=E0, cost=lambda n: 1.0):
    chosen = set(seed); rem = [it for it in items if not (it[2] & chosen)]
    forced = {next(iter(it[2])) for it in rem if len(it[2]) == 1}
    chosen |= forced; rem = [it for it in rem if not (it[2] & chosen)]
    cnt = collections.Counter(n for it in rem for n in it[2])
    import heapq
    while rem:
        cnt = collections.Counter(n for it in rem for n in it[2])
        n = max(cnt, key=lambda x: (cnt[x] / cost(x), x in pref, x))
        chosen.add(n); rem = [it for it in rem if n not in it[2]]
    # redundancy pass: drop configs not needed
    need = collections.Counter()
    for it in items:
        for n in it[2] & chosen: need[n] += 1
    for n in sorted(chosen, key=lambda x: (x in pref, cost(x))):  # try dropping non-E0 / cheaper-first? drop non-pref first
        if all(len(it[2] & chosen) > 1 for it in items if n in it[2]) and n not in forced:
            chosen.discard(n)
    return chosen, forced
def isD(n): return cls[n].endswith('D') or cls[n] == 'nl51'
res = {}
res['A'] = greedy(items)
res['B'] = greedy(items, seed=E0 & cand)
res['W'] = greedy(items, cost=lambda n: 1.0 if isD(n) else 10.0)
for k, (c, f) in res.items():
    ok = all(it[2] & c for it in items)
    print(k, 'size', len(c), 'forced', len(f), 'in E0', len(c & E0), 'D', sum(isD(n) for n in c), 'C', sum(not isD(n) for n in c), 'covers all', ok)
def ring(n):
    m = re.search(r'_r(\d+)$', n)
    if m: return int(m.group(1))
    return None
pickle.dump({'res': res, 'cls': cls, 'cand': cand, 'E0': E0, 'keep': keep, 'inF': inF}, open(OUT + '/cover.pkl', 'wb'))
