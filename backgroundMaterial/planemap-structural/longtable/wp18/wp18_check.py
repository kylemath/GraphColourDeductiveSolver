"""WP18 independent checker, amended 5 October to the audit's certificate contract.

Does not import wp18_core. For each graph record in a phase output it checks:
  * graph: parsed from the recorded ASCII, hash matches, simple spherical triangulation,
    minimum degree 5;
  * coverage: the rows are exactly the legal (degree-5 vertex, fan) pairs, enumerated here
    independently, and each row's chords are the named fan's chords at the named vertex;
  * witnesses: the start has length n, colours in {0,1,2,3}, exactly one hole at v, is proper,
    and both chords are bichromatic. The recorded path replays (whole Kempe components, legal
    singleton slides) and ends filled with exactly L moves. Every earlier breadth-first layer
    is enumerated here and contains no filled state, so the witness start's distance is exactly
    L, which certifies L(v,tau) >= L as a lower bound;
  * capped rows: start validity only, reported as lower bounds (>= cap+1);
  * interrupted graphs: reported as incomplete.
Upper bounds (that no start at a pair needs more than L) are producer claims; this checker
certifies them only for rows with L <= 1 by checking nothing, so they are listed as unverified.
A graph's m(T) >= k is certified when every legal pair carries a witness certified at >= k.
"""
import hashlib
import json
import sys
from itertools import combinations
from multiprocessing import Pool

HOLE = 4


def parse(line):
    n, code = line.strip().split(" ", 1)
    rot = [[ord(c) - 97 for c in row] for row in code.split(",")]
    if len(rot) != int(n):
        raise ValueError("vertex count")
    return rot


def check_graph(rot):
    n = len(rot)
    for v, ns in enumerate(rot):
        if len(ns) < 5 or len(set(ns)) != len(ns) or v in ns or any(v not in rot[w] for w in ns):
            raise ValueError(f"bad neighbourhood at {v}")
    e = sum(map(len, rot)) // 2
    if e != 3 * n - 6:
        raise ValueError("edge count")
    seen, faces = set(), 0
    for v, ns in enumerate(rot):
        for w in ns:
            if (v, w) in seen:
                continue
            d, k = (v, w), 0
            while d not in seen:
                seen.add(d)
                k += 1
                a, b = d
                d = (b, rot[b][(rot[b].index(a) + 1) % len(rot[b])])
            if k != 3:
                raise ValueError("non-triangular face")
            faces += 1
    if n - e + faces != 2:
        raise ValueError("Euler characteristic")


def legal_pairs(rot):
    out = {}
    for v, link in enumerate(rot):
        if len(link) != 5:
            continue
        for i in range(5):
            a, far, near = link[i], link[(i + 2) % 5], link[(i + 3) % 5]
            if far not in rot[a] and near not in rot[a]:
                out[(v, i)] = {frozenset((a, far)), frozenset((a, near))}
    return out


def relabel(st):
    m = {}
    return tuple(HOLE if x == HOLE else m.setdefault(x, len(m)) for x in st)


def proper(rot, st):
    return all(st[x] == HOLE or st[y] == HOLE or st[x] != st[y] for x in range(len(rot)) for y in rot[x])


def is_filled(rot, st):
    h = st.index(HOLE)
    return len({st[w] for w in rot[h]}) <= 3


def apply(rot, st, mv):
    h = st.index(HOLE)
    if mv[0] == "K":
        _, a, b, x0 = mv
        if st[x0] not in (a, b):
            raise ValueError("Kempe seed not in pair")
        comp, todo = {x0}, [x0]
        while todo:
            x = todo.pop()
            for y in rot[x]:
                if y not in comp and st[y] in (a, b):
                    comp.add(y)
                    todo.append(y)
        if min(comp) != x0:
            raise ValueError("seed is not the component minimum")
        return relabel([(b if st[x] == a else a) if x in comp else st[x] for x in range(len(st))])
    if mv[0] == "S":
        u = mv[1]
        if u not in rot[h]:
            raise ValueError("slide target not adjacent to hole")
        if [st[w] for w in rot[h]].count(st[u]) != 1:
            raise ValueError("slide colour not singleton on link")
        nx = list(st)
        nx[h], nx[u] = st[u], HOLE
        return relabel(nx)
    raise ValueError("unknown move")


def successors(rot, st):
    """Every state one move away: each whole bichromatic component, each legal slide."""
    h = st.index(HOLE)
    out = set()
    for a, b in combinations(range(4), 2):
        done = set()
        for x0 in range(len(st)):
            if st[x0] in (a, b) and x0 not in done:
                comp, todo = {x0}, [x0]
                while todo:
                    x = todo.pop()
                    for y in rot[x]:
                        if y not in comp and st[y] in (a, b):
                            comp.add(y)
                            todo.append(y)
                done |= comp
                out.add(relabel([(b if st[x] == a else a) if x in comp else st[x] for x in range(len(st))]))
    link = [st[w] for w in rot[h]]
    for u in rot[h]:
        if link.count(st[u]) == 1:
            nx = list(st)
            nx[h], nx[u] = st[u], HOLE
            out.add(relabel(nx))
    return out


def no_fill_before(rot, st, k):
    """True if no state at distance < k from st is filled (complete layer enumeration)."""
    seen = {st}
    layer = [st]
    for depth in range(k):
        if any(is_filled(rot, x) for x in layer):
            return False
        if depth == k - 1:
            break
        nxt = []
        for x in layer:
            for y in successors(rot, x):
                if y not in seen:
                    seen.add(y)
                    nxt.append(y)
        layer = nxt
    return True


def check_start(rot, v, chords, start):
    st = tuple(start)
    if len(st) != len(rot) or any(x not in (0, 1, 2, 3, HOLE) for x in st):
        raise ValueError("state length or alphabet")
    if st.count(HOLE) != 1 or st.index(HOLE) != v or not proper(rot, st):
        raise ValueError("start is not a proper colouring of T - v")
    for a, b in chords:
        if st[a] == st[b] or b in rot[a]:
            raise ValueError("chord not bichromatic or already an edge")
    return st


def check_row(rot, row, cap):
    v = row["v"]
    st = check_start(rot, v, row["chords"], row["witness"]["start"])
    moves = row["witness"]["moves"]
    if moves is None:
        if row["L"] is not None:
            raise ValueError("pathless witness on an uncapped row")
        return ("capped", cap + 1)
    L = row["L"]
    if L is None or len(moves) != L:
        raise ValueError("move count differs from L")
    if not no_fill_before(rot, st, L):
        raise ValueError(f"a fill exists at depth < {L}")
    cur = st
    for mv in moves:
        cur = apply(rot, cur, tuple(mv))
        if not proper(rot, cur):
            raise ValueError("improper after move")
    if not is_filled(rot, cur):
        raise ValueError("final link uses four colours")
    return ("exact", L)


def check_graph_record(args):
    g, cap = args
    if g.get("interrupted"):
        return {"key": [g["order"], g["graph_index"]], "interrupted": True}
    if hashlib.sha256(g["ascii"].encode()).hexdigest() != g["ascii_sha256"]:
        raise ValueError("ascii hash")
    rot = parse(g["ascii"])
    check_graph(rot)
    legal = legal_pairs(rot)
    rows = g["report"]["rows"]
    keys = [(r["v"], r["fan_index"]) for r in rows]
    if len(set(keys)) != len(keys) or set(keys) != set(legal):
        raise ValueError(f"pair coverage at {g['order']}:{g['graph_index']}")
    certified = {}
    for r in rows:
        if {frozenset(c) for c in r["chords"]} != legal[(r["v"], r["fan_index"])]:
            raise ValueError("chords are not the named fan")
        lb = 0
        if "witness" in r:
            kind, lb = check_row(rot, r, cap)
        elif r["L"] is None or r["L"] >= 2:
            raise ValueError("row with L >= 2 lacks a witness")
        certified[(r["v"], r["fan_index"])] = lb
    return {"key": [g["order"], g["graph_index"]], "pairs": len(rows),
            "witnesses": sum(1 for r in rows if "witness" in r),
            "m_lower_certified": min(certified.values()), "producer_m": g["report"]["m"]}


def main(path, procs=12):
    data = json.load(open(path))
    cap = data["cap"]
    with Pool(procs) as pool:
        res = pool.map(check_graph_record, [(g, cap) for g in data["graphs"]], chunksize=1)
    done = [r for r in res if not r.get("interrupted")]
    summary = {
        "file": path,
        "graphs": len(res),
        "interrupted": [r["key"] for r in res if r.get("interrupted")],
        "pairs_covered": sum(r["pairs"] for r in done),
        "witnesses_certified_exact": sum(r["witnesses"] for r in done),
        "graphs_m_ge_3_certified": [r["key"] for r in done if r["m_lower_certified"] >= 3],
        "graphs_m_ge_2_certified": sum(1 for r in done if r["m_lower_certified"] >= 2),
        "upper_bounds": "producer claims, not certified here",
    }
    print(json.dumps(summary))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        main(p)
