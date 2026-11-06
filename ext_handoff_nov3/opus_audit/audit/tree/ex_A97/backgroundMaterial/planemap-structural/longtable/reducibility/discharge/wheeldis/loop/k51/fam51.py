"""EXPLORE round 51 part 2, re-pointed (Long Table, 09:32Z): the whole face-five family of Opus's stage 19b.
A member is a sender context of a five v: link w0..w4 (exact letters; 9 = degree >= 9, never exact), hat classes
H0..H4 (H_k = s_k, the ring-2 vertex between w_k and w_{k+1}; small = 5 or 6, big = >= 7) and fan classes of the
6-spokes (F_k = the one private of w_k).  A member is killed when every exact case (each small vertex 5 or 6) has a
D/C configuration inside its exact vertices (v, the exact w_k, the small hats and fans):
  1. registry containment (round 44's 582 RSST verified on two engines + explore's twoeng names; census50's matcher,
     interior onto exact vertices only), else
  2. windows: connected subsets of the exact vertices, ring <= RMAX, in order ring, more fives, more sixes; kc -C, a
     kc D re-run on dfast/dfast18, a kc C sent to cfast --fixed with kc's conservative X (drive45's rule).
Big and free vertices are never in a window (they sit on its ring).  Windows are cached by kc line, so a window
shared by several cases or members runs once.  Kill line: a member with a case that has no D/C at ring <= RMAX.
Window names p5_<u|-><w>_<s>_<f> (u = the five v): w_k letter if in the window, F/N if s_(k-1) and s_k are in it (edge iff w_k = 5),
x if only its fan is in it (w_k = 6); s_k and F_k letters or '.'.
usage: python3 fam51.py FAMILY [RMAX TSEC CAP_MEMBER_S CAP_TOTAL_S]   (NW workers, default 3; SURVEY=1 lists every
surviving case of every member instead of stopping at the first; TWOENG = dir of twoeng's k3x_D.out, k3x_C.cfast)"""
import sys, os, re, json, time, itertools, subprocess, tempfile, threading
from concurrent.futures import ThreadPoolExecutor, FIRST_COMPLETED, wait
H = os.path.dirname(os.path.abspath(__file__)); LOOP = os.path.join(H, '..')
W = os.path.normpath(os.path.join(LOOP, '..')); DIS = os.path.dirname(W)
sys.path.insert(0, os.path.join(DIS, 'b8b')); sys.path.insert(0, DIS); sys.path.insert(0, os.path.join(LOOP, 'k42'))
from rings import Layered
import grow
BIN = os.path.join(LOOP, '..', 'bin'); KCC = os.path.join(LOOP, 'kc', 'kcc')
D = 5

def build(LK, r2):
    """v's 2-ball: link LK (9 = placeholder for >= 9), ring-2 letters r2 by name (unspecified = 9), fresh ring 3."""
    L = Layered(D); L.add_ring(list(LK))
    Wr = L.rings[1]; Z = L.ring(); adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    name = {0: ('u',)}
    for i, w in enumerate(Wr): name[w] = ('w', i)
    Wi = {w: i for i, w in enumerate(Wr)}; cnt = {}
    for z in Z:
        ws = sorted(Wi[x] for x in adj[z] if x in Wi)
        if len(ws) == 2:
            i, j = ws; name[z] = ('s', j if (i, j) == (0, D - 1) else i)
        else:
            i = ws[0]; cnt[i] = cnt.get(i, 0) + 1; name[z] = ('p', i, cnt[i])
    L.add_ring([r2.get(name[z], 9) for z in Z])
    adj = {}
    for a, b, c in L.tris:
        for x, y in ((a, b), (b, c), (c, a)): adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    return adj, name, {frozenset(t) for t in L.tris}

def extract(adj, I, deg):
    Is = set(I); RS = set(y for x in I for y in adj[x]) - Is
    for y in RS:
        if len(adj[y] & RS) != 2: return None
    start = min(RS); order = [start]; prev = None
    while True:
        cur = order[-1]; nb = sorted(adj[cur] & RS); nxt = nb[0] if nb[0] != prev else nb[1]
        if nxt == start: break
        order.append(nxt); prev = cur
    if len(order) != len(RS): return None
    for x in I: assert len(adj[x]) == deg[x], (x, len(adj[x]), deg[x])
    ri = {y: j for j, y in enumerate(order)}; Il = sorted(I); ii = {x: j for j, x in enumerate(Il)}
    f = lambda Ls: ';'.join(','.join(map(str, v)) if v else '-' for v in Ls)
    ia = [sorted(ii[y] for y in adj[x] if y in Is) for x in Il]
    ra = [sorted(ri[y] for y in adj[x] if y in RS) for x in Il]
    return len(order), len(Il), f(ra), f(ia)

def cases(m):
    """Exact-degree dicts of a member, hardest (most sixes) first.  A member from family.json brings its own expansion
    (every exact 5/6 choice of its small vertices, admissible or not); otherwise every choice is generated."""
    LK = m['word']; base = {('u',): D}; base.update({('w', k): LK[k] for k in range(D) if LK[k] != 9})
    slots = [('s', k) for k in range(D) if m['hat'][k] == 'S'] + [('p', k, 1) for k in sorted(m['fan']) if m['fan'][k] == 'S']
    base.update({('s', k): m['hat'][k] for k in range(D) if isinstance(m['hat'][k], int)})
    base.update({('p', k, 1): v for k, v in m['fan'].items() if isinstance(v, int)})
    if 'exp' in m:
        nm = lambda x: ('s', x[1]) if x[0] == 'H' else ('p', x[1], 1)
        assert all({nm(e) for e in c} == set(slots) for c in m['exp']), (m['id'], slots)
        allc = [tuple(c[x] for x in slots) for c in ({nm(k): v for k, v in c.items()} for c in m['exp'])]
        assert len(set(allc)) == len(allc) == 2 ** len(slots), m['id']
    else: allc = list(itertools.product((6, 5), repeat=len(slots)))
    out = []
    for lets in sorted(allc, key=lambda c: (sum(x == 5 for x in c), [-x for x in c])):
        d = dict(base); d.update(zip(slots, lets)); out.append(d)
    return slots, out

def wname(S, deg, LK):
    w = ''.join(str(LK[k]) if ('w', k) in S else ('F' if LK[k] == 5 else 'N') if (('s', (k - 1) % D) in S and ('s', k) in S)
                else 'x' if ('p', k, 1) in S else '.' for k in range(D))
    s = ''.join(str(deg[('s', k)]) if ('s', k) in S else '.' for k in range(D))
    f = ''.join(str(deg[('p', k, 1)]) if ('p', k, 1) in S else '.' for k in range(D))
    return 'p5_%s%s_%s_%s' % ('u' if ('u',) in S else '-', w, s, f)

def windows(LK, deg, RMAX, cache):
    """Connected windows of the exact vertices at ring <= RMAX: list of (ring, name, kc line), engine order."""
    r2 = {x: v for x, v in deg.items() if x[0] in 'sp'}
    key = (tuple(LK), tuple(sorted(r2.items())))   # the build depends on the word too
    if key not in cache: cache[key] = build(LK, r2)
    adj, name, _ = cache[key]; inv = {v: x for x, v in name.items()}
    V = sorted(deg); idx = {x: k for k, x in enumerate(V)}
    nb = {x: {name[y] for y in adj[inv[x]] if name.get(y) in deg} for x in V}
    seen = set(); out = []
    def grow_(S, ext):
        if S in seen: return
        seen.add(S)
        if len(S) >= 2:
            X = [inv[x] for x in S]; c = extract(adj, X, {inv[x]: deg[x] for x in S})
            if c and c[0] <= RMAX:
                nm = wname(S, deg, LK)
                out.append((c[0], -sum(deg[x] == 5 for x in S), -sum(deg[x] == 6 for x in S), nm, '%s %d %d %s %s' % ((nm,) + c)))
        for y in ext:
            if idx[y] > idx[min(S, key=lambda z: idx[z])]: grow_(S | {y}, (ext | nb[y]) - S - {y})
    for x in V: grow_(frozenset([x]), frozenset(nb[x]))
    out.sort(); return out

def registry(TD, TC):
    """RSST 582 + explore twoeng names as grow.kcline tuples (census50.registry)."""
    import glob
    K44 = os.path.join(LOOP, 'k44')
    ok = {l.split()[0] for l in open(os.path.join(K44, 'rsst_verdicts.txt')) if not l.startswith('#') and
          ('verdict=D2' in l.split() or 'verdict=C2cons' in l.split())}
    assert len(ok) == 582
    kcn = [l.split()[0] for l in open(os.path.join(K44, 'rsst.txt')) if l.strip()]
    C = [(n,) + tuple(c[1:]) for n, c in zip(kcn, grow.rsst()) if n in ok]
    want = {l.split()[0] for l in open(TD) if re.match(r'^[epf]\d+_', l)} | \
           {l.split()[0] for l in open(TC) if re.match(r'^[epf]\d+_\S+ r=\d+ ', l)}
    got = {}; pat = re.compile(r'^([epf]\d+_\S+) (\d+) (\d+) (\S+) (\S+)$')
    for fn in sorted(glob.glob(os.path.join(LOOP, 'k[0-9]*', '*'))):
        if not os.path.isfile(fn): continue
        try:
            for l in open(fn):
                mm = pat.match(l.rstrip('\n'))
                if mm and mm.group(1) in want and mm.group(1) not in got: got[mm.group(1)] = grow.kcline(l, 'explore')
        except UnicodeDecodeError: continue
    return C + list(got.values()), len(want) - len(got)

def contained(REG, LK, deg, cache):
    """First registry configuration whose interior maps onto exact vertices of this case, or None."""
    r2 = {x: v for x, v in deg.items() if x[0] in 'sp'}; key = (tuple(LK), tuple(sorted(r2.items())))   # the build depends on the word too
    if key not in cache: cache[key] = build(LK, r2)
    adj, name, faces = cache[key]; inv = {v: x for x, v in name.items()}
    P = sorted(deg); pa = {x: {name[y] for y in adj[inv[x]] if name.get(y) in deg} for x in P}
    pf = {frozenset(name[y] for y in f) for f in faces if all(name.get(y) in deg for y in f)}
    for c in REG:
        if len(c[2]) > len(P): continue
        if grow.embeddings(c, P, pa, pf, deg): return c[0]
    return None

class Engines:
    """drive45's per-window rule, with results cached by kc line in F_res.txt (name verdict line)."""
    def __init__(self, TSEC):
        self.T = TSEC; self.lock = threading.Lock()
        self.ko, self.do, self.co = (open(os.path.join(H, x), 'a') for x in ('F_kcc.out', 'F_df.out', 'F_cf.out'))
        self.res = {}
        fr = os.path.join(H, 'F_res.txt')
        if os.path.exists(fr):
            for l in open(fr):
                f = l.rstrip('\n').split(' ', 2)
                if len(f) == 3: self.res[f[2]] = f[1]
        self.fr = open(fr, 'a')
    def run(self, cmd, inp=None):
        return subprocess.run(cmd, input=inp, capture_output=True, text=True).stdout.rstrip('\n')
    def verdict(self, line):
        k = line.split(' ', 1)[1]
        if k in self.res: return self.res[k]
        nm, r = line.split()[0], int(line.split()[1])
        t0 = time.time(); o = self.run([KCC, '-C', '-s', '60', '-t', str(self.T)], line + '\n')
        with self.lock: self.ko.write(o + '\n'); self.ko.flush()
        v = 'none'
        if 'D=true' in o.split('\n')[0]:
            o2 = self.run([os.path.join(BIN, 'dfast' if r <= 16 else 'dfast18'), '/dev/stdin'], line + '\n')
            with self.lock: self.do.write(o2 + '\n'); self.do.flush()
            v = 'D' if 'D=true' in o2 else 'MISMATCH-D'
        m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', o)
        if v == 'none' and m:
            with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as t: t.write(line + '\n')
            o3 = self.run([os.path.join(BIN, 'cfast'), t.name, '--fixed', m.group(1)]); os.unlink(t.name)
            with self.lock: self.co.write(o3 + '\n'); self.co.flush()
            v = 'C{%s}' % m.group(1) if 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in o3 else 'CFAST-REJECTS'
        if v == 'none' and 'INCOMPLETE' in o.split('\n')[0]: v = 'timeout'   # kc -t hit (exit 3, no C line)
        with self.lock:
            self.res[k] = v; self.fr.write('%s %s %s\n' % (nm, v, k)); self.fr.flush()
        return v

def kills(v): return v == 'D' or v.startswith('C{')

def member(word, hats, fans, mid=None):
    """word: 5 letters (9 = >= 9); hats: H0..H4 as 0/'S' small, 1/'B' big, or an exact letter 5..8; fans: the 6-spokes'
    fans in order, same coding.  Privates of non-6 spokes are free."""
    LK = [int(c) for c in str(word)]; assert len(LK) == D
    code = lambda b: 'S' if b in (0, '0', 'S', 's') else 'B' if b in (1, '1', 'B', 'b') else int(b)
    six = [k for k in range(D) if LK[k] == 6]; assert len(fans) == len(six), (word, fans)
    return {'id': mid or '%s %s|%s' % (word, ','.join(map(str, hats)), ','.join(map(str, fans))),
            'word': LK, 'hat': [code(b) for b in hats], 'fan': {k: code(b) for k, b in zip(six, fans)}}

def load(fn):
    """Wf.txt-style lines 'word H0,..,H4|F..', or a JSON list of {word, hats, fans[, id]} (adapted to family.json)."""
    txt = open(fn).read()
    if fn.endswith('.json'):                 # Opus s19e/family.json: the senders, heaviest max dual first
        J = json.loads(txt); out = []
        for e in sorted(J['senders'], key=lambda e: -max(e['dual'].values())):
            m = member(e['word'], e['H'], e['F'])
            m['exp'] = [{(k[0], int(k[1:])): v for k, v in c['letters'].items()} for c in e['expansion']]
            m['adm'] = sum(c['admissible'] for c in e['expansion']); m['dual'] = max(e['dual'].values()); out.append(m)
        return out
    out = []
    for l in txt.splitlines():
        if not l.strip() or l.startswith('#'): continue
        w, b = l.split(); h, f = b.split('|')
        out.append(member(w, h.split(','), [x for x in f.split(',') if x]))
    return out

def main():
    FAM = sys.argv[1]; A = sys.argv[2:]
    RMAX = int(A[0]) if A else 18; TSEC = int(A[1]) if len(A) > 1 else 600
    CAPM = int(A[2]) if len(A) > 2 else 3600; CAPT = int(A[3]) if len(A) > 3 else 28800
    NW = int(os.environ.get('NW', '3')); TW = os.environ['TWOENG']; SURVEY = os.environ.get('SURVEY') == '1'
    members = load(FAM)
    REG, miss = registry(os.path.join(TW, 'k3x_D.out'), os.path.join(TW, 'k3x_C.cfast'))
    tag = os.path.splitext(os.path.basename(FAM))[0] + ('_survey' if SURVEY else '')
    log = open(os.path.join(H, 'fam51_%s.log' % tag), 'a')
    def say(*a):
        s = ' '.join(map(str, a)); print(s, flush=True); log.write(s + '\n'); log.flush()
    say('# %s start %s: %d members, RMAX %d, TSEC %d, caps %d s/member %d s total, registry %d configurations (%d names without kc line)'
        % (tag, time.strftime('%H:%MZ', time.gmtime()), len(members), RMAX, TSEC, CAPM, CAPT, len(REG), miss))
    eng = Engines(TSEC); bcache = {}; T0 = time.time(); verdicts = []
    for m in members:
        t0 = time.time(); slots, cs = cases(m); st = 'killed'; hold = None; surv = []
        say('member %s: %d cases over %s%s' % (m['id'], len(cs), ' '.join('%s%s' % (x[0], ''.join(map(str, x[1:]))) for x in slots),
            ' (max dual %.3f, %d admissible per Opus)' % (m['dual'], m['adm']) if 'adm' in m else ''))
        for deg in cs:
            cid = ''.join(str(deg[x]) for x in slots) or '-'
            r = contained(REG, m['word'], deg, bcache)
            if r: say('  case %s: registry %s' % (cid, r)); continue
            ws = windows(m['word'], deg, RMAX, bcache); found = None; tos = []; capped = False
            with ThreadPoolExecutor(NW) as ex:
                it = iter(ws); fut = {}
                def top():
                    while len(fut) < NW and not found and not capped:
                        w = next(it, None)
                        if w is None: return
                        fut[ex.submit(eng.verdict, w[4])] = w
                top()
                while fut:
                    done, _ = wait(list(fut), return_when=FIRST_COMPLETED)
                    for f in done:
                        w = fut.pop(f); v = f.result()
                        if v.startswith('MISMATCH') or v == 'CFAST-REJECTS': say('  !! %s %s' % (v, w[3]))
                        if kills(v) and (found is None or w < found[0]): found = (w, v)
                        if v == 'timeout': tos.append(w[3])
                    if time.time() - t0 > CAPM or time.time() - T0 > CAPT: capped = True
                    top()
            if found:
                say('  case %s: %s ring %d %s' % (cid, found[1], found[0][0], found[0][3])); continue
            st1 = 'cap' if capped else 'timeouts' if tos else 'survives'
            if SURVEY and st1 == 'survives':           # survey mode: list every surviving case, keep going
                say('  case %s: SURVIVES (%d windows at ring <= %d)' % (cid, len(ws), RMAX)); surv.append(cid); continue
            st = st1; hold = (cid, len(ws), tos[:5]); break
        if surv and st == 'killed': st = 'survives'; hold = (','.join(surv), 0, [])
        dt = time.time() - t0
        if st == 'killed': say('member %s KILLED (%d s)' % (m['id'], dt))
        else: say('member %s %s at case %s: %d windows at ring <= %d, timeouts %s (%d s)' % ((m['id'], st.upper()) + hold[:2] + (RMAX, hold[2], dt)))
        verdicts.append((m['id'], st, hold))
        if st == 'survives' and not SURVEY: say('# KILL LINE MET: member %s case %s has no D/C window at ring <= %d' % (m['id'], hold[0], RMAX)); break
        if time.time() - T0 > CAPT: say('# total cap hit'); break
    say('# %s end %s: %s' % (tag, time.strftime('%H:%MZ', time.gmtime()), '; '.join('%s %s' % (a, b) for a, b, _ in verdicts)))

if __name__ == '__main__':
    main()
