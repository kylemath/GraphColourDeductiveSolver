# s44: port fb (RELAY_SPEC_s44) into a copy of s43/eng.  Run once:  python3 port_fb.py s44/eng
import sys, os
E = sys.argv[1]
def patch(fn, reps):
    p = os.path.join(E, fn); s = open(p).read()
    for old, new in reps:
        assert s.count(old) == 1, (fn, old); s = s.replace(old, new)
    open(p, 'w').write(s); print('patched', p)
R = []
R.append(("def z6_terms(L, s):\n",
"FB = 'fb' in FLAGS                   # s44 (RELAY_SPEC_s44): face big u -> its k-vertex X (6: via cons2; big: via receiver), exact key\n"
"FBDIR = OPT.get('fbdir', '67'); FBV = {}; FBCAP = float(OPT['fbcap']) if 'fbcap' in OPT else None\n"
"def fb_face(T): return T[0] == 5 and T[2] == 5 and T[3] == 5\n"
"def fb_key(U, X, Tp, Tm):\n"
"    \"\"\"44.2: sigma = (U, X, min(T+, T-), max(T+, T-)); None unless a face side, X >= 6 and the direction is on\"\"\"\n"
"    if X < 6 or not (fb_face(Tp) or fb_face(Tm)): return None\n"
"    if ('6' if X == 6 else '7') not in FBDIR: return None\n"
"    a, b = min(Tp, Tm), max(Tp, Tm); return (U, X) + a + b\n"
"def fb_payer_keys(d, w, s):   # centre pays its link vertex X = w_j: T+ = (w_{j+1}, s_j, w_{j+2}, e+), T- mirrored\n"
"    out = []; U = min(d, 9)\n"
"    if not FB: return out\n"
"    for j in range(d):\n"
"        if w[j] < 6: continue\n"
"        e1, e2 = w[(j + 1) % d], w[(j - 1) % d]\n"
"        Tp = (e1, s[j], w[(j + 2) % d], s[(j + 1) % d] if e1 == 5 else 0); Tm = (e2, s[(j - 1) % d], w[(j - 2) % d], s[(j - 2) % d] if e2 == 5 else 0)\n"
"        k = fb_key(U, w[j], Tp, Tm)\n"
"        if k: out.append((j, k))\n"
"    return out\n"
"def fb_payee_keys(n, L, t, X):   # centre X (letter X) receives from its link vertex u = L_k >= 7: T+ = (L_{k+1}, L_{k+2}, t_k, e+)\n"
"    out = []\n"
"    if not FB or X < 6: return out\n"
"    for k in range(n):\n"
"        kk = fb_payee_at(n, L, t, X, k)\n"
"        if kk: out.append((k, kk))\n"
"    return out\n"
"def fb_payee_at(n, L, t, X, k):\n"
"    if not FB or X < 6 or L[k] < 7: return None\n"
"    e1, e2 = L[(k + 1) % n], L[(k - 1) % n]\n"
"    Tp = (e1, L[(k + 2) % n], t[k], t[(k + 1) % n] if e1 == 5 else 0); Tm = (e2, L[(k - 2) % n], t[(k - 1) % n], t[(k - 2) % n] if e2 == 5 else 0)\n"
"    return fb_key(L[k], X, Tp, Tm)\n"
"def fb_win(W, U):\n"
"    \"\"\"44.3 window terms: payer at c >= 6 (slots T+ = (e, r, f, s*), T- = (b, q, a, p*)); payee if U >= 7 at c >= 7 (T+ = (e, f, r, s*), T- = (b, a, q, p*))\"\"\"\n"
"    if not FB or not any(v for v in FBV.values()): return\n"
"    seen = set()\n"
"    for side in (0, 1):\n"
"        for t6 in itertools.product(range(5), repeat=6):\n"
"            for c in range(1, 5):\n"
"                for role in ('pay', 'get'):\n"
"                    if role == 'get' and (U < 7 or c < 2): continue\n"
"                    # place a face on the chosen side for this role, the 6 free slots fill the rest\n"
"                    if role == 'pay':   # + face: e = f = s = 0 ; - face: b = a = p = 0\n"
"                        if side == 0: e, f, s_ = 0, 0, 0; a, b, p, q, r, _x = t6\n"
"                        else: b, a, p = 0, 0, 0; e, f, s_, q, r, _x = t6\n"
"                    else:                # + face: e = r = s = 0 ; - face: b = q = p = 0\n"
"                        if side == 0: e, r, s_ = 0, 0, 0; a, b, p, q, f, _x = t6\n"
"                        else: b, q, p = 0, 0, 0; e, r, s_, a, f, _x = t6\n"
"                    if _x: continue\n"
"                    ix = (role, a, b, c, e, f, p, q, r, s_)\n"
"                    if ix in seen: continue\n"
"                    seen.add(ix)\n"
"                    A_, B_, C_, E_, F_, P_, Q_, R_, S_ = (LET[v] for v in (a, b, c, e, f, p, q, r, s_))\n"
"                    if role == 'pay': k = fb_key(U, C_, (E_, R_, F_, S_ if E_ == 5 else 0), (B_, Q_, A_, P_ if B_ == 5 else 0)); sg = -1\n"
"                    else: k = fb_key(C_, U, (E_, F_, R_, S_ if E_ == 5 else 0), (B_, A_, Q_, P_ if B_ == 5 else 0)); sg = 1\n"
"                    if k and FBV.get(k): W[a, b, c, e, f, p, q, r, s_] += sg * FBV[k]\n"
"def z6_terms(L, s):\n"))
R.append(("    if L6R: cf.update(z6_terms(L, s))\n",
          "    if L6R: cf.update(z6_terms(L, s))\n"
          "    for _, k in fb_payee_keys(6, L, s, 6): cf[('fb', k)] += 1   # s44: the 6 is an fb payee (inflow)\n"))
R.append(("    if L3Q: cf.update(l3q_terms(d, w, s))\n",
          "    if L3Q: cf.update(l3q_terms(d, w, s))\n"
          "    if FB:   # s44: the centre pays its face k-vertices; a big centre also receives from its face-big neighbours\n"
          "        for _, k in fb_payer_keys(d, w, s): cf[('fb', k)] -= 1\n"
          "        for _, k in fb_payee_keys(d, w, s, min(d, 9)) if min(d, 9) >= 7 else []: cf[('fb', k)] += 1\n"))
R.append(("    l3q_win(W, U)\n", "    l3q_win(W, U)\n    fb_win(W, U)\n"))
R.append(("LQCAP if key[0] == 'lq' else", "LQCAP if key[0] == 'lq' else (FBCAP if FBCAP is not None else inf) if key[0] == 'fb' else"))
R.append(("            if key[0] == 'lq' and XPEN[0]: h.changeColCost(cols[key], XPEN[0])",
          "            if key[0] == 'fb' and XPEN[0]: h.changeColCost(cols[key], XPEN[0])   # s44: fb carries the x penalty (keeppen)\n"
          "            if key[0] == 'lq' and XPEN[0]: h.changeColCost(cols[key], XPEN[0])"))
R.append(("if k[0] in ('x', 'D', 'lq', 'z6') or", "if k[0] in ('x', 'D', 'lq', 'z6', 'fb') or"))
R.append(("        LQV.clear(); LQV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'lq'})\n",
          "        LQV.clear(); LQV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'lq'})\n"
          "        FBV.clear(); FBV.update({k[1]: xv[i] for k, i in cols.items() if k[0] == 'fb'})\n"))
R.append(("'l6r': L6R,\n", "'l6r': L6R,\n         'fb': [[list(k[1]), float(xv[i])] for k, i in cols.items() if k[0] == 'fb' and xv[i] > 0], 'fbflag': FB,\n"))
R.append(("            elif k[0] == 'lq': D += rc * Fraction(OPT.get('lqcap', '3'))",
          "            elif k[0] == 'fb' and FBCAP is not None: D += rc * Fraction(OPT['fbcap'])   # s44: fb priced at its cap when capped\n"
          "            elif k[0] == 'lq': D += rc * Fraction(OPT.get('lqcap', '3'))"))
R.append(("    if (Sj.get('lq') or Sj.get('lQ')) and not L3Q: log('SOLUTION HAS lq BUT l3q FLAG OFF'); return\n",
          "    if (Sj.get('lq') or Sj.get('lQ')) and not L3Q: log('SOLUTION HAS lq BUT l3q FLAG OFF'); return\n"
          "    FBV.clear(); FBV.update({tuple(k): v for k, v in Sj.get('fb', [])})\n"
          "    if Sj.get('fb') and not FB: log('SOLUTION HAS fb BUT fb FLAG OFF'); return\n"
          "    if FBCAP is not None and any(v > FBCAP + 1e-9 for v in FBV.values()): log('fb VALUE ABOVE fbcap'); return\n"))
# cons2_delta: + fb inflow over all apex words (5^4 table in s_k, s_{k-1}, s_{k+1}, s_{k-2})
R.append(("        if L6R and L[j] == 6:   # RELAY_SPEC_s23.4\n",
          "        if FB and L[j] >= 7 and any(FBV.values()):   # s44: fb inflow at the 6 from u = L_j\n"
          "            T4 = np.zeros((5, 5, 5, 5))\n"
          "            for a4, b4, c4, e4 in itertools.product(range(5), repeat=4):\n"
          "                kk = fb_payee_at(6, L, {j: LET[a4], (j - 1) % 6: LET[b4], (j + 1) % 6: LET[c4], (j - 2) % 6: LET[e4]}, 6, j)\n"
          "                if kk: T4[a4, b4, c4, e4] = FBV.get(kk, 0.0)\n"
          "            D += T4[SALL[:, j], SALL[:, (j - 1) % 6], SALL[:, (j + 1) % 6], SALL[:, (j - 2) % 6]]\n"
          "        if L6R and L[j] == 6:   # RELAY_SPEC_s23.4\n"))
patch('prelay2.py', R)
# s44 run: binderR2 reads fb values too (reporting only)
patch('prelay2.py', [("    for fam in ('g', 'h', 'z', 'zr', 'r', 'rr', 'lq', 'lQ', 'z6', 'Z6', 'q', 'f'):",
                      "    for fam in ('g', 'h', 'z', 'zr', 'r', 'rr', 'lq', 'lQ', 'z6', 'Z6', 'q', 'f', 'fb'):")])
