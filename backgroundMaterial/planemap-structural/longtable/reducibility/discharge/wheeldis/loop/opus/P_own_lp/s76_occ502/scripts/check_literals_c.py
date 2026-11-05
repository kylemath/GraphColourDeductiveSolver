"""check_literals_c.py (as check_literals.py, but the Conf literal may open with "{" plus a newline, as in XRData cf fields). MOD.lean LEANDIR PREFIX : field-by-field check that gen_hd's <PFX>Confs entry k equals <PREFIX><kk>.cf
(name, r, m, ringAdj, intAdj), i.e. that HDxxOcc's `rfl` holds syntactically. Exit 1 on any mismatch."""
import re, sys, os
mod, d, pfx = sys.argv[1:4]
S = open(mod).read()
ents = re.findall(r'\{\s*name := "([^"]*)", r := (\d+), m := (\d+),\s*ringAdj := (#\[.*?\]\]|#\[\]),\s*intAdj := (#\[.*?\]\]|#\[\]) \}', S, re.S)
norm = lambda s: re.sub(r'\s+', '', s)
bad = 0
for k, e in enumerate(ents):
    f = os.path.join(d, '%s%02d.lean' % (pfx, k))
    if not os.path.exists(f): f = os.path.join(d, '%s%03d.lean' % (pfx, k))
    T = open(f).read()
    m = re.search(r'def cf : DCheck18\.Conf where\s*name := "([^"]*)"\s*r := (\d+)\s*m := (\d+)\s*ringAdj := (.*?)\n\s*intAdj := (.*?)\n', T, re.S)
    got = tuple(norm(x) for x in m.groups()); want = tuple(norm(x) for x in e)
    if got != want: bad += 1; print('MISMATCH', k, e[0], [i for i in range(5) if got[i] != want[i]])
print('entries', len(ents), 'mismatches', bad)
sys.exit(1 if bad or not ents else 0)
