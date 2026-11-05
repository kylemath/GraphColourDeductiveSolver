# comparison table: base-cert heavy rows (W7 top 15, b77 all) vs in13 slack / ext-load and shares in the new duals
import json, re, sys
C = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/sC_tight'
def canon_row(d, lk, sv):
    out = []
    for r in range(d):
        for refl in (False, True):
            W_ = [None] * d; S_ = [None] * d
            for i in range(d):
                j = (i + r) % d if not refl else (r - i) % d; W_[j] = lk[i]
                j = (i + r) % d if not refl else (r - i - 1) % d; S_[j] = sv[i]
            out.append((''.join(W_), ''.join(S_)))
    return min(out)
def clink(lk): return canon_row(len(lk), lk, '5' * len(lk))[0]
duals = {'floorOff': 'L_n13s010/cert_n13s010_recv.json', 'floorQ7': 'L_n13s010q/cert_n13s010q_recv.json', 'TRoff1e-4': 'TR_n13off/tr_n13off_d0.0001_recv.json', 'TRq7_2.9e-4': 'TR_n13q/tr_n13q_d0.00029_recv.json'}
D = {}; DL = {}
for k, f in duals.items():
    D[k] = {}; DL[k] = {}
    for sh, d, lk, sv in json.load(open(C + '/' + f)):
        D[k][(d,) + canon_row(d, lk, sv)] = sh; DL[k][(d, clink(lk))] = DL[k].get((d, clink(lk)), 0) + sh
probe = {}
for l in open(C + '/probe_in13.txt'):
    m = re.match(r'^(\S+)\s+(\S+) d=(\d+) (\d+)/(\d+) adm=\S+ slack (\S+) \(without rr/z/zr: (\S+)\) ext-load (\S+)', l)
    if m: probe[m.group(1)] = (float(m.group(2)), int(m.group(3)), m.group(4), m.group(5), float(m.group(6)), float(m.group(8)))
print('| base row | d | link class | W7 | b77 | in13 slack | rr+z+zr load | ' + ' | '.join('%s row (link)' % k for k in duals) + ' |')
print('|' + '---|' * (7 + len(duals)))
seen = set()
for tag in sorted(probe, key=lambda t: (t[:2] != 'b7', int(re.sub(r'\D', '', t[-2:]) or 0) if False else 0)):
    pass
order = [t for t in probe if t.startswith('W7')][:15] + [t for t in probe if t.startswith('b77')]
for tag in order:
    sh, d, lk, sv, sl, ext = probe[tag]; key = (d,) + canon_row(d, lk, sv)
    if key in seen: continue
    seen.add(key)
    w7 = [probe[t][0] for t in probe if t.startswith('W7') and (probe[t][1],) + canon_row(probe[t][1], probe[t][2], probe[t][3]) == key]
    b7 = [probe[t][0] for t in probe if t.startswith('b77') and (probe[t][1],) + canon_row(probe[t][1], probe[t][2], probe[t][3]) == key]
    cells = []
    for k in duals:
        a = D[k].get(key); b = DL[k].get((d, clink(lk)))
        cells.append('%s (%s)' % ('%.2f' % a if a else '-', '%.2f' % b if b else '-'))
    print('| %s/%s | %d | %s | %s | %s | %.4f | %+.4f | %s |' % (lk, sv, d, clink(lk), '%.3f' % w7[0] if w7 else '-', '%.3f' % b7[0] if b7 else '-', sl, ext, ' | '.join(cells)))
