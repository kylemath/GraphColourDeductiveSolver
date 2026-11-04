"""s72 weighted cover. usage: w.py SP OUT"""
import pickle, re, collections, sys, numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
SP, OUT = sys.argv[1:3]
S71='/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s71_ruleset/'
d = pickle.load(open(S71+'cover.pkl','rb')); items = [it for it in pickle.load(open(S71+'items.pkl','rb')) if it[2]]
cls, cand, E0 = d['cls'], d['cand'], d['E0']
rsr = {}
for l in open(SP + '/rsst.txt'):
    f = l.split(); rsr[f[0].split('_')[0]] = int(f[1])
def ring(n):
    if n.startswith('rsst'): return rsr[n.split('_')[0]]
    m = re.search(r'_r(\d+)$', n)
    if m: return int(m.group(1))
    m = re.match(r'[a-z]+(\d+)_', n)
    return int(m.group(1)) if m else -1
def isD(n): return cls[n].endswith('D') or cls[n] == 'nl51'
BASE={13:.1,14:25/60,15:1.25,16:4,17:13}
def cost(n,W):
    if not isD(n): return .25
    r=ring(n)
    if r==-1: return 2.
    if r<=12: return 2/60
    return W[r]
def solve(W):
    names=sorted(set().union(*[it[2] for it in items])); ix={n:j for j,n in enumerate(names)}
    rows=list({it[2] for it in items})
    A=lil_matrix((len(rows),len(names)))
    for r,ws in enumerate(rows):
        for n in ws: A[r,ix[n]]=1
    c=np.array([cost(n,W) for n in names])
    c2=c-1e-7*np.array([n in E0 for n in names])
    res=milp(c2,constraints=LinearConstraint(A.tocsr(),1,np.inf),integrality=np.ones(len(names)),bounds=Bounds(0,1),options={'time_limit':600,'mip_rel_gap':1e-9})
    S={n for n,x in zip(names,res.x) if x>.5}
    assert all(it[2]&S for it in items)
    return S,res
def rep(S,W):
    D=[n for n in S if isD(n)]
    return sum(cost(n,W) for n in S), len(S), len(D), len(S)-len(D), collections.Counter(ring(n) for n in D)
W0=dict(BASE)
cfgs={'base':W0,'half15':{**W0,15:W0[15]/2},'dbl16_17':{**W0,16:8,17:26},'half15_dbl16_17':{**W0,15:W0[15]/2,16:8,17:26}}
out={}
for k,W in cfgs.items():
    S,res=solve(W); r=rep(S,W); out[k]=(S,r,res.status,res.mip_dual_bound)
    print(k,'status',res.status,'obj %.3f h'%r[0],'dual %.3f'%res.mip_dual_bound,'n',r[1],'D',r[2],'C',r[3],sorted(r[4].items()))
    # cost of the s71 3282 cover under this weight
S71c=pickle.load(open(S71+'ilp.pkl','rb'))['ilp']
for k,W in cfgs.items(): print('s71 cover cost under',k,'%.3f'%sum(cost(n,W) for n in S71c), 'Dring', sorted(collections.Counter(ring(n) for n in S71c if isD(n)).items()) if k=='base' else '')
pickle.dump(out,open(OUT+'/wcover.pkl','wb'))
S=out['base'][0]
src={'nl51':'nl51','rsstD':'RSST D','rsstC':'RSST C','k3xD':'k3x D','k3xC':'k3x C','k3pD':'k3p D','k3pC':'k3p C'}
with open(OUT+'/weighted_configs.tsv','w') as f:
    f.write('# s72 ring-weighted cover (base weights)\n# name\tsource\tlean\tring\tcost_h\tin_s71_cover\tin_E0_S\n')
    for n in sorted(S,key=lambda x:(not isD(x),ring(x),x)):
        f.write('%s\t%s\t%s\t%d\t%.4f\t%d\t%d\n'%(n,src[cls[n]],'hD' if isD(n) else 'hC',ring(n),cost(n,W0),n in S71c,n in E0))
print('overlap with s71',len(S&S71c),'in E0',len(S&E0))
