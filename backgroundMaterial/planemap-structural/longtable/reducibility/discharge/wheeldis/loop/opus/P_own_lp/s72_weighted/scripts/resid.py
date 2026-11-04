import sys,collections,pickle
sys.argv=['x','/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/sp','.']
exec(open('scripts/w.py').read().split("W0=dict(BASE)")[0])
hi=lambda n: ring(n) in (16,17)
R=[it for it in items if all(hi(n) for n in it[2])]
print('residue items',len(R),collections.Counter(it[0].split('_')[0] if it[0].startswith('R_') else it[0][:2] if it[0].startswith('KT') else 'L3Q' for it in R))
F=set().union(*[it[2] for it in R]); print('distinct hi configs',len(F),collections.Counter(ring(n) for n in F))
sole={next(iter(it[2])) for it in R if len(it[2])==1}; print('of which sole-justifier',len(sole))
print('rules',sum(1 for it in R if it[0].startswith('R_')),'KT',sum(1 for it in R if it[0].startswith('KT')),'L3Q',sum(1 for it in R if it[0].startswith('L3Q')))
pickle.dump({'R':R,'F':F},open('resid.pkl','wb'))
with open('residue_items.tsv','w') as f:
    for it in R: f.write('%s\t%s\t%s\n'%(it[0],it[1],','.join(sorted(it[2]))))
