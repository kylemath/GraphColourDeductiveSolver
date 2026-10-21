"""pubrules: which PUBLISHED discharging rules move charge in a binder row (diagnostic map only; nothing here is a claim).

Input: binder rows in the receiverR2 form used by certs and explore queues, one per line:
    [w] d LINK SWORD [anything]        e.g.  -0.05701 7 7766556 6567568
w (the dual weight) is optional; '#' lines are skipped.  LINK = w_0..w_{d-1} (letters 5..8), SWORD = s_0..s_{d-1}
(letters 5..9, 9 = degree >= 9), s_i the apex of w_i w_{i+1} (window model of RELAY_SPEC_s39o 39.1).

Rule sets (both vendored under data/, see README.md):
- RSST: the 32 rules of Robertson-Sanders-Seymour-Thomas as Gonthier's Coq parts (discharge.v drule1..drule32,
  base_drules with multiplicity, 71 parts after symmetrize).  Fit semantics as Studio's rsst_score.py: a part fits at
  hub h when deg h = #subparts and every spoke / hat / fan range holds; each fit moves 1 unit from h to its third spoke.
- NL26: the 43 rules (84 files with mirrors) of Inoue et al. 2026, github.com/near-linear-4ct/discharging-rules (MIT).
  File: 'n src dst amount', then per vertex 'id lo hi nb.. -1' (hi 0 = unbounded); a neighbour list is a consecutive
  arc of that vertex's rotation (a full list closes it).  A rule applies once per (file, source, target) pair when
  its graph embeds (injective, arcs onto consecutive rotation slots, degrees in range).  Mirror files are matched
  in one fixed orientation, so _1/_2 labels may be swapped relative to the authors' drawing; the set is mirror-closed.
Both use charge 10(6 - deg); 1 unit = 0.1 in our 6 - deg scale.

Window: u, link w_i, apexes s_i, the privates p_i.k of each w_i (d_i - 5 of them, degree unknown 5..9+), and a fresh
third ring (degree unknown).  A rule test on a private becomes a condition; on ring 3 (or beyond) it is OPEN.
For every filling of the privates (5..9), u's net charge is reported as an interval [certain, possible].

usage: python3 pubrules.py ROWS.txt [--out REPORT.md] [--sets rsst,nl26] [--max-fill N] [--self-test]
"""
import os, re, sys, itertools, collections, argparse
import numpy as np

H = os.path.dirname(os.path.abspath(__file__))
FULL = (5, 9)

# ------------------------------------------------------------------ window
class Window:
    """u's 2-ball plus a fresh ring 3 as an explicit plane triangulated patch (ccw rotations)."""
    def __init__(self, d, link, sword):
        assert len(link) == d and len(sword) == d, 'row length'
        assert all(5 <= x <= 8 for x in link), 'link letters must be 5..8 (a 9+ link vertex has unknown privates)'
        self.d, self.link, self.sword = d, link, sword
        U = ('u',); W = [('w', i) for i in range(d)]; S = [('s', i) for i in range(d)]
        self.deg = {U: d}
        for i in range(d): self.deg[W[i]] = link[i]; self.deg[S[i]] = sword[i]
        self.priv = []
        R2 = []
        for i in range(d):
            for k in range(1, link[i] - 4):
                p = ('p', i, k); R2.append(p); self.priv.append(p)
            R2.append(S[i])
        self.R2 = R2
        faces = []
        for i in range(d):
            faces.append((U, W[i], W[(i + 1) % d]))
            seg = [S[(i - 1) % d]] + [('p', i, k) for k in range(1, link[i] - 4)] + [S[i]]
            for a, b in zip(seg, seg[1:]): faces.append((W[i], a, b))
            faces.append((W[i], S[i], W[(i + 1) % d]))
        # ring 3: r has c_r = deg - #w - 2 ring-3 neighbours; consecutive r share one (union-find on the joints)
        par = {}
        def f(x):
            while par.get(x, x) != x: x = par[x]
            return x
        n = len(R2); runs = []
        for k, r in enumerate(R2):
            nw = 2 if r[0] == 's' else 1
            dr = 8 if r[0] == 'p' else min(self.deg[r], 9)
            c = dr - nw - 2
            assert c >= 1, ('ring-2 vertex too small', r)
            first, last = ('j', (k - 1) % n), ('j', k)
            if c == 1: par[f(first)] = f(last)
            runs.append((first, [('t', k, m) for m in range(1, c - 1)], last, c))
        for k, r in enumerate(R2):
            first, mids, last, c = runs[k]
            T = [f(first)] if c == 1 else [f(first)] + mids + [f(last)]
            prv, nxt = R2[(k - 1) % n], R2[(k + 1) % n]
            faces.append((r, prv, T[0]))
            for a, b in zip(T, T[1:]): faces.append((r, a, b))
            # (r, T[-1], nxt) is the same face as nxt's (nxt, r, T0)
        self.faces = faces
        self.opp, self.succ = {}, collections.defaultdict(dict)
        for a, b, c in faces:
            for x, y, z in ((a, b, c), (b, c, a), (c, a, b)):
                assert (x, y) not in self.opp, ('face clash', x, y)
                self.opp[(x, y)] = z; self.succ[x][y] = z
        self.known = [U] + W + S
        self.ring3 = sorted({v for fc in faces for v in fc if v[0] in 'jt'}, key=str)
        self._rot = {}

    def rot(self, x):
        """('cyc', list) for a closed rotation, ('path', list) for a partial one (ring 3)."""
        if x in self._rot: return self._rot[x]
        s = self.succ[x]; preds = set(s.values())
        starts = [y for y in s if y not in preds]
        if not starts:
            y0 = min(s, key=str); cyc = [y0]
            while s[cyc[-1]] != y0: cyc.append(s[cyc[-1]])
            assert len(cyc) == len(s)
            r = ('cyc', cyc)
        else:
            assert len(starts) == 1, ('rotation not a path', x)
            path = [starts[0]]
            while path[-1] in s: path.append(s[path[-1]])
            r = ('path', path)
        self._rot[x] = r
        return r

    def kind(self, v):
        if v in self.deg: return 'known'
        if v[0] == 'p': return 'priv'
        return 'open'

    def name(self, v):
        if v == ('u',): return 'u'
        if v[0] in 'ws': return '%s%d' % v
        if v[0] == 'p': return 'p%d.%d' % (v[1], v[2])
        return 'T'

# ------------------------------------------------------------------ condition algebra
class Alt:
    """one way a rule instance fires: conjunction of private-degree ranges, plus OPEN if ring 3+ was read."""
    __slots__ = ('c', 'open')
    def __init__(self): self.c = {}; self.open = False
    def need(self, w, v, R):
        """record 'deg v in R'; returns False if impossible."""
        R = (R[0], min(R[1], 9))
        k = w.kind(v)
        if k == 'known':
            dv = min(w.deg[v], 9)
            return R[0] <= dv <= R[1]
        if R == FULL: return True
        if k == 'priv':
            lo, hi = self.c.get(v, FULL); lo, hi = max(lo, R[0]), min(hi, R[1])
            if lo > hi: return False
            self.c[v] = (lo, hi); return True
        self.open = True; return True
    def copy(self):
        a = Alt(); a.c = dict(self.c); a.open = self.open; return a
    def text(self, w):
        parts = []
        for v, (lo, hi) in sorted(self.c.items()):
            parts.append('%s%s' % (w.name(v), rtxt((lo, hi))))
        if self.open: parts.append('ring3')
        return ' & '.join(parts) if parts else 'always'

def rtxt(R):
    lo, hi = R
    if lo == hi: return '=%d' % lo if lo < 9 else '>=9'
    if hi == 9: return '>=%d' % lo
    if lo == 5: return '<=%d' % hi
    return 'in%d..%d' % (lo, hi)

# ------------------------------------------------------------------ RSST (Gonthier parts)
def rng(tok):
    if tok == '*': return (5, 9)
    m = re.fullmatch(r'(\d)\?(\d)', tok)
    if m: return (int(m.group(1)), int(m.group(2)))
    m = re.fullmatch(r'(\d)\+', tok)
    if m: return (int(m.group(1)), 9)
    m = re.fullmatch(r'(\d)-', tok)
    if m: return (5, int(m.group(1)))
    return (int(tok), int(tok))

def parse_part(txt):
    body = txt.strip(); assert body.endswith('$'); body = body[:-1]
    subs = []
    for m in re.finditer(r'\$\s*(\[([^\]]*)\])?\s*([^\s$\[\]]+)', body):
        br, sp = m.group(2), rng(m.group(3))
        hat, fans = (5, 9), []
        if br is not None:
            t = br.split(); hat = rng(t[0]); fans = [rng(x) for x in t[1:]]
        if sp[0] == sp[1] and 6 <= sp[0] <= 8:
            fans = fans + [(5, 9)] * (sp[0] - 5 - len(fans))
        subs.append((sp, hat, tuple(fans)))
    return subs

def mirror(p):
    n = len(p); out = []
    for k2 in range(n):
        k = (4 - k2) % n; sp, _, fans = p[k]; hat = p[(5 - k2) % n][1]
        out.append((sp, hat, tuple(reversed(fans))))
    return out

def _sub(a, b): return b[0] <= a[0] and a[1] <= b[1]
def part_subset(p, q):
    if len(p) != len(q): return False
    for (s1, h1, f1), (s2, h2, f2) in zip(p, q):
        if not (_sub(s1, s2) and _sub(h1, h2)): return False
        if f2 and not f1: return False
        if f1 and f2 and not all(_sub(a, b) for a, b in zip(f1, f2)): return False
    return True

def load_rsst():
    src = open(os.path.join(H, 'data', 'rsst_drules.v')).read()
    DR = {m.group(1): parse_part(m.group(2)) for m in re.finditer(r"Definition (drule\d+'?)\s*:=\s*Part (.*?)\.\n", src)}
    base = re.search(r'Definition base_drules : drules := @seqn part 38(.*?)\.', src, re.S).group(1).split()
    assert len(base) == 38
    rules, seen = [], collections.Counter()
    for nm in base:
        seen[nm] += 1; tag = nm + ('#2' if seen[nm] > 1 else '')
        p = DR[nm]; pm = mirror(p)
        rules.append((tag, p))
        if not part_subset(p, pm): rules.append((tag + 'm', pm))
    assert len(rules) == 71, len(rules)
    return rules

def rsst_fit(w, h, S, a, p):
    """Alt or None for part p at hub h (ccw spokes S), anchor a."""
    n = len(S); alt = Alt()
    for j, (sp, hr, fr) in enumerate(p):
        x = S[(a + j) % n]; xp = S[(a + j - 1) % n]; xn = S[(a + j + 1) % n]
        if not alt.need(w, x, sp): return None
        hv = w.opp.get((x, xp))
        if hr != FULL:
            if hv is None: alt.open = True
            elif not alt.need(w, hv, hr): return None
        if fr and any(r != FULL for r in fr):
            k = w.kind(x)
            if k != 'known': alt.open = True; continue      # private / ring-3 spoke: its fans are ring 3
            hn = w.opp.get((xn, x))
            kind, R = w.rot(x)
            if hv is None or hn is None or kind != 'cyc': alt.open = True; continue
            i = R.index(hv); F = []
            while True:
                i = (i + 1) % len(R)
                if R[i] == hn: break
                F.append(R[i])
            if len(F) != len(fr): return None
            for fv, Rg in zip(F, fr):
                if not alt.need(w, fv, Rg): return None
    return alt

def rsst_instances(w, rules, hubs):
    """[(rule, hub, target, Alt)] for every fit at the given hubs."""
    out = []
    for h in hubs:
        kind, S = w.rot(h)
        if kind != 'cyc': continue
        n = len(S)
        if not (5 <= n <= 8) or w.deg.get(h) != n: continue
        for a in range(n):
            for nm, p in rules:
                if len(p) != n: continue
                alt = rsst_fit(w, h, S, a, p)
                if alt is not None: out.append((nm, h, S[(a + 2) % n], alt))
    return out

# ------------------------------------------------------------------ NL26 (rule graphs)
def load_nl26():
    D = os.path.join(H, 'data', 'nl2026', 'R'); rules = []
    for fn in sorted(os.listdir(D)):
        if not fn.endswith('.rule'): continue
        L = [l.split() for l in open(os.path.join(D, fn)) if l.strip()]
        n, s, t, amt = map(int, L[0]); V = {}
        for row in L[1:]:
            vid, lo, hi = int(row[0]), int(row[1]), int(row[2])
            nb = [int(x) for x in row[3:]]
            closed = not nb or nb[-1] != -1           # no -1 terminator: the list is the whole rotation
            if not closed: nb = nb[:-1]
            R = (lo, 9 if hi == 0 or hi >= 9 else hi)
            if closed and nb: R = (max(R[0], len(nb)), min(R[1], len(nb)))
            V[vid] = (R, nb, closed)
        assert len(V) == n
        rules.append((fn[:-5], s, t, amt, V))
    return rules

class Anon:
    _n = 0
    def __init__(self): Anon._n += 1; self.id = Anon._n
    def __repr__(self): return 'anon%d' % self.id

def nl_embed(w, rule, a, b):
    """all Alts for rule with source -> a, target -> b."""
    nm, s, t, amt, V = rule
    res = []
    order = sorted(V)
    def is_anon(x): return isinstance(x, Anon)

    def placements(x, k, vneed, closed):
        """lists of k images for an arc at image x (None-free); each item may be an Anon; plus extra Alt conditions."""
        if is_anon(x):
            yield [Anon() for _ in range(k)], None, True; return
        if w.kind(x) == 'priv':
            _, R = w.rot(x)                    # built at degree 8: w_i, prev, J1, t, t, t, J2, next (cyclic)
            ti = [i for i, v in enumerate(R) if v[0] == 't']; assert len(ti) == 3
            st = next(i for i in ti if R[(i - 1) % len(R)][0] != 't')
            R = R[st:] + R[:st]                # mids first, then the 5 fixed neighbours
            mids, core = R[:3], R[3:]
            for N in range(max(5, vneed[0]), min(9, vneed[1]) + 1):
                if closed and N != k: continue
                g = N - 5
                Rn = (mids[:g] if g <= 3 else mids + [Anon() for _ in range(g - 3)]) + core
                L = len(Rn)
                if k > L: continue
                for j in range(L):
                    yield [Rn[(j + l) % L] for l in range(k)], (x, (N, N)), False
            return
        kind, R = w.rot(x)
        if kind == 'cyc':
            L = len(R)
            if k > L or (closed and k != L): return
            for j in range(L):
                yield [R[(j + l) % L] for l in range(k)], None, False
        else:
            L = len(R)
            for o in range(-(k - 1), L):
                imgs = [R[o + l] if 0 <= o + l < L else None for l in range(k)]
                op = closed or any(v is None for v in imgs)
                yield [v if v is not None else Anon() for v in imgs], None, op

    def rec(phi, used, done, alt):
        todo = [v for v in order if v in phi and v not in done]
        if not todo:
            if len(phi) < len(V):
                return  # disconnected rule part (should not happen)
            alt2 = alt.copy()
            for v, (R, _, _) in V.items():
                x = phi[v]
                if is_anon(x):
                    if R != FULL: alt2.open = True
                elif not alt2.need(w, x, R): return
            res.append(alt2); return
        v = todo[0]; x = phi[v]; R, arc, closed = V[v]
        if not arc:
            rec(phi, used, done | {v}, alt); return
        for imgs, cond, op in placements(x, len(arc), R, closed):
            phi2, used2, alt2, ok = dict(phi), set(used), alt.copy(), True
            if op: alt2.open = True
            if cond is not None and not alt2.need(w, cond[0], cond[1]): continue
            for nbv, img in zip(arc, imgs):
                if nbv in phi2:
                    y = phi2[nbv]
                    if y == img: continue
                    if is_anon(img) or is_anon(y):
                        if is_anon(img) and not is_anon(y) and w.kind(y) != 'open': ok = False; break
                        alt2.open = True; continue
                    ok = False; break
                if is_anon(img):
                    phi2[nbv] = img; continue
                if img in used2: ok = False; break
                phi2[nbv] = img; used2.add(img)
            if ok: rec(phi2, used2, done | {v}, alt2)

    if a == b: return res
    rec({s: a, t: b}, {a, b}, frozenset(), Alt())
    return res

def nl_instances(w, rules, pairs):
    out = []
    for rule in rules:
        for a, b in pairs:
            alts = nl_embed(w, rule, a, b)
            if alts:
                # keep only minimal alternatives (drop exact duplicates)
                seen = set(); keep = []
                for al in alts:
                    key = (tuple(sorted(al.c.items())), al.open)
                    if key not in seen: seen.add(key); keep.append(al)
                out.append((rule[0], a, b, rule[3], keep))
    return out

# ------------------------------------------------------------------ evaluation over private fillings
def fillings(w, max_fill, rng_seed=1):
    m = len(w.priv)
    if 5 ** m <= max_fill:
        F = np.array(list(itertools.product(range(5, 10), repeat=m)), dtype=np.int8).reshape(-1, m)
        return F, True
    r = np.random.default_rng(rng_seed)
    return r.integers(5, 10, size=(max_fill, m), dtype=np.int8), False

def alt_mask(w, F, alt):
    msk = np.ones(len(F), dtype=bool)
    for v, (lo, hi) in alt.c.items():
        col = F[:, w.priv.index(v)]; msk &= (col >= lo) & (col <= hi)
    return msk

def eval_instance(w, F, alts):
    sure = np.zeros(len(F), dtype=bool); poss = np.zeros(len(F), dtype=bool)
    for al in alts:
        m = alt_mask(w, F, al); poss |= m
        if not al.open: sure |= m
    return sure, poss

def u_ledger(w, F, inst):
    """inst: [(label, src, dst, amount, alts)] -> lo, hi charge arrays at u and per-instance masks."""
    u = ('u',); base = 10 * (6 - w.d)
    lo = np.full(len(F), base, dtype=np.int32); hi = lo.copy(); rows = []
    for lab, a, b, amt, alts in inst:
        if u not in (a, b): continue
        sure, poss = eval_instance(w, F, alts)
        if b == u: lo += amt * sure; hi += amt * poss
        else: lo -= amt * poss; hi -= amt * sure
        rows.append((lab, a, b, amt, alts, sure.mean(), poss.mean()))
    return lo, hi, rows

def merge_alts(alts):
    """merge alternatives that differ only in one private's range when the ranges are adjacent (display only)."""
    al = [(dict(a.c), a.open) for a in alts]
    changed = True
    while changed:
        changed = False
        for i in range(len(al)):
            for j in range(i + 1, len(al)):
                (c1, o1), (c2, o2) = al[i], al[j]
                if o1 != o2 or set(c1) != set(c2): continue
                diff = [v for v in c1 if c1[v] != c2[v]]
                if len(diff) != 1: continue
                v = diff[0]; (a1, b1), (a2, b2) = sorted([c1[v], c2[v]])
                if a2 > b1 + 1: continue
                c = dict(c1); c[v] = (a1, max(b1, b2))
                if c[v] == FULL: del c[v]
                al[i] = (c, o1); del al[j]; changed = True; break
            if changed: break
    out = []
    for c, o in al:
        a = Alt(); a.c = c; a.open = o; out.append(a)
    return out

def alts_text(w, alts):
    alts = merge_alts(alts)
    sure = [al for al in alts if not al.open]; op = [al for al in alts if al.open]
    if any(not al.c for al in sure): return 'always'
    t = ' | '.join(sorted({al.text(w) for al in sure}))
    if op and not sure: t = 'needs ' + ' | '.join(sorted({al.text(w) for al in op}))
    elif op: t += '  (+ ring-3 variants)'
    return t

# ------------------------------------------------------------------ report
def run_row(d, link, sword, sets, max_fill, wt=None):
    w = Window(d, link, sword)
    F, exact = fillings(w, max_fill)
    six = np.all(F >= 6, axis=1) if F.shape[1] else np.ones(len(F), dtype=bool)
    out = []
    key = '%d %s %s' % (d, ''.join(map(str, link)), ''.join(map(str, sword)))
    out.append('## %s%s' % (key, '' if wt is None else '   (cert weight %s)' % wt))
    out.append('')
    out.append('Privates: %s (%d; %s fillings over 5..9)' % (' '.join(w.name(p) for p in w.priv) or '-', len(w.priv),
               '%d exact' % len(F) if exact else '%d sampled' % len(F)))
    out.append('Base charge of u: 10(6-%d) = %d.' % (d, 10 * (6 - d)))
    summary = {}
    pairs_u = [(('u',), x) for x in w.rot(('u',))[1]] + [(x, ('u',)) for x in w.rot(('u',))[1]]
    for st in sets:
        if st == 'rsst':
            rules = load_rsst.cache if hasattr(load_rsst, 'cache') else load_rsst(); load_rsst.cache = rules
            raw = rsst_instances(w, rules, [('u',)] + [('w', i) for i in range(d)])
            agg = collections.defaultdict(list)
            for nm, h, tg, al in raw: agg[(nm, h, tg)].append(al)
            inst = [(nm, h, tg, 1, als) for (nm, h, tg), als in agg.items()]
            title = 'RSST (Gonthier drules; m = mirror)'
        else:
            rules = load_nl26.cache if hasattr(load_nl26, 'cache') else load_nl26(); load_nl26.cache = rules
            inst = nl_instances(w, rules, pairs_u)
            title = 'NL26 (Inoue et al. 2026 rule files)'
        lo, hi, rows = u_ledger(w, F, inst)
        out.append('')
        out.append('### %s' % title)
        out.append('')
        out.append('| dir | partner | units | rule | fires when | share of fillings (sure / possible) |')
        out.append('|---|---|---|---|---|---|')
        u = ('u',)
        def sk(r):
            lab, a, b, amt, alts, fs, fp = r
            return (0 if b == u else 1, str(a if b == u else b), lab)
        for lab, a, b, amt, alts, fs, fp in sorted(rows, key=sk):
            if fp == 0: continue
            dirn = 'in' if b == u else 'out'
            other = a if b == u else b
            out.append('| %s | %s (%s) | %d | %s | %s | %.3f / %.3f |' % (
                dirn, w.name(other), w.deg.get(other, '?'), amt, lab, alts_text(w, alts), fs, fp))
        def stats(msk):
            if not msk.any(): return 'n/a'
            l, h = lo[msk], hi[msk]
            return ('charge certain %d..%d, possible %d..%d; certain > 0 in %.1f%%, possibly > 0 in %.1f%%'
                    % (l.min(), l.max(), h.min(), h.max(), 100 * (l > 0).mean(), 100 * (h > 0).mean()))
        out.append('')
        out.append('- u net charge, all fillings: %s' % stats(np.ones(len(F), dtype=bool)))
        out.append('- u net charge, all privates >= 6: %s' % stats(six))
        # the regime explore's survivors live in: every private >= 6
        u = ('u',); outs, ins = collections.defaultdict(list), collections.defaultdict(int)
        for lab, a, b, amt, alts in inst:
            if u not in (a, b): continue
            sure, poss = eval_instance(w, F, alts)
            if not six.any() or not sure[six].all(): continue
            if a == u: outs[b].append('%s%s' % (lab, '' if amt == 1 else ' x%d' % amt)); continue
            ins[w.deg.get(a)] += amt
        o6 = '; '.join('%s(%s) %d [%s]' % (w.name(b), w.deg.get(b), len(v), ', '.join(v)) for b, v in sorted(outs.items(), key=lambda t: str(t[0])))
        i6 = ', '.join('from %ss %d' % (k, v) for k, v in sorted(ins.items()))
        out.append('- at privates >= 6, rules that fire in every filling: OUT %s; IN %s' % (o6 or 'none', i6 or 'none'))
        hist = collections.Counter(zip(lo.tolist(), hi.tolist()))
        out.append('- (certain, possible) histogram: %s' % ', '.join('%s:%d' % (('%d' % k[0]) if k[0] == k[1] else '[%d,%d]' % k, v)
                                                               for k, v in sorted(hist.items())))
        summary[st] = (lo, hi, rows, (int(lo[six].min()), int(hi[six].max())) if six.any() else None, o6)
    out.append('')
    return '\n'.join(out), w, summary

def read_rows(path):
    rows = []
    for l in open(path):
        l = l.split('#')[0].strip()
        if not l: continue
        f = l.split()
        tag = ''
        try:
            if re.fullmatch(r'-?[0-9.]+(/[0-9]+)?', f[0]) and len(f) >= 4 and f[2].isdigit() and len(f[2]) == int(f[1]):
                wt, d, lk, sw, tag = f[0], int(f[1]), f[2], f[3], ' '.join(f[4:])
            else:
                wt, d, lk, sw, tag = None, int(f[0]), f[1], f[2], ' '.join(f[3:])
        except (ValueError, IndexError):
            continue
        if len(lk) != d or len(sw) != d: continue
        rows.append((wt, d, [int(c) for c in lk], [int(c) for c in sw], tag))
    return rows

def self_test():
    """Long Table's BORROWED-CHANNEL-7FACE.md ledger on 7665566/6675676 (rsst): in 12, out 2 when p0.*, p1, p2 != 5;
    u at 0 in exactly 6,400 of 15,625 fillings, +1..+4 otherwise."""
    rep, w, s = run_row(7, [7, 6, 6, 5, 5, 6, 6], [6, 6, 7, 5, 6, 7, 6], ['rsst'], 10 ** 6)
    lo, hi, rows = s['rsst'][:3]
    assert (lo == hi).all(), 'expected exact ledger'
    zero = int((lo == 0).sum()); assert zero == 6400, zero
    assert lo.min() == 0 and lo.max() == 4, (lo.min(), lo.max())
    rep, w, s = run_row(7, [7, 6, 6, 5, 5, 6, 6], [6, 6, 7, 5, 6, 6, 6], ['rsst'], 10 ** 6)
    lo, hi = s['rsst'][0], s['rsst'][1]
    h = dict(collections.Counter(lo.tolist())); assert (lo == hi).all()
    want = {0: 3072, 1: 5888, 2: 4480, 3: 1760, 4: 380, 5: 43, 6: 2}
    assert h == want, h
    print('self-test OK: 7665566/6675676 RSST ledger reproduces BORROWED-CHANNEL-7FACE (0 in 6,400/15,625; max +4)')
    print('self-test OK: 7665566/6675666 RSST histogram reproduces Studio rsst_lt7.txt %s' % want)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('rows', nargs='?')
    ap.add_argument('--out')
    ap.add_argument('--sets', default='rsst,nl26')
    ap.add_argument('--max-fill', type=int, default=400000)
    ap.add_argument('--self-test', action='store_true')
    A = ap.parse_args()
    if A.self_test: self_test(); sys.exit(0)
    sets = A.sets.split(',')
    parts = ['# Published rules on binder rows (pubrules.py; diagnostic map, not a claim)', '',
             'Source rows: `%s`. Sets: %s. Units: 10(6-d) scale (1 unit = 0.1 in ours).' % (A.rows, ', '.join(sets)), '']
    top = ['| row | tag | ' + ' | '.join('%s: u net at privates >= 6 | %s: always-out at privates >= 6' % (x, x) for x in sets) + ' |',
           '|---|---|' + '---|---|' * len(sets)]
    body = []
    for wt, d, lk, sw, tag in read_rows(A.rows):
        rep, _, sm = run_row(d, lk, sw, sets, A.max_fill, wt)
        body.append(rep); print(rep, flush=True)
        cells = []
        for x in sets:
            r6, o6 = sm[x][3], sm[x][4]
            cells += ['n/a' if r6 is None else ('%d' % r6[0] if r6[0] == r6[1] else '%d..%d' % r6), o6 or 'none']
        top.append('| %d %s %s | %s | %s |' % (d, ''.join(map(str, lk)), ''.join(map(str, sw)), tag, ' | '.join(cells)))
    parts += ['## Summary', ''] + top + [''] + body
    if A.out: open(A.out, 'w').write('\n'.join(parts) + '\n')
