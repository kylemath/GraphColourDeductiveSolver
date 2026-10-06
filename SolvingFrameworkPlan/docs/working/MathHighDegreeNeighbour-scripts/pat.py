import collections,sys,pickle
from lib import parse,adj
from exh import graphs
def comp(Ad,c,a,b,s,skip):
    seen={s}; st=[s]
    while st:
        u=st.pop()
        for w in Ad[u]:
            if w!=skip and w not in seen and c[w] in (a,b): seen.add(w); st.append(w)
    return seen
def classify(Ad,c,L,h):
    cols=[c[x] for x in L]
    if len(set(cols))<=3: return ('F',None)
    j=[t for t in range(5) if cols[t]==cols[(t+2)%5]][0]
    x1,x3,x4=L[(j+1)%5],L[(j+3)%5],L[(j+4)%5]
    be,ga,de=c[x1],c[x3],c[x4]
    l1=x3 in comp(Ad,c,be,ga,x1,h); l2=x4 in comp(Ad,c,be,de,x1,h)
    return ('DL' if l1 and l2 else 'NL', j)
def canon(c,h):
    mp={};o=[]
    for i,x in enumerate(c):
        if i==h: o.append(-1); continue
        if x not in mp: mp[x]=len(mp)
        o.append(mp[x])
    return tuple(o)
