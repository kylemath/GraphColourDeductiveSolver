"""Named old-graph checks of Lemma A/E and an interlock overclaim."""
import json
from collections import Counter
from pathlib import Path
from wp18_independent import ROOT, canon, deletion_starts, parse_graph, replay, successors, target


def comp(rot,s,pair,seed,exclude=()):
    if seed in exclude:return set()
    seen={seed};todo=[seed]
    while todo:
        for w in rot[todo.pop()]:
            if w not in seen and w not in exclude and s[w] in pair:
                seen.add(w);todo.append(w)
    return seen


def swap(s,pair,c):
    a,b=pair;t=list(s)
    for w in c:t[w]=b if s[w]==a else a
    return tuple(t)


def main():
    graphs=json.loads((ROOT/'wp18'/'wp18-P1.json').read_text())['graphs']
    counts=Counter();counter=None
    for n,idx in ((12,0),(14,0),(17,0),(17,1)):
        g=next(g for g in graphs if (g['order'],g['graph_index'])==(n,idx));rot=parse_graph(g['ascii'])
        for h in range(n):
            if len(rot[h])!=5:continue
            for s in deletion_starts(rot,h):
                link=rot[h];cols=[s[w] for w in link]
                if len(set(cols))!=4:continue
                repeated=next(c for c,k in Counter(cols).items() if k==2)
                i=next(i for i in range(5) if cols[i]==cols[(i+2)%5]==repeated)
                a0,b,a2,gg,d=[link[(i+j)%5] for j in range(5)]
                alpha,beta,gamma,delta=s[a0],s[b],s[gg],s[d]
                gap=gg in comp(rot,s,(beta,gamma),b) and d in comp(rot,s,(beta,delta),b)
                one=any(target(rot,t) for mv,t in successors(rot,s))
                assert one==(not gap);counts['Lemma_A_four_colour_states']+=1
                if not gap:continue
                C=comp(rot,s,(alpha,gamma),a0)
                xg=gg not in comp(rot,s,(beta,gamma),b,C)
                D0=comp(rot,s,(alpha,delta),a2)
                xd=d not in comp(rot,s,(beta,delta),b,D0)
                t=swap(s,(alpha,gamma),C)
                D=comp(rot,t,(alpha,delta),a2)
                end=swap(t,(alpha,delta),D);fills=target(rot,end)
                assert xg or fills;counts['Lemma_E_gap_states']+=1
                if xg and fills:
                    counts['Xg_true_but_KPg_fills']+=1
                    if xd:counts['full_X_true_but_KPg_fills']+=1
                    if xd and counter is None:
                        names={}
                        for col in t:
                            if col!=4 and col not in names:names[col]=len(names)
                        path=[['K',alpha,gamma,min(C)],['K',names[alpha],names[delta],min(D)]]
                        replay(rot,s,path)
                        counter={'order':n,'graph_index':idx,'hole':h,'start':list(s),
                                 'roles':{'a0':a0,'b':b,'a2':a2,'g':gg,'d':d},
                                 'colours':[alpha,beta,gamma,delta],
                                 'C0':sorted(C),'D2':sorted(D0),'Xg':True,'Xd':True,
                                 'KPg_fills':True,'path':path}
    assert counter is not None
    out={'scope':'named old graphs12:0,14:0,17:0,17:1 only',
         'counts':dict(counts),'interlock_converse_counterexample':counter,
         'conclusion':'Lemma E necessity passes; Xg does not imply KPg failure'}
    Path(__file__).with_name('math-mechanism-review-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',dict(counts),'counterexample',counter,flush=True)


if __name__=='__main__':main()
