"""s80: negative controls for mkrules.py's soundness check: every verified rule is perturbed (killed letter changed; one
requirement dropped; side flipped for L') and must then FAIL the check (the check is not vacuous)."""
import sys, json, collections
src = open(sys.argv[1]).read().split('groups = {k')[0]
sys.argv = [sys.argv[1]] + sys.argv[2:5] + []
G0 = {'__name__': 'neg'}; exec(src, G0)
cnt = collections.Counter(); ex = []
for l in open(sys.argv[3] + '/rules_AL.tsv'):
    if l.startswith('#'): continue
    f = l.rstrip('\n').split('\t')
    if 'VERIFIED' not in f[7]: continue
    kc = None
    for cf in sys.argv[4:]: pass
    rk, wn, qn, dd, grp, orient, rs = f[0], f[1], f[2], int(f[3]), f[4], f[5], json.loads(f[6])
    kcs = [x for x in KC if x.split()[0] == wn]; kc = kcs[0]
    par = 6 if 'w6' in grp else 7; sg = 0 if par == 6 else int(grp.split('[')[1].rstrip(']'))
    p, wr, sr = rs[0], {o: v for o, v in rs[1]}, {o: v for o, v in rs[2]}
    ok, _, _ = G0['verify'](kc, dd, par, sg, 6 if p == 5 else 5, wr, sr); cnt['letter changed: ' + ('passes (BAD)' if ok else 'fails')] += 1
    for o in list(wr):
        w2 = dict(wr); del w2[o]; ok, _, _ = G0['verify'](kc, dd, par, sg, p, w2, sr); cnt['w req dropped: ' + ('passes' if ok else 'fails')] += 1
        if ok: ex.append((wn, dd, orient, 'w', o))
    for o in list(sr):
        s2 = dict(sr); del s2[o]; ok, _, _ = G0['verify'](kc, dd, par, sg, p, wr, s2); cnt['s req dropped: ' + ('passes' if ok else 'fails')] += 1
        if ok: ex.append((wn, dd, orient, 's', o))
    if sg: ok, _, _ = G0['verify'](kc, dd, par, -sg, p, wr, sr); cnt['side flipped: ' + ('passes' if ok else 'fails')] += 1
print(dict(cnt)); print('drops that still pass (requirement not needed by the embedding):', ex)
