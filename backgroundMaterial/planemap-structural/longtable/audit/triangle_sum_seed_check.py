"""Check only the existing 17:1 seed for a hand clique-sum construction."""
import hashlib,json
from collections import Counter
from wp18_independent import ROOT,parse_graph,deletion_starts,fans,replay,successors,target,require,state_ok
from wp19_named_kills import shortest


def no_short(rot,start):
    seen={start};front={start};counts=[]
    for depth in range(3):
        require(not any(target(rot,s) for s in front),'seed lower witness has short fill');counts.append(len(front))
        if depth==2:break
        nxt={t for s in front for _,t in successors(rot,s)}-seen;seen.update(nxt);front=nxt
    return counts


def main():
    p=ROOT/'wp18/wp18-P1.json';d=json.loads(p.read_text());g=next(g for g in d['graphs'] if (g['order'],g['graph_index'])==(17,1));rot=parse_graph(g['ascii']);legal=fans(rot)
    rows={(r['v'],r['fan_index']):r for r in g['report']['rows']};require(set(rows)==set(legal) and len(rows)==60,'seed complete legal-pair set')
    lower=[];cache={}
    for pair,chords in legal.items():
        w=rows[pair]['witness'];start=tuple(w['start']);state_ok(rot,start,pair[0]);require(all(start[a]!=start[b] for a,b in chords),'seed fan admissibility')
        if start not in cache:cache[start]=no_short(rot,start)
        lower.append({'pair':list(pair),'chords':[list(c) for c in chords],'start':list(start),'non_target_layer_sizes':cache[start]})
    S=[s for s in deletion_starts(rot,0) if all(s[a]!=s[b] for a,b in legal[0,1])];upper=[];hist=Counter()
    for start in S:
        k,path,layers=shortest(rot,start,3);replay(rot,start,path);hist[k]+=1
        upper.append({'start':list(start),'kempe_distance':k,'kempe_path':path})
    require(len(S)==34 and max(hist)==3,'seed pure-three complete upper family')
    filled=next(s for s in deletion_starts(rot,0) if target(rot,s));missing=next(c for c in range(4) if c not in {filled[v] for v in rot[0]});full=list(filled);full[0]=missing
    require(all(full[v]!=full[w] for v,ns in enumerate(rot) for w in ns),'explicit full seed colouring')
    faces=set()
    for a,ns in enumerate(rot):
        for b in ns:
            c=rot[b][(rot[b].index(a)+1)%len(rot[b])];faces.add(tuple(sorted((a,b,c))))
    left=(1,2,7);right=(3,4,11)
    require(left in faces and right in faces and not set(left)&set(right) and 0 not in left+right,'two actual disjoint faces avoid designated root')
    out={'scope':'existing17:1 only; no constructed new-order graph was generated or coloured',
         'input_file':'wp18/wp18-P1.json','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
         'ascii':g['ascii'],'ascii_sha256':hashlib.sha256(g['ascii'].encode()).hexdigest(),
         'lower_bound':{'pairs':60,'distinct_witnesses':len(cache),'certificates':lower},
         'upper_bound':{'pair':[0,1],'chords':[list(c) for c in legal[0,1]],'starts':34,'kappa_histogram':dict(hist),'certificates':upper},
         'full_colouring':full,'left_face':list(left),'right_face':list(right),'designated_root':0}
    (ROOT/'audit/triangle-sum-seed-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS existing seed: all60 lowerpairs, complete34-start upper',dict(hist),'fullcolouring',full,flush=True)

if __name__=='__main__':main()
