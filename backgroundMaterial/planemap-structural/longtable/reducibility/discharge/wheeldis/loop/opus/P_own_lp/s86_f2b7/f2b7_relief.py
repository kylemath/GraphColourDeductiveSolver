# f2b7_relief.py (Opus s86, 6 Nov): how much of the d = 7 q7 payee weight of a dual export f2b7 touches, under explicit definitions.
# usage: python3 f2b7_relief.py ENG DUAL RULES TAB+1,TAB-1
# For every d = 7 receiver row r (weight w_r) and every link 7 at j (one Q payee term), sig = q7sig before f2b7, sig' after f2b7
# (sides with c or apex >= 7: 31 -> 31 & ~extra7).  W(sig, k) = the dual's mrowQ weight on (sig, key k).  K'(sig') = q7keys(sig') (letters
# only; RBIG keys carry no mrowQ row, so they never enter).  Dropped keys D = {k : W(sig, k) != 0, k not in K'}.
#   A (key-weight share, the SPEC figure):  sum_(r,j) w_r * W(sig, D) / W(sig, all)  /  sum_(r,j) w_r
#   B (term share, any weighted key dropped): sum_(r,j) with D nonempty of w_r  /  sum_(r,j) w_r
#   C (term share, mask changed at all):     sum_(r,j) with sig' != sig of w_r  /  sum_(r,j) w_r
#   S (mrowQ weight on dropped keys):        sum over sigs of W(sig, k) for keys dropped in at least one term of sig / total mrowQ weight
import json, sys, collections, importlib.util, os
ENG, DUAL, RULES = sys.argv[1:4]; TABS = sys.argv[4].split(',')
sp = importlib.util.spec_from_file_location('f2bmod', os.path.join(ENG, 'f2b.py')); f2b = importlib.util.module_from_spec(sp); sp.loader.exec_module(f2b)
f2b.load(RULES)
L3T = {}
for fn in TABS:
    for k, v in json.load(open(fn)).items():
        sg, wd, ao = k.split(); L3T[(int(sg),) + tuple(int(ch) for ch in wd) + tuple(int(ch) for ch in ao)] = v[0]
LET = [5, 6, 7, 8, 9]
def lets(m): return [l for k, l in enumerate(LET) if (m >> k) & 1]
def q7sig(U, a, b, c, e, m1, m2):
    x = (U, a, b, c, e)
    if m1 == 31 and m2 == 31: return min(x, (U, e, c, b, a))
    return min(x + (m1, m2), (U, e, c, b, a, m2, m1))
def qkey(t): return min(t, (t[0],) + tuple(reversed(t[1:])))
def keys(sig):
    U, a, b, c, e = sig[:5]; m1, m2 = (sig[5], sig[6]) if len(sig) == 7 else (31, 31)
    return {qkey((U, a, b, p1, p2, c, e)) for p1 in lets(m1) for p2 in lets(m2)}
J = json.load(open(DUAL)); R = J['rows']
W = collections.defaultdict(dict)
for r in R:
    if r['type'] == 'mrowQ': W[tuple(r['sig'])][tuple(r['key'])] = r['w']
tot = A = B = C = 0.0; nt = nA = 0; dropped = collections.defaultdict(set); bysig = collections.defaultdict(float)
for r in R:
    if r['type'] != 'receiver' or r['d'] != 7: continue
    d = 7; U = 7; w = [int(ch) for ch in r['link']]; s = [int(ch) for ch in r['apex']]; wr = r['w']
    for j in range(d):
        if w[j] != 7: continue
        old, new = [], []
        for sgn in (1, -1):
            c = w[(j + sgn) % d]; ap_, o = (s[j], s[(j - 1) % d]) if sgn == 1 else (s[(j - 1) % d], s[j])
            if c <= 6 and ap_ <= 6:
                m = L3T[(sgn, c, w[(j + 2 * sgn) % d], w[(j + 3 * sgn) % d], w[(j + 4 * sgn) % d], ap_, o)] & ~f2b.extra7(d, w, s, j, sgn)
                old.append(m); new.append(m)
            else:
                old.append(31); new.append(31 & ~f2b.extra7(d, w, s, j, sgn))
        a, b, cc, e = w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d]
        sg0 = q7sig(U, a, b, cc, e, old[0], old[1]); sg1 = q7sig(U, a, b, cc, e, new[0], new[1])
        Wk = W.get(sg0, {}); K1 = keys(sg1)
        Dk = [k for k, v in Wk.items() if v != 0 and k not in K1]
        tot += wr; nt += 1
        Wall = sum(Wk.values())
        if Wall != 0: A += wr * sum(Wk[k] for k in Dk) / Wall
        if Dk: B += wr; nA += 1; dropped[sg0].update(Dk); bysig[sg0] += wr * sum(Wk[k] for k in Dk) / Wall
        if sg1 != sg0: C += wr
Wtot = sum(v for ks in W.values() for v in ks.values()); Sd = sum(W[sg][k] for sg, ks in dropped.items() for k in ks)
print('d = 7 Q payee terms: %d, payee weight %.6f' % (nt, tot))
print('A key-weight share  %.4f  (%.6f)' % (A / tot, A))
print('B any weighted key  %.4f  (%.6f, %d terms)' % (B / tot, B, nA))
print('C mask changed      %.4f  (%.6f)' % (C / tot, C))
print('S mrowQ weight on keys dropped somewhere: %.6f of %.6f = %.4f' % (Sd, Wtot, Sd / Wtot))
print('top signatures by A contribution:', ', '.join('%s%s %.4f' % (''.join(map(str, sg[:5])), '' if len(sg) == 5 else '/%d,%d' % sg[5:], v) for sg, v in sorted(bysig.items(), key=lambda kv: kv[1])[:6]))
