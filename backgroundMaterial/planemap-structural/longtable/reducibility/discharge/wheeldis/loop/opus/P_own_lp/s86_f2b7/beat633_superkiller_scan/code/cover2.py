# Read-only scan of beat_633 data/stage1_ext_profile.jsonl (k's outside team, origin/main 6eca7e244).
# usage: python3 -I cover2.py DATA_DIR OUT_DIR
import json, sys, collections
D, O = sys.argv[1], sys.argv[2]
pool = json.load(open(D + '/pool_configs.json'))['configs']
active = set(int(x) for x in open(D + '/synth_active.txt').read().split())
n = collections.Counter(); cov = collections.defaultdict(collections.Counter); words = collections.defaultdict(set); sole = collections.Counter()
with open(D + '/stage1_ext_profile.jsonl') as fh:
    for line in fh:
        r = json.loads(line); c = r['kS'][0]; n[c] += 1; words[c].add((r['d'], r['link']))
        ext = [p for p in set(r['kU']) if p != c]
        if not ext: sole[c] += 1
        for p in ext: cov[c][p] += 1
CAP = 395
with open(O + '/per_config.tsv', 'w') as f:
    f.write('id\tname\tring\tkind\ttier\tsampled_forced_leaves\tat_cap\tsampled_words\tleaves_no_other_pool_killer\tbest_ext\tbest_ext_ring\tbest_ext_kind\tbest_ext_cover\tpass1\n')
    for c in range(633):
        m = pool[c]; p, k = (cov[c].most_common(1)[0] if cov[c] else (-1, 0))
        f.write('\t'.join(str(x) for x in [c, m['name'], m['ring'], m['kind'], m['tier'], n[c], int(n[c] >= CAP), len(words[c]), sole[c], pool[p]['name'] if p >= 0 else '-', pool[p]['ring'] if p >= 0 else '-', pool[p]['kind'] if p >= 0 else '-', k, 'active' if c in active else 'dropped']) + '\n')
bye = collections.defaultdict(list)
for c in n:
    for p, k in cov[c].items():
        if k >= 0.9 * n[c]: bye[p].append(c)
multi = {p: sorted(v, key=lambda c: -n[c]) for p, v in bye.items() if len(v) >= 2}
with open(O + '/superkiller_candidates.tsv', 'w') as f:
    f.write('ext_id\text_name\text_ring\text_kind\tn_rsst\trsst (name ring kind sampled cover words pass1)\n')
    for p, v in sorted(multi.items(), key=lambda x: (-len(x[1]), -sum(n[c] for c in x[1]))):
        m = pool[p]
        f.write('\t'.join([str(p), m['name'], str(m['ring']), m['kind'], str(len(v))] + ['%s r%d %s %d %d w%d %s' % (pool[c]['name'], pool[c]['ring'], pool[c]['kind'], n[c], cov[c][p], len(words[c]), 'active' if c in active else 'dropped') for c in v]) + '\n')
# greedy disjoint merges among still-active RSST configs
used = set(); merges = []
for p, v in sorted(multi.items(), key=lambda x: (-len(x[1]), -sum(n[c] for c in x[1]))):
    vv = [c for c in v if c not in used and c in active]
    if len(vv) >= 2:
        merges.append((pool[p]['name'], [pool[c]['name'] for c in vv])); used.update(vv)
print('candidates', len(multi), 'kinds', collections.Counter((pool[p]['kind'], pool[p]['ring']) for p in multi))
print('disjoint merges (active only):', len(merges), 'configs saved if all work:', sum(len(v) - 1 for _, v in merges))
for m in merges: print(' ', m)
allsole = [c for c in range(633) if n[c] and sole[c] == n[c]]
print('configs with every sampled forced leaf uncovered by the rest of the pool:', len(allsole), [(pool[c]['name'], pool[c]['ring'], n[c]) for c in allsole][:40])
print('configs with sole >= 50%:', sum(1 for c in range(633) if sole[c] * 2 >= n[c]), ' sole leaves total', sum(sole.values()), 'of', sum(n.values()))
ring = collections.Counter(pool[c]['ring'] for c in allsole); print('rings of those', sorted(ring.items()))
print('at-cap by ring:', sorted(collections.Counter(pool[c]['ring'] for c in range(633) if n[c] >= CAP).items()))
print('words sampled for at-cap configs: median', sorted(len(words[c]) for c in range(633) if n[c] >= CAP)[155])
