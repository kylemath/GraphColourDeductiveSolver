"""[exploratory] Item 19 task 4 helper: abstract single-Kempe-swap neighbours of a link word.
A swap of colours {p,q} on one component flips p<->q on a set K of link vertices. Link-adjacent p/q vertices are adjacent in G, hence in the
same component, so K is a union of 'runs' (maximal arcs of the link whose colours alternate p,q). We list
 N_run   = filled words reachable by flipping ONE run (the least the component must contain),
 N_union = filled words reachable by flipping any union of runs of one colour pair (a component may link several runs through the interior)."""
import itertools
from lib import canon, is_filled

def runs(w, p, q):
    d = len(w); idx = [i for i in range(d) if w[i] in (p, q)]
    seen = set(); out = []
    for i in idx:
        if i in seen: continue
        comp = {i}; st = [i]
        while st:
            x = st.pop()
            for y in ((x + 1) % d, (x - 1) % d):
                if w[y] in (p, q) and y not in comp: comp.add(y); st.append(y)
        seen |= comp; out.append(sorted(comp))
    return out

def flip(w, K, p, q):
    return canon([(q if x == p else p) if i in K else x for i, x in enumerate(w)])

def neighbours(w):
    run, uni = set(), set()
    for p, q in itertools.combinations(range(4), 2):
        R = runs(w, p, q)
        for r in range(1, len(R) + 1):
            for sub in itertools.combinations(R, r):
                K = set(x for c in sub for x in c); t = flip(w, K, p, q)
                if t != w and is_filled(t):
                    uni.add(t)
                    if r == 1: run.add(t)
    return run, uni
