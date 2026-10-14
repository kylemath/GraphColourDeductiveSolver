"""B8b (exploratory): analyse the degree-5 vertices within distance 2 of a centre u in an explicit graph:
their 2-ball keys, number of big (>= 7) vertices, whether u is the only big one, and the status of the key in
the complete K <= 1 list (b8b/out/k1keys.tsv: R / notD / U)."""
import sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import ball, h0

_K1 = None
def k1():
    global _K1
    if _K1 is None:
        _K1 = {}
        for line in open(os.path.join(HERE, 'out', 'k1keys.tsv')):
            f = line.rstrip('\n').split('\t'); _K1[f[0]] = (f[5], f[6], f[3])
    return _K1


def dist_from(rot, u, R=2):
    d = {u: 0}; fr = [u]
    for k in range(1, R + 1):
        nf = []
        for x in fr:
            for y in rot[x]:
                if y not in d: d[y] = k; nf.append(y)
        fr = nf
    return d


def senders(rot, u):
    deg = [len(r) for r in rot]; D = dist_from(rot, u, 2); out = []
    for v, dv in sorted(D.items(), key=lambda z: (z[1], z[0])):
        if dv == 0 or deg[v] != 5: continue
        w, key, st = ball.ball_at(rot, v)
        B = dist_from(rot, v, 2)
        big = sorted(x for x in B if deg[x] >= 7)
        ks = ball.key_str(key) if key else None
        word = ''.join(map(str, ball.wheel_canon(w)))
        stat = k1().get(ks, ('K>=2' if len(big) >= 2 else '?', '', ''))
        out.append(dict(v=v, dist=dv, word=word, key=ks, regular=st, big=big, lone=(big == [u]), status=stat[0],
                        detail=stat[1], pos=stat[2]))
    return out


def report(rot, u, title=''):
    S = senders(rot, u); deg = [len(r) for r in rot]
    lone = [s for s in S if s['lone']]
    print('== %s: n=%d deg(u)=%d; 5s within distance 2: %d; lone-u: %d (66666: %d); lone-u non-R: notD %d, U %d' % (
        title, len(rot), deg[u], len(S), len(lone), sum(s['word'] == '66666' for s in lone),
        sum(s['status'] == 'notD' for s in lone), sum(s['status'] == 'U' for s in lone)))
    for s in S:
        print('   v=%d dist %d word %s lone=%s %s/%s pos=%s key %s %s' % (s['v'], s['dist'], s['word'], s['lone'],
              s['status'], s['detail'], s['pos'], s['key'], '' if s['regular'] == 'ok' else s['regular']))
    return S


def write_graph(fn, name, rot):
    with open(fn, 'a') as f:
        f.write('%s %d %s\n' % (name, len(rot), ';'.join(','.join(map(str, r)) for r in rot)))
