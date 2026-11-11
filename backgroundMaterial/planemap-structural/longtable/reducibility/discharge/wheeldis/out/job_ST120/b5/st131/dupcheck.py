import sys, os, collections
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare as C
d = int(os.environ.get('D', '7'))
T = C.theirs(d); c = collections.defaultdict(list)
for s in T: c[C.canon(s[0], s[1], s[2])].append(s)
print('W6r leaves', len(T), 'canonical states', len(c), 'extra', sum(len(v) - 1 for v in c.values()))
for k, v in list(c.items()):
    if len(v) > 1:
        for s in v: print(''.join(map(str, s[0])), ''.join(map(str, s[1])), '.'.join(''.join(map(str, x)) for x in s[2]))
        break
