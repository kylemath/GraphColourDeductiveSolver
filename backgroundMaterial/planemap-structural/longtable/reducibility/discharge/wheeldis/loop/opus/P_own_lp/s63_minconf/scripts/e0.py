import pickle, numpy as np, json, itertools, collections, hashlib, os
P = pickle.load(open('prov.pkl','rb')); cls = P['cls']
B='/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s60_f2b/'
OUT='e0/tab_E0/'
hs = pickle.load(open('hs_all.pkl','rb'))
bind = {l.split('\t')[0] for l in open('binding_configs.txt') if l.strip()}
S = set(hs)|bind
print('hs',len(hs),'binding',len(bind),'binding not in hs',len(bind-hs),'S',len(S), collections.Counter(cls[n] for n in S))
open('e0/S_configs.txt','w').write('\n'.join(sorted(S))+'\n')
inS = lambda n: n in S
def build(U):
    K = np.zeros((5,)*9, bool)   # starts EMPTY
    for mk, ws in P['KTREC'][U]:
        if not any(inS(n) for n in ws): continue
        K[np.ix_(*[[i for i in range(5) if (m>>i)&1] for m in mk])] = True
    return K
def pack(K):
    A = np.zeros((5,)*8, np.uint8)
    for b in range(5): A |= K[...,b].astype(np.uint8) << b
    return A
md5=lambda p: hashlib.md5(open(p,'rb').read()).hexdigest()
for U in (7,8,9):
    A = pack(build(9 if U==8 else U)); p=OUT+'kill/kill6_U%d.npy'%U
    ref = np.load(B+'tab_keep95p131/kill/kill6_U%d.npy'%U)
    np.save(p, A)
    print('U%d'%U,'shape',A.shape,A.dtype,ref.shape,ref.dtype,'equal',bool((A==ref).all()),'cells differ',int((A!=ref).sum()),'md5',md5(p),'ref md5',md5(B+'tab_keep95p131/kill/kill6_U%d.npy'%U))
LET=(5,6,7,8,9)
def l3mask(V):
    out={}
    for sig in (1,-1):
        rec=P['L3REC'][(V,sig)]
        for c,a_ in itertools.product((5,6),repeat=2):
            for w2,w3,w4,o in itertools.product(LET,repeat=4):
                ent={'c':c,'a':a_,'w2':w2,'w3':w3,'w4':w4,'o':o}; kill=set()
                for r,ws in rec:
                    if not any(inS(n) for n in ws): continue
                    if all(ent[k]==v for k,v in r.items() if k!='a2') and 'a2' in r: kill.add(r['a2'])
                out[(sig,c,a_,w2,w3,w4,o)]=sum(1<<(L-5) for L in LET if L not in kill)
    return out
for V,names in ((7,('tab_1','tab_-1')),(8,('tabV8_1','tabV8_-1'))):
    m=l3mask(V)
    for sig,nm in ((1,names[0]),(-1,names[1])):
        ref=json.load(open(B+'tab_keep95p131/%s.json'%nm)); new={}; d=[]
        for k,v in ref.items():
            sg,wd,ao=k.split(); s=int(sg); c=int(wd[0]);w2,w3,w4=int(wd[1]),int(wd[2]),int(wd[3]);a_=int(ao[0]);o=int(ao[1])
            mk=m[(s,c,a_,w2,w3,w4,o)]; new[k]=[mk,v[1]]
            if mk!=v[0]: d.append((k,v[0],mk))
        assert sorted(new)==sorted(ref)
        p=OUT+nm+'.json'; json.dump(new,open(p,'w'))
        rb = hashlib.md5(json.dumps(ref).encode()).hexdigest()==md5(B+'tab_keep95p131/%s.json'%nm)
        print(nm,'entries',len(ref),'mask diffs',len(d),'md5',md5(p),'ref md5',md5(B+'tab_keep95p131/%s.json'%nm),'dump-roundtrip-ok',rb, d[:5])
