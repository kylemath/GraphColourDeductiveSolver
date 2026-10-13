"""Proof-attempt library (Long Table, PROOF-ATTEMPT-1, 13 Oct 2026).

Sphere side: Tait duals of census holes via TrackT tt_lib (read-only import), near-rigid (1212) runs,
and planar quantities at every state (sides of H_t, regions of Q_t, A5v, chord positions).
Abstract side: chord-diagram normal form shared with the SAT code (sat_t1v.py in ..).

Conventions (frame-relative, TrackT): at state t with M_t containing f_k, e_i := f_{k-2+i}.
  Q_t = E - M_t = X_t u Y_t, X_t through e1,e3 (even), Y_t through e0,e4 (odd).
  H_t = M_{t-1} u M_t; at a Hamiltonian state it passes v via e2 (in M_t) and e4 (in M_{t-1}).
"""
import sys, os
from collections import deque
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.join(HERE, '../../../../../SolvingFrameworkPlan/docs/working/TrackT')
sys.path.insert(0, os.path.abspath(TT))
import tt_lib  # noqa: E402  (read-only reuse: G5, tait_dual, ham_states, run_from, run_back)


def bits(S):
    k = 0
    while S:
        if S & 1: yield k
        S >>= 1; k += 1


class Sphere:
    """A hole of a triangulated sphere in Tait form, with primal face data for side computations."""
    def __init__(self, rot, h):
        self.rot, self.h = rot, h
        self.g = tt_lib.tait_dual(rot, h)
        g = self.g
        self.pv = [u for u in range(len(rot)) if u != h]
        # primal adjacency through dual edge ids
        self.padj = {u: [] for u in self.pv}
        for e, (u, w) in enumerate(g.prim):
            self.padj[u].append((w, e)); self.padj[w].append((u, e))
        self.link = rot[h]  # x_0..x_4 ; f_t dual to x_t x_{t+1}

    def regions(self, S):
        """components of S^2 - S as sets of primal vertices (faces of G), S an edge mask of G."""
        seen = {}; comps = []
        for s in self.pv:
            if s in seen: continue
            comp = [s]; seen[s] = len(comps); dq = deque([s])
            while dq:
                x = dq.popleft()
                for y, e in self.padj[x]:
                    if (S >> e) & 1: continue
                    if y not in seen:
                        seen[y] = len(comps); comp.append(y); dq.append(y)
            comps.append(set(comp))
        return comps, seen

    def faces_of_fedge(self, t):
        """primal endpoints of f_t = link edge x_t x_{t+1}"""
        x = self.link
        return x[t % 5], x[(t + 1) % 5]


def nr_windows(sp, maxham=400000):
    """all maximal windows of a Hamiltonian-anchored run in which the k(H) word alternates exactly 1,2
    (DL-type states throughout).  Returns list of lists of states (P, M)."""
    g = sp.g
    hs = tt_lib.ham_states(g, limit=maxham)
    seen = set(); out = []
    for P, M in hs:
        if (P, M) in seen or g.dl_info(P, M) is None: continue
        fw, closed = tt_lib.run_from(g, P, M)
        if closed is not True and g.dl_info(*fw[-1]) is None: fw = fw[:-1]
        bw = tt_lib.run_back(g, P, M) if closed is not True else [(P, M)]
        states = list(reversed(bw))[:-1] + fw
        for s in states: seen.add(s)
        w = [g.kH(*s) for s in states]
        # maximal alternating 1/2 windows
        i = 0; L = len(states)
        while i < L:
            if w[i] not in (1, 2): i += 1; continue
            j = i
            while j + 1 < L and w[j + 1] in (1, 2) and w[j + 1] != w[j]: j += 1
            if j - i + 1 >= 2 and 1 in w[i:j + 1]:
                out.append(states[i:j + 1])
            i = j + 1
    # dedupe
    uniq = {}
    for W in out: uniq[tuple(W)] = W
    return list(uniq.values())


def state_info(sp, P, M):
    """planar quantities of the DL state (P, M) = (M_{t-1}, M_t)."""
    g = sp.g
    k, X, Y = g.dl_info(P, M)
    f = g.fv
    e = [f[(k - 2 + i) % 5] for i in range(5)]
    v = 0
    partner = g.other(e[2], v)
    Xv = set(); Yv = set()
    for ed in bits(X):
        a, b = g.E[ed]; Xv.update((a, b))
    for ed in bits(Y):
        a, b = g.E[ed]; Yv.update((a, b))
    Xv.discard(0); Yv.discard(0)
    a5v = partner in Xv
    # regions of S^2 - Q
    comps, where = sp.regions(X | Y)
    # D_X: region containing the faces of e2 (e2 not in Q; it lies on the e2 side of X)
    fx = sp.faces_of_fedge((k) % 5)        # e2 = f_k
    DX = comps[where[fx[0]]]
    fy = sp.faces_of_fedge((k - 2) % 5)    # e0 = f_{k-2}; e0 in Q.  use corner faces instead
    H = P | M
    kh = g.kH(P, M)
    info = dict(k=k, X=len(Xv), Y=len(Yv), a5v=a5v, kH=kh, nreg=len(comps),
                regsizes=sorted(len(c) for c in comps), DX=len(DX))
    # corners at v: corner (f_{t-1}, f_t) contains link vertex x_t.  D_Y = region of corner (e4,e0) = x_{k-2}
    xk = sp.link
    DY = comps[where[xk[(k - 2) % 5]]]          # corner between e4=f_{k+2} and e0=f_{k-2}: x_{k-2}
    info['DY_corner'] = len(DY)
    # the three regions: corner x_{k} (between e1=f_{k-1}, e2=f_k) and x_{k+1} (e2,e3) lie in D_X
    info['DX_corner'] = len(comps[where[xk[k % 5]]])
    info['O_corner'] = len(comps[where[xk[(k - 1) % 5]]])  # corner (e0,e1) = x_{k-1}
    if kh == 1:
        sides, sw = sp.regions(H)
        assert len(sides) == 2
        # inside := side of e3 = f_{k+1}: its faces x_{k+1}, x_{k+2}
        ins = sides[sw[xk[(k + 1) % 5]]]
        info['area_in'] = len(ins); info['area_out'] = len(sides[1 - sw[xk[(k + 1) % 5]]])
        # chord positions along H from v via e2
        seq = []; x = g.other(e[2], 0); ed = e[2]
        while x != 0:
            seq.append(x)
            nx = [tt for tt in g.inc[x] if (H >> tt & 1) and tt != ed]
            ed = nx[0]; x = g.other(ed, x)
        pos = {x: i + 1 for i, x in enumerate(seq)}
        info['pos_e0'] = pos[g.other(e[0], 0)]
        info['pos_e1'] = pos[g.other(e[1], 0)]
        info['pos_e3'] = pos[g.other(e[3], 0)]
        info['n'] = g.n
    return info
