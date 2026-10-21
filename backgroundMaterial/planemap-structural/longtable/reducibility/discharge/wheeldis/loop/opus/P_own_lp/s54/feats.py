# s54 feats.py: generic feature models for the discharging-rule families (raw letters / key positions only).
# A model maps a family key (engine format) to {feature: coefficient}; the weight is w[key] = sum_f theta_f * phi_f(key).
# Keys (RELAY_SPEC 2, 12.2):  y (D,a,b,c,d) reflection (D,d,c,b,a) ; g (n1,h,f,h',n5,ar,al) reflection (n5,h',f,h,n1,al,ar)
#   h (m0..m5, ar, al) reflection (m0,m5..m1,al,ar) ; x tau int ; r h5key(sx, sy) ; lq (c,a,a2) / (V,c,a,a2).
# Every model is symmetric under the key's reflection (positions paired), so it is well defined on canonical keys.
import collections

def _c(*items):
    out = collections.Counter()
    for f in items:
        if f is not None: out[f] += 1
    return dict(out)

# ---------- y: five -> big neighbour of degree D; abcd = five's link from the big (a, d flank the big) ----------
def y_D(k): D, a, b, c, d = k; return _c(('D', D))
def y_cnt(k): D, a, b, c, d = k; return _c(('D', D), ('L', a), ('L', b), ('L', c), ('L', d))
def y_cntD(k): D, a, b, c, d = k; return _c(('D', D), ('L', D, a), ('L', D, b), ('L', D, c), ('L', D, d))
def y_add(k): D, a, b, c, d = k; return _c(('D', D), ('F', a), ('F', d), ('N', b), ('N', c))
def y_addD(k): D, a, b, c, d = k; return _c(('D', D), ('F', D, a), ('F', D, d), ('N', D, b), ('N', D, c))
def y_pair(k):
    D, a, b, c, d = k; f = y_addD(k); f = collections.Counter(f)
    f[('FN', a, b)] += 1; f[('FN', d, c)] += 1; f[('NN',) + tuple(sorted((b, c)))] += 1; f[('FF',) + tuple(sorted((a, d)))] += 1
    return dict(f)
def y_pairD(k):
    D, a, b, c, d = k; f = collections.Counter(y_addD(k))
    f[('FN', D, a, b)] += 1; f[('FN', D, d, c)] += 1; f[('NN', D) + tuple(sorted((b, c)))] += 1; f[('FF', D) + tuple(sorted((a, d)))] += 1
    return dict(f)
def y_full(k): return {('K',) + tuple(k): 1}

# ---------- g: five -> 6.  n1, n5 exact spokes beside the 6; h, f, h' classes 0/1 (hat, fan, hat); ar, al apex classes 5/7 ----------
def g_const(k): return {('c',): 1}
def g_add(k):
    n1, h1, f, h2, n5, ar, al = k
    return _c(('c',), ('S', n1), ('S', n5), ('H', h1), ('H', h2), ('F', f), ('A', ar), ('A', al))
def g_pair(k):
    n1, h1, f, h2, n5, ar, al = k; o = collections.Counter(g_add(k))
    o[('AS', ar, n1)] += 1; o[('AS', al, n5)] += 1; o[('SH', n1, h1)] += 1; o[('SH', n5, h2)] += 1
    o[('HF', h1, f)] += 1; o[('HF', h2, f)] += 1; o[('SS',) + tuple(sorted((n1, n5)))] += 1
    return dict(o)
def g_full(k): return {('K',) + tuple(k): 1}

# ---------- h: 6 -> big.  m0 = big's letter, m1..m5 the 6's link from the big, ar (beyond m0 m1), al (beyond m5 m0) apex classes ----------
def h_D(k): return _c(('D', k[0]))
def h_nf(k): return _c(('D', k[0], sum(1 for l in k[1:6] if l == 5)))     # big's letter x number of fives in the 6's link
def h_add(k):
    m0, m1, m2, m3, m4, m5, ar, al = k
    return _c(('D', m0), ('S', m1), ('S', m5), ('T', m2), ('T', m4), ('O', m3), ('A', ar), ('A', al))
def h_addD(k):
    m0, m1, m2, m3, m4, m5, ar, al = k
    return _c(('D', m0), ('S', m0, m1), ('S', m0, m5), ('T', m0, m2), ('T', m0, m4), ('O', m0, m3), ('A', m0, ar), ('A', m0, al))
def h_pair(k):
    m0, m1, m2, m3, m4, m5, ar, al = k; o = collections.Counter(h_addD(k))
    o[('AS', ar, m1)] += 1; o[('AS', al, m5)] += 1; o[('ST', m1, m2)] += 1; o[('ST', m5, m4)] += 1; o[('TO', m2, m3)] += 1; o[('TO', m4, m3)] += 1
    return dict(o)
def h_full(k): return {('K',) + tuple(k): 1}

# ---------- x: big fl -> big tl.  two sides (c, a, b), c common neighbour, a its other common nbr with fl, b with tl ----------
def x_dec(t):
    hi = t % 125; lo = (t // 125) % 125; fi, ti = divmod(t // 15625, 3)
    sd = lambda s: (5 + s // 25, 5 + (s // 5) % 5, 5 + s % 5)
    return 7 + fi, 7 + ti, sd(lo), sd(hi)
def x_FT(k): fl, tl, s1, s2 = x_dec(k); return _c(('FT', fl, tl))
def x_add(k):
    fl, tl, s1, s2 = x_dec(k)
    return _c(('FT', fl, tl), ('C', s1[0]), ('C', s2[0]), ('A', s1[1]), ('A', s2[1]), ('B', s1[2]), ('B', s2[2]))
def x_side(k):
    fl, tl, s1, s2 = x_dec(k); return _c(('FT', fl, tl), ('s',) + s1, ('s',) + s2)
def x_full(k): return {('K', k): 1}

# ---------- r: big hat -> five (hat5).  key = two sides, each (x,) for a big spoke, (5, cls, letter) or (6, cls, cls) ----------
def r_split(k):
    n = len(k); first = 1 if k[0] >= 7 else 3; return tuple(k[:first]), tuple(k[first:])
def r_const(k): return {('c',): 1}
def r_type(k): a, b = r_split(k); return _c(('T',) + tuple(sorted((a[0], b[0]))))
def r_side(k): a, b = r_split(k); return _c(('c',), ('s',) + a, ('s',) + b)
def r_full(k): return {('K',) + tuple(k): 1}

def lq_const(k): return {('c', len(k)): 1}
def lq_full(k): return {('K',) + tuple(k): 1}

def zero(k): return {}

FEATS = {
    'y': {'D': y_D, 'cnt': y_cnt, 'cntD': y_cntD, 'add': y_add, 'addD': y_addD, 'pair': y_pair, 'pairD': y_pairD, 'full': y_full, 'zero': zero},
    'g': {'const': g_const, 'add': g_add, 'pair': g_pair, 'full': g_full, 'zero': zero},
    'h': {'D': h_D, 'nf': h_nf, 'add': h_add, 'addD': h_addD, 'pair': h_pair, 'full': h_full, 'zero': zero},
    'x': {'FT': x_FT, 'add': x_add, 'side': x_side, 'full': x_full, 'zero': zero},
    'r': {'const': r_const, 'type': r_type, 'side': r_side, 'full': r_full, 'zero': zero},
    'lq': {'const': lq_const, 'full': lq_full, 'zero': zero},
}
# leaf models (decision-tree partitions fitted elsewhere) are registered at run time: FEATS[fam]['tree:<file>']
def tree_model(fn):
    import json
    T = json.load(open(fn))   # {"family": f, "leaves": {"<repr key>": leaf_id}} ; unknown keys -> leaf "other"
    m = {tuple(json.loads(k)) if k.startswith('[') else int(k): v for k, v in T['leaves'].items()}
    return lambda k: {('leaf', m.get(k if not isinstance(k, tuple) else tuple(k), 'other')): 1}
def x_sideFT(k):
    fl, tl, s1, s2 = x_dec(k); return _c(('s', fl, tl) + s1, ('s', fl, tl) + s2)
FEATS['x']['sideFT'] = x_sideFT
# dictionaries for the lasso path: the union of a family's models, each feature tagged with its model name
DICT = {'y': ('D', 'addD', 'pairD', 'full'), 'g': ('const', 'add', 'pair', 'full'), 'h': ('D', 'addD', 'pair', 'full'),
        'x': ('FT', 'side', 'sideFT'), 'r': ('const', 'type', 'side', 'full'), 'lq': ('const', 'full')}
def dict_model(fam, parts=None):
    fs = [(m, FEATS[fam][m]) for m in (parts or DICT[fam])]
    def f(k):
        out = {}
        for m, fn in fs:
            for q, c in fn(k).items(): out[(m,) + tuple(q)] = c
        return out
    return f
def sup_model(fam, fn):
    import json
    S = json.load(open(fn)); keep = {eval(q) for q in S[fam]}   # feature reprs per family
    base = dict_model(fam, S.get('parts', {}).get(fam))
    return lambda k: {q: c for q, c in base(k).items() if q in keep}
def model(fam, name):
    if name.startswith('tree:'): return tree_model(name[5:])
    if name == 'dict': return dict_model(fam)
    if name.startswith('sup:'): return sup_model(fam, name[4:])
    return FEATS[fam][name]
