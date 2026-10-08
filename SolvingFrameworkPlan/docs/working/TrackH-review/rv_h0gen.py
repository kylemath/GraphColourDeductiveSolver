"""Item 2b: Lemma H0 on random GENERAL graphs (H0 is claimed for any graph), plus the 6-vertex
wheel test of H0's literal first sentence.
Usage: python3 rv_h0gen.py NGRAPHS SEED OUTJSON"""
import sys
import json
import random
from collections import Counter
import rv_core as R


def wheel_example():
    # h = 0, link 1..5 a 5-cycle, nothing else.  Colouring s = (alpha, mu, A, alpha, B) at x_0..x_4.
    adj = [[1, 2, 3, 4, 5], [0, 2, 5], [0, 1, 3], [0, 2, 4], [0, 3, 5], [0, 4, 1]]
    x = adj[0]
    s = (-1, 0, 1, 2, 0, 3)
    inf = R.state_info(adj, 0, x, s)
    ps = R.pi_map(adj, 0, x, s, inf)
    preimgs = [t for t in R.colourings(adj, 0, canonical=True)
               if R.state_info(adj, 0, x, t) is not None and R.pi_map(adj, 0, x, t) is not None
               and R.canon(R.pi_map(adj, 0, x, t)) == R.canon(s)]
    return dict(L1=inf['L1'], L2=inf['L2'], inA=inf['inA'], inB=inf['inB'], D1=inf['D1'], D2=inf['D2'],
                pi_defined=ps is not None, n_unfilled_preimages=len(preimgs))


def random_graph(rng):
    n = rng.randint(9, 16)
    p = rng.uniform(0.25, 0.55)
    S = [set() for _ in range(n)]
    def add(u, v):
        S[u].add(v); S[v].add(u)
    for i in range(1, 6):
        add(0, i)
        add(i, i % 5 + 1)
    for u in range(1, n):
        for v in range(u + 1, n):
            if u <= 5 and v <= 5:
                continue  # keep link induced
            if rng.random() < p:
                add(u, v)
    return [sorted(s) if v else [1, 2, 3, 4, 5] for v, s in enumerate(S)]


BASES = []
for fn in ('../TrackH/lp_general_min.txt', '../TrackH/lpc_general_min.txt', '../TrackH/lpc_general_40.txt'):
    BASES.append(R.parse_line(open(fn).readline())[1])


def perturbed(rng):
    """Toggle 1-6 random edges of a Track H counterexample graph (not at h, link kept induced)."""
    adj = rng.choice(BASES)
    n = len(adj)
    S = [set(a) for a in adj]
    link = set(adj[0])
    for _ in range(rng.randint(1, 6)):
        u, v = rng.sample(range(1, n), 2)
        if u in link and v in link:
            continue
        if v in S[u]:
            S[u].discard(v); S[v].discard(u)
        else:
            S[u].add(v); S[v].add(u)
    return [list(adj[0])] + [sorted(s) for s in S[1:]]


def main():
    ng, seed, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    mode = sys.argv[4] if len(sys.argv) > 4 else 'random'
    rng = random.Random(seed)
    T = Counter()
    for _ in range(ng):
        adj = random_graph(rng) if mode == 'random' else perturbed(rng)
        h, x = 0, list(adj[0])
        cols = R.colourings(adj, h, canonical=True)
        if not cols:
            continue
        T['graphs'] += 1
        info = {c: R.state_info(adj, h, x, c) for c in cols}
        pimg = {}
        for c, inf in info.items():
            if inf is not None:
                p = R.pi_map(adj, h, x, c, inf)
                pimg[c] = R.canon(p) if p is not None else None
        pre = Counter(v for v in pimg.values() if v is not None)
        for s, ps in pimg.items():
            if pre[s] and ps is not None:
                T['H0_literal_checked'] += 1
                if not (info[s]['D1'] and info[s]['D2']):
                    T['H0_literal_FAIL'] += 1
                    if not info[s]['DL']:
                        T['H0_literal_FAIL_nonDL'] += 1
        seen = set()
        for c0 in pimg:
            if c0 in seen:
                continue
            path, cur = [c0], pimg[c0]
            while cur is not None and cur not in path:
                path.append(cur)
                cur = pimg[cur]
            if cur == c0:
                seen.update(path)
                if all(info[s]['DL'] for s in path):
                    T['allDL_cycles'] += 1
                    T['allDL_cycle_states'] += len(path)
                    T['H0_cycle_FAIL'] += sum(1 for s in path if not (info[s]['D1'] and info[s]['D2']))
    res = dict(wheel=wheel_example(), tally=dict(T))
    json.dump(res, open(out, 'w'))
    print(json.dumps(res))


if __name__ == '__main__':
    main()
