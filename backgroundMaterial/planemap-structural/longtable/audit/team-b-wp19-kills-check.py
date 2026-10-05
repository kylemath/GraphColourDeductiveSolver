"""Targeted independent certificate check: two saved WP19 graphs, no census."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import hashlib,json
from wp18_independent import parse_graph,deletion_starts
BASE=Path(__file__).resolve().parent.parent

def canon(s):
    labels={};out=[]
    for c in s:
        if c==4:out.append(4)
        else:
            if c not in labels:labels[c]=len(labels)
            out.append(labels[c])
    return tuple(out)

def valid(adj,s,h=None):
    assert len(s)==len(adj) and s.count(4)==1 and all(type(c) is int and 0<=c<=4 for c in s)
    if h is not None:assert s[h]==4
    assert all(s[v]==4 or s[w]==4 or s[v]!=s[w] for v in range(len(s)) for w in adj[v])

def target(adj,s):return len({s[w] for w in adj[s.index(4)]})<=3

def component(adj,s,a,b,seed):
    assert s[seed] in (a,b)
    seen={seed};stack=[seed]
    while stack:
        for w in adj[stack.pop()]:
            if s[w] in (a,b) and w not in seen:seen.add(w);stack.append(w)
    return seen

def move(adj,s,m):
    t=list(s);h=s.index(4)
    if m[0]=='S':
        w=m[1];assert w in adj[h] and sum(s[j]==s[w] for j in adj[h])==1
        t[h],t[w]=t[w],4
    else:
        _,a,b,seed=m
        for w in component(adj,s,a,b,seed):t[w]=b if s[w]==a else a
    t=canon(t);valid(adj,t);return t

def successors(adj,s,mixed):
    for a,b in combinations(range(4),2):
        covered=set()
        for seed,c in enumerate(s):
            if c not in (a,b) or seed in covered:continue
            covered.update(component(adj,s,a,b,seed));m=('K',a,b,seed)
            yield m,move(adj,s,m)
    if mixed:
        h=s.index(4);counts=Counter(s[w] for w in adj[h])
        for w in adj[h]:
            if counts[s[w]]==1:
                m=('S',w);yield m,move(adj,s,m)

def bfs(adj,start,cap,mixed):
    start=canon(start);front={start:[]};seen={start};layers=[]
    for depth in range(cap+1):
        targets=[(s,path) for s,path in front.items() if target(adj,s)]
        layers.append({'depth':depth,'new_states':len(front),'targets':len(targets)})
        if targets:
            state,path=targets[0]
            return {'distance':depth,'path':path,'layers':layers,'terminal_state':list(state)}
        nxt={}
        if depth<cap:
            for s,path in front.items():
                for m,t in successors(adj,s,mixed):
                    if t not in seen:seen.add(t);nxt[t]=path+[list(m)]
        front=nxt
    return {'distance':None,'layers':layers,'searched_through':cap}

def legalpairs(adj):
    out={}
    for v,ns in enumerate(adj):
        if len(ns)!=5:continue
        for i,a in enumerate(ns):
            chords=[(a,ns[(i+2)%5]),(a,ns[(i+3)%5])]
            if all(b not in adj[a] for a,b in chords):out[v,i]=chords
    return out

def check_U(adj,h,chords):
    starts={canon(s) for s in deletion_starts(adj,h) if all(s[a]!=s[b] for a,b in chords)}
    aug=[list(ns) for ns in adj]
    for a,b in chords:aug[a].append(b);aug[b].append(a)
    remaining=set(starts);classes=[]
    while remaining:
        seed=min(remaining);seen={seed};stack=[seed]
        while stack:
            for _,t in successors(aug,stack.pop(),False):
                assert t in starts
                if t not in seen:seen.add(t);stack.append(t)
        remaining-=seen
        unlocked=[s for s in seen if target(adj,s) or any(target(adj,t) for _,t in successors(adj,s,False))]
        assert unlocked
        classes.append({'size':len(seen),'unlocked_members':len(unlocked),'unlocked_witness':list(min(unlocked))})
    return {'starts':len(starts),'class_count':len(classes),'locked_classes':0,'classes':classes,'U':True}

def main():
    raw=BASE/'wp19/wp19-P3.json'; data=json.loads(raw.read_text())
    gs={g['graph_index']:g for g in data['graphs'] if g['graph_index'] in (6406,7228)}
    result={'scope':'two existing named counterexamples only','input_sha256':hashlib.sha256(raw.read_bytes()).hexdigest()}
    g=gs[6406];adj=parse_graph(g['ascii']);pairs=legalpairs(adj)
    assert len(pairs)==70 and len([ns for ns in adj if len(ns)==5])==14
    assert Counter(map(len,adj))=={5:14,6:8,7:2}
    assert len(g['pairs'])==70 and {(p['v'],p['fan_index']) for p in g['pairs']}==set(pairs)
    kill=next(k for k in g['kills'] if k['stmt']=='C1');rows=[];cache={}
    assert len(kill['per_pair'])==70 and {tuple(p['pair']) for p in kill['per_pair']}==set(pairs)
    for p in kill['per_pair']:
        key=tuple(p['pair']);s=tuple(p['start']);valid(adj,s,key[0])
        assert all(s[a]!=s[b] for a,b in pairs[key])
        if s not in cache:cache[s]=bfs(adj,s,2,True)
        assert cache[s]['distance'] is None
        rows.append({'pair':list(key),'no_fill_layers_0_2':cache[s]['layers']})
    chosen=next(p for p in g['pairs'] if p['v']==0 and p['fan_index']==0)
    starts=[s for s in deletion_starts(adj,0) if all(s[a]!=s[b] for a,b in pairs[0,0])]
    hist=Counter()
    for s in starts:
        d=bfs(adj,s,3,True)['distance'];assert d is not None;hist[d]+=1
    assert len(starts)==134 and hist=={0:22,1:81,2:28,3:3}
    result['24:6406']={'degrees':dict(Counter(map(len,adj))),'legal_pairs':70,'C1_lower_certificates':rows,'unique_lower_starts':len(cache),'upper_pair':[0,0],'upper_pair_starts':len(starts),'upper_pair_mixed_histogram':dict(hist),'m_exact':3,'U_exists_reported':g['U_exists'],'reported_U_true_pairs':sum(p['U'] is True for p in g['pairs']),'independent_U_pair_0_0':check_U(adj,0,pairs[0,0])}
    print('PASS 24:6406 all70 lower certificates and134 upper starts: m=3',flush=True)
    g=gs[7228];adj=parse_graph(g['ascii']);pairs=legalpairs(adj)
    k=next(k for k in g['kills'] if k['stmt']=='M2');s=tuple(k['start']);pair=tuple(k['pair']);valid(adj,s,17)
    assert pair==(17,0) and all(s[a]!=s[b] for a,b in pairs[pair])
    states=[];t=s
    for m in k['l_path']:
        t=move(adj,t,m);h=t.index(4);states.append({'move':m,'hole':h,'hole_degree':len(adj[h]),'link':list(adj[h]),'link_colours':[t[w] for w in adj[h]],'state':list(t)})
    assert target(adj,t)
    lm=bfs(adj,s,3,True);kp=bfs(adj,s,5,False)
    assert lm['distance']==3 and kp['distance']==5
    kt=s
    for m in kp['path']:kt=move(adj,kt,m)
    assert target(adj,kt) and kt[17]==4
    result['24:7228']={'pair':list(pair),'chords':[list(e) for e in pairs[pair]],'start':list(s),'start_link':list(adj[17]),'start_link_colours':[s[w] for w in adj[17]],'mixed_supplied_path':k['l_path'],'mixed_supplied_trace':states,'mixed_bfs':lm,'pure_bfs':kp,'ell_exact':3,'kappa_exact':5,'raw_kill_kappa_field':k['kappa'],'raw_kill_kappa_lower':k['kappa_lower'],'reported_m':g['m'],'U_exists_reported':g['U_exists'],'independent_U_pair_17_0':check_U(adj,17,pairs[pair])}
    print('PASS 24:7228 fan admitted, ell=3,kappa=5',flush=True)
    result['complete']=True
    (BASE/'audit/team-b-wp19-kills-results.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
