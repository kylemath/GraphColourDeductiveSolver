#!/usr/bin/env python3
"""RSST-1SHOT second engine: d = 9..14 exact search, built from spec v2 (a7915274) §13 Addendum A alone.
All letters free in 5..9+, no domains, u never a hub and read as 9+, u IS a host with letter d (§13 A.1).
1. c+ table: for each 5-letter link window (L_{i-2..i+2}), the max number of possible fits w_i -> u over every
   apex/private value (exact branch-and-bound over the conjunction instances).
2. Link words up to rotation+reflection, DFS in site order with the word's first letter minimal; partial bound
   base + sum_i b_i (b_i = c+ if window assigned, cmax(L_i) if only L_i, else 6); full word: dihedral minimum
   and the cyclic c+ bound must be > 0.
3. Per word: fullworld.dfs over apexes/privates (dominance domains, bound = base + in-fits not violated,
   monotone kills by requirement sets with u as a host); modes 633 (pass test, threshold 0) and 582 (enum:
   every leaf is positive and not killed by a proved config; classified by the none configs it contains).
usage: d9.py D MODEL [shard nshard]     MODEL in {633, 582, nokill}"""
import sys, os, json, itertools, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcore as R
R.U_HOST_ALWAYS = True
import fullworld as FW

JOB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CMAX = {5: 6, 6: 6, 7: 6, 8: 4, 9: 0}

def maxsat(insts):
    """max over assignments of #instances whose conjunction holds (instances: dicts with conds)."""
    names = sorted(set(nm for I in insts for nm in I['conds']))
    pos = {nm: k for k, nm in enumerate(names)}
    by = [[] for _ in names]
    for t, I in enumerate(insts):
        for nm, iv in I['conds'].items(): by[pos[nm]].append((t, iv))
    dead = [False] * len(insts); best = [0]
    def rec(k, ub):
        if ub <= best[0]: return
        if k == len(names): best[0] = ub; return
        for v in (5, 6, 7, 8, 9):
            ch = []; nub = ub
            for t, (a, b) in by[k]:
                if not dead[t] and not (a <= v <= b): dead[t] = True; ch.append(t); nub -= 1
            rec(k + 1, nub)
            for t in ch: dead[t] = False
    rec(0, len(insts)); return best[0]

def cplus_table():
    fn = os.path.join(JOB, 'results', 'cplus_d9.json')
    if os.path.exists(fn): return {tuple(int(c) for c in k): v for k, v in json.load(open(fn)).items()}
    T = {}
    for win in itertools.product((5, 6, 7, 8, 9), repeat=5):
        if win[2] == 9: T[win] = 0; continue
        link = list(win) + [5] * 5           # d = 10 window, hub at site 2
        W = R.Window(10, link, None)
        ins = [I for I in R.instances(W) if I['hub'] == 'w2']
        T[win] = maxsat(ins)
    json.dump({''.join(map(str, k)): v for k, v in T.items()}, open(fn, 'w'))
    return T

def words(d, CP):
    base = 10 * (6 - d); L = [0] * d
    def bound(k):
        s = base
        for i in range(d):
            if i - 2 >= 0 and i + 2 <= k - 1: s += CP[tuple(L[i - 2:i + 3])]
            elif i <= k - 1: s += CMAX[L[i]]
            else: s += 6
        return s
    def rec(k):
        if k == d:
            w = tuple(L)
            if min(min(w[r:] + w[:r], (w[r:] + w[:r])[::-1]) for r in range(d)) != w: return
            if base + sum(CP[tuple(w[(i + t) % d] for t in (-2, -1, 0, 1, 2))] for i in range(d)) <= 0: return
            yield list(w); return
        for v in (5, 6, 7, 8, 9):
            if k > 0 and v < L[0]: continue
            L[k] = v
            if bound(k + 1) > 0: yield from rec(k + 1)
        L[k] = 0
    yield from rec(0)

def main():
    d = int(sys.argv[1]); model = sys.argv[2]
    shard, nsh = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 1)
    CP = cplus_table()
    tag = ('_' + R.CONTROL) if R.CONTROL else ''
    fo = open(os.path.join(JOB, 'logs', 'd9_d%d_%s_%dof%d%s.jsonl' % (d, model, shard, nsh, tag)), 'w')
    st = collections.Counter(); t0 = time.time(); best = None
    for wi, link in enumerate(words(d, CP)):
        if wi % nsh != shard: continue
        st['words'] += 1
        Lk = FW.Link(d, link)
        if model == 'nokill':
            mx, leaves, nodes = FW.dfs(Lk, 'nokill', best=0); st['nodes'] += nodes
            if mx is not None and (best is None or mx > best[0]):
                top = max(leaves); best = (top[0], ''.join(map(str, link)), FW.ftext(Lk, FW.leaf_fill(Lk, top[1])))
            continue
        mx, leaves, nodes = FW.dfs(Lk, model); st['nodes'] += nodes
        if mx is None and nodes == 0: st['link_killed'] += 1
        for hi, vals in leaves:
            f = FW.leaf_fill(Lk, vals); full = {nm: f.get(nm, 9) for nm in Lk.allvars}
            c = R.contained(Lk.reqs(), full)
            rec = {'link': ''.join(map(str, link)), 'hi': hi, 'filling': FW.ftext(Lk, f)}
            if c:
                assert model == '582' and not any(R.CONFIGS[i]['proved'] for i in c)
                rec['needs_none'] = sorted(R.CONFIGS[i]['name'] for i in c); st['states_need_none'] += 1
            else:
                rec['survivor'] = True; st['survivors'] += 1
            if best is None or hi > best[0]: best = (hi, rec['link'], rec['filling'])
            fo.write(json.dumps(rec) + '\n')
        fo.flush()
    summ = {'d': d, 'model': model, 'shard': shard, 'nshard': nsh, 'stats': dict(st), 'max_found': best,
            'secs': round(time.time() - t0, 1), 'control': R.CONTROL}
    fo.write(json.dumps({'summary': summ}) + '\n'); fo.close(); print(json.dumps(summ), flush=True)

if __name__ == '__main__':
    main()
