# verify hand claims on (graph file, hole h, p) where the other four link vertices have degree 5
import sys,collections
from lib import parse,adj
from exh import graphs
from pat import comp,classify,canon
from rules import swap,ring
ALLOWED={0:{'gdbab','dgdbg','dgbab'},2:{'gdbab','dgdbg','dgbab'},1:{'dgdbg','gdbab','dgbab','ddbab','ggbab'},
         3:{'gdbab','dgbab','dgdab','dgdbg','dgbbg'},4:{'gdbab','dgbab','dgbag','dgdbg','dgdbb'}}
def check(fn,h=None,p=None,exhaustive_filter=False):
    G=graphs(fn); out=__import__('subprocess').run(['./censusd',fn,'--dump']+(['--hole',str(h)] if h is not None else []),capture_output=True,text=True,check=True).stdout
    recs,links,dls=parse(out); viol=collections.Counter(); mx=collections.defaultdict(int); n_states=0
    for r in recs:
        g,v=r['g'],r['v']; n,F=G[g]; Ad=adj(n,F); d=[len(a) for a in Ad]; L=links[(g,v)]; ld=[d[x] for x in L]
        if r['sep'] or max(ld)<7 or sorted(ld)[-2]!=5: continue
        pp=L[ld.index(max(ld))]
        if r['unreached']: viol['UNREACHED']+=1
        dist={canon(col,v):dd for j,dd,col in dls[(g,v)]}
        def nd(c2):
            t,jj=classify(Ad,c2,L,v); return (0,None) if t!='DL' else (dist[canon(c2,v)],jj)
        for j,dd,col in dls[(g,v)]:
            n_states+=1; k=(L.index(pp)-j)%5; X=[L[(j+t)%5] for t in range(5)]
            a,b,gg,de=col[X[0]],col[X[1]],col[X[3]],col[X[4]]; nm={a:'a',b:'b',gg:'g',de:'d'}
            W=ring(Ad,X,v); pat=''.join(nm[col[w]] for w in W)
            if pat not in ALLOWED[k]: viol['pattern %d %s'%(k,pat)]+=1
            Fs,_=swap(Ad,col,a,gg,X[2],v); Bs,_=swap(Ad,col,a,de,X[0],v); ABs,K=swap(Ad,col,a,b,X[1],v)
            R1,R2,R3=pat=='gdbab',(pat=='dgbab' or (k==3 and pat=='dgdab') or (k==1 and pat in('ddbab','ggbab'))),pat=='dgdbg'
            easy = R2 or (k in(3,4) and pat in('dgbbg','dgbag','dgdbb','dgdbg'))
            if easy and dd>2: viol['easy>2 %d %s'%(k,pat)]+=1
            if R1 and k in (0,1,2):
                if dd>3: viol['R1>3 k%d'%k]+=1
                img=Fs if k in(1,2) else Bs; dI,jI=nd(img)
                if dI and dI>2: viol['R1 image not killable k%d'%k]+=1
            tag=('R1' if R1 else 'R3' if R3 else 'easy'); mx[(k,tag)]=max(mx[(k,tag)],dd)
    return n_states,dict(viol),dict(sorted(mx.items()))
if __name__=='__main__':
    for fn in sys.argv[1:]: print(fn,check(fn,h=2),flush=True)
