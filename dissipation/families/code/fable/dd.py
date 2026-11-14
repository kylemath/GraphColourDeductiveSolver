"""Idea B: the transfer function F_h(hub 2-ball, target) = sum of weights of fitting parts,
stored as a reduced multi-valued decision diagram (one per hub degree).
Variables, read outward from the target (slot 2): spoke degree, hat degree, then the spoke's fans
(only when the spoke is exactly 6, 7 or 8). Edges are labelled by degree INTERVALS (maximal runs of
values with the same child), so 'nodes' and 'edges' are comparable to parts and literals.
Canonical: two rule sets with the same F give the same diagram, however F was cut into parts."""
import sys, collections as C
from common import *
sys.setrecursionlimit(10000)

def order(h, mode):
    if mode == 'plain': return list(range(h))
    o = [2]
    for k in range(1, h):
        for j in ((2 + k) % h, (2 - k) % h):
            if j not in o: o.append(j)
    return o

def build(boxes, h, mode='centre'):
    """boxes: list of (weight, slots)."""
    od = order(h, mode)
    uniq = {}; nodes = []
    def mk(children):
        # children: tuple of 5 child ids for values 5..9
        if all(c == children[0] for c in children): return children[0]
        k = ('n', children)
        if k not in uniq: uniq[k] = len(nodes); nodes.append(children)
        return uniq[k]
    def term(v):
        k = ('t', v)
        if k not in uniq: uniq[k] = len(nodes); nodes.append(v)
        return uniq[k]
    memo = {}
    # state: (pos index in od, stage) stage 0=sp,1=hat,2+k=fan k ; spv = current spoke value
    def rec(pos, stage, spv, live):
        if not live: return term(0)
        if pos == h: return term(sum(boxes[i][0] for i in live))
        key = (pos, stage, spv if stage >= 1 else 0, live)
        if key in memo: return memo[key]
        j = od[pos]
        if stage == 0:
            ch = []
            for v in range(5, 10):
                l2 = frozenset(i for i in live if boxes[i][1][j][0][0] <= v <= boxes[i][1][j][0][1])
                ch.append(rec(pos, 1, v, l2))
        elif stage == 1:
            ch = []
            nf = spv - 5 if 6 <= spv <= 8 else 0
            for v in range(5, 10):
                l2 = frozenset(i for i in live if boxes[i][1][j][1][0] <= v <= boxes[i][1][j][1][1])
                ch.append(rec(pos, 2, spv, l2) if nf else rec(pos + 1, 0, 0, l2))
        else:
            k = stage - 2; nf = spv - 5
            ch = []
            for v in range(5, 10):
                l2 = frozenset(i for i in live if not boxes[i][1][j][2] or
                               boxes[i][1][j][2][k][0] <= v <= boxes[i][1][j][2][k][1])
                ch.append(rec(pos, stage + 1, spv, l2) if k + 1 < nf else rec(pos + 1, 0, 0, l2))
        r = mk(tuple(ch)); memo[key] = r
        return r
    root = rec(0, 0, 0, frozenset(range(len(boxes))))
    inner = [n for n in nodes if isinstance(n, tuple)]
    edges = sum(1 + sum(1 for a, b in zip(n, n[1:]) if a != b) for n in inner)
    terms = sorted(n for n in nodes if not isinstance(n, tuple))
    return dict(nodes=len(inner), edges=edges, values=terms)

def run(P, mode):
    tot = C.Counter(); per = {}
    for h in (5, 6, 7, 8):
        B = [(p['w'], norm(p)[1]) for p in P if p['hub'] == h]
        r = build(B, h, mode); per[h] = (len(B), r['nodes'], r['edges'], r['values'])
        tot['nodes'] += r['nodes']; tot['edges'] += r['edges']
    return tot, per

if __name__ == '__main__':
    P = load()
    for mode in ('centre', 'plain'):
        for lab, Q in [('real', P)] + [(f'null{i}', q) for i, q in enumerate(nulls(P))]:
            tot, per = run(Q, mode)
            print(mode, lab, dict(tot), {h: v[:3] for h, v in per.items()}, 'values', {h: v[3] for h, v in per.items()} if lab == 'real' else '')
    # mirror-quotient: keep one part per mirror pair -> diagram of the "half" function
    for pre in ('drule', 'SP_', 'ST'):
        Q = [p for p in P if p['pre'].startswith(pre)]
        tot, per = run(Q, 'centre'); print(pre, len(Q), dict(tot))
