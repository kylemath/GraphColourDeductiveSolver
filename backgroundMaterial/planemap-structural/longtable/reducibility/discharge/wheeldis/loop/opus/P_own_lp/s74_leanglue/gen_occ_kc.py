#!/usr/bin/env python3
"""gen_occ_kc.py (Team C, s74_leanglue, 5 Nov 2026): kc line -> Lean occurrence modules (Occ, configOcc, COccBridge glue).

A kc line is `name r m ringadj intadj` (the kc / dfast / cfast input line; gen_hd.py's and gen_ccover3.py's EXTRAFILE line
`name<TAB>r m ringadj intadj[<TAB>X]` is accepted too). From it this script derives the free-completion rotation (the
rotation of the configuration's own near-triangulation, ring cycle added, at every interior vertex), validates it, and writes

  <NS>.lean      `Occ T ring int` (rotation occurrence), `configOcc` (Occ -> ConfigOccW, or ConfigOcc with --form ring),
                 `cf : DCheck18.Conf` (the same Conf literal as gen_hd.py / gen_ccover3.py write for this kc line),
                 `intAdjOf_eq`, `ringAdjOf_eq`, `cf_sym`, `cf_loop`, `colorable_of_occ_dred`, `colorable_of_mirror_occ_dred`.
                 This is occ24/gen_occ_key.py (--form ring) or occ24/gen_occ_walk.py (--form walk, the default: ring
                 vertices may repeat, dart injectivity derived), called unchanged.
  COcc<NS>.lean  occ24/gen_rotbridge.py's bridge (rot, rot_ok, rotOcc_of_occ, local_facts_of_occ), then the registry glue
                 (new, see `registry_text`): occursW_of_occ (ClaimGlue.OccursW), dEntryOf (ClaimGlue.DEntry from gen_hd's
                 hD), colorable_of_occ_entry (+ mirror), occursCXR_of_occ / occursCXF_of_occ (CGlue C occurrences of any
                 CEntry on this cf), colorable_of_occ_centry (+ mirror).

The rotation: occ24's `gen_occ_key.rotation` already reads the rotation off a kc line (link cycles of the free completion).
This script keeps it as the first choice (so every occ24 module is reproduced byte for byte), checks its output with an
independent validator (`validate_rotation`: a coherently oriented disc triangulation whose boundary is the ring cycle, Euler
characteristic 1), cross-checks it against an independent derivation (`derive_rotation`, Hamiltonian link cycles with
face-consistency backtracking, which also handles links with chords), and falls back to the derivation when the old routine
raises. Every Bool side goal the Lean files close by decide / native_decide (rotOK, cf_sym, cf_loop, 2 <= r <= 19) is
evaluated in Python first (`precheck`), so a key that would fail them is refused here, not on the Studio.

Usage
  gen_occ_kc.py one SRC NS OUTDIR [--form walk|ring] [--walk-assume] [--no-bridge] [--no-registry]
        SRC = FILE:N (N-th non-blank line, 0-based), FILE@NAME (first line with that name) or a literal kc line.
  gen_occ_kc.py KEYFILE LINENO NS OUTDIR            (gen_occ_key.py's own argument order; --form ring implied)
  gen_occ_kc.py batch EXTRAFILE OUTDIR PREFIX [--form ..] [--hd MOD PFX] [--first N] [--count K]
        one module pair per non-blank line i, NS = PREFIX + %02d/%03d index; with --hd MOD PFX also MODOcc.lean, which
        ties gen_hd.py's `MODV.hD_i` (EXTRAFILE run through gen_hd.py with the same MOD, PFX) to each occurrence.
  gen_occ_kc.py check FILE...                      validate the rotation of every kc line, write nothing.
The occ24 generators are imported from $OCC24, else from the repository's reducibility/dcheck/occ24, else from ./vendor
(byte copies of origin/main, md5 in vendor/SOURCES.txt)."""
import sys, os, re, argparse, itertools, collections

HERE = os.path.dirname(os.path.abspath(__file__))


def _occ24_dir():
    cands = [os.environ.get('OCC24', ''),
             os.path.normpath(os.path.join(HERE, *(['..'] * 6), 'dcheck', 'occ24')),
             os.path.join(HERE, 'vendor')]
    for c in cands:
        if c and os.path.exists(os.path.join(c, 'gen_occ_key.py')) and os.path.exists(os.path.join(c, 'gen_occ_walk.py')):
            return c
    raise SystemExit('gen_occ_kc: occ24 generators not found (set OCC24)')


OCC24 = _occ24_dir()
sys.path.insert(0, OCC24)
import gen_occ_key as G      # noqa: E402
import gen_occ_walk as GW    # noqa: E402  (imports the same gen_occ_key module object)

_orig_rotation = G.rotation
STATS = collections.Counter()


class KcError(Exception):
    pass


# --------------------------------------------------------------------------------------------------------- kc lines
def parse_kc(line):
    """kc line or EXTRAFILE line -> (name, r, m, ra, ia, canonical kc line `name r m ringadj intadj`)."""
    line = line.rstrip('\n')
    if '\t' in line:
        f = line.split('\t')
        name, rest = f[0], f[1].split()
    else:
        f = line.split()
        name, rest = f[0], f[1:]
    if len(rest) < 4:
        raise KcError('not a kc line: %r' % line[:80])
    if not re.fullmatch(r'[^\s"\\]+', name):
        raise KcError('name %r has whitespace, a quote or a backslash (not a Lean string literal)' % name)
    canon = '%s %s %s %s %s' % (name, rest[0], rest[1], rest[2], rest[3])
    n2, r, m, ra, ia = G.parse(canon)
    return n2, r, m, ra, ia, canon


def read_src(src):
    """FILE:N, FILE@NAME, or a literal kc line."""
    m = re.fullmatch(r'(.+):(\d+)', src)
    if m and os.path.isfile(m.group(1)):
        lines = [l for l in open(m.group(1)) if l.strip()]
        return lines[int(m.group(2))]
    m = re.fullmatch(r'(.+)@(.+)', src)
    if m and os.path.isfile(m.group(1)):
        for l in open(m.group(1)):
            if l.strip() and re.split(r'[\t ]', l, 1)[0] == m.group(2):
                return l
        raise KcError('%s: no line named %s' % (m.group(1), m.group(2)))
    return src


def check_conf(r, m, ra, ia):
    """Structural facts of the kc line itself (the Lean side facts are rechecked in `precheck`)."""
    err = []
    if len(ra) != m or len(ia) != m:
        err.append('ringadj/intadj have %d/%d lists, m = %d' % (len(ra), len(ia), m))
        return err
    for a in range(m):
        if len(set(ia[a])) != len(ia[a]) or len(set(ra[a])) != len(ra[a]):
            err.append('repeated neighbour at I%d' % a)
        for b in ia[a]:
            if not 0 <= b < m: err.append('I%d: interior neighbour %d out of range' % (a, b))
            elif b == a: err.append('I%d: loop' % a)
            elif a not in ia[b]: err.append('I%d-I%d not symmetric' % (a, b))
        for t in ra[a]:
            if not 0 <= t < r: err.append('I%d: ring position %d out of range' % (a, t))
    cov = set(t for a in range(m) for t in ra[a])
    miss = sorted(set(range(r)) - cov)
    if miss:
        err.append('ring positions with no interior neighbour (the ring fan would need a chord): %s' % miss)
    seen = {0}; st = [0]
    while st:
        a = st.pop()
        for b in ia[a]:
            if 0 <= b < m and b not in seen: seen.add(b); st.append(b)
    if len(seen) != m:
        err.append('interior not connected')
    return err


# ------------------------------------------------------------------------------------------ free-completion rotation
def fc_graph(r, m, ra, ia):
    """Free completion in RSST labels (ring t -> t+1, interior a -> r+1+a): the configuration plus the ring cycle."""
    L = lambda a: r + 1 + a
    nb = {v: set() for v in range(1, r + m + 1)}
    for a in range(m):
        for b in ia[a]: nb[L(a)].add(L(b)); nb[L(b)].add(L(a))
        for t in ra[a]: nb[L(a)].add(t + 1); nb[t + 1].add(L(a))
    for t in range(r):
        u, w = t + 1, (t + 1) % r + 1
        nb[u].add(w); nb[w].add(u)
    return nb


def _ham_cycles(N, adj, cap=64):
    """Hamiltonian cycles of the link graph on N (each once: fixed start min(N), second < last)."""
    N = sorted(N); s = N[0]; out = []
    if len(N) < 3: return out
    def rec(path, used):
        if len(out) >= cap: return
        if len(path) == len(N):
            if s in adj[path[-1]] and path[1] < path[-1]: out.append(tuple(path))
            return
        for w in sorted(adj[path[-1]]):
            if w not in used:
                used.add(w); path.append(w); rec(path, used); path.pop(); used.discard(w)
    rec([s], {s})
    return out


def _faces_of(cyc, v):
    return [frozenset((v, cyc[i], cyc[(i + 1) % len(cyc)])) for i in range(len(cyc))]


def derive_rotation(r, m, ra, ia):
    """Independent derivation: one Hamiltonian cycle of each interior link, chosen so that the triangles agree (every
    interior edge in two faces, every ring edge in one), then a coherent orientation with the ring read forwards
    (ring t immediately before ring t+1 at the apex of ring edge (t, t+1), the orientation occ24's gen_occ accepts).
    Each list starts at its smallest label. Raises KcError when no such rotation exists or when it is not unique."""
    nb = fc_graph(r, m, ra, ia)
    I = [r + 1 + a for a in range(m)]
    cand = {}
    for v in I:
        N = nb[v]
        adj = {u: nb[u] & N for u in N}
        cs = _ham_cycles(N, adj)
        if not cs: raise KcError('link of RSST %d has no Hamiltonian cycle' % v)
        cand[v] = cs
    STATS['links_not_induced_cycle'] += sum(1 for v in I
                                            if any(len(nb[u] & nb[v]) != 2 for u in nb[v]))
    STATS['links_several_ham_cycles'] += sum(1 for v in I if len(cand[v]) > 1)
    order = sorted(I, key=lambda v: len(cand[v]))
    ringE = {frozenset((t + 1, (t + 1) % r + 1)) for t in range(r)}
    sols = []

    def consistent(chosen):
        faces = set()
        for v, c in chosen.items(): faces |= set(_faces_of(c, v))
        # a face seen from one interior vertex must be seen from every interior vertex on it that is chosen
        for f in faces:
            for w in f:
                if w in chosen and f not in set(_faces_of(chosen[w], w)): return False
        if len(chosen) < len(I): return True
        inner = collections.Counter()
        for f in faces:
            for e in itertools.combinations(sorted(f), 2): inner[frozenset(e)] += 1
        E = {frozenset((u, w)) for u in nb for w in nb[u]}
        for e in E:
            want = 1 if e in ringE else 2
            if inner[e] != want: return False
        return (r + m) - len(E) + len(faces) == 1

    def rec(i, chosen):
        if len(sols) > 1: return
        if i == len(order):
            if consistent(chosen): sols.append(dict(chosen))
            return
        v = order[i]
        for c in cand[v]:
            chosen[v] = c
            if consistent(chosen): rec(i + 1, chosen)
            del chosen[v]
    rec(0, {})
    if not sols: raise KcError('no face-consistent choice of link cycles (not a disc near-triangulation)')
    if len(sols) > 1: raise KcError('free-completion rotation not unique')
    rot = {v: list(c) for v, c in sols[0].items()}
    # coherent orientation, BFS from interior 0
    done = {I[0]}; q = [I[0]]
    while q:
        v = q.pop(); c = rot[v]
        for i, b in enumerate(c):
            if b not in rot or b in done: continue
            a = c[i - 1]; cb = rot[b]; j = cb.index(v)
            if cb[(j + 1) % len(cb)] != a: rot[b] = [cb[0]] + cb[1:][::-1]
            done.add(b); q.append(b)
    if len(done) != m: raise KcError('interior not connected')
    # ring forwards at the apex of ring edge (0, 1)
    if _ring_sign(r, rot) < 0:
        rot = {v: [c[0]] + c[1:][::-1] for v, c in rot.items()}
    return rot


def _ring_sign(r, rot):
    """+1 if at every ring-edge apex ring t comes immediately before ring t+1 (list order), -1 if always after, else 0."""
    sg = set()
    for t in range(r):
        u, w = t + 1, (t + 1) % r + 1
        for v, c in rot.items():
            d = len(c)
            for i in range(d):
                if c[i] == u and c[(i + 1) % d] == w: sg.add(1)
                if c[i] == w and c[(i + 1) % d] == u: sg.add(-1)
    return sg.pop() if len(sg) == 1 else 0


def validate_rotation(r, m, ra, ia, rot):
    """Independent check of a rotation dict {interior RSST label: neighbour list}. Returns (sign, problems)."""
    nb = fc_graph(r, m, ra, ia)
    I = [r + 1 + a for a in range(m)]
    P = []
    if sorted(rot) != I: return 0, ['rotation keys are not the interior labels']
    faces = set()
    for v in I:
        c = rot[v]; d = len(c)
        if len(set(c)) != d or set(c) != nb[v]: P.append('RSST %d: list is not its neighbour set' % v); continue
        for i in range(d):
            if c[(i + 1) % d] not in nb[c[i]]: P.append('RSST %d: %d,%d consecutive but not adjacent' % (v, c[i], c[(i + 1) % d]))
            b = c[i]
            if b in rot:   # coherence: (a, b) consecutive at v  =>  (v, a) consecutive at b
                a = c[i - 1]; cb = rot[b]
                if v in cb and cb[(cb.index(v) + 1) % len(cb)] != a: P.append('orientation clash at %d-%d' % (v, b))
        faces |= set(_faces_of(c, v))
    if P: return 0, P
    for f in faces:
        for w in f:
            if w in rot and f not in set(_faces_of(rot[w], w)): P.append('face %s not seen from %d' % (sorted(f), w))
    E = {frozenset((u, w)) for u in nb for w in nb[u]}
    ringE = {frozenset((t + 1, (t + 1) % r + 1)) for t in range(r)}
    inner = collections.Counter()
    for f in faces:
        for e in itertools.combinations(sorted(f), 2): inner[frozenset(e)] += 1
    for e in E:
        want = 1 if e in ringE else 2
        if inner[e] != want: P.append('edge %s in %d faces (want %d)' % (sorted(e), inner[e], want))
    if (r + m) - len(E) + len(faces) != 1: P.append('Euler characteristic %d' % ((r + m) - len(E) + len(faces)))
    s = _ring_sign(r, rot)
    if s == 0: P.append('ring orientation not uniform')
    return s, P


def _cyc_eq(c1, c2):
    if len(c1) != len(c2) or set(c1) != set(c2): return False
    j = c2.index(c1[0]); d = len(c1)
    return all(c1[i] == c2[(j + i) % d] for i in range(d))


def same_rotation(rot1, rot2):
    """Equal as cyclic orders, up to one global reversal."""
    if sorted(rot1) != sorted(rot2): return False
    fw = all(_cyc_eq(rot1[v], rot2[v]) for v in rot1)
    bw = all(_cyc_eq(rot1[v], rot2[v][::-1]) for v in rot1)
    return fw or bw


def rotation_kc(r, m, ra, ia):
    """Drop-in for gen_occ_key.rotation: the old routine's result when it is valid (byte-identical output), else the
    independent derivation. Both are validated, and when both exist they must agree."""
    try:
        old = _orig_rotation(r, m, ra, ia)
    except (ValueError, IndexError, KeyError, AssertionError) as e:
        old = None; STATS['old_rotation_raised'] += 1
    new = None
    try:
        new = derive_rotation(r, m, ra, ia)
    except KcError as e:
        newerr = str(e); STATS['derive_failed'] += 1
    if old is not None:
        s, P = validate_rotation(r, m, ra, ia, old)
        if not P:
            if new is not None and not same_rotation(old, new):
                raise KcError('gen_occ_key.rotation and derive_rotation disagree')
            STATS['rotation_old_validated'] += 1
            return old
        STATS['old_rotation_invalid'] += 1
    if new is None:
        raise KcError('no free-completion rotation: ' + newerr)
    s, P = validate_rotation(r, m, ra, ia, new)
    if P: raise KcError('derived rotation fails validation: %s' % P[:3])
    STATS['rotation_derived'] += 1
    return new


G.rotation = rotation_kc    # gen_key and gen_occ_walk.dinj_proof look the rotation up through this module attribute


# ------------------------------------------------------------------------------------------------------- the modules
def occ_text(line, ns, form='walk', walk_assume=False):
    """<NS>.lean: occ24's generators, unchanged (gen_occ_key.gen_key; gen_occ_walk.walk with dinj_proof)."""
    if form == 'ring':
        return G.gen_key(line, ns)
    r = int(line.split()[1])
    derive = None if walk_assume else GW.dinj_proof(line, ns)
    return GW.walk(G.gen_key(line, ns), r, derive)


def bridge_rot(occ):
    """The rotation as the bridge reads it off Occ's Nx fields (gen_rotbridge.py): {a: [('inl'|'inr', i), ...]}."""
    facts = {}
    for a, k, x, y in re.findall(r'  r(\d+)_(\d+) : Nx T \(int \d+\) (\((?:int|ring) \d+\)) (\((?:int|ring) \d+\))', occ):
        facts.setdefault(int(a), {})[int(k)] = (x, y)
    def slot(v):
        kind, i = v.strip('()').split()
        return ('inl' if kind == 'int' else 'inr', int(i))
    rot = {}
    for a in sorted(facts):
        F = facts[a]; d = len(F)
        Lr = [slot(F[k][1]) for k in range(d)]
        for k in range(d): assert slot(F[k][0]) == Lr[(k + 1) % d], (a, k)
        rot[a] = Lr
    return rot


def bridge_text(occ, ns, mod):
    """occ24/gen_rotbridge.py as a function (same output text as `python3 gen_rotbridge.py SRC NS MOD`)."""
    t = occ
    m = int(re.search(r'structure Occ \(T : SphericalMap n\) \(ring : Fin (\d+) → Fin n\) \(int : Fin (\d+) → Fin n\)', t).group(2))
    rr = int(re.search(r'ring : Fin (\d+)', t).group(1))
    R = bridge_rot(t)
    rot = {a: ['.inl %d' % i if k == 'inl' else '.inr %d' % i for k, i in R[a]] for a in R}
    out = []
    out.append('import COccBridge\nimport %s\n' % mod)
    out.append('/-! Bridge test (Long Table, 19 Oct 2026): the occ24 key `%s`\'s rotation occurrence `Occ` gives\n`RotOcc` with the rotation read off its own `Nx` fields, hence `OccExact`, `NbrInj` and `ApexFacts`.\nOnly `int_inj`, `disj`, `deg` and the `Nx` fields of `Occ` are used (no `ring_inj`). -/\n' % ns)
    out.append('namespace SimpleGraph.SphericalMap.%s\nopen VacancyIcosahedral DCheck DCheck.R2\n\nvariable {n : ℕ}\n' % ns)
    out.append('/-- The rotation at each interior vertex, as `Occ` states it. -/')
    out.append('def rot : Fin %d → List (Fin %d ⊕ ℕ) := ![%s]\n' % (m, m, ', '.join('[' + ', '.join(rot[a]) + ']' for a in range(m))))
    out.append('theorem rot_ok : rotOK (DCheck.Conf.of18 cf) rot = true := by\n  native_decide\n')
    out.append('theorem rotOcc_of_occ {T : SphericalMap n} {ring : Fin %d → Fin n} {int : Fin %d → Fin n}\n    (h : Occ T ring int) : RotOcc T (ρOf ring) int rot where' % (rr, m))
    out.append('  ιinj := h.int_inj\n  disj := fun t a => h.disj _ a\n  deg := fun a => by rw [h.deg a]; fin_cases a <;> rfl')
    out.append('  nx := by\n    intro a k hk\n    fin_cases a')
    for a in range(m):
        d = len(rot[a])
        out.append('    · replace hk : k < %d := hk\n      interval_cases k' % d)
        for k in range(d):
            out.append('      · exact h.r%d_%d' % (a, k))
    out.append('''
/-- **Falsification test, passed**: `Occ` gives the three local facts. -/
theorem local_facts_of_occ {T : SphericalMap n} {ring : Fin %d → Fin n} {int : Fin %d → Fin n}
    (h : Occ T ring int) :
    OccExact T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    NbrInj (DCheck.Conf.of18 cf).r (ρOf ring) (ringAdjOf (DCheck.Conf.of18 cf)) ∧
    ApexFacts T (DCheck.Conf.of18 cf).r (ρOf ring) int (intAdjOf (DCheck.Conf.of18 cf)) (ringAdjOf (DCheck.Conf.of18 cf)) :=
  ⟨(rotOcc_of_occ h).occExact rot_ok, (rotOcc_of_occ h).nbrInj rot_ok,
    (rotOcc_of_occ h).apexFacts rot_ok cf_sym⟩

end SimpleGraph.SphericalMap.%s

#print axioms SimpleGraph.SphericalMap.%s.local_facts_of_occ
''' % (rr, m, ns, ns))
    return '\n'.join(out) + '\n'


REG_NAMES = ['occursW_of_occ', 'dEntryOf', 'colorable_of_occ_entry', 'colorable_of_mirror_occ_entry',
             'occursCXR_of_occ', 'occursCXF_of_occ', 'colorable_of_occ_centry', 'colorable_of_mirror_occ_centry']


def registry_text(ns, r, m, form):
    """Registry glue (new; not yet compiled, see README): the occurrence in ClaimGlue's and CGlue's own terms.
    `c = cf` hypotheses let any registry Conf literal equal to this key's `cf` (gen_hd.py's `<PFX>Confs.get ⟨i, _⟩`,
    gen_ccover3.py's `(… .get k).cf`) be used with `rfl`."""
    W = 'O' if form == 'walk' else 'O.toW'
    IH = ('(IH : ∀ (m\' : ℕ) (N : SphericalMap m\'), Nat.card N.graph.support < Nat.card T.graph.support →\n'
          '      N.graph.Colorable 4)')
    occ = '{ring : Fin %d → Fin n}\n    {int : Fin %d → Fin n}' % (r, m)
    return f'''
/-! ## Registry glue (s74_leanglue/gen_occ_kc.py)

`Occ` in the registry's own terms: the D occurrence `ClaimGlue.OccursW` and entry `ClaimGlue.DEntry`, and the C
occurrence `CGlue.OccursCXR` / `CGlue.OccursCXF` of any C entry whose configuration is `cf`. A registry Conf literal for
this kc line (gen_hd.py's `<PFX>Confs.get ⟨i, _⟩`, gen_ccover3.py's `cf` field) is equal to `cf` by `rfl`. -/

/-- `Occ` gives the reduction-ready D occurrence of `cf`. -/
theorem occursW_of_occ {{T : SphericalMap n}} (htri : T.Triangulated) {occ}
    (h : Occ T ring int) : ClaimGlue.OccursW cf T := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  rw [← intAdjOf_eq, ← ringAdjOf_eq] at O
  exact ⟨G, ρOf ring, int, {W}, hlt⟩

/-- The D registry entry, from a checker verdict on any `c = cf` (gen_hd.py: `MODV.hD_i` with `hc := rfl`). -/
def dEntryOf {{c : DCheck18.Conf}} (hD : DCheck18.dReducible c = true) (hc : c = cf) : ClaimGlue.DEntry where
  cf := c
  hD := hD
  hr2 := by subst hc; decide
  hr := by subst hc; decide
  hsym := by subst hc; exact cf_sym
  hloop := by subst hc; exact cf_loop

/-- **Per-key D reduction, registry form.** -/
theorem colorable_of_occ_entry {{c : DCheck18.Conf}} (hD : DCheck18.dReducible c = true) (hc : c = cf)
    {{T : SphericalMap n}} (htri : T.Triangulated) {occ}
    (h : Occ T ring int)
    {IH} : T.graph.Colorable 4 :=
  (dEntryOf hD hc).colorable (show ClaimGlue.OccursW c T by rw [hc]; exact occursW_of_occ htri h) IH

/-- The same for an occurrence of the mirror image (`Occ` in `T.mirror`, same graph). -/
theorem colorable_of_mirror_occ_entry {{c : DCheck18.Conf}} (hD : DCheck18.dReducible c = true) (hc : c = cf)
    {{T : SphericalMap n}} (htri : T.Triangulated) {occ}
    (h : Occ T.mirror ring int)
    {IH} : T.graph.Colorable 4 :=
  colorable_of_occ_entry hD hc (T := T.mirror) (mirror_triangulated htri) h IH

/-- `Occ` gives the C occurrence in the rotation format of any C entry on `cf`. -/
theorem occursCXR_of_occ (e : CGlue.CEntry) (he : e.cf = cf) {{T : SphericalMap n}} (htri : T.Triangulated)
    {occ} (h : Occ T ring int) : CGlue.OccursCXR e T := by
  obtain ⟨G, O, hlt⟩ := configOcc htri h
  rw [← intAdjOf_eq, ← ringAdjOf_eq] at O
  first
  | (unfold CGlue.OccursCXR; rw [he]; exact ⟨G, ρOf ring, int, rot, {W}, rotOcc_of_occ h, rot_ok⟩)
  | (cases e; dsimp only at he; subst he; exact ⟨G, ρOf ring, int, rot, {W}, rotOcc_of_occ h, rot_ok⟩)
  | (cases e; subst he; exact ⟨G, ρOf ring, int, rot, {W}, rotOcc_of_occ h, rot_ok⟩)

/-- `Occ` gives the fold-safe C occurrence (`OccExact`, `NbrInj`, `ApexFacts` derived) of any C entry on `cf`. -/
theorem occursCXF_of_occ (e : CGlue.CEntry) (he : e.cf = cf) {{T : SphericalMap n}} (htri : T.Triangulated)
    {occ} (h : Occ T ring int) : CGlue.OccursCXF e T :=
  (occursCXR_of_occ e he htri h).toF

/-- **Per-key C reduction, registry form** (a fold-safe C entry on `cf`, e.g. `XRData.toCEntryF`). -/
theorem colorable_of_occ_centry (e : CGlue.CEntryF) (he : e.cf = cf) {{T : SphericalMap n}}
    (htri : T.Triangulated) {occ}
    (h : Occ T ring int)
    {IH} : T.graph.Colorable 4 :=
  e.colorable htri (occursCXF_of_occ e.toCEntry he htri h) IH

/-- The same for an occurrence of the mirror image. -/
theorem colorable_of_mirror_occ_centry (e : CGlue.CEntryF) (he : e.cf = cf) {{T : SphericalMap n}}
    (htri : T.Triangulated) {occ}
    (h : Occ T.mirror ring int)
    {IH} : T.graph.Colorable 4 :=
  colorable_of_occ_centry e he (T := T.mirror) (mirror_triangulated htri) h IH
'''


def cocc_text(occ, ns, r, m, form, registry=True):
    b = bridge_text(occ, ns, ns)
    if not registry: return b
    endl = '\nend SimpleGraph.SphericalMap.%s\n' % ns
    i = b.rindex(endl)
    return (b[:i] + '\n' + registry_text(ns, r, m, form).strip('\n') + '\n' + b[i:]
            + ''.join('#print axioms SimpleGraph.SphericalMap.%s.%s\n' % (ns, x) for x in REG_NAMES))


# ------------------------------------------------------------------------------------------------ Python prechecks
def rotok_py(r, m, ra, ia, rot):
    """CGlue/COccBridge `rotOK`, evaluated in Python on the bridge rotation."""
    for a in range(m):
        L = rot[a]; d = len(L)
        if not all(('inl', b) in L for b in ia[a]): return False
        if not all(t < r and ('inr', t) in L for t in ra[a]): return False
        for k, i in L:
            if k == 'inl' and i not in ia[a]: return False
            if k == 'inr' and i not in ra[a]: return False
        for k in range(d):
            s1, s0 = L[(k + 1) % d], L[k]
            if s1[0] == 'inl' and s0[0] == 'inr' and s0[1] not in ra[s1[1]]: return False
    return True


def precheck(r, m, ra, ia, occ):
    P = check_conf(r, m, ra, ia)
    if not 2 <= r <= 19: P.append('ring %d outside 2..19 (ClaimGlue.DEntry, DCheck18)' % r)
    R = bridge_rot(occ)
    if sorted(R) != list(range(m)): P.append('bridge rotation does not cover the interior')
    elif not rotok_py(r, m, ra, ia, R): P.append('rotOK fails')
    degs = re.search(r'deg : ∀ a, T\.graph\.degree \(int a\) = \(!\[([0-9, ]*)\]', occ)
    if not degs or [int(x) for x in degs.group(1).split(', ')] != [len(ia[a]) + len(ra[a]) for a in range(m)]:
        P.append('deg field is not the free-completion degree')
    return P


# -------------------------------------------------------------------------------------------------------- drivers
def doc_safe(s):
    """A name inside a Lean comment: no comment delimiters."""
    return s.replace('/-', '/ -').replace('-/', '- /')


def gen_one(line, ns, outdir, form='walk', walk_assume=False, bridge=True, registry=True, write=True):
    name, r, m, ra, ia, canon = parse_kc(line)
    P = check_conf(r, m, ra, ia)
    if P: raise KcError('%s: %s' % (name, '; '.join(P)))
    occ = occ_text(canon, ns, form, walk_assume)
    if doc_safe(name) != name:   # only the module docstring holds the name outside a string literal
        occ = occ.replace('# Occurrence of %s ' % name, '# Occurrence of %s ' % doc_safe(name), 1)
    P = precheck(r, m, ra, ia, occ)
    if P: raise KcError('%s: %s' % (name, '; '.join(P)))
    files = {ns + '.lean': occ}
    if bridge:
        files['COcc%s.lean' % ns] = cocc_text(occ, ns, r, m, form, registry)
    if write:
        for f, t in files.items():
            open(os.path.join(outdir, f), 'w').write(t)
    return name, r, m, files


def hd_glue_text(mod, pfx, ents, prefix):
    """MODOcc.lean: gen_hd.py's hD_i tied to each occurrence module (D side, registry form)."""
    out = ['import %sAll' % mod] + ['import COcc%s' % ns for (i, ns, name, r, m) in ents]
    out.append('''
/-! # %sOcc (s74_leanglue/gen_occ_kc.py): gen_hd.py's verdicts `%sV.hD_i` on `%s.%sConfs`, tied to the per-key
occurrence modules (`COcc<NS>`). `dEntry_i` is the `ClaimGlue.DEntry`; `colorable_i` is the per-key reduction from a
rotation occurrence `Occ` (face-walk ring by default). The `rfl` is `%s.%sConfs.get ⟨i, _⟩ = <NS>.cf` (same Conf literal). -/

open SimpleGraph SimpleGraph.SphericalMap

namespace %sOcc

variable {n : ℕ}
''' % (mod, mod, mod, pfx, mod, pfx, mod))
    names = []
    for (i, ns, name, r, m) in ents:
        names += ['dEntry_%d' % i, 'colorable_%d' % i]
        out.append('''/-- Entry %d, `%s` (ring %d, %d interior vertices). -/
def dEntry_%d : ClaimGlue.DEntry := %s.dEntryOf %sV.hD_%d rfl

theorem colorable_%d {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin %d → Fin n}
    {int : Fin %d → Fin n} (h : %s.Occ T ring int)
    (IH : ∀ (m' : ℕ) (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support →
      N.graph.Colorable 4) : T.graph.Colorable 4 :=
  %s.colorable_of_occ_entry %sV.hD_%d rfl htri h IH
''' % (i, doc_safe(name), r, m, i, ns, mod, i, i, r, m, ns, ns, mod, i))
    out.append('/-- The batch as a list of D registry entries. -/')
    out.append('def dEntries : List ClaimGlue.DEntry := [%s]\n' % ', '.join('dEntry_%d' % i for (i, *_ ) in ents))
    out.append('end %sOcc\n' % mod)
    out += ['#print axioms %sOcc.%s' % (mod, x) for x in names]
    return '\n'.join(out) + '\n'


def main(argv):
    if len(argv) >= 4 and argv[0] not in ('one', 'batch', 'check') and os.path.isfile(argv[0]) and argv[1].isdigit():
        argv = ['one', '%s:%s' % (argv[0], argv[1]), argv[2], argv[3], '--form', 'ring'] + argv[4:]   # gen_occ_key order
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sp = ap.add_subparsers(dest='cmd', required=True)
    for c in ('one', 'batch'):
        p = sp.add_parser(c)
        if c == 'one':
            p.add_argument('src'); p.add_argument('ns'); p.add_argument('outdir')
        else:
            p.add_argument('extrafile'); p.add_argument('outdir'); p.add_argument('prefix')
            p.add_argument('--hd', nargs=2, metavar=('MOD', 'PFX'))
            p.add_argument('--first', type=int, default=0); p.add_argument('--count', type=int, default=None)
        p.add_argument('--form', choices=('walk', 'ring'), default='walk')
        p.add_argument('--walk-assume', action='store_true', help='walk form with ring_dinj as an Occ field (WALK_ASSUME=1)')
        p.add_argument('--no-bridge', action='store_true'); p.add_argument('--no-registry', action='store_true')
    p = sp.add_parser('check'); p.add_argument('files', nargs='+')
    a = ap.parse_args(argv)
    if a.cmd == 'one':
        line = read_src(a.src)
        name, r, m, files = gen_one(line, a.ns, a.outdir, a.form, a.walk_assume, not a.no_bridge, not a.no_registry)
        print('%s: %s (r=%d m=%d) -> %s   [%s]' % (a.ns, name, r, m, ', '.join(files), dict(STATS)))
    elif a.cmd == 'batch':
        lines = [l for l in open(a.extrafile) if l.strip()]
        N = len(lines); w = 2 if N <= 100 else 3
        idx = range(a.first, N if a.count is None else min(N, a.first + a.count))
        ents = []; fail = []
        for i in idx:
            ns = '%s%0*d' % (a.prefix, w, i)
            try:
                name, r, m, files = gen_one(lines[i], ns, a.outdir, a.form, a.walk_assume, not a.no_bridge, not a.no_registry)
                ents.append((i, ns, name, r, m))
            except (KcError, AssertionError, KeyError, ValueError) as e:
                fail.append((i, str(e)[:200]))
        if a.hd:
            if fail or a.no_bridge or a.no_registry: raise SystemExit('--hd needs every entry generated with bridge and registry')
            open(os.path.join(a.outdir, a.hd[0] + 'Occ.lean'), 'w').write(hd_glue_text(a.hd[0], a.hd[1], ents, a.prefix))
        with open(os.path.join(a.outdir, a.prefix.rstrip('_') + '_modules.txt'), 'w') as f:
            for (i, ns, name, r, m) in ents: f.write('%d\t%s\t%s\t%d\t%d\n' % (i, ns, name, r, m))
        print('%d generated, %d failed %s  [%s]' % (len(ents), len(fail), fail[:5], dict(STATS)))
        return 1 if fail else 0
    else:
        bad = 0; n = 0
        for fn in a.files:
            for l in open(fn):
                if not l.strip(): continue
                n += 1
                try:
                    name, r, m, ra, ia, canon = parse_kc(l)
                    P = check_conf(r, m, ra, ia)
                    if P: raise KcError('; '.join(P))
                    rot = rotation_kc(r, m, ra, ia)
                except (KcError, AssertionError, ValueError) as e:
                    bad += 1; print('FAIL %s: %s' % (l.split()[0], e))
        print('%d kc lines, %d failed  [%s]' % (n, bad, dict(STATS)))
        return 1 if bad else 0
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
