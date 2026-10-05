"""Independently reconstruct every existing WP18 histogram; no new graphs.

Uses the independent audit's standard-library graph/colour/move implementation,
not producer code. Compares every legal fan's entire admitted start family.
"""
import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from wp18_independent import ROOT, deletion_starts, distance, fans, parse_graph, require

def graph_replay(g):
    rot=parse_graph(g['ascii'])
    require('interrupted' not in g,'interrupted graph needs a different contract')
    expected=fans(rot)
    reported={(r['v'],r['fan_index']):r for r in g['report']['rows']}
    require(set(expected)==set(reported),'pair coverage')
    starts_by_root={}; distances={}; rows=[]; pairs_hist=Counter(); starts_hist=Counter()
    for (v,i),chords in expected.items():
        if v not in starts_by_root: starts_by_root[v]=deletion_starts(rot,v)
        starts=[s for s in starts_by_root[v] if all(s[a]!=s[b] for a,b in chords)]
        require(starts,'empty fan family')
        histogram=Counter()
        for s in starts:
            if s not in distances:
                distances[s]=distance(rot,s,4)
                require(distances[s] is not None,'existing reported upper bound four fails')
            histogram[str(distances[s])]+=1
        L=max(map(int,histogram)); r=reported[v,i]
        require(len(starts)==r['starts'] and dict(histogram)==r['hist'],'start count/histogram mismatch')
        require(r['L']==L and r['L_at_least']==L,'row maximum mismatch')
        pairs_hist[str(L)]+=1; starts_hist.update(histogram)
        rows.append({'v':v,'fan':i,'starts':len(starts),'L':L})
    m=min(r['L'] for r in rows)
    require(g['report']['m']==m and g['report']['m_at_least']==m,'graph minimum mismatch')
    return {'order':g['order'],'graph_index':g['graph_index'],'m':m,
        'max_L':max(r['L'] for r in rows),'pairs':len(rows),'distinct_admitted_starts':len(distances),
        'pair_histogram':dict(pairs_hist),'start_histogram':dict(starts_hist),
        'ascii_sha256':hashlib.sha256(g['ascii'].encode()).hexdigest()}

def main():
    t=time.monotonic(); results={'scope':'complete independent replay of all starts on existing WP18 P1-P4 graphs',
        'implementation':'audit/wp18_independent.py; no producer imports','phases':[]}
    out=Path(__file__).parent/'wp18-full-replay-results.json'
    for phase in ('P1','P2','P3','P4'):
        p=ROOT/'wp18'/f'wp18-{phase}.json'; data=json.loads(p.read_text())
        graphs=[]; hist=Counter(); pairs=Counter(); starts=Counter()
        for i,g in enumerate(data['graphs']):
            r=graph_replay(g); graphs.append(r); hist[str(r['m'])]+=1
            pairs.update(r['pair_histogram']); starts.update(r['start_histogram'])
            if (i+1)%25==0: print(phase,i+1,'/',len(data['graphs']),'seconds',round(time.monotonic()-t,1),flush=True)
        require(dict(hist)==data['summary']['m_hist'],'phase minimum histogram mismatch')
        row={'phase':phase,'graphs_checked':len(graphs),'m_histogram':dict(hist),
            'pairs_checked':sum(r['pairs'] for r in graphs),
            'distinct_admitted_starts':sum(r['distinct_admitted_starts'] for r in graphs),
            'pair_histogram':dict(pairs),'start_histogram':dict(starts),
            'maximum_L':max(r['max_L'] for r in graphs),'graphs':graphs,
            'input_output_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        results['phases'].append(row); results['elapsed_seconds']=round(time.monotonic()-t,2)
        out.write_text(json.dumps(results,indent=2)+'\n')
        print('VERIFIED',phase,'m histogram',dict(hist),'seconds',round(time.monotonic()-t,1),flush=True)
    results['complete']=True
    results['source_hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [Path(__file__),Path(__file__).with_name('wp18_independent.py')]}
    out.write_text(json.dumps(results,indent=2)+'\n')
    print('PASS: every start, pair maximum and graph minimum reproduced',flush=True)

if __name__=='__main__':main()
