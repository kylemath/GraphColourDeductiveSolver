#!/usr/bin/env python3
"""Track M driver: run every rule from every unfilled state (or a sample) at the chosen degree-5 holes.

usage: tm_run.py OUT.jsonl --src rot:FILE | faces-json:FILE | heawood:FILE | jobbv:DIR
                 [--names a,b] [--stride k --offset o] [--holes-per-graph m] [--max-states S] [--max-starts M]
                 [--holes-from kclass3.jsonl] [--surface label]
One JSON line per hole: per rule, per category (U = all unfilled, DL, CYC = on an all-DL pi-cycle, TL = in a class with
no filled state), a histogram of steps-to-filled (index 0..10; index 11 = fail within 10). Plus failure records.
"""
import sys, os, json, time, random, argparse
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tm_lib import Hole, RULES, run_rule, RULES2, run_rule2, read_rot_lines, rot_from_faces, KMAX

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--src', required=True)
ap.add_argument('--names'); ap.add_argument('--stride', type=int, default=1); ap.add_argument('--offset', type=int, default=0)
ap.add_argument('--holes-per-graph', type=int, default=0); ap.add_argument('--max-states', type=int, default=400000)
ap.add_argument('--max-starts', type=int, default=0); ap.add_argument('--holes-from'); ap.add_argument('--surface', default='sphere')
ap.add_argument('--only-cycle-holes', action='store_true'); ap.add_argument('--max-graphs', type=int, default=0)
ap.add_argument('--fail-records', type=int, default=6); ap.add_argument('--pass2', action='store_true'); ap.add_argument('--both', action='store_true')
a = ap.parse_args()

kind, path = a.src.split(':', 1)
names = set(a.names.split(',')) if a.names else None
graphs = []
if kind == 'rot':
    graphs = read_rot_lines(path, names)
elif kind == 'faces-json':
    for p in path.split(','):
        d = json.load(open(p)); graphs.append((os.path.basename(p).replace('.json', ''), rot_from_faces(d.get('faces_ccw') or d['faces'])))
elif kind == 'heawood':
    d = json.load(open(path)); graphs.append(('Heawood1890', d['rotation']))
elif kind == 'jobbv':
    for f in sorted(os.listdir(path)):
        d = json.load(open(os.path.join(path, f))); F = d['faces'] if isinstance(d['faces'], list) else json.loads(d['faces'])
        graphs.append((f.replace('.json', ''), rot_from_faces(F)))
graphs = graphs[a.offset::a.stride]
if a.max_graphs: graphs = graphs[:a.max_graphs]
holes_from = None
if a.holes_from:
    holes_from = {}
    for l in open(a.holes_from):
        r = json.loads(l); g = r.get('name') or r.get('graph'); h = r.get('hole', r.get('h'))
        if a.only_cycle_holes and not r.get('allDLcyc'): continue
        holes_from.setdefault(g, set()).add(int(h))

rules = list(RULES2) if a.pass2 else list(RULES)
if a.pass2: RULES, run_rule = RULES2, run_rule2
if a.both:
    _R1, _r1 = RULES, run_rule
    RULES = dict(_R1); RULES.update(RULES2); rules = list(RULES)
    run_rule = lambda H, n, s: (run_rule2(H, n, s) if n in RULES2 else _r1(H, n, s))
fo = open(a.out, 'a')
for gname, rot in graphs:
    hs = [v for v in range(len(rot)) if len(rot[v]) == 5]
    if holes_from is not None: hs = [v for v in hs if v in holes_from.get(gname, ())]
    if a.holes_per_graph and len(hs) > a.holes_per_graph:
        random.Random(gname).shuffle(hs); hs = sorted(hs[:a.holes_per_graph])
    for h in hs:
        t0 = time.time()
        try:
            H = Hole(rot, h)
        except AssertionError as e:
            print('skip', gname, h, e, file=sys.stderr); continue
        if H.S > a.max_states:
            print('skip big', gname, h, H.S, file=sys.stderr); continue
        cl, dF = H.classes_and_dist()
        oncyc = H.allDL_cycle_state_set = H.allDL_cycle_states()
        # interior DL region: DL states with no non-DL neighbour (dNDL >= 2); component sizes
        inter = {x for x in range(H.S) if H.dNDL[x] >= 2}; seen = set(); interior = []
        for x in inter:
            if x in seen: continue
            comp = [x]; seen.add(x)
            for y in comp:
                for m in H.moves[y]:
                    if m[0] in inter and m[0] not in seen: seen.add(m[0]); comp.append(m[0])
            interior.append(len(comp))
        interior = sorted(interior, reverse=True)[:5]
        # longest run of consecutive interior-DL states along pi (resp. pi^-1); -1 if an interior pi-cycle exists
        def maxrun(f):
            best = 0
            for x in inter:
                k = 0; y = x; seen2 = set()
                while y is not None and y in inter:
                    if y in seen2: return -1
                    seen2.add(y); k += 1; y = f[y]
                best = max(best, k)
            return best
        pirun = [maxrun(H.pi), maxrun(H.pinv)]
        clfilled = Counter(cl[s] for s in range(H.S) if H.filled[s])
        starts = [s for s in range(H.S) if not H.filled[s]]
        if a.max_starts and len(starts) > a.max_starts:
            keep = set(oncyc) | {s for s in starts if H.phi[s] == 2}
            rest = [s for s in starts if s not in keep]
            random.Random(gname + str(h)).shuffle(rest)
            starts = sorted(keep | set(rest[:max(0, a.max_starts - len(keep))]))
        hist = {r: {c: [0] * (KMAX + 2) for c in ('U', 'DL', 'CYC', 'TL')} for r in rules}
        fails = {r: [] for r in rules}
        k2 = Counter(); budget_ex = Counter()
        for s in starts:
            cats = ['U']
            if H.phi[s] == 2: cats.append('DL')
            if s in oncyc: cats.append('CYC')
            tl = clfilled[cl[s]] == 0
            if tl: cats.append('TL')
            if H.kempe2[s] is not None:
                k2[('ok' if any(x[0] for x in H.kempe2[s]) else 'fail') + ('_interf' if all(x[1] for x in H.kempe2[s]) else '')] += 1
            for r in rules:
                st, p = run_rule(H, r, s)
                if st == -1: budget_ex[r] += 1; st = None
                idx = st if st is not None else KMAX + 1
                for c in cats: hist[r][c][idx] += 1
                if st is None and not tl and len(fails[r]) < a.fail_records and RULES[r][0] != 'opt':
                    fails[r].append(dict(s=s, phi=H.phi[s], dF=dF[s], dNDL=H.dNDL[s], cyc=s in oncyc,
                                         k2=[x[:2] for x in H.kempe2[s]] if H.kempe2[s] else None,
                                         path_phi=[H.phi[x] for x in p], path_len=len(p) - 1,
                                         kdeg=len(H.moves[s])))
        rec = dict(graph=gname, h=h, surface=a.surface, n=len(rot), word=''.join(str(len(rot[x])) for x in rot[h]),
                   S=H.S, F=sum(H.filled), U=H.S - sum(H.filled), nstarts=len(starts), ncl=H.ncl,
                   tlclasses=H.ncl - len(clfilled), ncyc=len(oncyc), maxdF=max((dF[s] for s in starts if dF[s] >= 0), default=0),
                   maxdNDL=max((H.dNDL[s] for s in starts if H.dNDL[s] >= 0), default=0),
                   kempe2=dict(k2), budget_ex=dict(budget_ex), interior=interior, pirun=pirun, hist=hist, fails={r: v for r, v in fails.items() if v}, sec=round(time.time() - t0, 2))
        fo.write(json.dumps(rec) + '\n'); fo.flush()
        print(gname, h, H.S, len(starts), rec['sec'], file=sys.stderr)
