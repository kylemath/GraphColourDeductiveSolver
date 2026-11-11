#!/usr/bin/env python3
"""Standalone, Zero-Dependency Full-Stack t=0 Four Colour Theorem Discharging & Unavoidability Verifier.

Run in isolated stdlib-only mode:
    python3 -I verify_4ct_t0.py

Independently verifies from first principles (sharing zero runtime state with C++ or upstream scripts):
  Phase 1: 79-part local integer discharging rules (71 RSST + 8 N2), 2-ball locality, exact multiset mirror
           involution, concrete genus-0 sphere triangulation conservation (independent in/out rule evaluation
           summing to +120) + Window2Ball interval bracketing across degrees {5,6,7,8,9,12}, and Euler's formula.
  Phase 2: Reducible configuration registry (878 configs: subtiers L_full, L_eval, E2; 0 unproved), uniform CCW
           (R_t, R_{t+1}) ring orientation, kc-line cycle reconstruction, slotTri, Lean's exact admissibleX +
           foldSafeX (CGlue.lean:375-838) on all 346 C-configs, and 2.126's admissibleXM + foldSafeX + coherB +
           starB + chordB (CGlueM.lean).
  Phase 3: Exact 3,125-window c+ table recomputation, Karp zero-potential certificate (lambda* = 6/1),
           and exact Fraction arithmetic proof that c_final(u) <= 60 - 4*d <= 0 for ALL d >= 15.
  Phase 4: Exhaustive dihedral link-word completeness (all 5^d = 487,500 words for d=5..8; all c+-positive
           canonical words for d=9..17) and deterministic certificate replay with strict global-chirality
           rotOK (RotOcc) witness verification (including 9+ split q_{i,L} != q_{i,R} and deg-5 apex merges).
  Phase 5: 7 planted negative controls (NC1..NC7) verifying behavioral failure on rule/config/mirror/window/CGlue perturbations.
"""
import collections
from fractions import Fraction
import itertools
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, 'data')
CERT_DIR = os.path.join(DATA_DIR, 'certs')

FULL = (5, 9)


# ==============================================================================
# 1. Independent Discharging Rules, Exact Mirror Involution & Sphere Conservation
# ==============================================================================
def mirror_part(subs):
    n = len(subs)
    return [
        (
            subs[(4 - k) % n][0],
            subs[(5 - k) % n][1],
            tuple(reversed(subs[(4 - k) % n][2])),
        )
        for k in range(n)
    ]


def check_mirror_closed(parts):
    """Verify exact multiset involution: the multiset of parts equals the multiset of their mirrors."""
    orig_counts = collections.Counter(tuple(subs) for _, subs in parts)
    mirr_counts = collections.Counter(tuple(mirror_part(subs)) for _, subs in parts)
    if orig_counts != mirr_counts:
        for tag, subs in parts:
            key = tuple(subs)
            mkey = tuple(mirror_part(subs))
            if orig_counts[key] != mirr_counts[key] or orig_counts[mkey] != mirr_counts[mkey]:
                return False, tag
        return False, 'multiset_mismatch'
    return True, None


def load_and_verify_parts79(path):
    raw = json.load(open(path))
    parts = []
    for entry in raw['parts']:
        tag = entry['tag']
        n = entry['hub']
        assert 5 <= n <= 8, f'Part {tag} hub degree {n} outside 5..8'
        assert entry['target'] == 2 and entry['amount'] == 1, f'Part {tag} non-unit or non-spoke-2 transfer'
        subs = []
        for j, (sp, hat, fans) in enumerate(entry['subs']):
            sp_t = (int(sp[0]), int(sp[1]))
            hat_t = (int(hat[0]), int(hat[1]))
            fans_t = tuple((int(a), int(b)) for a, b in fans)
            assert 5 <= sp_t[0] <= sp_t[1] <= 9, (tag, j, sp_t)
            assert 5 <= hat_t[0] <= hat_t[1] <= 9, (tag, j, hat_t)
            if fans_t:
                # 2-ball locality & 9+ middle safety: fans are only specified on exact spokes 6, 7, or 8!
                assert sp_t[0] == sp_t[1] and 6 <= sp_t[0] <= 8, (tag, j, sp_t, fans_t)
                assert len(fans_t) == sp_t[0] - 5, (tag, j, sp_t, fans_t)
                for fr in fans_t:
                    assert 5 <= fr[0] <= fr[1] <= 9, (tag, j, fr)
            subs.append((sp_t, hat_t, fans_t))
        assert len(subs) == n
        parts.append((tag, subs))
    assert len(parts) == 79, f'Expected 79 parts, got {len(parts)}'
    ok, bad_tag = check_mirror_closed(parts)
    assert ok, f'Mirror involution failed on part {bad_tag}'
    return parts


def make_icosahedron():
    rot = {0: [1, 2, 3, 4, 5], 11: [6, 10, 9, 8, 7]}
    for k in range(5):
        rot[1 + k] = [1 + ((k + 1) % 5), 0, 1 + ((k - 1) % 5), 6 + ((k - 1) % 5), 6 + k]
        rot[6 + k] = [1 + k, 6 + ((k - 1) % 5), 11, 6 + ((k + 1) % 5), 1 + ((k + 1) % 5)]
    return rot


def glue_icosa_cap(rot, a, b, c):
    m2 = make_icosahedron()
    base = max(rot) + 1
    mp = {0: a, 2: b, 1: c, **{v: base + v - 3 for v in range(3, 12)}}
    out = {u: list(ru) for u, ru in rot.items()}
    for v in range(3, 12):
        out[mp[v]] = [mp[x] for x in m2[v]]
    for src, u, xp, xn in [(0, a, 2, 1), (2, b, 1, 0), (1, c, 0, 2)]:
        ru = out[u]
        ib = ru.index(mp[xp])
        assert ru[(ib + 1) % len(ru)] == mp[xn]
        rm = m2[src]
        t = (rm.index(xp) + 1) % len(rm)
        mid = []
        while rm[t] != xn:
            mid.append(mp[rm[t]])
            t = (t + 1) % len(rm)
        out[u] = ru[:ib + 1] + mid + ru[ib + 1:]
    return out


def flip_edge(rot, u, v):
    ru, rv = list(rot[u]), list(rot[v])
    w = ru[(ru.index(v) + 1) % len(ru)]
    z = rv[(rv.index(u) + 1) % len(rv)]
    assert w not in rot[z] and len(ru) >= 6 and len(rv) >= 6
    out = {k: list(val) for k, val in rot.items()}
    out[u].remove(v)
    out[v].remove(u)
    iw = out[w].index(u)
    assert out[w][(iw + 1) % len(out[w])] == v
    out[w] = out[w][:iw + 1] + [z] + out[w][iw + 1:]
    iz = out[z].index(v)
    assert out[z][(iz + 1) % len(out[z])] == u
    out[z] = out[z][:iz + 1] + [w] + out[z][iz + 1:]
    return out


def build_mixed_degree_sphere():
    T = make_icosahedron()
    T = glue_icosa_cap(T, 0, 1, 2)
    T = glue_icosa_cap(T, 0, 3, 4)
    T = glue_icosa_cap(T, 1, 5, 10)
    T = flip_edge(T, 0, 1)
    T = flip_edge(T, 0, 3)
    T = flip_edge(T, 1, 2)
    # Glue one more icosahedral cap onto a face at vertex 0 avoiding the unique deg-7 vertex
    for k in range(len(T[0])):
        b, c = T[0][k], T[0][(k + 1) % len(T[0])]
        if len(T[b]) != 7 and len(T[c]) != 7:
            T = glue_icosa_cap(T, 0, b, c)
            break
    return T


def verify_sphere_triangulation(T):
    """Verify T is a connected simple genus-0 sphere triangulation with min-degree >= 5."""
    V = len(T)
    assert V >= 12
    edges = set()
    darts = []
    for u, ru in T.items():
        assert len(ru) >= 5 and len(set(ru)) == len(ru) and u not in ru
        for v in ru:
            assert u in T[v], (u, v)
            edges.add((min(u, v), max(u, v)))
            darts.append((u, v))

    # Connectivity BFS
    start = next(iter(T))
    vis = {start}
    q = collections.deque([start])
    while q:
        u = q.popleft()
        for v in T[u]:
            if v not in vis:
                vis.add(v)
                q.append(v)
    assert len(vis) == V

    succ = lambda x, y: T[x][(T[x].index(y) + 1) % len(T[x])]
    seen_darts = set()
    F = 0
    for u, v in darts:
        if (u, v) in seen_darts:
            continue
        w = succ(u, v)
        assert succ(v, w) == u and succ(w, u) == v, (u, v, w)
        seen_darts.update([(u, v), (v, w), (w, u)])
        F += 1
    E = len(edges)
    assert len(darts) == 2 * E and 3 * F == 2 * E
    assert V - E + F == 2, f'Non-spherical triangulation: V={V}, E={E}, F={F}'
    return V, E, F


def verify_sphere_discharging_and_windows(T, parts_by_n, win_cls=None, recv_anchor_shift=2):
    """Evaluate discharging directly on sphere T (independent in/out) AND verify Window2Ball bracketing."""
    if win_cls is None:
        win_cls = Window2Ball
    verify_sphere_triangulation(T)
    succ = lambda x, y: T[x][(T[x].index(y) + 1) % len(T[x])]
    dec = lambda x: min(len(T[x]), 9)

    def match_part_T(h, subs, anchor):
        S = T[h]
        n = len(S)
        if n != len(subs):
            return False
        for j, (sp, hat, fans) in enumerate(subs):
            x = S[(anchor + j) % n]
            xp = S[(anchor + j - 1) % n]
            xn = S[(anchor + j + 1) % n]
            if not (sp[0] <= dec(x) <= sp[1]):
                return False
            if hat != FULL and not (hat[0] <= dec(succ(x, xp)) <= hat[1]):
                return False
            if any(f != FULL for f in fans):
                hv, hn = succ(x, xp), succ(xn, x)
                rx = T[x]
                t = (rx.index(hv) + 1) % len(rx)
                fvs = []
                while rx[t] != hn:
                    fvs.append(rx[t])
                    t = (t + 1) % len(rx)
                if len(fvs) != len(fans):
                    return False
                if not all(fr[0] <= dec(fv) <= fr[1] for fv, fr in zip(fvs, fans)):
                    return False
        return True

    total_final_charge = Fraction(0, 1)
    total_firings = 0
    for u in sorted(T):
        d = len(T[u])
        out_u = 0
        if 5 <= d <= 8:
            for _, subs in parts_by_n[d]:
                for a in range(d):
                    if match_part_T(u, subs, a):
                        out_u += 1
        in_u = 0
        for w in T[u]:
            dw = len(T[w])
            if 5 <= dw <= 8:
                a = (T[w].index(u) - recv_anchor_shift) % dw
                for _, subs in parts_by_n[dw]:
                    if match_part_T(w, subs, a):
                        in_u += 1
        cf_u = Fraction(10 * (6 - d) + in_u - out_u, 1)
        total_final_charge += cf_u
        total_firings += out_u

        # Check Window2Ball interval soundness [win_lo, win_hi] around vertex u
        link_u = [dec(w) for w in T[u]]
        W = win_cls(d, link_u)
        ins, outs = build_window_instances(W, parts_by_n)
        vmap = {}
        for i, w in enumerate(T[u]):
            wp, wn = T[u][(i - 1) % d], T[u][(i + 1) % d]
            s_prev, s_cur = succ(w, wp), succ(wn, w)
            vmap[100 + i] = dec(s_cur)
            rw = T[w]
            t = (rw.index(s_prev) + 1) % len(rw)
            privs = []
            while rw[t] != s_cur:
                privs.append(rw[t])
                t = (t + 1) % len(rw)
            if link_u[i] <= 8:
                if len(privs) != link_u[i] - 5:
                    return False, total_final_charge, total_firings
                for j, pv in enumerate(privs):
                    vmap[200 + 3 * i + j] = dec(pv)
            else:
                if len(privs) < 4:
                    return False, total_final_charge, total_firings
                vmap[200 + 3 * i + 0] = dec(privs[0])
                vmap[200 + 3 * i + 2] = dec(privs[-1])

        in_lo = sum(1 for cs, o in ins if not o and all(lo <= vmap[c] <= hi for c, lo, hi in cs))
        in_hi = sum(1 for cs, o in ins if all(lo <= vmap[c] <= hi for c, lo, hi in cs))
        out_lo = sum(1 for cs, o in outs if not o and all(lo <= vmap[c] <= hi for c, lo, hi in cs))
        out_hi = sum(1 for cs, o in outs if all(lo <= vmap[c] <= hi for c, lo, hi in cs))
        win_lo = Fraction(10 * (6 - d) + in_lo - out_hi, 1)
        win_hi = Fraction(10 * (6 - d) + in_hi - out_lo, 1)
        ub0 = Fraction(10 * (6 - d) + len(ins) - sum(1 for cs, o in outs if not cs and not o), 1)
        if not (win_lo <= cf_u <= win_hi <= ub0):
            return False, total_final_charge, total_firings

    if total_final_charge != Fraction(120, 1):
        return False, total_final_charge, total_firings
    return True, total_final_charge, total_firings


def verify_conservation_and_euler(parts_by_n):
    """Verify global conservation (+120) and Window2Ball soundness on concrete sphere triangulations + Euler."""
    T_ico = make_icosahedron()
    ok_ico, sum_ico, _ = verify_sphere_discharging_and_windows(T_ico, parts_by_n)
    assert ok_ico and sum_ico == Fraction(120, 1), f'Icosahedron check failed: {ok_ico}, {sum_ico}'

    T_mix = build_mixed_degree_sphere()
    deg_set = {len(r) for r in T_mix.values()}
    assert {5, 6, 7, 8, 9}.issubset(deg_set) and max(deg_set) >= 10
    ok_mix, sum_mix, firings_mix = verify_sphere_discharging_and_windows(T_mix, parts_by_n)
    assert ok_mix and sum_mix == Fraction(120, 1) and firings_mix > 200, (ok_mix, sum_mix, firings_mix)

    # General algebraic Euler identity: for any V >= 4 with E = 3V - 6, F = 2V - 4:
    # sum_{v in V} 10*(6 - deg(v)) = 60*V - 20*E = 60*V - 20*(3V - 6) = 120 > 0.
    for V_cnt in (4, 6, 12, 48, 1000):
        E_cnt = 3 * V_cnt - 6
        F_cnt = 2 * V_cnt - 4
        assert V_cnt - E_cnt + F_cnt == 2 and 3 * F_cnt == 2 * E_cnt
        assert Fraction(60, 1) * V_cnt - Fraction(20, 1) * E_cnt == Fraction(120, 1) > 0
    return T_mix, firings_mix


# ==============================================================================
# 2. Independent Configuration Registry, CCW Orientation & Lean CGlue Checks
# ==============================================================================
def reconstruct_cycle(nbrs, adj):
    nb = list(nbrs)
    if len(nb) < 3:
        return None
    local = {x: [y for y in nb if y != x and y in adj[x]] for x in nb}
    if any(len(v) != 2 for v in local.values()):
        return None
    cyc = [nb[0], local[nb[0]][0]]
    while len(cyc) < len(nb):
        a, b = local[cyc[-1]]
        nx = a if a != cyc[-2] else b
        if nx == cyc[0]:
            return None
        cyc.append(nx)
    return cyc if cyc[0] in local[cyc[-1]] else None


def _cfg_adj(c):
    m = c['m']
    ring_adj = [sorted(v for k, v in c['rot'][a] if k == 'R') for a in range(m)]
    int_adj = [list(c['int_adj'][a]) for a in range(m)]
    return ring_adj, int_adj


def verify_admissible_x(c, eqR=None, eqI=None, lbl=None, check_ring_distinct=True):
    """Independent translation of CGlue.lean:375-388 admissibleX (or CGlueM.lean admissibleXM)."""
    m, r = c['m'], c['ring']
    if eqR is None:
        eqR = c['eqR']
    if eqI is None:
        eqI = c['eqI']
    if lbl is None:
        lbl = c['lbl']
    ring_adj, int_adj = _cfg_adj(c)
    if not (1 <= len(eqR) + len(eqI) <= 4):
        return False
    if len(lbl) != m + r:
        return False
    eqR_set = {(t, a) for t, a in eqR}
    eqI_set = {(a, b) for a, b in eqI}
    if not all(0 <= a < m and t in ring_adj[a] for t, a in eqR):
        return False
    if not all(0 <= a < m and 0 <= b < m and a in int_adj[b] for a, b in eqI):
        return False
    for a in range(m):
        for t in ring_adj[a]:
            if not (0 <= t < r):
                return False
            if (t, a) in eqR_set:
                if lbl[a] != lbl[m + t]:
                    return False
            else:
                if lbl[a] == lbl[m + t]:
                    return False
        for b in int_adj[a]:
            if not (0 <= b < m):
                return False
            if (b, a) in eqI_set or (a, b) in eqI_set:
                if lbl[a] != lbl[b]:
                    return False
            else:
                if lbl[a] == lbl[b]:
                    return False
    if check_ring_distinct:
        for s in range(r):
            for t in range(r):
                if s != t and lbl[m + s] == lbl[m + t]:
                    return False
    return True


def _excl_b(m, r, ring_adj, int_adj, p, q):
    if q == (p + 1) % r or p == (q + 1) % r:
        return True
    for c_idx in range(m):
        if p in ring_adj[c_idx]:
            if q in ring_adj[c_idx]:
                return True
            if any(0 <= a < m and q in ring_adj[a] for a in int_adj[c_idx]):
                return True
    return False


def _cyc_ex(m, r, ring_adj, int_adj, p, q):
    p1 = [[c_idx] for c_idx in range(m)]
    p2 = [path + [x] for path in p1 for x in int_adj[path[-1]]]
    p3 = [path + [x] for path in p2 for x in int_adj[path[-1]]]
    p4 = [path + [x] for path in p3 for x in int_adj[path[-1]]]
    for path in p2 + p3 + p4:
        plen = len(path)
        if not (2 <= plen <= 4) or len(set(path)) != plen:
            continue
        if not all(0 <= i < m for i in path):
            continue
        if p not in ring_adj[path[0]] or q not in ring_adj[path[-1]]:
            continue
        if not all(path[i + 1] in int_adj[path[i]] for i in range(plen - 1)):
            continue
        for j in range(3):
            if j + 1 >= plen:
                continue
            u, v = path[j], path[j + 1]
            if any(s in ring_adj[v] for s in ring_adj[u]):
                continue
            ok_apex = True
            for e in int_adj[u]:
                if e in int_adj[v]:
                    if e in path:
                        ok_apex = False
                        break
                    if plen == 4 and not any(0 <= f < m and f not in path for f in int_adj[e]):
                        ok_apex = False
                        break
            if ok_apex:
                return True
    return False


def verify_fold_safe_x(c, eqR=None, eqI=None, lbl=None):
    """Independent translation of CGlue.lean:779-838 foldSafeX."""
    m, r = c['m'], c['ring']
    if eqR is None:
        eqR = c['eqR']
    if eqI is None:
        eqI = c['eqI']
    if lbl is None:
        lbl = c['lbl']
    ring_adj, int_adj = _cfg_adj(c)
    eqR_set = {(t, a) for t, a in eqR}
    eqI_set = {(a, b) for a, b in eqI}
    touched = {t for t, _ in eqR}
    for a in range(m):
        for s in ring_adj[a]:
            if (s, a) in eqR_set:
                continue
            for t in range(r):
                if t not in touched or lbl[m + t] != lbl[a] or s == t:
                    continue
                if not (_excl_b(m, r, ring_adj, int_adj, s, t) or _cyc_ex(m, r, ring_adj, int_adj, s, t)):
                    return False
        for b in int_adj[a]:
            if (b, a) in eqI_set or (a, b) in eqI_set:
                continue
            for t in range(r):
                if t not in touched or lbl[m + t] != lbl[a]:
                    continue
                for tp in range(r):
                    if tp not in touched or lbl[m + tp] != lbl[b] or t == tp:
                        continue
                    if not (_excl_b(m, r, ring_adj, int_adj, t, tp) or _cyc_ex(m, r, ring_adj, int_adj, t, tp)):
                        return False
    return True


def verify_2o126_merge(c, eqR=None, eqI=None, lbl=None):
    """Independent translation of CGlueM.lean (ROUTE_I_PLAN.md:93-162): admissibleXM, foldSafeX, coherB, starB, chordB."""
    if eqR is None:
        eqR = c['eqR']
    if eqI is None:
        eqI = c['eqI']
    if lbl is None:
        lbl = c['lbl']
    if not verify_admissible_x(c, eqR, eqI, lbl, check_ring_distinct=False):
        return False
    if not verify_fold_safe_x(c, eqR, eqI, lbl):
        return False
    m, r = c['m'], c['ring']
    ring_adj, int_adj = _cfg_adj(c)
    touched = sorted({t for t, _ in eqR})
    # coherB
    for s in touched:
        for t in touched:
            if lbl[m + s] != lbl[m + t] and s != t:
                if not (_excl_b(m, r, ring_adj, int_adj, s, t) or _cyc_ex(m, r, ring_adj, int_adj, s, t)):
                    return False
    # starB
    by_lbl = collections.defaultdict(list)
    for t in touched:
        by_lbl[lbl[m + t]].append(t)
    eqR_set = {(t, a) for t, a in eqR}
    for lv, ts in by_lbl.items():
        if len(ts) >= 2:
            centres = [a for a in range(m) if lbl[a] == lv and all((t, a) in eqR_set for t in ts)]
            if len(centres) != 1:
                return False
    # chordB
    for s, c1 in eqR:
        for t, c2 in eqR:
            if c1 == c2 and s != t:
                rc = c['rot'][c1]
                g = len(rc)
                for j in range(g):
                    if rc[j] == ['R', s]:
                        if rc[(j - 1) % g] == ['R', t] or rc[(j + 1) % g] == ['R', t]:
                            return False
    return True


def load_and_verify_registry(path):
    raw = json.load(open(path))
    configs = raw['configs']
    assert len(configs) == 878
    c_verified_cnt = 0
    for c in configs:
        assert c['tier'] in ('L', 'E2'), f"Config {c['name']} has invalid tier {c.get('tier')}"
        assert c['subtier'] in ('L_full', 'L_eval', 'E2'), f"Config {c['name']} has invalid subtier {c.get('subtier')}"
        if c['tier'] == 'L':
            assert c['subtier'] in ('L_full', 'L_eval')
        else:
            assert c['subtier'] == 'E2'
        ev = c.get('evidence', '')
        assert ev and '(-)' not in ev and 'to confirm' not in ev.lower(), f"Bad provenance in {c['name']}: {ev}"

        if 'data/e2_recheck_nl/' in ev:
            fn = os.path.join(DATA_DIR, 'e2_recheck_nl', f"{c['name']}.out")
            assert os.path.exists(fn), f'Missing E2 recheck log {fn}'
            txt = open(fn).read()
            kc_part, df_part = txt.split('== dfast18')
            assert 'D=true' in kc_part and 'D=true' in df_part, f'Incomplete E2 log {fn}'
        if 'data/e2_recheck_win/' in ev:
            fn = os.path.join(DATA_DIR, 'e2_recheck_win', f"{c['name']}.out")
            assert os.path.exists(fn), f'Missing E2 window recheck log {fn}'
            txt = open(fn).read()
            kc_part, sec_part = txt.split('== second_engine')
            if c['kind'] == 'D':
                assert 'D=true' in kc_part and 'D=true' in sec_part, f'Incomplete E2 D-window log {fn}'
            else:
                assert 'adm=yes leftover 0' in kc_part and 'C-REDUCIBLE' in kc_part, f'Bad kc C-window log {fn}'
                assert 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in sec_part, f'Bad cfast log {fn}'

        m = c['m']
        r = c['ring']
        assert m >= 1 and r >= 6
        assert len(c['deg']) == m and len(c['rot']) == m and len(c['int_adj']) == m

        ring_sets = []
        int_sets = []
        for a in range(m):
            g = c['deg'][a]
            assert g >= 5 and len(c['rot'][a]) == g
            rset = set()
            iset = set()
            for kind_ch, val in c['rot'][a]:
                if kind_ch == 'I':
                    assert 0 <= val < m and val != a
                    assert val not in iset, f"Duplicate interior slot in {c['name']}"
                    iset.add(val)
                elif kind_ch == 'R':
                    assert 0 <= val < r
                    assert val not in rset, f"Duplicate ring slot in {c['name']}"
                    rset.add(val)
                else:
                    raise AssertionError(f'Bad slot kind {kind_ch}')
            assert sorted(iset) == c['int_adj'][a]
            ring_sets.append(rset)
            int_sets.append(iset)

        # Verify symmetric interior adjacency, consistent planar orientation, slotTri, AND uniform CCW (R_t, R_{t+1})
        for a in range(m):
            ra = [(k, v) for k, v in c['rot'][a]]
            g = len(ra)
            for idx in range(g):
                s0 = ra[idx]
                s1 = ra[(idx + 1) % g]
                if s0[0] == 'R' and s1[0] == 'R':
                    assert (s1[1] - s0[1]) % r == 1, f"Non-CCW R-R pair {s0}->{s1} in {c['name']}"
                if s0[0] == 'I':
                    b = s0[1]
                    assert a in int_sets[b], f"Asymmetric int_adj in {c['name']}"
                    rb = [(k, v) for k, v in c['rot'][b]]
                    if s1[0] == 'I':
                        assert s1 in rb, f"Missing triangle edge in {c['name']}"
                        pos_s1 = rb.index(s1)
                        assert rb[(pos_s1 + 1) % len(rb)] == ('I', a), f"Orientation mismatch in {c['name']}"
                    else:
                        # slotTri (COccBridge.lean:52-54)
                        assert s1[1] in ring_sets[b], f"slotTri(I->R) failed in {c['name']}"
                if s0[0] == 'R' and s1[0] == 'I':
                    b = s1[1]
                    assert s0[1] in ring_sets[b], f"slotTri(R->I) failed in {c['name']}"

        # Verify Lean contraction admissibility & fold-safety on EVERY C and C_merge config
        if c['kind'] == 'D':
            assert c['X'] == '-' and c['rim_pinned'] is False
        elif c['kind'] == 'C':
            assert c['X'] != '-' and c['rim_pinned'] == (len(c['eqR']) > 0) == ('R' in c['X'])
            assert verify_admissible_x(c), f"admissibleX failed on {c['name']}"
            assert verify_fold_safe_x(c), f"foldSafeX failed on {c['name']}"
            c_verified_cnt += 1
        elif c['kind'] == 'C_merge':
            assert c['name'] == '2.126' and c['rim_pinned'] is True
            assert verify_2o126_merge(c), '2.126 merge checks failed!'
        else:
            raise AssertionError(f"Unknown kind {c['kind']}")

        # Cross-check against kc_line
        assert 'kc_line' in c
        f = c['kc_line'].split()
        assert int(f[1]) == r and int(f[2]) == m
        rp = f[3].split(';')
        ip = f[4].split(';')
        adj = collections.defaultdict(set)
        for j in range(r):
            adj[('R', j)].add(('R', (j + 1) % r))
            adj[('R', (j + 1) % r)].add(('R', j))
        for u in range(m):
            r_list = [] if rp[u] == '-' else [int(x) for x in rp[u].split(',')]
            i_list = [] if ip[u] == '-' else [int(x) for x in ip[u].split(',')]
            assert set(r_list) == ring_sets[u]
            assert set(i_list) == int_sets[u]
            for j in r_list:
                adj[('I', u)].add(('R', j))
                adj[('R', j)].add(('I', u))
            for w in i_list:
                adj[('I', u)].add(('I', w))
                adj[('I', w)].add(('I', u))
        for u in range(m):
            cyc = reconstruct_cycle(adj[('I', u)], adj)
            assert cyc is not None and len(cyc) == c['deg'][u]
            ra = [(k, v) for k, v in c['rot'][u]]
            sh = cyc.index(ra[0])
            fwd = cyc[sh:] + cyc[:sh]
            rev_c = list(reversed(cyc))
            sh_r = rev_c.index(ra[0])
            bwd = rev_c[sh_r:] + rev_c[:sh_r]
            assert ra == fwd or ra == bwd, f"rot vs kc_line mismatch in {c['name']}"

    assert c_verified_cnt == 346, f'Expected 346 C configs, got {c_verified_cnt}'
    return configs


# ==============================================================================
# 3. Independent 2-Ball Window, Rule Evaluation, & Symbolic DFS Replay
# ==============================================================================
def npriv(letter):
    if letter == 5:
        return 0
    if letter >= 9:
        return 3
    return letter - 5


class Window2Ball:
    """Independent 2-ball window around hub u of degree d with spoke link letters in {5,6,7,8,9}."""

    def __init__(self, d, link):
        self.d = d
        self.link = list(link)
        self.rot_u = [1 + i for i in range(d)]
        self.rot_w = []
        self.seg = []
        r2 = []
        for i in range(d):
            k = npriv(self.link[i])
            s_prev = 1 + d + ((i - 1) % d)
            s_cur = 1 + d + i
            sg = [s_prev] + [1 + 2 * d + 3 * i + (j - 1) for j in range(1, k + 1)] + [s_cur]
            self.seg.append(sg)
            self.rot_w.append([0, 1 + ((i - 1) % d)] + sg + [1 + ((i + 1) % d)])
            r2.extend(sg[:-1])
        m = len(r2)
        self.r2prev = {r2[t]: r2[(t - 1) % m] for t in range(m)}
        self.r2next = {r2[t]: r2[(t + 1) % m] for t in range(m)}

    def deg_info(self, v):
        if v == -1:
            return ('open', 0)
        if v == 0:
            return ('dec', min(self.d, 9))
        if 1 <= v <= self.d:
            return ('dec', self.link[v - 1])
        if 1 + self.d <= v <= 2 * self.d:
            return ('var', 100 + (v - 1 - self.d))
        q = v - 1 - 2 * self.d
        i, j = q // 3, (q % 3) + 1
        assert not (self.link[i] >= 9 and j == 2), 'Unread 9+ middle placeholder accessed!'
        return ('var', 200 + 3 * i + (j - 1))

    def succ(self, x, y):
        if x == -1:
            return -1
        if x == 0:
            idx = self.rot_u.index(y)
            return self.rot_u[(idx + 1) % self.d]
        if 1 <= x <= self.d:
            rw = self.rot_w[x - 1]
            idx = rw.index(y)
            return rw[(idx + 1) % len(rw)]
        prev = self.r2prev[x]
        nxt = self.r2next[x]
        if 1 + self.d <= x <= 2 * d_val(self):
            i = x - 1 - self.d
            w1, w0 = 1 + ((i + 1) % self.d), 1 + i
            if y == w1:
                return w0
            if y == w0:
                return prev
            if y == prev:
                return -1
            if y == nxt:
                return w1
            return -1
        q = x - 1 - 2 * self.d
        wi = 1 + (q // 3)
        if y == wi:
            return prev
        if y == prev:
            return -1
        if y == nxt:
            return wi
        return -1


def d_val(W):
    return W.d


def fit_part(W, h, subs, anchor):
    S = W.rot_u if h == 0 else W.rot_w[h - 1]
    n = len(subs)
    if len(S) != n:
        return None
    conds = []
    is_open = False

    def test_v(v, rng):
        nonlocal is_open
        if rng == FULL:
            return True
        kind, val = W.deg_info(v)
        if kind == 'dec':
            return rng[0] <= val <= rng[1]
        if kind == 'open':
            is_open = True
            return True
        conds.append((val, rng[0], rng[1]))
        return True

    for j in range(n):
        sp, hat, fans = subs[j]
        x = S[(anchor + j) % n]
        xp = S[(anchor + j - 1) % n]
        xn = S[(anchor + j + 1) % n]
        if not test_v(x, sp):
            return None
        if hat != FULL:
            if not test_v(W.succ(x, xp), hat):
                return None
        if any(f != FULL for f in fans):
            if x == 0 or (1 <= x <= W.d):
                hv = W.succ(x, xp)
                hn = W.succ(xn, x)
                rr = W.rot_u if x == 0 else W.rot_w[x - 1]
                t = (rr.index(hv) + 1) % len(rr)
                fan_vs = []
                while rr[t] != hn:
                    fan_vs.append(rr[t])
                    t = (t + 1) % len(rr)
                    if len(fan_vs) > len(rr):
                        return None
                if len(fan_vs) != len(fans):
                    return None
                for fv, fr in zip(fan_vs, fans):
                    if not test_v(fv, fr):
                        return None
            else:
                is_open = True
    return (tuple(conds), is_open)


def build_window_instances(W, parts_by_n):
    ins = []
    outs = []
    if 5 <= W.d <= 8:
        for _, subs in parts_by_n[W.d]:
            for a in range(W.d):
                r = fit_part(W, 0, subs, a)
                if r is not None:
                    outs.append(r)
    for i in range(W.d):
        L = W.link[i]
        if L <= 8:
            for _, subs in parts_by_n[L]:
                assert W.rot_w[i][(L - 2 + 2) % L] == 0
                r = fit_part(W, 1 + i, subs, L - 2)
                if r is not None:
                    ins.append(r)
    return ins, outs


# ==============================================================================
# 4. Strict Global-Chirality rotOK (RotOcc) Witness Verifier (O(m * g), Zero Search)
# ==============================================================================
def verify_rot_witness(d, link, cfg, phi, sigma, shifts, rel_set):
    """Directly verify a certified RotOcc embedding witness (phi, sigma, shifts)."""
    m = cfg['m']
    if sigma not in (1, -1):
        return False, None
    if len(phi) != m or len(shifts) != m or len(set(phi)) != m:
        return False, None

    # Build exact R2 boundary cycle Z, splitting 9+ middle into two distinct non-hosts q_{i,L} != q_{i,R}
    Z = []
    pos_in_Z = {}
    for i in range(d):
        L = link[i]
        if L == 9:
            seq = [
                1 + 2 * d + 3 * i + 0,
                1000 + 2 * i + 0,
                1000 + 2 * i + 1,
                1 + 2 * d + 3 * i + 2,
                1 + d + i,
            ]
        else:
            seq = [1 + 2 * d + 3 * i + (j - 1) for j in range(1, L - 5 + 1)] + [1 + d + i]
        for v in seq:
            pos_in_Z[v] = len(Z)
            Z.append(v)

    M = len(Z)
    uf = list(range(M))

    def uf_find(x):
        while uf[x] != x:
            uf[x] = uf[uf[x]]
            x = uf[x]
        return x

    def uf_union(a, b):
        ra, rb = uf_find(a), uf_find(b)
        if ra != rb:
            uf[rb] = ra

    # Merge outside triangle apexes ONLY around s_i pinned to exact degree 5
    for a in range(m):
        h = phi[a]
        if 1 + d <= h < 1 + 2 * d and cfg['deg'][a] == 5:
            t = pos_in_Z[h]
            uf_union((t - 1) % M, t)

    next_fresh = 3000
    rf = []
    req = []
    phi_set = set(phi)

    for a in range(m):
        h = phi[a]
        g = cfg['deg'][a]
        sh = shifts[a]
        if not (0 <= sh < g):
            return False, None
        if h == 0:
            if d != g:
                return False, None
            r = [1 + i for i in range(d)]
        elif 1 <= h <= d:
            i = h - 1
            if link[i] > 8 or link[i] != g:
                return False, None
            r = (
                [0, 1 + ((i - 1) % d), 1 + d + ((i - 1) % d)]
                + [1 + 2 * d + 3 * i + (j - 1) for j in range(1, link[i] - 5 + 1)]
                + [1 + d + i, 1 + ((i + 1) % d)]
            )
        elif 1 + d <= h < 1 + 2 * d:
            if not (5 <= g <= 8):
                return False, None
            i = h - 1 - d
            vc = 100 + i
            if vc not in rel_set:
                return False, None
            req.append((vc, g))
            t = pos_in_Z[h]
            prev, nxt = Z[(t - 1) % M], Z[(t + 1) % M]
            r = [nxt, 1 + ((i + 1) % d), 1 + i, prev]
            if g == 5:
                r.append(2000 + uf_find((t - 1) % M))
            else:
                r.append(2000 + uf_find((t - 1) % M))
                for _ in range(g - 6):
                    r.append(next_fresh)
                    next_fresh += 1
                r.append(2000 + uf_find(t))
        else:
            if not (5 <= g <= 8):
                return False, None
            q = h - 1 - 2 * d
            i, j = q // 3, (q % 3) + 1
            if i < 0 or i >= d or j < 1 or j > npriv(link[i]) or (link[i] >= 9 and j == 2):
                return False, None
            vc = 200 + 3 * i + (j - 1)
            if vc not in rel_set:
                return False, None
            req.append((vc, g))
            t = pos_in_Z[h]
            prev, nxt = Z[(t - 1) % M], Z[(t + 1) % M]
            r = [nxt, 1 + i, prev, 2000 + uf_find((t - 1) % M)]
            for _ in range(g - 5):
                r.append(next_fresh)
                next_fresh += 1
            r.append(2000 + uf_find(t))

        if len(r) != g or len(set(r)) != g:
            return False, None
        rf.append(r)

    # Check cyclic slot correspondence and single-valued ring map rho disjoint from phi_set
    rho = {}
    for a in range(m):
        g = cfg['deg'][a]
        sh = shifts[a]
        rc = cfg['rot'][a]
        rfa = rf[a]
        for k in range(g):
            fv = rfa[(sh + sigma * k) % g]
            kind_ch, val = rc[k]
            if kind_ch == 'I':
                if fv != phi[val]:
                    return False, None
            else:
                if fv in phi_set:
                    return False, None  # RotOcc.disj
                if val in rho:
                    if rho[val] != fv:
                        return False, None
                else:
                    rho[val] = fv

    return True, tuple(sorted(req))


# ==============================================================================
# 5. Deterministic Symbolic DFS Replay & Dominance Verification
# ==============================================================================
def site_key(c):
    return (c - 100, 0, 0) if c < 200 else ((c - 200) // 3, 1, (c - 200) % 3)


def classes_of_verified(v, allc):
    ts = [(lo, hi) for cs, _ in allc for (c, lo, hi) in cs if c == v]
    pat = lambda x: tuple(lo <= x <= hi for lo, hi in ts)
    p9 = pat(9)
    c9 = [x for x in (5, 6, 7, 8, 9) if pat(x) == p9]
    for x in c9:
        assert pat(x) == p9
    return [c9] + [[x] for x in (5, 6, 7, 8) if pat(x) != p9]


def simp1(v, S, inst):
    cs, o = inst
    for c, lo, hi in cs:
        if c == v and not any(lo <= l <= hi for l in S):
            return None
    return (tuple(t for t in cs if not (t[0] == v and all(t[1] <= l <= t[2] for l in S))), o)


def simpR1(v, S, r_item):
    req, idx = r_item
    for c, l in req:
        if c == v and S != [l]:
            return None
    return (tuple(t for t in req if t[0] != v), idx)


def replay_dfs(base, vs, ins, outs, reqs):
    stats = {'nodes': 0, 'ub_leaves': 0, 'kill_leaves': 0}

    def rec(depth, cur_ins, cur_outs, cur_reqs):
        stats['nodes'] += 1
        ub = base + len(cur_ins) - sum(1 for cs, o in cur_outs if not cs and not o)
        if ub <= 0:
            stats['ub_leaves'] += 1
            return True
        if any(not rq for rq, _ in cur_reqs):
            stats['kill_leaves'] += 1
            return True
        if depth == len(vs):
            return False
        v, cls = vs[depth]
        for S in cls:
            i2 = [y for y in (simp1(v, S, x) for x in cur_ins) if y is not None]
            o2 = [y for y in (simp1(v, S, x) for x in cur_outs) if y is not None]
            r2 = [y for y in (simpR1(v, S, x) for x in cur_reqs) if y is not None]
            if not rec(depth + 1, i2, o2, r2):
                return False
        return True

    ok = rec(0, ins, outs, reqs)
    return ok, stats


# ==============================================================================
# 6. Independent 3,125-Window c+ Table, Karp Potential, & Word Enumerators
# ==============================================================================
def maxsat_independent(insts):
    vset = sorted({c for cs, _ in insts for c, _, _ in cs})
    nv = len(vset)
    pos = {v: k for k, v in enumerate(vset)}
    by_v = [[] for _ in range(nv)]
    for t, (cs, _) in enumerate(insts):
        for c, lo, hi in cs:
            by_v[pos[c]].append((t, lo, hi))
    dead = [0] * len(insts)
    best = 0

    def rec(k, ub):
        nonlocal best
        if ub <= best:
            return
        if k == nv:
            best = ub
            return
        for val in (5, 6, 7, 8, 9):
            nub = ub
            for t, lo, hi in by_v[k]:
                if not (lo <= val <= hi):
                    if dead[t] == 0:
                        nub -= 1
                    dead[t] += 1
            rec(k + 1, nub)
            for t, lo, hi in by_v[k]:
                if not (lo <= val <= hi):
                    dead[t] -= 1

    rec(0, len(insts))
    return best


def compute_and_verify_cplus_tail(parts_by_n, tail_cert_path):
    cp = {}
    cmax = {5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    for word in itertools.product((5, 6, 7, 8, 9), repeat=5):
        a, b, c, d, e = word
        if c == 9:
            val = 0
        else:
            W = Window2Ball(10, [a, b, c, d, e, 5, 5, 5, 5, 5])
            w2_ins = []
            for _, subs in parts_by_n[c]:
                r = fit_part(W, 1 + 2, subs, c - 2)
                if r is not None:
                    w2_ins.append(r)
            val = maxsat_independent(w2_ins)
        cp[word] = val
        if val > cmax[c]:
            cmax[c] = val

    assert len(cp) == 3125
    cert = json.load(open(tail_cert_path))
    for w, val in cp.items():
        s = ''.join(map(str, w))
        assert cert['cplus_3125'][s] == val, f'c+ mismatch at {s}'

    # Exact Fraction verification of Karp zero potential phi == 0 with lambda* = 6/1
    lam_star = Fraction(cert['karp_lambda_star_num'], cert['karp_lambda_star_den'])
    assert lam_star == Fraction(6, 1)
    phi = {st: Fraction(0, 1) for st in itertools.product((5, 6, 7, 8, 9), repeat=4)}
    max_edge = Fraction(-1000, 1)
    for st in phi:
        for e in (5, 6, 7, 8, 9):
            nxt = (st[1], st[2], st[3], e)
            lhs = Fraction(cp[st + (e,)], 1) + phi[nxt] - phi[st]
            assert lhs <= lam_star
            if lhs > max_edge:
                max_edge = lhs
    assert max_edge == lam_star == Fraction(6, 1)
    assert cp[(5, 5, 5, 5, 5)] == 6

    # Verify infinite tail: for all d >= 15, 10*(6 - d) + 6*d = 60 - 4*d <= 0
    assert Fraction(10, 1) * (6 - 15) + lam_star * 15 == Fraction(0, 1)
    for d in range(15, 200):
        assert Fraction(10, 1) * (6 - d) + lam_star * d == Fraction(60 - 4 * d, 1) <= 0

    return cp, cmax


def dihedral_canon_str(w):
    d = len(w)
    best = None
    for r in range(d):
        rot = w[r:] + w[:r]
        rev = rot[::-1]
        if best is None or rot < best:
            best = rot
        if rev < best:
            best = rev
    return ''.join(map(str, best))


def is_dihedral_canon(w):
    d = len(w)
    t = tuple(w)
    for r in range(d):
        rot = t[r:] + t[:r]
        if rot < t or rot[::-1] < t:
            return False
    return True


def enumerate_cplus_canon_words(d, cp, cmax):
    base = 10 * (6 - d)
    L = [0] * d
    out = []

    def partial_bound(k):
        s = base
        for i in range(d):
            if i - 2 >= 0 and i + 2 <= k - 1:
                s += cp[(L[i - 2], L[i - 1], L[i], L[i + 1], L[i + 2])]
            elif i <= k - 1:
                s += cmax[L[i]]
            else:
                s += 6
        return s

    def rec(k):
        if k == d:
            if not is_dihedral_canon(L):
                return
            cyc = base + sum(
                cp[(L[(i - 2) % d], L[(i - 1) % d], L[i], L[(i + 1) % d], L[(i + 2) % d])]
                for i in range(d)
            )
            if cyc > 0:
                out.append(''.join(map(str, L)))
            return
        for v in (5, 6, 7, 8, 9):
            if k > 0 and v < L[0]:
                continue
            L[k] = v
            if partial_bound(k + 1) > 0:
                rec(k + 1)
        L[k] = 0

    rec(0)
    return out


# ==============================================================================
# 7. Negative Controls (Anti-Goodharting Rule 2: Every Check Must Be Able to Fail)
# ==============================================================================
def run_negative_controls(parts, parts_by_n, configs, T_mix):
    print('\n=== Phase 5: Running 7 Planted Negative Controls (NC1..NC7) ===')

    # NC1: Drop 2.126 (rsst003_2o126) on d=6 canonical link 565667 -> MUST FAIL!
    rec_d6 = None
    for line in open(os.path.join(CERT_DIR, 'cert_d6.jsonl')):
        obj = json.loads(line)
        if obj['link'] == '565667':
            rec_d6 = obj
            break
    assert rec_d6 is not None and 'embs' in rec_d6
    W6 = Window2Ball(6, [5, 6, 5, 6, 6, 7])
    ins6, outs6 = build_window_instances(W6, parts_by_n)
    allc6 = ins6 + outs6
    rel6 = sorted({c for cs, _ in allc6 for c, _, _ in cs}, key=site_key)
    vs6 = [(v, classes_of_verified(v, allc6)) for v in rel6]
    reqs6_no_2126 = []
    for k, (cid, phi, sg, shifts) in enumerate(rec_d6['embs']):
        if configs[cid]['name'] == '2.126':
            continue
        ok_w, rq = verify_rot_witness(6, [5, 6, 5, 6, 6, 7], configs[cid], phi, sg, shifts, set(rel6))
        assert ok_w
        reqs6_no_2126.append((rq, k))
    ok_nc1, _ = replay_dfs(0, vs6, ins6, outs6, reqs6_no_2126)
    assert not ok_nc1, 'NC1 FAILED: d=6 link 565667 passed without 2.126!'
    print('  [PASS] NC1: Dropping 2.126 (rsst003_2o126) on d=6 link 565667 -> REJECTED as expected.')

    # NC2: Drop the 8 N2 parts on d=7 canonical link 5657669 (with 128.1324802 absent) -> MUST FAIL!
    parts71_by_n = collections.defaultdict(list)
    for tag, subs in parts:
        if not tag.startswith('N2_'):
            parts71_by_n[len(subs)].append((tag, subs))
    rec_d7 = None
    for line in open(os.path.join(CERT_DIR, 'cert_d7.jsonl')):
        obj = json.loads(line)
        if obj['link'] == '5657669':
            rec_d7 = obj
            break
    assert rec_d7 is not None
    W7 = Window2Ball(7, [5, 6, 5, 7, 6, 6, 9])
    ins7, outs7 = build_window_instances(W7, parts71_by_n)
    allc7 = ins7 + outs7
    rel7 = sorted({c for cs, _ in allc7 for c, _, _ in cs}, key=site_key)
    vs7 = [(v, classes_of_verified(v, allc7)) for v in rel7]
    reqs7 = []
    for k, (cid, phi, sg, shifts) in enumerate(rec_d7.get('embs', [])):
        ok_w, rq = verify_rot_witness(7, [5, 6, 5, 7, 6, 6, 9], configs[cid], phi, sg, shifts, set(rel7))
        if ok_w:
            reqs7.append((rq, k))
    ok_nc2, _ = replay_dfs(-10, vs7, ins7, outs7, reqs7)
    assert not ok_nc2, 'NC2 FAILED: d=7 link 5657669 passed without N2 parts and without 128.1324802!'
    print('  [PASS] NC2: Dropping 8 N2 parts on d=7 link 5657669 (no 128.1324802) -> REJECTED as expected.')

    # NC3: Drop 0.7322 (rsst000_0o7322) on d=5 canonical link 55555 -> MUST FAIL!
    W5 = Window2Ball(5, [5, 5, 5, 5, 5])
    ins5, outs5 = build_window_instances(W5, parts_by_n)
    ok_nc3, _ = replay_dfs(10, [], ins5, outs5, [])
    assert not ok_nc3, 'NC3 FAILED: d=5 link 55555 passed without 0.7322!'
    print('  [PASS] NC3: Dropping 0.7322 on d=5 link 55555 -> REJECTED as expected.')

    # NC4: (a) Corrupt cyclic shift AND (b) Whitney 2-isomorphism flip via verify_rot_witness directly -> BOTH MUST FAIL!
    cid0, phi0, sg0, shifts0 = rec_d6['embs'][0]
    bad_shifts = [(shifts0[0] + 1) % configs[cid0]['deg'][0]] + shifts0[1:]
    ok_shift, _ = verify_rot_witness(6, [5, 6, 5, 6, 6, 7], configs[cid0], phi0, sg0, bad_shifts, set(rel6))
    assert not ok_shift, 'NC4a FAILED: Corrupted cyclic shift accepted!'

    cfg_194 = [c for c in configs if c['name'] == 'nl0194_r12'][0]
    link_wh = [5, 5, 6, 7, 6, 6, 7]
    phi_whitney = [3, 12, 2, 5, 6, 0, 30, 9, 1, 8]  # Exact abstract induced-subgraph iso, Whitney 2-flipped!
    W_wh = Window2Ball(7, link_wh)
    ins_wh, outs_wh = build_window_instances(W_wh, parts_by_n)
    rel_wh = {c for cs, _ in (ins_wh + outs_wh) for c, _, _ in cs}

    # Build candidate shift lists per vertex a in 0..9 using first interior neighbour slot, then call verify_rot_witness!
    # Also sweep all 7 shifts at hub-mapped vertex I5 so verify_rot_witness is directly tested even when no global shift exists.
    m_wh = cfg_194['m']
    whitney_calls = 0
    for sg_try in (1, -1):
        cand_shifts_per_a = []
        for a in range(m_wh):
            g = cfg_194['deg'][a]
            rc = cfg_194['rot'][a]
            # Pick first interior slot k0 in rot[a] to anchor candidate shifts
            k0, b0 = next((k, val) for k, (kch, val) in enumerate(rc) if kch == 'I')
            # For hub I5 (phi=0), test all 7 shifts explicitly; for others, test shifts matching phi[b0] (or 0 as fallback)
            if a == 5:
                cand_shifts_per_a.append(list(range(g)))
            else:
                # Reconstruct local host rotation vertices to find where phi[b0] sits
                h = phi_whitney[a]
                if 1 <= h <= 7:
                    i_h = h - 1
                    r_h = (
                        [0, 1 + ((i_h - 1) % 7), 8 + ((i_h - 1) % 7)]
                        + [15 + 3 * i_h + (j - 1) for j in range(1, link_wh[i_h] - 5 + 1)]
                        + [8 + i_h, 1 + ((i_h + 1) % 7)]
                    )
                elif 8 <= h < 15:
                    i_h = h - 8
                    r_h = [0, 1 + ((i_h + 1) % 7), 1 + i_h, 0] + [0] * (g - 4)
                else:
                    i_h = (h - 15) // 3
                    r_h = [0, 1 + i_h, 0] + [0] * (g - 3)
                matches = [sh for sh in range(g) if r_h[(sh + sg_try * k0) % g] == phi_whitney[b0]]
                cand_shifts_per_a.append(matches if matches else [0])
        for sh_vec in itertools.product(*cand_shifts_per_a):
            whitney_calls += 1
            ok_wh, _ = verify_rot_witness(7, link_wh, cfg_194, phi_whitney, sg_try, list(sh_vec), rel_wh)
            assert not ok_wh, f'NC4b FAILED: Whitney 2-flipped non-planar occurrence accepted ({sg_try}, {sh_vec})!'
    assert whitney_calls >= 14
    print(f'  [PASS] NC4: Corrupted shift AND Whitney 2-flip via verify_rot_witness ({whitney_calls} calls) -> REJECTED.')

    # NC5: (a) Drop mirror parts AND (b) duplicate one chiral part without its mirror -> multiset involution MUST FAIL!
    parts_no_mirror = [(t, s) for t, s in parts if not t.endswith('m')]
    ok_mc_a, _ = check_mirror_closed(parts_no_mirror)
    assert not ok_mc_a, 'NC5a FAILED: Unmirrored part set passed mirror-closure check!'
    chiral_one = [(t, s) for t, s in parts if t == 'N2_97'][0]
    ok_mc_b, bad_tag_b = check_mirror_closed(list(parts) + [chiral_one])
    assert not ok_mc_b and bad_tag_b in ('N2_97', 'N2_97m'), 'NC5b FAILED: Asymmetric chiral multiplicity passed!'
    print('  [PASS] NC5: Dropping mirrors AND asymmetric chiral part duplication -> multiset involution REJECTED both.')

    # NC6: Perturb Window2Ball.succ orientation AND receiver anchor on concrete sphere triangulation T_mix -> MUST FAIL!
    class BadSuccWindow(Window2Ball):
        def succ(self, x, y):
            if 1 <= x <= self.d:
                rw = self.rot_w[x - 1]
                return rw[(rw.index(y) - 1) % len(rw)]
            return super().succ(x, y)

    ok_bad_succ, _, _ = verify_sphere_discharging_and_windows(T_mix, parts_by_n, win_cls=BadSuccWindow)
    assert not ok_bad_succ, 'NC6a FAILED: Perturbed Window2Ball.succ passed sphere window bracketing!'
    ok_bad_anch, _, _ = verify_sphere_discharging_and_windows(T_mix, parts_by_n, recv_anchor_shift=1)
    assert not ok_bad_anch, 'NC6b FAILED: Perturbed receiver anchor passed global conservation (+120)!'
    print('  [PASS] NC6: Perturbed Window2Ball.succ AND perturbed receiver anchor on sphere T_mix -> REJECTED both.')

    # NC7: Corrupt CGlue admissibleX, foldSafeX, and 2.126 chordB -> ALL THREE MUST FAIL!
    c_rim = [c for c in configs if c['kind'] == 'C' and c['rim_pinned']][0]
    bad_lbl = list(c_rim['lbl'])
    bad_lbl[c_rim['m'] + 1] = bad_lbl[c_rim['m'] + 0]
    assert not verify_admissible_x(c_rim, lbl=bad_lbl), 'NC7a FAILED: Merged ring labels passed admissibleX!'

    # Construct a synthetic D1 fold-unsafe labelling on a ring-14 config by pinning a ring vertex far from another
    # or test foldSafeX when an interior vertex a has un-excluded touched ring vertex t sharing its label:
    t0, a0 = c_rim['eqR'][0]
    # Pick a ring slot t_far not excluded from some other ring neighbour of a0 (or corrupt ring size to 20 so exclB/cycEx fail!)
    c_rim_wide = dict(c_rim)
    c_rim_wide['ring'] = c_rim['ring'] + 10
    wide_eqR = list(c_rim['eqR']) + [[c_rim['ring'] + 5, a0]]
    wide_lbl = list(c_rim['lbl']) + [90 + k for k in range(10)]
    wide_lbl[c_rim['m'] + c_rim['ring'] + 5] = wide_lbl[a0]
    assert not verify_fold_safe_x(c_rim_wide, eqR=wide_eqR, eqI=c_rim['eqI'], lbl=wide_lbl), (
        'NC7b FAILED: D1 fold-unsafe ring pin passed foldSafeX!'
    )

    c_2126 = [c for c in configs if c['name'] == '2.126'][0]
    # Replace R2-I0 with adjacent R1-I0 so R0 and R1 are adjacent slots in rot[I0] -> chordB MUST FAIL!
    bad_eqR_2126 = [[0, 0], [1, 0], [4, 2], [6, 2]]
    bad_lbl_2126 = [0, 1, 2, 3, 0, 0, 4, 5, 2, 6, 2, 7]
    assert not verify_2o126_merge(c_2126, eqR=bad_eqR_2126, eqI=[], lbl=bad_lbl_2126), (
        'NC7c FAILED: Adjacent star spokes R0,R1 on 2.126 passed chordB!'
    )
    print('  [PASS] NC7: Corrupted admissibleX ring labels, D1 fold-unsafe eqR, and 2.126 chordB -> REJECTED all three.')


# ==============================================================================
# 8. Main End-to-End Verification Entrypoint
# ==============================================================================
def main():
    t0 = time.time()
    print('========================================================================')
    print('  Standalone Zero-Dependency 4CT Full-Stack t=0 Verifier (python3 -I)  ')
    print('========================================================================')

    # Phase 1
    print('\n=== Phase 1: 79-Part Discharging Rules, Mirror Involution & Sphere Conservation ===')
    parts = load_and_verify_parts79(os.path.join(DATA_DIR, 'parts79.json'))
    parts_by_n = collections.defaultdict(list)
    for tag, subs in parts:
        parts_by_n[len(subs)].append((tag, subs))
    T_mix, firings_mix = verify_conservation_and_euler(parts_by_n)
    print(
        f'  [PASS] 79 parts (71 RSST + 8 N2): 2-ball local, exact mirror multiset involution, '
        f'sphere conservation = +120 ({firings_mix} rule firings on 48-vertex mixed sphere) & Window2Ball bracketed.'
    )

    # Phase 2
    print('\n=== Phase 2: Configuration Registry, CCW Orientation, CGlue & Provenance ===')
    configs = load_and_verify_registry(os.path.join(DATA_DIR, 'verified_registry.json'))
    tier_counts = collections.Counter(c['tier'] for c in configs)
    subtier_counts = collections.Counter(c['subtier'] for c in configs)
    print(
        f'  [PASS] {len(configs)} configs verified (tiers={dict(tier_counts)}, subtiers={dict(subtier_counts)}; '
        f'CCW R-R 100%; 346/346 C admissibleX+foldSafeX; 2.126 CGlueM PASS).'
    )

    # Phase 3
    print('\n=== Phase 3: Infinite Tail Proof (d >= 15) & Exact 3,125-Window c+ Table ===')
    cp, cmax = compute_and_verify_cplus_tail(parts_by_n, os.path.join(DATA_DIR, 'cert_karp_tail_d15.json'))
    print(f'  [PASS] Recomputed all 3,125 c+ entries (cmax={cmax}, lambda* = 6/1): c_final(u) <= 60 - 4*d <= 0 for all d >= 15.')

    # Phase 4
    print('\n=== Phase 4: Exhaustive Word Completeness & Certificate Replay (d = 5..17) ===')
    used_cfg_ids = set()
    total_all_words_d5_8 = 0
    total_replayed_words = 0
    total_dfs_nodes = 0
    total_witnesses_verified = 0

    for d in range(5, 18):
        td = time.time()
        cert_fn = os.path.join(CERT_DIR, f'cert_d{d}.jsonl')
        assert os.path.exists(cert_fn), f'Missing certificate file {cert_fn}'
        cert_map = {}
        for line in open(cert_fn):
            if not line.strip():
                continue
            obj = json.loads(line)
            lk = obj['link']
            assert lk not in cert_map, f'Duplicate link {lk} in {cert_fn}'
            cert_map[lk] = obj

        # 4a. Exhaustive completeness check
        if d <= 8:
            raw_cnt = 0
            canon_seen = set()
            for w in itertools.product((5, 6, 7, 8, 9), repeat=d):
                raw_cnt += 1
                ck = dihedral_canon_str(w)
                assert ck in cert_map, f'Uncovered link word {w} (canon {ck}) at d={d}!'
                canon_seen.add(ck)
            assert raw_cnt == 5 ** d
            assert canon_seen == set(cert_map.keys()), f'Extra/missing canonical words at d={d}'
            total_all_words_d5_8 += raw_cnt
        else:
            expected_canon = set(enumerate_cplus_canon_words(d, cp, cmax))
            assert expected_canon == set(cert_map.keys()), (
                f'c+ word mismatch at d={d}: missing={len(expected_canon - set(cert_map.keys()))}, '
                f'extra={len(set(cert_map.keys()) - expected_canon)}'
            )
            if d >= 15:
                assert len(expected_canon) == 0

        # 4b. Replay every certified canonical word
        deg_nodes = 0
        deg_wits = 0
        for lk, obj in cert_map.items():
            link = [int(ch) for ch in lk]
            assert len(link) == d and is_dihedral_canon(link)
            W = Window2Ball(d, link)
            ins, outs = build_window_instances(W, parts_by_n)
            base = 10 * (6 - d)
            ub0 = base + len(ins) - sum(1 for cs, o in outs if not cs and not o)

            if 'ub0' in obj:
                assert obj['ub0'] == ub0 and ub0 <= 0, f'Bad ub0 at d={d} link={lk}'
                deg_nodes += 1
                continue

            allc = ins + outs
            rel = sorted({c for cs, _ in allc for c, _, _ in cs}, key=site_key)
            assert obj['vars'] == rel, f'Var order mismatch at d={d} link={lk}'
            rel_set = set(rel)
            vs = [(v, classes_of_verified(v, allc)) for v in rel]

            reqs = []
            for idx, (cid, phi, sg, shifts) in enumerate(obj['embs']):
                cfg = configs[cid]
                assert cfg['tier'] in ('L', 'E2')
                assert not (cfg['source'] == 'SUB_WINDOW' and cfg.get('rim_pinned', False) and cfg['tier'] != 'L'), (
                    f"Forbidden non-Lean rim-pinned SUB_WINDOW {cfg['name']} used at d={d} link={lk}!"
                )
                ok_w, rq = verify_rot_witness(d, link, cfg, phi, sg, shifts, rel_set)
                assert ok_w, f"rotOK witness verification FAILED for {cfg['name']} at d={d} link={lk}!"
                reqs.append((rq, idx))
                used_cfg_ids.add(cid)
                deg_wits += 1

            ok_dfs, st = replay_dfs(base, vs, ins, outs, reqs)
            assert ok_dfs, f'DFS replay FAILED (unkilled positive leaf) at d={d} link={lk}!'
            assert st['ub_leaves'] == obj['ub_leaves'], f'ub_leaves mismatch at d={d} link={lk}'
            assert st['kill_leaves'] == obj['kill_leaves'], f'kill_leaves mismatch at d={d} link={lk}'
            deg_nodes += st['nodes']

        total_replayed_words += len(cert_map)
        total_dfs_nodes += deg_nodes
        total_witnesses_verified += deg_wits
        print(
            f'  [PASS] d={d:2d}: canon_words={len(cert_map):6d} | dfs_nodes={deg_nodes:8d} '
            f'| rotOK_witnesses={deg_wits:6d} | {time.time() - td:5.2f}s'
        )

    assert total_all_words_d5_8 == 5 ** 5 + 5 ** 6 + 5 ** 7 + 5 ** 8 == 487500

    # Phase 5: Negative Controls
    run_negative_controls(parts, parts_by_n, configs, T_mix)

    # Final provenance breakdown of configurations actually used in the proof
    used_by_tier = collections.Counter(configs[cid]['tier'] for cid in used_cfg_ids)
    used_by_subtier = collections.Counter(configs[cid]['subtier'] for cid in used_cfg_ids)
    used_by_src = collections.Counter(configs[cid]['source'] for cid in used_cfg_ids)
    used_rimpin = collections.Counter(
        (configs[cid]['source'], configs[cid]['subtier'])
        for cid in used_cfg_ids
        if configs[cid].get('rim_pinned', False)
    )
    used_whitney = sorted(configs[cid]['name'] for cid in used_cfg_ids if 'whitney_partner_of' in configs[cid])

    elapsed = time.time() - t0
    print('\n========================================================================')
    print(f'ALL POSITIVE CHECKS (d=5..17 + TAIL d>=15) & ALL 7 NEGATIVE CONTROLS PASSED 100% ({elapsed:.2f}s)!')
    print(f'  Exhaustive raw words covered (d=5..8) : {total_all_words_d5_8:,}')
    print(f'  Canonical words replayed (d=5..17)    : {total_replayed_words:,}')
    print(f'  Total symbolic DFS nodes verified     : {total_dfs_nodes:,}')
    print(f'  Total rotOK (RotOcc) witnesses checked: {total_witnesses_verified:,}')
    print(f'  Distinct reducible configs used       : {len(used_cfg_ids)} (tiers={dict(used_by_tier)}, subtiers={dict(used_by_subtier)})')
    print(f'  Used configs by source                : {dict(used_by_src)}')
    print(f'  Used rim-pinned configs (all foldSafe): {sum(used_rimpin.values())} ({dict(used_rimpin)})')
    print(f'  Whitney 2-flip partners used          : {len(used_whitney)} {used_whitney}')
    print('========================================================================')


if __name__ == '__main__':
    main()
