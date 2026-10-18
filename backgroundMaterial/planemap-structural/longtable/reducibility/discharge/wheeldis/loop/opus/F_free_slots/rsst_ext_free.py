"""For each filling, the private-letter completions (6 privates, letters 5,6,7,8,9+) that contain no RSST config
(hits from rsst_ext.target with privates wildcard; each embedding fixes the letters it puts on privates)."""
import sys, os, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['x', 'lib']; src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rsst_ext.py')).read()
exec(src[:src.index('FILL =')])
PR = [('p', 1, 1), ('p', 2, 1), ('p', 2, 2), ('p', 4, 1), ('p', 4, 2), ('p', 5, 1)]
for a in range(6, 10):
    for b in range(6, 10):
        s = list(s0); s[1], s[4] = a, b
        host, adj = target(s); pats = set(); who = {}
        for i, p in enumerate(R.P):
            if len(p['deg']) > len(host) or not R.contains(host, adj, p): continue
            for e in R.allemb(host, adj, p, cap=100000):
                pt = tuple(sorted((t, dg) for t, dg in e.values() if t[0] == 'p')); pats.add(pt); who.setdefault(pt, p['name'])
        free = []
        for asg in itertools.product((5, 6, 7, 8, 9), repeat=6):
            A = dict(zip(PR, asg))
            if not any(all(A[t] == dg for t, dg in pt) for pt in pats): free.append(''.join(map(str, asg)))
        print('s1=%d s4=%d: %d RSST-free private completions of 15625 (order p1 p2a p2b p4a p4b p5; 9=9+); e.g. %s' %
              (a, b, len(free), ' '.join(free[:5])), flush=True)
        if a == 9 and b == 9 or (a, b) == (6, 6):
            mn = collections.Counter(); 
            for f in free:
                for k, c in enumerate(f): mn[(k, c)] += 1
            print('   letter counts among free:', dict(sorted(mn.items())))
