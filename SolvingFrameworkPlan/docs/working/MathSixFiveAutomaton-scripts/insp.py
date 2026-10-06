from fix import *  # reruns; fine (fast)
import collections
S=lambda c:''.join('abgd'[x] for x in c[:5])+'|'+''.join('abgd'[x] for x in c[5:])
# stats on bad nodes
cnt=collections.Counter()
for n in bad:
    c,T,R=n
    L=locks_of_c=None
    j,l1,l2=DLlocks(c)
    st=[]
    for l in (l1,l2):
        if lockT(l)==T: st.append('L' if has_lock(c,R,l) else 'nol')
    cnt[(T==3-lockT(l1)-lockT(l2), tuple(st))]+=1
print('bad node stats (is non-lock type, lock status in own type):',cnt)
cs={n[0] for n in bad}; print('distinct link+ring colourings in bad set',len(cs))
# ring patterns of bad colourings in canonical DL frame: check endpoint conditions
def endpoint_ok(c):
    j,l1,l2=DLlocks(c)
    x1,x3,x4=(j+1)%5,(j+3)%5,(j+4)%5
    out=lambda t:[c[5+(2*t-2)%10],c[5+(2*t-1)%10],c[5+(2*t)%10]]
    L=c[:5]
    return L[x3] in out(x1) and L[x4] in out(x1) and L[x1] in out(x3) and L[x1] in out(x4)
print('bad colourings satisfying endpoint conditions:',sum(endpoint_ok(c) for c in cs),'of',len(cs))
# per pattern: which types have bad initial structures
tc=collections.Counter(tuple(any(n in bad for n in per[T]) for T in range(3)) for p,per in inits)
print(tc)
