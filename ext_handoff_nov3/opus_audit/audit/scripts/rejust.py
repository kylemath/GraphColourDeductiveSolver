"""Independent re-justification of f2b d7_w7/d8_w7 kills on 7-sides (review of f2b7).
Real 2-ball geometry (s16_filter.build with the row's actual link letters), all link letters / apexes exact (9 = never exact),
slot = w_j's private adjacent to s_j (sg=+1) or s_{j-1} (sg=-1), every other private never exact (strict 14').
Registry: s16_filter registry() with donly=0 (RSST D2 + C2cons, 582) + A97 k3x names + nl51 (8200), minus exname.
modes: sides FILE.json part=k/n  |  rules D SG part=k/n
"""
import sys, json, time, collections, os
ROOT = os.environ.get('F2B7_AUDIT_ROOT') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # package root
SC = ROOT + '/tree'  # was '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad'
P = ROOT + '/tree/P_own_lp'  # was '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
EX = SC + '/ex_A97'; TD = P + '/s33z/reg_A97/k3x_D_A97.out'; TC = P + '/s33z/reg_A97/k3x_C_A97.cfast'
EXN = P + '/s77_k6patch/tab/exname_keep95p131f.txt'; NL51 = P + '/s39o/k57/nl51_kc.txt'
args = sys.argv[1:]; mode = args[0]
part = [a for a in args if a.startswith('part=')]; pk, pn = (map(int, part[0][5:].split('/')) if part else (0, 1))
reg = [a for a in args if a.startswith('reg=')]; REG = reg[0][4:] if reg else 'broad'
sys.argv = ['s16', EX, TD, TC, 'unused', 'donly=%d' % (1 if REG == 'donly' else 0)]
exec(open(P + '/s30t/f/s16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
C = registry(); n0 = len(C); have = {c[0] for c in C}
if REG == 'broad':
    for l in open(NL51).read().splitlines():
        f = l.split()
        if len(f) == 5 and f[1].isdigit() and f[2].isdigit() and ';' in f[3] + f[4] and f[0] not in have:
            C.append(grow.kcline(l, 'nl51')); have.add(f[0])
X = set(l.split()[0] for l in open(EXN) if l.strip() and not l.startswith('#'))
C = [cf for cf in C if cf[0] not in X]
print('registry', REG, 'base', n0, 'with nl51', len(have), 'after exname', len(C), flush=True)
_B = {}
def kills(D, w, s, j, sg):
    LK = tuple(w)
    if (D, LK) not in _B: _B[(D, LK)] = build(D, list(LK))
    Pv, pa, pf = _B[(D, LK)]
    sa = ('s', j) if sg == 1 else ('s', (j - 1) % D)
    slot = [x for x in Pv if x[0] == 'p' and x[1] == j and sa in pa[x]]; assert len(slot) == 1, (w, j, sg, slot); slot = slot[0]
    # geometry sanity: slot adjacent to exactly w_j, its apex, and the other private of w_j among named vertices
    nb = pa[slot]; other = [x for x in Pv if x[0] == 'p' and x[1] == j and x != slot]
    assert nb == {('w', j), sa} | set(other), (slot, nb)
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = w[i] if w[i] < 9 else NEVER; fd[('s', i)] = s[i] if s[i] < 9 else NEVER
    for x in Pv:
        if x == slot or x in fd: continue
        fd[x] = NEVER
    kill = {}
    for cf in C:
        for e_ in grow.embeddings(cf, Pv, pa, pf, fd):
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            assert set(req) <= {slot}
            if slot in req: kill.setdefault(req[slot], cf[0])
    m = 31
    for val in kill: m &= ~(1 << LET.index(val))
    return m, kill
out = []; t0 = time.time()
if mode == 'sides':
    S = json.load(open(args[1]))[pk::pn]
    for e in S:
        w = [int(c) for c in e['link']]; s = [int(c) for c in e['apex']]
        m, kl = kills(7, w, s, e['j'], e['sg'])
        ok = (m & ~e['rmask']) == m  # every rule-killed letter is killed here too
        bad = [L for L in LET if not (e['rmask'] >> (L - 5)) & 1 and (m >> (L - 5)) & 1]
        out.append({'link': e['link'], 'apex': e['apex'], 'j': e['j'], 'sg': e['sg'], 'rmask': e['rmask'], 'broad_mask': m,
                    'unjustified_letters': bad, 'why': {str(k): v for k, v in kl.items()}})
    print('sides', len(S), 'unjustified', sum(1 for o in out if o['unjustified_letters']), '%.0fs' % (time.time() - t0))
    json.dump(out, open('rejust_sides_%d_%d.json' % (pk, pn), 'w'))
else:
    D = int(args[1]); SG = args[2]
    R = json.load(open(P + '/s77_k6patch/tab/rules_studio_keep95p131f.json'))['d%d_w7' % D][SG]
    sgi = int(SG); cOff = sgi % D; apOff = 0 if sgi == 1 else D - 1
    live = []
    for r in R:
        wd = {int(k): tuple(al) for k, al in r[1]}; sd = {int(k): int(v) for k, v in r[2]}
        c = wd.get(cOff); ap = sd.get(apOff)
        if (c is None or max(c) >= 7) or (ap is None or ap >= 7): live.append((int(r[0]), wd, sd))
    live = live[pk::pn]; nbad = 0
    for p, wd, sd in live:
        w = [9] * D; s = [9] * D; w[0] = 7
        for k, al in wd.items(): w[k % D] = al[0] if len(al) == 1 else 9
        for k, v in sd.items(): s[k % D] = v
        # choose c >= 7 completion where the rule leaves c open, to test on a genuine 7-side
        m, kl = kills(D, w, s, 0, sgi)
        okk = not (m >> (p - 5)) & 1
        if not okk: nbad += 1
        out.append({'p': p, 'w_req': {str(k): v for k, v in wd.items()}, 's_req': {str(k): v for k, v in sd.items()},
                    'test_link': ''.join(map(str, w)), 'test_apex': ''.join(map(str, s)), 'justified': okk,
                    'witness': kl.get(p)})
    print('D', D, 'sg', SG, 'live rules tested', len(live), 'NOT re-justified', nbad, '%.0fs' % (time.time() - t0))
    json.dump(out, open('rejust_rules_d%d_%s_%d_%d.json' % (D, SG, pk, pn), 'w'))
