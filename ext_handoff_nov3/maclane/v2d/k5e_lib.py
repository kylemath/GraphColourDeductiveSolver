"""maclane k5e add-on: helpers of the k86MS2 upper lane (K3gB5e LP, K3l5e checks).  usage: python3 k5e_lib.py <command> ...
(outbox86_k5e.py imports it; launch_upper_k5e.sh, launch_k86MS2.sh, recheck_k5e.sh and smoke_k5e.sh call the commands.)
A check counts only through its run.log line ("[s86U-<tag>] ... ARGS=<args> gkeys <keys> <sol> (md5 <8>) extra: <flags>: <verdict> <n>
tracebacks", written by U86.sh / U86e.sh when the check ends) and its log logs/upper_<tag>.log (same verdict): the family is the line's
args file, the point is the md5 of the checked file, the flags must be the lane's (c6le f2b7 f2b=<rules c67fa1d1 + A5 twins>
rpatN=<rpatN3 rotation-justified>, optionally vK= / vfile=), 0 tracebacks.
Commands:
  verified <sol json>        a FEASIBLE check of this exact file on K3l5e + the 240 keys (p1r/cg_keys_r13w16_16fik.txt) on this machine:
                             prints "OK <tag> <t> <log>" (exit 0) or "NO <reason>" (exit 1)
  state <sol json>           OK / NOTFEASIBLE (its latest K3l5e + 240-key check here ended without FEASIBLE) / NONE (no such check yet)
  pick <default> <max>       in-point candidates for launch_upper_k5e.sh, newest first: points of outbox/upper/POINTS.txt (family K3l or
                             K3l5e) filed after <default> with t below its t, at most <max> (one per md5), then the default:
                             "CAND <name> <json> <t> <family>" lines, then "DEFAULT <name> <json> <t>" (exit 1 if the default is not found)
  file <name> <json> <tag>   file a point FEASIBLE on K3l5e by check <tag> into outbox/upper as <name>__K3l5e.json / .log + POINTS.txt
  prevpass <tag> [family] [keys]   one last filing pass for the stopped lane <tag> (k86MS1: family K3l, keys cg_keys_r13w16.txt), as its
                             outbox86.sh does it (plain names), for FEASIBLE cand/ points it had not filed yet; only points whose
                             run.log check is on that family and keys
  expect <log> <EXPECT file> <section> [n]   the EXPECT lines of <log> (of its first n lines; f2b / gkeys / jcheck / exname / patterns /
                             bonus links, paths stripped) against section <section> (1, 2, ...) of the EXPECT file; exit 0 if equal
  snaprows <src> <dst>       copy the complete lines of a rows file (a K run may be writing it)
v2d (Opus 9 Nov): a lane may run on another key file than the 240 keys (env KEYS of launch_msfam.sh / recheck_fam.sh).  A check counts
only for the key file its run.log line names (gkeys <basename>); points checked on another key file are filed under the family name +
the key label (KLABEL: cg_keys_r13w16_16fikp.txt = the 260 keys -> '_k260', so K3l5j_k260), never under the bare K3l5x name.
  keyscheck <keys path>      the key file is a known one with the listed md5 (KNOWN; KEYS_UNLISTED=1 accepts another file): prints
                             "OK <basename> <md5 8> <label or ->" (exit 0) or "BAD ..." (exit 1)
  lanekeys <tag>             the key file of lane <tag>'s newest launch line in run.log (the 240 keys when none names one)
  verified <sol json> [keys basename]   as above, on that key file (default the 240 keys)"""
import os, re, sys, time, glob, shutil, hashlib

R = '/tmp/maclane-k86'
N = os.path.dirname(os.path.abspath(__file__))
RUNLOG = os.path.join(N, 'run.log')
O = os.environ.get('OUTBOX_UPPER', os.path.join(R, 'outbox', 'upper'))
QF, LF = 'K3l5e', 'K3gB5e'                 # quote family (checks), LP family
K240 = 'cg_keys_r13w16_16fik.txt'          # the 240 keys (3d996dbb)
K260 = 'cg_keys_r13w16_16fikp.txt'         # v2d: the 240 keys + W6b-16p's 20 (0470c459; the container's k86GS12 keys)
KNOWN = {K240: '3d996dbb', K260: '0470c459'}
KLABEL = {K240: '', K260: '_k260'}
LINE = re.compile(r'^(\S+) \[s86U-([^\]]+)\] (?:ENGINE (\S+) )?STACK=(\S+) ARGS=(\S+) gkeys (\S+) (\S+) \(md5 ([0-9a-f]{8})\) extra: (.*)$')
TAIL = re.compile(r'^(.*?): (UPPER-R2: .*?)? ?(\d+) tracebacks$')
FEAS = re.compile(r'^UPPER-R2: FEASIBLE at t = ([0-9.]+)$')


def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def utc(): return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
def logpath(tag): return os.path.join(N, 'logs', 'upper_%s.log' % tag)


def runlog(s):
    with open(RUNLOG, 'a') as fh: fh.write('%s %s\n' % (time.strftime('%H:%M:%SZ', time.gmtime()), s))


def klabel(kb):
    """the family-name label of key file basename kb ('' for the 240 keys)"""
    if kb in KLABEL: return KLABEL[kb]
    st = kb[len('cg_keys_'):] if kb.startswith('cg_keys_') else kb
    st = st[:-4] if st.endswith('.txt') else st
    return '_' + (re.sub(r'[^A-Za-z0-9]', '', st) or 'keys')


def keyscheck(path):
    """(ok, message) for a lane's key file"""
    if not os.path.isfile(path): return False, 'BAD %s: no such file' % path
    kb = os.path.basename(path); m = md5f(path)[:8]
    if kb in KNOWN:
        if m != KNOWN[kb]: return False, 'BAD %s: md5 %s, expected %s' % (path, m, KNOWN[kb])
    elif os.environ.get('KEYS_UNLISTED') != '1':
        return False, 'BAD %s (md5 %s): not a known key file (%s); KEYS_UNLISTED=1 accepts it' % (path, m, ', '.join('%s %s' % kv for kv in sorted(KNOWN.items())))
    return True, 'OK %s %s %s' % (kb, m, klabel(kb) or '-')


LAUNCH = {}


def lanekeys(tag):
    """the key file basename of lane <tag>'s newest '[maclane] launch <tag> (' run.log line (cached per process; K240 when none)"""
    if tag in LAUNCH: return LAUNCH[tag]
    kb = None; pat = re.compile(r'\[maclane\] launch %s \(.*?, keys (\S+) \(([0-9a-f]{8})\)' % re.escape(tag))
    if os.path.isfile(RUNLOG):
        for l in open(RUNLOG, errors='replace'):
            if '[maclane] launch ' + tag + ' (' not in l: continue
            m = pat.search(l)
            if m: kb = m.group(1)
    LAUNCH[tag] = kb or K240; return LAUNCH[tag]


def flags_ok(extra):
    t = extra.split()
    if len(t) < 4 or t[0] != 'c6le' or t[1] != 'f2b7': return False
    if not (t[2].startswith('f2b=') and t[2].endswith('/rules/A5final/rules_c67fa1d1_plus_A5_twins.json')): return False
    if not (t[3].startswith('rpatN=') and t[3].endswith('/rpat/rpatN3_rotation_justified.txt') and ',' not in t[3]): return False
    return all(x.startswith(('vK=', 'vfile=')) for x in t[4:])


def parse(l):
    m = LINE.match(l.rstrip('\n'))
    if not m: return None
    m2 = TAIL.match(m.group(9))
    if not m2: return None
    a = m.group(5); fam = a[len('args_A97_F_W13'):-len('.txt')] if a.startswith('args_A97_F_W13') and a.endswith('.txt') else a
    v = (m2.group(2) or '').strip(); f = FEAS.match(v)
    return {'tag': m.group(2), 'eng': m.group(3) or 'eng', 'stack': m.group(4), 'fam': fam, 'keys': m.group(6), 'sol': m.group(7),
            'm8': m.group(8), 'flags': flags_ok(m2.group(1)), 'verdict': v, 'tb': int(m2.group(3)), 't': f.group(1) if f else None}


class RunLog:
    """run.log, read incrementally: recs[tag] = the last complete [s86U-<tag>] line (a check's line is written when it ends)."""
    def __init__(self): self.pos, self.ino, self.buf, self.recs, self.order = 0, None, b'', {}, []

    def update(self):
        try: st = os.stat(RUNLOG)
        except OSError: return self
        if st.st_ino != self.ino or st.st_size < self.pos: self.__init__(); self.ino = st.st_ino
        with open(RUNLOG, 'rb') as fh: fh.seek(self.pos); data = fh.read()
        self.pos += len(data); lines = (self.buf + data).split(b'\n'); self.buf = lines.pop()
        for l in lines:
            r = parse(l.decode('utf-8', 'replace'))
            if r: self.recs[r['tag']] = r; self.order.append(r)
        return self


def valid(r, m8, fam, keys=K240):
    return r is not None and r['m8'] == m8 and r['fam'] == fam and r['keys'] == keys and r['stack'] == 's77' and r['flags'] and r['tb'] == 0


def feasible(r): return r is not None and r['t'] is not None


def log_ok(r):
    """the check's log still holds this verdict (a later check with the same tag rewrites the log and adds a newer run.log line)"""
    p = logpath(r['tag'])
    if not os.path.isfile(p): return False
    v = [l.rstrip('\n') for l in open(p, errors='replace') if l.startswith('UPPER-R2')]
    return bool(v) and v[-1] == r['verdict']


def verified(js, L=None, fam=QF, keys=K240):
    L = L or RunLog().update(); m8 = md5f(js)[:8]
    for r in reversed(L.order):
        if valid(r, m8, fam, keys) and feasible(r) and L.recs.get(r['tag']) is r and log_ok(r): return r
    return None


def state(js, L=None, keys=K240):
    """'OK' (a FEASIBLE K3l5e + 240-key check of this file), 'NOTFEASIBLE' (its latest such check ended without FEASIBLE and without
    tracebacks), or 'NONE' (no such check yet)"""
    L = L or RunLog().update(); r = verified(js, L, keys=keys)
    if r: return 'OK', r
    m8 = md5f(js)[:8]
    for r in reversed(L.order):
        if valid(r, m8, QF, keys) and L.recs.get(r['tag']) is r and r['verdict'].startswith('UPPER-R2: '): return 'NOTFEASIBLE', r
    return 'NONE', None


def md5sums(d):
    fs = sorted(f for f in os.listdir(d) if f != 'MD5SUMS' and not f.startswith('.') and os.path.isfile(os.path.join(d, f)))
    with open(os.path.join(d, '.MD5SUMS.tmp'), 'w') as fh:
        for f in fs: fh.write('%s  %s\n' % (md5f(os.path.join(d, f)), f))
    os.replace(os.path.join(d, '.MD5SUMS.tmp'), os.path.join(d, 'MD5SUMS'))


def copy_in(src, d, name):
    tmp = os.path.join(d, '.' + name + '.tmp'); shutil.copyfile(src, tmp); os.replace(tmp, os.path.join(d, name))


def file_point(name, js, r, fam, who):
    """outbox/upper/<name>__<fam>.json + .log (the check's log), one POINTS.txt line (same columns as k86MS1's: name t md5 family log
    filed-at), MD5SUMS, one run.log line.  The json goes last: its presence marks the point as filed."""
    os.makedirs(O, exist_ok=True); base = '%s__%s' % (name, fam)
    if os.path.exists(os.path.join(O, base + '.json')): return 'already filed'
    m = md5f(js); copy_in(logpath(r['tag']), O, base + '.log'); copy_in(js, O, base + '.json')
    with open(os.path.join(O, 'POINTS.txt'), 'a') as fh: fh.write('%s    %s    %s    %s    %s    %s\n' % (base, r['t'], m, fam, base + '.log', utc()))
    md5sums(O)
    runlog('[maclane-outbox-%s] filed %s (t = %s, md5 %s, %s; check %s on %s)' % (who, base, r['t'], m, fam, r['tag'], r['eng']))
    return 'filed %s (t = %s)' % (base, r['t'])


def points():
    p = os.path.join(O, 'POINTS.txt'); out = []
    if os.path.isfile(p):
        for l in open(p, errors='replace'):
            w = l.split()
            if len(w) >= 5:
                try: float(w[1])
                except ValueError: continue
                out.append({'name': w[0], 't': w[1], 'md5': w[2], 'fam': w[3], 'log': w[4]})
    return out


def base_name(n): return re.sub(r'__K3[A-Za-z0-9]+(_[A-Za-z0-9]+)?$', '', n)


def pick(default, maxn):
    ps = points(); idx = -1
    for i, p in enumerate(ps):
        if base_name(p['name']) == default: idx = i; break   # its first filing (a K3l5e recheck adds a later line)
    dj = os.path.join(N, 'cand', default + '.json')
    if not os.path.isfile(dj): dj = os.path.join(O, default + '.json')
    if not os.path.isfile(dj): print('NODEFAULT %s (not in cand/ nor in %s)' % (default, O)); return 1
    import json
    td = float(json.load(open(dj))['t']); seen = set(); out = []
    for p in reversed(ps[idx + 1:]):
        if p['fam'] not in ('K3l', QF) or float(p['t']) >= td - 1e-12 or p['md5'] in seen or base_name(p['name']) == default: continue
        js = os.path.join(O, p['name'] + '.json')
        if not os.path.isfile(js): continue
        seen.add(p['md5']); out.append('CAND %s %s %s %s' % (p['name'], js, p['t'], p['fam']))
        if len(out) >= maxn: break
    for l in out: print(l)
    print('DEFAULT %s %s %.12f' % (default, dj, td)); return 0


def prevpass(tag, fam='K3l', keys='cg_keys_r13w16.txt'):
    """the stopped lane's outbox86.sh, one pass: cand/sol_X.json (not _probe) not yet in the outbox whose first existing log of
    logs/upper_sol_X.log, logs/upper_F_X.log is FEASIBLE -> outbox/<name>.json + that log, POINTS.txt line with family <fam>.
    Added here: the log's run.log line must be a check of this file on <fam> + <keys> with the lane's flags."""
    L = RunLog().update(); n = 0; os.makedirs(O, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(N, 'cand', 'sol_*.json'))):
        b = os.path.basename(f)[:-5]
        if b.endswith('_probe') or os.path.exists(os.path.join(O, b + '.json')): continue
        tg = next((t for t in (b, 'F_' + b[4:]) if os.path.exists(logpath(t))), None)
        if tg is None: continue
        r = L.recs.get(tg)
        if not (valid(r, md5f(f)[:8], fam, keys) and feasible(r) and log_ok(r)): continue
        m = md5f(f); copy_in(logpath(tg), O, os.path.basename(logpath(tg))); copy_in(f, O, b + '.json')
        with open(os.path.join(O, 'POINTS.txt'), 'a') as fh:
            fh.write('%s    %s    %s    %s    %s    %s\n' % (b, r['t'], m, fam, os.path.basename(logpath(tg)), utc()))
        md5sums(O); n += 1
        runlog('[maclane-outbox-%s] filed %s (t = %s, md5 %s, %s) (k5e: last pass after the lane was stopped)' % (tag, b, r['t'], m, fam))
        print('filed %s (t = %s, %s)' % (b, r['t'], fam))
    print('%s: %d point(s) filed in the last pass' % (tag, n)); return 0


KEEP = ('f2b: ', 'gkeys: ', 'jcheck: ', 'exname: ', 'patterns: ', 'bonus links: ')


def strip(l): return re.sub(r"(?<![\w.-])/[^\s,:;'\"()\[\]{}]+/([^\s/,:;'\"()\[\]{}]+)", r'\1', l.rstrip('\n'))


def expect(log, ef, sec, nl=0):
    ls = [l for l in open(log, errors='replace') if l.strip() and not l.startswith('hshim: ')]
    got = [strip(l) for l in (ls[:nl] if nl else ls) if l.startswith(KEEP)]
    secs, cur = [], None
    for l in open(ef):
        l = l.rstrip('\n')
        if l.startswith('## '): cur = []; secs.append(cur); continue
        if cur is not None and l and not l.startswith('#'): cur.append(l)
    want = secs[sec - 1]
    pl = [l for l in got if l.startswith('patterns: ')]
    if pl:
        m = re.search(r'patterns: (\d+) files read.*?by d \{(.*?)\}; by kind \{(.*?)\}', pl[0])
        if m:
            d9 = re.search(r'\b9: (\d+)', m.group(2)); k = dict((a, int(b)) for a, b in re.findall(r"'(\w+)': (\d+)", m.group(3)))
            print('counts: %s files, distinct d9 %s, D %s / C %s / RPAT %s / RPATN %s' % (m.group(1), d9.group(1) if d9 else '?', k.get('D'), k.get('C'), k.get('RPAT'), k.get('RPATN')))
    bad = [('-' + w) for w in want if w not in got] + [('+' + g) for g in got if g not in want]
    for b in bad: print('  ' + b[:300])
    print('EXPECT section %d: %d lines, this log %d, %s' % (sec, len(want), len(got), 'SAME' if got == want else 'DIFFERENT'))
    return 0 if got == want else 1


def snaprows(src, dst):
    b = open(src, 'rb').read(); b = b[:b.rfind(b'\n') + 1]
    with open(dst + '.tmp', 'wb') as fh: fh.write(b)
    os.replace(dst + '.tmp', dst); print('%d complete lines -> %s' % (b.count(b'\n'), dst)); return 0


def main(a):
    if not a: print(__doc__); return 2
    c = a[0]
    if c == 'verified':
        kb = os.path.basename(a[2]) if len(a) > 2 else K240
        r = verified(os.path.abspath(a[1]), keys=kb)
        if r: print('OK %s %s %s' % (r['tag'], r['t'], logpath(r['tag']))); return 0
        print('NO FEASIBLE %s + %s check of %s (md5 %s) in run.log' % (QF, kb, os.path.basename(a[1]), md5f(a[1])[:8])); return 1
    if c == 'keyscheck':
        ok, msg = keyscheck(os.path.abspath(a[1])); print(msg); return 0 if ok else 1
    if c == 'lanekeys': print(lanekeys(a[1])); return 0
    if c == 'state':
        st, r = state(os.path.abspath(a[1])); print('%s %s %s' % (st, r['tag'] if r else '-', (r['t'] or r['verdict'].replace(' ', '_')) if r else '-')); return 0
    if c == 'pick': return pick(a[1], int(a[2]))
    if c == 'file':
        name, js, tag = a[1], os.path.abspath(a[2]), a[3]; L = RunLog().update(); r = L.recs.get(tag)
        if not (valid(r, md5f(js)[:8], QF) and feasible(r) and log_ok(r)):
            print('not filed: run.log has no FEASIBLE %s + %s check %s of %s' % (QF, K240, tag, os.path.basename(js))); return 1
        print(file_point(name, js, r, QF, 'k5e-recheck')); return 0
    if c == 'prevpass': return prevpass(*a[1:4])
    if c == 'expect': return expect(a[1], a[2], int(a[3]), int(a[4]) if len(a) > 4 else 0)
    if c == 'snaprows': return snaprows(a[1], a[2])
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
