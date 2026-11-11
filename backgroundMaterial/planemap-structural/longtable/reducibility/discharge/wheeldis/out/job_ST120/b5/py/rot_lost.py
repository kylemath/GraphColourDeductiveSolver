#!/usr/bin/env python3
"""For each 'FAILED link' line of a --rot export log: the positive state and the K768 configurations that checkEmb
(rotation-blind) would use there, i.e. the mirror-only kills. Codes: s_j 100+j, p_i.(k+1) 200+3i+k; a class of several
letters (9 with its dominated letters) is not a host. usage: python3 -I rot_lost.py LOG KCFILE"""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import export_cert as E
R = E.R; R.U_HOST_ALWAYS = True
log, kcf = sys.argv[1], sys.argv[2]; model = 'kc:' + kcf
names = [l.split()[0] for l in open(kcf) if l.strip()]
for l in open(log):
    if not l.startswith('FAILED link'): continue
    f = l.split(); link = [int(c) for c in f[2]]; d = len(link); hi = f[4]
    st = {}
    for t in f[6:]:
        c, S = t.split('='); st[int(c)] = [int(x) for x in S]
    W = R.Window(d, link, None)
    E.ROT[0] = False; E.ROTW[0] = None
    rq = E.link_reqs(W, model, None)
    used = sorted(set(names[k] for req, k, e in rq if all(st.get(c) == [L] for c, L in req)))
    print('%s hi=%s state %s | mirror-only (rotation-blind) kills: %s' % (f[2], hi,
          ' '.join('%d=%s' % (c, ''.join(map(str, S))) for c, S in sorted(st.items()) if S != [9] and len(S) == 1) or '(all 9+)',
          ', '.join(used) or 'NONE'))
