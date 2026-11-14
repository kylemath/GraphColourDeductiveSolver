"""Idea A: exact box-algebra normal form.
The charge a hub sends to a target is F = sum_w w*[part fits]; any part set with the same F is the
same discharging procedure. Exact moves: (1) identical boxes -> add weights; (2) two boxes of equal
weight that differ in ONE interval coordinate with adjacent disjoint intervals -> one box.
Greedy to a fixpoint, several random orders. Reports part count before/after, real vs null."""
import sys, random, collections as C
from common import *

def coords(box):
    hub, slots = box
    out = []
    for j, (sp, hat, fans) in enumerate(slots):
        out.append((j, 'sp')); out.append((j, 'hat'))
        for k in range(len(fans)): out.append((j, 'fan', k))
    return out

def get(box, c):
    s = box[1][c[0]]
    return s[0] if c[1] == 'sp' else s[1] if c[1] == 'hat' else s[2][c[2]]

def put(box, c, iv):
    hub, slots = box; slots = list(slots); sp, hat, fans = slots[c[0]]
    if c[1] == 'sp':
        if not (iv[0] == iv[1] and 6 <= iv[0] <= 8): fans = ()
        sp = iv
    elif c[1] == 'hat': hat = iv
    else: fans = fans[:c[2]] + (iv,) + fans[c[2] + 1:]
    slots[c[0]] = (sp, hat, fans)
    return (hub, tuple(slots))

def blank(box, c):
    """box with coordinate c wildcarded (key for finding merge partners)."""
    hub, slots = box; slots = list(slots); sp, hat, fans = slots[c[0]]
    if c[1] == 'sp':
        if any(f != FULL for f in fans): return None   # fan constraints pin the spoke degree
        slots[c[0]] = ('*', hat, ())
    elif c[1] == 'hat': slots[c[0]] = (sp, '*', fans)
    else: slots[c[0]] = (sp, hat, fans[:c[2]] + ('*',) + fans[c[2] + 1:])
    return (hub, tuple(slots), c)

def reduce(P, seed=0):
    rng = random.Random(seed)
    W = C.Counter()
    for p in P: W[norm(p)] += p['w']
    W = {b: w for b, w in W.items() if w != 0}
    n_dedup = len(W)
    changed = True
    while changed:
        changed = False
        idx = C.defaultdict(list)
        for b, w in W.items():
            for c in coords(b):
                k = blank(b, c)
                if k is not None: idx[(k, w)].append(b)
        keys = [k for k, v in idx.items() if len(v) > 1]
        rng.shuffle(keys)
        for k in keys:
            c = k[0][2]; w = k[1]
            live = [b for b in idx[k] if W.get(b) == w]
            live.sort(key=lambda b: get(b, c))
            i = 0
            while i + 1 < len(live):
                a, b = live[i], live[i + 1]
                ia, ib = get(a, c), get(b, c)
                if ia[1] + 1 == ib[0]:
                    m = put(a, c, (ia[0], ib[1]))
                    del W[a]; del W[b]
                    W[m] = W.get(m, 0) + w
                    if W[m] == 0: del W[m]
                    live[i + 1] = m if W.get(m) == w else None
                    changed = True
                    if live[i + 1] is None: i += 1
                i += 1
            
    return n_dedup, W

def literals(W):
    n = 0
    for b in W:
        for c in coords(b):
            if get(b, c) != FULL: n += 1
    return n

if __name__ == '__main__':
    P = load()
    for lab, Q in [('real', P)] + [(f'null{i}', q) for i, q in enumerate(nulls(P))]:
        best = None
        for seed in range(8 if lab == 'real' else 2):
            nd, W = reduce(Q, seed)
            if best is None or len(W) < len(best): best = W
        byt = C.Counter()
        print(lab, 'parts', len(Q), 'after dedup', nd, 'after exact merges', len(best),
              'literals', literals({norm(p): 1 for p in Q}), '->', literals(best),
              'weights', sorted(C.Counter(best.values()).items()))
        if lab == 'real':
            import pickle; pickle.dump(best, open('merged_real.pkl', 'wb'))
            print('  by hub', sorted(C.Counter(b[0] for b in best).items()))
    # per template
    for pre in ('drule', 'SP_', 'ST'):
        Q = [p for p in P if p['pre'].startswith(pre)]
        nd, W = reduce(Q, 0); print(pre, len(Q), nd, len(W))
