"""Independent named-17:1 diagonal and distance-three witness check."""
import itertools
import json
from collections import Counter
from pathlib import Path
from wp18_independent import ROOT, deletion_starts, distance, fans, parse_graph, replay, state_ok, successors


def main():
    g=next(g for g in json.loads((ROOT/'wp18'/'wp18-P1.json').read_text())['graphs']
           if (g['order'],g['graph_index'])==(17,1))
    rot=parse_graph(g['ascii']);legal=fans(rot);rows=[]
    report={(r['v'],r['fan_index']):r for r in g['report']['rows']}
    for v in sorted({v for v,i in legal}):
        starts=deletion_starts(rot,v);far=set();ells={};diags={}
        for s in starts:
            ell=distance(rot,s,4);assert ell is not None;ells[s]=ell
            cols=[s[w] for w in rot[v]]
            if len(set(cols))==4:
                repeated=next(c for c,n in Counter(cols).items() if n==2)
                d=tuple(i for i,c in enumerate(cols) if c==repeated)
                assert len(d)==2 and (d[1]-d[0])%5 in (2,3)
                diags[s]=d
                if ell>=3:far.add(d)
        lengths=[]
        for i in range(5):
            chords=legal[v,i]
            S=[s for s in starts if all(s[a]!=s[b] for a,b in chords)]
            for s in diags:assert (s in S)==(i not in diags[s])
            L=max(ells[s] for s in S);assert L==report[v,i]['L']
            assert (L<=2)==all(i in d for d in far)
            lengths.append(L)
        crossing=any(not set(a)&set(b) for a,b in itertools.combinations(far,2))
        assert crossing==all(x>=3 for x in lengths)
        rows.append({'vertex':v,'far_diagonals':sorted(far),'fan_L':lengths,'crossing':crossing})
    s=(0,1,2,1,3,2,3,4,0,3,0,2,1,0,1,2,3)
    state_ok(rot,s,7)
    assert distance(rot,s,2) is None and distance(rot,s,3)==3
    path=[['K',0,3,0],['K',1,2,1],['K',1,3,1]]
    replay(rot,s,path)
    neighbours={t for move,t in successors(rot,s)}-{s}
    assert len(neighbours)==6
    assert all(distance(rot,t,1) is None for t in neighbours)
    out={'scope':'named graph17:1, all12 degree-five roots, all60 fans',
         'rows':rows,'witness_vertex':7,'witness':s,'distance':3,'path':path,
         'nontrivial_distinct_neighbours':len(neighbours),'shorter_layers_excluded':True}
    Path(__file__).with_name('math-diagonal-review-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: diagonal/fan criterion all60pairs; witness distance exactly3, six neighbours each unfillable in one move')


if __name__=='__main__':main()
