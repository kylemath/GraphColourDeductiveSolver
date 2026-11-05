# group near-tight LP rows by (d, canonical link): count, min slack, the apex-word letter sets per position (link in canonical orientation)
import json, sys, collections
R = json.load(open(sys.argv[1])); TH = float(sys.argv[2])
def images(d, lk, sv):
    for r in range(d):
        for refl in (False, True):
            W_ = [None] * d; S_ = [None] * d
            for i in range(d):
                j = (i + r) % d if not refl else (r - i) % d; W_[j] = lk[i]
                j = (i + r) % d if not refl else (r - i - 1) % d; S_[j] = sv[i]
            yield ''.join(W_), ''.join(S_)
def clink(lk):
    d = len(lk); return min(w for w, s in images(d, lk, '5' * d))
G = collections.defaultdict(list)
for sl, d, lk, sv, n, mot, g, tch in R:
    if sl >= TH: continue
    G[(d, clink(lk))].append((sl, lk, sv, n, mot))
out = []
for (d, cl), L in G.items():
    svs = set()
    for sl, lk, sv, n, mot in L:
        best = min(s for w, s in images(d, lk, sv) if w == cl); svs.add(best)
    pos = [''.join(sorted({s[i] for s in svs})) for i in range(d)]
    mask = ''.join(p if len(p) == 1 else '.' if len(p) == 5 else '[' + p + ']' for p in pos)
    out.append((len(L), min(x[0] for x in L), d, cl, mask, collections.Counter(x[4] for x in L).most_common(1)[0][0]))
out.sort(key=lambda x: (-x[0], x[1]))
print('# groups of LP rows with slack < %g by (d, canonical link): rows, min slack, d, link, apex-letter sets (union, canonical orientation), motif' % TH)
for x in out: print('%4d %.2e d=%d %s %s %s' % x)
