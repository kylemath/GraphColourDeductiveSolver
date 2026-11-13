import sys, pickle, json; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT
W.init(); ns = W.NS
labs = pickle.load(open('data/world57.pkl', 'rb')); mine = {(l[2], l[3]) for l in labs if l[0] == 'R'}
J = json.load(open('/mnt/project-files/swarm/round6/W6-rule-grammar/round3/floor57.json'))
for wgt, rs in J['receivers']:
    lk, sv = rs.split('/'); w = tuple(int(c) for c in lk); s = tuple(int(c) for c in sv); c = TT.canon_ws(w, s)
    why = W.admissible_fast(7, w, s); st = ns['admissible'](7, list(w), list(s))
    print(rs, 'w', round(wgt, 4), 'in mine', c in mine, 'fast', why, 'st21', st)
