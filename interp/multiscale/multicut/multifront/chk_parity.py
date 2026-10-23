import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.')
import mf, collections
spec = sys.argv[1]; name, m, seed = spec.split(':')[:3]
adj = mf.mkmap(name); I = mf.MF(adj, int(m), int(seed), ren=True, mb=2)
orig = I.commit; stats = collections.Counter()
def commit(ctx, newcol, tagv):
    out = orig(ctx, newcol, tagv)
    for w in ctx['W']:
        Wset = set(w['V']); V = w['V']; L = len(V); st = None
        for j in range(L):
            a, u = V[(j-1) % L], V[j]; ru = I.rot[u]; z = ru[(I.ix[u][a] + 1) % len(ru)]
            if not I.present[z]: st = z; break
        seen = {st}; q = [st]
        while q:
            x = q.pop()
            for y in adj[x]:
                if y not in Wset and y not in seen: seen.add(y); q.append(y)
        oddD = sum(1 for x in seen if len(adj[x]) % 2); onW = sum(1 for x in set(w['V']) if len(adj[x]) % 2)
        simple = len(set(w['V'])) == len(w['V'])
        stats[(simple, (oddD + onW) % 2 == int(w['odd']))] += 1
    return out
I.commit = commit
k = sum(I.present); n = len(adj)
while k < n:
    prog = False
    for tg in range(int(m)):
        r = I.turn(tg, k)
        if r not in (None, 'none'): k += 1; prog = True
    if not prog: break
print(spec, k, n, dict(stats))
