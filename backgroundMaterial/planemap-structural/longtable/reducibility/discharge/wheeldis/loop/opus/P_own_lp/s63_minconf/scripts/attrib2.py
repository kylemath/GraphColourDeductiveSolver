import pickle, collections, sys
exec(open('attrib.py').read().split("A = pickle.load")[0])
src = open('attrib.py').read(); jdef = src[src.index('def just(e)'):src.index('J = {e: just(e)')]
exec(jdef)
T = 0.041565
res = {}
for f in sys.argv[2:]:
    res.update(pickle.load(open(f, 'rb'))['res'])
nec = collections.defaultdict(list); ents_any = set()
for (d, lk, sv), (L0, e) in res.items():
    slack = (d - 6 + T) - L0
    for k, dl in e.items():
        ents_any.add(k)
        if dl > slack + 1e-9: nec[k].append((d, lk, sv, dl - slack))
print(sys.argv[1], 'rows', len(res), 'entries with delta>0 in some row', len(ents_any), 'entries that would VIOLATE (delta>slack)', len(nec), collections.Counter(k[0] for k in nec))
J = {e: just(e) for e in nec}; Jk = {e: {n for n in s if is_keep(n)} for e, s in J.items()}
print(' empty provenance', sum(1 for s in J.values() if not s), ' configs(fullTierA)', len(set().union(*J.values())), ' configs(keep)', len(set().union(*Jk.values())))
print(' by group', collections.Counter((k[0], k[1]) for k in nec))
pickle.dump({'nec': dict(nec), 'J': J, 'Jk': Jk}, open(sys.argv[1] + '.pkl', 'wb'))
