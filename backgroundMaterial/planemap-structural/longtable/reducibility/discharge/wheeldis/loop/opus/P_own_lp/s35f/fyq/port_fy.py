# Port the s25c fy family (RELAY_SPEC_s20 level 1) into a copy of the s33z engine (l3q stack).  Run once on fyq/eng/prelay2.py.
import sys
p = sys.argv[1]; s = open(p).read()
def rep(old, new):
    global s
    assert s.count(old) == 1, old; s = s.replace(old, new)
rep("ZH = 'zh' in FLAGS                   # stage 13 (R7h): big-centred split, z[five link from the big, hat classes on both sides]\n",
    "FY = 'fy' in FLAGS                   # s35f-fyq (port of s25c, RELAY_SPEC_s20 level 1): face-aware five -> big split; z key = fykey\n"
    "ZH = 'zh' in FLAGS or FY             # stage 13 (R7h): big-centred split, z[five link from the big, hat classes on both sides]\n")
rep("assert not ZR or ZH, 'zr needs zh'\n", "assert not ZR or ZH, 'zr needs zh'\nassert not FY or ('hat5' in FLAGS and not ZR and 'zh' not in FLAGS), 'fy port: needs hat5, excludes zh/zr'\n")
rep("    a = tuple(n) + (hr, hl); b = (n[0], n[4], n[3], n[2], n[1], hl, hr); return min(a, b)\n",
    "    a = tuple(n) + (hr, hl); b = (n[0], n[4], n[3], n[2], n[1], hl, hr); return min(a, b)\n"
    "FYMASK = 2   # ---- fy (verbatim from s25c/prelay2.py)\n"
    "def fy_vis(n): return (True, n[1] == 5, False, n[4] == 5, True)\n"
    "def fykey(n, h):\n"
    "    v = fy_vis(n); hm = tuple(h[k] if v[k] else FYMASK for k in range(5))\n"
    "    a = tuple(n) + hm; b = (n[0], n[4], n[3], n[2], n[1]) + tuple(reversed(hm)); return min(a, b)\n"
    "def fy_sender_key(w, H, j): return fykey(tuple(w[(j + i) % 5] for i in range(5)), tuple(H[(j + i) % 5] for i in range(5)))\n"
    "def fy_recv_key(U, a, b, e, f, p, q, r, s_):\n"
    "    n = (U, e, r, q, b)\n"
    "    return fykey(n, (c2(f), c2(s_) if e == 5 else FYMASK, FYMASK, c2(p) if b == 5 else FYMASK, c2(a)))\n")
rep("                    zk_ = zkey(tuple(w[(j + i) % n] for i in range(5)), H[j], H[(j - 1) % n]); cf[('z', zk_)] += 1\n",
    "                    zk_ = fy_sender_key(w, H, j) if FY else zkey(tuple(w[(j + i) % n] for i in range(5)), H[j], H[(j - 1) % n]); cf[('z', zk_)] += 1\n")
rep("    W = window_table(U, y, x)\n    if ZH:\n",
    "    W = window_table(U, y, x)\n"
    "    if FY:\n"
    "        for a, b, e, f, p_, q, r, s_ in itertools.product(range(5), repeat=8):\n"
    "            wd = (U, LET[e], LET[r], LET[q], LET[b])\n"
    "            if isR5(list(wd)): continue\n"
    "            W[a, b, 0, e, f, p_, q, r, s_] += ZV.get(fy_recv_key(U, LET[a], LET[b], LET[e], LET[f], LET[p_], LET[q], LET[r], LET[s_]), 0.0)\n"
    "    elif ZH:\n")
rep("    if ZH: C = np.where(c == 0, (1 + 470000 if H5 else 1 + 100000000)",
    "    if FY:   # s25c: the five's class = y root slots (b, e, q, r) + c2(a), c2(f), c2(p) if b = 5, c2(s) if e = 5\n"
    "        bits = (a >= 2) * 8 + (f >= 2) * 4 + ((b == 0) & (p >= 2)) * 2 + ((e == 0) & (s_ >= 2))\n"
    "        C = np.where(c == 0, 470000 + ((b * 5 + e) * 5 + q) * 5 * 16 + r * 16 + bits, C)\n"
    "    elif ZH: C = np.where(c == 0, (1 + 470000 if H5 else 1 + 100000000)")
rep("            zk_ = zkey((U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d]), c2(w[(j + 2) % d]), c2(w[(j - 2) % d])); cf[('z', zk_)] += 1\n",
    "            zk_ = fy_recv_key(U, w[(j - 2) % d], w[(j - 1) % d], w[(j + 1) % d], w[(j + 2) % d], s[(j - 2) % d], s[(j - 1) % d], s[j], s[(j + 1) % d]) if FY else zkey((U, w[(j + 1) % d], s[j], s[(j - 1) % d], w[(j - 1) % d]), c2(w[(j + 2) % d]), c2(w[(j - 2) % d])); cf[('z', zk_)] += 1\n")
o = "'clsR2_%d%s%s%s%s.bin' % (int(xon), 'z' if ZH else '', 'f' if F16"
assert s.count(o) == 2; s = s.replace(o, "'clsR2_%d%s%s%s%s%s.bin' % (int(xon), 'z' if ZH else '', 'y' if FY else '', 'f' if F16")
rep("'zh': ZH, 'apexcls': AC,", "'zh': ZH, 'fy': FY, 'apexcls': AC,")
open(p, 'w').write(s); print('patched', p)
