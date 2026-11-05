# W5: price 7-to-7 sharing keys against certP2full_rat.json.  Independent of the engine's q7 code: keys built from raw words.
# Data taken from the engine: RBIG (reducible 7-wheels), L3T masks (allowed private letters beside a link 7), f2b extra7.
# Key families (sender = a certificate receiver 7 A, receiver = its link 7 B at position i):
#   K1 : A's link word rooted at B (reflection canonical)                      [= engine q7 family, stage 14 R77]
#   K2 : A's link word + A's apex word rooted at B (A's full 2-ball picture)
# Absorber slot = (cert row B, position j with B.w[j] = 7): may absorb any key whose letters B can see agree; hidden letters
# free inside 'opts' (lenient: any letter; strict: L3T/f2b masks on the two privates, link not RBIG).
import json, itertools, collections, sys
from fractions import Fraction as F
import load_engine as L
MODE = sys.argv[1] if len(sys.argv) > 1 else 'strict'
ns = L.load('help'); ns['l3q_load']()
RBIG = ns['RBIG']; L3T = ns['L3T']; extra7 = ns['f2bm'].extra7
LET = (5, 6, 7, 8, 9)
def canon_cyc(w):
    w = tuple(w); n = len(w); return min(min(s[k:] + s[:k] for k in range(n)) for s in (w, w[::-1]))
def rot(w, i): return tuple(w[(i + k) % len(w)] for k in range(len(w)))
def key1(lw):            # rooted link (L0..L6), reflection keeps L0
    r = (lw[0],) + tuple(reversed(lw[1:])); return min(tuple(lw), r)
def key2(lw, sw):        # rooted link + apex word S[k] = apex between L[k], L[k+1]; reflection: L'[k] = L[-k], S'[k] = S[-k-1]
    n = len(lw); a = (tuple(lw), tuple(sw))
    b = (tuple(lw[(-k) % n] for k in range(n)), tuple(sw[(-k - 1) % n] for k in range(n))); return min(a, b)
C = json.load(open('/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s62_w5check/certs/certP2full_rat.json'))
R = [(r['row'][2], r['row'][3], F(r['w'])) for r in C if r['row'][0] == 'receiverR2']
assert all(w == F(-10, 207) for _, _, w in R) and all(len(l) == 7 for l, _, _ in R)
rows = [([int(c) for c in l], [int(c) for c in s]) for l, s, _ in R]
names = ['%s/%s' % (l, s) for l, s, _ in R]
def mask(w, s, j, sg):
    """allowed letters for the private of link-7 w[j] next to the apex on side sg (engine L3T & ~f2b extra7); None = no table"""
    n = 7; c = w[(j + sg) % n]; ap, o = (s[j], s[(j - 1) % n]) if sg == 1 else (s[(j - 1) % n], s[j])
    if c > 6 or ap > 6: return None
    m = L3T[(sg, c, w[(j + 2 * sg) % n], w[(j + 3 * sg) % n], w[(j + 4 * sg) % n], ap, o)] & ~extra7(7, w, s, j, sg)
    return [l for k, l in enumerate(LET) if (m >> k) & 1]
# ---- emissions: every (row A, position i) with A.w[i] >= 7
EM = []
for a, (w, s) in enumerate(rows):
    for i in range(7):
        if w[i] >= 7:
            lw = rot(w, i); sw = rot(s, i)          # S[k] = s[i+k] = apex between w[i+k], w[i+k+1]
            EM.append((a, i, key1(lw), key2(lw, sw)))
# ---- absorber slots: every (row B, position j) with B.w[j] = 7; options built by explicit completion of hidden letters
def slot_opts(w, s, j, fam):
    n = 7; W = lambda k: w[(j + k) % n]; S = lambda k: s[(j + k) % n]
    Lvis = [7, W(1), S(0), None, None, S(-1), W(-1)]               # sender A = w[j]: link from B; B has degree 7
    if MODE == 'strict':
        m1, m2 = mask(w, s, j, 1), mask(w, s, j, -1)
        P1 = m1 if m1 is not None else LET; P2 = m2 if m2 is not None else LET
    else: P1 = P2 = LET
    out = set()
    for p1 in P1:
        for p2 in P2:
            lw = (7, W(1), S(0), p1, p2, S(-1), W(-1))
            if MODE == 'strict' and ''.join(map(str, canon_cyc(lw))) in RBIG: continue
            if fam == 1: out.add(key1(lw)); continue
            # A's apexes: S0 = apex(B, c+) = W(2); S6 = apex(c-, B) = W(-2); S1 = apex(c+, ap+) = S(1) if c+ = 5; S5 = apex(ap-, c-) = S(-2) if c- = 5
            hid = [k for k in range(1, 6) if not ((k == 1 and W(1) == 5) or (k == 5 and W(-1) == 5))]
            for hv in itertools.product(LET, repeat=len(hid)):
                sw = [W(2), S(1) if W(1) == 5 else None, None, None, None, S(-2) if W(-1) == 5 else None, W(-2)]
                for k, v in zip(hid, hv): sw[k] = v
                out.add(key2(lw, sw))
    return out
SL = []
for b, (w, s) in enumerate(rows):
    for j in range(7):
        if w[j] == 7: SL.append((b, j))
def match(fam):
    opts = {(b, j): slot_opts(rows[b][0], rows[b][1], j, fam) for b, j in SL}
    adj = {e: [sl for sl in SL if EM[e][1 + fam] in opts[sl]] for e in range(len(EM))}
    mt = {}
    def aug(e, seen):
        for sl in adj[e]:
            if sl in seen: continue
            seen.add(sl)
            if sl not in mt or aug(mt[sl], seen): mt[sl] = e; return True
        return False
    for e in range(len(EM)): aug(e, set())
    return opts, adj, mt
if __name__ == '__main__':
    print('MODE', MODE, '| emissions', len(EM), '| slots', len(SL))
    for fam in (1, 2):
        opts, adj, mt = match(fam)
        inv = {e: sl for sl, e in mt.items()}
        print('\n==== K%d family: matched %d of %d emissions' % (fam, len(mt), len(EM)))
        byk = collections.Counter(EM[e][1 + fam] for e in range(len(EM)))
        for e, (a, i, k1, k2) in enumerate(EM):
            k = (k1, k2)[fam - 1]
            cap = sum(1 for sl in SL if k in opts[sl])
            print('  emit %-16s pos %d key %s | compatible slots %d %s | matched to %s' % (names[a], i,
                  ''.join(map(str, k1)) if fam == 1 else (''.join(map(str, k2[0])) + '/' + ''.join(map(str, k2[1]))),
                  cap, [(names[b][:7], j) for b, j in adj[e]], (names[inv[e][0]][:7], inv[e][1]) if e in inv else 'UNABSORBED'))
        un = [e for e in range(len(EM)) if e not in inv]
        print('  K%d: unabsorbed emissions %d -> combined coefficient on their keys +%s each (improving by that per unit)' % (fam, len(un), F(10, 207)))
