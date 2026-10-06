# strict check of the transition table of Theorem HP (one free link vertex p, the other four of degree 5)
import sys,collections,subprocess
from lib import parse,adj
from exh import graphs
from pat import comp,classify,canon
from rules import swap,ring
EASY={(0,'dgbab'):'F',(2,'dgbab'):'B',(1,'dgbab'):'B',(1,'ddbab'):'B',(1,'ggbab'):'F',(3,'dgbab'):'B',(3,'dgdab'):'B',(3,'dgbbg'):'F',(3,'dgdbg'):'AB',
      (4,'dgbab'):'B',(4,'dgdbb'):'B',(4,'dgbag'):'F',(4,'dgdbg'):'AB'}
D={}
for key in EASY: D[key]=1
D[(1,'R1')]=2;D[(2,'R1')]=2;D[(0,'R1')]=2;D[(0,'R3')]=3;D[(2,'R3')]=3;D[(3,'R1')]=4;D[(4,'R1')]=4;D[(1,'R3')]=5
def typ(Ad,col,L,v,pp):
    t,j=classify(Ad,col,L,v)
    if t!='DL': return None
    k=(L.index(pp)-j)%5; X=[L[(j+i)%5] for i in range(5)]
    a,b,gg,de=col[X[0]],col[X[1]],col[X[3]],col[X[4]]; nm={a:'a',b:'b',gg:'g',de:'d'}
    pat=''.join(nm[col[w]] for w in ring(Ad,X,v))
    if (k,pat) in EASY: return (k,pat)
    if pat=='gdbab': return (k,'R1')
    if pat=='dgdbg': return (k,'R3')
    return (k,'UNKNOWN '+pat)
def run(fn,h):
    G=graphs(fn); out=subprocess.run(['./censusd',fn,'--dump']+(['--hole',str(h)] if h is not None else []),capture_output=True,text=True,check=True).stdout
    recs,links,dls=parse(out); bad=collections.Counter(); ok=0; mx=collections.defaultdict(int)
    for r in recs:
        g,v=r['g'],r['v']; n,F=G[g]; Ad=adj(n,F); d=[len(a) for a in Ad]; L=links[(g,v)]; ld=[d[x] for x in L]
        if r['sep'] or sorted(ld)[-2]!=5 or max(ld)<6: continue
        pp=L[ld.index(max(ld))]
        for j,dd,col in dls[(g,v)]:
            T=typ(Ad,col,L,v,pp); X=[L[(j+i)%5] for i in range(5)]; a,b,gg,de=col[X[0]],col[X[1]],col[X[3]],col[X[4]]
            if 'UNKNOWN' in T[1]: bad[T]+=1; continue
            mx[T]=max(mx[T],dd)
            if dd>1+D[T]: bad[('radius exceeds bound',T)]+=1
            Fs=swap(Ad,col,a,gg,X[2],v)[0]; Bs=swap(Ad,col,a,de,X[0],v)[0]; ABs=swap(Ad,col,a,b,X[1],v)[0]
            k=T[0]
            if T in EASY:
                img={'F':Fs,'B':Bs,'AB':ABs}[EASY[T]]
                if typ(Ad,img,L,v,pp) is not None: bad[('easy swap fails',T)]+=1
                continue
            other='R3' if T[1]=='R1' else 'R1'
            tf=typ(Ad,Fs,L,v,pp); tb=typ(Ad,Bs,L,v,pp)
            if tf not in (None,((k-3)%5,other)): bad[('F image',T,tf)]+=1
            if tb not in (None,((k+3)%5,other)): bad[('B image',T,tb)]+=1
            ok+=1
    return dict(bad),dict(sorted(mx.items()))
if __name__=='__main__':
    h=None if sys.argv[1]=='all' else int(sys.argv[1])
    for fn in sys.argv[2:]: print(fn,run(fn,h),flush=True)
