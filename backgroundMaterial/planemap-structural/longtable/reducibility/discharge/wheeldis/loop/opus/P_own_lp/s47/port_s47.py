"""s47 (RELAY_SPEC_s47): separation and upper check for l3qV V = 8, on s47/eng = s44/eng (with the 44.8 repair) + s45/port_l3qV.py.
   python3 port_s47.py ENGINE_DIR   -- patches ENGINE_DIR/prelay2.py and ENGINE_DIR/pcheck.py once; jsep7.cpp is built separately.
Default l3qV=7: every new branch is guarded by `8 in LQVX` (or LQVX), so the code path is s44/eng's.  V = 9 stays refused."""
import sys
E = sys.argv[1]
def patch(fn, reps):
    src = open(fn).read()
    assert 'RELAY_SPEC_s47' not in src, 'already patched ' + fn
    for old, new in reps:
        assert src.count(old) == 1, (fn, old[:80])
        src = src.replace(old, new)
    open(fn, 'w').write(src); print('patched', fn)
P2 = []
# 1. refusal now only for V = 9
P2.append(("""if LQVX and CMD in ('solveR2', 'upperR2'):
    log('l3qV=%s: separation / upper check for V >= 8 not built (RELAY_SPEC_s45 45.5); refusing %s' % (OPT['l3qV'], CMD)); sys.exit(7)
""", """if 9 in LQVX and CMD in ('solveR2', 'upperR2'):   # s47 (RELAY_SPEC_s47): V = 8 built, V = 9 still not
    log('l3qV=%s: separation / upper check for V = 9 not built (RELAY_SPEC_s47 47.6); refusing %s' % (OPT['l3qV'], CMD)); sys.exit(7)
"""))
# 2. write_l3q: the V = 7 payer array reads 3-tuple keys only; then the V = 8 file
P2.append(("""    for (c, a, a2), v in LQV.items(): PQ[(LI[c] * 5 + LI[a]) * 5 + LI[a2]] = v
""", """    for (c, a, a2), v in ((k_, v_) for k_, v_ in LQV.items() if len(k_) == 3): PQ[(LI[c] * 5 + LI[a]) * 5 + LI[a2]] = v   # s47: V = 7 keys only
"""))
P2.append(("""    L3FILE[0] = fn; return fn
def l3q_win(W, U):
""", """    L3FILE[0] = fn
    if 8 in LQVX: write_l3qV(8)   # s47
    return fn
L3VFILE = [None]; LQBROKEN = 'brokensignV' in FLAGS   # s47: brokensignV = control (c) only, the d = 7 payer term at a link 8 mis-signed
def l3q_QeffV(V, c, a, m):
    \"\"\"RELAY_SPEC_s45 45.2 / s47 47.2: Q[(V, c, a, m)] in the extended solution = max(LP value, max q[(V, c, a, a2)] over a2 in m)\"\"\"
    return max([LQQ.get((V, c, a, m), 0.0)] + [LQV.get((V, c, a, a2), 0.0) for a2 in l3q_mask_letters(m)])
def l3q_UBV(V):
    \"\"\"{(c, a): max over the V-table keys with that (c, a) of Qeff}; (c, a) outside {5, 6}^2 -> 0 (as l3q_UB)\"\"\"
    T = l3q_loadV(V); ub = {}
    for k, m in T.items():
        c, a = k[1], k[5]; ub[(c, a)] = max(ub.get((c, a), 0.0), l3q_QeffV(V, c, a, m))
    return ub
def write_l3qV(V):
    \"\"\"s47 47.3: the V = 8 leaf file for jsep7, same layout as write_l3q: QX[2*5^6] (Qeff - UB, <= 0), PQ[125] (payer q, >= 0), MK[2*5^6]\"\"\"
    T = l3q_loadV(V); ub = l3q_UBV(V)
    QX = np.zeros(31250); PQ = np.zeros(125); MK = -np.ones(31250)
    for k, m in T.items():
        sg, c, w2, w3, w4, a, o = k
        i = (((((0 if sg == 1 else 1) * 5 + LI[c]) * 5 + LI[w2]) * 5 + LI[w3]) * 5 + LI[w4]) * 25 + LI[a] * 5 + LI[o]
        QX[i] = l3q_QeffV(V, c, a, m) - ub.get((c, a), 0.0); MK[i] = m
    for k_, v in LQV.items():
        if len(k_) == 4 and k_[0] == V and not LQBROKEN: PQ[(LI[k_[1]] * 5 + LI[k_[2]]) * 5 + LI[k_[3]]] = v
    if QX.max() > 1e-15 or PQ.min() < -1e-15:
        log('  write_l3qV: noise QX.max %.3g PQ.min %.3g (clipped)' % (QX.max(), PQ.min()))
        assert QX.max() <= 1e-9 and PQ.min() >= -1e-9
        QX = np.minimum(QX, 0.0); PQ = np.maximum(PQ, 0.0)
    fn = os.path.join(WORK, 'l3q%d.bin' % V)
    with open(fn, 'wb') as f: f.write(QX.astype(np.float64).tobytes()); f.write(PQ.astype(np.float64).tobytes()); f.write(MK.astype(np.float64).tobytes())
    L3VFILE[0] = fn; return fn
def l3q_winV(W, U):
    \"\"\"s47 47.3: U = 8 window at a link 7 (c = index 2): + UB8 of the payee credit on both sides, read as l3q_win
    (+ side c = e, a = r ; - side c = b, a = q); jsep7's leaf corrects it exactly.  The d = 7 payer term at a link 8 is <= 0
    and is applied in the leaf only (as V = 7).  brokensignV (control): U = 7 window at a link 8 (c = index 3) gets
    + max_a2 q[(8, c, a, a2)] per side (c = e, a = f ; c = b, a = a), the payer term with the wrong sign, and the leaf drops it.\"\"\"
    if 8 not in LQVX: return
    if U == 8:
        ub = l3q_UBV(8)
        for b, e, q, r in itertools.product(range(5), repeat=4):
            W[:, b, 2, e, :, :, q, r, :] += ub.get((LET[e], LET[r]), 0.0) + ub.get((LET[b], LET[q]), 0.0)
    if U == 7 and LQBROKEN:
        mx = collections.defaultdict(float)
        for k_, v in LQV.items():
            if len(k_) == 4 and k_[0] == 8: mx[(k_[1], k_[2])] = max(mx[(k_[1], k_[2])], v)
        for a, b, e, f in itertools.product(range(5), repeat=4):
            W[a, b, 3, e, f, :, :, :, :] += mx.get((LET[e], LET[f]), 0.0) + mx.get((LET[b], LET[a]), 0.0)
def l3q_win(W, U):
"""))
# 3. window
P2.append(("""    l3q_win(W, U)
    fb_win(W, U)
""", """    l3q_win(W, U)
    l3q_winV(W, U)   # s47
    fb_win(W, U)
"""))
# 4. upperR2: the solution's l3q keys must be of a family that is on
P2.append(("""    if any(v < 0 or v > LQCAP + 1e-9 for v in LQV.values()) or any(v < 0 for v in LQQ.values()): log('lq VALUE OUTSIDE [0, lqcap]'); return
""", """    if any(v < 0 or v > LQCAP + 1e-9 for v in LQV.values()) or any(v < 0 for v in LQQ.values()): log('lq VALUE OUTSIDE [0, lqcap]'); return
    _bk = [k for k in LQV if len(k) != 3 and not (len(k) == 4 and k[0] in LQVX and k[1] in (5, 6) and k[2] in (5, 6) and k[3] in LET)]
    _bk += [k for k in LQQ if len(k) != 3 and not (len(k) == 4 and k[0] in LQVX and k[1] in (5, 6) and k[2] in (5, 6) and 0 <= k[3] < 32)]
    if _bk: log('SOLUTION HAS lq / lQ KEYS OF A FAMILY THAT IS OFF OR MALFORMED (l3qV=%s): %s' % (','.join(map(str, LQVS)), _bk[:5])); return   # s47
    if LQVX: log('l3qV: %d V >= 8 q > 0 (total %.9f), %d V >= 8 Q > 0%s' % (sum(1 for k in LQV if len(k) == 4), sum(v for k, v in LQV.items() if len(k) == 4), sum(1 for k in LQQ if len(k) == 4), ' (BROKEN-SIGN CONTROL)' if LQBROKEN else ''))
"""))
PC = []
PC.append(("""BIN6 = os.path.join(HERE, 'bin', 'jsep6')
""", """BIN6 = os.path.join(HERE, 'bin', 'jsep6')
BIN7 = os.path.join(HERE, 'bin', 'jsep7')   # s47 (RELAY_SPEC_s47): jsep6 + argv[9] = l3qV = 8 leaf file
"""))
PC.append(("""        extra = [NTH, SYMF, CLSFILE[0] if mode == 2 else 'none', (BONUSF[0] or 'none') if d == 7 else 'none', (L3FILE[0] or 'none') if d == 7 else 'none', ZTF[min(d, 9)]]
        out = subprocess.run([BIN6, hdr, wp] + extra, capture_output=True, text=True, check=True).stdout.split('\\n')
        return [l.split() for l in out if l], time.time() - t0, len(inst)
""", """        extra = [NTH, SYMF, CLSFILE[0] if mode == 2 else 'none', (BONUSF[0] or 'none') if d == 7 else 'none', (L3FILE[0] or 'none') if d == 7 else 'none', ZTF[min(d, 9)]]
        v7 = bool(LQVX and L3VFILE[0] and d in (7, 8))   # s47
        out = subprocess.run([BIN7 if v7 else BIN6, hdr, wp] + extra + ([L3VFILE[0]] if v7 else []), capture_output=True, text=True, check=True).stdout.split('\\n')
        return [l.split() for l in out if l], time.time() - t0, len(inst)
    if LQVX and L3VFILE[0] and d in (7, 8):   # s47 (RELAY_SPEC_s47 47.3): jsep7, V = 7 file at d = 7, V = 8 file at d = 7 (payer) and d = 8 (payee)
        extra = [NTH, SYMF, CLSFILE[0] if mode == 2 else 'none', (BONUSF[0] or 'none') if d == 7 else 'none', (L3FILE[0] or 'none') if d == 7 else 'none', 'none', L3VFILE[0]]
        out = subprocess.run([BIN7, hdr, wp] + extra, capture_output=True, text=True, check=True).stdout.split('\\n')
        return [l.split() for l in out if l], time.time() - t0, len(inst)
"""))
patch(E + '/prelay2.py', P2)
patch(E + '/pcheck.py', PC)
