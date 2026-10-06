#!/usr/bin/env python3
"""Generate a Lean D-reducibility certificate (single-block Kempe flips) for a configuration.

Input: ring size r, interior rotation lists (RSST free-completion format), a ring-position map.
Output: a Lean module with one lemma per canonical ring colouring class and a dispatch theorem.
"""
import itertools, sys

PAIRS = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]


def canon_map(k):
    m = {}
    for x in k:
        if x not in m:
            m[x] = len(m)
    return m


def canon(k):
    m = canon_map(k)
    return tuple(m[x] for x in k)


def proper_ring(r):
    for k in itertools.product(range(4), repeat=r):
        if k[0] == 0 and all(k[i] != k[(i + 1) % r] for i in range(r)):
            yield k


def noncrossing_partitions(pos):
    pos = list(pos)
    if not pos:
        yield []
        return
    first, rest = pos[0], pos[1:]
    for mask in range(1 << len(rest)):
        S = [rest[i] for i in range(len(rest)) if mask >> i & 1]
        block = [first] + S
        bset = set(block)
        gaps, cur = [], []
        for x in rest:
            if x in bset:
                gaps.append(cur)
                cur = []
            else:
                cur.append(x)
        gaps.append(cur)

        def rec(i):
            if i == len(gaps):
                yield []
                return
            for p in noncrossing_partitions(gaps[i]):
                for q in rec(i + 1):
                    yield p + q
        for q in rec(0):
            yield [block] + q


def crossing(b1, b2):
    s1, s2 = set(b1), set(b2)
    allp = sorted(s1 | s2)
    lab = [1 if x in s1 else 2 for x in allp]
    for a, b, c, d in itertools.combinations(range(len(allp)), 4):
        if lab[a] == lab[c] != lab[b] == lab[d]:
            return True
    return False


def respects(P, k, cols, r):
    blk = {}
    for bi, b in enumerate(P):
        for x in b:
            blk[x] = bi
    for i in range(r):
        j = (i + 1) % r
        if k[i] in cols and k[j] in cols and blk[i] != blk[j]:
            return False
    return True


def structures(k, pi, r):
    A, B = pi
    t1 = [i for i in range(r) if k[i] in A]
    t2 = [i for i in range(r) if k[i] in B]
    out = []
    for P1 in noncrossing_partitions(t1):
        if not respects(P1, k, A, r):
            continue
        for P2 in noncrossing_partitions(t2):
            if not respects(P2, k, B, r):
                continue
            if any(crossing(x, y) for x in P1 for y in P2):
                continue
            out.append((P1, P2))
    return out


def single_flip(k, blk, cols):
    a, b = cols
    kk = list(k)
    for x in blk:
        kk[x] = b if kk[x] == a else a
    return tuple(kk)


class Config:
    def __init__(self, name, r, rot, ringpos):
        """rot: dict interior label -> list of neighbours (RSST labels; ring labels 1..r);
        ringpos: function RSST ring label -> Lean ring position."""
        self.name, self.r = name, r
        labels = sorted(rot)
        self.idx = {v: i for i, v in enumerate(labels)}
        self.m = len(labels)
        self.ringAdj = [sorted(ringpos(u) for u in rot[v] if u <= r) for v in labels]
        self.intAdj = [sorted(self.idx[u] for u in rot[v] if u > r) for v in labels]

    def extension(self, k):
        for lam in itertools.product(range(4), repeat=self.m):
            if all(lam[a] != k[t] for a in range(self.m) for t in self.ringAdj[a]) and \
               all(lam[a] != lam[b] for a in range(self.m) for b in self.intAdj[a]):
                return lam
        return None


def build_certificate(cfg):
    r = cfg.r
    cols = sorted(set(canon(k) for k in proper_ring(r)))
    level, ext, pi_of = {}, {}, {}
    for k in cols:
        lam = cfg.extension(k)
        if lam is not None:
            level[k] = 0
            ext[k] = lam
    L = 0
    while True:
        L += 1
        new = {}
        for k in cols:
            if k in level:
                continue
            for pi in PAIRS:
                ok = True
                for (P1, P2) in structures(k, pi, r):
                    if not any(canon(single_flip(k, b, pi[0])) in level for b in P1) and \
                       not any(canon(single_flip(k, b, pi[1])) in level for b in P2):
                        ok = False
                        break
                if ok:
                    new[k] = pi
                    break
        if not new:
            break
        for k, pi in new.items():
            level[k] = L
            pi_of[k] = pi
    assert len(level) == len(cols), "not D-reducible with single flips"
    return cols, level, ext, pi_of


def lname(k):
    return "cls_" + "".join(map(str, k))


def perm_lit(f):
    """Lean literal for the permutation x ↦ f[x] of Fin 4."""
    inv = [0] * 4
    for x in range(4):
        inv[f[x]] = x
    return "(⟨![%s], ![%s], by decide, by decide⟩ : Equiv.Perm (Fin 4))" % (
        ", ".join(map(str, f)), ", ".join(map(str, inv)))


class Gen:
    def __init__(self, cfg, cols, level, ext, pi_of):
        self.cfg, self.cols, self.level, self.ext, self.pi_of = cfg, cols, level, ext, pi_of
        self.r = cfg.r
        self.ctr = 0

    def fresh(self):
        self.ctr += 1
        return "f%d" % self.ctr

    def reach(self, pair, x, y):
        a, b = pair
        return "(pairGraph G.graph O.hole c (σ %d) (σ %d)).Reachable (ρ %d) (ρ %d)" % (a, b, x, y)

    # ---- base lemma ----
    def base_lemma(self, k):
        lam = self.ext[k]
        r = self.r
        kl = "[" + ", ".join(map(str, k)) + "]"
        hs = ", ".join("h%d" % t for t in range(r))
        return """theorem {name} (σ : Equiv.Perm (Fin 4)) (c : Fin n → Fin 4)
    (hc : ProperOff G.graph O.hole c) {hyps} : T.graph.Colorable 4 :=
  O.colorable_of_ext hc σ (fun t => ({kl} : List (Fin 4)).getD t 0)
    (by intro t ht; interval_cases t; exacts [{hs}]) ![{lam}] (by decide) (by decide) (by decide)
""".format(name=lname(k), hyps=self.hyps(k), kl=kl, hs=hs, lam=", ".join(map(str, lam)))

    def hyps(self, k):
        return " ".join("(h%d : c (ρ %d) = σ %d)" % (t, t, k[t]) for t in range(self.r))

    # ---- non-base lemma: decision tree ----
    def lemma(self, k):
        pi = self.pi_of[k]
        r = self.r
        types = {t: (0 if k[t] in pi[0] else 1) for t in range(r)}
        tl = {0: [t for t in range(r) if types[t] == 0], 1: [t for t in range(r) if types[t] == 1]}
        structs = structures(k, pi, r)
        lines = []
        # positive base facts: ring adjacency
        pos = {}  # (x,y,ty) x<y -> term : Reach (ρ x) (ρ y)
        for t in range(r):
            u = (t + 1) % r
            if types[t] == types[u]:
                ty = types[t]
                a, b = pi[ty]
                if u == t + 1:
                    term = "(O.conn_ring %d (pair_active h%d (by decide)) (pair_active h%d (by decide)))" % (t, t, u)
                    pos[(t, u, ty)] = term
                else:
                    term = "(O.conn_wrap %d rfl (pair_active h%d (by decide)) (pair_active h0 (by decide)))" % (t, t)
                    pos[(0, t, ty)] = term + ".symm"
        body = self.tree(k, pi, types, tl, structs, pos, {}, 2)
        return """theorem {name} (σ : Equiv.Perm (Fin 4)) (c : Fin n → Fin 4)
    (hc : ProperOff G.graph O.hole c) {hyps} : T.graph.Colorable 4 := by
{body}""".format(name=lname(k), hyps=self.hyps(k), body=body)

    def path(self, posfacts, ty, u, v):
        """Lean term for Reach (ρ u) (ρ v) from positive facts of type ty, or None."""
        if u == v:
            return "(Reachable.refl _)"
        adj = {}
        for (x, y, t), term in posfacts.items():
            if t != ty:
                continue
            adj.setdefault(x, []).append((y, term))
            adj.setdefault(y, []).append((x, term + ".symm"))
        prev = {u: None}
        q = [u]
        while q:
            z = q.pop(0)
            for (w, term) in adj.get(z, []):
                if w not in prev:
                    prev[w] = (z, term)
                    q.append(w)
        if v not in prev:
            return None
        chain = []
        z = v
        while prev[z] is not None:
            z0, term = prev[z]
            chain.append(term)
            z = z0
        chain.reverse()
        out = chain[0]
        for t in chain[1:]:
            out = "(%s.trans %s)" % (out, t)
        return out

    def classes(self, posfacts, tl, ty):
        cl = {}
        for x in tl[ty]:
            cl[x] = x
        changed = True
        while changed:
            changed = False
            for (x, y, t) in posfacts:
                if t != ty:
                    continue
                if cl[x] != cl[y]:
                    a, b = cl[x], cl[y]
                    for z in cl:
                        if cl[z] == b:
                            cl[z] = a
                    changed = True
        return cl

    def neg_term(self, posfacts, negfacts, ty, x, y):
        """Lean term for ¬ Reach (ρ x) (ρ y), derived from an explicit negative fact, or None."""
        for (u, v, t), term in negfacts.items():
            if t != ty:
                continue
            for (uu, vv, tm) in ((u, v, term), (v, u, "(fun h => %s h.symm)" % term)):
                p1 = self.path(posfacts, ty, uu, x)
                p2 = self.path(posfacts, ty, y, vv)
                if p1 is not None and p2 is not None:
                    return "(fun hxy => %s (%s.trans (hxy.trans %s)))" % (tm, p1, p2)
        return None

    def consistent(self, posfacts, negfacts, S):
        P1, P2 = S
        def blk(P, x):
            for i, b in enumerate(P):
                if x in b:
                    return i
        for (x, y, t) in posfacts:
            P = P1 if t == 0 else P2
            if blk(P, x) != blk(P, y):
                return False
        for (x, y, t) in negfacts:
            P = P1 if t == 0 else P2
            if blk(P, x) == blk(P, y):
                return False
        return True

    def refute(self, k, pi, types, tl, posfacts, negfacts):
        r = self.r
        # (a) explicit negative inside a positive class
        for (x, y, t), term in negfacts.items():
            p = self.path(posfacts, t, x, y)
            if p is not None:
                return "exact absurd %s %s" % (p, term)
        # (b) crossing of two chains
        for ty1 in (0, 1):
            for ty2 in (0, 1):
                for i, j, kk, l in itertools.combinations(range(r), 4):
                    if types[i] != ty1 or types[kk] != ty1 or types[j] != ty2 or types[l] != ty2:
                        continue
                    p1 = self.path(posfacts, ty1, i, kk)
                    p2 = self.path(posfacts, ty2, j, l)
                    if p1 is None or p2 is None:
                        continue
                    if ty1 != ty2:
                        A, B = pi[ty1], pi[ty2]
                        return ("exact (chains_noncrossing O.ring (pair_disj σ (a := %d) (b := %d) (a' := %d) (b' := %d) (by decide)) "
                                "(by norm_num) (by norm_num) (by norm_num) (by norm_num) %s %s).elim") % (A[0], A[1], B[0], B[1], p1, p2)
                    ne = self.neg_term(posfacts, negfacts, ty1, i, j)
                    if ne is not None:
                        return ("exact (chains_noncrossing_same O.ring (by norm_num) (by norm_num) (by norm_num) (by norm_num) "
                                "%s %s %s).elim") % (p1, p2, ne)
        return None

    def try_flip(self, k, pi, types, tl, posfacts, negfacts):
        r = self.r
        for ty in (0, 1):
            cl = self.classes(posfacts, tl, ty)
            for x in tl[ty]:
                members, nonmembers, ok = [], [], True
                for y in tl[ty]:
                    if cl[y] == cl[x]:
                        members.append(y)
                    else:
                        nt = self.neg_term(posfacts, negfacts, ty, x, y)
                        if nt is None:
                            ok = False
                            break
                        nonmembers.append((y, nt))
                if not ok:
                    continue
                k2 = single_flip(k, members, pi[ty])
                kc = canon(k2)
                if self.level[kc] >= self.level[k]:
                    continue
                return self.flip_code(k, pi, ty, x, members, nonmembers, k2, kc, posfacts)
        return None

    def flip_code(self, k, pi, ty, x, members, nonmembers, k2, kc, posfacts):
        a, b = pi[ty]
        r = self.r
        # τ with k2 t = τ (kc t): τ = inverse of canonical renaming
        m = canon_map(k2)            # k2 value -> canonical value
        inv = {v: u for u, v in m.items()}
        used = set(inv.values())
        free_src = [v for v in range(4) if v not in inv]
        free_dst = [u for u in range(4) if u not in used]
        for s, d in zip(free_src, free_dst):
            inv[s] = d
        tau = [inv[v] for v in range(4)]
        S = "{v | %s}" % ("(pairGraph G.graph O.hole c (σ %d) (σ %d)).Reachable (ρ %d) v" % (a, b, x))
        args = []
        for t in range(r):
            if t in members:
                p = self.path(posfacts, ty, x, t)
                args.append("((flip_in (S := %s) %s h%d).trans (congrArg σ (by decide)))" % (S, p, t))
            elif any(t == y for y, _ in nonmembers):
                nt = [n for y, n in nonmembers if y == t][0]
                args.append("((flip_out (a := %d) (b := %d) (S := %s) %s h%d).trans (congrArg σ (by decide)))" % (a, b, S, nt, t))
            else:
                args.append("((flip_other (a := %d) (b := %d) (S := %s) (by decide) (by decide) h%d).trans (congrArg σ (by decide)))" % (a, b, S, t))
        whole = "(whole_component G.graph O.hole c (σ %d) (σ %d) (ρ %d) ⟨O.ring_ne_hole %d, pair_active h%d (by decide)⟩)" % (a, b, x, x, x)
        newc = "(swap c (σ %d) (σ %d) %s)" % (a, b, S)
        return "exact %s O (σ * %s) %s (properOff_swap G.graph hc %s)@@NL@@%s" % (
            lname(kc), perm_lit(tau), newc, whole, "@@NL@@".join(args))

    def tree(self, k, pi, types, tl, structs, posfacts, negfacts, ind):
        sp = " " * ind
        cand = [S for S in structs if self.consistent(posfacts, negfacts, S)]
        f = self.try_flip(k, pi, types, tl, posfacts, negfacts)
        if f is not None:
            return sp + f.replace("@@NL@@", "\n" + sp + "    ") + "\n"
        if not cand:
            ref = self.refute(k, pi, types, tl, posfacts, negfacts)
            if ref is not None:
                return sp + ref + "\n"
        # branch on the first unknown pair
        for ty in (0, 1):
            for x, y in itertools.combinations(tl[ty], 2):
                if self.path(posfacts, ty, x, y) is not None:
                    continue
                if self.neg_term(posfacts, negfacts, ty, x, y) is not None:
                    continue
                h = self.fresh()
                pair = pi[ty]
                s = sp + "by_cases %s : %s\n" % (h, self.reach(pair, x, y))
                s += sp + "· " + self.tree(k, pi, types, tl, structs, {**posfacts, (x, y, ty): h}, negfacts, ind + 2).lstrip()
                s += sp + "· " + self.tree(k, pi, types, tl, structs, posfacts, {**negfacts, (x, y, ty): h}, ind + 2).lstrip()
                return s
        raise Exception("stuck at class %s" % (k,))

    # ---- dispatch ----
    def dispatch(self):
        r = self.r
        out = []

        def rec(t, assign, reps, ind):
            sp = " " * ind
            if t == r:
                if assign[r - 1] == assign[0]:
                    return sp + "exact absurd (%s) (O.ring_proper_wrap hc %d rfl)\n" % ("e%d_%d" % (r - 1, 0), r - 1)
                kk = tuple(assign)
                nrep = len(reps)
                vals = " ".join("(c (ρ %d))" % p for p in reps)
                neqs = []
                for i in range(nrep):
                    for j in range(i + 1, nrep):
                        neqs.append("ne%d_%d" % (reps[i], reps[j]))
                lem = {2: "exists_perm_two", 3: "exists_perm_three'", 4: "exists_perm_four"}[nrep]
                names = ["s%d" % i for i in range(nrep)]
                s = sp + "obtain ⟨σ, %s⟩ := %s %s %s\n" % (", ".join(names), lem, vals, " ".join(neqs))
                hs = []
                for p in range(r):
                    j = assign[p]
                    if reps[j] == p:
                        hs.append("s%d.symm" % j)
                    else:
                        hs.append("(e%d_%d.trans s%d.symm)" % (p, reps[j], j))
                s += sp + "exact %s O σ c hc %s\n" % (lname(kk), " ".join(hs))
                return s
            s = ""
            nreps = len(reps)
            # try equal to each existing colour
            parts = []
            for j in range(nreps):
                h = "e%d_%d" % (t, reps[j])
                body_eq = None
                if j == assign[t - 1]:
                    body_eq = "exact absurd (%s.trans rfl) (fun e => O.ring_proper hc %d (e.trans (by rfl)))\n" % (h, t - 1)
                parts.append((h, j))
            # nested by_cases
            def nest(i, ind2):
                sp2 = " " * ind2
                if i == len(parts):
                    # new colour
                    if nreps == 4:
                        nes = " ".join("ne%d_%d" % (reps[i], reps[j]) for i in range(4) for j in range(i + 1, 4))
                        es = " ".join("e%d_%d" % (t, reps[j]) for j in range(4))
                        return sp2 + "exact (fin4_pigeon (c (ρ %d)) %s %s %s).elim\n" % (
                            t, " ".join("(c (ρ %d))" % reps[j] for j in range(4)), nes, es)
                    neqs = []
                    for j in range(nreps):
                        neqs.append(("ne%d_%d" % (reps[j], t), "e%d_%d" % (t, reps[j])))
                    s2 = ""
                    for (nn, ee) in neqs:
                        s2 += sp2 + "have %s : c (ρ %d) ≠ c (ρ %d) := fun e => %s e.symm\n" % (nn, int(nn.split('_')[0][2:]), t, ee)
                    return s2 + rec(t + 1, assign + [nreps], reps + [t], ind2)
                h, j = parts[i]
                s2 = sp2 + "by_cases %s : c (ρ %d) = c (ρ %d)\n" % (h, t, reps[j])
                if j == assign[t - 1]:
                    inner = "exact absurd (%s.trans %s).symm (O.ring_proper hc %d)\n" % (h, self.rep_eq(assign, reps, t - 1), t - 1)
                    s2 += sp2 + "· " + inner
                else:
                    s2 += sp2 + "· " + rec(t + 1, assign + [j], reps, ind2 + 2).lstrip()
                s2 += sp2 + "· " + nest(i + 1, ind2 + 2).lstrip()
                return s2
            return nest(0, ind)
        body = rec(1, [0], [0], 2)
        return """/-- **Dispatch.** Every proper colouring of the deleted map leads to a colouring of `T`. -/
theorem colorable (c : Fin n → Fin 4) (hc : ProperOff G.graph O.hole c) : T.graph.Colorable 4 := by
{body}""".format(body=body)

    def rep_eq(self, assign, reps, p):
        """term: c (ρ reps[assign[p]]) = c (ρ p)  i.e. from representative to p."""
        j = assign[p]
        if reps[j] == p:
            return "rfl"
        return "(e%d_%d).symm" % (p, reps[j])


def generate(cfg, module_name, namespace):
    cols, level, ext, pi_of = build_certificate(cfg)
    g = Gen(cfg, cols, level, ext, pi_of)
    r, m = cfg.r, cfg.m
    ring_lists = ", ".join("[%s]" % ", ".join(map(str, l)) for l in cfg.ringAdj)
    int_lists = ", ".join("[%s]" % ", ".join(map(str, l)) for l in cfg.intAdj)
    out = []
    out.append("""module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RingReduce

/-!
# D-reducibility certificate: {name} (generated)

Generated by `gen_cert.py` from the free-completion rotation lists. Ring size {r}, {m} interior
vertices, {nc} ring colouring classes up to renaming ({nb} extend directly), closure depth {d}.
Every step is a single whole-component Kempe swap of the map with the interior deleted; every
case split is on whether two ring vertices lie in one Kempe chain; impossible cases are refuted by
transitivity, ring adjacency, or the face Jordan lemma (`chains_noncrossing`,
`chains_noncrossing_same`).
-/

@[expose] public section
namespace SimpleGraph.SphericalMap.{ns}
open VacancySlide VacancyShortFill SimpleGraph.SphericalMap

/-- Ring neighbours of each interior vertex (ring positions). -/
def ringList : Fin {m} → List ℕ := ![{rl}]
/-- Interior neighbours of each interior vertex. -/
def intList : Fin {m} → List (Fin {m}) := ![{il}]
def ringAdj : Fin {m} → ℕ → Bool := fun a t => decide (t ∈ ringList a)
def intAdj : Fin {m} → Fin {m} → Bool := fun a b => decide (b ∈ intList a)

variable {{n : ℕ}} {{T G : SphericalMap n}} {{ρ : ℕ → Fin n}} {{ι : Fin {m} → Fin n}}
  (O : ConfigOcc T G {r} {m} ρ ι intAdj ringAdj)
include O
""".format(name=cfg.name, r=r, m=m, nc=len(cols), nb=sum(1 for k in cols if level[k] == 0),
           d=max(level.values()), ns=namespace, rl=ring_lists, il=int_lists))
    order = sorted(cols, key=lambda k: (level[k], k))
    for k in order:
        if level[k] == 0:
            out.append(g.base_lemma(k))
        else:
            out.append(g.lemma(k))
    out.append(g.dispatch())
    out.append("end SimpleGraph.SphericalMap.%s\n" % namespace)
    return "\n".join(out)


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "diamond":
        rot = {7: [2, 8, 9, 10, 1], 8: [2, 3, 4, 9, 7], 9: [8, 4, 5, 10, 7], 10: [9, 5, 6, 1, 7]}
        r = 6
    else:
        rot = {8: [2, 3, 9, 10, 11, 1], 9: [3, 4, 5, 10, 8], 10: [9, 5, 6, 11, 8], 11: [10, 6, 7, 1, 8]}
        r = 7
    rev = len(sys.argv) > 3 and sys.argv[3] == "rev"
    ringpos = (lambda u: (r - (u - 1)) % r) if rev else (lambda u: u - 1)
    cfg = Config(which, r, rot, ringpos)
    print(generate(cfg, None, sys.argv[2]))
