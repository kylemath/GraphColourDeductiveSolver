#!/usr/bin/env python3
"""Track J task 3 [data]: how far are sphere classes from being near-rigid closed?

Per hole (all degree-5 holes of each graph):
 (A) every Kempe class containing an all-DL pi-cycle: size, the N-profile of each cycle, 'good' states (on an all-DL
     cycle with N <= 9), cycle states with N >= 10, class states off the cycles, and the Kempe moves (distinct targets)
     from good states that leave the good set, split by target type (F / non-DL unfilled / DL off-cycle / on-cycle N>=10).
 (B) R = all DL states with N <= 9 (cycle or not).  Components of the Kempe graph restricted to R: size, #rigid, #nine,
     exits (distinct targets outside R).  A near-rigid closed class would be an R-component with 0 exits.
     Also: the longest pi-run inside R (consecutive pi-steps between R states) and whether any pi-cycle lies inside R;
     'in-shape' pairs: N = 9 states c with pi(c), pi^-1(c) rigid whose link-free swap partner is again in-shape.
usage: tj_nrcomp.py GRAPHFILE STRIDE OFFSET MAXGRAPHS [prefix] > log      (prints per-hole lines for (A) and a SUMMARY)
"""
import sys, json
from collections import Counter
from tj_lib import Engine, read_graphs, nholes, RIGID


def main():
    gf, stride, off, maxg = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    pref = sys.argv[5] if len(sys.argv) > 5 else ''
    E = Engine(dump=True, allholes=True)
    T = Counter(); k = 0; best = []
    for gi, (name, line, rot) in enumerate(read_graphs(gf, pref)):
        if gi % stride != off: continue
        k += 1
        if k > maxg: break
        for js, S in E.run(line, nholes(rot)):
            if S is None: T['err'] += 1; continue
            T['holes'] += 1; h = js['hole']
            inv = {}
            for s in S:
                if s['kind'] and not s['inB']:
                    for (x, pr, lm) in s['mv']:
                        if pr == 4 and (lm >> s['j']) & 1: inv[s['i']] = x
            tg = [sorted({x for (x, _, _) in s['mv'] if x != s['i']}) for s in S]
            # (A)
            if js['ncyc']:
                good = {s['i'] for s in S if s['oncyc'] and s['N'] <= 9}
                for c in js['cls']:
                    root = c[-1]; mem = [s['i'] for s in S if s['cls'] == root]
                    # cycles of this class in pi order
                    seen = set(); prof = []
                    for i in mem:
                        if S[i]['oncyc'] and i not in seen:
                            cyc = []; x = i
                            while x not in seen: seen.add(x); cyc.append(x); x = S[x]['pi']
                            prof.append(''.join(str(S[y]['N']) if S[y]['N'] < 10 else ('abcdefghij'[S[y]['N'] - 10]) for y in cyc))
                    g = [i for i in mem if i in good]
                    leave = Counter()
                    for i in g:
                        for x in tg[i]:
                            if x in good: continue
                            t = S[x]; leave['F' if t['kind'] == 0 else ('nonDL' if t['kind'] != 1 else ('DLoff' if not t['oncyc'] else 'cycN>=10'))] += 1
                    rec = dict(graph=name, hole=h, size=len(mem), filled=c[1], cyc_profiles=prof, good=len(g),
                               cyc_states=sum(S[i]['oncyc'] for i in mem), cyc_N10p=sum(1 for i in mem if S[i]['oncyc'] and S[i]['N'] >= 10),
                               off_cycle_states=sum(1 for i in mem if not S[i]['oncyc']), moves_leaving_good=dict(leave), nleave=sum(leave.values()))
                    print('A', json.dumps(rec), flush=True)
                    T['A_classes'] += 1; T['A_cycles'] += len(prof); T['A_good'] += len(g)
            # (B)
            R = {s['i'] for s in S if s['kind'] == 1 and s['N'] <= 9}
            T['R_states'] += len(R)
            comp = {}
            for i in R:
                if i in comp: continue
                st = [i]; comp[i] = i; mem = []
                while st:
                    u = st.pop(); mem.append(u)
                    for x in tg[u]:
                        if x in R and x not in comp: comp[x] = i; st.append(x)
                ex = {x for u in mem for x in tg[u] if x not in R}
                nr = sum(1 for u in mem if S[u]['N'] == 8); nn = len(mem) - nr
                T['R_comps'] += 1; T['R_comp_exits0'] += (len(ex) == 0)
                T['R_comp_size_%s' % (len(mem) if len(mem) < 6 else '6+')] += 1
                key = (len(mem), -len(ex))
                best.append((len(mem), len(ex), nr, nn, name, h))
            # pi-runs inside R
            runmax = 0
            for i in R:
                if inv.get(i) in R: continue      # start of a run only
                L = 1; x = S[i]['pi']
                while x in R and x != i and L < 1000: L += 1; x = S[x]['pi']
                runmax = max(runmax, L)
            cycR = any(all(y in R for y in cyc) for cyc in [] )
            T['R_pi_run_max_%d' % runmax] += 1
            # in-shape 9-states and their partners
            shape = set()
            for i in R:
                s = S[i]
                if s['N'] == 9 and s['pi'] >= 0 and S[s['pi']]['kind'] == 1 and S[s['pi']]['c6'] == RIGID and i in inv and S[inv[i]]['kind'] == 1 and S[inv[i]]['c6'] == RIGID:
                    shape.add(i)
            T['inshape9'] += len(shape)
            for i in shape:
                lf = [x for (x, pr, lm) in S[i]['mv'] if lm == 0 and x != i and pr in (0, 1)]
                T['inshape9_partner_inshape'] += any(x in shape for x in lf)
        if k % 50 == 0: print('progress', k, flush=True)
    best.sort(key=lambda b: (-b[0], b[1]))
    print('LARGEST_R_COMPONENTS', json.dumps(best[:15]), flush=True)
    best.sort(key=lambda b: (b[1] / b[0], -b[0]))
    print('LOWEST_EXIT_RATIO', json.dumps([b for b in best if b[0] >= 3][:15]), flush=True)
    print('SUMMARY', gf, pref, 'stride', stride, 'graphs', min(k, maxg), dict(sorted(T.items())), flush=True)
    E.close()


if __name__ == '__main__':
    main()
