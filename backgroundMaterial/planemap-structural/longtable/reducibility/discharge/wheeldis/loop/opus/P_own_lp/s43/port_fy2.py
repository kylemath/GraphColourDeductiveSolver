# s43: port fy cluster level 2 (flag fy2, RELAY_SPEC_s43) into a copy of s40f/eng.  Run once:  python3 port_fy2.py s43/eng
import sys, os
E = sys.argv[1]
def patch(fn, reps):
    p = os.path.join(E, fn); s = open(p).read()
    for old, new in reps:
        assert s.count(old) == 1, (fn, old); s = s.replace(old, new)
    open(p, 'w').write(s); print('patched', p)
P2 = []
P2.append(("ZH = 'zh' in FLAGS or FY ",
           "FY2 = 'fy2' in FLAGS                 # s43 (RELAY_SPEC_s43): fy cluster level 2, h2 = c2(face apex private t) unmasked at faces\n"
           "ZH = 'zh' in FLAGS or FY "))
P2.append(("assert not FY or ('hat5' in FLAGS and not ZR and 'zh' not in FLAGS), 'fy port: needs hat5, excludes zh/zr'\n",
           "assert not FY or ('hat5' in FLAGS and not ZR and 'zh' not in FLAGS), 'fy port: needs hat5, excludes zh/zr'\n"
           "assert not FY2 or FY, 'fy2 needs fy'\n"))
P2.append(("def fy_vis(n): return (True, n[1] == 5, False, n[4] == 5, True)\n",
           "def fy_vis(n): return (True, n[1] == 5, FY2 and ((n[1] == 5 and n[2] == 5) or (n[4] == 5 and n[3] == 5)), n[4] == 5, True)   # s43: level 2 at faces\n"))
P2.append(("def fy_recv_key(U, a, b, e, f, p, q, r, s_):\n"
           "    n = (U, e, r, q, b)\n"
           "    return fykey(n, (c2(f), c2(s_) if e == 5 else FYMASK, FYMASK, c2(p) if b == 5 else FYMASK, c2(a)))\n",
           "def fy_recv_key(U, a, b, e, f, p, q, r, s_, tau=None):\n"
           "    n = (U, e, r, q, b)\n"
           "    if fy_vis(n)[2]: assert tau in (0, 1), 'fy2: a face five needs its cell class'\n"
           "    return fykey(n, (c2(f), c2(s_) if e == 5 else FYMASK, tau if tau is not None else FYMASK, c2(p) if b == 5 else FYMASK, c2(a)))\n"
           "def fy2_allowed(sn, sp):   # s43 43.1: classes of t leaving the apex five's link (5, 5, sn, t, sp) non-R5; empty -> both\n"
           "    A = tuple(c for c in (0, 1) if any(not isR5((5, 5, sn, x, sp)) for x in CLS2[c])); return A or (0, 1)\n"
           "def fy2_cells(d, w, s):\n"
           "    \"\"\"faces i (w_i = w_{i+1} = s_i = 5) and the cells [(label, {face: class})] of a receiver row (s43 43.3)\"\"\"\n"
           "    if not FY2: return [('', {})]\n"
           "    F = [i for i in range(d) if w[i] == 5 and w[(i + 1) % d] == 5 and s[i] == 5]\n"
           "    for i in F: assert (i + 1) % d not in F, 'fy2: five in two faces (its link (U,5,5,5,5) is R5: row not admissible)'\n"
           "    As = [fy2_allowed(s[(i + 1) % d], s[(i - 1) % d]) for i in F]\n"
           "    return [(','.join('%d:%d' % (i, c) for i, c in zip(F, cb)), dict(zip(F, cb))) for cb in itertools.product(*As)]\n"
           "ZTF = {}\n"))
# window: UB at vis2 fives + the face file for jsep6
P2.append(("            W[a, b, 0, e, f, p_, q, r, s_] += ZV.get(fy_recv_key(U, LET[a], LET[b], LET[e], LET[f], LET[p_], LET[q], LET[r], LET[s_]), 0.0)\n",
           "            if FY2 and fy_vis(wd)[2]:   # s43: UB over the face's allowed classes here; exact coupling in jsep6's leaf (ZT)\n"
           "                A_ = fy2_allowed(LET[s_], LET[q]) if (e == 0 and r == 0) else fy2_allowed(LET[r], LET[p_])\n"
           "                zz = [ZV.get(fy_recv_key(U, LET[a], LET[b], LET[e], LET[f], LET[p_], LET[q], LET[r], LET[s_], tc), 0.0) if tc in A_ else None for tc in (0, 1)]\n"
           "                ix = (((((((a * 5 + b) * 5 + 0) * 5 + e) * 5 + f) * 5 + p_) * 5 + q) * 5 + r) * 5 + s_\n"
           "                for tc in (0, 1):\n"
           "                    if zz[tc] is not None: ZT[2 * ix + tc] = zz[tc]\n"
           "                W[a, b, 0, e, f, p_, q, r, s_] += max(v_ for v_ in zz if v_ is not None); continue\n"
           "            W[a, b, 0, e, f, p_, q, r, s_] += ZV.get(fy_recv_key(U, LET[a], LET[b], LET[e], LET[f], LET[p_], LET[q], LET[r], LET[s_]), 0.0)\n"
           "        if FY2:\n"
           "            ZTF[U] = os.path.join(WORK, 'fy2zt_U%d.bin' % U); ZT.astype(np.float64).tofile(ZTF[U])\n"))
P2.append(("    W = window_table(U, y, x)\n    if FY:\n        for a, b, e, f, p_, q, r, s_ in itertools.product(range(5), repeat=8):\n",
           "    W = window_table(U, y, x)\n    if FY:\n        ZT = np.full(2 * 5 ** 9, -1e300) if FY2 else None\n        for a, b, e, f, p_, q, r, s_ in itertools.product(range(5), repeat=8):\n"))
# receiver coefficients per cell
P2.append(("def recv_coef_R2(d, lk, sv, xon):\n    cy, cx = recv_coef(d, lk, sv, xon); cf = collections.Counter()\n",
           "def recv_coef_R2(d, lk, sv, xon, tau=None):\n    cy, cx = recv_coef(d, lk, sv, xon); cf = collections.Counter()\n"
           "    if FY2 and tau is None: tau = fy2_cells(d, [int(ch) for ch in lk], [int(ch) for ch in sv])[0][1]   # s43: reporting callers get the first cell\n"))
P2.append(("            zk_ = fy_recv_key(U, w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d]) if FY else",
           "            fc_ = j if (w[(j + 1) % d] == 5 and s[j] == 5) else (j - 1) % d if (w[(j - 1) % d] == 5 and s[(j - 1) % d] == 5) else None\n"
           "            zk_ = fy_recv_key(U, w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d], tau[fc_] if (FY2 and fc_ is not None) else None) if FY else"))
# solveR2: one row per cell, label carries the cell
P2.append(("    def recv(d, lk, sv):\n        cf = recv_coef_R2(d, lk, sv, xon)\n        key = (d, tuple(sorted(cf.items(), key=str)))\n        if key in have: return False\n        have.add(key)\n",
           "    def recv(d, lk, sv):\n        if FY2:   # s43: every cell of the row\n"
           "            got = False\n"
           "            for cl, tau in fy2_cells(d, [int(ch) for ch in lk], [int(ch) for ch in sv]): got = recv1(d, lk, sv, cl, tau) or got\n"
           "            return got\n"
           "        return recv1(d, lk, sv, None, None)\n"
           "    def recv1(d, lk, sv, cl, tau):\n        cf = recv_coef_R2(d, lk, sv, xon, tau)\n        key = (d, tuple(sorted(cf.items(), key=str)))\n        if key in have: return False\n        have.add(key)\n"))
P2.append(("        addrow(c2_, -inf, d - 6.0, ('receiverR2', d, lk, sv)); return True\n",
           "        addrow(c2_, -inf, d - 6.0, ('receiverR2', d, lk, sv) + ((cl,) if FY2 else ())); return True\n"))
P2.append(("'zh': ZH, 'fy': FY, 'apexcls': AC,", "'zh': ZH, 'fy': FY, 'fy2': FY2, 'apexcls': AC,"))
# lowerR2: cell label
P2.append(("            if w > 0: log('  WRONG SIGN', row); ok = False; continue\n            for k, v in recv_coef_R2(d, lk, sv, xon).items(): tot[k] += w * v\n",
           "            if w > 0: log('  WRONG SIGN', row); ok = False; continue\n"
           "            tau = None\n"
           "            if FY2:   # s43: the cell must be one of the row's cells\n"
           "                cm = dict(fy2_cells(d, [int(ch) for ch in lk], [int(ch) for ch in sv]))\n"
           "                if len(row) != 5 or row[4] not in cm: log('  BAD CELL', row); ok = False; continue\n"
           "                tau = cm[row[4]]\n"
           "            for k, v in recv_coef_R2(d, lk, sv, xon, tau).items(): tot[k] += w * v\n"))
# upperR2: flag consistency
P2.append(("    if Sj.get('z') and not ZH: log('SOLUTION HAS z BUT zh FLAG OFF'); return\n    ZRV.clear()",
           "    if Sj.get('z') and not ZH: log('SOLUTION HAS z BUT zh FLAG OFF'); return\n"
           "    if bool(Sj.get('fy2', False)) != FY2: log('fy2 FLAG DIFFERS FROM THE SOLUTION (level-1 and level-2 z keys differ in h2)'); return\n"
           "    ZRV.clear()"))
patch('prelay2.py', P2)
PC = []
PC.append(("BIN4 = os.path.join(HERE, 'bin', 'jsep4'); BONUSF = [None]; BIN5 = os.path.join(HERE, 'bin', 'jsep5')\n",
           "BIN4 = os.path.join(HERE, 'bin', 'jsep4'); BONUSF = [None]; BIN5 = os.path.join(HERE, 'bin', 'jsep5'); BIN6 = os.path.join(HERE, 'bin', 'jsep6')\n"))
PC.append(("    if L3FILE[0] and d == 7:   # stage 28",
           "    if 'fy2' in FLAGS:   # s43: jsep6 at every d (l3q at d = 7 only, fy2 face coupling at the leaf)\n"
           "        extra = [NTH, SYMF, CLSFILE[0] if mode == 2 else 'none', (BONUSF[0] or 'none') if d == 7 else 'none', (L3FILE[0] or 'none') if d == 7 else 'none', ZTF[min(d, 9)]]\n"
           "        out = subprocess.run([BIN6, hdr, wp] + extra, capture_output=True, text=True, check=True).stdout.split('\\n')\n"
           "        return [l.split() for l in out if l], time.time() - t0, len(inst)\n"
           "    if L3FILE[0] and d == 7:   # stage 28"))
patch('pcheck.py', PC)
