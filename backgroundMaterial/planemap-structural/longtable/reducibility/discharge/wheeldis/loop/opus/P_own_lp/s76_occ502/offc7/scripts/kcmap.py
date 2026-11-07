"""HOFFC7 (usage: kcmap.py P_OWN_LP OFFC KC55 OUT): map each kill's kc interior order to its own-window slots, compose with the line's phi, and check
OffcOK (offc_model) on gen_occ_kc's own rotation (the rot of the COcc modules), plus RingLinked."""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import offc_model as M
P = sys.argv[1]; offc = sys.argv[2]; kcf = sys.argv[3]; out = sys.argv[4]
sys.path.insert(0, os.path.join(P, 's74_leanglue'))
import gen_occ_kc as K

def kc_rot(canon):
    occ = K.G.gen_key(canon, 'X')
    rot = K.bridge_rot(occ)
    return {a: [(('I', i) if k == 'inl' else ('R', i)) for k, i in rot[a]] for a in rot}

def cyc_eq(s, t):
    if len(s) != len(t): return False
    return any(s[i:] + s[:i] == t for i in range(len(s))) if s else True

def ring_linked(r, rot):
    m = len(rot); fails = []
    occ = collections.defaultdict(list)
    for a in range(m):
        L = len(rot[a])
        for k in range(L):
            x = rot[a][k]
            if x[0] == 'R':
                if not 0 <= x[1] < r: fails.append('ring pos %d out of range' % x[1])
                occ[x[1]].append((a, k))
    for t in range(r):
        if not occ[t]: fails.append('ring %d unused' % t)
        if len(set(a for a, _ in occ[t])) != len(occ[t]): fails.append('ring %d twice at one vertex' % t)
    # links: (a,k)=inr t with (k+1)=inl b  ->  b has inr t at j+1 and inl a at j
    #        (a,k)=inr t with (k-1)=inl b  ->  b has inl a at j+1 and inr t at j
    def at(a, k): L = len(rot[a]); return rot[a][k % L]
    def link(a, k):
        t = rot[a][k][1]; res = []
        nb = at(a, k + 1)
        if nb[0] == 'I':
            b = nb[1]; L = len(rot[b])
            ok = [j for j in range(L) if at(b, j) == ('I', a) and at(b, j + 1) == ('R', t)]
            if not ok: fails.append('link fail %d %d t%d (after)' % (a, b, t))
            else: res.append((b, (ok[0] + 1) % L))
        nb = at(a, k - 1)
        if nb[0] == 'I':
            b = nb[1]; L = len(rot[b])
            ok = [j for j in range(L) if at(b, j + 1) == ('I', a) and at(b, j) == ('R', t)]
            if not ok: fails.append('link fail %d %d t%d (before)' % (a, b, t))
            else: res.append((b, ok[0]))
        return res
    fans = {}
    for t in range(r):
        if not occ[t]: continue
        seen = {occ[t][0]}; st = [occ[t][0]]
        while st:
            x = st.pop()
            for y in link(*x):
                if y not in seen: seen.add(y); st.append(y)
        if seen != set(occ[t]): fails.append('ring %d occurrences not linked' % t)
        # fan order: walk from an end (an occurrence with <2 links)
        fans[t] = sorted(a for a, _ in occ[t])
    return fails, fans

def iso_search(m, kdeg, kadj, verts, deg, adj):
    V = sorted(verts)
    order = sorted(range(m), key=lambda a: -len(kadj[a]))
    sols = []
    def bt(i, f, used):
        if i == m:
            sols.append(dict(f)); return
        a = order[i]
        for x in V:
            if x in used or deg[x] != kdeg[a] or len(adj[x]) != len(kadj[a]): continue
            if all((b in kadj[a]) == (f[b] in adj[x]) for b in f):
                f[a] = x; used.add(x); bt(i + 1, f, used); del f[a]; used.discard(x)
    bt(0, {}, set())
    return sols

lines = {}
for l in open(offc):
    if l.startswith('#') or not l.strip(): continue
    head, _, tail = l.partition(' # ')
    if head.split()[0] != '7': continue
    lines[tail.split()[1]] = l.rstrip('\n')
rows = []
for l in open(kcf):
    name, srcfile, canon = l.rstrip('\n').split('\t')
    line = lines[name]
    head, _, tail = line.partition(' # ')
    d, link, sword = head.split(); d = int(d)
    kv = dict(t.split('=', 1) for t in tail.split()[2:])
    phi = {M.slot_parse(x): M.slot_parse(y) for x, y in (p.split('>') for p in kv['phi'].split(','))}
    orot, deg, adj = M.own_rot(name, set(phi))
    n2, r, m, ra, ia = K.G.parse(canon)
    krot = kc_rot(canon)
    kdeg = {a: len(krot[a]) for a in range(m)}
    kadj = {a: set(x[1] for x in krot[a] if x[0] == 'I') for a in range(m)}
    note = []
    if m != len(phi): note.append('m %d != |K| %d' % (m, len(phi)))
    sols = iso_search(m, kdeg, kadj, set(phi), deg, adj) if not note else []
    good = []
    for f in sols:
        for sg in (1, -1):
            okall = True
            for a in range(m):
                s = [(f[x[1]] if x[0] == 'I' else ('R', None)) for x in krot[a]]
                t = orot[f[a]] if sg > 0 else list(reversed(orot[f[a]]))
                if not cyc_eq(s, t): okall = False; break
            if okall: good.append((f, sg))
    if not good:
        note.append('no rotation-preserving kc->slot map (%d graph isos)' % len(sols))
        rows.append((name, srcfile, d, link, sword, r, m, None, None, None, note, None, 0)); continue
    f, sg = good[0]
    phik = {a: phi[f[a]] for a in range(m)}
    rotm = {a: [(('I', x[1]) if x[0] == 'I' else ('R', x[1])) for x in krot[a]] for a in range(m)}
    # offc_model wants vertices as keys and ring markers 'R'
    rr = {('K', a): [(('R', None) if x[0] == 'R' else ('K', x[1])) for x in krot[a]] for a in range(m)}
    pat = M.pat_of(link, sword)
    eps = [e for e in (1, -1) if not M.offc_ok(d, rr, {('K', a): phik[a] for a in range(m)}, pat, e)]
    rl, fans = ring_linked(r, krot)
    if rl: note.append('RingLinked: ' + '; '.join(rl[:3]))
    if len(eps) != 1: note.append('OffcOK eps %s' % eps)
    rows.append((name, srcfile, d, link, sword, r, m, f, sg, eps, note, phik, len(good)))
with open(out, 'w') as o:
    o.write('name\tkc_src\td\tLINK\tSWORD\tr\tm\tphi_kc\teps\tmaps\tnote\n')
    for name, srcfile, d, link, sword, r, m, f, sg, eps, note, phik, ng in rows:
        sl = lambda x: 'u' if x[0] == 'u' else '%s%d' % x
        pk = ','.join('%d>%s' % (a, sl(phik[a])) for a in range(m)) if phik else '-'
        o.write('%s\t%s\t%d\t%s\t%s\t%d\t%d\t%s\t%s\t%s\t%s\n' % (name, srcfile, d, link, sword, r, m, pk,
                ('+' if eps == [1] else '-' if eps == [-1] else str(eps)) if eps is not None else '-',
                str(ng), '; '.join(note) or 'ok'))
c = collections.Counter('ok' if not x[10] else 'issue' for x in rows)
print(c)
for x in rows:
    if x[10]: print(x[0], x[10])
