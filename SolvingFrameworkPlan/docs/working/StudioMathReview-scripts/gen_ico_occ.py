import re, sys
P = sys.argv[1]
occs = {'DiamondM': ([11, 5, 6, 2, 9, 10], [0, 1, 8, 7]), 'DiamondP': ([5, 11, 10, 9, 2, 6], [0, 7, 8, 1])}
out = []
for ns, (ring, it) in occs.items():
    occ = open(P + ns + 'Occ.lean').read().split('structure Occ')[1].split('theorem')[0]
    fields = re.findall(r'^\s+(r\d+_\d+) : Nx T', occ, re.M)
    R = '![' + ', '.join(map(str, ring)) + ']'; I = '![' + ', '.join(map(str, it)) + ']'
    out.append(f'/-- The Birkhoff diamond occurs in the icosahedron (`{ns}`). -/')
    out.append(f'theorem occ_{ns} : {ns}.Occ sphericalMap {R} {I} where')
    out.append('  ring_inj := by decide')
    out.append('  int_inj := by decide')
    out.append('  disj := by decide')
    out.append('  deg := fun a => by rw [sphericalMap_degree]; revert a; decide')
    for f in fields: out.append(f'  {f} := nx_ico (by decide) rfl')
    out.append('')
out.append('''/-- **The icosahedron is not diamond-free**, so it lies outside the class of `RStarFrame`. -/
theorem not_diamondFree : ¬ DiamondFree sphericalMap := fun h => h.1 ⟨_, _, occ_DiamondM⟩

/-- RSST 2.122 does not occur in the icosahedron: it needs a vertex of degree six. -/
theorem conf2122Free : Conf2122Free sphericalMap := by
  refine ⟨fun ⟨_, int, h⟩ => ?_, fun ⟨_, int, h⟩ => ?_⟩
  · have := h.deg 0; rw [sphericalMap_degree] at this; exact absurd this (by decide)
  · have := h.deg 0; rw [sphericalMap_degree] at this; exact absurd this (by decide)

end Icosahedron
end SimpleGraph''')
print('\n'.join(out))
