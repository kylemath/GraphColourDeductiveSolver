#!/usr/bin/env python3
"""Track G [exploratory]: anatomy of every all-DL pi-cycle and of the escapes from it.

For each all-DL pi-cycle (in pi order) print one character per state:
   's' : sigma (swap of K_{alpha mu}(x_{j+2}), the hole's own alpha-mu chain) leads to a non-DL state
   'e' : sigma does not escape, but some other Kempe move does
   '.' : no Kempe move leaves DL (dS = 2)
plus the move-type multiset of escapes (role pair : link positions met, canonical modulo complement in the pair graph),
the escape targets' lock status, and (with --homology) the Z/2 classes of the chains at cycle states.
Also, for comparison, the same sigma-escape rate on all DL states of the hole that are not on cycles.
usage: tg_cycles.py GRAPHFILE OUT.jsonl [--names ...] [--holes-from KCLASS3.jsonl] [--homology]
"""
import sys, json, argparse
from collections import Counter
from tg_engine import HoleData, read_graphs

ROLE = 'aMAB'


def canon_type(H, k, p, q, K):
    inf = H.info[k]; s = H.sp.states[k]; li = H.sp.linki; j = inf['j']
    c = [s[li[(j + t) % 5]] for t in range(5)]
    role = {c[0]: 'a', c[1]: 'M', c[3]: 'A', c[4]: 'B'}
    pr = ''.join(sorted((role[p], role[q]), key=ROLE.index))
    touch = frozenset(t for t in range(5) if K >> li[(j + t) % 5] & 1)
    allpq = frozenset(t for t in range(5) if c[t] in (p, q))
    if not touch: return pr + ':-'            # component misses the link
    if touch == allpq: return pr + ':all'     # component holds every link vertex of colours p, q (e.g. sigma)
    tt = min(''.join(map(str, sorted(touch))), ''.join(map(str, sorted(allpq - touch))), key=lambda z: (len(z), z))
    return pr + ':' + tt


def sigma(H, k):
    sp = H.sp; s = sp.states[k]; li = sp.linki; j = H.info[k]['j']
    c = [s[li[(j + t) % 5]] for t in range(5)]; al, mu = c[0], c[1]
    cm = sp.cmasks(s); K = sp.flood(1 << li[(j + 2) % 5], cm[al] | cm[mu])
    return sp.index[sp.swap(s, K, al, mu)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('graphs'); ap.add_argument('out'); ap.add_argument('--names'); ap.add_argument('--holes-from')
    ap.add_argument('--homology', action='store_true')
    a = ap.parse_args()
    names = set(a.names.split(',')) if a.names else None; holes = None
    if a.holes_from:
        holes = {}
        for l in open(a.holes_from):
            d = json.loads(l)
            if d['allDLcyc']: holes.setdefault(d['graph'], []).append(d['hole'])
        names = set(holes) if names is None else names & set(holes)
    G = read_graphs(a.graphs, names); fo = open(a.out, 'w')
    for name, rot in sorted(G.items()):
        hs = holes[name] if holes else [v for v in range(len(rot)) if len(rot[v]) == 5]
        for h in hs:
            H = HoleData(rot, h, homology=a.homology)
            cycles = H.allDL_cycles()
            if not cycles: continue
            oncyc = set(x for c in cycles for x in c)
            # sigma-escape rate on non-cycle DL states
            ndl = [k for k in range(H.S) if H.kind[k] == 'DL' and k not in oncyc]
            sig_rate = sum(1 for k in ndl if H.kind[sigma(H, k)] != 'DL') / max(1, len(ndl))
            for c in cycles:
                word = []; types = Counter(); tgt = Counter(); hom = Counter(); jseq = []; dseq = []; hseq = []
                for k in c:
                    sg = H.kind[sigma(H, k)] != 'DL'
                    esc = [(t, canon_type(H, k, p, q, K)) for t, p, q, K in H.sp.moves(k) if t != k and H.kind[t] != 'DL']
                    for t, ty in esc:
                        types[ty] += 1; i = H.info[t] if H.kind[t] != 'F' else None
                        tgt['F' if i is None else ('L1only' if i['L1'] else ('L2only' if i['L2'] else 'nolock'))] += 1
                    word.append('s' if sg else ('e' if esc else '.')); jseq.append(H.info[k]['j'])
                    dseq.append(str(H.dS[k]))
                    if a.homology:
                        hb = H.info[k]['H']; hom[json.dumps(hb, sort_keys=True)] += 1
                        hseq.append(str(2 * (hb['C_MA'] or 0) + (hb['C_MB'] or 0)))
                cls = [k for k in range(H.S) if H.cl[k] == H.cl[c[0]]]; kinds = Counter(H.kind[k] for k in cls)
                viol = sum(1 for k in cls if H.kind[k] != 'F' and (H.info[k]['D1fail'] or H.info[k]['D2fail']))
                rec = dict(graph=name, h=h, word=''.join(str(min(len(rot[x]), 9)) for x in rot[h]), L=len(c),
                           esc=''.join(word), j=''.join(map(str, jseq)), dS=''.join(dseq), hseq=''.join(hseq), types=dict(types), targets=dict(tgt),
                           cls=[len(cls), kinds['F'], kinds['DL'], kinds['S'], viol], noncyc_DL=len(ndl),
                           noncyc_sigma_rate=round(sig_rate, 4), hom=dict(hom))
                fo.write(json.dumps(rec) + '\n'); fo.flush()
        print(name, flush=True)


if __name__ == '__main__':
    main()
