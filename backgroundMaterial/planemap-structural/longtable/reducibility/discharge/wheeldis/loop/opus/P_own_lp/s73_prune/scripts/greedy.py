# usage: greedy.py CANDFILE CURRENT_SET.json OUT_SET.json [k]   greedy set cover of violated rows (each covered >= k times)
import sys, json, heapq, collections
cf, cur, out = sys.argv[1:4]; k = int(sys.argv[4]) if len(sys.argv) > 4 else 1
cur = set(json.load(open(cur))); rows = []; byr = collections.defaultdict(list); nocand = 0
for l in open(cf):
    p = l.split()
    c = [int(x) for x in p[4].split(',')] if len(p) > 4 and p[4] else []
    c = [x for x in c if x not in cur]
    if not c: nocand += 1; continue
    i = len(rows); rows.append(c)
    for x in c: byr[x].append(i)
need = [k] * len(rows); print('rows', len(rows), 'no-candidate rows', nocand, 'candidate rules', len(byr))
cnt = {x: len(v) for x, v in byr.items()}; h = [(-c, x) for x, c in cnt.items()]; heapq.heapify(h)
chosen = []; left = len(rows)
while left and h:
    c, x = heapq.heappop(h)
    if cnt[x] != -c: 
        if cnt[x] > 0: heapq.heappush(h, (-cnt[x], x))
        continue
    chosen.append(x)
    for i in byr[x]:
        if need[i] > 0:
            need[i] -= 1
            if need[i] == 0:
                left -= 1
                for y in rows[i]:
                    if y != x: cnt[y] -= 1
    cnt[x] = 0
    if len(chosen) % 200 == 0: print(len(chosen), left, flush=True)
print('chosen', len(chosen), 'uncovered', left)
json.dump(sorted(cur | set(chosen)), open(out, 'w'))
