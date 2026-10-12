exec(open('finddl22.py').read().split('random.seed')[0])
c=[0, 3, 2, 1, 0, 1, 0, 1, 0, 2, 3, 1, 2, 3, 1, 3, 2, 3, 0, 2, 0, 0]
def ncomp(c,p,q):
    act=[v for v in range(1,n) if c[v] in (p,q)]; seen=set(); k=0
    for s in act:
        if s in seen: continue
        k+=1; seen|=comp(c,p,q,s)
    return k
def N(c): return sum(ncomp(c,p,q) for p in range(4) for q in range(p+1,4))
def dl(c):
    for j in range(5):
        x=lambda k: X[(j+k)%5]; L=[c[x(k)] for k in range(5)]
        if L[0]==L[2] and len(set([L[0],L[1],L[3],L[4]]))==4:
            return j, (x(3) in comp(c,L[1],L[3],x(1))) and (x(4) in comp(c,L[1],L[4],x(1)))
    return None
K=comp(c,1,3,5); d=[ (({1:3,3:1}[c[v]]) if v in K else c[v]) for v in range(n)]
print('N(c)',N(c),'dl',dl(c),'N(pi c)',N(d),'dl(pi c)',dl(d), 'x3 in K?', 3 in K)
