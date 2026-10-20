"""s39o: rpatN non-vacuity / oracle check.  Loads the engine (eng/pcheck.py, no command) with ONLY rpatN=FILE as patterns (no
registry, no rpatD), runs admissible() on the 45 A67 binders (k55/rows45_A67.txt) and compares with explore's hit sites
(k55/sites55_rows45_A67.txt): a row must be killed by pattern iff the sites file lists an embedding through u ('u ' line) of a
2026-set configuration.  Also counts, per (row, configuration), the u-embeddings of rpatN_build's own enumerator on the concrete row
against the sites file count.
usage: python3 rpatN_check.py RPATN [root=DIR]"""
import sys, os, re, collections
H = os.path.dirname(os.path.abspath(__file__))
RP = sys.argv[1]; extra = sys.argv[2:]
sys.argv = [os.path.join(H, 'eng', 'pcheck.py'), 'none', 'rpatN=' + RP] + extra
ns = {'__file__': sys.argv[0], '__name__': 'pcheck_lib'}
exec(open(sys.argv[0]).read().replace("}.get(CMD, lambda: print(__doc__))()", "}.get(CMD, lambda: None)()"), ns)
ns['load_patterns']()
sys.path.insert(0, H); import rpatN_build as B
# oracle
site = collections.defaultdict(dict); cur = None
for l in open(os.path.join(H, 'k55', 'sites55_rows45_A67.txt')):
    if l.startswith('#'): continue
    m = re.match(r'^\S+ d(\d+) (\d+)/(\d+):', l)
    if m: cur = (int(m.group(1)), m.group(2), m.group(3)); continue
    m = re.match(r'^  (\S+) \((2026 set D|registry), .*: (\d+) embeddings, (\d+) through u', l)
    if m and m.group(2) == '2026 set D': site[cur][m.group(1)] = (int(m.group(3)), int(m.group(4)))
rows = [l.split() for l in open(os.path.join(H, 'k55', 'rows45_A67.txt')) if l.strip() and not l.startswith('#')]
confs = {B.kc(l)[0]: B.kc(l) for l in open(os.path.join(H, 'k55', 'row55_hits_kc.txt')) if l.strip()}
def u_emb(conf, d, lk, sv):
    """u-embeddings of conf into the concrete row (d, lk, sv): rpatN_build's enumerator at centre c, then the pattern's
    slots checked against the row's letters"""
    n = 0
    for c in range(conf[1]):
        if conf[3][c] != d: continue
        for phi, cons in B.embeddings_c(conf, c, d):
            L, S = B.pattern(d, phi, cons, conf[3])
            if all(a == '.' or (a == 'N' and b != '5') or a == b for a, b in zip(L, lk)) and all(a == '.' or a == b for a, b in zip(S, sv)): n += 1
    return n
bad = 0; nk = 0; tab = collections.Counter()
for w, d, lk, sv in rows:
    d = int(d); key = (d, lk, sv); want = any(v[1] > 0 for v in site.get(key, {}).values())
    why = ns['admissible'](d, lk, sv); got = bool(why and why.startswith('pattern'))
    cnt = {nm: u_emb(c, d, lk, sv) for nm, c in confs.items()}
    cmp_ = [(nm, cnt[nm], site.get(key, {}).get(nm, (0, 0))[1]) for nm in confs if cnt[nm] or site.get(key, {}).get(nm, (0, 0))[1]]
    mis = [x for x in cmp_ if x[1] != x[2]]
    ok = (got == want) and not mis
    bad += not ok; nk += got; tab[(want, got)] += 1
    print('%s d%d %s/%s oracle-u-hit %s engine-killed %s %s | u-embeddings mine/sites %s%s' % ('OK ' if ok else 'BAD', d, lk, sv, want, got,
          '(%s)' % why if why else '', ' '.join('%s:%d/%d' % x for x in cmp_), ' MISMATCH' if mis else ''))
print('rpatN oracle check: %d rows, %d killed by rpatN, %d mismatches; (oracle u-hit, engine kill) counts %s' % (len(rows), nk, bad, dict(tab)))
