#!/usr/bin/env python3
"""Track J helpers: drive the C engine tj_eng (persistent pipe) and parse its JSON / --dump output.

State record (from --dump): idx, cls, kind (0 F, 1 DL, 2 single lock, 3 lockless), j, L1, L2, inA, inB, pi (-1 = undef),
N, c6 (component counts in role order am, AB, aA, mB, aB, mA), oncyc, E (H3 counts), moves [(target, rolepair, linkmask)].
"""
import subprocess, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.join(HERE, 'tj_eng')
ROLE = ['am', 'AB', 'aA', 'mB', 'aB', 'mA']
RIGID = (1, 1, 2, 1, 2, 1)
CLSF = ['size', 'filled', 'DL', 'onCyc', 'n8', 'n9', 'n10p', 'lawFail', 'r7Fail', 'h3Fail', 'minK', 'maxK', 'nonDLunf', 'exc', 'h3imb', 'root']


class Engine:
    def __init__(self, dump=False, allholes=False, hole=0, maxstates=400000):
        args = [ENG, '--maxstates', str(maxstates)]
        if dump: args.append('--dump')
        if allholes: args.append('--allholes')
        else: args += ['--hole', str(hole)]
        self.dump = dump
        self.p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

    def run(self, line, nholes=1):
        """send one graph line; return list of (json, states-or-None) for nholes results."""
        self.p.stdin.write(line.strip() + '\n'); self.p.stdin.flush()
        out = []
        for _ in range(nholes):
            js = json.loads(self.p.stdout.readline())
            sts = None
            if self.dump and 'err' not in js:
                sts = []
                while True:
                    l = self.p.stdout.readline()
                    if l.startswith('END'): break
                    sts.append(parse_state(l))
            out.append((js, sts))
        return out

    def close(self):
        self.p.stdin.close(); self.p.wait()


def parse_state(l):
    a, b = l.split('|')
    p = a.split()
    mv = []
    for t in b.split():
        x, y, z = t.split(':'); mv.append((int(x), int(y), int(z)))
    return dict(i=int(p[1]), cls=int(p[2]), kind=int(p[3]), j=int(p[4]), L1=int(p[5]), L2=int(p[6]), inA=int(p[7]), inB=int(p[8]),
                pi=int(p[9]), N=int(p[10]), c6=tuple(map(int, p[11].split(','))), oncyc=int(p[12]), E=tuple(map(int, p[13].split(','))), mv=mv)


def to_line(name, adj, n):
    return f"{name} {n} " + ';'.join(','.join(map(str, adj[v])) for v in range(n))


def read_graphs(path, prefix=''):
    for l in open(path):
        p = l.split()
        if len(p) >= 3 and p[0].startswith(prefix):
            yield p[0], l.strip(), [list(map(int, r.split(','))) for r in p[2].split(';')]


def nholes(rot):
    return sum(1 for r in rot if len(r) == 5)


def cls_dicts(js):
    return [dict(zip(CLSF, c)) for c in js.get('cls', [])]
