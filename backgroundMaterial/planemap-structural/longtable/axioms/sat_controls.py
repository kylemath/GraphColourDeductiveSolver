"""Controls for sat_t1v.py on fixed graphs (Long Table run 2).
1. n22 T1 graph: word 1212, AXV=0 -> must be SAT (power); AXV=1 -> must be UNSAT; AXV=2 -> SAT.
2. C30#0 planar graphs (TrackU seed_c30.txt): word relaxed, law imposed, AXV=1 -> must be SAT, L=20.
Every SAT orbit is re-verified with the independent engine ax_lib.G5."""
import sys, json
from ax_lib import G5, parse_line, law_ok
from sat_t1v import Enc, run

TU = '/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/TrackU/out/'


def verify(line_g, sol, enc):
    """independent check: the SAT orbit is a closed orbit of ax_lib's engine, with the same word."""
    n, E, fv = line_g
    g = G5(n, E, fv)
    P, good, cyc = g.orbits()
    Es, M, fvv, info = sol
    Mset = [frozenset(M[t]) for t in range(enc.L)]
    for c in cyc:
        if set(c) == set(Mset):
            w = ''.join(map(str, g.word(c)))
            # A5v at every state via ax_lib loops
            ax = []
            for M_ in c:
                k, d = g.dl(M_)
                a = g.other(g.fv[k], g.v)
                ax.append(a in d['X'][2])
            return dict(found_in_axlib=True, axlib_word=w, law_viol=law_ok(g.word(c)), A5v_all=all(ax),
                        A5v_none=not any(ax))
    return dict(found_in_axlib=False, n_axlib_cycles=len(cyc))


def one(label, line, L, axv, word, law):
    n, E, fv = parse_line(line)
    enc = Enc(n, L, axv, mode='fixed', fixed=(n, E, fv), word=word, law=law)
    st, sols, stats = run(enc, 300, verbose=False, max_sol=50)
    res = dict(control=label, L=L, axv=axv, word=word, law=law, status=st, n_orbits=len(sols), **stats)
    if sols:
        res['words'] = sorted(set(s[3]['word'] for s in sols))
        res['verify'] = [verify((n, E, fv), s, enc) for s in sols]
    print(json.dumps(res), flush=True)


if __name__ == '__main__':
    n22 = open(TU + 't1_n22_first.txt').readline()
    for axv in (0, 1, 2):
        one('n22_T1', n22, 10, axv, '1212', False)
    for i, line in enumerate(open(TU + 'seed_c30.txt')):
        if line.strip():
            one(f'C30#0_line{i}', line, 20, 1, None, True)
            one(f'C30#0_line{i}', line, 20, 2, None, True)
