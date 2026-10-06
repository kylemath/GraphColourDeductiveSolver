"""LEAD's independent check of the Conjecture L counterexamples. Written from Math's definitions only
(MathConfinementAttack Step 1, MathCleanVertexAttack Theorem C): shares no code with the L-Attack team.
Data in: oriented triangles + proper 4-colouring of T-v. Standard library only."""
import os, re, sys
from collections import deque
HERE = os.path.dirname(os.path.abspath(__file__))

def rotation(faces):
    succ = {}
    for a, b, c in faces:
        for u, p, q in ((a, b, c), (b, c, a), (c, a, b)):
            assert p not in succ.setdefault(u, {}), "inconsistent faces"
            succ[u][p] = q
    rot = {}
    for u, m in succ.items():
        start = next(iter(m)); cyc = [start]; x = m[start]
        while x != start:
            cyc.append(x); x = m[x]
        assert len(cyc) == len(m), "vertex link is not one cycle"
        rot[u] = cyc
    return rot

def check_triangulation(faces, rot):
    n = len(rot); E = sum(len(r) for r in rot.values()) // 2
    adj = {u: set(r) for u, r in rot.items()}
    assert all(u not in adj[u] for u in adj) and all(u in adj[w] for u in adj for w in adj[u])
    assert len(faces) == 2 * n - 4 and E == 3 * n - 6, (n, E, len(faces))
    return adj

def component(adj, col, start, colours, banned):
    seen = {start}; q = deque([start])
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w != banned and w not in seen and col[w] in colours:
                seen.add(w); q.append(w)
    return seen

def analyse(adj, ring, col, v):
    link = [col[x] for x in ring]
    if len(set(link)) != 4: return None
    js = [j for j in range(5) if link[j] == link[(j + 2) % 5]]
    assert len(js) == 1
    j = js[0]; a, b, g, d = link[j], link[(j + 1) % 5], link[(j + 3) % 5], link[(j + 4) % 5]
    x = lambda k: ring[(j + k) % 5]
    p1 = x(3) in component(adj, col, x(1), {b, g}, v)       # beta-gamma path x1 ~ x3
    p2 = x(4) in component(adj, col, x(1), {b, d}, v)       # beta-delta path x1 ~ x4
    return j, (a, b, g, d), p1 and p2

def F(adj, ring, col, v, j):
    link = [col[x] for x in ring]; a = link[j]; g = link[(j + 3) % 5]
    comp = component(adj, col, ring[(j + 2) % 5], {a, g}, v)
    new = dict(col)
    for u in comp: new[u] = g if col[u] == a else a
    return new

def run(faces, v, col, maxsteps=130, label=""):
    rot = rotation(faces); adj = check_triangulation(faces, rot)
    assert len(rot[v]) == 5
    ring = rot[v]
    for u in col:   # properness on T - v
        assert all(col[u] != col[w] for w in adj[u] if w != v and w in col), "improper colouring"
    assert set(col) == set(rot) - {v}
    states = []; cur = dict(col); chain = 0; seen = {}
    for step in range(maxsteps):
        key = tuple(sorted(cur.items()))
        if key in seen: 
            print(f"{label}: orbit closed at step {step}, period {step - seen[key]} (raw colours); chain length so far {chain}")
            break
        seen[key] = step
        r = analyse(adj, ring, cur, v)
        if r is None or not r[2]:
            print(f"{label}: chain of consecutive doubly locked states has length {chain}; state {step} is not doubly locked"); break
        chain += 1
        cur = F(adj, ring, cur, v, r[0])
    else:
        print(f"{label}: all {chain} iterates doubly locked, no closure within {maxsteps} steps")
    return chain

if __name__ == "__main__":
    # --- W6: from the report text
    rep = open(os.path.join(HERE, "../../../../SolvingFrameworkPlan/docs/working/creative-intel-2026-10-05/l-attack.md")).read().split("\n")
    fl = next(l for l in rep if l.startswith("Witness W6")); cl = next(l for l in rep if l.startswith("Colours (vertex:colour)"))
    faces6 = [tuple(map(int, m.groups())) for m in re.finditer(r"\[(\d+),(\d+),(\d+)\]", fl)]
    col6 = {int(a): int(b) for a, b in re.findall(r"(\d+):(\d+)", cl.split("Link of v")[0].split("):")[1])}
    c6 = run(faces6, 16, col6, label="W6 (20 vertices)")
    # --- A_3: from the team's data file, constants only (no team code executed)
    src = open(os.path.join(HERE, "lattack_witness.py")).read()
    faces3 = eval(re.search(r"^A3_FACES\s*=\s*(.+)$", src, re.M).group(1))
    col3 = eval(re.search(r"^A3_COL\s*=\s*(.+)$", src, re.M).group(1))
    c3 = run(faces3, 0, col3, label="A_3 (17 vertices)")
    print("vertices/degrees of A_3:", sorted(len(r) for r in rotation(faces3).values()))
