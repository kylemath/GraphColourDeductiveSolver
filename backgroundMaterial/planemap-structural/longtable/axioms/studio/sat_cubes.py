"""Studio Job 3 (13 Oct 2026, exploratory): cube-and-conquer version of Long Table's exact T1-v search
(sat_t1v.py / sat_window.py, README Run 2).  Same encoding (Enc, eager=1) and the same lazy CEGAR cuts.

Cubes: the positions of v's chords.  In the ham normal form v = 0, f_2 = (0,1), f_0 = (0,n-1); the labels
f_1, f_3, f_4 sit on chords (0, j), j in 2..n-2.  depth 1 pins f_1's chord (n-3 cubes); depth 2 pins f_1 and
f_3 ((n-3)(n-4) cubes); depth 3 pins all three.  The cubes partition the search space exactly (each label
sits on exactly one v-edge), so all cubes UNSAT <=> the uncubed instance UNSAT.

Each worker process keeps ONE solver for all its cubes and solves each cube under assumptions.  Every lazy cut
is valid for the whole instance, so cuts learnt in one cube are kept for the next.  Proof material: CaDiCaL in
python-sat returns no DRAT trace, so every cut is appended to OUT.cuts-<pid> (DIMACS clauses); the eager CNF is
reproducible from sat_t1v.Enc, so  eager CNF + all cuts + cube units  is a plain CNF that a proof-producing solver
can refute offline (and that a Lean checker could consume later).

Env: NOCUTLOG=1 skips the cut log (SAT-direction controls); STOP_AFTER_SAT=k stops after k SAT cubes.
Any SAT is checked independently with ax_lib.G5 (orbit, word, A5v at every state) and written to OUT.sat.

    python3 sat_cubes.py closed|window n L_or_W axv depth workers cube_tlimit OUT
"""
import sys, os, json, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from sat_t1v import Enc, to_line          # noqa: E402
from pysat.solvers import Cadical153      # noqa: E402

G = {}


def build(kind, n, L, axv):
    if kind == 'closed':
        return Enc(n, L, axv, eager=1)
    return Enc(n, L, axv, word='1212', eager=1, closed=False)


def init(kind, n, L, axv, out):
    enc = build(kind, n, L, axv)
    G.update(enc=enc, s=Cadical153(bootstrap_with=enc.cl), cutf=(open(os.devnull, 'w') if os.environ.get('NOCUTLOG') else open('%s.cuts-%d' % (out, os.getpid()), 'a')), kind=kind)


def vedge(enc, j): return enc.eid[(0, j)]


def cubes(n, depth):
    J = range(2, n - 1)
    if depth == 1: return [(j,) for j in J]
    if depth == 2: return [(a, b) for a in J for b in J if a != b]
    return [(a, b, c) for a in J for b in J for c in J if len({a, b, c}) == 3]


def verify(enc, E, M, fv, axv):
    """independent check with ax_lib: the solved M_t form an orbit of the TrackU dynamics on the graph,
    word alternates 1,2 (closed) and A5v holds at every state."""
    from ax_lib import G5, parse_line
    line = to_line(enc, E, fv)
    g = G5(*parse_line(line))
    idx = {e: i for i, e in enumerate(E)}
    Ms = [frozenset(idx[e] for e in M[t]) for t in range(enc.L)]
    res = {'line': line}
    ok = True; ax = []
    for t, Mt in enumerate(Ms):
        d = g.dl(Mt)
        if d is None: ok = False; ax.append(None); continue
        k, info = d
        a = g.other(g.fv[k], g.v)
        ax.append(a in info['X'][2])
    res['allDL'] = ok; res['A5v_by_state'] = ax
    if enc.closed:
        P, good, cyc = g.orbits()
        sm = set(Ms)
        res['axlib_orbit'] = [''.join(map(str, g.word(c))) for c in cyc if set(c) == sm]
    return res


def solve_cube(cube):
    enc, s = G['enc'], G['s']
    asm = [enc.lab[s_][vedge(enc, j)] for s_, j in zip((1, 3, 4), cube)]
    t0 = time.time(); it = 0; nc = 0
    tl = G['tl']
    while True:
        left = tl - (time.time() - t0)
        if left <= 0:
            return dict(cube=cube, status='TIMEOUT', iters=it, cuts=nc, sec=round(time.time() - t0, 1))
        # CaDiCaL in python-sat cannot be interrupted: the time limit is checked between CEGAR rounds
        r = s.solve(assumptions=asm)
        if r is False:
            return dict(cube=cube, status='UNSAT', iters=it, cuts=nc, sec=round(time.time() - t0, 1))
        it += 1
        E, M, fv = enc.decode(s.get_model())
        cuts, info = enc.check(E, M, fv)
        if cuts:
            for c in cuts:
                s.add_clause(c); G['cutf'].write(' '.join(map(str, c)) + ' 0\n')
            G['cutf'].flush(); nc += len(cuts)
            continue
        out = dict(cube=cube, status='SAT', iters=it, cuts=nc, sec=round(time.time() - t0, 1), word=info['word'])
        out['check'] = verify(enc, E, M, fv, G['axv'])
        return out


def init2(kind, n, L, axv, out, tl):
    init(kind, n, L, axv, out); G['tl'] = tl; G['axv'] = axv


if __name__ == '__main__':
    kind, n, L, axv, depth, W, tl, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), float(sys.argv[7]), sys.argv[8]
    done = set()
    if os.path.exists(out + '.jsonl'):
        for l in open(out + '.jsonl'):
            r = json.loads(l)
            if r['status'] in ('UNSAT', 'SAT'): done.add(tuple(r['cube']))
    C = [c for c in cubes(n, depth) if c not in done]
    print(f'{kind} n={n} L/W={L} axv={axv} depth={depth} cubes={len(C)} (done {len(done)}) workers={W} tl={tl}', flush=True)
    t0 = time.time(); tally = {}
    with Pool(W, initializer=init2, initargs=(kind, n, L, axv, out, tl)) as p, open(out + '.jsonl', 'a') as f:
        for r in p.imap_unordered(solve_cube, C):
            f.write(json.dumps(r) + '\n'); f.flush()
            tally[r['status']] = tally.get(r['status'], 0) + 1
            if r['status'] == 'SAT':
                open(out + '.sat', 'a').write(json.dumps(r) + '\n')
                print('SAT', json.dumps(r), flush=True)
                if tally['SAT'] >= int(os.environ.get('STOP_AFTER_SAT', '1000000')):
                    p.terminate(); print('stopped after', tally['SAT'], 'SAT cubes', flush=True); break
    print(json.dumps(dict(kind=kind, n=n, L=L, axv=axv, depth=depth, tally=tally, wall=round(time.time() - t0, 1))), flush=True)
