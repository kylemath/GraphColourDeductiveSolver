# s44 (cont.): exact cert repair for lowerR2 (RELAY_SPEC_s44.md §44.8).
#   python3 port_repair.py ENGINE_DIR   -- replaces cmd_lowerR2 in ENGINE_DIR/prelay2.py (idempotent check).
# The check itself is unchanged in meaning: rows re-derived from labels, signs enforced, capped families priced at cap,
# any uncapped column with negative reduced cost -> INVALID.  New: (1) a weight given as a string "p/q" is taken exactly
# (no limit_denominator); (2) if the only failure is uncapped columns with |rc| <= reptol (default 1e-9), the free cons2
# weights and the strictly negative mrow* weights are moved by an exact rational solve so those columns get rc = 0, the
# repaired cert is written with exact string weights, and the whole check is rerun from that file with 'norepair'.
import sys, re
E = sys.argv[1]; p = E + '/prelay2.py'; src = open(p).read()
if 'def lr2_xsolve' in src: print('already patched'); sys.exit(0)
m = re.search(r'\ndef cmd_lowerR2\(\):\n.*?\n(?=def all6_words)', src, re.S)
NEW = r'''
def lr2_xsolve(eqs):
    """exact sparse Gaussian elimination: eqs = [(dict var->Fraction, rhs)]; free variables 0; None if inconsistent"""
    piv = []
    for e0, r in eqs:
        e = dict(e0)
        for v, pe, pr in piv:
            f = e.pop(v, None)
            if f:
                for u, a in pe.items():
                    if u != v:
                        x = e.get(u, 0) - f * a
                        if x: e[u] = x
                        else: e.pop(u, None)
                r -= f * pr
        if not e:
            if r != 0: return None
            continue
        v = max(e, key=lambda u: (abs(e[u]), -hash(u) % 7))
        a = e[v]; pe = {u: b / a for u, b in e.items()}; piv.append((v, pe, r / a))
    x = {}
    for v, pe, pr in reversed(piv):
        x[v] = pr - sum(a * x.get(u, 0) for u, a in pe.items() if u != v)
    return x
def cmd_lowerR2():
    """exact check from signed duals (as lowerR): senderR2 >= (w>=0), cons2 = (any sign), mrowR2 h - M <= 0 (w<=0),
    receiverR2 <= (w<=0); rows re-derived from labels; rescale so t's reduced cost is 0; x priced at its cap.
    s44: string weights are exact; tiny float noise on uncapped columns is repaired exactly (see port_repair.py)."""
    load_patterns()
    xon = 'xon' in FLAGS; XCAP = Fraction(OPT.get('xcap', '3')); C = json.load(open(OPT['cert']))
    SR = {(wd, tuple(map(str, b))): cf for wd, cf, b in R2_sender_rows()}
    ok = True; cnt = collections.Counter(); RW = []   # RW: (cert index, kind, w, unit coefficients, t coefficient, D coefficient)
    for ci, c in enumerate(C):
        w = Fraction(c['w']) if isinstance(c['w'], str) else Fraction(c['w']).limit_denominator(int(float(OPT.get('wden', '1e7'))))   # s33: wden=; s44: "p/q" exact
        row = c['row']; cnt[row[0]] += 1; cf = None; tc = 0; dc = 0
        if row[0] == 'senderR2':
            cf = SR.get((row[1], tuple(map(str, row[2]))))
            if cf is None: log('  NOT A SENDER ROW', row); ok = False; continue
            if w < 0: log('  WRONG SIGN', row); ok = False; continue
            tc = 1; dc = 1
        elif row[0] == 'cons2':
            L = tuple(row[1]); s = tuple(row[2])
            if isR6(L) or len(L) != 6 or len(s) != 6 or any(v not in LET for v in L + s): log('  BAD CONS2', row); ok = False; continue
            cf = cons2_coef(L, s)
        elif row[0] == 'mrowR2':
            sg = tuple(row[1]); k = tuple(row[2])
            g0 = sg[:-1] if F16 else sg
            if F16 and not (0 <= sg[-1] < 32): log('  BAD MASK', row); ok = False; continue
            if len(g0) != (7 if AP else 5) or g0 != sig2_of(*(g0 if AP else g0 + (5, 5))): log('  NONCANON SIG', row); ok = False; continue
            if k not in sig2_keys(sg): log('  BAD MROW', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            cf = {('h', k): 1, ('M', sg): -1}
        elif row[0] == 'mrowV':
            sg = tuple(row[1]); k = tuple(row[2])
            g0 = sg[:7]
            if g0 != sigv_of(*g0) or len(sg) != (8 if F16 else 7) or k not in sigv_keys(sg): log('  BAD MROWV', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            cf = {('V', sg): 1, ('v', k): -1}
        elif row[0] == 'mrowQ':
            sg = tuple(row[1]); k = tuple(row[2])
            if sg != q7sig(*sg) or k not in q7keys(sg): log('  BAD MROWQ', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            cf = {('q', k): 1, ('Q', sg): -1}
        elif row[0] == 'mrowZ':
            K = tuple(row[1])
            if not L6R or K not in set(z6_first()): log('  BAD MROWZ', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            cf = {('z6', K): 1, ('Z6', zsig6_of_key(K)): -1}
        elif row[0] == 'mrowL':
            sg = tuple(row[1]); k = tuple(row[2])
            if not L3Q or len(sg) != 3 or sg[0] > 6 or sg[1] > 6 or k[:2] != sg[:2] or k[2] not in l3q_mask_letters(sg[2]): log('  BAD MROWL', row); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            cf = {('lq', k): 1, ('lQ', sg): -1}
        elif row[0] == 'receiverR2':
            d, lk, sv = int(row[1]), row[2], row[3]
            why = admissible(d, lk, sv)
            if why: log('  RECEIVER NOT ADMISSIBLE', row, why); ok = False; continue
            if w > 0: log('  WRONG SIGN', row); ok = False; continue
            tau = None
            if FY2:   # s43: the cell must be one of the row's cells
                cm = dict(fy2_cells(d, [int(ch) for ch in lk], [int(ch) for ch in sv]))
                if len(row) != 5 or row[4] not in cm: log('  BAD CELL', row); ok = False; continue
                tau = cm[row[4]]
            cf = recv_coef_R2(d, lk, sv, xon, tau); tc = -1; dc = d - 6
        else: log('  UNKNOWN', row); ok = False; continue
        RW.append((ci, row[0], w, cf, tc, dc))
    UCAP = Fraction(OPT['ucap']) if 'ucap' in OPT else None
    def capof(k):   # the cap a family is priced at, None if uncapped
        if k[0] == 'x': return XCAP
        if k[0] == 'D': return Fraction(OPT.get('dcap', '3'))   # stage 24: D is capped like x (RELAY_SPEC 19.5)
        if k[0] == 'fb' and FBCAP is not None: return Fraction(OPT['fbcap'])   # s44: fb priced at its cap when capped
        if k[0] == 'lq': return Fraction(OPT.get('lqcap', '3'))   # stage 28
        if ZR and k[0] in ('z', 'zr', 'rr'): return Fraction(OPT.get('zcap', '3'))   # stage 33
        if k[0] == 'z6': return Fraction(OPT.get('z6cap', '3'))   # RELAY_SPEC_s23.5
        return UCAP   # s33 ucap=: every other column priced at UCAP (only if the LP family had that cap)
    def evaluate(ws):
        tot = collections.defaultdict(Fraction); tco = Fraction(0); D = Fraction(0)
        for (ci, kd, w0, cf, tc, dc), w in zip(RW, ws):
            for k, v in cf.items(): tot[k] += w * v
            tco += w * tc; D += w * dc
        return tot, tco, D
    WS = [r[2] for r in RW]
    tot, tco, D = evaluate(WS)
    if tco <= 0: log('  t coefficient sum not positive'); ok = False; tco = Fraction(1)
    def price(tot, tco, D):
        D = D / tco; neg = []; nu = 0; du = Fraction(0)
        for k, v in tot.items():
            rc = -v / tco
            if rc < 0:
                cp = capof(k)
                if cp is not None:
                    D += rc * cp
                    if UCAP is not None and cp is UCAP: nu += 1; du += rc * UCAP
                else: neg.append((k, rc))
        if UCAP is not None: log('  ucap=%s: %d uncapped columns priced at cap, total %.3g' % (UCAP, nu, float(du)))
        return D, neg
    Dp, neg = price(tot, tco, D)
    if neg: log('  negative reduced costs:', len(neg), sorted(neg, key=lambda kv: kv[1])[:5])
    log('rows by type: %s' % dict(cnt))
    rep = ok and neg and 'norepair' not in FLAGS
    log('LOWER-R2%s: %s  t >= %s = %.9f  (%d rows)' % (' (unrepaired)' if rep else '', 'VALID' if ok and not neg else 'INVALID', Dp, float(Dp), len(C)))
    if not rep: return
    # s44 repair: only uncapped columns with tiny negative rc; only free (cons2) and strictly negative mrow* weights move.
    TOL = Fraction(OPT.get('reptol', '1e-9')); RMAX = Fraction(OPT.get('repmax', '1e-6'))
    worst = min(rc for _, rc in neg)
    if worst < -TOL: log('REPAIR: refused (worst rc %.3g beyond reptol %s)' % (float(worst), OPT.get('reptol', '1e-9'))); log('LOWER-R2: INVALID  t >= %s = %.9f  (%d rows)' % (Dp, float(Dp), len(C))); return
    adj = [j for j, r in enumerate(RW) if r[1] == 'cons2' or (r[1].startswith('mrow') and r[2] < 0)]
    colrows = collections.defaultdict(dict)
    for j in adj:
        for k, v in RW[j][3].items():
            if v: colrows[k][j] = Fraction(v)
    tot0 = tot; E = {}; ws = None
    for rnd in range(30):
        for k, _ in neg: E[k] = True
        eqs = [(colrows.get(k, {}), -tot0[k]) for k in E]
        x = lr2_xsolve(eqs)
        if x is None: log('REPAIR: round %d: no exact solution on %d columns' % (rnd, len(E))); break
        big = max([abs(v) for v in x.values()] or [0])
        if big > RMAX: log('REPAIR: round %d: largest weight move %.3g beyond repmax' % (rnd, float(big))); x = None; break
        ws = list(WS)
        for j, v in x.items(): ws[j] += v
        if any(RW[j][1].startswith('mrow') and ws[j] > 0 for j in x): log('REPAIR: round %d: an mrow weight would change sign' % rnd); x = None; break
        tot, tco, D = evaluate(ws); Dr, neg = price(tot, tco, D)
        log('REPAIR: round %d: %d columns pinned to rc 0, %d weights moved (max %.3g); %d negative columns left' % (rnd, len(E), len(x), float(big), len(neg)))
        if not neg: break
        if min(rc for _, rc in neg) < -TOL: x = None; log('REPAIR: round %d: a moved column went beyond reptol' % rnd); break
    if x is None or neg: log('LOWER-R2: INVALID  t >= %s = %.9f  (%d rows; repair failed)' % (Dp, float(Dp), len(C))); return
    C2 = json.loads(json.dumps(C))
    for (ci, kd, w0, cf, tc, dc), w in zip(RW, ws): C2[ci]['w'] = str(w)
    out = re.sub(r'\.json$', '', OPT['cert']) + '_rep.json'; json.dump(C2, open(out, 'w'))
    log('REPAIR: exact cert written to %s; rechecking it from the file (norepair)' % out)
    OPT['cert'] = out; FLAGS.add('norepair'); cmd_lowerR2()
'''
src = src[:m.start()] + NEW + src[m.end():]
open(p, 'w').write(src); print('patched', p)
