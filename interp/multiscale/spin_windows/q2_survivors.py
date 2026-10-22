"""Re-sample exactly as q2_budget.py (same seed, per group) and analyse only the bad classes that survive AC:
which spin variants kill them and whether the spin-free baselines already do."""
import sys, csv, random, collections
sys.path.insert(0, '/mnt/project-files/multiscale/spin_windows')
from q2_budget import Window, random_ring, all_rings
rows = list(csv.DictReader(open('/mnt/project-files/explore/dataset/windows_judged.tsv'), delimiter='\t'))
groups = {
  'a7_D':    [x for x in rows if x['name'].startswith('a7_') and x['two_engine'] == 'D'],
  'a7_notD': [x for x in rows if x['name'].startswith('a7_') and x['kc_D'] == 'false' and 10 <= int(x['ring']) <= 15],
  'a9_D':    [x for x in rows if x['name'].startswith('a9_') and x['two_engine'] == 'D'],
  'a9_notD': [x for x in rows if x['name'].startswith('a9_') and x['kc_D'] == 'false' and 10 <= int(x['ring']) <= 15]}
for g, pool in groups.items():
    rng = random.Random(2026); rng.shuffle(pool); c = collections.Counter(); ex = []
    for row in pool[:12]:
        W = Window(row); r = W.r
        rings = all_rings(r) if r <= 9 else list({random_ring(r, rng) for _ in range(120)})
        for ring in rings:
            if W.extend(ring) is not None or W.ac_refutes(ring): continue
            c['surv'] += 1
            b0 = not W.budget(ring, mode='none'); b0o = not W.budget(ring, odd_proper=True, mode='none')
            kA = not W.budget(ring); kAo = not W.budget(ring, odd_proper=True)
            c['blocked'] += b0; c['oddcol_free'] += b0o; c['A'] += kA; c['A_odd'] += kAo
            c['A_odd_not_oddcol'] += kAo and not b0o
            if kAo and not b0o and len(ex) < 3: ex.append((W.name, ring))
    print(g, dict(c), ex, flush=True)
