#!/usr/bin/env python3
"""WP19 independent checker (Long Table).

Independence: this file imports only the Python standard library.  It does not
import, copy or call the WP19 producer, wp18_core, wp18_check, mass_core or any
audit code.  All graph, colouring and search logic below is written here.

Usage:
    python3 wp19_check.py PHASE.json [PHASE2.json ...]
        [--declaration PATH]      declaration file to hash (default: ../WP19-...md)
        [--declaration-rev REV]   hash the declaration as committed at git REV instead
        [--input PLANTRI_FILE]    plantri ASCII output; its sha256 is compared with
                                  "input_sha256" and graph lines are matched
        [--out SUMMARY.json]

What is VERIFIED here (certificates): graph validity and hashes, pair coverage,
witness paths and the absence of shorter fills, u_fail classes (validity,
locked members, closure under T*-Kempe swaps), kill certificates and summary
consistency.  What is NOT verified (producer claims): exact upper bounds such as
L for pairs without a witness, histograms, start counts, T*-class counts, and
U == true verdicts.  The summary says so.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from collections import deque

HOLE = 4
COLOUR_PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
DEFAULT_CAPS = {"mixed": 6, "kempe": 7}
HERE = os.path.dirname(os.path.abspath(__file__))
DECL_NAME = "WP19-preregistered-conjectures-declaration.md"
DEFAULT_DECL = os.path.normpath(os.path.join(HERE, "..", DECL_NAME))
P1_INPUT_SHA = "d233b4efafdd3510f133760d9d918beab70e7496759aef512fb302cbd594bafa"
PRODUCER_CLAIMS_NOTE = (
    "Upper bounds (exact L where no witness is given, m, hist_l, hist_k, start "
    "counts, tstar_classes, locked_classes, U==true verdicts) are PRODUCER CLAIMS "
    "and are not re-derived by this checker; only certificates are verified.")


class CheckError(Exception):
    pass


# --------------------------------------------------------------------------
# Graph
# --------------------------------------------------------------------------

class Graph:
    def __init__(self, n, rot):
        self.n = n
        self.rot = rot                       # list of lists (rotation order)
        self.adj = [frozenset(r) for r in rot]
        self.nbrs = [tuple(r) for r in rot]

    def has_edge(self, a, b):
        return b in self.adj[a]


def parse_ascii(text):
    """Parse plantri ASCII 'n abc,def,...'.  Raises CheckError on bad syntax."""
    text = text.strip()
    parts = text.split(" ", 1)
    if len(parts) != 2:
        raise CheckError("ascii: expected '<n> <rows>'")
    try:
        n = int(parts[0])
    except ValueError:
        raise CheckError("ascii: bad order")
    rows = parts[1].split(",")
    if len(rows) != n:
        raise CheckError("ascii: %d rows for order %d" % (len(rows), n))
    rot = []
    for i, r in enumerate(rows):
        row = []
        for ch in r:
            k = ord(ch) - ord("a")
            if not (0 <= k < n):
                raise CheckError("ascii: bad letter %r in row %d" % (ch, i))
            row.append(k)
        rot.append(row)
    return Graph(n, rot)


def validate_graph(g):
    """Return a list of error strings (empty when valid)."""
    errs = []
    n = g.n
    for v in range(n):
        r = g.rot[v]
        if v in r:
            errs.append("self-loop at %d" % v)
        if len(set(r)) != len(r):
            errs.append("repeated neighbour at %d" % v)
        if len(r) < 5:
            errs.append("degree %d < 5 at %d" % (len(r), v))
        for w in r:
            if v not in g.adj[w]:
                errs.append("asymmetric edge %d-%d" % (v, w))
    if errs:
        return errs
    e = sum(len(r) for r in g.rot)
    if e % 2:
        return ["odd degree sum"]
    e //= 2
    if e != 3 * n - 6:
        errs.append("edges %d != 3n-6 = %d" % (e, 3 * n - 6))
    # faces: dart (u,w) -> (w, x) with x the successor of u in rot[w]
    pos = [{w: k for k, w in enumerate(r)} for r in g.rot]
    seen = set()
    faces = 0
    for u in range(n):
        for w in g.rot[u]:
            if (u, w) in seen:
                continue
            length = 0
            a, b = u, w
            while (a, b) not in seen:
                seen.add((a, b))
                length += 1
                rb = g.rot[b]
                x = rb[(pos[b][a] + 1) % len(rb)]
                a, b = b, x
                if length > 2 * e:
                    break
            if (a, b) != (u, w):
                errs.append("face orbit does not close at dart %d-%d" % (u, w))
            if length != 3:
                errs.append("face of length %d at dart %d-%d" % (length, u, w))
            faces += 1
    if n - e + faces != 2:
        errs.append("Euler characteristic %d != 2" % (n - e + faces))
    return errs


def fan_chords(g, v, i):
    link = g.rot[v]
    return ((link[i], link[(i + 2) % 5]), (link[i], link[(i + 3) % 5]))


def legal_pairs(g):
    """{(v,i): chords} for every degree-5 v and legal fan i."""
    out = {}
    for v in range(g.n):
        if len(g.rot[v]) != 5:
            continue
        for i in range(5):
            ch = fan_chords(g, v, i)
            if not any(g.has_edge(a, b) for a, b in ch):
                out[(v, i)] = ch
    return out


def star_nbrs(g, v, chords):
    """Neighbour tuples of T*_tau = (T - v) + chords (v keeps no edges)."""
    nb = [set(x) for x in g.adj]
    for w in g.adj[v]:
        nb[w].discard(v)
    nb[v] = set()
    for a, b in chords:
        nb[a].add(b)
        nb[b].add(a)
    return [tuple(sorted(s)) for s in nb]


# --------------------------------------------------------------------------
# States and moves
# --------------------------------------------------------------------------

def canon(s):
    m = {}
    out = []
    for x in s:
        if x == HOLE:
            out.append(HOLE)
        else:
            y = m.get(x)
            if y is None:
                y = len(m)
                m[x] = y
            out.append(y)
    return tuple(out)


def hole_of(s):
    return s.index(HOLE)


def is_proper(g, s):
    for u in range(g.n):
        cu = s[u]
        if cu == HOLE:
            continue
        for w in g.nbrs[u]:
            if s[w] == cu:
                return False
    return True


def is_filled(g, s):
    h = hole_of(s)
    return len({s[w] for w in g.nbrs[h]}) <= 3


def state_errors(g, s, v=None):
    """Structural validity of a JSON state; returns error string or None."""
    if not isinstance(s, (list, tuple)) or len(s) != g.n:
        return "state has wrong length"
    for x in s:
        if not isinstance(x, int) or isinstance(x, bool) or not (0 <= x <= 4):
            return "state has a bad entry"
    if list(s).count(HOLE) != 1:
        return "state must have exactly one hole"
    if v is not None and s[v] != HOLE:
        return "hole is not at v=%d" % v
    if tuple(s) != canon(s):
        return "state not canonical"
    if not is_proper(g, s):
        return "state improper"
    return None


def start_errors(g, s, v, chords):
    e = state_errors(g, s, v)
    if e:
        return e
    for a, b in chords:
        if s[a] == s[b]:
            return "chord %d-%d monochromatic (not proper on T*)" % (a, b)
    return None


def kempe_successors(nbrs, s, hole):
    """Yield (a, b, seed, canonical successor) for every component swap.

    Components are in the graph given by nbrs restricted to vertices coloured
    a or b; the hole (colour 4) never belongs to one.  seed = min vertex.
    """
    n = len(s)
    for a, b in COLOUR_PAIRS:
        seen = set()
        for u in range(n):
            cu = s[u]
            if (cu != a and cu != b) or u in seen:
                continue
            comp = [u]
            seen.add(u)
            k = 0
            while k < len(comp):
                x = comp[k]
                k += 1
                for y in nbrs[x]:
                    cy = s[y]
                    if (cy == a or cy == b) and y not in seen:
                        seen.add(y)
                        comp.append(y)
            t = list(s)
            for x in comp:
                t[x] = b if t[x] == a else a
            yield a, b, u, canon(t)


def slide_successors(g, s, hole):
    cols = [s[w] for w in g.nbrs[hole]]
    for w in g.nbrs[hole]:
        if cols.count(s[w]) == 1:
            t = list(s)
            t[hole] = s[w]
            t[w] = HOLE
            yield w, canon(t)


def successors(g, s, mixed):
    h = hole_of(s)
    for a, b, seed, t in kempe_successors(g.nbrs, s, h):
        yield ["K", a, b, seed], t
    if mixed:
        for w, t in slide_successors(g, s, h):
            yield ["S", w], t


def apply_move(g, s, move):
    """Apply one encoded move; raise CheckError if illegal."""
    h = hole_of(s)
    if not isinstance(move, list) or not move:
        raise CheckError("bad move encoding %r" % (move,))
    if move[0] == "K":
        if len(move) != 4:
            raise CheckError("bad Kempe move %r" % (move,))
        _, a, b, seed = move
        if a not in (0, 1, 2, 3) or b not in (0, 1, 2, 3) or a == b:
            raise CheckError("bad Kempe colours %r" % (move,))
        if not (isinstance(seed, int) and 0 <= seed < g.n) or s[seed] not in (a, b):
            raise CheckError("Kempe seed not coloured a/b %r" % (move,))
        comp = [seed]
        seen = {seed}
        k = 0
        while k < len(comp):
            x = comp[k]
            k += 1
            for y in g.nbrs[x]:
                if s[y] in (a, b) and y not in seen:
                    seen.add(y)
                    comp.append(y)
        if min(comp) != seed:
            raise CheckError("Kempe seed %d is not the minimum of its component" % seed)
        t = list(s)
        for x in comp:
            t[x] = b if t[x] == a else a
        return canon(t)
    if move[0] == "S":
        if len(move) != 2:
            raise CheckError("bad slide %r" % (move,))
        u = move[1]
        if not isinstance(u, int) or u not in g.adj[h]:
            raise CheckError("slide target %r not adjacent to hole" % (u,))
        cols = [s[w] for w in g.nbrs[h]]
        if cols.count(s[u]) != 1:
            raise CheckError("slide target colour is not a singleton on the link")
        t = list(s)
        t[h] = s[u]
        t[u] = HOLE
        return canon(t)
    raise CheckError("unknown move type %r" % (move[0],))


def replay(g, start, path):
    s = tuple(start)
    if not isinstance(path, list):
        raise CheckError("path is not a list")
    for mv in path:
        s = apply_move(g, s, mv)
        if not is_proper(g, s):
            raise CheckError("replay produced an improper state")
    return s


def first_fill_depth(g, start, max_depth, mixed):
    """Complete layer-by-layer BFS.  Return the first depth <= max_depth that
    contains a filled state, or None if layers 0..max_depth contain none.
    max_depth=None means: explore the whole closure."""
    start = tuple(start)
    if is_filled(g, start):
        return 0
    seen = {start}
    frontier = [start]
    d = 0
    while frontier and (max_depth is None or d < max_depth):
        d += 1
        nxt = []
        for s in frontier:
            for _, t in successors(g, s, mixed):
                if t in seen:
                    continue
                if is_filled(g, t):
                    return d
                seen.add(t)
                nxt.append(t)
        frontier = nxt
    return None


def shortest_fill(g, start, max_depth, mixed):
    """(depth, path) of a shortest fill within max_depth, or (None, None)."""
    start = tuple(start)
    if is_filled(g, start):
        return 0, []
    parent = {start: None}
    frontier = [start]
    d = 0
    while frontier and d < max_depth:
        d += 1
        nxt = []
        for s in frontier:
            for mv, t in successors(g, s, mixed):
                if t in parent:
                    continue
                parent[t] = (s, mv)
                if is_filled(g, t):
                    path = []
                    x = t
                    while parent[x] is not None:
                        p, m = parent[x]
                        path.append(m)
                        x = p
                    return d, path[::-1]
                nxt.append(t)
        frontier = nxt
    return None, None


def is_locked(g, s):
    if is_filled(g, s):
        return False
    h = hole_of(s)
    for _, _, _, t in kempe_successors(g.nbrs, s, h):
        if is_filled(g, t):
            return False
    return True


def tstar_successors(snb, s):
    for _, _, _, t in kempe_successors(snb, s, hole_of(s)):
        yield t


def enumerate_starts(g, v, chords):
    """All canonical proper 4-colourings of T*_tau (hole at v)."""
    snb = star_nbrs(g, v, chords)
    order = [u for u in range(g.n) if u != v]
    col = [HOLE] * g.n
    out = []

    def rec(k, used):
        if k == len(order):
            out.append(tuple(col))
            return
        u = order[k]
        for c in range(min(used + 1, 4)):
            if all(col[w] != c for w in snb[u]):
                col[u] = c
                rec(k + 1, max(used, c + 1))
                col[u] = HOLE
    rec(0, 0)
    return out


def tstar_classes(g, v, chords, starts):
    snb = star_nbrs(g, v, chords)
    idx = {s: k for k, s in enumerate(starts)}
    comp = [-1] * len(starts)
    classes = []
    for k, s in enumerate(starts):
        if comp[k] >= 0:
            continue
        cl = [s]
        comp[k] = len(classes)
        q = 0
        while q < len(cl):
            x = cl[q]
            q += 1
            for t in tstar_successors(snb, x):
                j = idx.get(t)
                if j is None:
                    raise CheckError("T*-swap left the start set (bug)")
                if comp[j] < 0:
                    comp[j] = len(classes)
                    cl.append(t)
        classes.append(cl)
    return classes


# --------------------------------------------------------------------------
# Phase checking
# --------------------------------------------------------------------------

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def declaration_sha(path, rev=None):
    if rev:
        rel = os.path.relpath(path, os.path.dirname(path))
        data = subprocess.check_output(
            ["git", "show", "%s:./%s" % (rev, rel)], cwd=os.path.dirname(path))
        return sha256_bytes(data)
    with open(path, "rb") as f:
        return sha256_bytes(f.read())


def pair_key(p):
    if isinstance(p, dict):
        return (p.get("v"), p.get("fan_index"))
    if isinstance(p, (list, tuple)) and len(p) == 2:
        return (p[0], p[1])
    return None


class GraphChecker:
    def __init__(self, G, caps, truncated, fails, stats):
        self.G = G
        self.caps = caps
        self.truncated = truncated
        self.fails = fails
        self.stats = stats
        self.tag = "%s:%s" % (G.get("order"), G.get("graph_index"))

    def fail(self, code, msg):
        self.fails.append({"graph": self.tag, "code": code, "msg": msg})

    def run(self):
        G = self.G
        st = self.stats
        try:
            g = parse_ascii(G["ascii"])
        except (CheckError, KeyError, TypeError) as e:
            self.fail("parse", str(e))
            return
        self.g = g
        if sha256_bytes(G["ascii"].encode()) != G.get("ascii_sha256"):
            self.fail("ascii_hash", "ascii_sha256 mismatch")
        if G.get("order") != g.n:
            self.fail("order", "order field %r != %d" % (G.get("order"), g.n))
        for e in validate_graph(g):
            self.fail("graph_invalid", e)
        if any(f["graph"] == self.tag and f["code"] in ("graph_invalid",) for f in self.fails):
            return
        # Long Table reconciliation, 5 October: the producer spec lists degrees sorted.
        if G.get("degrees") != sorted(len(r) for r in g.rot):
            self.fail("degrees", "degree list mismatch")

        interrupted = bool(G.get("interrupted"))
        if interrupted:
            st["graphs_interrupted"] += 1
        else:
            st["graphs_checked"] += 1

        legal = legal_pairs(g)
        self.legal = legal
        pairs = G.get("pairs") or []
        seen = {}
        for P in pairs:
            k = (P.get("v"), P.get("fan_index"))
            if k in seen:
                self.fail("coverage", "duplicate pair %r" % (k,))
            seen[k] = P
        if set(seen) != set(legal):
            missing = sorted(set(legal) - set(seen))
            extra = sorted(set(seen) - set(legal), key=str)
            self.fail("coverage", "pair set mismatch: missing %s extra %s"
                      % (missing[:10], extra[:10]))
        self.pairs = seen
        st["pairs"] += len(seen)

        unresolved_listed = set()
        for p in G.get("unresolved_pairs") or []:
            unresolved_listed.add(pair_key(p))
        unresolved_actual = set()
        for k, P in seen.items():
            if k in legal:
                self.check_pair(k, P, legal[k])
            r = P.get("unresolved_reason")
            if r is not None:
                unresolved_actual.add(k)
        if unresolved_listed != unresolved_actual:
            self.fail("unresolved", "unresolved_pairs %s != pairs with a reason %s"
                      % (sorted(unresolved_listed, key=str)[:10],
                         sorted(unresolved_actual)[:10]))
        if interrupted and not unresolved_actual:
            # an interrupted graph cannot claim everything resolved
            self.fail("unresolved", "interrupted graph lists no unresolved pairs")
        self.unresolved = bool(unresolved_actual) or interrupted
        if self.unresolved:
            st["graphs_unresolved"] += 1
            if G.get("m") is not None:
                self.fail("m_exact", "m must be null when pairs are unresolved")

        # summary consistency
        nonempty = [P for P in seen.values() if not P.get("empty")]
        if nonempty:
            lo = min(P.get("L_at_least", -1) for P in nonempty)
            if G.get("m_at_least") != lo:
                self.fail("m_at_least", "m_at_least %r != min L_at_least %r"
                          % (G.get("m_at_least"), lo))
            if not self.unresolved and G.get("m") != G.get("m_at_least"):
                self.fail("m_exact", "resolved graph with m != m_at_least")
        u_any = any(P.get("U") is True for P in seen.values())
        if not interrupted and G.get("U_exists") != u_any:
            self.fail("U_exists", "U_exists %r != any(U) %r" % (G.get("U_exists"), u_any))

        for K in G.get("kills") or []:
            self.check_kill(K)

    # -- pairs --------------------------------------------------------------

    def check_pair(self, k, P, chords):
        g = self.g
        st = self.stats
        v, i = k
        pc = P.get("chords")
        try:
            if {frozenset(c) for c in pc} != {frozenset(c) for c in chords} or len(pc) != 2:
                self.fail("chords", "pair %r chords %r != %r" % (k, pc, chords))
        except TypeError:
            self.fail("chords", "pair %r chords malformed" % (k,))
        reason = P.get("unresolved_reason")
        if reason not in (None, "capped", "interrupted"):
            self.fail("unresolved", "pair %r bad unresolved_reason %r" % (k, reason))
        if P.get("empty"):
            if P.get("starts") not in (0, None):
                self.fail("empty", "pair %r empty but starts=%r" % (k, P.get("starts")))
            return
        La = P.get("L_at_least")
        if not isinstance(La, int):
            self.fail("L", "pair %r has no integer L_at_least" % (k,))
            return
        if reason is None:
            if P.get("L") != La:
                self.fail("L", "resolved pair %r has L %r != L_at_least %r"
                          % (k, P.get("L"), La))
        else:
            if P.get("L") is not None:
                self.fail("L", "unresolved pair %r has non-null L" % (k,))
            if reason == "capped" and La != self.caps["mixed"] + 1:
                self.fail("L", "capped pair %r has L_at_least %r != cap+1" % (k, La))
        if isinstance(P.get("hist_l"), dict) and isinstance(P.get("starts"), int):
            if sum(P["hist_l"].values()) != P["starts"]:
                st["warnings"].append("%s pair %r: sum(hist_l) != starts" % (self.tag, k))

        W = P.get("witness_L")
        if W is not None:
            self.check_witness(k, P, chords, W, La, reason)
        elif La >= 3 and reason is None:
            if self.truncated:
                st["witnesses_missing_truncated"] += 1
            else:
                self.fail("witness_missing", "pair %r has L >= 3 but no witness_L" % (k,))

        U = P.get("U")
        uf = P.get("u_fail_class")
        if U is True and uf is not None:
            self.fail("u_fail", "pair %r has U true and a u_fail_class" % (k,))
        if U is True and P.get("locked_classes") not in (0, None):
            self.fail("u_fail", "pair %r has U true but locked_classes>0" % (k,))
        if U is False:
            if uf is None:
                if self.truncated:
                    st["u_fail_missing_truncated"] += 1
                else:
                    self.fail("u_fail_missing", "pair %r has U false and no u_fail_class" % (k,))
            else:
                if self.check_u_fail(k, chords, uf):
                    st["u_fail_classes_verified"] += 1
                    self.verified_ufail = getattr(self, "verified_ufail", set())
                    self.verified_ufail.add(k)
                if P.get("locked_classes") in (0,):
                    self.fail("u_fail", "pair %r has U false but locked_classes 0" % (k,))
        elif uf is not None:
            self.fail("u_fail", "pair %r has u_fail_class but U is %r" % (k, U))

    def check_witness(self, k, P, chords, W, La, reason):
        g = self.g
        v = k[0]
        start = W.get("start")
        e = start_errors(g, start, v, chords)
        if e:
            self.fail("witness", "pair %r witness start: %s" % (k, e))
            return
        start = tuple(start)
        path = W.get("path")
        cap = self.caps["mixed"]
        if path is None:
            # capped witness: no fill in layers 0..cap
            if La != cap + 1:
                self.fail("witness", "pair %r witness without path but L_at_least %r" % (k, La))
                return
            if first_fill_depth(g, start, cap, True) is not None:
                self.fail("witness", "pair %r capped witness fills within cap" % (k,))
                return
            self.stats["witnesses_verified"] += 1
            return
        try:
            end = replay(g, start, path)
        except CheckError as ex:
            self.fail("witness", "pair %r path replay: %s" % (k, ex))
            return
        if not is_filled(g, end):
            self.fail("witness", "pair %r path does not end filled" % (k,))
            return
        if len(path) != La:
            self.fail("witness", "pair %r path length %d != L_at_least %d" % (k, len(path), La))
            return
        if len(path) > 0 and first_fill_depth(g, start, len(path) - 1, True) is not None:
            self.fail("witness", "pair %r a shorter fill exists" % (k,))
            return
        # Lemma A consistency: locked iff l >= 2
        if is_locked(g, start) != (len(path) >= 2):
            self.fail("lemmaA", "pair %r witness: locked=%r but l=%d"
                      % (k, is_locked(g, start), len(path)))
        self.stats["witnesses_verified"] += 1

    def check_u_fail(self, k, chords, members):
        g = self.g
        v = k[0]
        if not isinstance(members, list) or not members:
            self.fail("u_fail", "pair %r u_fail_class empty or malformed" % (k,))
            return False
        S = set()
        for s in members:
            e = start_errors(g, s, v, chords)
            if e:
                self.fail("u_fail", "pair %r class member: %s" % (k, e))
                return False
            S.add(tuple(s))
        if len(S) != len(members):
            self.fail("u_fail", "pair %r class has duplicate members" % (k,))
            return False
        for s in S:
            if not is_locked(g, s):
                self.fail("u_fail", "pair %r class contains an unlocked member" % (k,))
                return False
        snb = star_nbrs(g, v, chords)
        for s in S:
            for t in tstar_successors(snb, s):
                if t not in S:
                    self.fail("u_fail", "pair %r class not closed under T*-swaps" % (k,))
                    return False
        # Lemma A consistency on one member (locked => no fill in 0..1)
        s0 = min(S)
        if first_fill_depth(g, s0, 1, True) is not None:
            self.fail("lemmaA", "pair %r locked member fills in <= 1 mixed move" % (k,))
            return False
        return True

    # -- kills --------------------------------------------------------------

    def kill_start(self, pair, start):
        k = pair_key(pair)
        if k not in self.legal:
            raise CheckError("kill pair %r is not a legal pair" % (pair,))
        e = start_errors(self.g, start, k[0], self.legal[k])
        if e:
            raise CheckError("kill start for %r: %s" % (k, e))
        return k, tuple(start)

    def check_kill(self, K):
        g = self.g
        stmt = K.get("stmt") if isinstance(K, dict) else None
        try:
            if stmt == "M1":
                _, s = self.kill_start(K.get("pair"), K.get("start"))
                if first_fill_depth(g, s, 4, True) is not None:
                    raise CheckError("M1: start fills within 4 mixed moves")
            elif stmt == "M2":
                _, s = self.kill_start(K.get("pair"), K.get("start"))
                kap = K.get("kappa")
                if kap == "nofill":
                    if first_fill_depth(g, s, None, False) is not None:
                        raise CheckError("M2 nofill: Kempe-only closure contains a fill")
                elif kap == "lower":
                    lp = K.get("l_path")
                    end = replay(g, s, lp)
                    if not is_filled(g, end):
                        raise CheckError("M2: l_path does not fill")
                    depth = len(lp) + 1
                    kl = K.get("kappa_lower")
                    if kl is not None:
                        if not isinstance(kl, int) or kl < len(lp) + 2:
                            raise CheckError("M2: kappa_lower %r < len(l_path)+2" % (kl,))
                        if kl - 1 > self.caps["kempe"]:
                            raise CheckError("M2: kappa_lower beyond Kempe cap")
                        depth = max(depth, kl - 1)
                    if first_fill_depth(g, s, depth, False) is not None:
                        raise CheckError("M2: Kempe-only fill within depth %d" % depth)
                else:
                    raise CheckError("M2: unknown kappa %r" % (kap,))
            elif stmt == "M3":
                _, s = self.kill_start(K.get("pair"), K.get("start"))
                lp = K.get("l_path")
                if not isinstance(lp, list) or len(lp) != 2:
                    raise CheckError("M3: l_path must have length 2")
                if not is_filled(g, replay(g, s, lp)):
                    raise CheckError("M3: l_path does not fill")
                if first_fill_depth(g, s, 1, True) is not None:
                    raise CheckError("M3: l < 2 (mixed fill within 1 move)")
                if first_fill_depth(g, s, 2, False) is not None:
                    raise CheckError("M3: Kempe-only fill within 2 moves")
            elif stmt in ("C1", "C2", "C3"):
                depth = 3 if stmt == "C2" else 2
                if stmt == "C1" and g.n < 18:
                    raise CheckError("C1: order %d < 18, statement does not apply" % g.n)
                if stmt == "C3" and max(len(r) for r in g.rot) < 7:
                    raise CheckError("C3: no vertex of degree >= 7")
                pp = K.get("per_pair")
                if not isinstance(pp, list):
                    raise CheckError("%s: per_pair missing" % stmt)
                keys = [pair_key(x.get("pair")) for x in pp]
                if len(set(keys)) != len(keys) or set(keys) != set(self.legal):
                    raise CheckError("%s: per_pair does not cover every legal pair exactly once"
                                     % stmt)
                for x in pp:
                    k, s = self.kill_start(x.get("pair"), x.get("start"))
                    if first_fill_depth(g, s, depth, True) is not None:
                        raise CheckError("%s: pair %r start fills within %d mixed moves"
                                         % (stmt, k, depth))
            elif stmt == "U_exists":
                ver = getattr(self, "verified_ufail", set())
                if set(self.legal) - ver:
                    raise CheckError("U_exists: %d legal pairs lack a verified u_fail_class"
                                     % len(set(self.legal) - ver))
            else:
                raise CheckError("unknown kill statement %r" % (stmt,))
        except CheckError as ex:
            self.fail("kill_" + str(stmt), str(ex))
            return
        self.stats["kills_verified"][stmt] = self.stats["kills_verified"].get(stmt, 0) + 1
        if self.unresolved:
            self.stats["kills_on_unresolved_graphs"].append("%s %s" % (self.tag, stmt))


def check_phase(D, decl_sha, input_path=None, label="phase"):
    fails = []
    stats = {
        "graphs_checked": 0, "graphs_interrupted": 0, "graphs_unresolved": 0,
        "pairs": 0, "witnesses_verified": 0, "u_fail_classes_verified": 0,
        "witnesses_missing_truncated": 0, "u_fail_missing_truncated": 0,
        "kills_verified": {}, "kills_on_unresolved_graphs": [], "warnings": [],
    }
    info = {"file": label}

    def ff(code, msg):
        fails.append({"graph": None, "code": code, "msg": msg})

    if not isinstance(D, dict) or "graphs" not in D:
        ff("format", "top level is not a phase object")
        return {"info": info, "stats": stats, "failures": fails}
    # binding by hash: refuse on a declaration mismatch
    if D.get("declaration_sha256") != decl_sha:
        ff("declaration_sha256", "REFUSED: declaration_sha256 %r != recomputed %s"
           % (D.get("declaration_sha256"), decl_sha))
        return {"info": info, "stats": stats, "failures": fails, "refused": True}
    info["declaration_sha256"] = decl_sha
    info["source_sha256"] = D.get("source_sha256")
    if not isinstance(D.get("source_sha256"), dict):
        ff("format", "source_sha256 missing or not a dict")
    info["input_sha256_claimed"] = D.get("input_sha256")
    lines = None
    if input_path:
        with open(input_path, "rb") as f:
            raw = f.read()
        info["input_sha256_recomputed"] = sha256_bytes(raw)
        claimed = D.get("input_sha256")
        if isinstance(claimed, dict):
            # P2 binds two input files (orders 21 and 22) as {filename: sha}. The given
            # file must be one of them; per-line matching is skipped for a multi-file phase.
            if info["input_sha256_recomputed"] not in claimed.values():
                ff("input_sha256", "input file hash is not among the phase's input_sha256 values")
            lines = None
            info["line_matching"] = "skipped (multi-file phase)"
        else:
            if info["input_sha256_recomputed"] != claimed:
                ff("input_sha256", "input file hash differs from input_sha256")
            lines = [ln for ln in raw.decode().splitlines() if ln.strip()]
    else:
        info["input_sha256_recomputed"] = "not checked (no --input given)"
    orders = {G.get("order") for G in D["graphs"]}
    if orders == {23}:
        info["input_sha256_matches_declared_P1"] = (D.get("input_sha256") == P1_INPUT_SHA)
        if D.get("input_sha256") != P1_INPUT_SHA:
            ff("input_sha256", "order-23 phase input hash != declared P1 hash")

    caps = D.get("caps") or {}
    if caps != DEFAULT_CAPS:
        ff("caps", "caps %r != declared %r" % (caps, DEFAULT_CAPS))
        caps = DEFAULT_CAPS
    truncated = bool(D.get("truncated"))
    info["truncated"] = truncated
    for G in D["graphs"]:
        if lines is not None:
            gi = G.get("graph_index")
            if not (isinstance(gi, int) and 0 <= gi < len(lines)
                    and lines[gi].strip() == G.get("ascii")):
                fails.append({"graph": "%s:%s" % (G.get("order"), gi), "code": "input_line",
                              "msg": "ascii is not line graph_index (0-based) of the input"})
        GraphChecker(G, caps, truncated, fails, stats).run()
    return {"info": info, "stats": stats, "failures": fails,
            "producer_claims_not_verified": PRODUCER_CLAIMS_NOTE}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("phase", nargs="+")
    ap.add_argument("--declaration", default=DEFAULT_DECL)
    ap.add_argument("--declaration-rev", default=None)
    ap.add_argument("--input", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    dsha = declaration_sha(a.declaration, a.declaration_rev)
    results = []
    for p in a.phase:
        with open(p) as f:
            D = json.load(f)
        results.append(check_phase(D, dsha, a.input, label=p))
    out = {"checker": "wp19_check.py (independent, stdlib only)",
           "declaration_sha256_recomputed": dsha, "results": results,
           "total_failures": sum(len(r["failures"]) for r in results)}
    txt = json.dumps(out, indent=1, sort_keys=True)
    if a.out:
        with open(a.out, "w") as f:
            f.write(txt + "\n")
    print(txt)
    return 1 if out["total_failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
