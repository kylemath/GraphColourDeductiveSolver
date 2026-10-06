"""verify.py checks (A: real components = abstract for some M; B: real radius <= game value)
applied to the vdred_joint ('full' adversary) values.  [computed, exploratory] 2026-10-06."""
import random, sys
import graphs, vdred_joint, verify

nvar = int(sys.argv[1]) if len(sys.argv) > 1 else 5
rng = random.Random(20261006)
cases = [('T4', graphs.T4(), 4), ('A3', graphs.A(3), 0), ('A4', graphs.A(4), 0), ('pentakis', graphs.pentakis(), 0)]
for name, F, v in cases:
    cfg = graphs.ball_config(F, v, 2)
    res = vdred_joint.solve_joint(cfg, verbose=False)
    print(name, 'joint: reducible', res['reducible'], 'depth', res['depth'], res['hist'], flush=True)
    print('  ', verify.check(F, v, cfg, res, name + ' original'), flush=True)
    nv = nvar if name != 'pentakis' else 1
    for k in range(nv):
        F2 = verify.outside_flips(F, cfg, rng.randint(1, 8), rng)
        print('  ', verify.check(F2, v, cfg, res, f'{name} flipped#{k}'), flush=True)
