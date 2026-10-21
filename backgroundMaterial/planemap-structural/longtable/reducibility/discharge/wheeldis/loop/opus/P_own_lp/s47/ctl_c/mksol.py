# s47 control (c): hand-made solutions from s42a's A78 solution: t raised by DT, plus q[(8, 6, 6, 5)] = DQ (Q left out: the
# check takes Qeff = max(sol, max q over mask)).  usage: python3 mksol.py SOL OUT DT DQ
import json, sys
S = json.load(open(sys.argv[1])); DT, DQ = float(sys.argv[3]), float(sys.argv[4])
S['t'] = S['t'] + DT; S['lq'] = S['lq'] + [[[8, 6, 6, 5], DQ]]
json.dump(S, open(sys.argv[2], 'w')); print('t', S['t'], 'lq', S['lq'])
