#!/usr/bin/env python3
"""Track U: shrink T1 violators. Reduction: delete an edge xy between two cubic vertices (x: other nbrs a,b; y: c,d)
and reconnect a-c, b-d or a-d, b-c (n -> n-2, cubic kept, v's labels kept). Keep any reduced graph that still has
a T1-violating closed orbit (tu_eng2 eval). BFS by levels, capped width.
usage: tu_shrink.py GRAPHLINES OUT.txt [width]"""
import sys, os, json, subprocess, random
HERE = os.path.dirname(os.path.abspath(__file__))

def parse(l):
    p = list(map(int, l.split())); n, m = p[0], p[1]
    return n, [(p[2+2*i], p[3+2*i]) for i in range(m)], p[2+2*m:7+2*m]

def line(n, E, fv): return ' '.join(map(str, [n, len(E)] + [x for e in E for x in e] + list(fv)))

def reductions(n, E, fv):
    for k, (x, y) in enumerate(E):
        if x == 0 or y == 0: continue
        ex = [j for j, e in enumerate(E) if x in e and j != k]; ey = [j for j, e in enumerate(E) if y in e and j != k]
        if len(ex) != 2 or len(ey) != 2: continue
        oth = lambda j, z: E[j][1] if E[j][0] == z else E[j][0]
        a, b = oth(ex[0], x), oth(ex[1], x); c, d = oth(ey[0], y), oth(ey[1], y)
        for (p1, q1), (p2, q2), (j1, j2) in (((a, c), (b, d), (ex[0], ex[1])), ((a, d), (b, c), (ex[0], ex[1]))):
            if p1 == q1 or p2 == q2: continue
            NE = list(E); NE[j1] = (p1, q1); NE[j2] = (p2, q2)
            # j1 keeps its id (it may be a v-edge if a == 0 etc.): fix fv: v-edges among ex/ey
            drop = {k, ey[0], ey[1]}
            fv2 = list(fv); ok = True
            # if a v-edge is in ey, it was replaced: map ey[0]->? ; simple: reject if any fv in ey
            if any(f in drop for f in fv): continue
            keep = [j for j in range(len(NE)) if j not in drop]
            ren = {j: i for i, j in enumerate(keep)}
            NE2 = [NE[j] for j in keep]
            verts = sorted({z for e in NE2 for z in e}); vr = {z: i for i, z in enumerate(verts)}
            if verts[0] != 0 or len(verts) != n - 2: continue
            NE3 = [(vr[p], vr[q]) for p, q in NE2]
            G = {}
            if len({tuple(sorted(e)) for e in NE3}) != len(NE3): continue   # simple only
            yield n - 2, NE3, [ren[f] for f in fv]

def t1_of(lines):
    open('/tmp/_tu_shrink_in.txt', 'w').write('\n'.join(lines) + '\n')
    out = subprocess.run([os.path.join(HERE, 'tu_eng2'), 'eval', '/tmp/_tu_shrink_in.txt'], capture_output=True, text=True).stdout
    res = []
    for l in out.splitlines():
        d = json.loads(l)
        if d['event'] == 'summary': res.append(d['t1'])
    return res

def main():
    cur = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    best = []
    rnd = random.Random(1)
    while cur:
        cand = []
        for l in cur:
            for g in reductions(*parse(l)): cand.append(line(*g))
        cand = list(dict.fromkeys(cand))
        if not cand: break
        res = t1_of(cand)
        good = [c for c, r in zip(cand, res) if r > 0]
        print('n=%d candidates %d T1-violators %d' % (parse(cand[0])[0], len(cand), len(good)), flush=True)
        if not good: break
        best = good; rnd.shuffle(good); cur = good[:width]
    open(sys.argv[2], 'w').write('\n'.join(best) + '\n')

if __name__ == '__main__':
    main()
