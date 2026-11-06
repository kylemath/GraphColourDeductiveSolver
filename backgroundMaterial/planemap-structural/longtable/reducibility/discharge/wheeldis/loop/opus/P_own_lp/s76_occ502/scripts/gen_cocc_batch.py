#!/usr/bin/env python3
"""gen_cocc_batch.py (Opus, s76_occ502, 6 Nov 2026): the C-batch occurrence template (HW13Occ.lean's pattern) for any Studio C job.

usage: gen_cocc_batch.py MODULES.txt MOD VALL VNS ENTRIES PFX OUT.lean "DOC"
  MODULES.txt  gen_occ_kc.py batch's <PFX>modules.txt (k, module, name, r, m per line)
  MOD          the Lean module / namespace to write (e.g. HW2AOcc)
  VALL         Studio's verdict module to import (e.g. W2AVAll); VNS its namespace (W2AV, theorem hC_all)
  ENTRIES      the CGlue entry list (w2aEntries; with theorems ENTRIES_ok, ENTRIES_length)
  PFX          the occurrence module prefix (HW2A_; modules PFXkk and COccPFXkk)
  DOC          the docstring's lead sentence (job, main sha)
Regression: run with HW3_modules.txt HW13Occ HW13All HW13V w13Entries HW3_ and the original lead -> byte-identical HW13Occ.lean
"""
import sys
mods, MOD, VALL, VNS, ENT, PFX, OUT, DOC = sys.argv[1:9]
rows = [l.rstrip('\n').split('\t') for l in open(mods) if l.strip()]
n = len(rows)
assert [int(r[0]) for r in rows] == list(range(n)), 'modules file not 0..n-1'
L = ['import %s' % VALL] + ['import COcc%s' % r[1] for r in rows] + ['']
L.append(DOC)
L.append('')
L.append('open SimpleGraph SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck')
L.append('')
L.append('namespace %s' % MOD)
L.append('')
L.append('variable {n : ℕ}')
L.append('')
L.append('/-- The fold-safe C entry `k` of `CGlue.%s`, with Studio\'s `hC`. -/' % ENT)
L.append('def cEntry (k : Fin %d) : CEntryF :=' % n)
L.append('  (%s.get (k.cast %s_length.symm)).toCEntryF' % (ENT, ENT))
L.append('    (List.all_eq_true.1 %s_ok _ (List.get_mem _ _)) (%s.hC_all k)' % (ENT, VNS))
for k, mod, name, r, m in rows:
    k = int(k)
    for mir in (False, True):
        L.append('')
        if not mir: L.append('/-- Entry %d, `%s` (ring %s, %s interior vertices). -/' % (k, name, r, m))
        else: L.append('/-- The same for an occurrence of the mirror image. -/')
        L.append('theorem colorable_%s%d {T : SphericalMap n} (htri : T.Triangulated) {ring : Fin %s → Fin n}' % ('mirror_' if mir else '', k, r))
        L.append('    {int : Fin %s → Fin n} (h : %s.Occ T%s ring int)' % (m, mod, '.mirror' if mir else ''))
        L.append('    (IH : ∀ (m\' : ℕ) (N : SphericalMap m\'), Nat.card N.graph.support < Nat.card T.graph.support →')
        L.append('      N.graph.Colorable 4) : T.graph.Colorable 4 :=')
        L.append('  %s.colorable_of_%socc_centry (cEntry %d) rfl htri h IH' % (mod, 'mirror_' if mir else '', k))
L.append('')
L.append('/-- The batch as a list of C registry entries. -/')
L.append('def cEntries : List CEntryF := [%s]' % ', '.join('cEntry %d' % k for k in range(n)))
L.append('')
L.append('end %s' % MOD)
L.append('')
L.append('#print axioms %s.cEntry' % MOD)
for k in range(n):
    L.append('#print axioms %s.colorable_%d' % (MOD, k))
    L.append('#print axioms %s.colorable_mirror_%d' % (MOD, k))
open(OUT, 'w').write('\n'.join(L) + '\n')
print('%s: %d entries -> %s' % (MOD, n, OUT))
