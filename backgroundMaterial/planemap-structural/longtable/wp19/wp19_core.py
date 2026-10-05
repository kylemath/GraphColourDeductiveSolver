"""WP19 core: per-graph fill lengths, Kempe-only lengths, locking, T*-Kempe classes, U(v,tau),
and kill certificates for M1, M2, M3, C1, C2, C3 and U-exists.

Declaration: ../WP19-preregistered-conjectures-declaration.md (statements fixed there).

States are tuples over all n vertices, HOLE = 4 at the hole, other colours canonical by first
occurrence in vertex order skipping the hole (wp18_core.canon). Moves (wp18_core.moves):
("K", a, b, seed) swaps one whole {a,b}-component of T - hole (seed = its minimum vertex),
("S", u) slides the hole onto a singleton-coloured link vertex u. Both moves are reversible,
so the mixed move graph and the Kempe-only graph at a fixed hole are undirected.

Method (exact, and equal to per-start breadth-first search with the declared caps):
  * ell: one multi-source breadth-first search from every filled state of every hole, over
    the mixed move graph, to depth CAP_MIXED = 6. A state not reached has ell > 6 ("capped").
  * kappa at hole v: one multi-source breadth-first search from the filled states at hole v
    over Kempe moves only, run to exhaustion. A state never reached lies in a Kempe class of
    T - v with no fill ("nofill"); a state reached at depth > CAP_KEMPE = 7 is "capped".
  * locked(s): s not filled and kappa(s) != 1 (no single Kempe swap of T - v fills it).
  * Lemma A (wp18/mechanism.md) is asserted at every start: for a start with a 4-colour link,
    locked <=> ell >= 2 (ell capped counts as >= 2). A mismatch raises LemmaAFault.
  * T*_tau Kempe classes: union-find over S(v,tau) under Kempe swaps in T - v plus the two
    chord edges. U(v,tau): every class has a member that is not locked.

Resource hooks: check() is called inside enumeration and breadth-first search; it raises
Interrupted("deadline") past the deadline and Interrupted("memory") past the memory limit
(peak RSS from resource.getrusage). An interrupted graph keeps every completed pair and the
partial counts of the pair in progress; every legal pair still appears in the output.
"""
from __future__ import annotations

import hashlib
import resource
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "wp18"))
sys.path.insert(0, str(HERE.parent))
from wp18_core import HOLE, PAIRS, canon, filled, legal_fans, moves, parse_ascii  # noqa: E402,F401

CAP_MIXED = 6
CAP_KEMPE = 7
MEM_LIMIT_KB = 8 * 1024 * 1024  # 8 GB per worker
CHECK_EVERY = 2048


class Interrupted(Exception):
    pass


class LemmaAFault(AssertionError):
    pass


def peak_rss_kb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r // 1024 if sys.platform == "darwin" else r


class Guard:
    """In-loop hook: deadline (time.monotonic() value or None) and memory limit."""

    def __init__(self, deadline=None, mem_limit_kb=MEM_LIMIT_KB):
        self.deadline, self.mem, self.n = deadline, mem_limit_kb, 0

    def check(self, force=False):
        self.n += 1
        if not force and self.n % CHECK_EVERY:
            return
        if self.deadline is not None and time.monotonic() > self.deadline:
            raise Interrupted("deadline")
        if self.mem is not None and peak_rss_kb() > self.mem:
            raise Interrupted("memory")


# ---------------------------------------------------------------- enumeration and moves

def deletion_states(rot, v, guard):
    """Every proper 4-colouring of T - v, canonical, HOLE at v (vertex-order enumeration)."""
    n = len(rot)
    order = [u for u in range(n) if u != v]
    pos = {u: i for i, u in enumerate(order)}
    earlier = [[pos[w] for w in rot[u] if w != v and pos[w] < i] for i, u in enumerate(order)]
    cur = [0] * len(order)
    out = []

    def go(i, top):
        guard.check()
        if i == len(order):
            st = [HOLE] * n
            for j, u in enumerate(order):
                st[u] = cur[j]
            out.append(canon(st))
            return
        blocked = {cur[j] for j in earlier[i]}
        for a in range(min(3, top + 1) + 1):
            if a not in blocked:
                cur[i] = a
                go(i + 1, max(top, a))

    go(0, -1)
    return out


def kempe_moves_nb(nb, state):
    """Kempe swaps of the current deletion in the graph with neighbour sets nb (hole fixed)."""
    for a, b in PAIRS:
        seen = set()
        for s, col in enumerate(state):
            if (col != a and col != b) or s in seen:
                continue
            comp = {s}
            stack = [s]
            while stack:
                x = stack.pop()
                for y in nb[x]:
                    if y not in comp and (state[y] == a or state[y] == b):
                        comp.add(y)
                        stack.append(y)
            seen |= comp
            nxt = list(state)
            for x in comp:
                nxt[x] = b if state[x] == a else a
            yield ("K", a, b, min(comp)), canon(nxt)


def link_colours(rot, state):
    h = state.index(HOLE)
    return len({state[w] for w in rot[h]})


# ---------------------------------------------------------------- distances

def mixed_distances(rot, states_by_hole, guard, cap=CAP_MIXED):
    """ell for every state with ell <= cap (dict); absent states have ell > cap."""
    dist = {}
    frontier = []
    for sts in states_by_hole.values():
        for s in sts:
            guard.check()
            if filled(rot, s):
                dist[s] = 0
                frontier.append(s)
    for d in range(1, cap + 1):
        nxt = []
        for x in frontier:
            for _, y in moves(rot, x):
                guard.check()
                if y not in dist:
                    dist[y] = d
                    nxt.append(y)
        frontier = nxt
        if not frontier:
            break
    return dist


def kempe_distances(rot, v, states, guard):
    """Kempe-only distance to a fill at fixed hole v, run to exhaustion (absent = nofill)."""
    nb = [set(ns) for ns in rot]
    dist = {}
    frontier = []
    for s in states:
        guard.check()
        if filled(rot, s):
            dist[s] = 0
            frontier.append(s)
    d = 0
    while frontier:
        d += 1
        nxt = []
        for x in frontier:
            for _, y in kempe_moves_nb(nb, x):
                guard.check()
                if y not in dist:
                    dist[y] = d
                    nxt.append(y)
        frontier = nxt
    return dist


def path_to_fill(rot, s, dist, kempe_only=False):
    """Shortest move list from s to a filled state, following dist downhill (first move in
    generation order). Moves as JSON lists."""
    nb = [set(ns) for ns in rot]
    out = []
    cur = s
    while dist[cur] > 0:
        gen = kempe_moves_nb(nb, cur) if kempe_only else moves(rot, cur)
        for mv, y in gen:
            if dist.get(y) == dist[cur] - 1:
                out.append(list(mv))
                cur = y
                break
        else:
            raise AssertionError("distance map inconsistent")
    return out


class UF:
    def __init__(self, items):
        self.p = {x: x for x in items}

    def find(self, x):
        p = self.p
        r = x
        while p[r] != r:
            r = p[r]
        while p[x] != r:
            p[x], x = r, p[x]
        return r

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def tstar_classes(rot, chords, S, guard):
    nb = [set(ns) for ns in rot]
    for a, b in chords:
        nb[a].add(b)
        nb[b].add(a)
    Sset = set(S)
    uf = UF(S)
    for s in S:
        for _, t in kempe_moves_nb(nb, s):
            guard.check()
            if t not in Sset:
                raise AssertionError("T* swap left S(v,tau)")
            uf.union(s, t)
    classes = {}
    for s in S:
        classes.setdefault(uf.find(s), []).append(s)
    return list(classes.values())


# ---------------------------------------------------------------- per graph

def hist_l_empty():
    h = {str(k): 0 for k in range(CAP_MIXED + 1)}
    h["capped"] = 0
    return h


def hist_k_empty():
    h = {str(k): 0 for k in range(CAP_KEMPE + 1)}
    h["capped"] = 0
    h["nofill"] = 0
    return h


def kappa_value(kd, s):
    k = kd.get(s)
    if k is None:
        return "nofill"
    if k > CAP_KEMPE:
        return "capped"
    return k


def blank_pair(v, i, c1, c2, starts=None):
    return {"v": v, "fan_index": i, "chords": [list(c1), list(c2)],
            "empty": False if starts is None else starts == 0,
            "starts": starts, "hist_l": hist_l_empty(), "hist_k": hist_k_empty(),
            "L": None, "L_at_least": 0, "unresolved_reason": "interrupted",
            "tstar_classes": None, "locked_classes": None, "U": None}


def graph_report(rot, deadline=None, mem_limit_kb=MEM_LIMIT_KB, order=None, graph_index=None,
                 ascii_=None):
    """The G record of the declaration's output format (see wp19_run.py for the schema)."""
    guard = Guard(deadline, mem_limit_kb)
    n = len(rot)
    G = {"order": n if order is None else order, "graph_index": graph_index, "ascii": ascii_,
         "ascii_sha256": hashlib.sha256(ascii_.encode()).hexdigest() if ascii_ else None,
         "degrees": sorted(len(ns) for ns in rot), "interrupted": None, "peak_rss_kb": 0,
         "pairs": [], "m": None, "m_at_least": 0, "unresolved_pairs": [], "U_exists": None,
         "kills": []}
    deg5 = [u for u in range(n) if len(rot[u]) == 5]
    legal = [(v, f) for v in deg5 for f in legal_fans(rot, v)]
    done = {}           # (v,i) -> finished pair record
    partial = {}        # (v,i) -> pair in progress
    starts_count = {}
    aux = {}            # (v,i) -> data for kills
    states_by_hole = {}
    try:
        guard.check(force=True)
        for h in range(n):
            states_by_hole[h] = deletion_states(rot, h, guard)
        for v, (i, c1, c2) in legal:
            starts_count[(v, i)] = sum(1 for s in states_by_hole[v]
                                       if s[c1[0]] != s[c1[1]] and s[c2[0]] != s[c2[1]])
        ld = mixed_distances(rot, states_by_hole, guard)
        for v in deg5:
            fans = [f for (w, f) in legal if w == v]
            if not fans:
                continue
            kd = kempe_distances(rot, v, states_by_hole[v], guard)
            for i, c1, c2 in fans:
                P = blank_pair(v, i, c1, c2, starts_count[(v, i)])
                partial[(v, i)] = P
                S = [s for s in states_by_hole[v] if s[c1[0]] != s[c1[1]] and s[c2[0]] != s[c2[1]]]
                worst, wstart = -1, None
                locked = {}
                A = {"S": S, "ell": {}, "kappa": {}}
                for s in S:
                    guard.check()
                    ell = ld.get(s)
                    kap = kappa_value(kd, s)
                    four = link_colours(rot, s) == 4
                    lk = four and kd.get(s) != 1
                    if four and lk != (ell is None or ell >= 2):
                        raise LemmaAFault(f"Lemma A mismatch v={v} fan={i} start={list(s)} "
                                          f"ell={ell} locked={lk}")
                    if not four:
                        assert ell == 0 and kd.get(s) == 0
                    locked[s] = lk
                    A["ell"][s], A["kappa"][s] = ell, kap
                    P["hist_l"]["capped" if ell is None else str(ell)] += 1
                    P["hist_k"][str(kap)] += 1
                    score = CAP_MIXED + 1 if ell is None else ell
                    if score > worst:
                        worst, wstart = score, s
                    P["L_at_least"] = max(P["L_at_least"], score)
                classes = tstar_classes(rot, (c1, c2), S, guard)
                bad = [c for c in classes if all(locked[s] for s in c)]
                P["tstar_classes"] = len(classes)
                P["locked_classes"] = len(bad)
                if not S:
                    P["L"], P["L_at_least"], P["unresolved_reason"] = None, 0, None
                    P["U"] = None  # vacuous; recorded as unknown, see report
                else:
                    capped = P["hist_l"]["capped"] > 0
                    P["L"] = None if capped else worst
                    P["L_at_least"] = worst
                    P["unresolved_reason"] = "capped" if capped else None
                    P["U"] = not bad
                    if worst >= 3:
                        P["witness_L"] = {"start": list(wstart),
                                          "path": None if ld.get(wstart) is None
                                          else path_to_fill(rot, wstart, ld)}
                    if bad:
                        P["u_fail_class"] = [list(s) for s in bad[0]]
                A["ld"], A["kd"] = ld, kd
                aux[(v, i)] = A
                done[(v, i)] = P
                del partial[(v, i)]
    except Interrupted as e:
        G["interrupted"] = str(e)
    for v, (i, c1, c2) in legal:
        if (v, i) in done:
            G["pairs"].append(done[(v, i)])
        elif (v, i) in partial:
            G["pairs"].append(partial[(v, i)])
        else:  # never reached: placeholder, counts unknown
            G["pairs"].append({"v": v, "fan_index": i, "chords": [list(c1), list(c2)],
                               "empty": False, "starts": None, "hist_l": {}, "hist_k": {},
                               "L": None, "L_at_least": 0, "tstar_classes": None,
                               "locked_classes": None, "U": None,
                               "unresolved_reason": "interrupted"})
    G["peak_rss_kb"] = peak_rss_kb()
    summarise(rot, G, aux)
    return G


def summarise(rot, G, aux):
    pairs = G["pairs"]
    nonempty = [P for P in pairs if not P["empty"]]
    G["unresolved_pairs"] = [[P["v"], P["fan_index"]] for P in pairs if P["unresolved_reason"]]
    G["m_at_least"] = min((P["L_at_least"] for P in nonempty), default=0)
    if pairs and not G["unresolved_pairs"] and G["interrupted"] is None and nonempty:
        G["m"] = min(P["L"] for P in nonempty)
    us = [P["U"] for P in pairs]
    if any(u is True for u in us):
        G["U_exists"] = True
    elif pairs and all(u is False for u in us) and G["interrupted"] is None:
        G["U_exists"] = False
    kills = []
    # M1, M2, M3: first start in (pair order, start order).
    found = {}
    for P in pairs:
        A = aux.get((P["v"], P["fan_index"]))
        if A is None:
            continue
        pr = [P["v"], P["fan_index"]]
        for s in A["S"]:
            ell, kap = A["ell"][s], A["kappa"][s]
            if "M1" not in found and (ell is None or ell >= 5):
                found["M1"] = {"stmt": "M1", "pair": pr, "start": list(s)}
            if "M2" not in found:
                if kap == "nofill":
                    found["M2"] = {"stmt": "M2", "pair": pr, "start": list(s), "kappa": "nofill"}
                elif ell is not None and (kap == "capped" or kap >= ell + 2):
                    lp = path_to_fill(rot, s, A["ld"])
                    found["M2"] = {"stmt": "M2", "pair": pr, "start": list(s), "l_path": lp,
                                   "kappa": "lower", "kappa_lower": len(lp) + 2}
            if "M3" not in found and ell == 2 and (kap in ("nofill", "capped") or kap > 2):
                found["M3"] = {"stmt": "M3", "pair": pr, "start": list(s),
                               "l_path": path_to_fill(rot, s, A["ld"])}
    kills += [found[k] for k in ("M1", "M2", "M3") if k in found]

    def c_cert(depth):
        per = []
        for P in pairs:
            A = aux.get((P["v"], P["fan_index"]))
            if A is None:
                return None
            s = next((s for s in A["S"] if A["ell"][s] is None or A["ell"][s] > depth), None)
            if s is None:
                return None
            per.append({"pair": [P["v"], P["fan_index"]], "start": list(s)})
        return per or None

    c1 = c_cert(2)
    if c1 and G["order"] >= 18:
        kills.append({"stmt": "C1", "per_pair": c1})
    c2 = c_cert(3)
    if c2:
        kills.append({"stmt": "C2", "per_pair": c2})
    if c1 and max(G["degrees"]) >= 7:
        kills.append({"stmt": "C3", "per_pair": c1})
    if pairs and G["U_exists"] is False and all("u_fail_class" in P for P in pairs):
        kills.append({"stmt": "U_exists"})
    G["kills"] = kills
