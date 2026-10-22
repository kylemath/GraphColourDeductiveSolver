# Semigroup closure with S3 symmetry reduction (stabiliser of the skeleton colour 0), uint16 relations, k inserted rows.
# Words: pairs (a,b) of level rows, both with skeleton colour 0; top row glued as pi(b), pi in S4 (all 24 tracked jointly).
# Element of a word of length m: keys (qa0,qa1,qb0,qb1,a0,b0), P[pi] = 16x16 relation (inner column states col 0 -> col m-1).
# Layers E_m = canon(E_{m-1} . G).  Closed elements of E_m (qa0==qa1, qb0==qb1) <-> level pairs of length m.
# Pair fillable with renaming pi iff trace(P[pi] . T(a_last, a0, pi b_last, pi b0)) != 0.  Sequence of layers is eventually periodic.
import sys, itertools, numpy as np, time, json, collections
from fill import build_T, inner_states
from lev import PERMS

S3 = [p for p in PERMS if p[0] == 0]                      # stabiliser of colour 0
PIDX = {p: i for i, p in enumerate(PERMS)}
def lev_automaton(nodefect=False):
    S = [(g, d, x) for g in range(4) for d in range(2) for x in range(4)]
    A = {}
    for (g, d, x) in S:
        outs = []
        for y in range(4):
            if y == x: continue
            if y == 0:
                if g == 2: outs.append((y, (0, d, 0)))
                elif g in (1, 3) and d == 0 and not nodefect: outs.append((y, (0, 1, 0)))
            else:
                if g + 1 <= 2: outs.append((y, (g+1, d, y)))
                elif g + 1 == 3 and d == 0 and not nodefect: outs.append((y, (3, d, y)))
        A[(g, d, x)] = outs
    return A
def run(k, nodefect=False, maxm=80, verbose=True, logf=None):
    T, n = build_T(k); T = T.astype(np.uint16); assert n == 16
    IS = inner_states(k); isid = {s: i for i, s in enumerate(IS)}
    A = lev_automaton(nodefect); S = sorted(A); sid = {s: i for i, s in enumerate(S)}; nS = len(S)
    succ = {sid[s]: [(y, sid[t]) for (y, t) in A[s]] for s in S}
    lastx = np.array([s[2] for s in S])
    def D(xa, xb):
        out = np.zeros(n, dtype=np.uint16)
        for i, s in enumerate(IS):
            col = (xa,) + s + (xb,)
            if all(col[j] != col[j+1] for j in range(len(col)-1)): out[i] = 1 << i
        return out
    Dm = {(xa, xb): D(xa, xb) for xa in range(4) for xb in range(4)}
    # symmetry data: for rho in S3: state map, inner-state permutation, pi conjugation map
    sym = []
    for rho in S3:
        smap = np.array([sid[(g, d, rho[x])] for (g, d, x) in S])
        imap = np.array([isid[tuple(rho[c] for c in s)] for s in IS])      # inner state i -> rho(i)
        pmap = np.array([PIDX[tuple(rho[PERMS[p][rho.index(c)]] for c in range(4))] for p in range(24)])  # rho pi rho^-1
        sym.append((rho, smap, imap, pmap))
    # bit permutation of a 16-bit mask by imap: lookup table
    def bitperm_table(imap):
        tab = np.zeros(1 << 16, dtype=np.uint16)
        for mval in range(1 << 16):
            v = 0
            for i in range(16):
                if (mval >> i) & 1: v |= 1 << int(imap[i])
            tab[mval] = v
        return tab
    tabs = [bitperm_table(imap) for (_, _, imap, _) in sym]
    def canon(keys, Ps):
        """elementwise lexicographic min over the S3 images"""
        N = len(keys); best_k = None; best_P = None
        cands = []
        for (rho, smap, imap, pmap), tab in zip(sym, tabs):
            rho = np.array(rho)
            K2 = keys.copy(); K2[:, 0] = smap[keys[:, 0]]; K2[:, 1] = smap[keys[:, 1]]; K2[:, 2] = smap[keys[:, 2]]; K2[:, 3] = smap[keys[:, 3]]
            K2[:, 4] = rho[keys[:, 4]]; K2[:, 5] = rho[keys[:, 5]]
            # P'[rho pi rho^-1] = Q P[pi] Q^T : rows permuted by imap, columns by bit permutation
            P2 = np.zeros_like(Ps)
            Pperm = tab[Ps]                                   # columns permuted
            P2[:, pmap, :] = Pperm[:, :, :]                   # pi index -> rho pi rho^-1
            P3 = np.zeros_like(P2); P3[:, :, imap] = P2       # rows permuted: new row imap[i] = old row i
            flat = np.concatenate([K2.astype(np.uint16), P3.reshape(N, -1)], axis=1)
            cands.append(flat)
        C = np.stack(cands)                                   # (6, N, W)
        W = C.shape[2]; alive = np.ones((len(sym), N), dtype=bool); out = np.zeros((N, W), dtype=np.uint16)
        for w in range(W):
            col = np.where(alive, C[:, :, w], np.uint16(65535))
            mn = col.min(axis=0); out[:, w] = mn
            alive &= (C[:, :, w] == mn[None, :])
        keys2 = out[:, :6].astype(np.int16); Ps2 = out[:, 6:].reshape(N, 24, n)
        return keys2, Ps2
    def dedupe(keys, Ps):
        flat = np.concatenate([keys.astype(np.uint16), Ps.reshape(len(Ps), -1)], axis=1)
        u = np.unique(flat, axis=0)
        return u[:, :6].astype(np.int16), u[:, 6:].reshape(len(u), 24, n)
    keys = []; Ps = []
    for qa0 in S:
        for (ya, qa1) in A[qa0]:
            for qb0 in S:
                for (yb, qb1) in A[qb0]:
                    keys.append((sid[qa0], sid[qa1], sid[qb0], sid[qb1], ya, yb))
                    Ps.append(np.stack([Dm[(ya, p[yb])] for p in PERMS]))
    keys = np.array(keys, dtype=np.int16); Ps = np.array(Ps, dtype=np.uint16)
    keys, Ps = dedupe(*canon(keys, Ps))
    perms_arr = np.array(PERMS)
    def step(keys, Ps):
        newk = []; newP = []
        qa1 = keys[:, 1]; qb1 = keys[:, 3]
        for ia in range(nS):
            ma = qa1 == ia
            if not ma.any(): continue
            for ib in range(nS):
                m = ma & (qb1 == ib)
                if not m.any(): continue
                K = keys[m]; P = Ps[m]; xa = lastx[ia]; xb = lastx[ib]
                for (ya, na) in succ[ia]:
                    for (yb, nb) in succ[ib]:
                        Tt = T[xa, ya, perms_arr[:, xb], perms_arr[:, yb]]      # (24, n)
                        C = np.zeros_like(P)
                        for j in range(n):
                            C |= (((P >> np.uint16(j)) & np.uint16(1)) * Tt[None, :, j][:, :, None]).astype(np.uint16)
                        K2 = K.copy(); K2[:, 1] = na; K2[:, 3] = nb
                        newk.append(K2); newP.append(C)
        keys2 = np.concatenate(newk); Ps2 = np.concatenate(newP)
        return dedupe(*canon(keys2, Ps2))
    def closed_check(keys, Ps):
        m = (keys[:, 0] == keys[:, 1]) & (keys[:, 2] == keys[:, 3])
        K = keys[m]; P = Ps[m]; N = len(K)
        if N == 0: return 0, 0, [], collections.Counter()
        xa = lastx[K[:, 1]]; xb = lastx[K[:, 3]]; a0 = K[:, 4]; b0 = K[:, 5]
        Tc = T[xa[:, None], a0[:, None], perms_arr[:, xb.astype(int)].T, perms_arr[:, b0.astype(int)].T]   # (N, 24, n)
        tr = np.zeros((N, 24), dtype=bool)
        for i in range(n):
            for j in range(n):
                tr |= (((P[:, :, i] >> np.uint16(j)) & 1) & ((Tc[:, :, j] >> np.uint16(i)) & 1)).astype(bool)
        good = tr.any(axis=1); bad = int((~good).sum())
        badlist = [tuple(int(v) for v in K[r]) for r in np.where(~good)[0][:5]]
        npi = collections.Counter(tr.sum(axis=1).tolist())
        return N, bad, badlist, npi
    seen = {}; layers = []
    for m in range(1, maxm+1):
        t0 = time.time()
        if m > 1: keys, Ps = step(keys, Ps)
        h = hash((keys.tobytes(), Ps.tobytes()))
        N, bad, badlist, npi = closed_check(keys, Ps)
        rec = dict(k=k, nodefect=nodefect, m=m, nelem=len(keys), nclosed=N, bad=bad, badex=badlist, npi=sorted(npi.items()), sec=round(time.time()-t0, 1))
        if verbose: print(json.dumps(rec), flush=True)
        if logf: logf.write(json.dumps(rec) + '\n'); logf.flush()
        layers.append(rec)
        if h in seen:
            msg = dict(PERIODIC=True, layer=m, equals=seen[h], period=m - seen[h])
            print(json.dumps(msg), flush=True)
            if logf: logf.write(json.dumps(msg) + '\n'); logf.flush()
            return layers, seen[h], m
        seen[h] = m
    return layers, None, None
if __name__ == '__main__':
    k = int(sys.argv[1]); nodefect = len(sys.argv) > 2 and sys.argv[2] == 'nodefect'
    with open(f'closure2_k{k}{"_nodefect" if nodefect else ""}.jsonl', 'w') as f:
        run(k, nodefect, logf=f)
