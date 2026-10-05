"""Independent audit of ONLY two named counterexample graphs in saved WP19 output."""
import hashlib,json,time
from collections import Counter
from pathlib import Path
from wp18_independent import parse_graph,state_ok,fans,deletion_starts,successors,target,canon,replay
ROOT=Path(__file__).resolve().parent.parent

def shortest(rot,start,cap,kempe_only=False):
    start=canon(start);seen={start};frontier=[start];previous={start:None};layers=[]
    if target(rot,start):return {'distance':0,'path':[],'layers':[1]}
    for depth in range(1,cap+1):
        following=[]
        for s in frontier:
            for move,ns in successors(rot,s):
                if kempe_only and move[0]!='K':continue
                if ns in seen:continue
                seen.add(ns);previous[ns]=(s,move)
                if target(rot,ns):
                    path=[];at=ns
                    while previous[at] is not None:
                        old,m=previous[at];path.append(m);at=old
                    return {'distance':depth,'path':list(reversed(path)),'complete_non_target_layer_sizes':[1]+layers,'visited_until_first_target':len(seen)}
                following.append(ns)
        layers.append(len(following));frontier=following
        if not frontier:break
    return {'distance':None,'path':None,'complete_non_target_layer_sizes':[1]+layers,'visited':len(seen),'excluded_through':cap}

def main():
    t=time.monotonic();rawpath=ROOT/'wp19/wp19-P3.json'
    raw=json.loads(rawpath.read_text());graphs={g['graph_index']:g for g in raw['graphs'] if g['graph_index'] in (6406,7228)};del raw
    g=graphs[6406];rot=parse_graph(g['ascii']);expected=fans(rot)
    assert len(expected)==70 and Counter(map(len,rot))==Counter({5:14,6:8,7:2})
    rows={(r['v'],r['fan_index']):r for r in g['pairs']};assert set(rows)==set(expected)
    kills={k['stmt']:k for k in g['kills']};assert {'C1','C3'}<=set(kills)
    seen=set();memo={};lower=[]
    for w in kills['C1']['per_pair']:
        key=tuple(w['pair']);assert key in expected and key not in seen;seen.add(key)
        start=tuple(w['start']);state_ok(rot,start,key[0]);assert all(start[a]!=start[b] for a,b in expected[key])
        assert [list(x) for x in expected[key]]==rows[key]['chords']
        if start not in memo:memo[start]=shortest(rot,start,2)
        assert memo[start]['distance'] is None
        lower.append({'pair':key,'verified_lower':3,'non_target_layers':memo[start]['complete_non_target_layer_sizes']})
        witness=rows[key]['witness_L'];state_ok(rot,tuple(witness['start']),key[0]);replay(rot,tuple(witness['start']),witness['path'])
    assert seen==set(expected)
    # One fully independently re-enumerated pair suffices to prove m<=3.
    key=(0,0);upperhist=Counter();allstarts=deletion_starts(rot,0)
    admitted=[s for s in allstarts if all(s[a]!=s[b] for a,b in expected[key])]
    for s in admitted:
        result=shortest(rot,s,3);assert result['distance'] is not None;upperhist[result['distance']]+=1
    assert len(admitted)==rows[key]['starts']==134 and max(upperhist)==3
    assert {str(k):v for k,v in upperhist.items()}=={k:v for k,v in rows[key]['hist_l'].items() if v}
    c={'graph':'24:6406','ascii_sha256':hashlib.sha256(g['ascii'].encode()).hexdigest(),'degree_counts':dict(Counter(map(len,rot))),'legal_pairs':len(expected),'all_pair_lower_witnesses':lower,'distinct_lower_starts':len(memo),'exact_m':3,'upper_bound_pair':key,'upper_bound_pair_starts':len(admitted),'upper_bound_pair_histogram':dict(upperhist),'kill_implications':['C1','C3'],'U_exists_reported':g['U_exists']}
    print('6406 PASS',len(expected),'pairs',len(memo),'distinctlowerstarts',dict(upperhist),flush=True)
    g=graphs[7228];rot=parse_graph(g['ascii']);expected=fans(rot);w=next(k for k in g['kills'] if k['stmt']=='M2');key=tuple(w['pair']);start=tuple(w['start'])
    assert key==(17,0);state_ok(rot,start,17);assert all(start[a]!=start[b] for a,b in expected[key]);replay(rot,start,w['l_path'])
    l=shortest(rot,start,3);k=shortest(rot,start,5,True);assert l['distance']==3 and k['distance']==5
    replay(rot,start,k['path'])
    d={'graph':'24:7228','ascii_sha256':hashlib.sha256(g['ascii'].encode()).hexdigest(),'pair':key,'fan_chords':expected[key],'start':start,'producer_mixed_path':w['l_path'],'mixed':l,'kempe_only':k,'M2_false_inequality':'5 > 3+1','producer_kill_certificate_is_lower_bound_only':True,'U_exists_reported':g['U_exists']}
    print('7228 PASS','ell',l['distance'],'kappa',k['distance'],'Kpath',k['path'],flush=True)
    out={'scope':'Two named saved-output graphs only; independent move engine and graph/start checks, no new census','source_sha256':{str(rawpath.relative_to(ROOT)):hashlib.sha256(rawpath.read_bytes()).hexdigest()},'seconds':round(time.monotonic()-t,3),'counterexamples':[c,d]}
    Path(__file__).with_name('team-a-wp19-kills-check-results.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
