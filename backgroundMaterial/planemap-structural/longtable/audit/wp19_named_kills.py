"""Readable certificates extracted and independently replayed from completed P3."""
import json
from collections import Counter
from pathlib import Path
from wp18_independent import ROOT, parse_graph, replay, require, successors, target


def shortest(rot,start,cap,kempe=True):
    seen={start};front=[start];parents={start:None};layers=[]
    for depth in range(cap+1):
        fills=[s for s in front if target(rot,s)]
        layers.append({'depth':depth,'new_states':len(front),'filled_states':len(fills)})
        if fills:
            s=fills[0];path=[]
            while parents[s] is not None:
                prev,m=parents[s];path.append(list(m));s=prev
            return depth,list(reversed(path)),layers
        following=[]
        for s in front:
            for m,t in successors(rot,s):
                if (kempe and m[0]!='K') or t in seen:continue
                seen.add(t);parents[t]=(s,m);following.append(t)
        front=following
    raise ValueError('no fill within cap')


def main():
    data=json.loads((ROOT/'audit/wp19-counterexamples.json').read_text());gs={g['graph_index']:g for g in data['graphs']}
    g=gs[7228];rot=parse_graph(g['ascii']);kill=g['kills'][0];start=tuple(kill['start'])
    replay(rot,start,kill['l_path']);k,path,layers=shortest(rot,start,5);require(k==5,'exact kappa');replay(rot,start,path)
    pair=next(p for p in g['pairs'] if [p['v'],p['fan_index']]==kill['pair'])
    require(all(start[a]!=start[b] for a,b in pair['chords']),'fan admissibility')
    ell,mixed_path,mixed_layers=shortest(rot,start,3,kempe=False);require(ell==3,'exact mixed distance')
    a=gs[6406];rot_a=parse_graph(a['ascii']);best=next(p for p in a['pairs'] if p['L']==3)
    out={'scope':'two named completed P3 records only; no new census','phase_sha256':data['phase_sha256'],
         '24:6406':{'ascii':a['ascii'],'ascii_sha256':a['ascii_sha256'],'m':a['m'],
                      'degree_histogram':dict(Counter(map(len,rot_a))),
                      'degree_7_vertices':[v for v,ns in enumerate(rot_a) if len(ns)==7],
                      'pairs':len(a['pairs']),'pair_L_histogram':dict(Counter(p['L'] for p in a['pairs'])),
                      'best_pair':[best['v'],best['fan_index']],'best_pair_worst_witness':best['witness_L'],
                      'U_exists':a['U_exists']},
         '24:7228':{'ascii':g['ascii'],'ascii_sha256':g['ascii_sha256'],'pair':kill['pair'],
                     'chords':pair['chords'],'link':rot[17],'start':kill['start'],'ell':3,'kappa':k,
                     'mixed_path':kill['l_path'],'kempe_path':path,'kempe_BFS_layers':layers,'mixed_BFS_layers':mixed_layers,
                     'm':g['m'],'U_exists':g['U_exists']}}
    (ROOT/'audit/wp19-named-kills-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',json.dumps(out),flush=True)

if __name__=='__main__':main()
