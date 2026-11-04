import pickle, collections, itertools, json
exec(open('validate.py').read().split('def build(')[0])
A = pickle.load(open('an_full.pkl','rb')); res = A['res']; ents = A['ents']
mind = min(dl for (L0, e) in res.values() for dl in e.values()); print('min delta', mind, 'rows w/ binding', sum(1 for v in res.values() if v[1]))
kinds = collections.Counter(e[0] for e in ents); print('entries by type', kinds)
byd = collections.Counter((k[0], k[1] if k[0] != 'KT' else k[1]) for k in ents); print(byd)
def just(e):
    if e[0] == 'KT':
        _, U, idx, p = e; out = set(); pm = p - 5
        for mk, ws in P['KTREC'][U]:
            if all((mk[i] >> idx[i]) & 1 for i in range(8)) and (mk[8] >> pm) & 1: out |= ws
        return out
    if e[0] == 'L3Q':
        _, d, key, p = e; sig, c, a, a2, w4, ap, o = key; ent = {'c': c, 'a': ap, 'w2': a, 'w3': a2, 'w4': w4, 'o': o}; out = set()
        for r, ws in P['L3REC'][(d, sig)]:
            if r.get('a2') == p and all(ent[k] == v for k, v in r.items() if k != 'a2'): out |= ws
        return out
    if e[0] == 'RULE':
        _, g, wr, sr, p = e; Dv = int(g[1]); w0 = 6 if 'w6' in g else 7
        sg = None if 'w6' in g else int(g.split('_')[-1]); pv = ('p', 0, 1) if (sg in (None, -1)) else ('p', 0, 2)
        rule = (p, tuple((int(k), tuple(sorted(al))) for k, al in wr), tuple((int(k), int(v)) for k, v in sr))
        return set(P['RULEPROV'].get((Dv, w0, pv, rule), set()))
J = {e: just(e) for e in ents}
for e in sorted(J, key=str): pass
unattr = [e for e in J if not J[e]]
print('entries with empty provenance', len(unattr), [e[:2]+(e[3] if e[0]=='RULE' else e[3],) for e in unattr][:5], collections.Counter(e[0] for e in unattr))
allc = set().union(*J.values()); print('distinct configs justifying binding entries (full TierA):', len(allc), collections.Counter(cls[n] for n in allc))
Jk = {e: {n for n in s if is_keep(n)} for e, s in J.items()}
allk = set().union(*Jk.values()); print('... of which in keep95p131:', len(allk), collections.Counter(cls[n] for n in allk))
print('per-entry justifier counts (keep):', sorted(len(s) for s in Jk.values()))
# greedy hitting set among keep-justifiers (attributed entries only)
need = {e: s for e, s in Jk.items() if s}
sing = {next(iter(s)) for s in need.values() if len(s) == 1}
rem = {e for e, s in need.items() if not (s & sing)}; chosen = set(sing)
while rem:
    cnt = collections.Counter(n for e in rem for n in need[e]); n, _ = cnt.most_common(1)[0]; chosen.add(n); rem = {e for e in rem if n not in need[e]}
print('forced (singleton justifier) configs', len(sing), 'greedy hitting set size', len(chosen), collections.Counter(cls[n] for n in chosen))
pickle.dump({'J': J, 'Jk': Jk, 'chosen': chosen, 'sing': sing}, open('attrib.pkl', 'wb'))
for e in sorted(J, key=str)[:0]: print(e)
# per-type summary of the justifiers
for kind in ('KT', 'L3Q', 'RULE'):
    s = set().union(*[Jk[e] for e in Jk if e[0] == kind] or [set()]); print(kind, 'entries', sum(1 for e in Jk if e[0]==kind), 'keep-configs', len(s), dict(collections.Counter(cls[n] for n in s)))
