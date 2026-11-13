import sys, random; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W
W.init(); random.seed(3); n = 0; tot = [0, 0]
for it in range(3000):
    w = [random.choice([5, 5, 6, 7, 7, 8]) for _ in range(7)]; s = [random.choice([5, 5, 6, 7, 8, 9]) for _ in range(7)]
    p, g = W.kstar_terms(7, w, s); tot[0] += p; tot[1] += g
    if (p or g) and n < 6: n += 1; print(w, s, p, g)
print('pay slots', tot[0], 'payee slots', tot[1])
print(W.coef_of(('R', 7, (5, 5, 7, 5, 5, 7, 5), (7, 7, 7, 7, 7, 5, 7))))
