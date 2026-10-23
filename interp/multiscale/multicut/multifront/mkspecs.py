import json
done = {json.loads(l)['spec'] for l in open('/mnt/project-files/multiscale/multicut/multifront/main.jsonl')}
Z = 'ren=1,mb=2'; S = []
for sd in range(1, 7):
    for m in (1, 2, 4, 8, 16): S.append(f'ico10:{m}:{sd}:{Z}')
for sd in range(1, 4):
    for m in (1, 4, 16): S.append(f'L18:{m}:{sd}:{Z}')
for mp in ('defect10_1', 'flip10_1', 'defect14_1', 'defect22_1'):
    for m in (1, 4, 16): S.append(f'{mp}:{m}:1:{Z}')
for mp in ('helix_100', 'helix_200', 'w02_200', 'w021_200'):
    for m in (1, 4): S.append(f'rigid_{mp}:{m}:1:{Z}')
for sd in (1, 2):
    for m in (4, 8):
        for o in ('ren=0,mb=0', 'ren=0,mb=2', 'ren=1,mb=0'): S.append(f'ico10:{m}:{sd}:{o}')
    S.append(f'L18:4:{sd}:ren=0,mb=0')
for sd in range(1, 5):
    for m in (1, 4, 16): S.append(f'ico10:{m}:{sd}:{Z},tz=1')
for sd in (1, 2):
    for m in (1, 4, 16): S.append(f'L18:{m}:{sd}:{Z},tz=1')
for m in (1, 16): S.append(f'ico16:{m}:1:{Z}')
print(' '.join(s for s in S if s not in done))
