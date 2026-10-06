#!/usr/bin/env python3
"""WP20 independent checker.  Written from WP20-D1-declaration.md and
WP20-output-format.md only.  Standard library only.

usage:  d1_check.py OUTPUT.json PLANTRI_STDOUT DECLARATION.md [--workers K] [--all]
        d1_check.py --selftest ORDER [--plantri PATH] [--workers K]

Two independent code paths live here:
  * BULK  (bitmask colour classes, union-find over all colourings) computes every
    per-vertex statistic;
  * WITNESS (plain colour lists, plain BFS, nothing shared with BULK except the
    plantri parser) re-verifies every witness from scratch.
Exit status 0 only if there is no mismatch and no fault.
"""
import sys, os, json, hashlib, copy, argparse, subprocess, multiprocessing as mp

PLANTRI_DEFAULT = ("/private/tmp/claude-501/-Users-fulkanjou-GraphColour/"
                   "28402cc5-3e09-4c31-94e9-5ae923a5533c/scratchpad/plantri58/plantri")
EXPECTED_INPUT = {}   # WP21: the expected input hash, if any, is given with --expect-input-sha
EXPECT_SHA = [None]
SAMPLE_MOD = [20]
P_CAP = 200000
BIG = 1 << 60


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# ----------------------------------------------------------------- plantri
def parse_plantri(path):
    """returns list of (ascii_line, n, rot) ; rot[v] = list of neighbours in plantri order"""
    graphs = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tok = line.split()
            n = int(tok[0])
            lists = tok[1].split(",")
            assert len(lists) == n, "bad ascii line"
            rot = [[ord(ch) - 97 for ch in s] for s in lists]
            graphs.append((line, n, rot))
    return graphs


def sample_index(i):
    return int(hashlib.sha256(("WP21-" + str(i)).encode()).hexdigest()[:8], 16) % SAMPLE_MOD[0] == 0


def triangulation_ok(n, rot):
    """independent validity check: simple, symmetric, min degree 5, 3n-6 edges, every directed
    edge in exactly one triangular face, 2n-4 faces."""
    adj = [set(r) for r in rot]
    if any(len(adj[v]) != len(rot[v]) or v in adj[v] or len(rot[v]) < 5 for v in range(n)):
        return False
    if any(v not in adj[w] for v in range(n) for w in rot[v]):
        return False
    if sum(len(r) for r in rot) != 2 * (3 * n - 6):
        return False
    seen, faces = set(), 0
    for u in range(n):
        for v in rot[u]:
            if (u, v) in seen:
                continue
            a, b, length = u, v, 0
            while (a, b) not in seen:
                seen.add((a, b))
                length += 1
                d = len(rot[b])
                c = rot[b][(rot[b].index(a) + 1) % d]
                a, b = b, c
            if length != 3:
                return False
            faces += 1
    return faces == 2 * n - 4


# ================================================================== BULK path
def canon(m4):
    return tuple(sorted(m4, key=lambda m: (m & -m) or BIG))


def enumerate_colourings(adjm, verts):
    """all proper 4-colourings (up to renaming) of the graph induced on verts,
    as canonical tuples of 4 class bitmasks (sorted by lowest vertex, empties last)."""
    verts = list(verts)
    placed = 0
    order = []
    remaining = set(verts)
    while remaining:
        best = max(remaining, key=lambda v: (bin(adjm[v] & placed).count("1"), -v))
        order.append(best)
        placed |= 1 << best
        remaining.discard(best)
    out = []
    cls = [0, 0, 0, 0]
    L = len(order)
    nbm = [adjm[v] for v in order]
    bits = [1 << v for v in order]

    def rec(i, used):
        if i == L:
            out.append(canon(cls))
            return
        a = nbm[i]
        b = bits[i]
        for k in range(min(used + 1, 4)):
            if cls[k] & a == 0:
                cls[k] |= b
                rec(i + 1, used + 1 if k == used else used)
                cls[k] ^= b
    rec(0, 0)
    return out


def kempe_nbrs(key, adjm):
    res = set()
    for a in range(4):
        for b in range(a + 1, 4):
            A, B = key[a], key[b]
            S = A | B
            rem = S
            while rem:
                seed = rem & -rem
                comp = seed
                fr = seed
                while fr:
                    v = fr & -fr
                    fr ^= v
                    nb = adjm[v.bit_length() - 1] & S & ~comp
                    comp |= nb
                    fr |= nb
                rem &= ~comp
                new = list(key)
                new[a] = (A & ~comp) | (comp & B)
                new[b] = (B & ~comp) | (comp & A)
                res.add(canon(new))
    return res


def key_to_state(key, n, x):
    col = [4] * n
    for k, m in enumerate(key):
        v = 0
        while m:
            if m & 1:
                col[v] = k
            m >>= 1
            v += 1
    return col


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        p = self.p
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.p[a] = b


def analyse_vertex(n, rot, adjm, x):
    ring = rot[x]
    assert len(ring) == 5
    ringmask = 0
    for r in ring:
        ringmask |= 1 << r
    legal = []
    for j in range(5):
        rj = ring[j]
        c1 = ring[(j + 2) % 5]
        c2 = ring[(j + 3) % 5]
        if not (adjm[rj] >> c1 & 1) and not (adjm[rj] >> c2 & 1):
            legal.append(j)
    xb = 1 << x
    adj_tx = [adjm[v] & ~xb for v in range(n)]
    verts_tx = [v for v in range(n) if v != x]
    states = enumerate_colourings(adj_tx, verts_tx)
    idx = {k: i for i, k in enumerate(states)}
    N = len(states)
    nbrs = []
    for k in states:
        nbrs.append([idx[q] for q in kempe_nbrs(k, adj_tx)])
    # fan data: classes of colourings of G_j
    fan = {}
    locked = 0
    for j in legal:
        rj = ring[j]
        adjg = list(adjm)
        adjg[x] &= ~(1 << rj)
        adjg[rj] &= ~xb
        gcols = enumerate_colourings(adjg, range(n))
        gidx = {k: i for i, k in enumerate(gcols)}
        uf = UF(len(gcols))
        for i, k in enumerate(gcols):
            for q in kempe_nbrs(k, adjg):
                uf.union(i, gidx[q])
        free = {}
        for i, k in enumerate(gcols):
            r = uf.find(i)
            same = any((m >> x & 1) and (m >> rj & 1) for m in k)
            if r not in free:
                free[r] = False
            if not same:
                free[r] = True
        locked += sum(1 for v in free.values() if not v)
        fan[j] = (gidx, uf, free)

    unfilled = []
    adm = []
    for i, k in enumerate(states):
        cnt = [bin(m & ringmask).count("1") for m in k]
        unf = all(c >= 1 for c in cnt)
        unfilled.append(unf)
        a = []
        if unf:
            for j in legal:
                rj = ring[j]
                for t in range(4):
                    if k[t] >> rj & 1:
                        if cnt[t] == 1:
                            a.append((j, t))
        adm.append(a)

    def separable(i, j, t):
        g = list(states[i])
        g[t] |= xb
        gidx, uf, free = fan[j]
        return free[uf.find(gidx[canon(g)])]

    good = [False] * N
    hasadm = [False] * N
    for i in range(N):
        if unfilled[i] and adm[i]:
            hasadm[i] = True
            good[i] = any(separable(i, j, t) for (j, t) in adm[i])

    unfilled_total = sum(unfilled)
    nstates = sum(hasadm)
    nolegal = unfilled_total - nstates
    bad = [i for i in range(N) if hasadm[i] and not good[i]]

    depth = {"1": 0, "2": 0, "3": 0, ">3": 0}
    fnb = 0
    d1 = []
    depth_of = {}
    for i in bad:
        if any(is_filled(states[q], ringmask) for q in nbrs[i]):
            fnb += 1
        seen = {i}
        front = [i]
        dd = ">3"
        for lev in (1, 2, 3):
            nxt = []
            for u in front:
                for q in nbrs[u]:
                    if q not in seen:
                        seen.add(q)
                        nxt.append(q)
            if any(good[q] for q in nxt):
                dd = str(lev)
                break
            front = nxt
        depth[dd] += 1
        depth_of[i] = dd
        if dd != "1":
            d1.append(i)

    uf = UF(N)
    for i in range(N):
        for q in nbrs[i]:
            uf.union(i, q)
    size = {}
    hasfilled = {}
    for i in range(N):
        r = uf.find(i)
        size[r] = size.get(r, 0) + 1
        if is_filled(states[i], ringmask):
            hasfilled[r] = True
    pk = []
    pcap = 0
    for i in range(N):
        if unfilled[i]:
            r = uf.find(i)
            if size[r] > P_CAP:
                pcap += 1
            elif not hasfilled.get(r):
                pk.append(i)

    rec = {"x": x, "status": "capped" if pcap else "complete",
           "unfilled_total": unfilled_total, "states": nstates, "no_legal_fan": nolegal,
           "sep_bad": len(bad), "depth": depth, "filled_neighbour_for_bad": fnb,
           "d1_kills": len(d1), "p_kills": len(pk), "p_capped": pcap,
           "locked_classes": locked, "legal_fans": list(legal)}
    wit = {"sep_bad": [{"index": None, "x": x, "state": key_to_state(states[i], n, x),
                        "depth": depth_of[i]} for i in bad],
           "d1_kills": [{"index": None, "x": x, "state": key_to_state(states[i], n, x)} for i in d1],
           "p_kills": [{"index": None, "x": x, "state": key_to_state(states[i], n, x)} for i in pk]}
    return rec, wit


def nbr_filled_check(k, ringmask):
    return ()


def is_filled(k, ringmask):
    return any(m & ringmask == 0 for m in k)


def adjmasks(n, rot):
    adjm = [0] * n
    for v in range(n):
        for w in rot[v]:
            adjm[v] |= 1 << w
    return adjm


def analyse_graph(n, rot):
    adjm = adjmasks(n, rot)
    verts, wits = [], {"sep_bad": [], "d1_kills": [], "p_kills": []}
    for x in range(n):
        if len(rot[x]) == 5:
            r, w = analyse_vertex(n, rot, adjm, x)
            verts.append(r)
            for kk in wits:
                wits[kk].extend(w[kk])
    return verts, wits


# ============================================================== WITNESS path
def t_canon(col):
    m, out = {}, []
    for c in col:
        if c == 4:
            out.append(4)
        else:
            if c not in m:
                m[c] = len(m)
            out.append(m[c])
    return tuple(out)


def t_proper(col, adjl):
    return all(col[v] == 4 or col[w] == 4 or col[v] != col[w]
               for v in range(len(col)) for w in adjl[v])


def t_kempe(col, adjl):
    n = len(col)
    for a in range(4):
        for b in range(a + 1, 4):
            seen = [False] * n
            for s in range(n):
                if seen[s] or col[s] not in (a, b):
                    continue
                comp, st = [s], [s]
                seen[s] = True
                while st:
                    u = st.pop()
                    for w in adjl[u]:
                        if not seen[w] and col[w] in (a, b):
                            seen[w] = True
                            comp.append(w)
                            st.append(w)
                new = list(col)
                for u in comp:
                    new[u] = a + b - col[u]
                yield t_canon(new)


class WGraph:
    def __init__(self, n, rot, x):
        self.n, self.rot, self.x = n, rot, x
        self.adj = [list(r) for r in rot]
        self.adj_tx = [[w for w in self.adj[v] if w != x] if v != x else [] for v in range(n)]
        self.ring = rot[x]
        self.edge = set((v, w) for v in range(n) for w in rot[v])
        self.legal = [j for j in range(5)
                      if (self.ring[j], self.ring[(j + 2) % 5]) not in self.edge
                      and (self.ring[j], self.ring[(j + 3) % 5]) not in self.edge]
        self.gadj = {}
        self.sepcache = {}
        self.goodcache = {}

    def g_adj(self, j):
        if j not in self.gadj:
            rj = self.ring[j]
            a = [list(l) for l in self.adj]
            a[self.x].remove(rj)
            a[rj].remove(self.x)
            self.gadj[j] = a
        return self.gadj[j]

    def admitting(self, st):
        cs = [st[r] for r in self.ring]
        if len(set(cs)) != 4:
            return None  # filled
        return [j for j in self.legal if cs.count(cs[j]) == 1]

    def separable(self, st, j):
        key = (st, j)
        if key in self.sepcache:
            return self.sepcache[key]
        rj, x = self.ring[j], self.x
        start = list(st)
        start[x] = st[rj]
        start = t_canon(start)
        adj = self.g_adj(j)
        seen = {start}
        stack = [start]
        res = False
        while stack and not res:
            c = stack.pop()
            if c[x] != c[rj]:
                res = True
                break
            for q in t_kempe(c, adj):
                if q not in seen:
                    seen.add(q)
                    stack.append(q)
        self.sepcache[key] = res
        return res

    def good(self, st):
        if st in self.goodcache:
            return self.goodcache[st]
        a = self.admitting(st)
        r = bool(a) and any(self.separable(st, j) for j in a)
        self.goodcache[st] = r
        return r

    def nbrs(self, st):
        return set(t_kempe(st, self.adj_tx))


def verify_state_basic(W, st):
    errs = []
    n, x = W.n, W.x
    if len(st) != n or st[x] != 4:
        return ["state length/hole entry wrong"]
    if any(c not in (0, 1, 2, 3) for i, c in enumerate(st) if i != x):
        return ["state entries not in 0..3"]
    if t_canon(st) != tuple(st):
        errs.append("state not canonical")
    if not t_proper(st, W.adj_tx):
        errs.append("state not proper on T-x")
    return errs


def depth_of_state(W, st):
    seen = {st}
    front = [st]
    for lev in (1, 2, 3):
        nxt = []
        for u in front:
            for q in W.nbrs(u):
                if q not in seen:
                    seen.add(q)
                    nxt.append(q)
        if any(W.good(q) for q in nxt):
            return str(lev)
        front = nxt
    return ">3"


def verify_witnesses(n, rot, index, wits):
    """returns list of error strings"""
    msgs = []
    cache = {}
    for kind in ("sep_bad", "d1_kills", "p_kills"):
        for w in wits.get(kind, []):
            tag = "witness %s graph %s x=%s" % (kind, index, w.get("x"))
            x = w["x"]
            if not isinstance(x, int) or not (0 <= x < n) or len(rot[x]) != 5:
                msgs.append(tag + ": x is not a degree-5 vertex")
                continue
            if x not in cache:
                cache[x] = WGraph(n, rot, x)
            W = cache[x]
            st = tuple(w["state"])
            e = verify_state_basic(W, st)
            if e:
                msgs.append(tag + ": " + "; ".join(e))
                continue
            adm = W.admitting(st)
            if adm is None:
                msgs.append(tag + ": ring is not 4-coloured (filled state)")
                continue
            if kind in ("sep_bad", "d1_kills"):
                if not adm:
                    msgs.append(tag + ": no legal admitting fan")
                    continue
                if W.good(st):
                    msgs.append(tag + ": state is separable, not SEP-bad")
                    continue
                d = depth_of_state(W, st)
                if kind == "sep_bad":
                    if str(w.get("depth")) != d:
                        msgs.append(tag + ": stated depth %r, recomputed %s" % (w.get("depth"), d))
                else:
                    if d == "1":
                        msgs.append(tag + ": D1 kill claimed but a pure neighbour is good (depth 1)")
            else:  # p_kills
                seen = {st}
                stack = [st]
                filled = False
                capped = False
                while stack:
                    c = stack.pop()
                    if W.admitting(c) is None:
                        filled = True
                        break
                    for q in t_kempe(c, W.adj_tx):
                        if q not in seen:
                            seen.add(q)
                            stack.append(q)
                    if len(seen) > P_CAP:
                        capped = True
                        break
                if filled:
                    msgs.append(tag + ": class contains a filled state, P not killed")
                elif capped:
                    msgs.append(tag + ": class exceeds cap (would be capped, not a kill)")
    return msgs


# ================================================================= comparison
VFIELDS = ["unfilled_total", "states", "no_legal_fan", "sep_bad", "filled_neighbour_for_bad",
           "d1_kills", "p_kills", "p_capped", "locked_classes"]


def compare_vertex(gi, mine, prod):
    out = []
    tag = "graph %d x=%d" % (gi, mine["x"])
    if prod.get("status") == "interrupted":
        return out, True
    if prod.get("status") != mine["status"]:
        out.append("MISMATCH %s status: producer %r checker %r" % (tag, prod.get("status"), mine["status"]))
    for f in VFIELDS:
        if prod.get(f) != mine[f]:
            out.append("MISMATCH %s %s: producer %r checker %r" % (tag, f, prod.get(f), mine[f]))
    pd = prod.get("depth", {})
    for k in ("1", "2", "3", ">3"):
        if pd.get(k) != mine["depth"][k]:
            out.append("MISMATCH %s depth[%s]: producer %r checker %r" % (tag, k, pd.get(k), mine["depth"][k]))
    if prod.get("legal_fans") != mine["legal_fans"]:
        out.append("MISMATCH %s legal_fans: producer %r checker %r" % (tag, prod.get("legal_fans"), mine["legal_fans"]))
    return out, False


def wkey(kind, w, index):
    if kind == "sep_bad":
        return (index, w["x"], tuple(w["state"]), str(w.get("depth")))
    return (index, w["x"], tuple(w["state"]))


def work(task):
    index, n, rot, wits = task
    verts, mywits = analyse_graph(n, rot)
    msgs = verify_witnesses(n, rot, index, wits)
    return index, verts, mywits, msgs


def check_output(out, plantri_path, decl_path, workers, check_all, quiet=False):
    """returns (list_of_problems, stats dict)"""
    P = []
    log = (lambda s: None) if quiet else (lambda s: print(s, flush=True))
    # 1. hashes
    if out.get("declaration_sha256") != sha256_file(decl_path):
        P.append("FAULT declaration_sha256 mismatch: output %s file %s" %
                 (out.get("declaration_sha256"), sha256_file(decl_path)))
    ish = sha256_file(plantri_path)
    if out.get("input_sha256") != ish:
        P.append("FAULT input_sha256 mismatch: output %s file %s" % (out.get("input_sha256"), ish))
    order = out.get("order")
    if order in EXPECTED_INPUT and ish != EXPECTED_INPUT[order]:
        P.append("FAULT plantri stdout hash differs from the hash pre-registered for order %d" % order)
    if EXPECT_SHA[0] and ish != EXPECT_SHA[0]:
        P.append("FAULT plantri input hash differs from the expected hash %s" % EXPECT_SHA[0])
    if out.get("wp") != "WP21":
        P.append("FAULT wp field is not WP21")
    # 2. parse
    graphs = parse_plantri(plantri_path)
    if any(g[1] != order for g in graphs):
        P.append("FAULT plantri input contains graphs of order other than %r" % order)
    for i, (line, n, rot) in enumerate(graphs):
        if not triangulation_ok(n, rot):
            P.append("FAULT graph %d is not a valid minimum-degree-5 spherical triangulation" % i)
    og = out.get("graphs", [])
    if len(og) != len(graphs):
        P.append("FAULT output has %d graphs, plantri has %d" % (len(og), len(graphs)))
    byidx = {}
    for pos, g in enumerate(og):
        if g.get("index") != pos:
            P.append("FAULT graph at position %d has index %r" % (pos, g.get("index")))
        byidx[g.get("index")] = g
    # accounting + check set
    chk = set()
    unresolved = 0
    for i, (line, n, rot) in enumerate(graphs):
        g = byidx.get(i)
        if g is None:
            P.append("FAULT graph %d missing from output" % i)
            continue
        if g.get("ascii") != line:
            P.append("MISMATCH graph %d ascii differs from plantri line" % i)
        deg5 = [v for v in range(n) if len(rot[v]) == 5]
        pv = [v["x"] for v in g.get("vertices", [])]
        if g.get("status") == "complete" and pv != deg5:
            P.append("MISMATCH graph %d vertex list %r != degree-5 vertices %r" % (i, pv, deg5))
        if g.get("status") != "complete":
            chk.add(i)
            unresolved += 1
        for v in g.get("vertices", []):
            if (v.get("sep_bad", 0) or 0) > 0 or (v.get("d1_kills", 0) or 0) > 0 or \
               (v.get("p_kills", 0) or 0) > 0 or v.get("status") != "complete":
                chk.add(i)
            if v.get("status") == "interrupted":
                unresolved += 1
        if sample_index(i) or check_all:
            chk.add(i)
    # global witness/count consistency (all graphs)
    W = out.get("witnesses", {})
    trunc = bool(out.get("truncated"))
    for kind, field in (("sep_bad", "sep_bad"), ("d1_kills", "d1_kills"), ("p_kills", "p_kills")):
        tot = sum(v.get(field, 0) or 0 for g in og for v in g.get("vertices", []))
        nw = len(W.get(kind, []))
        if not trunc and tot != nw:
            P.append("MISMATCH total %s: sum of vertex counts %d, witnesses listed %d" % (field, tot, nw))
    wby = {}
    for kind in ("sep_bad", "d1_kills", "p_kills"):
        for w in W.get(kind, []):
            wby.setdefault(w.get("index"), {"sep_bad": [], "d1_kills": [], "p_kills": []})[kind].append(w)
    tasks = []
    for i in sorted(chk | set(k for k in wby if isinstance(k, int) and 0 <= k < len(graphs))):
        line, n, rot = graphs[i]
        tasks.append((i, n, rot, wby.get(i, {})))
    for k in wby:
        if not (isinstance(k, int) and 0 <= k < len(graphs)):
            P.append("FAULT witness refers to non-existent graph index %r" % (k,))
    log("checking %d graphs (check set %d, with witnesses %d) on %d workers" %
        (len(tasks), len(chk), len(wby), workers))
    results = []
    if workers > 1 and len(tasks) > 1:
        with mp.Pool(workers) as pool:
            for r in pool.imap_unordered(work, tasks, chunksize=1):
                results.append(r)
                log("  done graph %d (%d/%d)" % (r[0], len(results), len(tasks)))
    else:
        for t in tasks:
            results.append(work(t))
    nchecked = 0
    for index, verts, mywits, msgs in sorted(results, key=lambda r: r[0]):
        for m in msgs:
            P.append("MISMATCH " + m)
        if index not in chk:
            continue
        nchecked += 1
        g = byidx[index]
        pvs = {v["x"]: v for v in g.get("vertices", [])}
        for mine in verts:
            pv = pvs.get(mine["x"])
            if pv is None:
                if g.get("status") == "complete":
                    P.append("MISMATCH graph %d x=%d missing in producer output" % (index, mine["x"]))
                continue
            m, _ = compare_vertex(index, mine, pv)
            P.extend(m)
        if not trunc and g.get("status") == "complete":
            for kind in ("sep_bad", "d1_kills", "p_kills"):
                a = set(wkey(kind, dict(w, index=index), index) for w in mywits[kind])
                b = set(wkey(kind, w, index) for w in wby.get(index, {}).get(kind, []))
                for w in sorted(a - b, key=str):
                    P.append("MISMATCH graph %d %s witness missing from producer: %r" % (index, kind, w))
                for w in sorted(b - a, key=str):
                    P.append("MISMATCH graph %d %s witness not found by checker: %r" % (index, kind, w))
    return P, {"checked": nchecked, "graphs": len(graphs), "unresolved": unresolved}


# ===================================================================== selftest
def build_output(order, plantri_path, decl_path, graphs, results):
    og, wit = [], {"sep_bad": [], "d1_kills": [], "p_kills": []}
    for i, (line, n, rot) in enumerate(graphs):
        verts, w = results[i]
        og.append({"index": i, "ascii": line, "status": "complete", "vertices": copy.deepcopy(verts)})
        for kind in wit:
            for e in w[kind]:
                e = dict(e)
                e["index"] = i
                wit[kind].append(e)
    return {"wp": "WP21", "phase": "SELFTEST", "order": order,
            "declaration_sha256": sha256_file(decl_path), "input_sha256": sha256_file(plantri_path),
            "producer_sha256": {"selftest": "none"}, "graphs": og, "witnesses": wit, "truncated": False}


def selftest(order, plantri, workers, decl_path):
    import tempfile
    print("selftest order", order)
    raw = subprocess.run([plantri, "-m5", str(order), "-a"], capture_output=True, check=True).stdout
    tmp = tempfile.mkdtemp()
    ppath = os.path.join(tmp, "plantri_%d.txt" % order)
    with open(ppath, "wb") as f:
        f.write(raw)
    graphs = parse_plantri(ppath)
    print("graphs:", len(graphs))
    with mp.Pool(workers) as pool:
        results = pool.starmap(analyse_graph, [(n, rot) for (_, n, rot) in graphs])
    ok = True
    per = []
    for verts, w in results:
        per.append((sum(v["sep_bad"] for v in verts), sum(v["locked_classes"] for v in verts),
                    {k: sum(v["depth"][k] for v in verts) for k in ("1", "2", "3", ">3")},
                    sum(v["d1_kills"] for v in verts), sum(v["p_kills"] for v in verts),
                    sum(v["p_capped"] for v in verts)))
    totbad = sum(p[0] for p in per)
    totlock = sum(p[1] for p in per)
    print("SEP-bad per graph:", [p[0] for p in per], "total", totbad)
    print("locked per graph:", [p[1] for p in per], "total", totlock)
    print("depth totals:", {k: sum(p[2][k] for p in per) for k in ("1", "2", "3", ">3")})
    print("d1_kills", sum(p[3] for p in per), "p_kills", sum(p[4] for p in per),
          "p_capped", sum(p[5] for p in per))

    def expect(name, cond):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + name)
        ok = ok and cond
    if order == 16:
        expect("3 graphs", len(graphs) == 3)
        expect("0 SEP-bad", totbad == 0)
    elif order == 17:
        expect("4 graphs", len(graphs) == 4)
        expect("8 SEP-bad total", totbad == 8)
        expect("4 SEP-bad at graph 0 and 4 at graph 1, none elsewhere",
               [p[0] for p in per] == [4, 4, 0, 0])
        expect("all depth 1", sum(p[2]["1"] for p in per) == 8)
        expect("32 locked classes (10 at graph 0, 22 at graph 1)",
               totlock == 32 and per[0][1] == 10 and per[1][1] == 22)
    elif order == 18:
        expect("12 graphs", len(graphs) == 12)
        expect("0 SEP-bad", totbad == 0)
    else:
        print("(no known facts for this order)")
    # round trip + mutation test
    out = build_output(order, ppath, decl_path, graphs, results)
    P, st = check_output(out, ppath, decl_path, workers, True, quiet=True)
    expect("clean synthetic output accepted (%d graphs checked)" % st["checked"], not P)
    for p in P[:5]:
        print("  ", p)
    bad = copy.deepcopy(out)
    gi = next((g for g in bad["graphs"] if any(v["sep_bad"] for v in g["vertices"])), bad["graphs"][0])
    v0 = gi["vertices"][0]
    v0["locked_classes"] += 1
    n_counts_mut = 1
    wl = bad["witnesses"]["sep_bad"]
    n_wit_mut = 0
    if wl:
        w = wl[0]
        w["depth"] = "2" if str(w["depth"]) != "2" else "3"
        st2 = list(w["state"])
        n_wit_mut = 1
    else:
        # no SEP-bad witnesses: corrupt a p_kill/d1 witness is impossible; corrupt a state instead
        extra = {"index": 0, "x": gi["vertices"][0]["x"], "state": [0] * len(graphs[0][2]), "depth": 1}
        bad["witnesses"]["sep_bad"].append(extra)
        n_wit_mut = 1
    P2, _ = check_output(bad, ppath, decl_path, workers, True, quiet=True)
    cnt = [p for p in P2 if "locked_classes" in p]
    wit = [p for p in P2 if "witness" in p]
    expect("mutation: corrupted count reported", len(cnt) >= 1)
    expect("mutation: corrupted witness reported", len(wit) >= 1)
    # third mutation: wrong hash
    bad2 = copy.deepcopy(out)
    bad2["input_sha256"] = "0" * 64
    P3, _ = check_output(bad2, ppath, decl_path, workers, False, quiet=True)
    expect("mutation: bad input hash reported", any("input_sha256" in p for p in P3))
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 1)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--selftest", type=int)
    ap.add_argument("--plantri", default=PLANTRI_DEFAULT)
    ap.add_argument("--decl", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                   "WP21-declaration.md"))
    ap.add_argument("--expect-input-sha", default=None)
    ap.add_argument("--subset-of", default=None, help="full plantri stdout file; the input must be exactly its rule-selected lines")
    ap.add_argument("--subset-tag", default="WP21-A")
    ap.add_argument("--subset-mod", type=int, default=20)
    ap.add_argument("--full-sha", default=None, help="expected SHA-256 of the full file given to --subset-of")
    ap.add_argument("--sample-mod", type=int, default=20)
    a = ap.parse_args()
    EXPECT_SHA[0] = a.expect_input_sha
    SAMPLE_MOD[0] = a.sample_mod
    if a.selftest is not None:
        if a.selftest > 18:
            print("selftest refused above order 18")
            return 2
        return selftest(a.selftest, a.plantri, a.workers, a.decl)
    if len(a.files) != 3:
        ap.error("need OUTPUT.json PLANTRI_STDOUT DECLARATION_FILE")
    outp, pl, decl = a.files
    if a.subset_of:
        full = [l.strip() for l in open(a.subset_of) if l.strip()]
        if a.full_sha and sha256_file(a.subset_of) != a.full_sha:
            print("FAULT full plantri file hash differs from the expected %s" % a.full_sha)
            return 1
        want = [l for i, l in enumerate(full)
                if int(hashlib.sha256((a.subset_tag + "-" + str(i)).encode()).hexdigest()[:8], 16) % a.subset_mod == 0]
        have = [l.strip() for l in open(pl) if l.strip()]
        if want != have:
            print("FAULT the input is not exactly the %s mod %d selection of the full file (%d vs %d lines)"
                  % (a.subset_tag, a.subset_mod, len(have), len(want)))
            return 1
        print("subset rule verified: %d of %d graphs (tag %s, mod %d)" % (len(have), len(full), a.subset_tag, a.subset_mod))
    with open(outp) as f:
        out = json.load(f)
    P, st = check_output(out, pl, decl, a.workers, a.all)
    for p in P:
        print(p)
    print("graphs in input: %d, graphs recomputed in check set: %d, unresolved (producer interrupted/non-complete): %d"
          % (st["graphs"], st["checked"], st["unresolved"]))
    if st["unresolved"]:
        print("NOTE: unresolved vertices/graphs are inconclusive and were not compared count-for-count")
    print("CHECK FAILED: %d problem(s)" % len(P) if P else "CHECK OK: no mismatch")
    return 1 if P else 0


if __name__ == "__main__":
    sys.exit(main())
