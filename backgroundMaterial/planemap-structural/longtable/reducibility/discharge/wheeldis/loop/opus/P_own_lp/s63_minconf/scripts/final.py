import pickle, collections, json
exec(open('validate.py').read().split('def build(')[0])
A = pickle.load(open('nec_b1e2.pkl','rb')); Bv = pickle.load(open('nec_vk.pkl','rb')); T5 = pickle.load(open('nec_b1e5.pkl','rb'))
def summ(name, Js):
    Jk = {}
    for J in Js:
        for e, s in J.items(): Jk[e] = {n for n in s if is_keep(n)}
    allk = set().union(*Jk.values())
    sing = {next(iter(s)) for s in Jk.values() if len(s) == 1}
    need = {e: s for e, s in Jk.items() if s and not (s & sing)}; chosen = set(sing)
    while need:
        cnt = collections.Counter(n for s in need.values() for n in s); n = cnt.most_common(1)[0][0]; chosen.add(n); need = {e: s for e, s in need.items() if n not in s}
    print(name, 'entries', len(Jk), collections.Counter(e[0] for e in Jk), 'configs', len(allk), dict(collections.Counter(cls[n] for n in allk)), 'forced', len(sing), 'greedy HS', len(chosen), 'zero-keep-just', sum(1 for s in Jk.values() if not s))
    return Jk, allk, chosen
summ('tight1e-5', [T5['J']]); Jb, ab, cb = summ('band1e-2', [A['J']]); Jv, av, cv = summ('KT-d>=10 (baseline-KT violators)', [Bv['J']])
Ju, au, cu = summ('UNION (lower bound of binding set)', [A['J'], Bv['J']])
with open('binding_entries.tsv','w') as f:
    f.write('type\tentry\tn_keep_justifiers\tkeep_justifiers(class:name)\n')
    for e, s in sorted(Ju.items(), key=str): f.write('%s\t%s\t%d\t%s\n' % (e[0], str(e[1:]), len(s), ';'.join(sorted('%s:%s' % (cls[n], n) for n in s))))
with open('binding_configs.txt','w') as f:
    for n in sorted(au): f.write('%s\t%s\t%s\n' % (n, cls[n], 'greedyHS' if n in cu else ''))
print(len(au), sorted(collections.Counter(cls[n] for n in cu).items()))
# KT breakdown of cells
print('KT cells:', sum(1 for e in Ju if e[0]=='KT'), 'rules', sum(1 for e in Ju if e[0]=='RULE'), 'L3Q', sum(1 for e in Ju if e[0]=='L3Q'))
