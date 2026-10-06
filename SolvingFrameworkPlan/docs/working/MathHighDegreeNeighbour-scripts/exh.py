import collections,sys
from lib import parse,adj
def graphs(fn):
    G=[]
    for l in open(fn):
        if l[0]!='G': continue
        t=l.split(); n=int(t[1]); nf=int(t[3]); x=list(map(int,t[4:4+3*nf])); G.append((n,[tuple(x[3*i:3*i+3]) for i in range(nf)]))
    return G
if __name__=='__main__':
  tab=collections.defaultdict(lambda:[0,0,collections.Counter(),collections.defaultdict(int)])
  for N in [12,14,15,16,17,18,19,20,21,22]:
      G=graphs(f'g{N}.txt'); recs,links,dls=parse(open(f'c{N}.txt').read())
      for r in recs:
          g,v=r['g'],r['v']; n,F=G[g]; Ad=adj(n,F); d=[len(a) for a in Ad]; L=links[(g,v)]
          ld=[d[x] for x in L]; top=max(ld); kp=ld.index(top)
          if sorted(ld)[-2]>=7 or top<7: continue
          oth=max(sorted(ld)[:-1]); key=(top,'o5' if oth<=5 else 'o6' if oth<=6 else 'o<=11',r['sep'])
          e=tab[key]; e[0]+=1; e[1]+=r['ndl']; e[2].update({i:c for i,c in enumerate(r['hist_dl'])})
          for j,dd,col in dls[(g,v)]: e[3][(kp-j)%5]=max(e[3][(kp-j)%5],dd)
          if r['unreached']: print('UNREACHED',N,g,v)
  for k in sorted(tab): e=tab[k]; print(k,'holes',e[0],'DL',e[1],'radius hist',dict(e[2]),'max radius by pos of p rel. j',dict(sorted(e[3].items())))
