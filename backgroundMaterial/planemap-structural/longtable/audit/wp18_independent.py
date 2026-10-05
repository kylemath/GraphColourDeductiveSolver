"""Independent review of existing WP18 certificates, not a census producer.

No imports from mass_core, WP18, or the team's checker. Validates graph rotations,
all pair metadata, histogram arithmetic, witnesses, and their exact distances.
Re-enumerates all starts only on the named order-17 graph-1 regression, to certify
the full min/max claim there. Writes its own JSON next to this file.
"""
import hashlib
import itertools
import json
import time
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOLE = 4

def require(condition, message):
    if not condition: raise ValueError(message)

def parse_graph(line):
    n, code = line.split(' ', 1)
    rot = [[ord(x)-97 for x in row] for row in code.split(',')]
    n=int(n)
    require(n==len(rot) and n>=12, 'graph order')
    for v,ns in enumerate(rot):
        require(len(ns)>=5 and len(ns)==len(set(ns)) and v not in ns, 'simple/min-degree')
        require(all(0<=w<n and v in rot[w] for w in ns), 'symmetric edges')
    e=sum(map(len,rot))//2
    require(e==3*n-6,'edge count')
    reached={0}; stack=[0]
    while stack:
        for w in rot[stack.pop()]:
            if w not in reached: reached.add(w); stack.append(w)
    require(len(reached)==n,'connectivity')
    seen=set(); f=0
    for v,ns in enumerate(rot):
        for w in ns:
            if (v,w) in seen: continue
            start=dart=(v,w); length=0
            while dart not in seen:
                seen.add(dart); length+=1
                a,b=dart; dart=(b,rot[b][(rot[b].index(a)+1)%len(rot[b])])
            require(dart==start and length==3,'triangular faces')
            f+=1
    require(n-e+f==2,'sphere')
    return rot

def state_ok(rot,s,h=None):
    require(len(s)==len(rot) and all(type(x) is int and 0<=x<=4 for x in s),'state alphabet/length')
    require(s.count(HOLE)==1,'exactly one hole')
    if h is not None: require(s[h]==HOLE,'root/hole mismatch')
    require(all(s[v]==HOLE or s[w]==HOLE or s[v]!=s[w]
                for v,ns in enumerate(rot) for w in ns),'proper colouring')

def canon(s):
    names={}; out=[]
    for x in s:
        if x==HOLE: out.append(HOLE)
        else:
            if x not in names: names[x]=len(names)
            out.append(names[x])
    return tuple(out)

def target(rot,s): return len({s[w] for w in rot[s.index(HOLE)]})<=3

def successors(rot,s):
    h=s.index(HOLE)
    for a,b in itertools.combinations(range(4),2):
        remaining={v for v,x in enumerate(s) if x in (a,b)}
        while remaining:
            seed=min(remaining); remaining.remove(seed); comp={seed}; todo=[seed]
            while todo:
                for w in rot[todo.pop()]:
                    if w in remaining: remaining.remove(w); comp.add(w); todo.append(w)
            nxt=list(s)
            for v in comp: nxt[v]=b if s[v]==a else a
            yield ('K',a,b,seed),canon(nxt)
    counts=Counter(s[w] for w in rot[h])
    for w in rot[h]:
        if counts[s[w]]==1:
            nxt=list(s); nxt[h],nxt[w]=nxt[w],HOLE
            yield ('S',w),canon(nxt)

def replay(rot,start,path):
    s=start
    for move in path:
        mv=tuple(move)
        require(all(type(x) is int for x in mv[1:]),'move labels')
        candidates={m:ns for m,ns in successors(rot,s)}
        require(mv in candidates,'illegal component swap or slide')
        s=candidates[mv]; state_ok(rot,s)
    require(target(rot,s),'path does not fill')

def distance(rot,start,cap):
    if target(rot,start): return 0
    seen={start}; frontier=[start]
    for depth in range(1,cap+1):
        following=[]
        for s in frontier:
            for _,ns in successors(rot,s):
                if ns in seen: continue
                seen.add(ns)
                if target(rot,ns): return depth
                following.append(ns)
        frontier=following
        if not frontier: break
    return None

def fans(rot):
    out={}
    for v,ns in enumerate(rot):
        if len(ns)!=5: continue
        for i,a in enumerate(ns):
            b,c=ns[(i+2)%5],ns[(i+3)%5]
            if b not in rot[a] and c not in rot[a]:
                out[v,i]=[(a,b),(a,c)]
    return out

def deletion_starts(rot,h):
    order=[v for v in range(len(rot)) if v!=h]
    state=[HOLE]*len(rot); out=[]
    def walk(i,top):
        if i==len(order): out.append(tuple(state)); return
        v=order[i]; banned={state[w] for w in rot[v] if state[w]!=HOLE}
        for x in range(min(3,top+1)+1):
            if x not in banned:
                state[v]=x; walk(i+1,max(top,x)); state[v]=HOLE
    walk(0,-1)
    return out

def verify_report(g,cap):
    rot=parse_graph(g['ascii']); require(len(rot)==g['order'],'metadata order')
    require(hashlib.sha256(g['ascii'].encode()).hexdigest()==g['ascii_sha256'],'ASCII digest')
    if 'interrupted' in g: return {'interrupted':True},rot
    report=g['report']; expected=fans(rot); rows=report['rows']; have=set()
    memo={}; checked=0; capped=0; certified_lower=[]
    for row in rows:
        key=row['v'],row['fan_index']
        require(key in expected and key not in have,'missing/duplicate/invalid pair'); have.add(key)
        require([tuple(p) for p in row['chords']]==expected[key],'chords do not match fan')
        require(type(row['starts']) is int and row['starts']>0,'empty or invalid starts')
        hist=row['hist']; require(sum(hist.values())==row['starts'],'histogram total')
        require(all(type(n) is int and n>0 for n in hist.values()),'histogram counts')
        require(all(k=='capped' or k in {str(i) for i in range(cap+1)} for k in hist),'histogram depth')
        expected_lower=max(cap+1 if k=='capped' else int(k) for k in hist)
        require(row['L_at_least']==expected_lower,'row lower arithmetic')
        require(row['L']==(None if 'capped' in hist else expected_lower),'row maximum arithmetic')
        if expected_lower>=2:
            require('witness' in row,'missing lower witness')
            w=row['witness']; start=tuple(w['start']); state_ok(rot,start,row['v'])
            require(all(start[a]!=start[b] for a,b in expected[key]),'start improper on fan')
            path=w['moves']
            if expected_lower<=cap:
                require(path is not None and len(path)==expected_lower,'path length')
                replay(rot,start,path)
                depth_key=(start,expected_lower-1)
                if depth_key not in memo: memo[depth_key]=distance(rot,start,expected_lower-1)
                require(memo[depth_key] is None,'witness has a shorter fill')
                checked+=1; certified_lower.append(expected_lower)
            else:
                require(path is None,'capped path')
                # Complete exclusion through depth six; do not accept a mere null path.
                require(distance(rot,start,cap) is None,'false cap lower bound')
                capped+=1; certified_lower.append(cap+1)
        else:
            # No witness supplied; this row's claimed upper bound remains producer-only.
            certified_lower.append(0)
    require(have==set(expected) and report['pairs']==len(expected),'incomplete pair coverage')
    lower=min(row['L_at_least'] for row in rows)
    exact=[row['L'] for row in rows if row['L'] is not None]
    best=min(exact) if exact else None
    m=best if best is not None and best<=lower else None
    require(report['m']==m and report['m_at_least']==lower,'min/max arithmetic')
    require(report['max_L_at_least']==max(row['L_at_least'] for row in rows),'maximum arithmetic')
    return {'pairs':len(rows),'witnesses':checked,'capped':capped,
            'certified_m_lower':min(certified_lower),'distinct_witnesses':len({s for s,_ in memo})},rot

def exact_named_graph(g):
    rot=parse_graph(g['ascii']); reported={(r['v'],r['fan_index']):r for r in g['report']['rows']}
    memo={}; rows=[]; states_by_root={}
    for key,chords in fans(rot).items():
        h,i=key
        if h not in states_by_root: states_by_root[h]=deletion_starts(rot,h)
        starts=[s for s in states_by_root[h] if all(s[a]!=s[b] for a,b in chords)]
        hist=Counter()
        for s in starts:
            if s not in memo: memo[s]=distance(rot,s,4)
            require(memo[s] is not None,'named graph distance exceeds four')
            hist[str(memo[s])]+=1
        saved=reported[key]
        require(saved['starts']==len(starts) and saved['hist']==dict(hist),'named graph starts/hist disagreement')
        L=max(map(int,hist)); require(saved['L']==L,'named graph max disagreement')
        rows.append({'v':h,'fan_index':i,'starts':len(starts),'L':L,'hist':dict(hist)})
    require(len(rows)==60 and min(r['L'] for r in rows)==3,'named graph min/max')
    return {'pairs':60,'m':3,'max_L':4,'distinct_starts_checked':len(memo),
            'rows':rows,'scope':'all legal pairs and all admitted starts independently enumerated'}

def negative_regressions(g):
    import copy
    source=next(r for r in g['report']['rows'] if r['L']>=2)
    coloured_index=next(i for i,c in enumerate(source['witness']['start']) if c!=HOLE)
    tests=[]
    def reject(label,change):
        changed=copy.deepcopy(g); change(changed)
        try: verify_report(changed,6)
        except (ValueError,IndexError,KeyError,TypeError): tests.append(label); return
        raise ValueError('accepted malformed fixture: '+label)
    idx=g['report']['rows'].index(source)
    reject('missing legal pair',lambda x:x['report']['rows'].pop())
    reject('wrong fan chords',lambda x:x['report']['rows'][idx]['chords'].__setitem__(0,[0,0]))
    reject('invalid colour alphabet',lambda x:x['report']['rows'][idx]['witness']['start'].__setitem__(coloured_index,9))
    reject('duplicate hole',lambda x:x['report']['rows'][idx]['witness']['start'].__setitem__(coloured_index,4))
    reject('illegal slide',lambda x:x['report']['rows'][idx]['witness']['moves'].__setitem__(0,['S',999]))
    reject('wrong graph hash',lambda x:x.__setitem__('ascii_sha256','0'*64))
    # A valid but padded path must not be mistaken for a shortest path.
    rot=parse_graph(g['ascii']); final=tuple(source['witness']['start'])
    for mv in source['witness']['moves']:
        final=dict(successors(rot,final))[tuple(mv)]
    first,intermediate=next(iter(successors(rot,final)))
    second=next(mv for mv,ns in successors(rot,intermediate) if ns==final)
    padded=copy.deepcopy(source); padded['witness']['moves'] += [list(first),list(second)]
    length=len(padded['witness']['moves']); start=tuple(padded['witness']['start'])
    replay(rot,start,padded['witness']['moves'])
    require(distance(rot,start,length-1) is not None,'padded shortestness regression')
    tests.append('valid but non-shortest padded path detected')
    return tests

def main():
    t=time.monotonic(); out={'scope':'existing WP18 outputs; independent witness distances, pair metadata, arithmetic; all starts replayed only for 17:1'}
    manifest=[]
    for name in ('SHA256SUMS-source','SHA256SUMS-output'):
        p=ROOT/'wp18'/name
        for line in p.read_text().splitlines():
            if not line.strip(): continue
            digest,rel=line.split(None,1); file=p.parent/rel.strip()
            require(hashlib.sha256(file.read_bytes()).hexdigest()==digest,'manifest mismatch '+str(file))
            manifest.append(str(file.relative_to(ROOT)))
    out['manifest_files_checked']=len(manifest); out['phases']=[]; named=None
    for phase in ('P1','P2','P3','P4'):
        path=ROOT/'wp18'/('wp18-'+phase+'.json'); data=json.loads(path.read_text())
        if phase in ('P1','P2'):
            input_path=ROOT/'wp11-run-manifest.json'
            source=json.loads(input_path.read_text())
            key='discovery_graphs' if phase=='P1' else 'validation_graphs'
            expected={(g['order'],g['graph_index']):g['ascii'] for g in source[key]}
        else:
            order=21 if phase=='P3' else 22
            input_path=ROOT/'wp17-last-roots'/f'triangulations-min5-{order}.txt'
            expected={(order,i):line for i,line in enumerate(input_path.read_text().splitlines()) if line.strip()}
        require({(g['order'],g['graph_index']):g['ascii'] for g in data['graphs']}==expected,'phase input coverage')
        require(data['phase']==phase and data['cap']==6,'phase metadata')
        counts=Counter(); seen=set(); m_hist=Counter(); m_lower_ge3=[]
        for g in data['graphs']:
            key=g['order'],g['graph_index']; require(key not in seen,'duplicate graph'); seen.add(key)
            row,_=verify_report(g,data['cap'])
            if row.get('interrupted'): counts['interrupted']+=1; continue
            counts['pairs']+=row['pairs']; counts['witnesses']+=row['witnesses']; counts['distinct_witnesses']+=row['distinct_witnesses']
            counts['capped']+=row['capped']; m_hist[str(g['report']['m'])]+=1
            if row['certified_m_lower']>=3: m_lower_ge3.append(list(key))
            if key==(17,1): named=g
        require(dict(m_hist)==data['summary']['m_hist'],'phase histogram arithmetic')
        out['phases'].append({'phase':phase,'graphs':len(seen),**counts,
            'reported_m_hist':dict(m_hist),'independently_certified_m_at_least_3':m_lower_ge3,
            'input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),
            'output_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        print(phase,dict(counts),'seconds',round(time.monotonic()-t,1),flush=True)
    require(named is not None,'missing named counterexample')
    out['order17_graph1']=exact_named_graph(named)
    out['negative_regressions_rejected']=negative_regressions(named)
    out['seconds']=round(time.monotonic()-t,2)
    (Path(__file__).parent/'wp18-independent-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: independently verified m(17:1)=3; all supplied witness distances verified',flush=True)

if __name__=='__main__': main()
