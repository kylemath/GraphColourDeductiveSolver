#!/usr/bin/env python3
"""Track I: check the switching-parity identity (*) and rigid isolation on real triangulations (any closed surface).

For every DL state c (locks from the TrackH vertex engine, read-only import) at every degree-5 hole:
  build the dual Tait instance (ti_lib.primal_to_tait; faces = link triangles, no orientation needed), then
    kH = #comp(H), k12 = #comp(F12), kHX = #comp(H^X), k12X = #comp(F12^X), pHX = pairing of H^X at v,
    (*)  kH + k12 + kHX + k12X + [pHX == (e1e4)(e2e3)]  == 0 (mod 2)      [Track I Lemma 3]
  with X = F13-trail of v through e1.  Also: Tait pairings of F12/F13 at c (DL-type on the sphere by D),
  rigid flags (engine component counts (1,1,2,1,2,1)) of c and of pi(c), and the Tait prediction of pi(c) rigid.
usage: ti_check.py GRAPHFILE STRIDE MAXGRAPHS OUT.jsonl [name-prefix-filter]"""
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TrackH'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th_engine import Hole                       # read-only reuse
from th_rigidscan_lib import counts              # read-only reuse
from ti_lib import Tait, primal_to_tait, DL12, DL13, DLimg, NDLimg

def tait_data(E):
    T = Tait(E)
    M = {c: {k for k, e in enumerate(E) if e[2] == c} for c in (1, 2, 3)}
    H = M[2] | M[3]; F12 = M[1] | M[2]; F13 = M[1] | M[3]
    d = dict(kH=T.ncomp(H), k12=T.ncomp(F12), k13=T.ncomp(F13), p12=T.pairing(F12), p13=T.pairing(F13))
    X, back = T.trail(F13, T.lab['e1']); X = set(X)
    d['Xback'] = back
    HX = H ^ X; F12X = F12 ^ X
    d['kHX'] = T.ncomp(HX); d['k12X'] = T.ncomp(F12X); d['pHX'] = T.pairing(HX)
    d['star'] = (d['kH'] + d['k12'] + d['kHX'] + d['k12X'] + (d['pHX'] == DLimg)) % 2
    d['pHXtype'] = 'DL' if d['pHX'] == DLimg else ('NDL' if d['pHX'] == NDLimg else 'cross')
    return d

def main():
    gf, stride, maxg, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    filt = sys.argv[5] if len(sys.argv) > 5 else ''
    tot = Counter(); k = 0; fo = open(out, 'a')
    for ln, l in enumerate(open(gf)):
        if ln % stride: continue
        p = l.split()
        if len(p) < 3 or not p[0].startswith(filt): continue
        rot = [list(map(int, r.split(','))) for r in p[2].split(';')]
        k += 1
        if k > maxg: break
        st = Counter()
        for h in [v for v in range(len(rot)) if len(rot[v]) == 5]:
            try:
                Hh = Hole(rot, h)
            except AssertionError:
                st['skip_hole'] += 1; continue
            S = len(Hh.states); info = [None] * S; rig = [False] * S; cols = [None] * S
            for i in range(S):
                r, col = Hh.analyse_state(i); info[i] = r; cols[i] = col
                if r['kind'] == 'DL': rig[i] = counts(Hh, col, r['roles']) == [1, 1, 2, 1, 2, 1]
            for i in range(S):
                r = info[i]
                if r['kind'] != 'DL': continue
                E = primal_to_tait(rot, h, cols[i], r['roles'], r['j'])
                d = tait_data(E)
                tag = 'rig' if rig[i] else 'nr'
                st['DL'] += 1
                st['tait_DL_pairings'] += (d['p12'] == DL12 and d['p13'] == DL13)
                st['D_ok'] += (r['D1'] and r['D2'])
                st['star_fail'] += d['star']
                st['star_fail_' + tag] += d['star']
                st['pHX_' + d['pHXtype']] += 1
                if rig[i]:
                    st['rigid'] += 1
                    st['rigid_tait_k111'] += (d['kH'], d['k12'], d['k13']) == (1, 1, 1)
                    t = r['pi']
                    if t is None: st['rigid_pi_undef'] += 1; continue
                    img_rig = rig[t]
                    st['rigid_to_rigid'] += img_rig
                    pred = d['pHXtype'] == 'DL' and d['kHX'] == 1 and d['k12X'] == 1 and d['k13'] == 1
                    st['pred_mismatch'] += (pred != img_rig)
                    if img_rig:
                        fo.write(json.dumps(dict(graph=p[0], hole=h, state=i, pi=t, D=[r['D1'], r['D2']],
                                                 tait={a: (sorted(map(sorted, b)) if isinstance(b, frozenset) else b)
                                                       for a, b in d.items()})) + '\n')
        tot.update(st)
        fo.write(json.dumps(dict(graph=p[0], stats=dict(st))) + '\n'); fo.flush()
    print(gf, filt, 'graphs', k, dict(sorted(tot.items())), flush=True)

if __name__ == '__main__':
    main()
