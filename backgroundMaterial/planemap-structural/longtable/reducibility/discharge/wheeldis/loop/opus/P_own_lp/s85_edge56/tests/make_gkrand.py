# s85 test point: sol_k83D_in01_c6le.json (from_opus) with random gkeys amounts in [0, 0.05] (seed 5) and kstar off -> tests/sol_k83D_gkrand.json
import json, random
S = json.load(open('/mnt/project-files/swarm/round6/W12-studio-K/from_opus/sol_k83D_in01_c6le.json'))
names = [l.split()[0] for l in open('keys/relax_ceiling_87keys.txt') if l.strip() and not l.startswith('#')]
rng = random.Random(5)
S['ks'] = [[n, round(rng.uniform(0.0, 0.05), 6)] for n in names]; S['kstar'] = False
json.dump(S, open('tests/sol_k83D_gkrand.json', 'w'))
