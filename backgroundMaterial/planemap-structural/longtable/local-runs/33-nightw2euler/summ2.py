import json, sys
from collections import Counter
R=[json.loads(l) for l in open(sys.argv[1])]
R=[r for r in R if r['ok']]
def vec(st): return tuple(st[p][1] for p in ('12','13','14'))+('|',)+tuple(st[p][1] for p in ('34','24','23'))
for cls in sorted(set((r['gamma'],tuple(r['fixed'])) for r in R)):
  S=[r for r in R if (r['gamma'],tuple(r['fixed']))==cls]
  print('==',cls,len(S))
  for r in S[:4]:
    print('  ',r['tag'],r['hole'],'L',r['L'],'back',r['back'],'fwd',r['fwd'])
    for i in sorted(r['st'],key=int): print('     pos',i,vec(r['st'][i]), 'R=',sum(v[0] for v in r['st'][i].values()))
