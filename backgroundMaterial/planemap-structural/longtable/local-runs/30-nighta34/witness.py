exec(open('table.py').read().split('nm=lambda')[0])
# local graph, q=0, fixed names: p=x0, x+=x1, x2, x3, x-=x4 ; z=w0, w+=w1, w2, w3, y=w4 ; m
E=set()
def e(a,b): E.add(frozenset((a,b)))
for t in range(5): e('x%d'%t,'x%d'%((t+1)%5))
for t in range(1,5): e('x%d'%t,'w%d'%((t-1)%5)); e('x%d'%t,'w%d'%t)
e('x0','w4'); e('x0','m'); e('x0','w0')
for t in range(4): e('w%d'%t,'w%d'%(t+1))
e('w4','m'); e('m','w0')
NB=lambda v:[ (set(f)-{v}).pop() for f in E if v in f]
link=['x%d'%t for t in range(5)]
nmv={'x0':'p','x1':'x+','x4':'x-','w0':'z','w1':'w+','w4':'y'}
N=lambda v: nmv.get(v,v)
def reduce(col,u,pair):
    # follow forced moves out of link vertices: return set of non-link vertices reachable from u via link vertices only
    seen={u}; st=[u]; out=set()
    while st:
        v=st.pop()
        for t in NB(v):
            if col[t] in pair and t not in seen:
                seen.add(t)
                if t in link: st.append(t)
                else: out.add(t)
    return seen&set(link), out
for b in range(2):
  for t in range(10):
    s=state(t,b); j=s['j']; col={'x%d'%r:s['x'][r] for r in range(5)}; col.update({'w%d'%r:s['w'][r] for r in range(5)}); col['m']=s['m']
    al,mu,A,B=s['al'],s['mu'],s['A'],s['B']
    res=[]
    for nmL,a,bb,end in (('L1',mu,A,(j+3)%5),('L2',mu,B,(j+4)%5)):
        u='x%d'%((j+1)%5); v='x%d'%end
        lu,ou=reduce(col,u,(a,bb)); lv,ov=reduce(col,v,(a,bb))
        joined = bool(lu&lv)
        res.append('%s %s~%s {%d,%d}: %s'%(nmL,N(u),N(v),a,bb,'LOCAL' if joined else '{%s} ~ {%s}'%(','.join(sorted(map(N,ou))),','.join(sorted(map(N,ov))))))
    yv,zv=col['w4'],col['w0']
    print('b%d %d %s j=%d |'%(b,t,names[t],j),' | '.join(res),'| J {%d,%d}'%(yv,zv), ' c(p,m,y,z)=',(col['x0'],col['m'],col['w4'],col['w0']))
