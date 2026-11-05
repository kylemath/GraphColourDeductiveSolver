import json, ast, sys
B='/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
S73=B+'s73_prune/'
UNI=B+'s72_weighted/rules_drop276.json'
GR=('d7_w6','d8_w6','d9_w6','d7_w7_1','d7_w7_-1','d8_w7_1','d8_w7_-1')
def load_uni():
    R=json.load(open(UNI))
    G={'d7_w6':R['d7_w6'],'d8_w6':R['d8_w6'],'d9_w6':R['d9_w6'],'d7_w7_1':R['d7_w7']['1'],'d7_w7_-1':R['d7_w7']['-1'],'d8_w7_1':R['d8_w7']['1'],'d8_w7_-1':R['d8_w7']['-1']}
    L=[];off={}
    for g in GR:
        off[g]=len(L); L+= [(g,r) for r in G[g]]
    return L,off
def write_rules(path, L, ids):
    ids=set(ids); out={'d7_w6':[],'d8_w6':[],'d9_w6':[],'d7_w7':{'1':[],'-1':[]},'d8_w7':{'1':[],'-1':[]}}
    for i in sorted(ids):
        g,r=L[i]
        if g.endswith('w6'): out[g].append(r)
        else: out[g[:5]][g.split('_')[-1]].append(r)
    json.dump(out,open(path,'w'))
def norm(r):
    p,wr,sr=r
    return (int(p),tuple(sorted((int(o),tuple(sorted(al))) for o,al in wr)),tuple(sorted((int(o),int(v)) for o,v in sr)))
def counts(L,ids):
    c={g:0 for g in GR}
    for i in ids: c[L[i][0]]+=1
    return c
