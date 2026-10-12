#!/usr/bin/env python3
"""Track U: collect law-respecting closed orbits and T1 violators from tu_eng anneal/rand logs, dedupe, re-evaluate
with `tu_eng eval`, verify with tu_verify (TrackT engine + independent networkx engine), add graph statistics.
usage: tu_collect.py OUTPREFIX LOG.jsonl ...   -> OUTPREFIX_graphs.txt, OUTPREFIX_eval.jsonl, OUTPREFIX_verify.jsonl,
                                                 OUTPREFIX_summary.json"""
import sys, os, json, subprocess, hashlib
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tu_verify import eng1, eng2


def main():
    pre = sys.argv[1]; seen = {}; src = {}
    for fn in sys.argv[2:]:
        for l in open(fn):
            try: d = json.loads(l)
            except Exception: continue
            if d.get('event') not in ('lawcycle', 'record') or 'edges' not in d: continue
            if d['event'] == 'record' and not d.get('nlaw'): continue
            key = hashlib.md5(json.dumps([d['edges'], d['fv']]).encode()).hexdigest()
            if key in seen: continue
            seen[key] = d; src[key] = os.path.basename(fn)
    keys = list(seen)
    with open(pre + '_graphs.txt', 'w') as f:
        for k in keys:
            d = seen[k]; E = d['edges']
            f.write(' '.join(map(str, [d['n'], len(E)] + [x for e in E for x in e] + d['fv'])) + '\n')
    ev = subprocess.run([os.path.join(HERE, 'tu_eng2'), 'eval', pre + '_graphs.txt'], capture_output=True, text=True).stdout
    open(pre + '_eval.jsonl', 'w').write(ev)
    out = open(pre + '_verify.jsonl', 'w'); graph = None
    stats = dict(graphs=len(keys), law_cycles=0, t1_cycles=0, t1_graphs=set(), verified_t1=0, verify_fail=0,
                 law_words={}, t1_by_n={}, law_by_n={}, planar_t1=0, minn_t1=None, L_t1={})
    for l in ev.splitlines():
        d = json.loads(l)
        if d['event'] == 'graph': graph = d; gi = d['gi']; continue
        if d['event'] != 'cycle' or d['viol'] != 0: continue
        n, E, fv, Ms = graph['n'], graph['edges'], graph['fv'], d['M']
        ok1, w1 = eng1(n, E, fv, Ms); ok2, w2, law, t1, msgs = eng2(n, E, fv, Ms)
        G = nx.Graph(); G.add_edges_from(E)
        r = dict(gi=gi, src=src[keys[gi]], n=n, L=len(Ms), word=''.join(map(str, w2)), eng1=ok1, eng2=ok2,
                 agree=(w1 == w2 == list(map(int, d['word'].split()))), law=law, T1=t1,
                 simple=G.number_of_edges() == len(E), planar=nx.check_planarity(G)[0])
        out.write(json.dumps(r) + '\n')
        good = ok1 and ok2 and r['agree'] and law
        if not good: stats['verify_fail'] += 1; continue
        stats['law_cycles'] += 1
        kset = ''.join(sorted(set(r['word'])))
        stats['law_words'][kset] = stats['law_words'].get(kset, 0) + 1
        stats['law_by_n'][n] = stats['law_by_n'].get(n, 0) + 1
        if t1:
            stats['t1_cycles'] += 1; stats['t1_graphs'].add(gi); stats['t1_by_n'][n] = stats['t1_by_n'].get(n, 0) + 1
            stats['L_t1'][len(Ms)] = stats['L_t1'].get(len(Ms), 0) + 1
            if r['planar']: stats['planar_t1'] += 1
            if stats['minn_t1'] is None or n < stats['minn_t1']: stats['minn_t1'] = n
    stats['t1_graphs'] = len(stats['t1_graphs'])
    json.dump(stats, open(pre + '_summary.json', 'w'), indent=1)
    print(json.dumps(stats))


if __name__ == '__main__':
    main()
