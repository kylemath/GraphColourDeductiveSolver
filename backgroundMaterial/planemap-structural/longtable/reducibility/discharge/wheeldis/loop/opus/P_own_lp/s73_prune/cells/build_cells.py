"""build_cells.py: exact per-cell / per-bit justifier sets for the keep95p131f tables (run from P_own_lp).
KT7/KT9: a kill6 table cell is killed iff some keep-justified requirement box of s63 prov.pkl KTREC contains it;
its justifier set is the union over those boxes (s71 items.pkl keep-restricted sets). Checked: 84,396 U7 and 73,342 U9 cells.
L3B<V><sg>: each cleared a2 bit (mask 30) of s64_keep95p131f/tab l3q tables; justifiers = union over matching a2 boxes of L3REC.
Output: dict tag -> list of distinct justifier sets (the cover rows used by scripts/cover73pb.py)."""
import pickle, itertools, collections, json, sys
P = pickle.load(open('s63_minconf/prov.pkl', 'rb')); items = pickle.load(open('s71_ruleset/items.pkl', 'rb'))
out = {}
for U, tag in ((7, 'KT7'), (9, 'KT9')):
    its = {int(it[1]): it[2] for it in items if it[0] == tag}; rec = P['KTREC'][U]
    for i, ws in its.items(): assert ws <= rec[i][1]
    cell = collections.defaultdict(set)
    for i, ws in its.items():
        if not ws: continue
        for c in itertools.product(*[[b for b in range(5) if m >> b & 1] for m in rec[i][0]]): cell[c] |= ws
    print(tag, 'cells', len(cell)); out[tag] = list({frozenset(v) for v in cell.values()})
T = 's64_keep95p131f/tab/'
for V, files in ((7, ('tab_1.json', 'tab_-1.json')), (8, ('tabV8_1.json', 'tabV8_-1.json'))):
    for fn in files:
        sg = -1 if '-1' in fn else 1; t = json.load(open(T + fn)); rec = P['L3REC'][(V, sg)]
        its = {int(it[1]): it[2] for it in items if it[0] == 'L3Q%d%+d' % (V, sg)}; sets = set(); nk = 0
        for k, v in t.items():
            if v[0] == 31: continue
            assert v[0] == 30; nk += 1
            _, wd, ao = k.split(); c, w2, w3, w4 = map(int, wd); ap, o = map(int, ao)
            cell = {'c': c, 'w2': w2, 'w3': w3, 'w4': w4, 'a': ap, 'a2': 5}
            J = set().union(*[its[i] for i, (r, ws) in enumerate(rec) if i in its and all(cell.get(x) == y for x, y in r.items())])
            assert J; sets.add(frozenset(J))
        print('L3B%d%+d' % (V, sg), 'killed bits', nk); out['L3B%d%+d' % (V, sg)] = list(sets)
pickle.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else 's73_prune/cells/percell_all.pkl', 'wb'))
print({k: len(v) for k, v in out.items()})
