import pickle, numpy as np, json, itertools, collections
exec(open('validate.py').read().split('def build(')[0])
bsrc = open('../gcoct26/build_upgraded_kills.py').read()
a=bsrc.index('def filter_extra_w6'); b=bsrc.index('def build_extra_rules_dict'); exec(bsrc[a:b])
LET=(5,6,7,8,9)
def l3mask(V, keepf):
    out={}
    for sig in (1,-1):
        rec=P['L3REC'][(V,sig)]
        for c,a_ in itertools.product((5,6),repeat=2):
            for w2,w3,w4,o in itertools.product(LET,repeat=4):
                ent={'c':c,'a':a_,'w2':w2,'w3':w3,'w4':w4,'o':o}; kill=set()
                for r,ws in rec:
                    if keepf and not any(keepf(n) for n in ws): continue
                    if all(ent[k]==v for k,v in r.items() if k!='a2') and 'a2' in r: kill.add(r['a2'])
                out[(sig,c,a_,w2,w3,w4,o)]=sum(1<<(L-5) for L in LET if L not in kill)
    return out
for V,names in ((7,('tab_1','tab_-1')),(8,('tabV8_1','tabV8_-1'))):
    for sel,tag in ((is_keep,'keep'),(None,'full')):
        m=l3mask(V,sel); d=0; n=0
        tabs = {1:json.load(open(B+'tab_keep95p131/%s.json'%names[0])), -1:json.load(open(B+'tab_keep95p131/%s.json'%names[1]))} if tag=='keep' else {1:json.load(open(B+'tab/%s.json'%names[0])),-1:json.load(open(B+'tab/%s.json'%names[1]))}
        for (sig,c,a_,w2,w3,w4,o),mk in m.items():
            key='%+d %d%d%d%d %d%d'%(sig,c,w2,w3,w4,a_,o); fm=tabs[sig].get(key)
            fm=fm[0] if isinstance(fm,list) else fm
            n+=1
            if fm!=mk: d+=1
        print('l3q V%d %s: %d entries, mismatches vs file %d (killed bits scratch %d)'%(V,tag,n,d,sum(5-bin(x).count('1') for x in m.values())))
# rules
RP=P['RULEPROV']
def rules_for(keepf):
    R=collections.defaultdict(set)
    for (Dv,w0,pv,rule),ws in RP.items():
        if keepf and not any(keepf(n) for n in ws): continue
        R[(Dv,w0,pv)].add(rule)
    def conv(r): return (r[0],tuple((k,tuple(a)) for k,a in r[1]),tuple(tuple(x) for x in r[2]))
    out={}
    for Dv,ue in ((7,True),(8,True),(9,False)):
        out['d%d_w6'%Dv]=set(filter_extra_w6(sorted(R[(Dv,6,('p',0,1))]),Dv,ue)) if True else None
    for Dv in (7,8):
        rb={('p',0,1):sorted(R[(Dv,7,('p',0,1))]),('p',0,2):sorted(R[(Dv,7,('p',0,2))])}
        e=filter_extra_w7(rb,Dv); out['d%d_w7_-1'%Dv]=set(e['-1']); out['d%d_w7_1'%Dv]=set(e['1'])
    return out
def norm(r): return json.dumps(r,sort_keys=True)
def fromfile(path):
    f=json.load(open(path)); o={}
    o['d7_w6']=f['d7_w6'];o['d8_w6']=f['d8_w6'];o['d9_w6']=f['d9_w6']
    for d in (7,8):
        o['d%d_w7_1'%d]=f['d%d_w7'%d]['1']; o['d%d_w7_-1'%d]=f['d%d_w7'%d]['-1']
    return {k:{norm(x) for x in v} for k,v in o.items()}
for sel,tag,path in ((is_keep,'keep',B+'tab_keep95p131/rules_studio_keep95p131.json'),(None,'full','/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/gcoct26/kill_upgraded/tierA/full2ball_extra_rules.json')):
    R=rules_for(sel); F=fromfile(path)
    for k in F:
        mine={norm(json.loads(json.dumps(x))) for x in R[k]}
        print('rules',tag,k,'file',len(F[k]),'mine',len(mine),'mine-not-file',len(mine-F[k]),'file-not-mine',len(F[k]-mine))
