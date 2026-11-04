import json,pickle
B='/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/'
R=pickle.load(open('resid.pkl','rb'))['R']
N=lambda r: json.dumps(r,sort_keys=True,separators=(',',':'))
drop=set()
for k,i,_ in R:
    _,g1,g2,*rest=k.split('_'); g=g1+'_'+g2; sd=rest[0]; drop.add((g,sd,i))
rf=json.load(open(B+'s64_keep95p131f/tab/rules_studio_keep95p131f.json'))
n=0;out={}
for g,v in rf.items():
    if isinstance(v,list):
        out[g]=[r for r in v if (g,'0',N(r)) not in drop]; n+=len(v)-len(out[g])
    else:
        out[g]={sd:[r for r in l if (g,sd,N(r)) not in drop] for sd,l in v.items()}
        n+=sum(len(l)-len(out[g][sd]) for sd,l in v.items())
print('dropped',n,'of',len(drop))
json.dump(out,open('rules_drop276.json','w'))
print({g:(len(v) if isinstance(v,list) else {a:len(b) for a,b in v.items()}) for g,v in out.items()})
