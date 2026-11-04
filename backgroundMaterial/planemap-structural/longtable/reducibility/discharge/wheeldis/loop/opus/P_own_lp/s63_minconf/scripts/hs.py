import pickle, collections, json
exec(open('validate2.py').read().split('def l3mask')[0].replace("print('keep size'", "0 and print('keep size'"))
LET=(5,6,7,8,9)
keep = {n for n in cls if is_keep(n)}
def hs(sets, name):
    sets = [frozenset(s & keep) for s in sets]; sets = [s for s in sets if s]
    sing = {next(iter(s)) for s in sets if len(s) == 1}; need = [s for s in sets if not (s & sing)]; ch = set(sing)
    while need:
        cnt = collections.Counter(n for s in need for n in s); n = cnt.most_common(1)[0][0]; ch.add(n); need = [s for s in need if n not in s]
    print('%-28s items %5d  configs-in-union %5d  forced %4d  greedy hitting set %4d' % (name, len(sets), len(set().union(*sets)), len(sing), len(ch))); return ch
# KT: only boxes that are not wholly covered by other kept boxes matter; use all boxes (upper bound), U7 and U9 (U8 = U9)
c1 = hs([ws for mk, ws in P['KTREC'][7]], 'KT U7 boxes'); c2 = hs([ws for mk, ws in P['KTREC'][9]], 'KT U8/U9 boxes')
c3 = hs([ws for (V, s), rec in P['L3REC'].items() for r, ws in rec if 'a2' in r], 'l3q V7+V8 boxes (a2-kill)')
# rules in the keep95p131 Studio file that the outside extractor reproduces (exact tuple match)
RP = P['RULEPROV']; f = json.load(open(B+'tab_keep95p131/rules_studio_keep95p131.json'))
inf = {}
for g, grp in (('d7_w6', f['d7_w6']), ('d8_w6', f['d8_w6']), ('d9_w6', f['d9_w6'])):
    Dv = int(g[1]); 
    for p, wr, sr in grp: 
        k = (Dv, 6, ('p',0,1), (p, tuple((a, tuple(b)) for a, b in wr), tuple((a, b) for a, b in sr)))
        inf[(g, k)] = RP.get(k)
for Dv in (7, 8):
    for sg in ('1', '-1'):
        pv = ('p',0,2) if sg == '1' else ('p',0,1)
        for p, wr, sr in f['d%d_w7' % Dv][sg]:
            k = (Dv, 7, pv, (p, tuple((a, tuple(b)) for a, b in wr), tuple((a, b) for a, b in sr))); inf[('d%d_w7_%s' % (Dv, sg), k)] = RP.get(k)
att = [s for s in inf.values() if s]; print('Studio rules in keep95p131 file: %d, attributed by outside extractor: %d (%.0f%%)' % (len(inf), len(att), 100*len(att)/len(inf)))
c4 = hs(att, 'rules (attributed subset)')
allc = c1 | c2 | c3 | c4; print('UNION hitting set (tables identical up to unattributed rules):', len(allc), collections.Counter(cls[n] for n in allc), 'of', len(keep))
pickle.dump(allc, open('hs_all.pkl','wb'))
