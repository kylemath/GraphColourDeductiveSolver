# f2b041 job 2 (Studio): per-violator cause of the keep-only failure. For each violator of keep (all D + 531 Lean C): full vs keep
# admissibility (replay), then per position the source of every mask difference: w6 -> pmask (kill table) and/or full2ball rules;
# w7 at d = 7 -> V7 mask and/or rules; w7 at d = 8 -> V8 mask and/or rules (tables recomputed here from the two configs' files).
import os, sys, json, collections, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); F = os.path.dirname(H); W = os.path.abspath(os.path.join(F, '..', '..', '..', '..'))
src = open(os.path.join(W, 'out', 'job31', 'st21_check_f2b.py')).read(); a = src.index("F2BR = os.environ.get('F2B')"); b = src.index('# ================= 12.5: receiverR2 rows')
def matcher(path):
    os.environ['F2B'] = path; G = {'os': os, 'json': json, 'LET': (5, 6, 7, 8, 9), 'V6': False, 'FB': False, 'XO': False, 'fail': sys.exit, 'print': lambda *x, **k: None}
    exec(src[a:b], G); return G['f2b_extra']
exF = matcher(os.path.join(F, 'in', 'gc', 'kill_upgraded', 'tierA', 'full2ball_extra_rules.json')); exK = matcher(os.path.join(H, 'rules_studio_keep.json'))
def kt(d): return {7: np.load(d + '/kill_U7.npy'), 9: np.load(d + '/kill_U9.npy')}
KF = kt(os.path.join(W, 'out', 'job31', 'f2bA', 'kill')); KK = kt(os.path.join(H, 'tab', 'kill')); KF[8] = KF[9]; KK[8] = KK[9]
def pm(KT, U, *x): K = KT[U][tuple(v - 5 for v in x)]; return sum(1 << b for b in range(5) if not K[b])
def mtab(p):
    M = {}
    for sg, fn in ((1, p % '+1'), (-1, p % '-1')):
        for r in json.load(open(fn)): M[(sg,) + tuple(r[:6])] = r[6]
    return M
M7F = mtab(os.path.join(W, 'out', 'job31', 'f2bA', 'studio_l3qtab_%s.json')); M7K = mtab(os.path.join(H, 'tab', 'studio_l3qtab_%s.json'))
M8F = mtab(os.path.join(W, 'out', 'job31', 'f2bA', 'V8', 'studio_l3qtabV8_%s.json')); M8K = mtab(os.path.join(H, 'tab', 'V8', 'studio_l3qtabV8_%s.json'))
hits = {}
for fn in ('viol_k7a_d7.txt', 'viol_k8a_d8.txt'):
    for l in open(os.path.join(H, 'run', fn)):
        t = l.split(); hits[(int(t[0]), t[2], t[3])] = t[4:] if t[4] != '-' else []
full = {tuple(j[:3]): j for j in map(json.loads, open(os.path.join(H, 'run', 'replay_full.jsonl')))}
keep = {tuple(j[:3]): j for j in map(json.loads, open(os.path.join(H, 'run', 'replay_keep.jsonl')))}
cls = collections.Counter(); pos = collections.Counter(); ex = {}
for k, jk in keep.items():
    d, lk, sv = k; jf = full[k]; w = [int(c) for c in lk]; s = [int(c) for c in sv]; U = min(d, 9); W_ = lambda i: w[i % d]; S_ = lambda i: s[i % d]
    if not jf[3]:
        c = 'full-inadmissible: dropped receiver C pattern' if hits.get(k) else 'full-inadmissible: C wheel / RBIG (CKEEP)'
        cls[(d, c)] += 1; ex.setdefault((d, c), k); continue
    causes = set()
    for i in range(d):
        if w[i] == 6:
            pf = pm(KF, U, W_(i - 2), W_(i - 1), W_(i + 1), W_(i + 2), S_(i - 2), S_(i - 1), S_(i), S_(i + 1)); pk = pm(KK, U, W_(i - 2), W_(i - 1), W_(i + 1), W_(i + 2), S_(i - 2), S_(i - 1), S_(i), S_(i + 1))
            ef = exF(d, w, s, i, ('w6', d)) if d <= 9 else 0; ek = exK(d, w, s, i, ('w6', d)) if d <= 9 else 0
            mf, mk = pf & ~ef, pk & ~ek
            if mk & ~mf:   # a letter allowed in keep but killed in full (keep-only extra kills are harmless and not counted)
                lost = mk & ~mf; c_ = []
                if lost & ~pf & pk: c_.append('kill table (w6, U%d)' % U)
                if lost & pf & ef & ~ek: c_.append('rule d%d_w6' % d)
                if lost & ~pf & pk & ef & ~ek: pass
                causes.update(c_ or ['w6 other']); pos.update(c_ or ['w6 other'])
        if w[i] == 7 and d in (7, 8):
            for sg in (1, -1):
                c_, a_, o_ = W_(i + sg), (S_(i) if sg == 1 else S_(i - 1)), (S_(i - 1) if sg == 1 else S_(i))
                if c_ not in (5, 6) or a_ not in (5, 6): continue
                key = (sg, c_, a_, W_(i + 2 * sg), W_(i + 3 * sg), W_(i + 4 * sg), o_)
                tf, tk = (M7F, M7K) if d == 7 else (M8F, M8K)
                ef = exF(d, w, s, i, ('w7', d, sg)); ek = exK(d, w, s, i, ('w7', d, sg)); mf, mk = tf[key] & ~ef, tk[key] & ~ek
                if mk & ~mf:
                    lost = mk & ~mf; c__ = []
                    if lost & ~tf[key] & tk[key]: c__.append('V%d mask side %+d' % (d, sg))
                    if lost & tf[key] & ef & ~ek: c__.append('rule d%d_w7 side %+d' % (d, sg))
                    causes.update(c__ or ['w7 other']); pos.update(c__ or ['w7 other'])
    c = 'admissible in both: ' + (' + '.join(sorted(causes)) if causes else 'NO mask difference (row value differs otherwise)')
    cls[(d, c)] += 1; ex.setdefault((d, c), k)
print('violators %d (d7 %d, d8 %d)' % (len(keep), sum(1 for k in keep if k[0] == 7), sum(1 for k in keep if k[0] == 8)))
for (d, c), n in sorted(cls.items()): print('  d=%d %6d  %s   e.g. %s %s' % (d, n, c, ex[(d, c)][1], ex[(d, c)][2]))
print('position-level causes (count of positions/sides):'); [print('  %6d %s' % (n, c)) for c, n in pos.most_common()]
