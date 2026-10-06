from auto import *
import sys, collections
def nblocks(R): return len(set(R))
def locks_of(c):
    if filled(c): return []
    j,l1,l2=DLlocks(c); return [l1,l2]
def sigma(c,T,mode):
    best=None;bk=None
    Ls=[l for l in locks_of(c) if lockT(l)==T]
    for R in structures(c,T):
        R=canonR(R)
        nl=sum(has_lock(c,R,l) for l in Ls)
        if mode=='min': key=(-nl,nblocks(R),R)
        elif mode=='max': key=(-nl,-nblocks(R),R)
        if bk is None or key<bk: bk=key;best=R
    return best
def search(mode,limit=2000000):
    seen={}; Q=collections.deque()
    for p in pats:
        c=init(p)
        st=(c,)+tuple(sigma(c,T,mode) for T in range(3))
        # initial must be DL
        assert all(has_lock(c,st[1+lockT(l)],l) for l in locks_of(c)),p
        seen[st]=None; Q.append(st)
    while Q:
        st=Q.popleft(); c=st[0]; Rs=st[1:]
        for p,q in itertools.combinations(range(4),2):
            T=type_of(p,q)
            for K in comps(c,p,q,Rs[T]):
                c2=flip(c,K,p,q)
                if filled(c2): return ('FILLED',st,(p,q,sorted(K)),seen)
                if all(v<5 for v in K): R2=Rs
                else: R2=tuple(Rs[T] if T2==T else sigma(c2,T2,mode) for T2 in range(3))
                s2=(c2,)+R2
                if s2 not in seen:
                    seen[s2]=st; Q.append(s2)
                    if len(seen)>limit: return ('LIMIT',None,None,seen)
    return ('CLOSED',None,None,seen)
if __name__=='__main__':
    for mode in sys.argv[1:]:
        r,st,mv,seen=search(mode)
        print(mode,r,len(seen),flush=True)
        if r=='FILLED':
            path=[]; s=st
            while s is not None: path.append(s); s=seen[s]
            for s in reversed(path): print(' ',''.join('abgd'[x] for x in s[0][:5]),''.join('abgd'[x] for x in s[0][5:]),s[1:])
            print('  move',mv)
