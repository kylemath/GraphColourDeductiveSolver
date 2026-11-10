#!/usr/bin/env python3
"""RSST-1SHOT full-world engine (spec §5 d = 5, 6 'no domains'; also used for a free-domain d = 7, 8 world).
Every link word (up to rotation + reflection; parts and containment are reflection-closed, spec §3.2/§7),
every apex word, every private letter in 5..9+.  Exhaustive branch-and-bound DFS over the variables that the
ledger reads (apexes s_i and privates p_i.k, values 5..9); unread variables are held at 9+ (the minimal
member, spec §8.2; for an unread apex this is the hardest row, so pass/fail over all rows is exact).
Pruning is sound: (1) hi upper bound = base + #in-fits not yet falsified - #out-fits already sure  <= 0;
(2) a configuration requirement already met by assigned letters kills every completion (monotonicity §7).
At a leaf every read variable is assigned, so hi is exact.  Survivors (hi > 0, not killed) are reported with
the unread apexes then enumerated to list the failing rows.

usage: fullworld.py D MODEL [shard nshard]     MODEL in {nokill, 582, 633}
  nokill: exact max hi over all fillings (branch-and-bound on the best value)
  582   : kills by proved configs only; leaves that only a 'none' config kills are listed (needs_none)
  633   : kills by all 633
"""
import sys, os, json, itertools, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcore as R
DOMINANCE = os.environ.get('DOMINANCE', '1') == '1'

def canon_links(d):
    seen = set()
    for wd in itertools.product((5, 6, 7, 8, 9), repeat=d):
        c = min(min(wd[r:] + wd[:r], (wd[r:] + wd[:r])[::-1]) for r in range(d))
        if c == wd and c not in seen:
            seen.add(c); yield list(c)

def var_order(d, link, names):
    def key(nm):
        if nm[0] == 's': return (int(nm[1:]), 0, 0)
        a, b = nm[1:].split('.'); a = int(a)
        return (a, 1, int(b))
    return sorted(names, key=key)

class Link:
    def __init__(self, d, link):
        self.d = d; self.link = link; self.base = 10 * (6 - d)
        self.W = R.Window(d, link, None)
        self.insts = R.instances(self.W)
        names = set(nm for I in self.insts for nm in I['conds'])
        self.vars = var_order(d, link, names)
        self.pos = {nm: k for k, nm in enumerate(self.vars)}
        self.allvars = sorted(set(R.window_hostgraph(self.W)[2].values()))
        # static bound: every in-fit possible, out-fits sure only if unconditional & not open
        self.ub0 = self.base + sum(1 for I in self.insts if I['dir'] > 0) - sum(1 for I in self.insts if I['dir'] < 0 and not I['conds'] and not I['open'])
        self._reqs = None

    def reqs(self):
        if self._reqs is None: self._reqs = R.requirements(self.W)
        return self._reqs

def dfs(L, model, best=None, on_leaf=None):
    """model: 'nokill' | '582' | '633'. Returns (max_hi_seen_at_leaves, leaves list for survivors)."""
    insts = L.insts; nv = len(L.vars)
    by_var = [[] for _ in range(nv)]
    rem = []; dead = [False] * len(insts)
    ub = L.base
    for t, I in enumerate(insts):
        rem.append(len(I['conds']))
        for nm, iv in I['conds'].items(): by_var[L.pos[nm]].append((t, iv))
        if I['dir'] > 0: ub += 1
        elif rem[t] == 0 and not I['open']: ub -= 1
    # requirements by last read variable; requirements on unread variables can never hold (they are 9+)
    kreq = [[] for _ in range(nv)]; kill0 = False; none0 = []
    if model != 'nokill':
        for ci, rl in L.reqs().items():
            p = R.CONFIGS[ci]
            if model == '582' and not p['proved']: continue
            for r in rl:
                if any(nm not in L.pos for nm, _ in r): continue
                if not r: kill0 = True; break
                last = max(L.pos[nm] for nm, _ in r)
                kreq[last].append(([(L.pos[nm], v) for nm, v in r], ci))
            if kill0: break
    if kill0: return None, [], 0
    # dominance (spec §13 A.3.2): a letter whose truth pattern on the variable's conditions equals 9's gives the
    # same charge and only adds a host, so it never beats 9.  DOMINANCE=0 disables it.
    doms = []
    for k in range(nv):
        ivs = [iv for t, iv in by_var[k]]
        pat = lambda a: tuple(lo_ <= a <= hi_ for lo_, hi_ in ivs)
        doms.append([9] + [a for a in (5, 6, 7, 8) if pat(a) != pat(9)] if DOMINANCE else [5, 6, 7, 8, 9])
    val = [9] * nv
    out = []; state = {'best': best if best is not None else -10 ** 9, 'nodes': 0, 'maxleaf': None}
    def rec(k, ub):
        state['nodes'] += 1
        if model == 'nokill':
            if ub <= state['best']: return
        elif ub <= 0: return
        if k == nv:
            if state['maxleaf'] is None or ub > state['maxleaf']: state['maxleaf'] = ub
            if model == 'nokill': state['best'] = max(state['best'], ub); out.append((ub, list(val)))
            else: out.append((ub, list(val)))
            return
        for v in doms[k]:
            val[k] = v
            if model != 'nokill' and v <= 8:
                if any(all(val[q] == x for q, x in rq) for rq, ci in kreq[k]): continue
            nub = ub; changed = []
            for t, (a, b) in by_var[k]:
                if dead[t]: continue
                I = insts[t]
                if not (a <= v <= b):
                    dead[t] = True; changed.append((t, 'd'))
                    if I['dir'] > 0: nub -= 1
                else:
                    rem[t] -= 1; changed.append((t, 'r'))
                    if I['dir'] < 0 and rem[t] == 0 and not I['open']: nub -= 1
            rec(k + 1, nub)
            for t, c in changed:
                if c == 'd': dead[t] = False
                else: rem[t] += 1
        val[k] = 9
    rec(0, ub)
    return state['maxleaf'], out, state['nodes']

def leaf_fill(L, vals):
    return {nm: v for nm, v in zip(L.vars, vals)}

def ftext(L, f):
    s = ' '.join('%s=%d' % (nm, f[nm]) for nm in L.vars if f.get(nm, 9) != 9)
    return s or '(all read letters 9+)'

def main():
    d = int(sys.argv[1]); model = sys.argv[2]
    shard, nshard = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 1)
    job = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    tagc = ('_' + R.CONTROL) if R.CONTROL else ''
    outp = os.path.join(job, 'logs', 'fw_d%d_%s_%dof%d%s.jsonl' % (d, model, shard, nshard, tagc))
    fo = open(outp, 'w'); t0 = time.time()
    stats = collections.Counter(); best = None; bestrow = None
    for li, link in enumerate(canon_links(d)):
        if li % nshard != shard: continue
        L = Link(d, link); stats['links'] += 1
        if L.ub0 <= 0: stats['links_ub0_le0'] += 1; continue
        stats['links_ub0_pos'] += 1
        if model == 'nokill':
            mx, leaves, nodes = dfs(L, 'nokill', best=0)
            stats['nodes'] += nodes
            if mx is not None and mx > 0:
                stats['links_pos'] += 1
                top = max(leaves)
                if best is None or top[0] > best:
                    best = top[0]; bestrow = (''.join(map(str, link)), ftext(L, leaf_fill(L, top[1])))
                fo.write(json.dumps({'link': ''.join(map(str, link)), 'max_hi': top[0], 'argmax': ftext(L, leaf_fill(L, top[1]))}) + '\n')
            continue
        mx, leaves, nodes = dfs(L, model)
        stats['nodes'] += nodes
        for hi, vals in leaves:
            f = leaf_fill(L, vals)
            full = {nm: f.get(nm, 9) for nm in L.allvars}
            c = R.contained(L.reqs(), full)
            rec = {'link': ''.join(map(str, link)), 'hi': hi, 'filling': ftext(L, f)}
            if model == '582' and c:
                # killed only by 'none' configurations (proved ones were pruned)
                assert not any(R.CONFIGS[i]['proved'] for i in c)
                rec['needs_none'] = sorted(R.CONFIGS[i]['name'] for i in c); stats['leaves_need_none'] += 1
            else:
                assert not c or model == '582'
                # survivor: enumerate unread apexes to list failing rows
                unread = [i for i in range(d) if 's%d' % i not in L.pos]
                bad_rows = 0
                for combo in itertools.product((5, 6, 7, 8, 9), repeat=len(unread)):
                    g = dict(full)
                    for i, a in zip(unread, combo): g['s%d' % i] = a
                    cc = [z for z in R.contained(L.reqs(), g) if model == '633' or R.CONFIGS[z]['proved']]
                    if not cc: bad_rows += 1
                rec['survivor'] = True; rec['unread_apexes'] = unread; rec['surviving_apex_completions'] = bad_rows
                stats['survivors'] += 1
            fo.write(json.dumps(rec) + '\n')
        fo.flush()
    summ = {'d': d, 'model': model, 'shard': shard, 'nshard': nshard, 'stats': dict(stats), 'max_hi': best, 'argmax': bestrow,
            'secs': round(time.time() - t0, 1), 'control': R.CONTROL}
    fo.write(json.dumps({'summary': summ}) + '\n'); fo.close()
    print(json.dumps(summ))

if __name__ == '__main__':
    main()
