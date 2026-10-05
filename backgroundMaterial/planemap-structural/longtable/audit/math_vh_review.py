"""Independent class/containment/U replay on the existing 118 old graphs only."""
import json
from collections import Counter
from pathlib import Path
from wp18_independent import ROOT, deletion_starts, fans, parse_graph, successors, target


def components(rot,states):
    universe=set(states);unseen=set(states);out=[]
    while unseen:
        s=unseen.pop();todo=[s];comp=[s]
        while todo:
            for mv,t in successors(rot,todo.pop()):
                if mv[0]!='K':continue
                assert t in universe
                if t in unseen:unseen.remove(t);todo.append(t);comp.append(t)
        out.append(comp)
    return out


def main():
    graphs=[]
    for phase in ('P1','P2'):
        graphs+=json.loads((ROOT/'wp18'/('wp18-'+phase+'.json')).read_text())['graphs']
    rows=[];pairs=ufail=contain=0;kt_bad=[]
    for g in graphs:
        rot=parse_graph(g['ascii']);legal=fans(rot);data={};us=[];kts=[]
        for v in sorted({v for v,i in legal}):
            starts=deletion_starts(rot,v)
            comps=components(rot,starts);labels={s:i for i,c in enumerate(comps) for s in c}
            unlocked={s:(target(rot,s) or any(target(rot,t) for mv,t in successors(rot,s) if mv[0]=='K')) for s in starts}
            data[v]=(starts,labels,unlocked)
        pair_rows=[]
        for (v,i),ch in legal.items():
            starts,labels,unlocked=data[v]
            S=[s for s in starts if all(s[a]!=s[b] for a,b in ch)]
            assert S
            assert all(sum(s[w]==s[rot[v][i]] for w in rot[v])==1 for s in S)
            augmented=[list(row) for row in rot]
            for a,b in ch:augmented[a].append(b);augmented[b].append(a)
            classes=components(augmented,S)
            for c in classes:assert len({labels[s] for s in c})==1;contain+=1
            bad=sum(not any(unlocked[s] for s in c) for c in classes)
            u=(bad==0);kt=all(any(target(rot,s) for s in c) for c in classes)
            us.append(u);kts.append(kt);pairs+=1;ufail+=not u
            pair_rows.append({'v':v,'fan':i,'starts':len(S),'classes':len(classes),'locked_classes':bad,'U':u,'KTstar':kt})
        assert any(us)
        if not any(kts):kt_bad.append([g['order'],g['graph_index']])
        rows.append({'order':g['order'],'index':g['graph_index'],'pairs':pair_rows,'U_exists':any(us)})
    assert len(graphs)==118 and pairs==7930 and ufail==41 and len(kt_bad)==16
    out={'scope':'existing 118 graphs through20; secondary reading for19-20',
         'graphs':len(graphs),'pairs':pairs,'U_failing_pairs':ufail,'U_exists_graphs':len(graphs),
         'containment_classes_checked':contain,'containment_failures':0,
         'KTstar_exists_failure_graphs':kt_bad,'rows':rows}
    Path(__file__).with_name('math-vh-review-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS:118graphs,7930pairs,41U-failpairs,16KTstar-existsfailuregraphs; containment and apex singleton pass',flush=True)


if __name__=='__main__':main()
