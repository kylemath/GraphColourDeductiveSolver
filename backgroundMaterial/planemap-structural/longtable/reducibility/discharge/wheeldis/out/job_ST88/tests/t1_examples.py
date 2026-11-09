# ST-88 T1: the two worked examples of PAYER8SPEC.md (sections 3.1 and 3.2) through code_gk8/gkfam.py.
import sys, collections
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else '/tmp/swarm-W17/code_gk8')
import gkfam as G
KEY = 'x EDGE(8->5)[S.L+1={5678} S.L-1=5 S.A-1=B R.L+2={5689}]'
k = G.parse_key(KEY); eng = G.Engine([k])
def nopmask(*a): raise AssertionError('pmask not expected (no link 6 near a payer)')
win = G.Win(eng, nopmask)
ok = True
# (a) receiver row R8 55558578/58585558: label 'R<d> <link>/<apex>', s_i between w_i and w_{i+1}
w = [int(c) for c in '55558578']; s = [int(c) for c in '58585558']
row = win.row(8, w, s)
U = 8; pay = sum(len(win.out_counts(U, *((w[(j-2)%8], w[(j-1)%8], w[j], w[(j+1)%8], w[(j+2)%8], s[(j-2)%8], s[(j-1)%8], s[j], s[(j+1)%8])))) for j in range(8))
get = sum(len(win.counts(U, *((w[(j-2)%8], w[(j-1)%8], w[j], w[(j+1)%8], w[(j+2)%8], s[(j-2)%8], s[(j-1)%8], s[j], s[(j+1)%8])))) for j in range(8))
# which (i, sg) OUT slots match
det = []
for j in range(8):
    wi = (w[(j-2)%8], w[(j-1)%8], w[j], w[(j+1)%8], w[(j+2)%8], s[(j-2)%8], s[(j-1)%8], s[j], s[(j+1)%8])
    op, om = G.Win.out_vecs(*wi)
    for sg, v in ((1, op), (-1, om)):
        if eng.out_hits(G.bit(8), G.bit(w[j]), v): det.append((j, sg))
print('T1a row R8 55558578/58585558 key %s: pay(OUT) %d get(IN) %d coefficient IN-OUT %d; OUT slots (i, sg) %s' % (KEY.split(None, 1)[1], pay, get, row['x'], det))
ok &= (pay, get, row['x']) == (4, 0, -4) and det == [(0, -1), (1, 1), (2, -1), (3, 1)]
# (b) sender row S 55868 BSBBS, six private class {3: S}: H_k = 1 for B (apex h_k between w_k, w_{k+1}), F_3 = 0 (S)
P = G.sender_pic([5, 5, 8, 6, 8], [1, 0, 1, 1, 0], [0, 0, 0, 0, 0])
o, i = eng.pic_counts(P)
det = []
for j in range(5):
    for e in (1, -1):
        if eng.in_hits(P.lk(j), P.C, P.in_vec(j, e)): det.append((j, -e))   # gkfam e (S.L+1 = w_{j+e}) = spec's -sg (S.L+1 = w_{j-sg})
print('T1b sender S 55868 BSBBS {3: S}: pay(OUT) %d get(IN) %d coefficient OUT-IN %d; IN slots (payer j, spec sg) %s' % (o['x'], i['x'], o['x'] - i['x'], det))
ok &= (o['x'], i['x']) == (0, 2) and det == [(2, -1), (4, 1)]
print('T1 %s' % ('PASS' if ok else 'FAIL'))
