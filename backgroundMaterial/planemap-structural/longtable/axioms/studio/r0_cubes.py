"""Studio Job 4 (13 Oct 2026, exploratory): Conjecture R0 (Long Table PROOF-ATTEMPT-1 section 5) at larger n,
by cubes.  Same encoding as proof/relax2.py with rule 'planar' (or 'none') and frame advance -2:
H = M_0 u M_1 Hamiltonian (normal form), M_0..M_{L-1} perfect matchings, M_t n M_{t+1} = 0 cyclically,
v-edge of M_t = f_{2-2t}; planarity by the circle rule of sat_planar.PEnc.  Pure SAT: no CEGAR cuts, so there is
no cut log; instead the whole CNF is written once to OUT.cnf (DIMACS) and the cube units to OUT.jsonl, so every
UNSAT cube can be re-refuted offline by a proof-producing solver (DRAT/LRAT).

Cubes: positions of the chords carrying f_1 (depth 1), f_1 and f_3 (depth 2), or all three (depth 3).
Any SAT under planarity is a counterexample to R0: it is verified as in relax2.py --verify (perfect matchings,
disjointness, frames, Hamiltonian M_0 u M_1, planar_rot) and written to OUT.sat.

    python3 r0_cubes.py n L planar(1|0) depth workers OUT    [env STOP_AFTER_SAT=k]
"""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
PROOF = os.path.join(os.path.dirname(HERE), 'proof')
sys.path.insert(0, PROOF)
import sat_t1v                         # noqa: E402  (proof/ copy, as relax2.py uses)
import sat_planar                      # noqa: E402
from pysat.solvers import Cadical153   # noqa: E402

sat_t1v.Enc._eager_loops = lambda self: None   # R0: no z-loops / parity / A5v (relax2.py)
G = {}


def build(n, L, planar):
    if planar:
        return sat_planar.PEnc(n, L, 0, closed=True)
    return sat_t1v.Enc(n, L, 0, eager=0, closed=True)


def cubes(n, depth):
    J = range(2, n - 1)
    if depth == 1: return [(j,) for j in J]
    if depth == 2: return [(a, b) for a in J for b in J if a != b]
    return [(a, b, c) for a in J for b in J for c in J if len({a, b, c}) == 3]


def asm_of(enc, cube):
    return [enc.lab[s][enc.eid[(0, j)]] for s, j in zip((1, 3, 4), cube)]


def init(n, L, planar):
    enc = build(n, L, planar)
    G.update(enc=enc, s=Cadical153(bootstrap_with=enc.cl), n=n, L=L)


def verify(enc, model, n, L):
    sys.path.insert(0, os.path.dirname(PROOF))
    from ax_lib import G5, parse_line, planar_rot
    E, M, fv = enc.decode(model)
    line = sat_t1v.to_line(enc, E, fv)
    g = G5(*parse_line(line)); idx = {e: i for i, e in enumerate(E)}
    Ms = [frozenset(idx[e] for e in M[t]) for t in range(L)]
    return dict(line=line, M=[sorted(Mt) for Mt in Ms],
                PM=all(sorted(x for e in Mt for x in g.E[e]) == list(range(n)) for Mt in Ms),
                disjoint=all(not (Ms[t] & Ms[(t + 1) % L]) for t in range(L)),
                frames=[g.kidx(Mt) for Mt in Ms], ham01=g.ncomp(Ms[0] | Ms[1]) == 1, planar_rot=bool(planar_rot(g)))


def solve_cube(cube):
    enc, s = G['enc'], G['s']
    t0 = time.time()
    r = s.solve(assumptions=asm_of(enc, cube))
    out = dict(cube=cube, status='SAT' if r else 'UNSAT', sec=round(time.time() - t0, 1))
    if r: out['check'] = verify(enc, s.get_model(), G['n'], G['L'])
    return out


if __name__ == '__main__':
    n, L, planar, depth, W, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    enc = build(n, L, planar)
    if not os.path.exists(out + '.cnf'):
        with open(out + '.cnf', 'w') as f:
            f.write('c R0 n=%d L=%d planar=%d (studio/r0_cubes.py); cube literals in %s.jsonl\n' % (n, L, planar, os.path.basename(out)))
            f.write('p cnf %d %d\n' % (enc.pool.top, len(enc.cl)))
            for c in enc.cl: f.write(' '.join(map(str, c)) + ' 0\n')
    done = set()
    if os.path.exists(out + '.jsonl'):
        done = {tuple(json.loads(l)['cube']) for l in open(out + '.jsonl')}
    C = [c for c in cubes(n, depth) if c not in done]
    print(f'R0 n={n} L={L} planar={planar} depth={depth} vars={enc.pool.top} clauses={len(enc.cl)} cubes={len(C)} (done {len(done)}) workers={W}', flush=True)
    stop = int(os.environ.get('STOP_AFTER_SAT', '1000000'))
    t0 = time.time(); tally = {}
    with Pool(W, initializer=init, initargs=(n, L, planar)) as p, open(out + '.jsonl', 'a') as f:
        for r in p.imap_unordered(solve_cube, C):
            r['asm'] = asm_of(enc, r['cube'])
            f.write(json.dumps(r) + '\n'); f.flush()
            tally[r['status']] = tally.get(r['status'], 0) + 1
            if r['status'] == 'SAT':
                open(out + '.sat', 'a').write(json.dumps(r) + '\n')
                print('SAT', json.dumps(r), flush=True)
                if tally['SAT'] >= stop:
                    p.terminate(); print('stopped after', tally['SAT'], 'SAT cubes', flush=True); break
    print(json.dumps(dict(n=n, L=L, planar=planar, depth=depth, tally=tally, wall=round(time.time() - t0, 1))), flush=True)
