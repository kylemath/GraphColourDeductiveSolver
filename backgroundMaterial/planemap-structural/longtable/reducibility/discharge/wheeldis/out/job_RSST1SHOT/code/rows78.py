#!/usr/bin/env python3
"""RSST-1SHOT d = 7 / 8 row engine (spec §5, §8.1, §8.2, §9). Grouping by relevant privates, exact
multiplicities, numpy evaluation of lo/hi on the group grid, kills by minimal-member combinations using
precomputed embedding requirements (rcore.requirements)."""
import sys, os, json, itertools, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rcore as R

GMAX = 4 * 10 ** 6
CMAX = 64

def site_options(d, link, sword, j, pairs):
    """-> list of (assignment dict var->letter over this site's privates, multiplicity, display dict)."""
    L = link[j]; out = []
    if L == 5:
        return [({}, 1)] if pairs else []
    for x, y in pairs:
        if L == 6:
            assert x == y; out.append(({'p%d.1' % j: x}, 1))
        elif L == 7:
            out.append(({'p%d.1' % j: y, 'p%d.2' % j: x}, 1))
        elif L == 8:
            for m in (5, 6, 7, 8, 9):
                out.append(({'p%d.1' % j: y, 'p%d.2' % j: m, 'p%d.3' % j: x}, 1))
        else:   # 9+: middle held at 9+, counted as 5 values
            out.append(({'p%d.1' % j: y, 'p%d.2' % j: 9, 'p%d.3' % j: x}, 5))
    return out

def fill_text(link, f):
    parts = []
    for j, L in enumerate(link):
        g = lambda k: f.get('p%d.%d' % (j, k), 9)
        if L == 5: continue
        if L == 6: parts.append('p%d=%d' % (j, g(1)))
        elif L == 7: parts.append('x%d=%d,y%d=%d' % (j, g(2), j, g(1)))
        elif L == 8: parts.append('x%d=%d,m%d=%d,y%d=%d' % (j, g(3), j, g(2), j, g(1)))
        else: parts.append('x%d=%d,y%d=%d' % (j, g(3), j, g(1)))
    return ' '.join(parts)

def site_vars(link, j):
    return ['p%d.%d' % (j, k) for k in range(1, R.npriv(link[j]) + 1)]

def full_privates(link, f):
    out = {}
    for j in range(len(link)):
        for nm in site_vars(link, j): out[nm] = f.get(nm, 9)
    return out

class Row:
    def __init__(self, label, dom):
        d, lk, sw = label.split(); self.d = d = int(d)
        self.link = [int(c) for c in lk]; self.sword = [int(c) for c in sw]; self.label = label
        self.W = R.Window(d, self.link, self.sword)
        self.insts = R.instances(self.W)
        self.rel = sorted(set(nm for I in self.insts for nm in I['conds']))
        self.opts = [site_options(d, self.link, self.sword, j, dom[j]) for j in range(d)]
        self.dom = dom
        self._reqs = None

    @property
    def reqs(self):
        if self._reqs is None: self._reqs = R.requirements(self.W)
        return self._reqs

    def classes(self):
        """per site: list of classes; class = (projection dict, size, members list of assignment dicts)."""
        rel = set(self.rel); out = []
        for j in range(self.d):
            cl = collections.OrderedDict()
            for a, m in self.opts[j]:
                key = tuple(sorted((k, v) for k, v in a.items() if k in rel))
                if key not in cl: cl[key] = [dict(key), 0, []]
                cl[key][1] += m; cl[key][2].append(a)
            out.append(list(cl.values()))
        return out

def kill_group(row, members_per_site, ci_filter):
    """members_per_site: list of member lists (assignment dicts). Returns (killed_dict{model:bool}, ncomb, configs set, inexact)."""
    row._last_needed = []
    mins = []
    for mem in members_per_site:
        hs = []
        for a in mem:
            h = frozenset((k, v) for k, v in a.items() if v <= 8)
            if h not in hs: hs.append(h)
        mn = [h for h in hs if not any(o < h for o in hs)]
        mins.append(mn)
    ncomb = 1
    for m in mins: ncomb *= len(m)
    if ncomb > CMAX:
        return {'633': False, '582': False}, ncomb, set(), True
    k633 = True; k582 = True; used = set(); needed = []
    for comb in itertools.product(*mins):
        f = {}
        for h in comb: f.update(h)
        c = R.contained(row.reqs, f)
        used |= set(c)
        if not c: k633 = False
        if not any(R.CONFIGS[i]['proved'] for i in c):
            k582 = False
            if c: needed.append(sorted(R.CONFIGS[i]['name'] for i in c))
        if not k633 and not k582: break
    row._last_needed = needed
    return {'633': k633, '582': k582}, ncomb, used, False

def run_row(label, dom, kill_all=False, keep_pos=400, need_log=None):
    row = Row(label, dom)
    d = row.d; base = 10 * (6 - d)
    res = {'label': label, 'n_inst': len(row.insts), 'relevant': len(row.rel),
           'rel_8mid': sum(1 for nm in row.rel if row.link[int(nm[1:].split('.')[0])] == 8 and nm.endswith('.2'))}
    if any(len(o) == 0 for o in row.opts):
        res.update({'status': 'empty_domain', 'n_fill': 0, 'n_groups': 0}); return res, row
    cls = row.classes()
    shape = tuple(len(c) for c in cls)
    G = int(np.prod(shape, dtype=np.int64))
    res['n_fill'] = int(np.prod([sum(c[1] for c in cs) for cs in cls], dtype=object))
    res['n_groups'] = G
    if G > GMAX:
        res['status'] = 'not done'; return res, row
    res['status'] = 'done'
    # weights
    wt = np.ones(shape, dtype=np.int64)
    for j, cs in enumerate(cls):
        v = np.array([c[1] for c in cs], dtype=np.int64); sh = [1] * d; sh[j] = len(cs)
        wt = wt * v.reshape(sh)
    lo = np.full(shape, base, dtype=np.int32); hi = np.full(shape, base, dtype=np.int32)
    site_of = lambda nm: int(nm[1:].split('.')[0])
    for I in row.insts:
        h = np.ones(shape, dtype=bool)
        for nm, (a, b) in I['conds'].items():
            j = site_of(nm)
            v = np.array([a <= c[0][nm] <= b for c in cls[j]]); sh = [1] * d; sh[j] = len(cls[j])
            h = h & v.reshape(sh)
        sure = h & (not I['open'])
        if I['dir'] > 0: hi += h; lo += sure
        else: lo -= h; hi -= sure
    def rep(idx):
        f = {}
        for j, k in enumerate(idx): f.update(cls[j][k][0])
        return f
    def argmax(arr, mask=None):
        a = arr if mask is None else np.where(mask, arr, np.iinfo(np.int32).min)
        if mask is not None and not mask.any(): return None, None
        k = int(np.argmax(a)); idx = np.unravel_index(k, shape)
        return int(arr[idx]), idx
    res['lo_max'], ilo = argmax(lo); res['hi_max'], ihi = argmax(hi)
    res['argmax_lo'] = R_fill(row, rep(ilo)); res['argmax_hi'] = R_fill(row, rep(ihi))
    res['fills_lo_pos'] = int(wt[lo > 0].sum()); res['fills_hi_pos'] = int(wt[hi > 0].sum())
    res['groups_lo_pos'] = int((lo > 0).sum()); res['groups_hi_pos'] = int((hi > 0).sum())
    # diagnostic only (NOT the spec convention): multiplicity taken over sites that hold a relevant private
    relsites = set(int(nm[1:].split('.')[0]) for nm in row.rel)
    wr = np.ones(shape, dtype=np.int64)
    for j, cs in enumerate(cls):
        if j not in relsites: continue
        v = np.array([c[1] for c in cs], dtype=np.int64); sh = [1] * d; sh[j] = len(cs)
        wr = wr * v.reshape(sh)
    row._wr = wr
    res['diag_relsites_fills_lo_pos'] = int(wr[lo > 0].sum()); res['diag_relsites_fills_hi_pos'] = int(wr[hi > 0].sum())
    # kills on groups with hi > 0 (spec §8.3/§9)
    kept633 = np.ones(shape, dtype=bool); kept582 = np.ones(shape, dtype=bool)
    pos = np.argwhere(hi > 0)
    inexact = 0; killed = 0; killed_p = 0; cfg_used = collections.Counter(); positives = []
    checked = {}; row._last_needed_by = {}
    def check(idx):
        idx = tuple(int(z) for z in idx)
        if idx in checked: return checked[idx]
        mem = [cls[j][k][2] for j, k in enumerate(idx)]
        kd, ncomb, used, inex = kill_group(row, mem, None)
        row._last_needed_by[idx] = getattr(row, '_last_needed', [])
        checked[idx] = (kd, ncomb, used, inex); return checked[idx]
    for idx in pos:
        idx = tuple(int(z) for z in idx)
        kd, ncomb, used, inex = check(idx)
        inexact += inex
        if kd['633']: killed += 1; kept633[idx] = False
        if kd['582']: killed_p += 1; kept582[idx] = False
        if kd['633'] or kd['582']:
            for c in used: cfg_used[R.CONFIGS[c]['name']] += 1
        if len(positives) < keep_pos:
            positives.append({'filling': R_fill(row, rep(idx)), 'lo': int(lo[idx]), 'hi': int(hi[idx]), 'fills': int(wt[idx]),
                              'killed': kd['633'], 'killed_proved': kd['582'], 'minimal_combinations': ncomb,
                              'configs': [[R.CONFIGS[c]['name'], R.CONFIGS[c]['verdict']] for c in sorted(used)]})
        if need_log is not None and kd['633'] and not kd['582']:
            # filling needs a 'none' config: record which none configs cover it
            need_log.append({'label': label, 'filling': R_fill(row, rep(idx)), 'hi': int(hi[idx]), 'fills': int(wt[idx]),
                             'minimal_combinations': ncomb,
                             'none_sets_per_uncovered_combination': row._last_needed_by[idx]})
    res.update({'groups_hi_pos_killed': killed, 'groups_hi_pos_kept': int(len(pos) - killed), 'inexact_groups': inexact,
                'groups_hi_pos_killed_proved': killed_p})
    for tag, kept in (('', kept633), ('_proved', kept582)):
        a, ia = argmax(lo, kept); b, ib = argmax(hi, kept)
        res['lo_max_after' + tag] = a; res['hi_max_after' + tag] = b
        res['argmax_lo_after' + tag] = R_fill(row, rep(ia)) if ia is not None else None
        res['argmax_hi_after' + tag] = R_fill(row, rep(ib)) if ib is not None else None
        res['fills_lo_pos_after' + tag] = int(wt[(lo > 0) & kept].sum()); res['fills_hi_pos_after' + tag] = int(wt[(hi > 0) & kept].sum())
        res['diag_relsites_fills_hi_pos_after' + tag] = int(row._wr[(hi > 0) & kept].sum())
    if kill_all:
        # coordinator addendum B: kill-check every group; lazily, in descending order, until the first kept group
        for tag, model in (('', '633'), ('_proved', '582')):
            for which, arr in (('lo', lo), ('hi', hi)):
                flat = arr.reshape(-1); order = np.lexsort((np.arange(flat.size), -flat))
                got = None
                for k in order:
                    idx = np.unravel_index(int(k), shape)
                    kd = check(idx)[0]
                    if not kd[model]: got = idx; break
                res['%s_max_after%s_allkill' % (which, tag)] = int(arr[got]) if got is not None else None
                res['argmax_%s_after%s_allkill' % (which, tag)] = R_fill(row, rep(got)) if got is not None else None
    res['configs_used'] = dict(cfg_used); res['positives'] = positives
    row._cls = cls; row._lo = lo; row._hi = hi
    return res, row

def R_fill(row, f): return fill_text(row.link, f)
