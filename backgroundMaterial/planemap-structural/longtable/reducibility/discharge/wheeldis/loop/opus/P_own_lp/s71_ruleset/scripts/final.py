import pickle, re, collections, sys, csv
SP, OUT = sys.argv[1:3]
exec(open(OUT + '/scripts/report.py').read().split('# ILP on residual')[0].replace('sys.argv[1:3]', 'sys.argv[1:3]'))
I = pickle.load(open(OUT + '/ilp.pkl', 'rb')); ilp = I['ilp']; allforced = I['allforced']
gre = d['res']['A'][0]
# W11 map
w11 = {}; alias2key = {}
for l in open('/mnt/project-files/swarm/round6/W11-dside-lean/needed_D.tsv'):
    if l.startswith('#') or l.startswith('key'): continue
    f = l.rstrip('\n').split('\t'); w11[f[0]] = f
    for a in f[1].split(';'): alias2key[a] = f[0]
    alias2key[f[0]] = f[0]
def key(n):
    b = n.split('_')[0] if n.startswith('rsst') else n
    return alias2key.get(n) or alias2key.get(b) or n
Dset = {n for n in ilp if isD(n)}; Cset = {n for n in ilp if not isD(n)}
tbl_side = {k for k, f in w11.items() if 'table' in f[4]}
pat_side = {k for k, f in w11.items() if 'pattern' in f[4]}; rpat = {k for k, f in w11.items() if 'rpatN' in f[4]}
Dkeys = {key(n) for n in Dset}
rule_just_D = {n for it in items if it[0].startswith('R_') for n in it[2] if isD(n)}
sets = {}
def block(S, title):
    s, r, sr = stats(S)
    out = ['**%s**: %d configs (D %d, C %d; in E0_S %d; not in E0_S %d)' % (title, len(S), sum(isD(n) for n in S), sum(not isD(n) for n in S), len(S & E0), len(S - E0)), '']
    out.append('| source | n | D/C |'); out.append('|---|---|---|')
    for k in ['nl51', 'RSST D', 'RSST C', 'k3x D', 'k3x C', 'k3p D', 'k3p C']:
        out.append('| %s | %d | %s |' % (k, s.get(k, 0), 'D (hD)' if k.endswith('D') or k == 'nl51' else 'C (hC)'))
    out += ['', '| ring | n | D | C |', '|---|---|---|---|']
    for rg in sorted(r): out.append('| %d | %d | %d | %d |' % (rg, r[rg], sum(1 for n in S if ring(n) == rg and isD(n)), sum(1 for n in S if ring(n) == rg and not isD(n))))
    return '\n'.join(out)
# E0_S comparison
E0D = {n for n in E0 if isD(n)}
# configs of tables only
tabitems = [it for it in items if not it[0].startswith('R_')]
def greedy_only(its):
    ch = set(); rem = list(its)
    sing = {next(iter(i[2])) for i in rem if len(i[2]) == 1}; ch |= sing; rem = [i for i in rem if not (i[2] & ch)]
    while rem:
        cnt = collections.Counter(n for i in rem for n in i[2]); n = max(cnt, key=lambda x: (cnt[x], x in E0, x)); ch.add(n); rem = [i for i in rem if n not in i[2]]
    return ch
tabcov = greedy_only(tabitems)
# write config list
with open(OUT + '/ruleset_configs.tsv', 'w') as f:
    f.write('# s71 ruleset: greedy+ILP cover of kill boxes (U7,U9), l3q a2-kill boxes and keep95p131f rules (9,326). Combinatorial cover on recorded provenance, NOT a minimality proof of the proof stack.\n')
    f.write('# name\tsource\tlean_need\tring\tin_E0_S\tforced(sole justifier of some item)\tforced_kinds\n')
    fk = collections.defaultdict(list)
    for k, v in I['forced'].items():
        for n in v: fk[n].append(k)
    for n in sorted(ilp, key=lambda x: (not isD(x), SRC[cls[x]], ring(x), x)):
        f.write('%s\t%s\t%s\t%d\t%d\t%d\t%s\n' % (n, SRC[cls[n]], 'hD' if isD(n) else 'hC', ring(n), n in E0, n in allforced, ','.join(sorted(fk[n]))))
# numbers for md
nD_cover = len(Dset)
print('D', len(Dset), 'C', len(Cset), 'tabcov', len(tabcov), 'E0', len(E0), 'E0 D', len(E0D), 'ruleJD', len(rule_just_D))
print('D keys', len(Dkeys), 'in W11 table', len(Dkeys & tbl_side), 'pattern', len(Dkeys & pat_side), 'rpat', len(Dkeys & rpat), 'new', len(Dkeys - set(w11)))
union = Dkeys | pat_side | rpat
print('union with pattern+rpat', len(union))
print('E0_S D cover?', 'E0D not in cover', len(E0D - ilp), 'cover D not in E0', len(Dset - E0))
print('forced D/C', sum(isD(n) for n in allforced), sum(not isD(n) for n in allforced))
print('rsstD in cover', sum(cls[n]=='rsstD' for n in Dset))
print('E0 breakdown', collections.Counter(SRC[cls[n]] for n in E0))
print('rules justifier D union', len(rule_just_D), 'keepD', sum(isD(n) for n in cand))
print(block(ilp, 'cover'))
print('kill+l3q-only cover size', len(tabcov), 'D', sum(isD(n) for n in tabcov), 'C', sum(not isD(n) for n in tabcov))
print('single-justifier kinds', {k: len(v) for k, v in I['forced'].items()})
pickle.dump(dict(block=block(ilp,'cover')), open(OUT+'/blk.pkl','wb'))
