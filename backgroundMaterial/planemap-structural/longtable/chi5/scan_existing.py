"""Step 1a (Studio Job 6): every graph line 'name n rot' under TrackF/out and TrackF/graphs -> exact 4-colourability.
Writes out/existing_scan.jsonl (one line per distinct graph name+file) and prints a summary; non-4-colourable ones
are listed with their good holes (degree 5, T - h 4-colourable)."""
import os, sys, json, glob, collections
import chilib
out = open('out/existing_scan.jsonl', 'w'); tally = collections.Counter(); bad = []
files = [f for f in glob.glob(chilib.TRACKF + '/out/**/*', recursive=True) + glob.glob(chilib.TRACKF + '/graphs/**/*', recursive=True)
         if os.path.isfile(f) and f.endswith('.txt')]
seen = set()
for f in sorted(files):
    for l in open(f, errors='ignore'):
        p = l.split()
        if len(p) < 3 or ';' not in p[2] or not p[1].isdigit(): continue
        try: name, rot = chilib.read_line(l)
        except Exception: continue
        if len(rot) != int(p[1]) or (name, p[2]) in seen: continue
        seen.add((name, p[2]))
        adj = chilib.adj_of_rot(rot)
        c4 = chilib.colourable(adj, 4) is not None
        surf = name.split('_')[0]
        tally[(surf, c4)] += 1
        rec = dict(file=os.path.relpath(f, chilib.TRACKF), name=name, n=len(rot), col4=c4)
        if not c4:
            rec['good_holes'] = chilib.good_holes(rot, adj); bad.append(rec)
        out.write(json.dumps(rec) + '\n')
print('distinct graphs', len(seen))
for k in sorted(tally): print(k, tally[k])
print('non-4-colourable:', len(bad))
for r in bad[:40]: print(r)
