# p1r_gk67.py (s86 p1r): exec'd by eng_p1r/pcheck_dbg.py (ROWDBG=p1r_gk67.py); replaces lowerR2 by path checks of keys with a
# multi-letter payer or payee set.  For every loaded key K whose payer set (or payee set) has several letters, the single-letter split
# keys K_u = EDGE(u->V)[X] (resp. EDGE(U->v)[X]) are built in memory, and on every path the engine has
#   receiver pictures d = 7, 8, 9 (gk_counts pay / get), sender pictures (R2_sender_rows' (w, H, Fn) labels), cons2 pictures (all6 links x
#   {5,7}^6 class words), the gkwin window tables gk_tables(k, U) (U = 7, 8, 9, both chiralities)
# the counts of K must equal the sum over its split keys (a slot has one payer and one payee letter).  p1_r (d = 7, 8): max IN of K
# must lie between the largest split max and the sum of the split maxes.  The leaf files gkedge_d7.bin (7802) and gkin_d7.bin (7804)
# are written and K's records decoded and compared with the key (payee mask / payer mask and conditions).
def cmd_lowerR2():
    import random as _r
    load_patterns(); l3q_load(); kt_load(); rng = _r.Random(int(OPT.get('seed', '1'))); bad = 0
    multi = [k for k, key in enumerate(GKEYS) if bin(int(key['um'])).count('1') > 1 or bin(int(key['vm'])).count('1') > 1]
    log('GK67: %d keys with a multi-letter payer or payee set: %s' % (len(multi), [(GKNAMES[k], GKEYS[k]['spec']) for k in multi]))
    def split(key):
        if bin(int(key['um'])).count('1') > 1: return [dict(key, um=np.uint8(1 << b)) for b in range(5) if (int(key['um']) >> b) & 1]
        return [dict(key, vm=np.uint8(1 << b)) for b in range(5) if (int(key['vm']) >> b) & 1]
    def arr(keys): return (np.array([int(k['um']) for k in keys], dtype=np.uint8), np.array([int(k['vm']) for k in keys], dtype=np.uint8), np.stack([k['m'] for k in keys]).astype(np.uint8))
    def counts(c, W, A, PV, keys):
        global _GK_UM, _GK_VM, _GK_M
        sv_ = (_GK_UM, _GK_VM, _GK_M); _GK_UM, _GK_VM, _GK_M = arr(keys)
        try: return gk_counts(c, W, A, PV)
        finally: _GK_UM, _GK_VM, _GK_M = sv_
    st = collections.Counter()
    for k in multi:
        key = GKEYS[k]; parts = split(key); allk = [key] + parts
        def chk(kind, c, W, A, PV):
            nonlocal bad
            pay, get = counts(c, W, A, PV, allk)
            if (int(pay[0]), int(get[0])) != (int(pay[1:].sum()), int(get[1:].sum())):
                bad += 1
                if bad <= 5: log('  GK67 %s %s c=%d W=%s: pay %d get %d, split sums %d %d' % (GKNAMES[k], kind, c, W, pay[0], get[0], pay[1:].sum(), get[1:].sum()))
            st[(GKNAMES[k], kind, 'nonzero')] += int(pay[0] != 0 or get[0] != 0); st[(GKNAMES[k], kind)] += 1
        for d in (7, 8, 9):
            n_ = 0
            while n_ < int(OPT.get('N', '3000')):
                w = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]; s = [rng.choice((5, 6, 7, 8, 9)) for _ in range(d)]
                if n_ % 2: w = [rng.choice((5, 6, 7)) for _ in range(d)]; s = [rng.choice((5, 6, 7)) for _ in range(d)]
                lk = ''.join(map(str, w)); sv = ''.join(map(str, s))
                if admissible(d, lk, sv) is not None: continue
                n_ += 1; A, PV = gk_recv_picture(d, w, s); chk('receiver d=%d' % d, d, w, A, PV)
                if d in (7, 8):
                    r = p1r_core(d, w, s, *arr(allk))
                    if not r['empty']:
                        mx = int(r['inmax'][0]); parts_ = [int(v) for v in r['inmax'][1:]]
                        if not (max(parts_) <= mx <= sum(parts_)):
                            bad += 1; log('  GK67 p1r %s %s/%s: max IN %d, split maxes %s' % (GKNAMES[k], lk, sv, mx, parts_))
                        st[(GKNAMES[k], 'p1r d=%d' % d, 'sum strictly above')] += mx < sum(parts_)
        for wd, cf, bits in R2_sender_rows():
            b = list(bits); i = b.index('|'); H = {q: int(x) for q, x in enumerate(b[:i])}; w5 = [int(ch) for ch in wd]
            Fn = dict(zip([q for q in range(5) if w5[q] == 6], [int(x) for x in b[i + 1:]]))
            A = [31 if H.get(q) is None else (28 if H[q] else 3) for q in range(5)]
            PV = [None if x == 5 else ((lambda m: (m, m))(31 if Fn.get(q) is None else (28 if Fn[q] else 3)) if x == 6 else (31, 31)) for q, x in enumerate(w5)]
            chk('sender', 5, w5, A, PV)
        for L in all6_words():
            for s_ in itertools.product((5, 7), repeat=6):
                A, PV = gk_cons2_picture(tuple(L), s_); chk('cons2', 6, list(L), A, PV)
        for U in (7, 8, 9):   # window tables: build the split keys' tables through the same code (temporarily appended to GKEYS)
            T0 = gk_tables(k, U)
            n0 = len(GKEYS); GKEYS.extend(parts)
            try: Tp = [gk_tables(n0 + q, U) for q in range(len(parts))]
            finally:
                del GKEYS[n0:]
                for q in range(len(parts)): _GKTAB.pop((n0 + q, U), None)
            Tp = [t_ for t_ in Tp if t_ is not None]
            if T0 is None: ok = not Tp
            else: ok = all(np.array_equal(T0[c_].astype(np.int32), sum(t_[c_].astype(np.int32) for t_ in Tp)) for c_ in (0, 1)) if Tp else False
            bad += not ok; log('  GK67 %s window tables U=%d: %s (%s split tables)' % (GKNAMES[k], U, 'equal to the split sum' if ok else 'MISMATCH', len(Tp)))
    # leaf files
    KSV.clear(); KSV.update({nm_: 0.01 for nm_ in GKNAMES})
    fe = gk_write(); fi = gkin_write()
    def rd7802(fn):
        b_ = open(fn, 'rb').read(); o = 0; mg, nk = np.frombuffer(b_, '<i4', 2, o); o += 8; out = []
        for _ in range(nk):
            a_ = float(np.frombuffer(b_, '<f8', 1, o)[0]); o += 8; vm, nc = np.frombuffer(b_, '<i4', 2, o); o += 8
            cd = np.frombuffer(b_, '<i4', 3 * nc, o).reshape(-1, 3).tolist(); o += 12 * nc; out.append((a_, int(vm), cd))
        return int(mg), out
    def rd7804(fn):
        b_ = open(fn, 'rb').read(); o = 0; mg, nk = np.frombuffer(b_, '<i4', 2, o); o += 8; out = []
        for _ in range(nk):
            a_ = float(np.frombuffer(b_, '<f8', 1, o)[0]); o += 8; um, nc = np.frombuffer(b_, '<i4', 2, o); o += 8
            cd = np.frombuffer(b_, '<i4', 2 * nc, o).reshape(-1, 2).tolist(); o += 8 * nc; out.append((a_, int(um), cd))
        return int(mg), out
    mg, E = rd7802(fe); ks7 = [k for k, key in enumerate(GKEYS) if key['um'] & 4]
    mg2, I = rd7804(fi); ksi = [k for k in range(len(GKEYS)) if gk_tables(k, 7) is not None]
    log('GK67 leaf files: 7802 magic %d, %d keys (payer-7 keys %d); 7804 magic %d, %d keys (payee-7 keys %d)' % (mg, len(E), len(ks7), mg2, len(I), len(ksi)))
    bad += (mg != 7802) + (len(E) != len(ks7)) + (mg2 != 7804) + (len(I) != len(ksi))
    for k in multi:
        key = GKEYS[k]; cl = [(p_, int(key['m'][i])) for i, p_ in enumerate(GK_POS) if key['m'][i] != 31]
        if k in ks7:
            a_, vm, cd = E[ks7.index(k)]; ok = vm == int(key['vm']) and cd == [list(_GK_KIND[p_]) + [m_] for p_, m_ in cl]
            bad += not ok; log('  GK67 %s 7802 record: payee mask %d (key %d), %d conditions %s' % (GKNAMES[k], vm, key['vm'], len(cd), 'ok' if ok else 'MISMATCH'))
        if k in ksi:
            a_, um, cd = I[ksi.index(k)]; ok = um == (int(key['um']) & 7) and cd == [[i, int(key['m'][i])] for i in range(10) if key['m'][i] != 31]
            bad += not ok; log('  GK67 %s 7804 record: payer mask %d (key %d), %d conditions %s' % (GKNAMES[k], um, key['um'], len(cd), 'ok' if ok else 'MISMATCH'))
    for k_, v_ in sorted(st.items(), key=str): log('  GK67 coverage %s: %d' % (k_, v_))
    log('GK67: %s (%d failures)' % ('PASS' if bad == 0 else 'FAIL', bad))
