"""Complete independent WP19 replay, importing only the audit's own move code.

Rebuilds every deletion family, both distances, and every fan Kempe class.
Unlike the package certificate checker, also verifies positive U verdicts and
all start/distance/class histograms. Uses existing phase inputs only.
"""
import argparse
import hashlib
import json
import time
from collections import Counter, deque
from multiprocessing import Pool
from pathlib import Path
from wp18_independent import ROOT, deletion_starts, fans, parse_graph, require, successors, target


def flood(rot,seeds,cap=None,kempe=False,universe=None):
    dist=dict.fromkeys(seeds,0)
    todo=deque(seeds)
    while todo:
        s=todo.popleft(); depth=dist[s]
        if cap is not None and depth==cap: continue
        for move,t in successors(rot,s):
            if kempe and move[0]!='K': continue
            if universe is not None: require(t in universe,'move left independently enumerated family')
            if t not in dist:
                dist[t]=depth+1;todo.append(t)
    return dist


def classes(rot,chords,starts,kdist):
    augmented=[list(row) for row in rot]
    for a,b in chords:
        augmented[a].append(b);augmented[b].append(a)
    unseen=set(starts); universe=set(starts); number=bad=0
    while unseen:
        number+=1; seed=unseen.pop(); todo=[seed]
        unlocked=kdist.get(seed) in (0,1)
        while todo:
            s=todo.pop()
            for move,t in successors(augmented,s):
                if move[0]!='K': continue
                require(t in universe,'T-star move left independent fan family')
                if t in unseen:
                    unseen.remove(t);todo.append(t)
                    unlocked |= kdist.get(t) in (0,1)
        bad+=not unlocked
    return number,bad


def replay_graph(g):
    require(not g['interrupted'],'interrupted producer graph needs separate partial review')
    rot=parse_graph(g['ascii']); n=len(rot)
    require(n==g['order'],'order mismatch')
    require(sorted(map(len,rot))==g['degrees'],'degree sequence mismatch')
    require(hashlib.sha256(g['ascii'].encode()).hexdigest()==g['ascii_sha256'],'graph hash mismatch')
    allstarts={h:deletion_starts(rot,h) for h in range(n)}
    universe=set().union(*allstarts.values())
    seeds=[s for s in universe if target(rot,s)]
    ld=flood(rot,seeds,6,universe=universe)
    legal=fans(rot)
    reported={(p['v'],p['fan_index']):p for p in g['pairs']}
    require(len(reported)==len(g['pairs']) and set(reported)==set(legal),'complete unique pair coverage')
    roots=sorted({v for v,i in legal})
    kd={v:flood(rot,[s for s in allstarts[v] if target(rot,s)],kempe=True,
                universe=set(allstarts[v])) for v in roots}
    total_l=Counter();total_k=Counter();lengths=[];us=[];kill=set()
    pair_counts=Counter();unique=set(); examples={}
    for (v,i),chords in legal.items():
        p=reported[v,i]
        require(p['chords']==[list(c) for c in chords],'chords mismatch')
        S=[s for s in allstarts[v] if all(s[a]!=s[b] for a,b in chords)]
        require(p['starts']==len(S) and p['empty']==(not S),'independent fan family count')
        hl=Counter({str(j):0 for j in range(7)});hl['capped']=0
        hk=Counter({str(j):0 for j in range(8)});hk.update({'capped':0,'nofill':0})
        for s in S:
            unique.add(s);ell=ld.get(s); kap=kd[v].get(s)
            hl['capped' if ell is None else str(ell)]+=1
            hk['nofill' if kap is None else 'capped' if kap>7 else str(kap)]+=1
            if ell is None or ell>4: kill.add('M1');examples.setdefault('M1',{'pair':[v,i],'start':list(s)})
            if kap is None or (ell is not None and kap>ell+1):
                kill.add('M2');examples.setdefault('M2',{'pair':[v,i],'start':list(s),'ell':ell,'kappa':kap})
            if ell==2 and (kap is None or kap>2):
                kill.add('M3');examples.setdefault('M3',{'pair':[v,i],'start':list(s),'ell':ell,'kappa':kap})
            require((kap is None or kap>1)==(ell is None or ell>1),'one-move/locking consistency')
        require(dict(hl)==p['hist_l'] and dict(hk)==p['hist_k'],'complete distance histograms')
        nc,bc=classes(rot,chords,S,kd[v]);u=(bc==0) if S else None
        require(nc==p['tstar_classes'] and bc==p['locked_classes'] and u==p['U'],'complete class/U verdict')
        L=max((ld.get(s,7) for s in S),default=0)
        exact=None if not S or hl['capped'] else L
        require(exact==p['L'] and L==p['L_at_least'],'pair maximum')
        if S:lengths.append(L)
        us.append(u);pair_counts[str(L)]+=1;total_l.update(hl);total_k.update(hk)
    require(lengths,'no nonempty pair')
    m=min(lengths);ue=any(u is True for u in us)
    exact_m=None if g['unresolved_pairs'] else m
    require(exact_m==g['m'] and m==g['m_at_least'],'graph minimum')
    require(ue==g['U_exists'],'graph U-exists')
    if m>2 and n>=18:kill.add('C1')
    if m>3:kill.add('C2')
    if m>2 and max(map(len,rot))>=7:kill.add('C3')
    if not ue:kill.add('U_exists')
    require(kill=={x['stmt'] for x in g['kills']},'complete kill predicates')
    return {'order':n,'graph_index':g['graph_index'],'pairs':len(legal),
            'all_hole_states':len(universe),'distinct_admitted_starts':len(unique),
            'm':exact_m,'m_at_least':m,'U_exists':ue,'hist_l':dict(total_l),'hist_k':dict(total_k),
            'pair_L_histogram':dict(pair_counts),'kills':sorted(kill),'examples':examples}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['P1','P2','P3'])
    ap.add_argument('--procs',type=int,default=10);a=ap.parse_args()
    path=ROOT/'wp19'/f'wp19-{a.phase}.json';data=json.loads(path.read_text())
    require(data['phase']==a.phase and data['caps']=={'mixed':6,'kempe':7},'phase/caps')
    require(hashlib.sha256((ROOT/data['declaration']).read_bytes()).hexdigest()==data['declaration_sha256'],'declaration binding')
    for f,h in data['source_sha256'].items():require(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,'producer source binding')
    rows=[];hist_l=Counter();hist_k=Counter();mh=Counter();uh=Counter();kills=Counter()
    t0=time.monotonic()
    with Pool(a.procs,maxtasksperchild=1) as pool:
        for r in pool.imap(replay_graph,data['graphs']):
            rows.append(r)
            mh[str(r['m']) if r['m'] is not None else '>='+str(r['m_at_least'])]+=1
            uh[str(r['U_exists']).lower()]+=1
            hist_l.update(r['hist_l']);hist_k.update(r['hist_k']);kills.update(r['kills'])
            if len(rows)%100==0:print(a.phase,'verified',len(rows),'/',len(data['graphs']),round(time.monotonic()-t0,1),'seconds',flush=True)
    summary=data['summary']
    require(dict(mh)==summary['m_hist'],'phase m histogram')
    require(dict(hist_l)==summary['hist_l'] and dict(hist_k)==summary['hist_k'],'phase distance histograms')
    require(summary['graphs']==len(rows),'summary count')
    require(all(uh.get(k,0)==v for k,v in summary['U_exists'].items()),'phase U histogram')
    for stmt,s in summary['statements'].items():
        require(kills.get(stmt,0)==s['killed_count'],'statement kill count')
    # Bind exact graph coverage to raw phase inputs independently of producer.
    if a.phase=='P2':
        files=[ROOT/'wp17-last-roots'/f'triangulations-min5-{n}.txt' for n in (21,22)]
        require({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}==data['input_sha256'],'P2 inputs')
        expected=[(n,i,line) for n,f in zip((21,22),files) for i,line in enumerate(f.read_text().splitlines()) if line.strip()]
        require(expected==[(g['order'],g['graph_index'],g['ascii']) for g in data['graphs']],'P2 graph identity')
    else:
        raw=''.join(g['ascii']+'\n' for g in data['graphs']).encode()
        require(hashlib.sha256(raw).hexdigest()==data['input_sha256'],'raw input graph coverage hash')
        require(all(g['graph_index']==i and g['order']==(23 if a.phase=='P1' else 24)
                    for i,g in enumerate(data['graphs'])),'phase indices/orders')
    out={'scope':'complete independent WP19 replay','phase':a.phase,'complete':True,
         'phase_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (Path(__file__),Path(__file__).with_name('wp18_independent.py'))},
         'seconds':round(time.monotonic()-t0,2),'graphs':rows,'summary':{'graphs':len(rows),
         'm_hist':dict(mh),'U_exists':dict(uh),'kills':dict(kills),'hist_l':dict(hist_l),'hist_k':dict(hist_k)}}
    Path(__file__).with_name(f'wp19-{a.phase}-math-replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',a.phase,json.dumps(out['summary']),flush=True)


if __name__=='__main__':main()
