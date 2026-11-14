"""Who pays whom: charge volume by (sender degree, receiver degree, template), over all receiver
neighbourhoods d=5..8 (exhaustive, each link word counted once: orbit weight) and d=9..11 (sampled,
scaled to 5^d words). Unknown second-ring degrees uniform on 5..9+."""
import sys, json, random, collections as C
sys.path.insert(0, 'code')
from parts import parse
from behav import W2B, fit_part, to3, canon_words, sample_words
sc, P = parse('data/synth_rules_588.txt')
tmpl = lambda p: {'drule': 'RSST', 'SP_': 'push', 'STm_': 'tunnel', 'STp_': 'tunnel'}[p['pre']]
byhub = C.defaultdict(list)
for k, p in enumerate(P): byhub[p['hub']].append(k)
S3 = [to3(p['slots']) for p in P]
F = C.Counter(); FP = C.Counter(); NPAIR = C.Counter()
for d in range(5, 12):
    if d <= 8:
        words = canon_words(d); scale = 1.0
    else:
        words = sample_words(d, 15000, random.Random(d)); scale = 5 ** d / sum(o for _, o in words)
    dd = min(d, 9)
    for w, orb in words:
        W = W2B(d, w); wt = orb * scale
        for i in range(d):
            L = w[i]
            NPAIR[(min(L, 9), dd)] += wt
            if L > 8: continue
            for k in byhub[L]:
                s = P[k]['slots']
                if not (s[2][0] <= dd <= s[2][1] and s[3][0] <= w[(i - 1) % d] <= s[3][1] and s[1][0] <= w[(i + 1) % d] <= s[1][1]):
                    continue
                pr = fit_part(W, 1 + i, S3[k], L - 2)
                if pr:
                    amt = P[k]['w'] * pr * wt
                    # positive: hub L pays receiver d; negative: receiver pays hub
                    F[(L, dd, tmpl(P[k]), amt > 0)] += abs(amt); FP[k] += abs(amt)
    print('done', d, flush=True)
# average charge (in 1/60) moved per adjacent (a, b) pair, a pays b; (a,b) adjacency counted from b's side
rows = []
for (L, dd, t, pos), v in F.items():
    a, b = (L, dd) if pos else (dd, L)
    rows.append([a, b, t, v / NPAIR[(L, dd)]])
rows.sort(key=lambda r: -r[3])
# rule-level: number of parts and total weight per (hub degree -> target range), tunnels as A -> B
json.dump(dict(avg=rows), open('db/flow.json', 'w'))
for r in rows[:30]: print(r[0], '->', r[1], r[2], round(r[3], 4))
