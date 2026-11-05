import sys
N = sys.argv[1]
KC = []
for cf in (N + '/scripts/B3_configs_D_kill6wide.txt', N + '/scripts/B3_configs_D_l3qrow.txt'):
    for l in open(cf):
        if not l.startswith('#') and l.strip(): KC.append(l.split('|')[0].strip())
sys.argv = [N + '/scripts/mkrules_negctl.py', N + '/scripts/mkrules.py', N + '/scripts/k6in/discharge/wheeldis/loop/k42/grow.py', N + '/eng/privcell.py', N + '/rules']
G = {'__name__': 'x', 'KC': KC}; exec(open(sys.argv[0]).read(), G)
