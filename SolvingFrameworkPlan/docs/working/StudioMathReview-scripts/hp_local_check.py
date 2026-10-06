import itertools
# independent local check of HP Lemma 1/2/3 (symbolic ring patterns only)
A,B,G,D='a','b','g','d'
link=[A,B,A,G,D]
allowed=[{G,D},{G,D},{B,D},{A,B},{B,G}]   # w_t not in {c(x_t),c(x_{t+1})}
def patterns(k):
    out=[]
    for w in itertools.product(*[sorted(s) for s in allowed]):
        ok=True
        for t in range(5):                       # x_t degree 5 => w_{t-1}~w_t
            if t!=k and w[(t-1)%5]==w[t]: ok=False
        if k!=1 and set(w[:2])!={G,D}: ok=False      # x1 deg5: P1,P2 leave via w0,w1
        if k!=3 and B not in (w[2],w[3]): ok=False   # P1 enters x3 via b
        if k!=4 and B not in (w[3],w[4]): ok=False   # P2 enters x4 via b
        if ok: out.append(''.join(w))
    return out
claimed={0:{'gdbab','dgbab','dgdbg'},2:{'gdbab','dgbab','dgdbg'},
 1:{'dgdbg','gdbab','dgbab','ddbab','ggbab'},
 3:{'gdbab','dgbab','dgdab','dgbbg','dgdbg'},4:{'gdbab','dgbab','dgbag','dgdbb','dgdbg'}}
for k in range(5):
    P=set(patterns(k)); print(k,sorted(P),'EQUAL' if P==claimed[k] else ('DIFF',P^claimed[k]))
# starvation kills (need x0 / x2 degree 5 i.e. k!=0 / k!=2)
def Bkill(w,k): return k!=0 and G not in (w[4],w[0])   # x0 nbrs: x1=b,x4=d,w4,w0 -> no g
def Fkill(w,k): return k!=2 and D not in (w[1],w[2])   # x2 nbrs: x1=b,x3,w1,w2 -> no d
def R(w): return w in('gdbab','dgdbg')
for k in range(5):
    for w in sorted(set(patterns(k))):
        if w=='gdbab': t='R1'
        elif w=='dgdbg': t='R3'
        else: t='easy?'
        kill=Bkill(w,k) or Fkill(w,k)
        if t=='R3' and k in(3,4): kill='AB'
        print(k,w,t,'kill:',kill)
# transition relabel: F from R1 -> read (w3,w4,w0,w1,w2) with roles (a,d,b,g) after w3:a->g
def reread(ring,roles):  # roles: dict colour->new letter
    return ''.join(roles[c] for c in ring)
r1=list('gdbab'); r1[3]=G                      # F changes w3 a->g
ring=[r1[3],r1[4],r1[0],r1[1],r1[2]]
print('F(R1)',reread(ring,{A:A,D:B,B:G,G:D}))   # a'=a,b'=d,g'=b,d'=g
r3=list('dgdbg'); r3[1]=A                      # F on R3: w1 g->a
ring=[r3[3],r3[4],r3[0],r3[1],r3[2]]
print('F(R3)',reread(ring,{A:A,D:B,B:G,G:D}))
# B from R1: w3 a->d ; frame j'=2, roles b'=g,g'=d,d'=b
r=list('gdbab'); r[3]=D
ring=[r[2],r[3],r[4],r[0],r[1]]; print('B(R1)',reread(ring,{A:A,G:B,D:G,B:D}))
r=list('dgdbg'); r[4]=A                        # B on R3: w4 g->a (adjacent x4? mirror of w1)
ring=[r[2],r[3],r[4],r[0],r[1]]; print('B(R3)',reread(ring,{A:A,G:B,D:G,B:D}))
# B(R3): w0 (d, adjacent x0=a) joins K_B and becomes a; the script above's last line
# changed w4 by mistake. Corrected check:
r=list('dgdbg'); r[0]=A
ring=[r[2],r[3],r[4],r[0],r[1]]
print('B(R3) corrected',reread(ring,{A:A,G:B,D:G,B:D}))   # expect gdbab = R1
