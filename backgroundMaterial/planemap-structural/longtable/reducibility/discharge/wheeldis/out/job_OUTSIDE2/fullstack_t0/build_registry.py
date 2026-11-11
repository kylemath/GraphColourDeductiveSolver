#!/usr/bin/env python3
"""Build self-contained, provenance-audited 79-part discharging rules + [E2]/[L] configuration registry.

Reads read-only upstream sources from GraphColourDeductiveSolver/inspiring-lamport-831744:
1. 71 RSST parts (rsst_drules.v, md5 5ee470f8) + 8 N2 unit parts (RSSTFP_SPEC_v2 §16.2),
   cross-checked byte-for-byte against Lean's exported lean_parts.txt and lean_parts_n2.txt.
2. 582 [E2]/[L] RSST D2/C2cons configurations (unavoidable.conf + rsst_verdicts.txt, cross-checked
   against ST-120R verdicts.tsv and ST-122).
3. 1 [L] RSST configuration 2.126 (rsst003_2o126), closed in Lean 4 with 0 sorry (ST-123/ST-125).
4. Substitute configurations from ST-111 (d9_greedy.tsv + fix_63c8a193fe P20 [L]),
   ST-119 (fw_greedy.tsv L7 + N51 + windows13.tsv), and ST-123 (nl2208_r13 [E2]),
   with full cyclic vertex rotations reconstructed and verified.
"""
import collections
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
os.makedirs(DATA, exist_ok=True)

WT = '/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744'
WD = os.path.join(WT, 'backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis')
PS = os.path.join(WT, 'backgroundMaterial/planemap-structural')

DRULES = os.path.join(WD, 'loop/pubrules/data/rsst_drules.v')
CONF = os.path.join(PS, 'studiointel/routeb/rsst/unavoidable.conf')
RSST_KC = os.path.join(WD, 'loop/k44/rsst.txt')
VERD = os.path.join(WD, 'loop/k44/rsst_verdicts.txt')
NL51_KC = os.path.join(WD, 'loop/studio/opus_check/s39o/nl51_kc.txt')

LEAN_P71 = os.path.join(WD, 'out/job_ST120/b2/lean_parts.txt')
LEAN_PN2 = os.path.join(WD, 'out/job_ST120/b2/lean_parts_n2.txt')

FULL = (5, 9)


def md5_file(fn):
    return hashlib.md5(open(fn, 'rb').read()).hexdigest()


def rng(tok):
    if tok == '*':
        return FULL
    m = re.fullmatch(r'(\d)\?(\d)', tok)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r'(\d)\+', tok)
    if m:
        return (int(m.group(1)), 9)
    m = re.fullmatch(r'(\d)-', tok)
    if m:
        return (5, int(m.group(1)))
    if re.fullmatch(r'\d', tok):
        return (int(tok), int(tok))
    raise ValueError(tok)


def parse_part(body):
    chunks = body.split('$')[1:-1]
    subs = []
    for ch in chunks:
        ch = ch.strip()
        hat = FULL
        fans = []
        m = re.match(r'\[([^\]]*)\]\s*(.*)', ch)
        if m:
            toks = m.group(1).split()
            ch = m.group(2).strip()
            hat = rng(toks[0])
            fans = [rng(t) for t in toks[1:]]
        sp = rng(ch)
        if sp[0] == sp[1] and 6 <= sp[0] <= 8:
            fans = fans + [FULL] * (sp[0] - 5 - len(fans))
        assert len(fans) <= max(0, sp[0] - 5) or not fans, (body, ch)
        subs.append((sp, hat, tuple(fans)))
    return subs


def mirror_part(p):
    n = len(p)
    return [
        (p[(4 - k) % n][0], p[(5 - k) % n][1], tuple(reversed(p[(4 - k) % n][2])))
        for k in range(n)
    ]


def rsub(a, b):
    return b[0] <= a[0] and a[1] <= b[1]


def psub(p, q):
    if len(p) != len(q):
        return False
    for (s1, h1, f1), (s2, h2, f2) in zip(p, q):
        if not (rsub(s1, s2) and rsub(h1, h2)):
            return False
        if f2:
            if len(f1) != len(f2):
                return False
            if not all(rsub(a, b) for a, b in zip(f1, f2)):
                return False
    return True


def fmt_r(r):
    if r == FULL:
        return '*'
    if r[0] == r[1]:
        return '=%d' % r[0]
    if r[1] == 9:
        return '>=%d' % r[0]
    if r[0] == 5:
        return '<=%d' % r[1]
    return 'in%d..%d' % r


def parts_text(parts):
    lines = []
    for tag, p in parts:
        body = '  '.join(
            '%s[%s|%s]' % (fmt_r(s), fmt_r(h), ','.join(fmt_r(f) for f in fs))
            for s, h, fs in p
        )
        lines.append('%s\t%d\t%s' % (tag, len(p), body))
    return lines


def build_parts79():
    txt = open(DRULES).read()
    defs = {}
    for m in re.finditer(r'Definition\s+(\S+)\s*:=\s*Part(.*?)\.\s*\n', txt):
        defs[m.group(1)] = parse_part(m.group(2))
    m = re.search(r'base_drules\s*:\s*drules\s*:=\s*@seqn part (\d+)(.*?)\.', txt, re.S)
    names = m.group(2).split()
    assert len(names) == int(m.group(1)) == 38
    seen = collections.Counter()
    p71 = []
    for nm in names:
        seen[nm] += 1
        tag = nm if seen[nm] == 1 else '%s#%d' % (nm, seen[nm])
        p = defs[nm]
        p71.append((tag, p))
        mp = mirror_part(p)
        if not psub(mp, p):
            p71.append((tag + 'm', mp))
    assert len(p71) == 71

    # Cross-check against Lean's exported lean_parts.txt
    lean71 = [l.rstrip('\n') for l in open(LEAN_P71) if l.strip()]
    assert parts_text(p71) == lean71, 'Mismatch vs Lean lean_parts.txt!'

    # Build the 8 N2 unit parts (RSSTFP_SPEC_v2 §16.2)
    pn2 = []
    for g2, g5 in [(9, 7), (9, 8), (9, 9), (8, 8)]:
        body = ' $ 6 $[5] 5 $ %d $ 6 $[5] 6 $ %d $ 5 $' % (g2, g5)
        p = parse_part(body)
        base = 'N2_%d%d' % (g2, g5)
        pn2.append((base, p))
        mp = mirror_part(p)
        assert not psub(mp, p)
        pn2.append((base + 'm', mp))
    assert len(pn2) == 8

    lean_n2 = [l.rstrip('\n') for l in open(LEAN_PN2) if l.strip()]
    assert parts_text(pn2) == lean_n2, 'Mismatch vs Lean lean_parts_n2.txt!'

    p79 = p71 + pn2
    # Check mirror closure and 2-ball locality on all 79 parts
    for tag, p in p79:
        n = len(p)
        assert 5 <= n <= 8, (tag, n)
        mp = mirror_part(p)
        assert any(psub(mp, q) for _, q in p79), ('Mirror not covered!', tag)
        for j, (sp, hat, fans) in enumerate(p):
            assert 5 <= sp[0] <= sp[1] <= 9
            assert 5 <= hat[0] <= hat[1] <= 9
            if fans:
                assert sp[0] == sp[1] and 6 <= sp[0] <= 8 and len(fans) == sp[0] - 5, (tag, j, sp, fans)

    return p71, pn2, p79


# --- Cyclic rotation reconstruction & verification ---
def _cycle(nbrs, adj):
    nb = list(nbrs)
    if len(nb) < 3:
        return None
    L = {x: [y for y in nb if y != x and y in adj[x]] for x in nb}
    if any(len(v) != 2 for v in L.values()):
        return None
    cyc = [nb[0], L[nb[0]][0]]
    while len(cyc) < len(nb):
        a, b = L[cyc[-1]]
        nx = a if a != cyc[-2] else b
        if nx == cyc[0]:
            return None
        cyc.append(nx)
    return cyc if cyc[0] in L[cyc[-1]] else None


def _orient(rot, edges_order):
    nxt = lambda R, x: R[(R.index(x) + 1) % len(R)]
    done = set()
    bad = 0
    for s in edges_order:
        if s in done or s not in rot:
            continue
        done.add(s)
        Q = collections.deque([s])
        while Q:
            u = Q.popleft()
            for v in rot[u]:
                if v not in rot:
                    continue
                w = nxt(rot[u], v)
                if v in done:
                    if w in rot[v] and nxt(rot[v], w) != u:
                        bad += 1
                    continue
                if w in rot[v] and nxt(rot[v], w) != u:
                    rot[v] = rot[v][::-1]
                done.add(v)
                Q.append(v)
    return bad


def kc_to_entry(line):
    f = line.strip().split()
    name = f[0]
    r, m = int(f[1]), int(f[2])
    rp = f[3].split(';')
    ip = f[4].split(';')
    assert len(rp) == m and len(ip) == m, line
    I = [('I', u) for u in range(m)]
    adj = collections.defaultdict(set)
    for j in range(r):
        a, b = ('R', j), ('R', (j + 1) % r)
        adj[a].add(b)
        adj[b].add(a)
    for u in range(m):
        for j in ([] if rp[u] == '-' else map(int, rp[u].split(','))):
            adj[('I', u)].add(('R', j))
            adj[('R', j)].add(('I', u))
        for w in ([] if ip[u] == '-' else map(int, ip[u].split(','))):
            adj[('I', u)].add(('I', w))
            adj[('I', w)].add(('I', u))
    rot = {}
    for u in I:
        c = _cycle(adj[u], adj)
        assert c is not None, ('Non-cycle link in kc line:', name)
        rot[u] = c
    rr_seeds = []
    for u in I:
        R_ = rot[u]
        has_rr = False
        for k in range(len(R_)):
            a, b = R_[k], R_[(k + 1) % len(R_)]
            if a[0] == 'R' and b[0] == 'R':
                has_rr = True
                if (b[1] - a[1]) % r == r - 1:
                    rot[u] = R_[::-1]
                break
        if has_rr:
            rr_seeds.append(u)
    assert rr_seeds, ('No adjacent R-R slot pair in kc line:', name)
    assert _orient(rot, rr_seeds + I) == 0, ('Orientation inconsistency:', name)
    for u in I:
        R_ = rot[u]
        for k in range(len(R_)):
            a, b = R_[k], R_[(k + 1) % len(R_)]
            if a[0] == 'R' and b[0] == 'R':
                assert (b[1] - a[1]) % r == 1, ('Non-CCW R-R pair in kc_to_entry:', name, u, a, b)
    deg = [len(rot[('I', u)]) for u in range(m)]
    int_adj = [sorted(x[1] for x in rot[('I', u)] if x[0] == 'I') for u in range(m)]
    cyc_rot = [[[x[0], x[1]] for x in rot[('I', u)]] for u in range(m)]
    return {
        'name': name,
        'ring': r,
        'm': m,
        'deg': deg,
        'int_adj': int_adj,
        'rot': cyc_rot,
        'kc_line': line.strip(),
    }


def parse_unavoidable_conf():
    toks = open(CONF).read().split('\n')
    out = []
    t = 0
    while t < len(toks):
        line = toks[t].strip()
        if not line:
            t += 1
            continue
        name = line
        t += 1
        n, r, _a, _b = [int(z) for z in toks[t].split()[:4]]
        t += 1
        cl = [int(z) for z in toks[t].split()]
        t += 1
        adj = {}
        for _ in range(n):
            f = [int(z) for z in toks[t].split()]
            t += 1
            v, dg = f[0], f[1]
            adj[v] = f[2:]
            assert len(adj[v]) == dg
        while t < len(toks) and toks[t].strip():
            t += 1
        m = n - r
        deg = [len(adj[r + 1 + u]) for u in range(m)]
        int_adj = [sorted(x - r - 1 for x in adj[r + 1 + u] if x > r) for u in range(m)]
        cyc_rot = [
            [['I', x - r - 1] if x > r else ['R', x - 1] for x in adj[r + 1 + u]]
            for u in range(m)
        ]
        # Verify consistent orientation among interior vertices and CCW (R_t, R_{t+1}) ring direction
        rot_map = {('I', u): [(x[0], x[1]) for x in cyc_rot[u]] for u in range(m)}
        assert _orient(rot_map, [('I', u) for u in range(m)]) == 0, ('Orientation:', name)
        for u in range(m):
            R_ = rot_map[('I', u)]
            for k in range(len(R_)):
                a, b = R_[k], R_[(k + 1) % len(R_)]
                if a[0] == 'R' and b[0] == 'R':
                    assert (b[1] - a[1]) % r == 1, ('Non-CCW R-R pair in unavoidable.conf:', name, u, a, b)
        cyc_rot = [[[x[0], x[1]] for x in rot_map[('I', u)]] for u in range(m)]
        out.append({
            'name': name,
            'ring': r,
            'm': m,
            'deg': deg,
            'int_adj': int_adj,
            'rot': cyc_rot,
        })
    assert len(out) == 633
    return out


# --- Lean CGlue.lean & CGlueM.lean decidable contraction checks (admissibleX, foldSafeX, 2.126 merge) ---
def parse_x_and_labels(m, r, xstr):
    s = xstr.strip().strip('{}')
    assert s and s != '-', xstr
    eqR = []
    eqI = []
    uf = list(range(m + r))

    def find(x):
        while uf[x] != x:
            uf[x] = uf[uf[x]]
            x = uf[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            if ra < rb:
                uf[rb] = ra
            else:
                uf[ra] = rb

    for tok in s.split(','):
        a_s, b_s = tok.strip().split('-')
        if a_s.startswith('R') and b_s.startswith('I'):
            t, a = int(a_s[1:]), int(b_s[1:])
            eqR.append([t, a])
            union(a, m + t)
        elif a_s.startswith('I') and b_s.startswith('R'):
            a, t = int(a_s[1:]), int(b_s[1:])
            eqR.append([t, a])
            union(a, m + t)
        elif a_s.startswith('I') and b_s.startswith('I'):
            a, b = int(a_s[1:]), int(b_s[1:])
            if a > b:
                a, b = b, a
            eqI.append([a, b])
            union(a, b)
        else:
            raise ValueError(f'Bad X edge token {tok} in {xstr}')

    comp_id = {}
    lbl = []
    for v in range(m + r):
        rv = find(v)
        if rv not in comp_id:
            comp_id[rv] = len(comp_id)
        lbl.append(comp_id[rv])
    return eqR, eqI, lbl


def cfg_ring_int_adj(c):
    m = c['m']
    ring_adj = [sorted(v for k, v in c['rot'][a] if k == 'R') for a in range(m)]
    int_adj = [list(c['int_adj'][a]) for a in range(m)]
    return ring_adj, int_adj


def lean_admissible_x(c, eqR, eqI, lbl, check_ring_distinct=True):
    """Exact translation of CGlue.lean:375-388 admissibleX (or CGlueM.lean admissibleXM when check_ring_distinct=False)."""
    m, r = c['m'], c['ring']
    ring_adj, int_adj = cfg_ring_int_adj(c)
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


def lean_fold_safe_x(c, eqR, eqI, lbl):
    """Exact translation of CGlue.lean:779-838 foldSafeX."""
    m, r = c['m'], c['ring']
    ring_adj, int_adj = cfg_ring_int_adj(c)
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


def lean_merge_checks_2o126(c, eqR, eqI, lbl):
    """Exact translation of CGlueM.lean (ROUTE_I_PLAN.md:93-162): admissibleXM, foldSafeX, coherB, chordB, starB."""
    if not lean_admissible_x(c, eqR, eqI, lbl, check_ring_distinct=False):
        return False
    if not lean_fold_safe_x(c, eqR, eqI, lbl):
        return False
    m, r = c['m'], c['ring']
    ring_adj, int_adj = cfg_ring_int_adj(c)
    touched = sorted({t for t, _ in eqR})
    # coherB: touched s, t with L(m+s) != L(m+t) -> s == t || exclB || cycEx
    for s in touched:
        for t in touched:
            if lbl[m + s] != lbl[m + t] and s != t:
                if not (_excl_b(m, r, ring_adj, int_adj, s, t) or _cyc_ex(m, r, ring_adj, int_adj, s, t)):
                    return False
    # starB: every label class with >=2 touched ring positions is a star centred at a single interior vertex
    by_lbl = collections.defaultdict(list)
    for t in touched:
        by_lbl[lbl[m + t]].append(t)
    eqR_set = {(t, a) for t, a in eqR}
    for lv, ts in by_lbl.items():
        if len(ts) >= 2:
            centres = [a for a in range(m) if lbl[a] == lv and all((t, a) in eqR_set for t in ts)]
            if len(centres) != 1:
                return False
    # chordB: for (s, c_idx), (t, c_idx) in eqR with s != t, neither neighbour of ('R', s) in rot[c_idx] is ('R', t)
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


def main():
    p71, pn2, p79 = build_parts79()
    print(f'Verified 79 parts (71 RSST + 8 N2): mirror-closed, 2-ball local, exact match with Lean B2.')

    # Load 633 RSST configs + verdicts + kc lines
    rsst_confs = parse_unavoidable_conf()
    rsst_kc_lines = [l.strip() for l in open(RSST_KC) if l.strip()]
    assert len(rsst_kc_lines) == 633
    verds = []
    for line in open(VERD):
        f = line.split()
        if f and f[0].startswith('rsst') and len(f) > 2:
            vd = [z for z in f if z.startswith('verdict=')][0].split('=')[1]
            xtok = [z for z in f if z.startswith('X=')][0].split('=', 1)[1].strip('{}')
            verds.append((f[0], vd, xtok, line.strip()))
    assert len(verds) == 633

    # Load ST-120R own-engine recheck verdicts (403 configs), ST-122 Lean 4 CONFIRMED verdicts (191 configs),
    # and ST-113 rsst582_lean_coverage.tsv (179 base Lean configs with exact module routes).
    st120r = {}
    for line in open(os.path.join(WD, 'out/job_ST120R/verdicts.tsv')):
        f = line.rstrip('\n').split('\t')
        st120r[f[0]] = f
        assert f[3] == 'PASS', f

    st122 = {}
    for line in open(os.path.join(WD, 'out/job_ST122/results.tsv')):
        if line.startswith('#') or line.startswith('idx\t') or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        assert f[14] == 'CONFIRMED', f
        st122[f[1]] = f

    in_lean179 = {}
    for line in open(os.path.join(WD, 'out/job_ST113/rsst582_lean_coverage.tsv')):
        if line.startswith('#') or not line.strip():
            continue
        f = line.rstrip('\n').split('\t')
        if f[5] == 'covered':
            assert f[6] != '-', f
            in_lean179[f[0]] = f[6]
    assert len(in_lean179) == 179

    registry = []
    for idx, (c, kcl, (rid, vd, xtok, vline)) in enumerate(zip(rsst_confs, rsst_kc_lines, verds)):
        assert rid.startswith('rsst%03d_' % idx)
        c['rsst_id'] = rid
        c['kc_line'] = kcl
        if vd in ('D2', 'C2cons'):
            if rid in in_lean179:
                tier = 'L'
                route = in_lean179[rid]
                if vd == 'D2':
                    subtier = 'L_full'
                    ev = f'ST-113 base Lean D+Occ glue ({route}) + rsst_verdicts.txt ({vd})'
                else:
                    subtier = 'L_eval'
                    ev = f'ST-113 base Lean cReducible18 ({route}) + rsst_verdicts.txt ({vd}, X={{{xtok}}}) + admissibleX/foldSafeX'
            elif rid in st122:
                tier = 'L'
                row122 = st122[rid]
                if row122[9] == 'yes':
                    subtier = 'L_full'
                    ev = f'ST-122 CONFIRMED Lean 4 with Occ glue ({row122[15]}; {row122[10]}) + rsst_verdicts.txt ({vd})'
                else:
                    subtier = 'L_eval'
                    ev = f'ST-122 CONFIRMED Lean 4 cReducible18 ({row122[15]}) + rsst_verdicts.txt ({vd}, X={{{xtok}}}) + admissibleX/foldSafeX'
            else:
                assert rid in st120r, rid
                tier = 'E2'
                subtier = 'E2'
                ev = f'ST-120R PASS ({st120r[rid][4]}) + rsst_verdicts.txt ({vd})'
            c['source'] = 'RSST_582'
            c['kind'] = 'D' if vd == 'D2' else 'C'
            c['X'] = '-' if vd == 'D2' else xtok
            c['rim_pinned'] = ('R' in xtok) if vd == 'C2cons' else False
            if vd == 'C2cons':
                eqR, eqI, lbl = parse_x_and_labels(c['m'], c['ring'], xtok)
                assert lean_admissible_x(c, eqR, eqI, lbl), ('admissibleX failed:', rid, xtok)
                assert lean_fold_safe_x(c, eqR, eqI, lbl), ('foldSafeX failed:', rid, xtok)
                c['eqR'] = eqR
                c['eqI'] = eqI
                c['lbl'] = lbl
            c['tier'] = tier
            c['subtier'] = subtier
            c['evidence'] = ev
            registry.append(c)
        elif c['name'] == '2.126':
            x2126 = 'R0-I0,R2-I0,R4-I2,R6-I2'
            eqR, eqI, lbl = parse_x_and_labels(c['m'], c['ring'], x2126)
            assert lean_merge_checks_2o126(c, eqR, eqI, lbl), '2.126 merge checks failed!'
            c['source'] = 'RSST_2o126_LEAN'
            c['kind'] = 'C_merge'
            c['X'] = x2126
            c['rim_pinned'] = True
            c['eqR'] = eqR
            c['eqI'] = eqI
            c['lbl'] = lbl
            c['tier'] = 'L'
            c['subtier'] = 'L_full'
            c['evidence'] = 'Lean 4 0-sorry: ST-123 CGlueM.lean + ST-125 colorable_of_occ_2o126 & mirror (commits 0aed53439, fe5e9c528, c86fee03b)'
            registry.append(c)
    assert len(registry) == 583, len(registry)

    # Load nl51_kc dictionary
    nl51 = {}
    for line in open(NL51_KC):
        if line.strip():
            nm = line.split()[0]
            nl51[nm] = line.strip()

    # Load existing [E2] / [L] verification records for nl51 substitutes
    st119_verd = {}
    for line in open(os.path.join(WD, 'out/job_ST119/verdicts.tsv')):
        f = line.rstrip('\n').split('\t')
        assert f[3] == 'PASS', f
        st119_verd[f[0]] = f[4]

    st111_d9 = {}
    for line in open(os.path.join(WD, 'out/job_ST111/in/d9plus/greedy_Drecheck.txt')):
        if line.startswith('nl') and 'D=true' in line:
            nm = line.split()[0]
            assert 'kc:[' in line and 'D=true' in line and 'dfast18:[D=true]' in line, line
            st111_d9[nm] = line.strip()

    st111_nl = {}
    fn_nl_dre = os.path.join(WD, 'out/job_ST111/in/results/nl51_Drecheck.txt')
    if os.path.exists(fn_nl_dre):
        for line in open(fn_nl_dre):
            if line.startswith('nl') and 'D=true' in line:
                st111_nl[line.split()[0]] = line.strip()

    L7_NAMES = {'nl0004_r8', 'nl0078_r11', 'nl0008_r9', 'nl0050_r10', 'nl2837_r11', 'nl0018_r11', 'nl0067_r10'}

    # Collect union of substitute nl configs from fw_greedy.tsv + d9_greedy.tsv + nl2208_r13
    sub_nl = []
    seen_sub = set()
    for fn, col in [
        (os.path.join(WD, 'out/job_ST119/in/results/fw_greedy.tsv'), 2),
        (os.path.join(WD, 'out/job_ST111/in/d9plus/d9_greedy.tsv'), 1),
    ]:
        for i, line in enumerate(open(fn)):
            if i == 0 or not line.strip():
                continue
            nm = line.rstrip('\n').split('\t')[col]
            if nm not in seen_sub:
                seen_sub.add(nm)
                sub_nl.append(nm)
    if 'nl2208_r13' not in seen_sub:
        seen_sub.add('nl2208_r13')
        sub_nl.append('nl2208_r13')

    # Also include exact Whitney 2-isomorphism partners in nl51_kc.txt:
    # upstream fwsub.py / r2_scheck.py matched abstract induced subgraphs without cyclic rotations (rotOK),
    # so configurations with a 2-vertex interior cut need their planar Whitney 2-flip partners under strict RotOcc!
    def _graph_sig(e):
        return (
            e['m'],
            tuple(sorted((e['deg'][u], tuple(sorted(e['deg'][v] for v in e['int_adj'][u]))) for u in range(e['m']))),
        )

    def _is_abstract_iso(a, b):
        if a['m'] != b['m']:
            return False
        m = a['m']
        ea = [set(x) for x in a['int_adj']]
        eb = [set(x) for x in b['int_adj']]
        phi = [-1] * m
        used = set()

        def rec(k):
            if k == m:
                return True
            for t in range(m):
                if t in used or a['deg'][k] != b['deg'][t]:
                    continue
                if any((y in ea[k]) != (phi[y] in eb[t]) for y in range(k)):
                    continue
                phi[k] = t
                used.add(t)
                if rec(k + 1):
                    return True
                used.remove(t)
                phi[k] = -1
            return False

        return rec(0)

    base_sub_entries = [kc_to_entry(nl51[nm]) for nm in sub_nl]
    by_sig = collections.defaultdict(list)
    for c_base in base_sub_entries:
        by_sig[_graph_sig(c_base)].append(c_base)

    whitney_of = {}
    for nm_cand, kcl_cand in nl51.items():
        if nm_cand in seen_sub:
            continue
        e_cand = kc_to_entry(kcl_cand)
        cands = by_sig.get(_graph_sig(e_cand), ())
        for c_base in cands:
            if _is_abstract_iso(e_cand, c_base):
                seen_sub.add(nm_cand)
                sub_nl.append(nm_cand)
                whitney_of[nm_cand] = c_base['name']
                break
    print(f'Included {len(whitney_of)} exact Whitney 2-isomorphism partners from nl51_kc.txt.')

    # Load rim-free D/C windows from ST-119 s4..s7.tsv + vc_fw_windows.tsv (for Whitney-flipped window coverage)
    vc_rimfree_ok = set()
    for i_vc, l_vc in enumerate(open(os.path.join(WD, 'out/job_ST119/in/results/vc_fw_windows.tsv'))):
        if i_vc == 0 or not l_vc.strip():
            continue
        f_vc = l_vc.rstrip('\n').split('\t')
        if f_vc[23] == 'True' and f_vc[24] == 'True' and 'R' not in f_vc[7]:
            vc_rimfree_ok.add(f_vc[0])

    rimfree_win_pool = {}
    for fn_s in sorted(glob.glob(os.path.join(WD, 'out/job_ST119/in/results/s*.tsv'))):
        if fn_s.endswith('.log'):
            continue
        for l_s in open(fn_s):
            f_s = l_s.rstrip('\n').split('\t')
            if len(f_s) < 12:
                continue
            nm_s, kind_s, x_s, v2_s, kcl_s = f_s[0], f_s[4], f_s[6], f_s[10], f_s[11]
            if kind_s == 'D' and 'dfast18:D' in v2_s:
                rimfree_win_pool[nm_s] = ('D', '-', kcl_s)
            elif kind_s == 'C' and 'cfast:C-REDUCIBLE' in v2_s and nm_s in vc_rimfree_ok and 'R' not in x_s:
                rimfree_win_pool[nm_s] = ('C', x_s, kcl_s)

    disc_fn = os.path.join(DATA, 'discovered_whitney_subs.txt')
    whitney_masked = set()
    disc_wins = []
    if os.path.exists(disc_fn):
        for line in open(disc_fn):
            nm = line.strip()
            if not nm:
                continue
            if nm in nl51 and nm not in seen_sub:
                seen_sub.add(nm)
                sub_nl.append(nm)
                whitney_masked.add(nm)
            elif nm in rimfree_win_pool and nm not in disc_wins:
                disc_wins.append(nm)
        print(
            f'Included {len(whitney_masked)} Whitney-masked D-substitutes and {len(disc_wins)} rim-free windows '
            f'from data/discovered_whitney_subs.txt.'
        )

    unchecked_nl = []
    for nm in sub_nl:
        kcl = nl51[nm]
        e = kc_to_entry(kcl)
        e['source'] = 'SUB_NL51'
        e['kind'] = 'D'
        e['X'] = '-'
        e['rim_pinned'] = False
        if nm in whitney_of:
            e['whitney_partner_of'] = whitney_of[nm]
        if nm in whitney_masked:
            e['whitney_masked_sub'] = True
        if nm in L7_NAMES:
            e['tier'] = 'L'
            e['subtier'] = 'L_full'
            e['evidence'] = 'Lean L7 D+Occ glue (0 sorry) + ST-111 greedy_Drecheck (kc D=true, dfast18 D=true)'
        elif nm in st119_verd:
            e['tier'] = 'E2'
            e['subtier'] = 'E2'
            e['evidence'] = f'ST-119 verdicts.tsv PASS ({st119_verd[nm]})'
        elif nm in st111_d9:
            e['tier'] = 'E2'
            e['subtier'] = 'E2'
            e['evidence'] = f'ST-111 greedy_Drecheck.txt PASS ({st111_d9[nm]})'
        elif nm in st111_nl:
            e['tier'] = 'E2'
            e['subtier'] = 'E2'
            e['evidence'] = f'ST-111 nl51_Drecheck.txt PASS ({st111_nl[nm]})'
        elif nm == 'nl2208_r13':
            kc_out = open(os.path.join(WD, 'out/job_ST123/chk/kc.out')).read().strip()
            df_out = open(os.path.join(WD, 'out/job_ST123/chk/df18.out')).read().strip()
            assert 'D=true' in kc_out and 'D=true' in df_out
            e['tier'] = 'E2'
            e['subtier'] = 'E2'
            e['evidence'] = 'ST-123 chk PASS (kc D=true, dfast18 D=true)'
        else:
            unchecked_nl.append((nm, kcl, e))
            continue
        registry.append(e)

    # If any nl51 substitute was from Round 11's 39-config check outside those 3 files, verify on kc + dfast18 right now!
    if unchecked_nl:
        print(f'Running direct [E2] check (kc -C + dfast18) on {len(unchecked_nl)} Round-11 nl51 configs...')
        chk_dir = os.path.join(DATA, 'e2_recheck_nl')
        os.makedirs(chk_dir, exist_ok=True)
        kc_bin = os.path.join(WD, 'loop/kc/kc')
        df_bin = os.path.join(WD, 'out/job52/dfast18')
        for nm, kcl, e in unchecked_nl:
            outfn = os.path.join(chk_dir, f'{nm}.out')
            if os.path.exists(outfn):
                txt_out = open(outfn).read()
                assert 'D=true' in txt_out.split('== dfast18')[0] and 'D=true' in txt_out.split('== dfast18')[1]
            else:
                infn = os.path.join(chk_dir, f'{nm}.in')
                open(infn, 'w').write(kcl + '\n')
                a = subprocess.run(['nice', '-n', '15', kc_bin, '-t', '600', '-C', infn], capture_output=True, text=True).stdout
                b = subprocess.run(['nice', '-n', '15', df_bin, infn], capture_output=True, text=True).stdout
                open(outfn, 'w').write(f'== kc\n{a}== dfast18\n{b}')
                assert 'D=true' in a and 'D=true' in b, (nm, a, b)
            e['tier'] = 'E2'
            e['subtier'] = 'E2'
            e['evidence'] = f'Direct E2 recheck data/e2_recheck_nl/{nm}.out (kc D=true, dfast18 D=true)'
            registry.append(e)
        print(f'All {len(unchecked_nl)} Round-11 nl51 configs passed kc D=true + dfast18 D=true!')

    # Add the verified windows from windows13.tsv
    for line in open(os.path.join(WD, 'out/job_ST119/windows13.tsv')):
        nm, kind, xstr, kcl = line.rstrip('\n').split('\t')
        x_clean = '-' if kind == 'D' else xstr.strip('{}')
        e = kc_to_entry(kcl)
        e['source'] = 'SUB_WINDOW'
        e['kind'] = kind
        e['X'] = x_clean
        e['rim_pinned'] = ('R' in x_clean) if kind == 'C' else False
        if kind == 'C':
            eqR, eqI, lbl = parse_x_and_labels(e['m'], e['ring'], x_clean)
            assert lean_admissible_x(e, eqR, eqI, lbl), ('admissibleX failed:', nm, x_clean)
            assert lean_fold_safe_x(e, eqR, eqI, lbl), ('foldSafeX failed:', nm, x_clean)
            e['eqR'] = eqR
            e['eqI'] = eqI
            e['lbl'] = lbl
        if nm == 'fix_63c8a193fe':
            e['tier'] = 'L'
            e['subtier'] = 'L_full'
            e['evidence'] = 'ST-111 S1 PASS + Lean CK5PS1 / HCK5P20 C+Occ glue (0 sorry, kc + cfast C-REDUCIBLE) + admissibleX/foldSafeX'
        else:
            assert nm in st119_verd, nm
            e['tier'] = 'E2'
            e['subtier'] = 'E2'
            e['evidence'] = f'ST-119 verdicts.tsv PASS ({st119_verd[nm]}) + admissibleX/foldSafeX PASS'
        registry.append(e)

    win_known = {c['name'] for c in registry if c['source'] == 'SUB_WINDOW'}
    if disc_wins:
        wchk_dir = os.path.join(DATA, 'e2_recheck_win')
        os.makedirs(wchk_dir, exist_ok=True)
        kc_bin = os.path.join(WD, 'loop/kc/kc')
        df_bin = os.path.join(WD, 'out/job52/dfast18')
        cf_bin = os.path.join(WD, '../studio15/cfast')
        for nm in disc_wins:
            if nm in win_known:
                continue
            kind, xstr, kcl = rimfree_win_pool[nm]
            x_clean = '-' if kind == 'D' else xstr.strip('{}')
            assert 'R' not in x_clean
            e = kc_to_entry(kcl)
            e['source'] = 'SUB_WINDOW'
            e['kind'] = kind
            e['X'] = x_clean
            e['rim_pinned'] = False
            e['whitney_masked_sub'] = True
            if kind == 'C':
                eqR, eqI, lbl = parse_x_and_labels(e['m'], e['ring'], x_clean)
                assert lean_admissible_x(e, eqR, eqI, lbl), ('admissibleX failed:', nm, x_clean)
                assert lean_fold_safe_x(e, eqR, eqI, lbl), ('foldSafeX failed:', nm, x_clean)
                e['eqR'] = eqR
                e['eqI'] = eqI
                e['lbl'] = lbl
            outfn = os.path.join(wchk_dir, f'{nm}.out')
            if not os.path.exists(outfn):
                infn = os.path.join(wchk_dir, f'{nm}.in')
                open(infn, 'w').write(kcl + '\n')
                if kind == 'D':
                    a = subprocess.run(['nice', '-n', '15', kc_bin, '-t', '600', '-C', infn], capture_output=True, text=True).stdout
                    b = subprocess.run(['nice', '-n', '15', df_bin, infn], capture_output=True, text=True).stdout
                else:
                    xfn = os.path.join(wchk_dir, f'{nm}.x')
                    open(xfn, 'w').write(f'{nm} {{{x_clean}}}\n')
                    a = subprocess.run(['nice', '-n', '15', kc_bin, '-t', '600', '-C', '-x', xfn, infn], capture_output=True, text=True).stdout
                    b = subprocess.run(['nice', '-n', '15', cf_bin, infn, '--fixed', x_clean], capture_output=True, text=True).stdout
                open(outfn, 'w').write(f'== kc\n{a}== second_engine\n{b}')
            txt_w = open(outfn).read()
            p_kc, p_sec = txt_w.split('== second_engine')
            if kind == 'D':
                assert 'D=true' in p_kc and 'D=true' in p_sec, (nm, txt_w)
            else:
                assert 'adm=yes leftover 0' in p_kc and 'C-REDUCIBLE' in p_kc, (nm, p_kc)
                assert 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in p_sec, (nm, p_sec)
            e['tier'] = 'E2'
            e['subtier'] = 'E2'
            e['evidence'] = f'Direct E2 recheck data/e2_recheck_win/{nm}.out + admissibleX/foldSafeX PASS (rim=no)'
            registry.append(e)
        print(f'Verified {len(disc_wins)} Whitney-flipped rim-free windows on two engines!')

    # Sanity-check provenance strings and C-contraction fields across the entire registry
    for c in registry:
        assert '(-)' not in c['evidence'] and 'to confirm' not in c['evidence'].lower(), c
        assert c['subtier'] in ('L_full', 'L_eval', 'E2'), c
        if c['kind'] in ('C', 'C_merge'):
            assert 'eqR' in c and 'eqI' in c and 'lbl' in c, c['name']

    # Save parts79.json and verified_registry.json
    parts_json = {
        'meta': {
            'rsst_drules_md5': md5_file(DRULES),
            'lean_parts71_md5': md5_file(LEAN_P71),
            'lean_parts_n2_md5': md5_file(LEAN_PN2),
            'count_rsst': len(p71),
            'count_n2': len(pn2),
            'count_total': len(p79),
        },
        'parts': [
            {
                'tag': tag,
                'hub': len(p),
                'target': 2,
                'amount': 1,
                'subs': [[list(s), list(h), [list(f) for f in fs]] for s, h, fs in p],
            }
            for tag, p in p79
        ],
    }
    json.dump(parts_json, open(os.path.join(DATA, 'parts79.json'), 'w'), indent=1)

    by_src = collections.Counter(c['source'] for c in registry)
    by_tier = collections.Counter(c['tier'] for c in registry)
    by_subtier = collections.Counter(c['subtier'] for c in registry)
    by_rimpin = collections.Counter((c['source'], c.get('rim_pinned', False)) for c in registry)
    reg_json = {
        'meta': {
            'unavoidable_conf_md5': md5_file(CONF),
            'rsst_verdicts_md5': md5_file(VERD),
            'nl51_kc_md5': md5_file(NL51_KC),
            'count_total': len(registry),
            'by_source': dict(by_src),
            'by_tier': dict(by_tier),
            'by_subtier': dict(by_subtier),
            'rim_pinned_counts': {f'{k[0]}:{k[1]}': v for k, v in sorted(by_rimpin.items())},
        },
        'configs': registry,
    }
    json.dump(reg_json, open(os.path.join(DATA, 'verified_registry.json'), 'w'), separators=(',', ':'))
    print(
        f'Wrote parts79.json (79 parts) and verified_registry.json '
        f'({len(registry)} configs: {dict(by_src)}, tiers={dict(by_tier)}, subtiers={dict(by_subtier)}).'
    )

    # Also write flat text engine_input.txt for fast_unavoidable.cpp (zero custom JSON parsing needed in C++)
    with open(os.path.join(DATA, 'engine_input.txt'), 'w') as fo:
        fo.write(f'PARTS {len(p79)}\n')
        for tag, p in p79:
            fo.write(f'{tag} {len(p)}\n')
            for sp, hat, fs in p:
                fo.write(f'{sp[0]} {sp[1]} {hat[0]} {hat[1]} {len(fs)}')
                for a, b in fs:
                    fo.write(f' {a} {b}')
                fo.write('\n')
        fo.write(f'CONFIGS {len(registry)}\n')
        for idx, c in enumerate(registry):
            rp_flag = 1 if c.get('rim_pinned', False) else 0
            fo.write(f"{idx} {c['name']} {c['source']} {c['kind']} {c['tier']} {rp_flag} {c['ring']} {c['m']}\n")
            for u in range(c['m']):
                rot_u = c['rot'][u]
                fo.write(f'{len(rot_u)}')
                for kind_ch, val in rot_u:
                    fo.write(f' {0 if kind_ch == "I" else 1} {val}')
                fo.write('\n')
    print('Wrote data/engine_input.txt.')

    if '--export-pool' in sys.argv:
        pool_fn = os.path.join(DATA, 'nl51_pool.txt')
        pool_entries = [('SUB_NL51', 'D', kc_to_entry(kcl)) for kcl in nl51.values()]
        for nm_w, (kind_w, _x_w, kcl_w) in sorted(rimfree_win_pool.items()):
            pool_entries.append(('SUB_WINDOW', kind_w, kc_to_entry(kcl_w)))
        with open(pool_fn, 'w') as fp:
            fp.write(f'POOL {len(pool_entries)}\n')
            for idx, (src_p, kind_p, c) in enumerate(pool_entries):
                fp.write(f"{idx} {c['name']} {src_p} {kind_p} E2 0 {c['ring']} {c['m']}\n")
                for u in range(c['m']):
                    rot_u = c['rot'][u]
                    fp.write(f'{len(rot_u)}')
                    for kind_ch, val in rot_u:
                        fp.write(f' {0 if kind_ch == "I" else 1} {val}')
                    fp.write('\n')
        print(f'Wrote {len(pool_entries)} candidate D + rim-free window configs to {pool_fn}.')


if __name__ == '__main__':
    main()
