"""Constructive SK checks on four already enumerated fixtures, no new census."""
import itertools
import json
from collections import Counter
from pathlib import Path
from wp18_independent import ROOT, HOLE, deletion_starts, parse_graph, state_ok, successors, target
from math_mechanism_review import comp, swap


def components(rot,s,pair):
    remaining={v for v,c in enumerate(s) if c in pair};out=[]
    while remaining:
        c=comp(rot,s,pair,min(remaining));out.append(c);remaining-=c
    return out


def main():
    graphs=json.loads((ROOT/'wp18'/'wp18-P1.json').read_text())['graphs'];counts=Counter()
    for n,idx in ((12,0),(14,0),(17,0),(17,1)):
        g=next(g for g in graphs if (g['order'],g['graph_index'])==(n,idx));rot=parse_graph(g['ascii'])
        for h in range(n):
            if len(rot[h])!=5:continue
            for s in deletion_starts(rot,h):
                if target(rot,s):continue
                counts['four_colour_starts']+=1
                one=any(target(rot,t) for _,t in successors(rot,s))
                if not one:counts['not_one_move_starts']+=1
                linkcounts=Counter(s[v] for v in rot[h])
                for u in rot[h]:
                    sigma=s[u]
                    if linkcounts[sigma]!=1:continue
                    z=list(s);z[h],z[u]=sigma,HOLE;z=tuple(z)
                    for pair in itertools.combinations(range(4),2):
                        for K in components(rot,z,pair):
                            end=swap(z,pair,K)
                            if not target(rot,end):continue
                            counts['all_SK_fill_paths']+=1
                            missing={c for c in range(4) if c not in {end[v] for v in rot[u]}}
                            if sigma in pair:
                                outside=missing-set(pair)
                                if outside:
                                    x=min(outside);J=comp(rot,s,(sigma,x),u);assert J=={u}
                                    filled=swap(s,(sigma,x),J);counts['outside_pair_singleton_collapses']+=1
                                else:
                                    J=comp(rot,s,pair,u);filled=swap(s,pair,J)
                                    counts['hole_in_component_collapses' if h in K else 'hole_outside_component_collapses']+=1
                                state_ok(rot,filled,h);assert target(rot,filled) and one
                            else:
                                first=swap(s,pair,K);state_ok(rot,first,h)
                                x=min(missing)
                                assert comp(rot,first,(sigma,x),u)=={u}
                                filled=swap(first,(sigma,x),{u});state_ok(rot,filled,h);assert target(rot,filled)
                                counts['commuting_SK_conversions']+=1
                                if not one:counts['exact_two_SK_conversions']+=1
    out={'scope':'old fixtures 12:0,14:0,17:0,17:1; no new census','counts':dict(counts),
         'conclusion':'All SK witnesses using the slide colour collapse to one original Kempe move; all remaining SK witnesses convert to two.'}
    Path(__file__).with_name('math-m3-review-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',dict(counts),flush=True)

if __name__=='__main__':main()
