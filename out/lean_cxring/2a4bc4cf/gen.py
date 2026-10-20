"""CXRing batch (Long Table 00:54Z): one Lean file per ring-X C entry K = 0..95 proving its C verdict
  hC_K : cReducible18 e.cf e.eqR e.eqI = true  (e = xrEntries.get K), by native_decide,
then an assembly file proving the verdict for all 96 (fin_cases over the per-entry theorems) and building the CEntryF
list with XRData.toCEntryF. Usage: python3 gen.py OUTDIR"""
import sys, os
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
HDR = 'import CXRing\nopen SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck\nnamespace CXR\n'
def ent(k): return '(xrEntries.get ⟨%d, by rw [xrEntries_length]; decide⟩)' % k
for k in range(96):
    open(os.path.join(OUT, 'CXR%02d.lean' % k), 'w').write(HDR +
        'theorem hC_%d : cReducible18 %s.cf %s.eqR %s.eqI = true := by native_decide\nend CXR\n#print axioms CXR.hC_%d\n' % (k, ent(k), ent(k), ent(k), k))
imp = ''.join('import CXR%02d\n' % k for k in range(96))
body = ('open SimpleGraph.SphericalMap SimpleGraph.SphericalMap.CGlue DCheck\nnamespace CXR\n'
        'theorem hC_all (k : Fin 96) : cReducible18 (xrEntries.get (k.cast xrEntries_length.symm)).cf\n'
        '    (xrEntries.get (k.cast xrEntries_length.symm)).eqR (xrEntries.get (k.cast xrEntries_length.symm)).eqI = true := by\n'
        '  fin_cases k\n' + ''.join('  · exact hC_%d\n' % k for k in range(96)) +
        '/-- every ring-X entry as a fold-safe CEntryF -/\n'
        'def cxF (k : Fin 96) : CEntryF :=\n'
        '  (xrEntries.get (k.cast xrEntries_length.symm)).toCEntryF\n'
        '    (List.all_eq_true.1 xrEntries_ok _ (List.get_mem _ _)) (hC_all k)\n'
        'end CXR\n#print axioms CXR.hC_all\n#print axioms CXR.cxF\n')
open(os.path.join(OUT, 'CXRAll.lean'), 'w').write(imp + body)
print('wrote 96 entry files + CXRAll.lean')
