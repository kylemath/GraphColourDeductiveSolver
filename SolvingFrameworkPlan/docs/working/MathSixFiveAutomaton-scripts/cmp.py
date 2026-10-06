import pickle, collections
from auto import *
def canon(c,T):
    m={}
    for x in c: m.setdefault(x,len(m))
    for x in range(4): m.setdefault(x,len(m))
    c2=tuple(m[x] for x in c)
    P=TYPES[T][0]; return c2,type_of(m[P[0]],m[P[1]])
def norm(lc,T,R):
    lab=list(R)
    cls=[lc[5+i] in TYPES[T][0] for i in range(10)]
    for i in range(10):
        j=(i+1)%10
        if cls[i]==cls[j] and lab[i]!=lab[j]:
            a,b=lab[i],lab[j]; lab=[a if z==b else z for z in lab]
    return canonR(lab)
nodes,groups,bad,inits=pickle.load(open('fix.pkl','rb'))
pats=set(open('../six/local.txt').read().split())
st=collections.Counter(); viol=0
for fn in ('real22.pkl','real23.pkl'):
    for f,line,res in pickle.load(open(fn,'rb')):
        for v,lc,rad,Rs in res:
            Rs=[norm(lc,T,Rs[T]) for T in range(3)]
            pat=''.join('abgd'[x] for x in lc[5:])
            assert pat in pats, pat
            for T in range(3):
                assert canonR(Rs[T]) in [canonR(R) for R in structures(lc,T)], (pat,T,Rs[T])
            # abstract value with actual structures
            val=None
            for k in range(1,6):
                if any(g(k,lc,T,canonR(Rs[T])) for T in range(3)): val=k;break
            if val is not None and val<rad: viol+=1
            inb=tuple((lambda cc,TT:(cc,TT,canonR(Rs[T])) in bad)(*canon(lc,T)) for T in range(3))
            st[(rad,val,inb)]+=1
print('soundness violations (abstract bound < true radius):',viol)
for k,v in sorted(st.items(),key=str): print(k,v)
