#!/usr/bin/env python3
"""[exploratory] Euler-slack features of a 4-colouring state of G = T - v (see README.md for exact definitions).
Pure Python, stdlib only. Input: adjacency lists of G (indices 0..N-1), colours (list of 0..3), link (indices of the 5-cycle, cyclic order)."""
from itertools import combinations

FEATURES = [
    "N", "min_sl", "mean_sl",
    # colour-symmetric Kawarabayashi-Yoneda: ky_tot of colour c as mu, min / mean over the four c
    "ky_min_c", "ky_mean_c",
    # unfilled only (nan for filled)
    "sl_mu", "sl_alpha", "sl_A", "sl_B", "sl_mu_rel",
    "Uv", "Ue", "Urank", "Uslack",
    "Fv", "Fe", "Fslack",
    "ky_alpha", "ky_A", "ky_B", "ky_tot", "pen_alpha", "pen_A", "pen_B", "pen_tot", "ky_pen",
    "DL",
]
NAN = float("nan")


def pair_components(adj, col, p, q):
    """components of the {p,q}-subgraph: list of (vertex list, n_p, n_q, edges, penalty_q_side, penalty_p_side)"""
    seen = set(); out = []
    for s in range(len(col)):
        if col[s] not in (p, q) or s in seen: continue
        seen.add(s); st = [s]; comp = [s]
        while st:
            x = st.pop()
            for y in adj[x]:
                if col[y] in (p, q) and y not in seen:
                    seen.add(y); st.append(y); comp.append(y)
        out.append(comp)
    return out


def ky_pair(adj, col, mu, i):
    """sum over components C of H = G[V_mu u V_i] of max(b-a,-1), and the penalty sum over colour-i vertices of max(2-deg_H, 0)"""
    ky = 0; pen = 0
    for comp in pair_components(adj, col, mu, i):
        a = sum(1 for x in comp if col[x] == mu); b = len(comp) - a
        ky += max(b - a, -1)
        for x in comp:
            if col[x] == i:
                d = sum(1 for y in adj[x] if col[y] == mu)
                pen += max(2 - d, 0)
    return ky, pen


def slacks(adj, col):
    """slack_c = 2|V(B_c)| - 4 - |E(B_c)| for c = 0..3, B_c = all edges with exactly one endpoint coloured c (isolated vertices dropped)"""
    N = len(col); out = []
    for c in range(4):
        E = 0; V = set()
        for x in range(N):
            for y in adj[x]:
                if x < y and (col[x] == c) != (col[y] == c):
                    E += 1; V.add(x); V.add(y)
        out.append((2 * len(V) - 4 - E, len(V)))
    return out


def comp_of(adj, col, p, q, s):
    seen = {s}; st = [s]
    while st:
        x = st.pop()
        for y in adj[x]:
            if col[y] in (p, q) and y not in seen:
                seen.add(y); st.append(y)
    return seen


def frame(col, link):
    """None if filled; else (j, alpha, m, a, b, mu, A, B) with c(x_j)=c(x_{j+2}) (x_{j+1}=m, x_{j+3}=a, x_{j+4}=b)"""
    cs = [col[x] for x in link]
    if len(set(cs)) <= 3: return None
    assert len(set(cs)) == 4
    for j in range(5):
        if cs[j] == cs[(j + 2) % 5]:
            m = link[(j + 1) % 5]; a = link[(j + 3) % 5]; b = link[(j + 4) % 5]
            return j, cs[j], m, a, b, col[m], col[a], col[b]
    raise AssertionError("no repeat found")


def features(adj, col, link):
    N = len(col)
    slv = slacks(adj, col); sl = [x[0] for x in slv]
    f = {"N": N, "min_sl": min(sl), "mean_sl": sum(sl) / 4.0}
    kys = []
    for c in range(4):
        kys.append(sum(ky_pair(adj, col, c, i)[0] for i in range(4) if i != c))
    f["ky_min_c"] = min(kys); f["ky_mean_c"] = sum(kys) / 4.0
    fr = frame(col, link)
    for k in FEATURES:
        f.setdefault(k, NAN)
    if fr is None:
        f["DL"] = NAN
        return f, None
    j, al, m, a, b, mu, A, B = fr
    f["sl_mu"] = sl[mu]; f["sl_alpha"] = sl[al]; f["sl_A"] = sl[A]; f["sl_B"] = sl[B]
    f["sl_mu_rel"] = sl[mu] / (2.0 * slv[mu][1] - 4)
    K1 = comp_of(adj, col, mu, A, m); K2 = comp_of(adj, col, mu, B, m)
    f["DL"] = int(a in K1 and b in K2)
    U = K1 | K2
    Ue = sum(1 for x in U for y in adj[x] if x < y and y in U and
             ((x in K1 and y in K1) or (x in K2 and y in K2)))
    f["Uv"] = len(U); f["Ue"] = Ue; f["Urank"] = Ue - len(U) + 1; f["Uslack"] = 2 * len(U) - 4 - Ue
    # full mu versus {A,B}
    Fe = 0; Fv = set()
    for x in range(N):
        for y in adj[x]:
            if x < y and {col[x], col[y]} in ({mu, A}, {mu, B}):
                Fe += 1; Fv.add(x); Fv.add(y)
    f["Fv"] = len(Fv); f["Fe"] = Fe; f["Fslack"] = 2 * len(Fv) - 4 - Fe
    tot = 0; ptot = 0
    for name, i in (("alpha", al), ("A", A), ("B", B)):
        ky, pen = ky_pair(adj, col, mu, i)
        f["ky_" + name] = ky; f["pen_" + name] = pen; tot += ky; ptot += pen
    f["ky_tot"] = tot; f["pen_tot"] = ptot; f["ky_pen"] = tot + ptot
    return f, fr
