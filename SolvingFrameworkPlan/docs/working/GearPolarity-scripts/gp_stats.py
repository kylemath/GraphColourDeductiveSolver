import json, sys, collections, math
rows=[]; cls=[]
for f in sys.argv[1:]:
    d=json.load(open(f)); rows+= [dict(r, src=f) for r in d['rows']]; cls += d['cls']
print('DL states', len(rows), 'from', len({r['map'] for r in rows}), 'holes')
dist=collections.Counter(r['dF'] for r in rows); print('dF among DL:', sorted(dist.items()))
def H(cnt):
    n=sum(cnt.values()); return -sum(v/n*math.log2(v/n) for v in cnt.values() if v)
H0=H(dist)
def rank(xs):
    o=sorted(range(len(xs)),key=lambda i:xs[i]); r=[0]*len(xs); i=0
    while i<len(o):
        j=i
        while j+1<len(o) and xs[o[j+1]]==xs[o[i]]: j+=1
        for t in range(i,j+1): r[o[t]]=(i+j)/2
        i=j+1
    return r
def spear(a,b):
    ra,rb=rank(a),rank(b); n=len(a); ma=sum(ra)/n; mb=sum(rb)/n
    c=sum((x-ma)*(y-mb) for x,y in zip(ra,rb)); va=sum((x-ma)**2 for x in ra); vb=sum((y-mb)**2 for y in rb)
    return c/math.sqrt(va*vb) if va and vb else float('nan')
dF=[r['dF'] for r in rows]
feats=['dd','slack','N','l1','l2','shared','kpi','quiet','moves','n']
base=max(dist.values())/len(rows)
print('baseline majority acc %.3f, H(dF)=%.3f bits'%(base,H0))
def condH(keyf):
    g=collections.defaultdict(collections.Counter)
    for r in rows: g[keyf(r)][r['dF']]+=1
    n=len(rows); ch=sum(sum(c.values())/n*H(c) for c in g.values())
    acc=sum(max(c.values()) for c in g.values())/n
    mixed=sum(1 for c in g.values() if len(c)>1)
    return ch,acc,len(g),mixed
for f in feats:
    ch,acc,ng,mixed=condH(lambda r:r[f])
    print('%-7s spearman %+.3f  H(dF|f)=%.3f  majority-acc %.3f  groups %d (mixed %d)'%(f,spear([r[f] for r in rows],dF),ch,acc,ng,mixed))
# exact: dd=0 => dF=2
print('dd=0 dF dist', collections.Counter(r['dF'] for r in rows if not r['dd']))
print('dd=1 dF dist', collections.Counter(r['dF'] for r in rows if r['dd']))
# lock-chain geometry key (the 'nest/cross' structure): (l1,l2,shared,kpi)
for name,kf in [('lockgeom',lambda r:(r['l1'],r['l2'],r['shared'])),('lockgeom+kpi',lambda r:(r['l1'],r['l2'],r['shared'],r['kpi'])),
                ('all feats',lambda r:tuple(r[f] for f in feats)),('all minus n',lambda r:tuple(r[f] for f in feats if f!='n'))]:
    ch,acc,ng,mixed=condH(kf); print('%-13s H(dF|key)=%.3f  majority-acc %.3f  groups %d mixed %d'%(name,ch,acc,ng,mixed))
# counterexample: same all-feature key, different dF
g=collections.defaultdict(list)
for r in rows: g[tuple(r[f] for f in feats)].append(r)
for k,v in g.items():
    if len({r['dF'] for r in v})>1:
        a=min(v,key=lambda r:r['dF']); b=max(v,key=lambda r:r['dF'])
        print('counterexample key',dict(zip(feats,k)),'->',(a['map'],a['k'],a['dF']),(b['map'],b['k'],b['dF'])); break
# class level: winding vs odd_total
print('classes',len(cls))
ws=[c['w'] for c in cls]; ot=[c['odd_total']/(c['U']+c['F']) for c in cls]
print('class winding w=(U-3F)/5 distribution', collections.Counter(int(w) if w==int(w) else w for w in ws).most_common(12))
print('spearman(odd rings per state, w/|S|) = %.3f'%spear(ot,[c['w']/(c['U']+c['F']) for c in cls]))
print('spearman(odd rings per state, filled share) = %.3f'%spear(ot,[c['F']/(c['U']+c['F']) for c in cls]))
