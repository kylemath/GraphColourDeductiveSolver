"""Build the 0125c46b forbidden set exactly as s25/f/s16_filter.registry() (used for s25 kill tables) and pickle it."""
import sys, os, pickle, hashlib
P = '/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp'
EX = '/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ex59'
F16 = P + '/s25/f/s16_filter.py'
sys.argv = ['x', EX, P + '/s25/k3x_D_0125c46b.out', P + '/s25/k3x_C_0125c46b.cfast', '/dev/null']
g = {'__name__': 'lib', '__file__': F16}
exec(compile(open(F16).read().split("if __name__ == '__main__':")[0], F16, 'exec'), g)
C = g['registry']()
print('forbidden set', len(C), 'names md5', hashlib.md5('\n'.join(sorted(c[0] for c in C)).encode()).hexdigest())
pickle.dump(C, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reg_A59.pkl'), 'wb'))
