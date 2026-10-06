#!/usr/bin/env python3
"""studiointel fcycle_census.py -- [exploratory] Fellow F's computation 2 (FellowF-55656.md sec.7; Lemma O, Lemma Gamma).
At every degree-5 hole whose cyclic link degrees are (5,5,6,5,6) up to rotation/reflection: iterate F on EXACT (labelled) colourings
of T - v starting from every DL state. F(s) = swap the {alpha, c(x_{j+3})}-component of x_{j+2} (repeat alpha at x_j, x_{j+2}).
An orbit either leaves the DL set (path) or returns to the exact starting colouring (cycle). Record every cycle once, with its
labelled length and its length in canonical (renaming-quotient) states. Kill condition: a cycle whose labelled length is not a
multiple of 15 (Lemma O)."""
import sys, json
from collections import Counter
sys.path.insert(0, '.')
import radius, graphs
from r55566_test import graphs_from

def comp(nb, col, s, cols):
    K = {s}; st = [s]
    while st:
        u = st.pop()
        for w in nb[u]:
            if w not in K and col[w] in cols: K.add(w); st.append(w)
    return K

def F(nb, link, col):
    lc = [col[x] for x in link]; j = [j for j in range(5) if lc[j] == lc[(j + 2) % 5]][0]
    x2, x3 = link[(j + 2) % 5], link[(j + 3) % 5]; al, A = col[x2], col[x3]
    K = comp(nb, col, x2, (al, A)); new = list(col)
    for u in K: new[u] = A if col[u] == al else al
    return tuple(new)

def is55656(ds): 
    for k in range(5):
        r = ds[k:] + ds[:k]
        if r in ((5,5,6,5,6), (6,5,6,5,5)): return True
    return False

def main():
    cycles = []; res = Counter(); canon_len = Counter(); kills = []; nholes = 0; paths = 0
    for arg in sys.argv[1:]:
        for name, Fc in graphs_from(arg):
            if graphs.n_separating_triangles(Fc): continue
            deg = graphs.degrees(Fc)
            for v in sorted(u for u in deg if deg[u] == 5):
                order, idx, nb, link = radius.prepare(Fc, v)
                ds = tuple(deg[order[i]] for i in link)
                if not is55656(ds): continue
                nholes += 1; seen = set()
                for s in radius.enumerate_states(nb, 10 ** 7):
                    if radius.classify(nb, link, s) != 2 or s in seen: continue
                    orb = [s]; cur = s; cyc = False
                    while True:
                        cur = F(nb, link, cur)
                        if cur == s: cyc = True; break
                        if radius.classify(nb, link, cur) != 2: break
                        orb.append(cur)
                        if len(orb) > 100000: break
                    if not cyc: paths += 1; continue
                    cs = frozenset(radius.canon(x) for x in orb)
                    key = (name, v, min(cs))
                    if key in seen: continue
                    seen.add(key); seen.update(orb)
                    L = len(orb); res[L] += 1; canon_len[len(cs)] += 1; cycles.append({'graph': name, 'hole': v, 'link_degrees': ds, 'labelled_length': L, 'canonical_length': len(cs)})
                    if L % 15: kills.append({'graph': name, 'hole': v, 'labelled_length': L, 'state': list(s)})
    print(json.dumps({'holes_55656': nholes, 'DL_orbits_ending_in_paths_(starts)': paths, 'cycle_labelled_lengths': dict(sorted(res.items())),
                      'cycle_canonical_lengths': dict(sorted(canon_len.items())), 'kills_not_mult_15': len(kills), 'first_kills': kills[:3], 'cycles': cycles[:50]}))

if __name__ == '__main__':
    main()
