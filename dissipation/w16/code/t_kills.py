import sys, pickle; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT
ARGV = list(sys.argv); W.init()
found = pickle.load(open(ARGV[1], 'rb'))
for key, P in found.items():
    T = TT.Torus(P['n'], P['faces']); T.check()
    for v in range(T.n):
        if T.deg[v] >= 7:
            w, s, r, ap = TT.words(T, v); pv = W.privates(T, v)
            print(v, T.deg[v], w, s, pv, W.payee_kills(T.deg[v], w, s, pv))
