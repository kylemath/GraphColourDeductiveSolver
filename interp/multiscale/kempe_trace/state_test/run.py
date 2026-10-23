"""usage: run.py EXP  (EXP = L<L>_<side> or opus_<side>).  Writes pop_<EXP>.json"""
import sys, json, random, time, hashlib
sys.path.insert(0, '/mnt/project-files/multiscale/kempe_trace/state_test')
from st import *
from pysat.solvers import Cadical153
OUT = '/mnt/project-files/multiscale/kempe_trace/state_test/'
NALL, NCOL, NDEEP, NBEL = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])

def sampler(adj, S, fixed, rng):
    vs = sorted(S); ix = {v: k for k, v in enumerate(vs)}; x = lambda v, c: 4*ix[v] + c + 1; cls = []
    for v in vs:
        cls.append([x(v, c) for c in range(4)])
        for c in range(4):
            for c2 in range(c+1, 4): cls.append([-x(v, c), -x(v, c2)])
        for u in adj[v]:
            if u in ix and u > v:
                for c in range(4): cls.append([-x(v, c), -x(u, c)])
    s = Cadical153(bootstrap_with=cls); ass = [x(v, c) for v, c in fixed.items()]
    if not s.solve(assumptions=ass): s.delete(); return None
    free = [v for v in vs if v not in fixed]; rng.shuffle(free)
    for v in free:
        cs = list(range(4)); rng.shuffle(cs)
        for c in cs:
            if s.solve(assumptions=ass + [x(v, c)]): ass.append(x(v, c)); break
    s.solve(assumptions=ass); mod = set(l for l in s.get_model() if l > 0); s.delete()
    return {v: next(c for c in range(4) if x(v, c) in mod) for v in vs}

H = lambda o: hashlib.md5(repr(o).encode()).hexdigest()[:12]
exp = sys.argv[1]
ce = json.load(open('/mnt/project-files/multiscale/opus_attack/bandfill/counterexamples.json'))
if exp.startswith('opus'):
    side = exp[-1]; E = opus_setup(side); w = 4; k0 = 10 if side == 'A' else 8
else:
    L = int(exp[1:].split('_')[0]); side = exp[-1]; c = [c for c in ce if c['L'] == L][0]
    E = tube_setup(c, side); w = c['w']
    mb = json.load(open(f'/mnt/project-files/multiscale/kempe_trace/minimal_bad/tube_L{L}_{side}_w{w}_k' +
                        [f for f in os.listdir('/mnt/project-files/multiscale/kempe_trace/minimal_bad') if f.startswith(f'tube_L{L}_{side}_')][0].split('_k')[1]))
    k0 = mb['k0']
L = E['L']; tris = tri_list(E['adj'], E['S']); rng = random.Random(hash(exp) % 1000)
recs = []
def add(mode, col):
    t0 = time.time()
    ob = unsat(E['adj'], E['S'], col, E['bd'], w, k0)
    rows, Hs = state(E, col, w, tris); pb, pt = parity_check(rows, E, col)
    K = keys(rows, Hs, L, w)
    word = lambda r: ''.join(str(col[v]) for v in E['rowv'](r))
    recs.append(dict(mode=mode, obstructing=ob, heights=Hs, rows=[word(r) for r in range(w+1)],
                     keys={k: H(v) for k, v in K.items()}, parity_bad=pb, parity_tot=pt,
                     colour=''.join(str(col[v]) for v in sorted(E['S'])),
                     sec=round(time.time()-t0, 2)))
add('orig', E['col'])
seam = {v: E['col'][v] for v in E['bd']}
for i in range(NALL):
    col = sampler(E['adj'], E['S'], seam, rng); add('all', col)
for i in range(NCOL):
    fx = {v: E['col'][v] for v in E['S'] if E['depth'][v] == 0 or E['depth'][v] >= w}
    col = sampler(E['adj'], E['S'], fx, rng); add('collar', col)
for i in range(NDEEP):
    fx = {v: E['col'][v] for v in E['S'] if E['depth'][v] <= w-1}
    col = sampler(E['adj'], E['S'], fx, rng); add('deep', col)
for i in range(NBEL):
    fx = {v: E['col'][v] for v in E['S'] if E['depth'][v] <= w}
    col = sampler(E['adj'], E['S'], fx, rng); add('below', col)
json.dump(dict(exp=exp, L=L, w=w, k0=k0, seam=recs[0]['rows'][0], recs=recs), open(OUT + f'pop_{exp}.json', 'w'))
print(exp, 'L', L, 'w', w, 'k0', k0, 'n', len(recs), 'obstructing', sum(r['obstructing'] for r in recs), flush=True)
