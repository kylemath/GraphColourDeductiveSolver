"""maclane k5g add-on: helpers of the generic upper-lane family switch (k86MS2 -> k86MS3 -> ...).  usage: python3 fam_lib.py <command> ...
A family is named by its suffix x: LP family K3gB5x = args_A97_F_W13K3gB5x.txt, check family K3l5x = args_A97_F_W13K3l5x.txt; each one is
the previous suffix's args + one line naming the kill file (cpat=<file> for a C kill, pat=<file> for a D kill).  The pack's fam/FAMILIES.txt (append-only; install_fam.sh adds one line per
data add-on) holds, per suffix: prev, the kill file, the md5s of the kill file and of both args (args md5 with the pack root taken out = the
container's), the EXPECT file and its md5, and the status (E2 = the Lead's [E2] note is in; anything else: launch_upper_fam.sh needs
E2_NOTE=...).  A check counts as in k5e_lib.py: its run.log line (family, keys, md5 of the file, flags, 0 tracebacks) and its log.
Commands:
  famcheck <x> [quiet]       the FAMILIES.txt line of x: every file there, md5s as listed, both args = prev's args + exactly one line
                             "cpat=<the kill file>" (or "pat=<the kill file>"); prints "OK x=<x> prev=<p> status=<s> l=<K3l args path> gb=<K3gB args path> pat=<kill file>
                             expect=<EXPECT path>" (exit 0) or the problems (exit 1; 2 = no line for x)
  families                   the FAMILIES.txt suffixes, in order
  lane                       the newest upper lane k86MS<n> in run.log: "<tag> <suffix or -> <max n> <its in-point json or -> <LP args>"
                             ("none - 1 - -" when no k86MS lane started yet)
  verified <x> <json>        a FEASIBLE check of this exact file on K3l5x + the 240 keys here: "OK <tag> <t> <log>" (exit 0) / "NO ..." (1)
  state <x> <json>           OK / NOTFEASIBLE / NONE, as k5e_lib.py state, for K3l5x
  file <x> <name> <json> <tag>   file a point FEASIBLE on K3l5x by check <tag> as outbox/upper/<name>__K3l5x.json / .log + POINTS.txt
  pick <ref json> <max>      in-point candidates for launch_upper_fam.sh: POINTS.txt lines filed after the reference's first filing (all
                             lines when it was never filed), of a check family (K3l, K3l5<any>; never K3gB*), t below the reference's,
                             newest first, one per md5, at most <max>: "CAND <name> <json> <t> <family>" lines, then "REF <json> <t>"
  outpass <tag> <x> [once]   (outbox86_fam.py) one filing pass of lane <tag>'s points under K3l5x / K3gB5x
  expect / snaprows          as k5e_lib.py
v2d (Opus 9 Nov): key files.  verified / state / pick take an optional last argument, the key file basename (default the 240 keys,
k5e_lib.K240); a check counts only on that key file.  Points of a lane on another key file (its launch line in run.log names it:
k5e_lib.lanekeys) are filed by outpass under K3l5<x><label> / K3gB5<x><label> (k5e_lib.klabel: the 260 keys -> K3l5j_k260), and file
uses the key file of the check it files.  pick on the 240 keys never offers a labelled point (is_check_fam: K3l or K3l5<letters/digits>).
  lanekeys <tag>             as k5e_lib.py"""
import os, re, sys, json, glob, hashlib
import k5e_lib as K

N, R, O = K.N, K.R, K.O
FD = os.path.join(R, 'fam'); FAMF = os.environ.get('FAM_FILE') or os.path.join(FD, 'FAMILIES.txt')   # FAM_FILE: install_fam.py's check of a new line
RF = os.environ.get('REPL_FAM', 'MW')


def cmd5(p):
    """md5 with the pack root taken out: the container's md5 of an args file"""
    return hashlib.md5(open(p, 'rb').read().replace((R + '/fs/').encode(), b'/')).hexdigest()


def families():
    out = []
    if not os.path.isfile(FAMF): return out
    for l in open(FAMF, errors='replace'):
        l = l.rstrip('\n')
        if not l.startswith('suf='): continue
        head, _, note = l.partition(' note=')
        d = dict(w.split('=', 1) for w in head.split() if '=' in w); d['note'] = note; d['line'] = l
        out.append(d)
    return out


def fam(x):
    for d in families():
        if d['suf'] == x: return d
    return None


def famcheck(x):
    d = fam(x)
    if d is None: return None, ['no line for suffix %r in %s (install its data add-on: bash install_fam.sh <maclane-k86-fam-%s.tgz>)' % (x, FAMF, x)]
    bad = []
    pat = os.path.join(N, d['pat']); la = os.path.join(N, d['l']); ga = os.path.join(N, d['gb']); ex = os.path.join(R, d['expect'])
    if d['l'] != 'args_A97_F_W13K3l5%s.txt' % x or d['gb'] != 'args_A97_F_W13K3gB5%s.txt' % x: bad.append('args names %s / %s do not match suffix %s' % (d['l'], d['gb'], x))
    for p, key, f in ((pat, 'pat_md5', K.md5f), (la, 'l_md5', cmd5), (ga, 'gb_md5', cmd5), (ex, 'expect_md5', K.md5f)):
        if not os.path.isfile(p): bad.append('%s missing' % p); continue
        m = f(p)
        if m != d.get(key): bad.append('%s: md5 %s, FAMILIES.txt says %s' % (os.path.basename(p), m, d.get(key)))
    pv = d.get('prev', '')
    for kind, a in (('K3l5', la), ('K3gB5', ga)):
        pa = os.path.join(N, 'args_A97_F_W13%s%s.txt' % (kind, pv))
        if not (os.path.isfile(pa) and os.path.isfile(a)): bad.append('chain: %s or %s missing' % (os.path.basename(pa), os.path.basename(a))); continue
        old, new = open(pa).read(), open(a).read()
        if not new.startswith(old) or new[len(old):].split() not in (['cpat=' + pat], ['pat=' + pat]):
            bad.append('chain: %s is not %s + one line cpat=%s (C kill) or pat=%s (D kill)' % (os.path.basename(a), os.path.basename(pa), d['pat'], d['pat']))
    d.update(lp=la, gp=ga, patp=pat, exp=ex)
    return d, bad


def qf(x): return 'K3l5' + x
def lf(x): return 'K3gB5' + x


def verified(x, js, L=None, keys=K.K240): return K.verified(js, L, fam=qf(x), keys=keys)


def state(x, js, L=None, keys=K.K240):
    L = L or K.RunLog().update(); r = verified(x, js, L, keys)
    if r: return 'OK', r
    m8 = K.md5f(js)[:8]
    for r in reversed(L.order):
        if K.valid(r, m8, qf(x), keys) and L.recs.get(r['tag']) is r and r['verdict'].startswith('UPPER-R2: '): return 'NOTFEASIBLE', r
    return 'NONE', None


START = re.compile(r'\[s86K-(k86MS(\d+))\] start .*?ARGS=(\S+) .*? feas (\S+)')


def lane():
    """the newest k86MS<n> start line of run.log: (tag, suffix or '-', max n seen, in-point json, LP args name)"""
    best, mx = None, 1
    if os.path.isfile(K.RUNLOG):
        for l in open(K.RUNLOG, errors='replace'):
            m = START.search(l)
            if m: best = m; mx = max(mx, int(m.group(2)))
    if best is None: return 'none', '-', mx, '-', '-'
    a = best.group(3); s = re.match(r'^args_A97_F_W13K3gB5(\w+)\.txt$', a)
    return best.group(1), s.group(1) if s else '-', mx, best.group(4), a


def is_check_fam(f, kl=''):
    """a check-family name of POINTS.txt for key label kl ('' = the 240 keys: K3l or K3l5<letters/digits>)"""
    if not kl: return f == 'K3l' or bool(re.match(r'^K3l5[A-Za-z0-9]+$', f))
    return f.endswith(kl) and bool(re.match(r'^K3l5[A-Za-z0-9]+$', f[:-len(kl)]))


def pick(ref, maxn, keys=K.K240):
    ref = os.path.abspath(ref); mref = K.md5f(ref); td = float(json.load(open(ref))['t']); rb = K.base_name(os.path.basename(ref)[:-5])
    ps = K.points(); idx = -1
    for i, p in enumerate(ps):
        if p['md5'] == mref or K.base_name(p['name']) == rb: idx = i; break
    seen = {mref}; out = []
    for p in reversed(ps[idx + 1:]):
        if not is_check_fam(p['fam'], K.klabel(keys)) or float(p['t']) >= td - 1e-12 or p['md5'] in seen: continue
        js = os.path.join(O, p['name'] + '.json')
        if not os.path.isfile(js): continue
        seen.add(p['md5']); out.append('CAND %s %s %s %s' % (p['name'], js, p['t'], p['fam']))
        if len(out) >= maxn: break
    for l in out: print(l)
    print('REF %s %.12f' % (ref, td)); return 0


def outpass(tag, x, once=False, L=None, keys=None):
    """outbox86_k5e.py's pass for any family: a lane point (sol_<tag>_inNN, sol_rep<last 2 of tag><REPL_FAM>_NN, their _tight) is filed
    once, under K3l5x when a check of exactly this file on K3l5x is FEASIBLE (in-point check, ladder sub-check F_<x>_sub, tighten final
    F_<x>_tight), else under K3gB5x when it is a ladder point whose LP-family check F_<x> is FEASIBLE and whose K3l5x sub-check ended
    without FEASIBLE (with once: or never ran).  v2d: on the lane's key file (keys, default its launch line's: k5e_lib.lanekeys), the
    family names carrying its label (K3l5<x><label> / K3gB5<x><label>)"""
    own = re.compile(r'^sol_(%s_in\d\d|rep%s%s_\d\d)(_tight)?$' % (re.escape(tag), re.escape(tag[-2:]), re.escape(RF)))
    L = L or K.RunLog().update(); res = []
    kb = keys or K.lanekeys(tag); kl = K.klabel(kb)
    for f in sorted(glob.glob(os.path.join(N, 'cand', 'sol_*.json'))):
        b = os.path.basename(f)[:-5]
        if not own.match(b) or glob.glob(os.path.join(O, glob.escape(b) + '__*.json')): continue
        m8 = K.md5f(f)[:8]; y = b[4:]; tq, tm = 'F_%s_sub' % y, 'F_%s' % y
        pk = None
        for tg in (b, tq, tm):
            r = L.recs.get(tg)
            if K.valid(r, m8, qf(x), kb) and K.feasible(r) and K.log_ok(r): pk = (r, qf(x) + kl); break
        if pk is None and b.startswith('sol_rep') and not b.endswith('_tight'):
            rq, rm = L.recs.get(tq), L.recs.get(tm)
            sub_done = (K.valid(rq, m8, qf(x), kb) and not K.feasible(rq)) or (once and rq is None)
            if sub_done and K.valid(rm, m8, lf(x), kb) and K.feasible(rm) and K.log_ok(rm): pk = (rm, lf(x) + kl)
        if pk: res.append(K.file_point(b, f, pk[0], pk[1], tag))
    return res


def main(a):
    if not a: print(__doc__); return 2
    c = a[0]
    if c == 'famcheck':
        d, bad = famcheck(a[1])
        if d is None: print(bad[0]); return 2
        if bad:
            for b in bad: print('BAD ' + b)
            return 1
        print('OK x=%s prev=%s status=%s l=%s gb=%s pat=%s expect=%s' % (a[1], d.get('prev'), d.get('status'), d['lp'], d['gp'], d['patp'], d['exp']))
        if len(a) < 3: print('   note: %s' % d['note'])
        return 0
    if c == 'families': print(' '.join(d['suf'] for d in families())); return 0
    if c == 'lane': t, s, mx, ip, la = lane(); print('%s %s %d %s %s' % (t, s, mx, ip, la)); return 0
    if c == 'verified':
        kb = os.path.basename(a[3]) if len(a) > 3 else K.K240
        r = verified(a[1], os.path.abspath(a[2]), keys=kb)
        if r: print('OK %s %s %s' % (r['tag'], r['t'], K.logpath(r['tag']))); return 0
        print('NO FEASIBLE %s + %s check of %s (md5 %s) in run.log' % (qf(a[1]), kb, os.path.basename(a[2]), K.md5f(a[2])[:8])); return 1
    if c == 'state':
        kb = os.path.basename(a[3]) if len(a) > 3 else K.K240
        st, r = state(a[1], os.path.abspath(a[2]), keys=kb); print('%s %s %s' % (st, r['tag'] if r else '-', (r['t'] or r['verdict'].replace(' ', '_')) if r else '-')); return 0
    if c == 'file':
        x, name, js, tag = a[1], a[2], os.path.abspath(a[3]), a[4]; L = K.RunLog().update(); r = L.recs.get(tag)
        kb = r['keys'] if r else K.K240
        if kb not in K.KNOWN and os.environ.get('KEYS_UNLISTED') != '1':
            print('not filed: check %s is on key file %s, not a known one (KEYS_UNLISTED=1 files it)' % (tag, kb)); return 1
        if not (K.valid(r, K.md5f(js)[:8], qf(x), kb) and K.feasible(r) and K.log_ok(r)):
            print('not filed: run.log has no FEASIBLE %s + %s check %s of %s' % (qf(x), kb, tag, os.path.basename(js))); return 1
        print(K.file_point(name, js, r, qf(x) + K.klabel(kb), 'fam-recheck')); return 0
    if c == 'pick': return pick(a[1], int(a[2]), os.path.basename(a[3]) if len(a) > 3 else K.K240)
    if c == 'lanekeys': print(K.lanekeys(a[1])); return 0
    if c == 'outpass':
        res = outpass(a[1], a[2], once=a[3:4] == ['once'])
        for s in res: print(s)
        print('%s: %d point(s) filed (%s / %s)' % (a[1], len(res), qf(a[2]), lf(a[2]))); return 0
    if c == 'expect': return K.expect(a[1], a[2], int(a[3]), int(a[4]) if len(a) > 4 else 0)
    if c == 'snaprows': return K.snaprows(a[1], a[2])
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
