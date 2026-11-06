"""s85 (Opus, 6 Nov): +-2-window private-letter exclusions at a link 7 (the q7 hidden letter p next to the side's apex), d = 7 centre.
Side sg = +1 at link position 0: w_0 = 7, c = w_1, ap = s_0, slot = w_0's private adjacent to s_0.  Window known letters:
w_{-2} = w_5, w_{-1} = w_6, w_1, w_2 (fixed per combo, 9 = 9+ never exact); apexes s_5, s_6, s_0, s_1 FREE (their required exact
letters are read off each embedding); centre 7.  Unknown (degree 99, strict 14' rule, no match may touch them): w_3, w_4, the
other apexes and every other private.  Reading (A): a letter X of the slot is killed under apex letters A when some forbidden
configuration embeds using known vertices, the slot at X and free apexes at exactly the letters A (each <= 8: 9 = 9+ is never exact).
Side -1 is the mirror image.  Forbidden set = s16_filter registry() donly=1 (RSST D2 + TD/TC names) minus exname.
Output: {'w5 w6 w1 w2': [[slotletter, {apex: letter}] ...]} (apex keys s5 s6 s0 s1).
usage: python3 f2b7win.py EXDIR TD TC EXNAME OUT.json [sg=1|-1] [part=k/n]   (sg = -1: slot = w_0's private adjacent to s_6 = s_{-1}, computed directly, not by mirror)"""
import sys, json, time, itertools
EX, TD, TC, EXN, OUTF = sys.argv[1:6]; XO = dict(a.split('=', 1) for a in sys.argv[6:])
F = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s30t/f/'
sys.argv = [sys.argv[0], EX, TD, TC, 'unused', 'donly=1']
exec(open(F + 's16_filter.py').read().replace("if __name__ == '__main__':", "if False:"))
D = 7; SG = int(XO.get('sg', '1'))
C = registry(); n0 = len(C); X = set(l.split()[0] for l in open(EXN) if l.strip() and not l.startswith('#')); C = [cf for cf in C if cf[0] not in X]
print('forbidden', n0, 'after exname', len(C), flush=True)
APX = {('s', 5): 's5', ('s', 6): 's6', ('s', 0): 's0', ('s', 1): 's1'}
def rules(w5, w6, w1, w2):
    LK = [7, w1, w2, 9, 9, w5, w6]
    P, pa, pf = build(D, LK)
    SA = ('s', 0) if SG == 1 else ('s', D - 1)
    slot = [x for x in P if x[0] == 'p' and x[1] == 0 and SA in pa[x]]; assert len(slot) == 1; slot = slot[0]
    fd = {('u',): 7, ('w', 0): 7}; UNKV = set()
    for i, l in ((1, w1), (2, w2), (5, w5), (6, w6)): fd[('w', i)] = l if l < 9 else NEVER
    for x in P:
        if x == slot or x in fd or x in APX: continue
        fd[x] = NEVER; UNKV.add(x)
    out = set()
    for cf in C:
        for e_ in grow.embeddings(cf, P, pa, pf, fd):
            if any(v in UNKV for u, v in e_): continue
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            if slot not in req: continue
            if any(l > 8 for l in req.values()): continue
            out.add((req[slot], tuple(sorted((APX[v], l) for v, l in req.items() if v != slot)), cf[0]))
    # keep, per (slot letter, apex requirement), one witness name; drop requirements implied by a weaker one
    best = {}
    for x, ar, nm in sorted(out):
        best.setdefault((x, ar), nm)
    keys = list(best)
    keep = [k for k in keys if not any(k2 != k and k2[0] == k[0] and set(k2[1]) <= set(k[1]) for k2 in keys)]
    return [[x, dict(ar), best[(x, ar)]] for x, ar in sorted(keep)]
combos = list(itertools.product(LET, repeat=4))
if 'part' in XO: k, n = map(int, XO['part'].split('/')); combos = combos[k::n]
res = {}; t0 = time.time()
for i, (w5, w6, w1, w2) in enumerate(combos):
    res['%d %d %d %d' % (w5, w6, w1, w2)] = rules(w5, w6, w1, w2)
    if (i + 1) % 25 == 0: print('  %d/%d %.0fs' % (i + 1, len(combos), time.time() - t0), flush=True)
json.dump(res, open(OUTF, 'w')); print('done', len(combos), '%.0fs' % (time.time() - t0), 'rules', sum(len(v) for v in res.values()))
