#!/usr/bin/env python3
"""Track A task 3: two-engine re-check of graphs carrying positive pi-cycles (w > 0).
Engine 1: picyc --full (both orientations): per hole the pi-cycle hist and class signatures [N, F, sum w].
Engine 2: uv_lib.Hole (kempe_py.Space + escape.pi_of, independent Python): per class N, F, the pi-cycles (L, w, kind counts)
and the Theorem W identity 4F - N = -5 sum w; class multisets (N, F, sum w) compared with engine 1 hole by hole.
Engine 2 is run at every hole that has a w > 0 cycle in either orientation (and at --holes extra ones).
usage: posw_verify.py GRAPHS.json OUT.jsonl     (GRAPHS.json: list of {name, faces}; one process)"""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, '/Users/kylemathewson/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/local-runs/27-studio-positive-config/jobuv')
from uv_lib import Hole
from tracka_lib import rot_from_faces, G
from posw_scan import picyc_raw, hole_summary
def py_hole(name, rot, h, mirror):
    H = Hole(name, h, mirror, rot=rot); sp = H.sp; sp.build_graph(); cl, nc = sp.classes()
    mem = [[] for _ in range(nc)]
    for k in range(H.S): mem[cl[k]].append(k)
    out = []
    for c in range(nc):
        M = mem[c]; F = sum(H.filled(k) for k in M); cyc = sorted({H.cyc[k] for k in M})
        assert all(cl[x] == c for z in cyc for x in H.cycles[z])     # classes are unions of pi-cycles
        cy = []
        for z in cyc:
            kinds = Counter(H.kind[x] for x in H.cycles[z]); cy.append((len(H.cycles[z]), H.W[z], dict(kinds), sum(H.DL[x] for x in H.cycles[z])))
        sw = sum(c_[1] for c_ in cy); wh = Counter(c_[1] for c_ in cy)
        out.append(dict(N=len(M), F=F, sumw=sw, thmW=(4 * F - len(M) == -5 * sw), ncyc=len(cy), w_hist=sorted(wh.items()),
                        pos=[c_ for c_ in cy if c_[1] > 0], negw=sum(c_[1] for c_ in cy if c_[1] < 0), Lpos=sum(c_[0] for c_ in cy if c_[1] > 0),
                        kinds=dict(sum((Counter(c_[2]) for c_ in cy), Counter()))))
    return H.L, [len(rot[x]) for x in H.L], out
if __name__ == '__main__':
    Gs = json.load(open(sys.argv[1])); f = open(sys.argv[2], 'w')
    for g in Gs:
        rot = rot_from_faces([tuple(t) for t in g['faces']]); s = G(rot).summary()
        rec = dict(name=g['name'], n=s['n'], frame=s['frame'], deg5=s['deg5'], maxdeg=s['maxdeg'], orient={})
        for mir in (False, True):
            hs = [hole_summary(r) for r in picyc_raw(rot, g['name'], mir)]
            rec['orient']['m' if mir else 'p'] = dict(holes=len(hs), npos=sum(h['npos'] for h in hs), posw=sum(h['posw'] for h in hs),
                max_cls_sumw=max(h['max_cls_sumw'] for h in hs), min_slack_big=min([-c[2] / c[0] for h in hs for c in h['cls'] if c[0] > 8] or [None]),
                pos_holes={str(h['hole']): dict(link=h['linkdeg'], pos=h['pos'], cls=h['cls'], states=h['states']) for h in hs if h['npos']},
                eq_big={str(h['hole']): [c for c in h['cls'] if c[0] > 8 and c[2] == 0] for h in hs if any(c[0] > 8 and c[2] == 0 for c in h['cls'])})
        rec['py'] = {}
        for o, mir in (('p', False), ('m', True)):
            todo = set(map(int, rec['orient']['p']['pos_holes'])) | set(map(int, rec['orient']['m']['pos_holes'])) \
                 | set(map(int, rec['orient'][o]['eq_big']))
            hs1 = {r['hole']: r for r in picyc_raw(rot, g['name'], mir)}
            for h in sorted(todo):
                L, ld, cls = py_hole(g['name'], rot, h, mir)
                agree = sorted((c['N'], c['F'], c['sumw']) for c in cls) == sorted(tuple(c[:3]) for c in hs1[h]['clsig'])
                rec['py']['%s%d' % (o, h)] = dict(link=L, linkdeg=ld, agree=agree, thmW=all(c['thmW'] for c in cls), classes=cls)
                print(g['name'], o, h, 'agree', agree, 'thmW', all(c['thmW'] for c in cls),
                      [(c['N'], c['F'], c['sumw'], c['pos'], c['negw']) for c in cls if c['pos'] or c['N'] > 8 and c['sumw'] == 0], flush=True)
        f.write(json.dumps(rec) + '\n'); f.flush()
        print(g['name'], {o: {k: v for k, v in rec['orient'][o].items() if k not in ('pos_holes', 'eq_big')} for o in rec['orient']}, flush=True)
