#!/usr/bin/env python3
"""Track H: dump the all-DL pi-cycles of a hole and their class.
usage: th_dump.py GRAPHFILE NAME HOLE [--json out.jsonl]
For each cycle (in pi order): per state the link (absolute normalised colours), j, roles, locks, inA/inB, D1/D2,
|K_aA|,|K_aB|,|K_am| (+ odd counts), sigma-image kind, every Kempe move leaving DL (role pair, link positions hit
relative to j, target kind), distance to a non-DL state (dS) and to a filled state (dF) with the shortest path."""
import sys, json
from collections import Counter
from th_engine import read_graphs, Hole

def rolename(r, p):
    return 'amAB'[r['roles'].index(p)]

def describe_move(H, r, m):
    p, q, hit, size, k, _ = m
    pr = ''.join(sorted(rolename(r, p) + rolename(r, q), key='amAB'.index))
    rel = ''.join(str(t) for t in sorted((t - r['j']) % 5 for t in hit))
    return pr, rel, size, H.info[k]['kind'], k

def main():
    gf, name, hole = sys.argv[1], sys.argv[2], int(sys.argv[3])
    H = Hole(read_graphs(gf)[name], hole).build(); info = H.info
    deg = [len(H.rot[x]) for x in H.X]
    cycs = H.allDL_cycles()
    print(f'# {name} hole {hole} link degrees {deg} states {len(H.states)} cycles {[len(c) for c in cycs]}')
    out = []
    for ci, cyc in enumerate(cycs):
        mem = H.class_members(cyc[0]); ms = set(mem)
        kinds = Counter(info[i]['kind'] for i in mem)
        viol = sum(1 for i in mem if info[i]['kind'] != 'F' and not (info[i]['D1'] and info[i]['D2']))
        oncyc = sum(1 for c in cycs if c[0] in ms for _ in c)
        print(f'## cycle {ci} len {len(cyc)}: class N={len(mem)} F={kinds["F"]} DL={kinds["DL"]} S={kinds["S"]} N0={kinds["N"]} viol={viol} onCycles={oncyc}')
        dS = H.dist_to(cyc, lambda u: info[u]['kind'] != 'DL', ms)
        dF = H.dist_to(cyc, lambda u: info[u]['kind'] == 'F', ms)
        sig = ''
        for t, i in enumerate(cyc):
            r = info[i]; s = info[r['sigma']]
            esc = [describe_move(H, r, m) for m in H.moves[i] if info[m[4]]['kind'] != 'DL']
            sig += 's' if s['kind'] != 'DL' else '.'
            pth = ' '.join(f"{describe_move(H, info[u], m)[0]}:{describe_move(H, info[u], m)[1] or '-'}->{info[m[4]]['kind']}" for u, m in dF[i][1])
            print(f"{t:2d} st{i:5d} j={r['j']} link={''.join(map(str, r['link']))} L={int(r['L1'])}{int(r['L2'])} in={int(r['inA'])}{int(r['inB'])} "
                  f"|KaA|={r['KA']}({r['oA']}) |KaB|={r['KB']}({r['oB']}) |Kam|={r['KM']}({r['oM']}) |KmA|={r['KmA']} |KmB|={r['KmB']} "
                  f"sigma->{s['kind']}{'' if s['kind'] in 'F' else ' L=%d%d' % (s['L1'], s['L2'])} dS={dS[i][0]} dF={dF[i][0]} "
                  f"exits={sorted(Counter((e[0], e[1] or '-', e[3]) for e in esc).items())} pathF=[{pth}]")
            out.append(dict(graph=name, hole=hole, cyc=ci, t=t, state=i, j=r['j'], link=r['link'], L1=r['L1'], L2=r['L2'], inA=r['inA'], inB=r['inB'],
                            KA=r['KA'], oA=r['oA'], KB=r['KB'], oB=r['oB'], KM=r['KM'], oM=r['oM'], sigma=s['kind'],
                            exits=[list(e[:4]) for e in esc], dS=dS[i][0], dF=dF[i][0]))
        print('   sigma string:', sig)
    if '--json' in sys.argv:
        with open(sys.argv[sys.argv.index('--json') + 1], 'a') as f:
            for o in out: f.write(json.dumps(o) + '\n')

if __name__ == '__main__':
    main()
