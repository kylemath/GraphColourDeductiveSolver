exec(open('/tmp/claude-0/ms/vortex_spin.py').read().split('for seed in range(3):')[0])
import collections
# quaternion units as (sign, idx) idx 0=1,1=i,2=j,3=k
def qmul(a,b):
    sa,x=a; sb,y=b
    if x==0: return (sa*sb,y)
    if y==0: return (sa*sb,x)
    if x==y: return (-sa*sb,0)
    z=6-x-y; s=1 if (y-x)%3==1 else -1
    return (sa*sb*s,z)
names={0:'1',1:'i',2:'j',3:'k'}
p,adj=sphere(2000,0); rot=[rotation(p,adj,v) for v in range(len(adj))]
tab=collections.Counter(); tab2=collections.Counter()
for cs in range(3):
    col=colour(adj,cs)
    for v in range(len(adj)):
        L=[col[v]^col[u] for u in rot[v]]
        q=(1,0)
        for l in L: q=qmul(q,(1,l))
        w=winding(col,rot[v],v); d=len(L)
        tab[(d%2,w,('-' if q[0]<0 else '+')+names[q[1]])]+=1
        # product of consecutive 'turns': l_i^{-1} l_{i+1}
        q2=(1,0)
        for i in range(d):
            a,b=L[i],L[(i+1)%d]; q2=qmul(q2,qmul((-1,a),(1,b)))
        tab2[(w,('-' if q2[0]<0 else '+')+names[q2[1]])]+=1
print('label product around v: (deg parity, spin, product) counts'); [print(' ',k,c) for k,c in sorted(tab.items())]
print('turn product: (spin, product)'); [print(' ',k,c) for k,c in sorted(tab2.items())]
tab3=collections.Counter()
for cs in range(3):
    col=colour(adj,cs)
    for v in range(len(adj)):
        L=[col[v]^col[u] for u in rot[v]]; d=len(L); s=1
        for i in range(d): s*=qmul((1,L[i]),(1,L[(i+1)%d]))[0]
        tab3[(d%4,winding(col,rot[v],v)%4,s)]+=1
print('sign of product of consecutive pairs l_i*l_{i+1}: (d mod 4, spin mod 4, sign)'); [print(' ',k,c) for k,c in sorted(tab3.items())]
