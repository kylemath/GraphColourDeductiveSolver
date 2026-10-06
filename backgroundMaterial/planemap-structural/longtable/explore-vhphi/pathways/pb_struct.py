"""[exploratory] degree-5 subgraph structure; icosahedral vertices; for T4, A_3, order-14 bicapped hex antiprism, order-42 GC(2,0) icosahedron."""
import itertools
from pb_lib import *
def stats(name, adj):
    deg = {u: len(adj[u]) for u in adj}
    d5 = [u for u in adj if deg[u] == 5]
    ico = [u for u in d5 if all(deg[w] == 5 for w in adj[u])]
    seen = set(); cs = []
    for s in d5:
        if s in seen: continue
        K = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if deg[w] == 5 and w not in K: K.add(w); st.append(w)
        seen |= K; cs.append(sorted(K))
    print(f"[exploratory] {name}: n={len(adj)} deg-multiset={sorted(deg.values())}")
    print("   degree-5 components:", [(len(c), [u for u in c if u in ico]) for c in cs])
    print("   icosahedral vertices:", ico)
    return deg, d5, ico, cs
def hexanti():
    adj = {}
    def e(a, b): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    for t in range(6):
        e(('a', t), ('a', (t+1) % 6)); e(('b', t), ('b', (t+1) % 6))
        e(('a', t), ('b', t)); e(('a', t), ('b', (t+1) % 6)); e('N', ('a', t)); e('S', ('b', t))
    return relabel(adj)[0]
def gc20():
    # icosahedron from antiprism: ring a(5), ring b(5), poles; then 1-to-4 split of every triangle
    adj = {}
    def e(a, b): adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    faces = []
    for t in range(5):
        faces += [('N', ('a', t), ('a', (t+1) % 5)), ('S', ('b', t), ('b', (t+1) % 5)),
                  (('a', t), ('a', (t+1) % 5), ('b', (t+1) % 5)), (('b', t), ('b', (t+1) % 5), ('a', t))]
    mid = lambda x, y: ('m',) + tuple(sorted([str(x), str(y)]))
    for f in faces:
        x, y, z = f; m = [mid(x, y), mid(y, z), mid(z, x)]
        for a, b in [(x, m[0]), (m[0], y), (y, m[1]), (m[1], z), (z, m[2]), (m[2], x), (m[0], m[1]), (m[1], m[2]), (m[2], m[0])]: e(a, b)
    return relabel(adj)[0]
if __name__ == '__main__':
    stats('T4', from_faces(T4F))
    stats('A_3', a3()[0])
    stats('hex-antiprism+2 caps', hexanti())
    stats('GC(2,0) icosahedron (42)', gc20())
