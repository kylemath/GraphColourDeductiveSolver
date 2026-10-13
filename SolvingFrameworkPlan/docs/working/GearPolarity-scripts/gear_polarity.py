# Gear-polarity test (exploratory). Reads 4square maps and gentri census files; uses ~/4square/kempe_engine.py.
# Usage: python3 gear_polarity.py [maps|gentri ORDERS...]
import sys, os, json, glob, time, math, collections, itertools
sys.path.insert(0, os.path.expanduser('~/4square'))
from kempe_engine import HoleGame
import mapio

GENTRI = os.path.expanduser('~/GraphColour/backgroundMaterial/planemap-structural/studiointel/gentri')


def gentri_graphs(order):
    for idx, line in enumerate(open(os.path.join(GENTRI, 'tri%d.txt' % order))):
        p = line.split()
        n = int(p[1]); nf = int(p[3]); nums = list(map(int, p[4:4 + 3 * nf]))
        faces = [nums[3 * i:3 * i + 3] for i in range(nf)]
        yield '%d:%d' % (order, idx), mapio.rot_from_faces(faces)


def map_graphs():
    for f in sorted(glob.glob(os.path.expanduser('~/4square/maps/*.json'))):
        d = json.load(open(f))
        rot, tri = mapio.load_map(d)
        if not tri: continue
        yield os.path.basename(f)[:-5] + '@%d' % d['hole'], rot, d['hole']


def same_comp(H, c, u, v, pair):
    if c[u] not in pair or c[v] not in pair: return False
    other = pair[1] if c[u] == pair[0] else pair[0]
    return v in H.chain_at(c, u, other)


class Acc:
    def __init__(self):
        self.c = collections.Counter(); self.fail = collections.Counter(); self.ex = {}
        self.rows = []  # DL-state feature rows
        self.moves = collections.Counter()
        self.cls = []

    def bad(self, key, ex):
        self.fail[key] += 1
        self.ex.setdefault(key, ex)


def analyse(name, rot, hole, A, cap=60000):
    n = len(rot); link = rot[hole]
    if len(link) != 5: return
    t0 = time.time()
    try:
        H = HoleGame(n, rot, hole, link, ncol=4, limit=cap)
    except RuntimeError:
        A.c['skipped_big'] += 1; return
    L = link
    nbrs_rim = lambda i: {(i + 1) % 5, (i - 1) % 5}
    # per-class tallies for the Theorem W identity
    tally = collections.defaultdict(collections.Counter)
    for k, c in enumerate(H.states):
        cid = H.cls[k]
        rimc = [c[x] for x in L]
        if H.filled[k]:
            # singleton index i: rim W X Y X Y
            i = next(t for t in range(5) if rimc.count(rimc[t]) == 1)
            x = [L[(i + s) % 5] for s in range(5)]
            W, X, Y = rimc[i], rimc[(i + 1) % 5], rimc[(i + 2) % 5]
            Z = ({0, 1, 2, 3} - {W, X, Y}).pop()
            m3s = not same_comp(H, c, x[2], x[4], (Y, Z))
            m3s_alt = same_comp(H, c, x[0], x[3], (W, X))
            m2s = not same_comp(H, c, x[1], x[3], (X, Z))
            m2s_alt = same_comp(H, c, x[0], x[2], (W, Y))
            if m3s != m3s_alt: A.bad('M3 dichotomy', (name, k))
            if m2s != m2s_alt: A.bad('M2 dichotomy', (name, k))
            tally[cid]['F'] += 1; tally[cid]['F_m3s'] += m3s; tally[cid]['F_m2s'] += m2s
            A.c['filled'] += 1
            # filled: odd rings (distance-2 rim pairs of different colours joined, ignoring the always-joined X..Y path)
            A.c['filled_odd_%d' % (int(m3s) + int(m2s))] += 1
        else:
            x, al, mu, ga, de = H.frame(c)
            l1, l2 = H.L1[k], H.L2[k]
            tally[cid]['U'] += 1; tally[cid]['U_notL1'] += (not l1); tally[cid]['U_notL2'] += (not l2)
            # full rim signature: for every colour pair, the partition of the rim cells of those colours into chains
            sig = []
            for p, q in itertools.combinations(range(4), 2):
                cells = [s for s in range(5) if rimc[(L.index(x[0]) + s) % 5] in (p, q)]
                # use frame positions s=0..4 (x[s])
                cells = [s for s in range(5) if c[x[s]] in (p, q)]
                part = []
                for s in cells:
                    for blk in part:
                        if same_comp(H, c, x[s], x[blk[0]], (p, q)): blk.append(s); break
                    else: part.append([s])
                rolemap = {al: 'a', mu: 'm', ga: 'A', de: 'B'}
                sig.append((''.join(sorted(rolemap[p] + rolemap[q])), tuple(tuple(b) for b in part)))
            sig = tuple(sorted(sig))
            A.c[('sig', l1, l2, sig)] += 1
            # dichotomies D1: L1 xor x2~x4 in {alpha,B};  D2: L2 xor x0~x3 in {alpha,A}
            j24 = same_comp(H, c, x[2], x[4], (al, de)); j03 = same_comp(H, c, x[0], x[3], (al, ga))
            if l1 == j24: A.bad('D1 dichotomy (L1 xor x2~x4 in aB)', (name, k))
            if l2 == j03: A.bad('D2 dichotomy (L2 xor x0~x3 in aA)', (name, k))
            odd = int(l1) + int(l2) + int(j24) + int(j03)
            A.c['unfilled_odd_%d' % odd] += 1
            # one-swap criterion
            if (H.dF[k] == 1) != (not (l1 and l2)): A.bad('dF=1 <=> not DL', (name, k))
        # F2: every non-web chain: count drop iff all rim cells of one colour and none of the other
        before = len(set(rimc))
        for K in H.chains(c):
            if K['web']: continue
            p, q = K['pair']
            Rp = {x for x in L if c[x] == p}; Rq = {x for x in L if c[x] == q}
            Kp, Kq = K['set'] & Rp, K['set'] & Rq
            d = H.flip(c, K); after = len({d[x] for x in L})
            pred = bool(Rp) and bool(Rq) and ((Kp == Rp and not Kq) or (Kq == Rq and not Kp))
            if (after < before) != bool(pred): A.bad('F2 single-polarity rule', (name, k, p, q))
            if Kp and Kq and after < before: A.bad('two-polarity chain reduced count', (name, k))
            if not H.filled[k]:
                kind = 'both' if (Kp and Kq) else ('one' if (Kp or Kq) else 'quiet')
                t = H.index[H.canon(d)]
                good = H.dF[k] > 0 and H.dF[t] == H.dF[k] - 1
                A.moves[(H.dl[k], kind, 'best' if good else 'other')] += 1
        # DL features
        if not H.filled[k] and H.dl[k]:
            x, al, mu, ga, de = H.frame(c)
            ch = H.chains(c)
            ncomp = len(ch)  # components over all 6 pairs (webs included)
            K1 = H.chain_at(c, x[1], ga); K2 = H.chain_at(c, x[1], de)
            shared_mu = len({u for u in K1 & K2})
            Kpi = H.chain_at(c, x[2], ga)
            dd = H.pi[k] is not None and H.dl[H.pi[k]]
            quiet = sum(1 for K in ch if not K['web'] and not (K['set'] & H.rimset))
            A.rows.append(dict(map=name, k=k, dF=H.dF[k], slack=ncomp - 8, N=ncomp, l1=len(K1), l2=len(K2),
                               shared=shared_mu, kpi=len(Kpi), dd=int(dd), quiet=quiet, n=n,
                               moves=len(H.moves[k])))
    # per-class identities
    for cid, t in tally.items():
        U, F = t['U'], t['F']
        if (U - 3 * F) % 5: A.bad('5 | U-3F', (name, cid, U, F))
        a = t['U_notL2'] == t['F_m3s'] and t['U_notL1'] == t['F_m2s']
        b = t['U_notL2'] == t['F_m2s'] and t['U_notL1'] == t['F_m3s']
        if not (a or b): A.bad('U_notL2 = F_short (per class)', (name, cid, dict(t)))
        A.c['classes'] += 1; A.c['classes_orient_a'] += a; A.c['classes_orient_b'] += b
        A.cls.append(dict(map=name, U=U, F=F, w=(U - 3 * F) / 5,
                          odd_total=2 * U + t['F_m3s'] + t['F_m2s']))
    A.c['holes'] += 1; A.c['states'] += H.S
    print('%-22s n=%2d S=%6d classes=%3d  %.1fs' % (name, n, H.S, len(H.classes), time.time() - t0), flush=True)


def main():
    A = Acc()
    what = sys.argv[1] if len(sys.argv) > 1 else 'maps'
    if what == 'maps':
        for name, rot, h in map_graphs(): analyse(name, rot, h, A)
    else:
        for o in map(int, sys.argv[2:]):
            for name, rot in gentri_graphs(o):
                for h in range(len(rot)):
                    if len(rot[h]) == 5: analyse('%s h%d' % (name, h), rot, h, A)
    out = os.path.join(os.path.dirname(__file__), 'gp_%s.json' % ('_'.join(sys.argv[1:]) or 'maps'))
    json.dump(dict(counts={str(k): v for k, v in A.c.items()}, fails=dict(A.fail), ex={k: str(v) for k, v in A.ex.items()},
                   moves={str(k): v for k, v in A.moves.items()}, rows=A.rows, cls=A.cls), open(out, 'w'))
    print('FAILS', dict(A.fail))
    for k, v in A.ex.items(): print('  ex', k, v)
    sigs = collections.defaultdict(set)
    for k in A.c:
        if isinstance(k, tuple) and k[0] == 'sig': sigs[(k[1], k[2])].add(k[3])
    print('distinct rim signatures per (L1,L2):', {k: len(v) for k, v in sigs.items()})
    print({k: v for k, v in A.c.items() if not isinstance(k, tuple)})
    print('moves', dict(A.moves))
    print('wrote', out)


if __name__ == '__main__':
    main()
