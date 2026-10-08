exec(open('finddl22.py').read().split('random.seed')[0])
c=[0, 3, 2, 1, 0, 1, 0, 1, 0, 2, 3, 1, 2, 3, 1, 3, 2, 3, 0, 2, 0, 0]
def path(p,q,s,t):
    act=lambda v: v!=h and c[v] in (p,q)
    prev={s:None};st=[s]
    while st:
        u=st.pop(0)
        for w in adj[u]:
            if act(w) and w not in prev: prev[w]=u;st.append(w)
    P=[t]
    while prev[P[-1]] is not None: P.append(prev[P[-1]])
    return P[::-1]
print(path(0,3,4,1)); print(path(0,2,4,2))
