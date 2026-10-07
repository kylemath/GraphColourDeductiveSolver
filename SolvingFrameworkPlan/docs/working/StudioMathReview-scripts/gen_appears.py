"""Generate `occ_of_appears` for a K4-e configuration with M/P occurrence modules.
Usage: python3 -I gen_appears.py <PlaneMap dir/> <M ns> <P ns> <Name>   (prints a Lean module)"""
import re, sys
P, NSM, NSP, NAME = sys.argv[1:5]

def parse(ns):
    occ = open(P + ns + 'Occ.lean').read().split('structure Occ')[1].split('\ntheorem')[0]
    sym = lambda k, i: ('i' if k == 'int' else 'r') + i
    F = []
    for l in occ.splitlines():
        m = re.match(r'\s+(r\d+_\d+) : Nx T \((int|ring) (\d+)\) \((int|ring) (\d+)\) \((int|ring) (\d+)\)', l)
        if m:
            g = m.groups(); F.append((g[0], sym(g[1], g[2]), sym(g[3], g[4]), sym(g[5], g[6])))
    deg = [int(x) for x in re.search(r'!\[([\d, ]+)\]', occ.split('deg :')[1]).group(1).split(',')]
    R = 1 + max(int(x[1:]) for f in F for x in f[1:] if x[0] == 'r')
    return F, deg, R

def lean(x): return f'(int {x[1:]})' if x[0] == 'i' else f'q{x[1:]}'
KADJ = {('i0','i1'): 'A.a01', ('i0','i2'): 'A.a02', ('i0','i3'): 'A.a03', ('i1','i2'): 'A.a12', ('i2','i3'): 'A.a23'}
def kadj(a, b):
    if (a, b) in KADJ: return KADJ[(a, b)]
    if (b, a) in KADJ: return f'{KADJ[(b, a)]}.symm'
    return None

def engine(ns, seed, F, deg, R, ind):
    out = []; w = lambda s: out.append(' ' * ind + s)
    target = {(v, a): b for _, v, a, b in F}
    closure = set(target.items())
    for (v, a), b in list(target.items()):
        closure |= {((b, v), a), ((a, b), v)}
    facts = {}; cnt = [0]; defined = {'i0', 'i1', 'i2', 'i3'}
    def add(v, a, b, expr):
        if v[0] != 'i': return False
        if (v, a) in facts:
            assert facts[(v, a)][0] == b, (ns, v, a, b, facts[(v, a)]); return False
        assert ((v, a), b) in closure, (ns, 'unexpected fact', v, a, b)
        cnt[0] += 1; nm = f'f{cnt[0]}'
        w(f'have {nm} : Nx T {lean(v)} {lean(a)} {lean(b)} := {expr}')
        facts[(v, a)] = (b, nm); return True
    # seed
    sv, sa, sb = seed
    add(sv, sa, sb, 'h0')
    def adjp(v, x):
        if (v, x) in facts: return f'(nx_adj_left {facts[(v, x)][1]})'
        for (vv, a), (b, nm) in facts.items():
            if vv == v and b == x: return f'(nx_adj_right {nm})'
        return None
    chains = {}; faced = False
    def step():
        nonlocal faced
        prog = False
        for (v, u), (y, nm) in list(facts.items()):
            prog |= add(y, v, u, f'(nx_tri htri {nm}).1')
            prog |= add(u, y, v, f'(nx_tri htri {nm}).2')
        if prog: return True
        if not faced:
            faced = True
            d1 = (('i2', 'i0', 'i3')); d2 = (('i0', 'i2', 'i3'))
            good, bad, side = ((d1, d2, 0) if ((d1[0], d1[1]), d1[2]) in closure else (d2, d1, 1))
            assert ((good[0], good[1]), good[2]) in closure
            known = facts[(bad[0], bad[1])]
            assert known[0][0] == 'i' and known[0] != bad[2]
            cnt[0] += 1; nm = f'f{cnt[0]}'
            w(f'have {nm} : Nx T {lean(good[0])} {lean(good[1])} {lean(good[2])} := by')
            w(f'  rcases hns (int 0) (int 2) (int 3) A.a02 A.a23 A.a03.symm with h | h')
            if side == 0:
                w('  · exact h')
                w(f'  · exact absurd (nx_func {known[1]} h) (fun e => absurd (A.int_inj e) (by decide))')
            else:
                w(f'  · exact absurd (nx_func {known[1]} h) (fun e => absurd (A.int_inj e) (by decide))')
                w('  · exact h')
            facts[(good[0], good[1])] = (good[2], nm); return True
        for k in range(4):
            v = f'i{k}'; d = deg[k]
            if v in chains: continue
            fv = {a: b for (vv, a), (b, _) in facts.items() if vv == v}
            if len(fv) < d - 1: continue
            starts = [a for a in fv if a not in fv.values()] or list(fv)
            for a0 in starts:
                ent = [a0]
                while len(ent) < d and ent[-1] in fv: ent.append(fv[ent[-1]])
                if len(ent) == d and len(set(ent)) == d: break
            else: continue
            hyps = ' '.join(facts[(v, ent[i])][1] for i in range(d - 1))
            pairs = [(i, j) for i in range(d) for j in range(i + 1, d)]
            names = ', '.join(f'n{k}_{i}_{j}' for i, j in pairs)
            lem = 'chain5' if d == 5 else 'chain6'
            pat = f'⟨cl{k}, ⟨{names}⟩, -⟩' if d == 5 else f'⟨cl{k}, ⟨{names}⟩⟩'
            w(f'obtain {pat} := {lem} (show T.graph.degree (int {k}) = {d} by rw [A.deg {k}]; rfl) {hyps}')
            chains[v] = ent
            if (v, ent[-1]) not in facts:
                assert ((v, ent[-1]), ent[0]) in closure
                facts[(v, ent[-1])] = (ent[0], f'cl{k}')
            return True
        for _, v, a, b in F:
            if (v, a) not in facts and a in defined and b not in defined and b[0] == 'r':
                ap = adjp(v, a)
                if ap is None: continue
                cnt[0] += 1; nm = f'f{cnt[0]}'
                w(f'obtain ⟨{lean(b)}, {nm}⟩ : ∃ r, Nx T {lean(v)} {lean(a)} r := ⟨_, {ap}, rfl⟩')
                facts[(v, a)] = (b, nm); defined.add(b); return True
        return False
    while step(): pass
    for fname, v, a, b in F: assert facts.get((v, a), (None,))[0] == b, (ns, fname, v, a, b, facts.get((v, a)))
    assert len(chains) == 4
    # distinctness
    N = {f'r{t}': sorted({v for _, v, a, b in F if f'r{t}' in (a, b)}) for t in range(R)}
    def ne(x, y):
        if x[0] == 'i' and y[0] == 'i': return '(fun e => absurd (A.int_inj e) (by decide))'
        for k in range(4):
            ent = chains[f'i{k}']
            if x in ent and y in ent:
                i, j = ent.index(x), ent.index(y)
                return f'n{k}_{i}_{j}' if i < j else f'(n{k}_{j}_{i}).symm'
        if x[0] == 'r' and y[0] == 'i': return f'dj{x[1:]}_{y[1:]}'
        if x[0] == 'i' and y[0] == 'r': return f'(dj{y[1:]}_{x[1:]}).symm'
        return None
    for t in range(R):
        x = f'r{t}'
        for a in range(4):
            y = f'i{a}'; pf = None
            for k in range(4):
                ent = chains[f'i{k}']
                if x in ent and y in ent: pf = ne(x, y)
            if pf is None and y in N[x]:
                pf = f'(SimpleGraph.Adj.ne {adjp(y, x)}).symm'
            if pf is None:
                b = N[x][0]; assert {b, y} == {'i1', 'i3'}, (x, y, N[x])
                pf = (f'fun e => A.n13 (by rw [← e]; exact {adjp(b, x)})' if b == 'i1'
                      else f'fun e => A.n13 (by rw [← e]; exact {adjp(b, x)}.symm)')
            w(f'have dj{t}_{a} : {lean(x)} ≠ int {a} := {pf}')
    for s in range(R):
        for t in range(s + 1, R):
            xs, xt = f'r{s}', f'r{t}'
            pf = ne(xs, xt) if any(xs in e and xt in e for e in chains.values()) else None
            if pf is not None:
                w(f'have rg{s}_{t} : q{s} ≠ q{t} := {pf}'); continue
            pair = next(((a, b) for a in N[xs] for b in N[xt] if kadj(a, b)), None)
            if pair:
                a, b = pair
                e2, fe2 = facts[(b, a)]; e1, fe1 = facts[(a, b)]
                w(f'have rg{s}_{t} : q{s} ≠ q{t} := by')
                w(f'  intro h')
                w(f'  rcases hns {lean(a)} {lean(b)} q{s} {kadj(a, b)} (by rw [h]; exact {adjp(b, xt)}) {adjp(a, xs)}.symm with h1 | h1')
                w(f'  · exact {ne(e2, xt)} ((nx_func {fe2} h1).trans h)')
                w(f'  · exact {ne(e1, xs)} (nx_func {fe1} h1)')
                continue
            a = next(a for a in N[xs] if a in ('i1', 'i3')); b = next(b for b in N[xt] if b in ('i1', 'i3') and b != a)
            a1 = adjp(a, xs); a3 = f'(by rw [h]; exact {adjp(b, xt)})'
            if a == 'i3': a1, a3 = a3, a1
            w(f'have rg{s}_{t} : q{s} ≠ q{t} := by')
            w(f'  intro h')
            w(f'  rcases htip q{s} {a1} {a3} with e | e')
            w(f'  · exact dj{s}_0 e')
            w(f'  · exact dj{s}_2 e')
    ring = '![' + ', '.join(f'q{t}' for t in range(R)) + ']'
    w(f'refine ⟨{ring}, {{')
    w('  ring_inj := ?_')
    w('  int_inj := A.int_inj')
    w('  disj := ?_')
    w('  deg := A.deg')
    for fname, v, a, b in F: w(f'  {fname} := {facts[(v, a)][1]}')
    w('  }⟩')
    w('· intro s t h; fin_cases s <;> fin_cases t <;> first | rfl | exact absurd h ‹_› | exact absurd h.symm ‹_›')
    w('· intro t a; fin_cases t <;> fin_cases a <;> assumption')
    return out

FM, deg, R = parse(NSM); FP, degP, RP = parse(NSP)
assert deg == degP and R == RP
# which disjunct of Facial (int 0) (int 1) (int 2) = Nx (int1)(int0)(int2) ∨ Nx (int0)(int1)(int2) is M?
def clos(F):
    c = set()
    for _, v, a, b in F: c |= {(v, a, b), (b, v, a), (a, b, v)}
    return c
left = ('i1', 'i0', 'i2'); right = ('i0', 'i1', 'i2')
mleft = left in clos(FM); assert mleft != (left in clos(FP))
gam = '![' + ', '.join(map(str, deg)) + ']'
print(f'''module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.AppearsOcc
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.{NSM}Occ
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.{NSP}Occ

/-!
# {NAME}: an appearance with clean tips is an occurrence

Generated by `gen_appears.py`. In a triangulation with no separating triangle, an appearance
(`Appears`) whose tips share only the centres (`TipsClean`) is an occurrence `{NSM}.Occ` or
`{NSP}.Occ`, according to the orientation of the face `int 0, int 1, int 2`. The ring vertices
are the rotation successors at the interior vertices, and they are distinct:
* two ring positions seen from one interior vertex are distinct entries of its rotation;
* positions seen from adjacent interior vertices are excluded by `NoSep`, since the triangle is
  facial and the rotations then force equality with a third, distinct entry;
* the two tip-only positions are excluded by `TipsClean`.
-/

@[expose] public section
namespace SimpleGraph.SphericalMap.{NAME}
open VacancyIcosahedral

variable {{n : ℕ}}

set_option maxHeartbeats 1000000 in
theorem occ_of_appears {{T : SphericalMap n}} (htri : T.Triangulated) (hns : NoSep T)
    {{int : Fin 4 → Fin n}} (A : Appears {gam} T int) (htip : TipsClean T int) :
    (∃ ring, {NSM}.Occ T ring int) ∨ (∃ ring, {NSP}.Occ T ring int) := by
  rcases hns (int 0) (int 1) (int 2) A.a01 A.a12 A.a02.symm with h0 | h0''')
bl = [(FM, NSM, 'left'), (FP, NSP, 'right')]
if not mleft: bl = bl[::-1]
for F, ns, side in bl:
    seed = left if F is (FM if mleft else FP) else right
    print(f'  · {side}')
    print('\n'.join(engine(ns, seed, F, deg, R, 4)))
print(f'\nend SimpleGraph.SphericalMap.{NAME}')
