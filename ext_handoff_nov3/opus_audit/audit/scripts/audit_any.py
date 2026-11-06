"""Per-rule strict test of rejust.py `rules` mode, on ANY group of rules_studio_keep95p131f.json (package wrapper).

It runs rejust.py's own preamble unchanged (same registry C = broad minus exname, same build / kills) and then, for each
rule [p, w_req, s_req] of the chosen group, builds the test row exactly as rejust.py `rules` mode does:
  u = exact degree D;  w_0 = 7 (w7 groups) or 6 (w6 groups);
  a link position whose rule entry allows ONE letter gets that letter, every other link position gets 9 (never exact);
  apexes the rule fixes get their value, every other apex 9 (never exact);
  slot = the private of w_0 adjacent to s_0 (SG = 1) or to s_{D-1} (SG = -1); every other private never exact (strict 14').
  justified = some registry configuration kills letter p at the slot; witness = the first such configuration (registry order).
w7 groups: the test is rejust.py's kills() itself, called as rejust.py calls it.
w6 groups: w_0 has degree 6, so it has ONE private, adjacent to both s_0 and s_{D-1}; that private is the slot. rejust.py's
  kills() cannot run there, because its geometry assertion is written for a link-7 vertex with two privates. The test is
  ext.py's strict() instead, copied verbatim below: the same computation as kills() without that assertion, run here on
  rejust.py's registry C. A w6 sanity check asserts the private is unique and adjacent to exactly {w_0, s_0, s_{D-1}}.

usage (cwd = any writable dir; output goes there):
  python3 -I -B audit_any.py GROUP [SG] [part=k/n] [live=1] [reg=donly]
    GROUP  d7_w6 | d8_w6 | d9_w6 | d7_w7 | d8_w7
    SG     1 | -1    (w7 groups only, required there; w6 groups have no side split)
    part   k/n: rules k, k+n, k+2n, ... of the selected list (default 0/1 = all)
    live=1 w7 groups only: keep only rejust.py's live rules (7-sides), so `d7_w7 1 live=1 part=k/4` reproduces
           rejust_rules_d7_1_k_4.json entry by entry. Default: every rule of the group.
    reg    passed to rejust.py's preamble (default broad)
output: anyrule_<GROUP>_<sg1|sg-1|w6>_<k>_<n>[_live].json, one entry per tested rule:
  group, sg, idx (index in the group's rule list), p, w_req, s_req, test_link, test_apex, justified, witness
"""
import sys, os
A_HERE = os.path.dirname(os.path.abspath(__file__))
A_ARGS = sys.argv[1:]
A_GROUPS = ('d7_w6', 'd8_w6', 'd9_w6', 'd7_w7', 'd8_w7')
if not A_ARGS or A_ARGS[0] not in A_GROUPS: sys.exit(__doc__)
A_G = A_ARGS[0]; A_D = int(A_G[1]); A_W0 = int(A_G[4])
A_SG = None
if A_W0 == 7:
    if len(A_ARGS) < 2 or A_ARGS[1] not in ('1', '-1'): sys.exit('w7 groups need SG = 1 or -1')
    A_SG = A_ARGS[1]
A_PART = [a for a in A_ARGS if a.startswith('part=')]
A_PK, A_PN = (map(int, A_PART[0][5:].split('/')) if A_PART else (0, 1))
A_LIVE = 'live=1' in A_ARGS
if A_LIVE and A_W0 != 7: sys.exit('live=1 is rejust.py\'s 7-side filter, defined only for w7 groups')
A_REG = [a for a in A_ARGS if a.startswith('reg=')]

# ---- rejust.py preamble, unchanged (everything before its mode dispatch): registry C, build, kills, LET, NEVER, grow
A_SRC = open(os.path.join(A_HERE, 'rejust.py')).read()
A_CUT = 'out = []; t0 = time.time()'
assert A_SRC.count(A_CUT) == 1
sys.argv = [os.path.join(A_HERE, 'rejust.py'), 'rules'] + A_REG
exec(A_SRC.split(A_CUT)[0])

def strict(D, w, s, j, sgi, CC):          # verbatim from ext.py lines 10-23
    Pv, pa, pf = build(D, list(w))
    sa = ('s', j) if sgi == 1 else ('s', (j - 1) % D)
    slot = [x for x in Pv if x[0] == 'p' and x[1] == j and sa in pa[x]][0]
    fd = {('u',): D}
    for i in range(D): fd[('w', i)] = w[i] if w[i] < 9 else NEVER; fd[('s', i)] = s[i] if s[i] < 9 else NEVER
    for x in Pv:
        if x != slot and x not in fd: fd[x] = NEVER
    res = {}
    for cf in CC:
        for e_ in grow.embeddings(cf, Pv, pa, pf, fd):
            req = dict((v, cf[3][u]) for u, v in e_ if v not in fd)
            if slot in req: res.setdefault(req[slot], cf[0])
    return res

A_RF = json.load(open(P + '/s77_k6patch/tab/rules_studio_keep95p131f.json'))
A_R = A_RF[A_G][A_SG] if A_W0 == 7 else A_RF[A_G]
A_SGI = int(A_SG) if A_W0 == 7 else 1          # w6: slot found via s_0; it is also adjacent to s_{D-1} (asserted)
A_COFF = A_SGI % A_D; A_APOFF = 0 if A_SGI == 1 else A_D - 1   # rejust.py's live filter offsets
A_SEL = []
for A_I, A_r in enumerate(A_R):
    A_wd = {int(k): tuple(al) for k, al in A_r[1]}; A_sd = {int(k): int(v) for k, v in A_r[2]}
    if A_LIVE:
        A_c = A_wd.get(A_COFF); A_ap = A_sd.get(A_APOFF)
        if not ((A_c is None or max(A_c) >= 7) or (A_ap is None or A_ap >= 7)): continue
    A_SEL.append((A_I, int(A_r[0]), A_wd, A_sd))
A_N_ALL = len(A_SEL)
A_SEL = A_SEL[A_PK::A_PN]
print('group', A_G, 'sg', A_SG, 'rules in group', len(A_R), 'selected', A_N_ALL, 'this part', len(A_SEL), flush=True)

A_OUT = []; A_NBAD = 0; A_T0 = time.time(); A_TS = []
for A_I, A_p, A_wd, A_sd in A_SEL:
    A_t = time.time()
    w = [9] * A_D; s = [9] * A_D; w[0] = A_W0
    for k, al in A_wd.items(): w[k % A_D] = al[0] if len(al) == 1 else 9
    for k, v in A_sd.items(): s[k % A_D] = v
    if A_W0 == 7:
        m, kl = kills(A_D, w, s, 0, A_SGI)
    else:
        A_Pv, A_pa, A_pf = build(A_D, list(w))
        A_pr = [x for x in A_Pv if x[0] == 'p' and x[1] == 0]
        assert len(A_pr) == 1 and A_pa[A_pr[0]] == {('w', 0), ('s', 0), ('s', A_D - 1)}, (w, A_pr)
        kl = strict(A_D, w, s, 0, A_SGI, C)
        m = 31
        for val in kl: m &= ~(1 << LET.index(val))
    A_ok = not (m >> (A_p - 5)) & 1
    if not A_ok: A_NBAD += 1
    A_OUT.append({'group': A_G, 'sg': A_SG, 'idx': A_I, 'p': A_p,
                  'w_req': {str(k): v for k, v in A_wd.items()}, 's_req': {str(k): v for k, v in A_sd.items()},
                  'test_link': ''.join(map(str, w)), 'test_apex': ''.join(map(str, s)), 'justified': A_ok,
                  'witness': kl.get(A_p)})
    A_TS.append(time.time() - A_t)
    if len(A_OUT) % 50 == 0:
        print('  %d/%d rules  %.0fs  not justified so far %d' % (len(A_OUT), len(A_SEL), time.time() - A_T0, A_NBAD), flush=True)
A_FN = 'anyrule_%s_%s_%d_%d%s.json' % (A_G, ('sg' + A_SG) if A_SG else 'w6', A_PK, A_PN, '_live' if A_LIVE else '')
json.dump(A_OUT, open(A_FN, 'w'))
print('group', A_G, 'sg', A_SG, 'tested', len(A_OUT), 'NOT justified', A_NBAD, '%.0fs' % (time.time() - A_T0),
      'per rule mean %.2fs max %.2fs' % ((sum(A_TS) / len(A_TS), max(A_TS)) if A_TS else (0, 0)), '->', A_FN)
