import sys,collections
from lib import parse,adj
from exh import graphs
from pat import comp,classify,canon
from rules import swap,ring
fn=sys.argv[1]; h=int(sys.argv[2]); want=int(sys.argv[3])
G=graphs(fn); n,F=G[0]; Ad=adj(n,F); d=[len(a) for a in Ad]
out=__import__('subprocess').run(['./censusd',fn,'--dump','--hole',str(h)],capture_output=True,text=True).stdout
recs,links,dls=parse(out); L=links[(0,h)]; ld=[d[x] for x in L]; pp=L[ld.index(max(ld))]
print('n',n,'hole',h,'link',L,'degs',ld,'p',pp,'hist',recs[0]['hist_dl'])
shown=0
for j,dd,col in dls[(0,h)]:
    if dd<want: continue
    k=(L.index(pp)-j)%5; X=[L[(j+t)%5] for t in range(5)]; a,b,gg,de=col[X[0]],col[X[1]],col[X[3]],col[X[4]]; nm={a:'a',b:'b',gg:'g',de:'d'}
    W=ring(Ad,X,h); pat=''.join(nm[col[w]] for w in W)
    K=comp(Ad,col,a,b,X[1],h)
    # BFS path inside K from x1 to w3
    par={X[1]:None}; q=[X[1]]
    for u in q:
        for w in Ad[u]:
            if w in K and w not in par and w!=h: par[w]=u; q.append(w)
    path=[];u=W[3] if W[3] in par else None
    while u is not None: path.append(u); u=par[u]
    print('radius',dd,'k',k,'pattern',pat,'|K_ab(x1)|',len(K),'w3 in K',W[3] in K,'path x1->w3 in K:',[ (u,nm[col[u]],'p-nbr' if u in Ad[pp] else '', 'deg%d'%d[u]) for u in path[::-1]])
    shown+=1
    if shown>=3: break
