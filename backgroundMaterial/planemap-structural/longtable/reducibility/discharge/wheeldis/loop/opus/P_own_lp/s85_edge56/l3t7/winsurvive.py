"""s85 (Opus, 6 Nov): full 2-ball private-letter kills at the link 7s of the receiver rows of a dual export.
For each d = 7 receiver row (link w, apexes s, all exact, 9 = 9+ never exact) and each link 7 w_j and side sg, the slot is
w_j's private adjacent to the apex on side sg (s_j for sg = +1, s_{j-1} for sg = -1), i.e. the q7 hidden letter p1 / p2 and
the l3q hidden letter a2.  Known: the centre (7), every link letter and every apex.  Unknown (degree 99, strict 14' rule):
every other private.  A letter is killed when some forbidden configuration embeds using known vertices plus the slot at that
letter (reading (A) of RELAY_SPEC_s21 21.4).  Forbidden set = s16_filter registry() with donly=1 (RSST D2 + the TD/TC names),
minus exname.  usage: python3 f2ball7.py EXDIR TD TC EXNAME DUAL.json OUT.json [all]"""
import sys, json, time, collections
EX, TD, TC, EXN, DUAL, OUTF = sys.argv[1:7]; F7 = sys.argv[8]; ALL = 'all' in sys.argv[7:]
F = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s30t/f/'
sys.argv = [sys.argv[0], EX, TD, TC, 'unused', 'donly=1']
exec(open(F + 's16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
D = 7
C = registry(); n0 = len(C); X = set(l.split()[0] for l in open(EXN) if l.strip() and not l.startswith('#')); C = [cf for cf in C if cf[0] not in X]
print('forbidden', n0, 'after exname', len(C), flush=True)
_B = {}
RW = int(__import__('os').environ.get('RW', '2'))
def kills(w, s, j, sg):
    LK = tuple(w)
    if LK not in _B: _B[LK] = build(D, list(LK))
    P, pa, pf = _B[LK]
    sa = ('s', j) if sg == 1 else ('s', (j - 1) % D)
    slot = [x for x in P if x[0] == 'p' and x[1] == j and sa in pa[x]]; assert len(slot) == 1, (w, j, sg, slot); slot = slot[0]
    fd = {('u',): 7}; UNKV = set()
    KW = {(j + k) % D for k in range(-RW, RW + 1)}; KS = {(j + k) % D for k in range(-RW, RW)}
    for i in range(D):
        if i in KW: fd[('w', i)] = w[i] if w[i] < 9 else NEVER
        if i in KS: fd[('s', i)] = s[i] if s[i] < 9 else NEVER
    for x in P:
        if x == slot or x in fd: continue
        fd[x] = NEVER; UNKV.add(x)
    kill = {}
    for cf in C:
        for e_ in grow.embeddings(cf, P, pa, pf, fd):
            if any(v in UNKV for u, v in e_): continue
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            if slot in req: kill.setdefault(req[slot], cf[0])
    m = 31
    for val in kill: m &= ~(1 << LET.index(val))
    return m, {str(k): v for k, v in kill.items()}
R = json.load(open(DUAL))['rows']; TODO = {(x['link'], x['apex'], x['j'], x['sg']) for x in json.load(open(F7)) if (x['c'] >= 7 or x['ap'] >= 7) and x['mask'] != 31}; out = []; t0 = time.time(); n = 0
for r in R:
    if r['type'] != 'receiver' or r['d'] != 7: continue
    w = [int(ch) for ch in r['link']]; s = [int(ch) for ch in r['apex']]
    for j in range(D):
        if w[j] != 7: continue
        for sg in (1, -1):
            c = w[(j + sg) % D]; ap = s[j] if sg == 1 else s[(j - 1) % D]
            if (r['link'], r['apex'], j, sg) not in TODO: continue
            if not ALL and not ((c == 7 or ap == 7) and c <= 7 and ap <= 7): continue
            m, why = kills(w, s, j, sg); n += 1
            out.append({'w': r['w'], 'link': r['link'], 'apex': r['apex'], 'j': j, 'sg': sg, 'c': c, 'ap': ap, 'mask': m, 'why': why})
            if n % 200 == 0: print('  %d %.0fs' % (n, time.time() - t0), flush=True)
json.dump(out, open(OUTF, 'w')); print('done', n, '%.0fs' % (time.time() - t0))

