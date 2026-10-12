"""Item 3: rigid isolation (RI) on sphere triangulations, own rigidity computation.
Input formats per line:  'name n a,b;c,d;...'  (Census29)   or plantri -a ascii 'n bcd,acd,...'.
Usage: python3 rv_ri.py OUTJSON FILE [stride offset] [maxgraphs] [exclude_names_file]"""
import sys
import json
from collections import Counter
import rv_core as R


def parse_any(line):
    t = line.split()
    if len(t) >= 3 and ';' in t[2]:
        return R.parse_line(line)
    # plantri ascii: n then comma-separated letter lists (a = vertex 0)
    n = int(t[0])
    rows = t[1].split(',')
    assert len(rows) == n
    return f'pl{n}', [[ord(ch) - 97 for ch in r] for r in rows]


def is_sphere_triangulation(adj):
    n = len(adj)
    E = sum(map(len, adj)) // 2
    if E != 3 * n - 6 or R.validate_simple(adj):
        return False
    # rotation check: consecutive neighbours adjacent (faces are triangles)
    S = [set(a) for a in adj]
    for v in range(n):
        d = len(adj[v])
        for i in range(d):
            if adj[v][(i + 1) % d] not in S[adj[v][i]]:
                return False
    # face count via rotation system (assumes lists are rotations): count face orbits
    pos = {(v, w): i for v in range(n) for i, w in enumerate(adj[v])}
    seen = set()
    F = 0
    for v in range(n):
        for w in adj[v]:
            if (v, w) in seen:
                continue
            F += 1
            a, b = v, w
            while (a, b) not in seen:
                seen.add((a, b))
                # next dart in face: at b, the neighbour after a (one orientation)
                i = pos[(b, a)]
                c = adj[b][(i - 1) % len(adj[b])]
                a, b = b, c
    return n - E + F == 2


def run_graph(adj, tally, examples, name):
    n = len(adj)
    for h in range(n):
        if len(adj[h]) != 5:
            continue
        x = adj[h]  # rotation order
        tally['holes'] += 1
        cols = R.colourings(adj, h, canonical=True)
        for c in cols:
            inf = R.state_info(adj, h, x, c)
            tally['states'] += 1
            if inf is None:
                continue
            if not (inf['D1'] and inf['D2']):
                tally['D_FAIL'] += 1
            if not (inf['P1'] and inf['P2'] and inf['P3']):
                tally['P_FAIL'] += 1
            if not inf['DL']:
                continue
            tally['DL'] += 1
            cnt = R.pair_counts(adj, h, x, c, inf)
            if any(a < b for a, b in zip(cnt, R.RIGID)):
                tally['H4_FAIL'] += 1
            if cnt != R.RIGID:
                continue
            tally['rigid'] += 1
            p = R.pi_map(adj, h, x, c, inf)
            if p is None:
                tally['pi_undefined'] += 1
                continue
            pi_inf = R.state_info(adj, h, x, p)
            if pi_inf is None:
                tally['pi->filled'] += 1
                continue
            if R.is_rigid(adj, h, x, p, pi_inf):
                tally['pi->RIGID'] += 1
                if len(examples) < 10:
                    examples.append(dict(graph=name, h=h, c=c))
                continue
            L = (pi_inf['L1'], pi_inf['L2'])
            if L == (True, True):
                tally['pi->DL_nonrigid'] += 1
                pc = R.pair_counts(adj, h, x, p, pi_inf)
                exc = sum(a - b for a, b in zip(pc, R.RIGID))
                tally[f'pi->DL_nonrigid_excess{exc}'] += 1
            elif L == (False, False):
                tally['pi->lockless'] += 1
            else:
                tally['pi->singlelock'] += 1


def main():
    out = sys.argv[1]
    fn = sys.argv[2]
    stride = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    offset = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    maxg = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 9
    excl = set()
    if len(sys.argv) > 6:
        excl = {l.split()[0] for l in open(sys.argv[6]) if l.strip()}
    tally = Counter()
    examples = []
    k = 0
    for i, line in enumerate(open(fn)):
        if not line.strip() or line.startswith('>'):
            continue
        if i % stride != offset:
            continue
        name, adj = parse_any(line)
        if name in excl:
            tally['excluded'] += 1
            continue
        if not is_sphere_triangulation(adj):
            tally['not_sphere_tri'] += 1
            continue
        tally['graphs'] += 1
        run_graph(adj, tally, examples, name)
        k += 1
        if k >= maxg:
            break
    res = dict(file=fn, stride=stride, offset=offset, tally=dict(tally), examples=examples)
    json.dump(res, open(out, 'w'))
    print(json.dumps(res))


if __name__ == '__main__':
    main()
