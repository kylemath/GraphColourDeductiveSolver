# symbolic local colours along one period at a (5,5,5,5,6) hole, q = 0 (p = x0), actual colours
roles=[(1,2,3),(3,1,2),(2,3,1)]  # (mu,A,B) by i mod 3, alpha=0
types=['R3','R1']*5
q=0
names=['R3k4','R1k1','R3k3','R1k0','R3k2','R1k4','R3k1','R1k3','R3k0','R1k2']
def state(i,b=0):
    t=i%10; ty=types[t]; k=int(names[t][-1]); j=(q-k)%5
    mu,A,B=roles[(10*b+t)%3]; al=0
    x={}; w={}
    lc=[al,mu,al,A,B]
    for r in range(5): x[(j+r)%5]=lc[r]
    rc=[B,A,B,mu,A] if ty=='R3' else [A,B,mu,al,mu]
    for r in range(5): w[(j+r)%5]=rc[r]
    p=x[q]; y=w[(q-1)%5]; z=w[q]
    mcol=({0,1,2,3}-{p,y,z}).pop()
    return dict(ty=ty,k=k,j=j,al=al,mu=mu,A=A,B=B,x=x,w=w,m=mcol)
nm=lambda d,c: {v:k for k,v in [('al',d['al']),('mu',d['mu']),('A',d['A']),('B',d['B'])]}[c]
for b in range(2):
  for t in range(10):
    s=state(t,b); s2=state(t+1, b+(t==9)) if t<9 else state(0,b+1)
    j=s['j']
    loc={'x%d'%r:s['x'][r] for r in range(5)}; loc.update({'w%d'%r:s['w'][r] for r in range(5)}); loc['m']=s['m']
    loc2={'x%d'%r:s2['x'][r] for r in range(5)}; loc2.update({'w%d'%r:s2['w'][r] for r in range(5)}); loc2['m']=s2['m']
    pair={s['al'],s['A']}
    chg=[v for v in loc if loc[v]!=loc2[v]]
    bad=[v for v in chg if not ({loc[v],loc2[v]}==pair)]
    # roles of p m y z
    rl={'p':nm(s,s['x'][0]),'m':nm(s,s['m']),'y':nm(s,s['w'][4]),'z':nm(s,s['w'][0])}
    J=(s['w'][4],s['w'][0])
    print(b,t,names[t],'j=%d'%j,'colors x0..4',[s['x'][r] for r in range(5)],'w0..4',[s['w'][r] for r in range(5)],'m',s['m'],
      'roles',rl,'Lock1 x%d~x%d {mu,A}={%d,%d}'%((j+1)%5,(j+3)%5,s['mu'],s['A']),'Lock2 x%d~x%d {mu,B}={%d,%d}'%((j+1)%5,(j+4)%5,s['mu'],s['B']),
      'Jpair',sorted(J),'swap {%d,%d} of x%d'%(s['al'],s['A'],(j+2)%5),'local in K:',chg, 'BAD' if bad else '')
