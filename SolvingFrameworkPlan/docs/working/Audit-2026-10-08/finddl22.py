import random,sys
E=[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 5), (1, 6), (1, 7), (2, 3), (2, 7), (2, 8), (3, 4), (3, 8), (3, 9), (3, 10), (4, 5), (4, 10), (4, 11), (4, 12), (5, 6), (5, 12), (5, 13), (6, 7), (6, 13), (6, 14), (6, 15), (7, 8), (7, 15), (7, 16), (8, 9), (8, 16), (8, 17), (9, 10), (9, 17), (9, 18), (10, 11), (10, 18), (11, 12), (11, 18), (11, 19), (11, 20), (12, 13), (12, 20), (13, 14), (13, 20), (14, 15), (14, 19), (14, 20), (14, 21), (15, 16), (15, 21), (16, 17), (16, 21), (17, 18), (17, 19), (17, 21), (18, 19), (19, 20), (19, 21)]
n=22
adj={v:set() for v in range(n)}
for a,b in E: adj[a].add(b); adj[b].add(a)
h=0
X=[1,2,3,4,5]  # rotation order around 0 per nextTable row0: next(0,1)=5? check cyclic adjacency
# verify cycle
for i in range(5): assert X[(i+1)%5] in adj[X[i]], (X[i],X[(i+1)%5])
def comp(c,p,q,s):
    act=lambda v: v!=h and c[v] in (p,q)
    seen={s};st=[s]
    while st:
        u=st.pop()
        for w in adj[u]:
            if act(w) and w not in seen: seen.add(w);st.append(w)
    return seen
def colour():
    order=list(range(1,n)); c=[None]*n; c[0]=0
    def bt(i):
        if i==len(order): return True
        v=order[i]; cs=list(range(4)); random.shuffle(cs)
        for k in cs:
            if all(c[w]!=k for w in adj[v] if w!=h and c[w] is not None):
                c[v]=k
                if bt(i+1): return True
        c[v]=None; return False
    bt(0); return c
random.seed(1)
for t in range(200000):
    c=colour()
    for j in range(5):
        x=lambda k: X[(j+k)%5]
        L=[c[x(k)] for k in range(5)]
        if L[0]==L[2] and len(set([L[0],L[1],L[3],L[4]]))==4:
            if x(3) in comp(c,L[1],L[3],x(1)) and x(4) in comp(c,L[1],L[4],x(1)):
                print("FOUND",c,j); sys.exit()
print("none")
