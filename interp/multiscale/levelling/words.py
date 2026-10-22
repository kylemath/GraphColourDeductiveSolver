# [P-check] For every gauge sign pattern s (length m, both closure parities), is there a proper boundary word
# using exactly 3 colours (so realizable by a triangulated polygon) whose walk has tau <= 1 (resp. sqrt(3)/2)?
# Also brute-force check: every proper 3-colouring of C_m using all 3 colours is the 3-colouring of some
# triangulated polygon (ear argument).
import itertools, math, functools
from lev import INC, n2
def walk(word, s):
    H=[(0,0)]
    for i in range(len(word)):
        l=word[i]^word[(i+1)%len(word)]; d=INC[l]; H.append((H[-1][0]+s[i]*d[0],H[-1][1]+s[i]*d[1]))
    return H
def tau(word,s,odd):
    H=walk(word,s)
    if odd:
        q=((H[0][0]+H[-1][0])/2,(H[0][1]+H[-1][1])/2); return math.sqrt(max(n2((h[0]-q[0],h[1]-q[1])) for h in H))
    As=[h[0] for h in H]; Bs=[h[1] for h in H]
    return math.sqrt(min(max(n2((h[0]-A,h[1]-B)) for h in H) for A in range(min(As)-1,max(As)+2) for B in range(min(Bs)-1,max(Bs)+2)))
@functools.lru_cache(None)
def polygon_ok(word):
    m=len(word)
    if m==3: return len(set(word))==3
    for i in range(m):
        a,b=word[i-1],word[(i+1)%m]
        if a!=b:
            w2=word[:i]+word[i+1:]
            if polygon_ok(w2): return True
    return False
# ear lemma check
for m in range(3,11):
    bad=0
    for w in itertools.product(range(3),repeat=m):
        if w[0]!=0: continue
        if all(w[i]!=w[(i+1)%m] for i in range(m)) and len(set(w))==3 and not polygon_ok(w): bad+=1
    print('m',m,'proper 3-col words using 3 colours not realizable:',bad)
words={}
for m in range(4,15):
    W=[w for w in itertools.product(range(3),repeat=m) if w[0]==0 and all(w[i]!=w[(i+1)%m] for i in range(m)) and len(set(w))==3]
    worst={}
    for sp in itertools.product([1,-1],repeat=m-1):
        s=(1,)+sp
        # closure parity: odd iff product of flips around != 1; here s_i free, parity determined by s_m vs s_0 via k_0
        for odd in (False,True):
            best=min(tau(w,s,odd) for w in W)
            key=(odd, sum(s)%3 if not odd else None)
            worst[key]=max(worst.get(key,0),best)
    print('m',m,{k:round(v,3) for k,v in worst.items()},flush=True)
