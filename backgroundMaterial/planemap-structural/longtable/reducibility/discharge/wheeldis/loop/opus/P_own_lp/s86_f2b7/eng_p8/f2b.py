# Independent implementation (ext_f2b) of the outside team's full-wheel 2-ball private-letter exclusions.
# Semantics (read from their step2_cutting_plane.make_recv_spec_full2ball, re-implemented here):
#   rule = (p_deg, w_req, s_req); at spoke i of a receiver row of degree d it MATCHES iff
#     for every (off, allowed) in w_req: w[(i+off) % d] in allowed, and for every (off, v) in s_req: s[(i+off) % d] == v.
#   A matching rule removes the letter p_deg from the private-letter mask of that spoke:
#     d7_w6 / d8_w6 / d9_w6 : at every spoke with w_i = 6 (d = 7, 8, 9): Studio pmask(...) -> pmask & ~(1 << (p_deg - 5))  (M row)
#     d7_w7 / d8_w7 [sg]    : at every spoke with w_i = 7 (d = 7, 8), side sg = +1 / -1, neighbour c = w_{i+sg} and apex
#                             a = (s_i if sg == 1 else s_{i-1}) both in {5,6}: l3q mask m -> m & ~(1 << (p_deg - 5))  (lQ row)
#   Nothing is changed for d >= 10, for other letters, or for sides with c or a >= 7.
import json, random, itertools
import numpy as np
ACTIVE = True
_R = {}      # group -> list of (p_deg, wreq tuple, sreq tuple)
_IDX = {}    # group -> {(req_sm1, req_s0): [(wreq, sreq, bit)]}
STATS = {}
GROUPS = ('d7_w6', 'd8_w6', 'd9_w6', 'd7_w7_1', 'd7_w7_-1', 'd8_w7_1', 'd8_w7_-1')
def load(path, off=False, drop_frac=0.0, seed=0):
    R = json.load(open(path)); G = {'d7_w6': R['d7_w6'], 'd8_w6': R['d8_w6'], 'd9_w6': R['d9_w6'],
        'd7_w7_1': R['d7_w7']['1'], 'd7_w7_-1': R['d7_w7']['-1'], 'd8_w7_1': R['d8_w7']['1'], 'd8_w7_-1': R['d8_w7']['-1']}
    rng = random.Random(seed)
    for g in GROUPS:
        lst = []
        for p, wr, sr in G[g]:
            wd = {}
            for off_, al in wr:
                assert off_ not in wd; wd[int(off_)] = frozenset(int(x) for x in al)
            sd = {}
            for off_, v in sr:
                assert off_ not in sd; sd[int(off_)] = int(v)
            assert int(p) in (5, 6, 7, 8, 9)
            lst.append((int(p), tuple(sorted(wd.items())), tuple(sorted(sd.items()))))
        if off: lst = []
        elif drop_frac > 0:
            keep = sorted(rng.sample(range(len(lst)), int(round(len(lst) * (1 - drop_frac)))))
            lst = [lst[k] for k in keep]
        _R[g] = lst; STATS[g] = len(lst)
        idx = {}
        for p, wr, sr in lst:
            sd = dict(sr); key = (sd.get(-1), sd.get(0))
            idx.setdefault(key, []).append((wr, tuple((o, v) for o, v in sr), 1 << (p - 5)))
        _IDX[g] = idx
    return dict(STATS)
def _extra(g, d, w, s, i):
    idx = _IDX[g]; sm1, s0 = s[(i - 1) % d], s[i]; ex = 0
    for key in ((sm1, s0), (sm1, None), (None, s0), (None, None)):
        for wr, sr, bit in idx.get(key, ()):
            if ex & bit: continue
            if all(w[(i + o) % d] in al for o, al in wr) and all(s[(i + o) % d] == v for o, v in sr): ex |= bit
    return ex
def extra6(d, w, s, i):
    if not ACTIVE or d > 9 or d < 7: return 0
    return _extra('d%d_w6' % d, d, w, s, i)
def extra7(d, w, s, i, sg):
    if not ACTIVE or d not in (7, 8): return 0
    return _extra('d%d_w7_%d' % (d, sg), d, w, s, i)
def build_tables(path, rules_in_use, KT, MASK, MASK8, Mval, Qeff, Qeff8, sig2_of, ap, V6):
    """binary table for sep3r_f2b (SEP_F2B); the rules in use are the ones loaded into _IDX/_R (same objects as the python rows)."""
    assert not V6
    out = bytearray()
    pm = []
    for U in (7, 8, 9):
        K = np.asarray(KT[U]).astype(bool)
        pm.append(((~K).astype(np.uint8) * (1 << np.arange(5, dtype=np.uint8))).sum(axis=-1).astype(np.uint8))
    PM = np.stack(pm); assert PM.shape == (3,) + (5,) * 8
    out += PM.tobytes()
    for M, nm in ((MASK, 'MASK'), (MASK8, 'MASK8')):
        a = np.zeros(31250, dtype=np.uint8)
        for (sg_, c_, a_, w2_, w3_, w4_, o_), m_ in M.items():
            a[((((((0 if sg_ == 1 else 1) * 5 + c_ - 5) * 5 + a_ - 5) * 5 + w2_ - 5) * 5 + w3_ - 5) * 5 + w4_ - 5) * 5 + o_ - 5] = m_
        out += a.tobytes()
    EXM = np.zeros((3, 5, 5, 5, 5, 2, 2, 32))
    for ui, U in enumerate((7, 8, 9)):
        for wm1, sm1, s0, wp1 in itertools.product(range(5), repeat=4):
            for am, ar in itertools.product((0, 1), repeat=2):
                for m in range(32):
                    sg = sig2_of(U, wp1 + 5, s0 + 5, sm1 + 5, wm1 + 5, 7 if ar else 5, 7 if am else 5) + (m,)
                    EXM[ui, wm1, sm1, s0, wp1, am, ar, m] = Mval(sg)
    out += EXM.tobytes()
    for fn in (Qeff, Qeff8):
        Q = np.zeros((5, 5, 32))
        for c_, a_ in itertools.product((5, 6), repeat=2):
            for m in range(32): Q[c_ - 5, a_ - 5, m] = fn(c_, a_, m) if fn is Qeff else fn(c_, a_, m)
        out += Q.tobytes()
    def ser(g, dval):
        buckets = [dict() for _ in range(25)]
        for p, wr, sr in _R[g]:
            fw = 0
            for o, al in wr:
                bits = sum(1 << (x - 5) for x in al); fw |= ((~bits) & 31) << (5 * (o % dval))
            fs = 0; sd = dict(sr)
            for o, v in sr: fs |= ((~(1 << (v - 5))) & 31) << (5 * (o % dval))
            sm1s = [sd[-1] - 5] if -1 in sd else range(5); s0s = [sd[0] - 5] if 0 in sd else range(5)
            for a in sm1s:
                for b in s0s:
                    k = (fw, fs); buckets[a * 5 + b][k] = buckets[a * 5 + b].get(k, 0) | (1 << (p - 5))
        o = bytearray()
        for b in range(25):
            items = sorted(buckets[b].items()); o += np.array([len(items)], dtype='<u4').tobytes()
            if items: o += np.array([(fw, fs, kb) for (fw, fs), kb in items], dtype='<u8').tobytes()
        return bytes(o)
    for g, dv in (('d7_w6', 7), ('d8_w6', 8), ('d9_w6', 9), ('d7_w7_1', 7), ('d7_w7_-1', 7), ('d8_w7_1', 8), ('d8_w7_-1', 8)):
        out += ser(g, dv)
    open(path, 'wb').write(bytes(out))
