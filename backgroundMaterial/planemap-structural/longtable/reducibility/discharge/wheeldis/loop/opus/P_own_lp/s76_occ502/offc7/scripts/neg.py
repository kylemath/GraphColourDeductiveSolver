"""HOFFC7 negative controls for offc_model (usage: neg.py OFFC [d]): swap two phi images, change one image letter,
flip a 5/N w-condition; count lines that still pass OffcOK."""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import offc_model as M
rows = [l for l in open(sys.argv[1]) if l.strip() and not l.startswith('#') and (len(sys.argv) < 3 or l.split()[0] == sys.argv[2])]
random.seed(7)
def run(line, mut):
    head, _, tail = line.partition(' # ')
    d, link, sword = head.split(); d = int(d)
    src, name = tail.split()[:2]
    kv = dict(t.split('=', 1) for t in tail.split()[2:])
    phi = {M.slot_parse(x): M.slot_parse(y) for x, y in (p.split('>') for p in kv['phi'].split(','))}
    rot, deg, adj = M.own_rot(name, set(phi))
    if mut == 'swap':
        ks = sorted(phi); a, b = random.sample(ks, 2); phi[a], phi[b] = phi[b], phi[a]
    if mut == 'letter':
        L = list(link); idx = [i for i, c in enumerate(L) if c in '5678']; i = random.choice(idx)
        L[i] = '6' if L[i] == '5' else '5'; link = ''.join(L)
    if mut == 'cond':   # flip a 5/N w-condition if any, else skip
        L = list(link); idx = [i for i, c in enumerate(L) if c in '5N' and ('w', i) not in phi.values()]
        if not idx: return None
        i = idx[0]; L[i] = 'N' if L[i] == '5' else '5'; link = ''.join(L)
    pat = M.pat_of(link, sword)
    return any(not M.offc_ok(d, rot, phi, pat, e) for e in (1, -1))
for mut in ('swap', 'letter', 'cond'):
    r = [run(l, mut) for l in rows]
    r2 = [x for x in r if x is not None]
    print(mut, 'lines', len(r2), 'still pass', sum(r2))
# broken window (as OFFC_SPEC's offcbroken): every s_{i-1} s_i pair adjacent, i.e. every w letter read as a five
_pf = M.pfive
M.pfive = lambda l: True
r = [run(l, None) for l in rows]
M.pfive = _pf
print('broken-window lines', len(r), 'still pass', sum(r))
