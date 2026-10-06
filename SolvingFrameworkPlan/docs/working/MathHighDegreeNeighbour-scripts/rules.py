import collections,sys
from lib import parse,adj
from exh import graphs
from pat import *
want=sys.argv[1] if len(sys.argv)>1 else 'o5'
def swap(Ad,col,p,q,s,v):
    K=comp(Ad,col,p,q,s,v); c2=list(col)
    for u in K: c2[u]= q if col[u]==p else p
    return c2,K
def ring(Ad,X,v):
    return [ [w for w in Ad[X[t]]&Ad[X[(t+1)%5]] if w!=v][0] for t in range(5)]
if __name__=='__main__':
    stats=collections.defaultdict(collections.Counter); bad=collections.Counter(); ex={}
    for N in [16,17,18,19,20,21,22]:
        G=graphs(f'g{N}.txt'); recs,links,dls=parse(open(f'c{N}.txt').read())
        for r in recs:
            g,v=r['g'],r['v']; n,F=G[g]; Ad=adj(n,F); d=[len(a) for a in Ad]; L=links[(g,v)]
            ld=[d[x] for x in L]; top=max(ld)
            if top<7 or sorted(ld)[-2]>(5 if want=='o5' else 6) or r['sep']: continue
            kp=ld.index(top)
            dist={canon(col,v):dd for j,dd,col in dls[(g,v)]}
            for j,dd,col in dls[(g,v)]:
                k=(kp-j)%5; X=[L[(j+t)%5] for t in range(5)]
                a,b,gg,de=col[X[0]],col[X[1]],col[X[3]],col[X[4]]
                nm={a:'a',b:'b',gg:'g',de:'d'}
                W=ring(Ad,X,v); pat=''.join(nm[col[w]] for w in W)
                def nd(c2): 
                    t,_=classify(Ad,c2,L,v); return 0 if t!='DL' else dist[canon(c2,v)]
                Fs,_=swap(Ad,col,a,gg,X[2],v); Bs,_=swap(Ad,col,a,de,X[0],v); ABs,K=swap(Ad,col,a,b,X[1],v)
                f,bb,ab=nd(Fs),nd(Bs),nd(ABs)
                # starvation predicates
                Fst= not any(col[y]==de for y in Ad[X[2]] if y!=v)
                Bst= not any(col[y]==gg for y in Ad[X[0]] if y!=v)
                key=(k,pat)
                stats[key][('r',dd)]+=1
                if Fst and f!=0: bad['Fstarve-fail']+=1
                if Bst and bb!=0: bad['Bstarve-fail']+=1
                stats[key][('F0' if f==0 else 'F%d'%f)]+=1; stats[key][('B0' if bb==0 else 'B%d'%bb)]+=1; stats[key][('AB0' if ab==0 else 'AB%d'%ab)]+=1
                stats[key][('Kclosed',len(K)==3)]+=1
                if Fst: stats[key]['Fst']+=1
                if Bst: stats[key]['Bst']+=1
    print('starvation rule failures (must be 0):',dict(bad))
    for key in sorted(stats):
        s=stats[key]; print(key, dict(sorted(((str(a),b) for a,b in s.items()))))
    