"""Regenerate the derived line files and random samples used in R0-SCOPE.md (needs out/r0enum_n{14,16}.jsonl,
out/genus_o_n14.txt).  Same seeds as used in the session."""
import json, random
def lines(n): return [json.loads(l)['line'] for l in open(f'out/r0enum_n{n}.jsonl')]
L14 = lines(14); open('out/r0lines_n14.txt', 'w').write(''.join(x + '\n' for x in L14))
random.seed(1); idx = sorted(random.sample(range(len(L14)), 300))
open('out/r0lines_n14_sample.txt', 'w').write(''.join(L14[i] + '\n' for i in idx))
og = [l.split()[0] for l in open('out/genus_o_n14.txt')]
open('out/r0lines_n14_og1.txt', 'w').write(''.join(x + '\n' for x, g in zip(L14, og) if g == '1'))
L16 = lines(16); open('out/r0lines_n16.txt', 'w').write(''.join(x + '\n' for x in L16))
random.seed(2); idx = sorted(random.sample(range(len(L16)), 300))
open('out/r0lines_n16_sample.txt', 'w').write(''.join(L16[i] + '\n' for i in idx))
random.seed(3); idx = sorted(random.sample(range(len(L16)), 15000))
open('out/r0lines_n16_s15k.txt', 'w').write(''.join(L16[i] + '\n' for i in idx))
