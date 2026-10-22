"""Q1 extras: (i) explicit pairwise form 3(X_a-X_b) = sigma(c->d;a)*delta(c->d), {c,d} = complement of {a,b},
sigma(c->d;a) = +1 iff (c^a) == (c^d)%3+1 ; (ii) per-face boundary law N(F_acd)-N(F_bcd) = same;
(iii) Kempe swap: vertices inside a swapped chain flip spin sign (and swap class)."""
import sys, random, collections
sys.path.insert(0, '/mnt/project-files/multiscale/spin_windows')
from spinlib import *
from q1_verify_lib import cap_disc
def sig(c, d, a): return 1 if (c ^ a) == (c ^ d) % 3 + 1 else -1
bad = 0; tests = 0; facebad = 0; kempe = collections.Counter()
for seed in range(60):
    d = cap_disc(random.Random(seed).choice([150, 300, 600]), 5000 + seed, random.Random(seed).uniform(-0.2, 0.6))
    if d is None: continue
    adj, r = d; rot, succ = embed_disc(adj, r); n = len(adj)
    for col in sat_colourings(adj, k=3, seed=seed):
        X3 = [0] * 4
        for v in range(r, n): X3[col[v]] += 3 * spin(col, rot, v)
        for v in range(r): X3[col[v]] += fan_turn(col, rot, v)
        D = flux([col[v] for v in ring_word(succ, r)])
        N = collections.Counter()
        for t in triangles(adj, rot, r): N[frozenset(col[x] for x in t)] += orient_sign(col, rot, t)
        for a in range(4):
            for b in range(4):
                if a == b: continue
                c, dd = [x for x in range(4) if x not in (a, b)]
                tests += 1; bad += (X3[a] - X3[b] != sig(c, dd, a) * D[c][dd])
                facebad += (N[frozenset((a, c, dd))] - N[frozenset((b, c, dd))] != sig(c, dd, a) * D[c][dd])
        # Kempe: pick a random (a,b) chain among interior vertices not touching ring, swap, compare spins
        a, b = random.Random(seed).sample(range(4), 2)
        for start in range(r, n):
            if col[start] not in (a, b): continue
            comp = {start}; st = [start]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y not in comp and col[y] in (a, b): comp.add(y); st.append(y)
            if any(x < r for x in comp): continue
            new = list(col)
            for x in comp: new[x] = a ^ b ^ col[x]
            for x in range(r, n):
                w0, w1 = spin(col, rot, x), spin(new, rot, x)
                if x in comp: kempe['in_chain_flip' if w1 == -w0 else 'in_chain_other'] += 1
                elif any(y in comp for y in adj[x]): kempe['adjacent_same' if w1 == w0 else 'adjacent_changed'] += 1
            break
print('pairwise explicit law: %d/%d mismatches; per-face law mismatches %d' % (bad, tests, facebad))
print('Kempe swap of an interior chain:', dict(kempe))
