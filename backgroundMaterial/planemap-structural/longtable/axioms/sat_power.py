"""Power control for the free ('ham') encoding of sat_t1v.py (Long Table run 2).
Relabel the n = 22 T1 counterexample along a Hamiltonian state of its orbit (the ham normal form),
then fix a random fraction p of its chords as present (all other chords, the f-labels and all
matchings M_2..M_9 free) and solve with axv = 0 / 2 (must find an orbit) and axv = 1.
Usage: sat_power.py p seed axv [tlimit]"""
import sys, json, random
from ax_lib import G5, parse_line
from sat_t1v import Enc, run, to_line

TU = '/Users/fulkanjou/GraphColour/SolvingFrameworkPlan/docs/working/TrackU/out/'


def ham_normal_form(n, E, fv):
    g = G5(n, E, fv)
    P, good, cyc = g.orbits()
    c = cyc[0]; L = len(c)
    w = g.word(c)
    for t0 in range(L):
        M0, M1 = c[t0], c[(t0 + 1) % L]
        if g.ncomp(M0 | M1) == 1: break
    k0 = g.kidx(M0)
    sh = (k0 - 2) % 5           # new label s' = s - sh, so M0's edge gets label 2
    nfv = [fv[(s + sh) % 5] for s in range(5)]
    # walk H = M0 u M1 from v leaving by M0's v-edge
    v = g.v; order = [v]; x = g.other(fv[k0], v); last = fv[k0]
    while x != v:
        order.append(x)
        nxt = [e for e in g.inc[x] if e in (M0 | M1) and e != last][0]
        last = nxt; x = g.other(nxt, x)
    new = {u: i for i, u in enumerate(order)}
    chords = set()
    for i, (a, b) in enumerate(E):
        if i in M0 or i in M1: continue
        chords.add(tuple(sorted((new[a], new[b]))))
    lab = {s: tuple(sorted((new[E[nfv[s]][0]], new[E[nfv[s]][1]]))) for s in range(5)}
    return chords, lab


if __name__ == '__main__':
    p, seed, axv = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600
    n, E, fv = parse_line(open(TU + 't1_n22_first.txt').readline())
    chords, lab = ham_normal_form(n, E, fv)
    enc = Enc(n, 10, axv, eager=1)
    rnd = random.Random(seed)
    # fix a fraction p of the T1 chords as present; everything else (other chords, labels, M_2..M_9) free
    cand = [e for e in range(enc.m) if enc.X[e] is not None and tuple(sorted(enc.edges[e])) in chords]
    fixed = rnd.sample(cand, int(round(p * len(cand))))
    for e in fixed:
        enc.add([enc.X[e]])
    st, sols, stats = run(enc, tl, verbose=False)
    out = dict(p=p, seed=seed, axv=axv, nfixed=len(fixed), of=len(cand), status=st, **stats)
    if sols:
        Es, M, fvv, info = sols[0]
        line = to_line(enc, Es, fvv)
        got = set(tuple(sorted(enc.edges[e])) for e in Es if enc.X[e] is not None)
        out['same_chords_as_T1'] = got == chords
        out['word'] = info['word']
        g = G5(*parse_line(line)); P_, good, cyc = g.orbits()
        out['axlib_orbits'] = [''.join(map(str, g.word(c))) for c in cyc]
        out['line'] = line
    print(json.dumps(out), flush=True)
