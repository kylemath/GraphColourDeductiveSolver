import pickle, collections as C, numpy as np, random, sys
rows = pickle.load(open('overflow_rows.pkl', 'rb'))
random.seed(3)
def show(r):
    return ' '.join(f"{r['link'][i]}{'*' if r['spo'][i]==6 else '+' if r['spo'][i]==3 else '#' if r['spo'][i] else ''}" + (f"({r['et'][i]:.0f})" if r['link'][i] >= 7 and r['et'][i] is not None else '') for i in range(r['d']))
for r in random.sample(rows, 30): print(r['d'], 'c=', r['c_hi'], '|', show(r))
# geometry of two-target pushes: cyclic distance between the two targets, and local context
dist = C.Counter(); ctx = C.Counter(); ctx1 = C.Counter()
for r in rows:
    d = r['d']; T = [i for i in range(d) if r['spo'][i]]
    L = r['link']
    for i in T:
        a, b = sorted((L[(i - 1) % d], L[(i + 1) % d]))
        (ctx if len(T) == 2 else ctx1)[(L[i], a, b)] += 1
    if len(T) == 2:
        k = (T[1] - T[0]) % d; dist[(d, min(k, d - k))] += 1
print('two-target distance (hub, cyclic gap):', sorted(dist.items()))
print('two-target ctx (target, nbrs):', ctx.most_common(12))
print('one-target ctx:', ctx1.most_common(12))
# which >=7 spokes are NOT chosen: context
no = C.Counter(); yes = C.Counter()
for r in rows:
    d = r['d']; L = r['link']
    for i in range(d):
        if L[i] >= 7:
            a, b = sorted((L[(i - 1) % d], L[(i + 1) % d]))
            n5 = (a == 5) + (b == 5)
            key = (min(L[i], 9), n5)
            (yes if r['spo'][i] else no)[key] += 1
print('chosen vs not by (target degree, number of 5s among its two hub-side neighbours):')
for k in sorted(set(yes) | set(no)): print('  ', k, 'chosen', yes[k], 'not', no[k])
# slack threshold
ch = [r['et'][i] for r in rows for i in range(r['d']) if r['spo'][i] and r['et'][i] is not None]
nc = [r['et'][i] for r in rows for i in range(r['d']) if not r['spo'][i] and r['link'][i] in (7, 8) and r['et'][i] is not None]
print('expected RSST charge of chosen targets pct', np.percentile(ch, [5, 25, 50, 75, 95]).round(1), ' of non-chosen 7/8 spokes', np.percentile(nc, [5, 25, 50, 75, 95]).round(1), len(ch), len(nc))
