#!/usr/bin/env python3
"""Track G [exploratory]: collect DL->DL pi-step feature data and cycle-class certificates.

usage: tg_collect.py GRAPHFILE OUTPREFIX [--names a,b,...] [--holes-from KCLASS3.jsonl] [--homology] [--stride K --offset R]
Writes OUTPREFIX.steps.jsonl (one line per hole: steps with feature vectors of s and pi s)
       OUTPREFIX.cert.jsonl  (one line per Kempe class containing an all-DL pi-cycle)
       OUTPREFIX.hole.jsonl  (one line per hole: class sizes, #DL, #DL->DL steps, cycle lengths, violators, D-fail homology)
"""
import sys, json, argparse
from collections import Counter
import networkx as nx
from tg_engine import HoleData, read_graphs, FEATS

ROLE = 'aMAB'


def move_type(H, k, p, q, K):
    """local type of a Kempe move at state k: role pair in k's frame + link positions (relative to j) the component meets."""
    inf = H.info[k]; s = H.sp.states[k]; li = H.sp.linki; j = inf['j']
    c = [s[li[(j + t) % 5]] for t in range(5)]
    role = {c[0]: 'a', c[1]: 'M', c[3]: 'A', c[4]: 'B'}
    pr = ''.join(sorted((role[p], role[q]), key=ROLE.index))
    touch = ''.join(str(t) for t in range(5) if K >> li[(j + t) % 5] & 1)
    return pr + ':' + (touch or '-')


def cert(H, cls_states, cycles):
    S = set(cls_states)
    oncyc = [x for c in cycles for x in c]
    fill = [k for k in cls_states if H.kind[k] == 'F']
    # escape moves from cycle states
    esc_types = []; nesc = []; esc_to = Counter(); alltypes = Counter()
    for k in oncyc:
        ts = set(); ne = 0
        for t, p, q, K in H.sp.moves(k):
            if t == k: continue
            ty = move_type(H, k, p, q, K); alltypes[ty] += 1
            if H.kind[t] != 'DL':
                ts.add(ty); ne += 1; esc_to[H.kind[t]] += 1
        esc_types.append(ts); nesc.append(ne)
    common = set.intersection(*esc_types) if esc_types else set()
    # vertex-disjoint drains (Menger): cycle states -> filled states inside the class
    D = nx.DiGraph()
    for k in cls_states:
        D.add_edge(('i', k), ('o', k), capacity=1)
        for t in H.sp.G[k]:
            D.add_edge(('o', k), ('i', t), capacity=1)
    for k in oncyc: D.add_edge('SRC', ('i', k), capacity=1)
    for k in fill: D.add_edge(('o', k), 'SNK', capacity=1)
    flow = nx.maximum_flow_value(D, 'SRC', 'SNK') if fill else 0
    # violators in the class (D failures) and their homology bits
    viol = [k for k in cls_states if H.kind[k] != 'F' and (H.info[k]['D1fail'] or H.info[k]['D2fail'])]
    vh = Counter()
    if H.homology:
        for k in viol:
            i = H.info[k]; Hh = i['H']
            if i['D2fail']: vh['D2:' + str((Hh['C_MB'], Hh['C_AA']) if i['L2'] else ('noL2', Hh['C_AA']))] += 1
            if i['D1fail']: vh['D1:' + str((Hh['C_MA'], Hh['C_AB']) if i['L1'] else ('noL1', Hh['C_AB']))] += 1
    cych = Counter(str(H.info[k].get('H')) for k in oncyc) if H.homology else {}
    kinds = Counter(H.kind[k] for k in cls_states)
    return dict(N=len(cls_states), F=kinds['F'], DL=kinds['DL'], S=kinds['S'], cyc=[len(c) for c in cycles],
                dF=sorted(Counter(H.dF[k] for k in oncyc).items()), dS=sorted(Counter(H.dS[k] for k in oncyc).items()),
                nesc_min=min(nesc), nesc_max=max(nesc), esc_to=dict(esc_to), common_escape_types=sorted(common),
                esc_type_count=Counter(t for ts in esc_types for t in ts).most_common(12),
                drains=flow, nviol=len(viol), viol_homology=dict(vh), cyc_homology=dict(cych))


def run_hole(rot, h, homology):
    H = HoleData(rot, h, homology=homology)
    cycles = H.allDL_cycles(); steps = H.dl_steps()
    oncyc = {x: ci for ci, c in enumerate(cycles) for x in c}
    st = [dict(s=s, t=t, cyc=oc, cl=H.cl[s], fs=[H.info[s]['f'][f] for f in FEATS], ft=[H.info[t]['f'][f] for f in FEATS],
               H=(H.info[s].get('H'), H.info[t].get('H')) if homology else None) for s, t, oc in steps]
    cls = {}
    for k in range(H.S): cls.setdefault(H.cl[k], []).append(k)
    certs = []
    for c, mem in cls.items():
        cc = [cy for cy in cycles if H.cl[cy[0]] == c]
        if cc: certs.append(cert(H, mem, cc))
    viol = [k for k in range(H.S) if H.kind[k] not in ('F',) and (H.info[k]['D1fail'] or H.info[k]['D2fail'])]
    vh = Counter()
    if homology:
        for k in viol:
            i = H.info[k]; Hh = i['H']
            if i['D2fail'] and i['L2']: vh['D2(L2,inA) MB,AA=%s,%s' % (Hh['C_MB'], Hh['C_AA'])] += 1
            if i['D2fail'] and not i['L2']: vh['D2(noL2,notinA)'] += 1
            if i['D1fail'] and i['L1']: vh['D1(L1,inB) MA,AB=%s,%s' % (Hh['C_MA'], Hh['C_AB'])] += 1
            if i['D1fail'] and not i['L1']: vh['D1(noL1,notinB)'] += 1
    kinds = Counter(H.kind)
    hole = dict(h=h, S=H.S, ncls=len(cls), F=kinds['F'], DL=kinds['DL'], Sk=kinds['S'], nsteps=len(steps),
                ncycsteps=sum(1 for x in steps if x[2]), cyc=[len(c) for c in cycles], nviol=len(viol), viol_homology=dict(vh),
                word=''.join(str(min(len(rot[x]), 9)) for x in rot[h]))
    return hole, st, certs


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('graphs'); ap.add_argument('out')
    ap.add_argument('--names'); ap.add_argument('--holes-from'); ap.add_argument('--homology', action='store_true')
    ap.add_argument('--stride', type=int, default=1); ap.add_argument('--offset', type=int, default=0)
    ap.add_argument('--maxn', type=int, default=10 ** 9)
    a = ap.parse_args()
    names = set(a.names.split(',')) if a.names else None
    holes = None
    if a.holes_from:
        holes = {}
        for l in open(a.holes_from):
            d = json.loads(l)
            if d['allDLcyc']: holes.setdefault(d['graph'], []).append(d['hole'])
        names = set(holes) if names is None else names & set(holes)
    G = read_graphs(a.graphs, names)
    fs = open(a.out + '.steps.jsonl', 'w'); fc = open(a.out + '.cert.jsonl', 'w'); fh = open(a.out + '.hole.jsonl', 'w')
    for gi, (name, rot) in enumerate(sorted(G.items())):
        if gi % a.stride != a.offset or len(rot) > a.maxn: continue
        hs = holes[name] if holes else [v for v in range(len(rot)) if len(rot[v]) == 5]
        for h in hs:
            hole, st, certs = run_hole(rot, h, a.homology)
            fh.write(json.dumps(dict(graph=name, **hole)) + '\n')
            fs.write(json.dumps(dict(graph=name, h=h, steps=st)) + '\n')
            for c in certs: fc.write(json.dumps(dict(graph=name, h=h, word=hole['word'], **c)) + '\n')
        fs.flush(); fc.flush(); fh.flush()
        print(name, flush=True)
