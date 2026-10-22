import json,collections,sys
R=[json.loads(l) for l in open(sys.argv[1]) if 'err' not in l]
print(len(R))
g=collections.defaultdict(list)
for r in R: g[(r['name'][:4],r['kind'],r['r'])].append(r)
for k in sorted(g):
    L=g[k]
    f=lambda key: [x[key] if x[key] is not None else 'X' for x in L]
    print(k,'nA/nB',[ (x['nA'],x['nB']) for x in L],'seam',f('seam'),'Rpl(level in)',f('R_plain_level_in'),'tauU',[round(x['tauU_after_plain'],2) for x in L],'Rlev',f('R_level_level_in'),'Rpl(rand in)',f('R_plain_rand_in'),[x['log'] for x in L if x['log']])
