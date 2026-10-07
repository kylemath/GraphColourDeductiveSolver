#!/usr/bin/env python3
"""[exploratory] NightSigmaImage: the sigma-image set of every Gamma-cycle at a (5,5,5,5,6) hole.
Sources: (a) the 27 holes x 2 orientations of jobak-66dump.json (orders 25-27, rotations included);
(b) gentri orders 17-24 (both orientations), every (5,5,5,5,6) hole.  Output: one JSON line per Gamma-cycle.
Per state r of Z: pos (period position 0..9, 0 = R3k4), sigma(r)=s: fixed?, locks of s, cycle of s (Z? Gamma?),
place of s in its excursion (index in u-run, u, f), and (for Lock2-only / lockless s) the excursion mass u-3f."""
import sys, os, json
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../27-studio-positive-config/jobuv'))
import uv_lib
from kempe_py import gentri_rotation
NM = {(3, 4): 0, (1, 1): 1, (3, 3): 2, (1, 0): 3, (3, 2): 4, (1, 4): 5, (3, 1): 6, (1, 3): 7, (3, 0): 8, (1, 2): 9}
def holes6(rot):
    for h, L in enumerate(rot):
        if len(L) != 5: continue
        d = sorted(len(rot[x]) for x in L)
        if d != [5, 5, 5, 5, 6]: continue
        ring = set(u for x in L for u in rot[x]) - set(L) - {h}
        if len(ring) != 6: continue
        if sum(1 for a in ring for b in rot[a] if b in ring) != 12: continue
        yield h
def analyse(rot, h, tag):
    uv_lib.load = lambda name, mirror: rot
    H = uv_lib.Hole('x', h, False); S = H.S
    q = next(t for t in range(5) if len(rot[H.L[t]]) == 6)
    filled = [H.filled(k) for k in range(S)]
    # excursion structure: for unfilled s, run start, index, u, f
    def place(s):
        if not any(filled[x] for x in H.cycles[H.cyc[s]]): return -1, 0, 0
        a = s; i = 0
        while not filled[H.pinv[a]]: a = H.pinv[a]; i += 1
        u = 0; b = a
        while not filled[b]: b = H.pi[b]; u += 1
        f = 0
        while filled[b]: b = H.pi[b]; f += 1
        return i, u, f
    # class membership (Kempe classes) via sp.classes if available
    out = []
    for ci, Z in enumerate(H.cycles):
        if not all(H.DL[x] for x in Z): continue
        rows = []
        for r in Z:
            j, ty, hi, roles = H.frame(r); k = (q - j) % 5; pos = NM.get((ty, k))
            al, mu, A, B = roles
            strict = [H.col(r, H.w[(j + t) % 5]) for t in range(5)] == [B, A, B, mu, A]
            s = H.sigma(r); lk = H.locks(s); T = H.cyc[s]
            i, u, f = place(s)
            rows.append(dict(r=r, pos=pos, strict=strict, ty=ty, k=k, s=s, fixed=(s == r), l1=lk[0], l2=lk[1], T=T, TisZ=(T == ci),
                             Tgamma=all(H.DL[x] for x in H.cycles[T]), TL=len(H.cycles[T]), TW=H.W[T], i=i, u=u, f=f,
                             sDL=H.DL[s], tpos=H.cycles[T].index(s)))
        out.append(dict(tag=tag, hole=h, cyc=ci, L=len(Z), rows=rows))
    return out, H
if __name__ == '__main__':
    mode = sys.argv[1]; fo = open(sys.argv[2], 'w')
    if mode == 'dump':
        d = json.load(open(os.path.join(HERE, '../27-studio-positive-config/jobuv/jobak-66dump.json'))); seen = set()
        for r in d:
            key = (r['run'], r['name'], r['hole'])
            if key in seen: continue
            seen.add(key)
            res, H = analyse(r['rotation'], r['hole'], '%s:%s' % (r['run'], r['name']))
            for x in res: fo.write(json.dumps(x) + '\n')
            print(key, len(res), flush=True)
    else:
        G = os.path.join(HERE, '../../../studiointel/gentri/tri%d.txt')
        orders = [int(x) for x in mode.split(',')]
        for n in orders:
            for gi, l in enumerate(open(G % n)):
                if not l.startswith('G'): continue
                rot0 = gentri_rotation(l)
                for mir in (0, 1):
                    rot = [list(reversed(x)) for x in rot0] if mir else rot0
                    for h in holes6(rot):
                        res, H = analyse(rot, h, 'g%d#%d%s' % (n, gi, 'm' if mir else ''))
                        for x in res: fo.write(json.dumps(x) + '\n')
                        if res: print(n, gi, mir, h, len(res), flush=True)
