"""EXPLORE round 54b: Studio's verdicts on a census window file (drive45 / drive54s format: A_kcc.out, A_df.out,
A_cf.out, KILL, progress.txt) -> census cache lines 'name verdict key' (key = the window line after its name), by the
rule of cen53.Engines.verdict: kc D=true and dfast(18) D=true -> D (else MISMATCH-D); else kc C-REDUCIBLE X and cfast
--fixed X leftover 0 -> C{X} (else CFAST-REJECTS); else kc INCOMPLETE -> timeout; else none.  A window whose second
engine has not reported yet is left out.  Kills are checked against KILL.
usage: python3 -I imp54.py WINFILE STUDIODIR OUT   (OUT appended, keys already in OUT or G_res.txt skipped)"""
import sys, os, re
WF, SD, OUT = sys.argv[1:4]; H = os.path.dirname(os.path.abspath(__file__))
win = {}
for l in open(WF):
    if l.strip(): nm, key = l.rstrip('\n').split(' ', 1); assert nm not in win, nm; win[nm] = key
def blocks(f):
    out, cur = {}, None
    if not os.path.exists(f): return out
    for l in open(f):
        if l.strip() and not l.startswith(' ') and not l.startswith('#'): cur = l.split()[0]; out.setdefault(cur, []).append([])
        if cur and not l.startswith('#'): out[cur][-1].append(l)
    return out
kb, db, cb = (blocks(os.path.join(SD, f)) for f in ('A_kcc.out', 'A_df.out', 'A_cf.out'))
kill = {l.split()[0]: l.split(None, 1)[1].strip() for l in open(os.path.join(SD, 'KILL')) if l.strip()}
have = set()
for f in (OUT, os.path.join(H, 'G_res.txt')):
    if os.path.exists(f): have |= {l.rstrip('\n').split(' ', 2)[2] for l in open(f) if l.count(' ') >= 2}
res = {}; pend = []
for nm, key in win.items():
    if nm not in kb: continue
    assert len(kb[nm]) == 1, (nm, 'kc blocks', len(kb[nm]))
    o = ''.join(kb[nm][0]); first = kb[nm][0][0]; v = 'none'
    if 'D=true' in first:
        if nm not in db: pend.append(nm); continue
        v = 'D' if 'D=true' in ''.join(db[nm][-1]) else 'MISMATCH-D'
    m = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', o)
    if v == 'none' and m:
        if nm not in cb: pend.append(nm); continue
        v = 'C{%s}' % m.group(1) if 'C-REDUCIBLE, leftover bad classes extending after contraction = 0' in ''.join(cb[nm][-1]) else 'CFAST-REJECTS'
    if v == 'none' and 'INCOMPLETE' in first: v = 'timeout'
    res[nm] = v
kv = {n for n, v in res.items() if v == 'D' or v.startswith('C{')}
assert kv == set(kill) & set(res), ('kills differ from KILL', sorted(kv ^ (set(kill) & set(res)))[:5])
new = [(n, v) for n, v in res.items() if win[n] not in have]
with open(OUT, 'a') as o:
    for n, v in new: o.write('%s %s %s\n' % (n, v, win[n]))
import collections
print('windows with verdicts %d (pending second engine %d); by verdict %s; kills = KILL; new cache lines %d -> %s' % (
    len(res), len(pend), dict(collections.Counter(v if v[0] != 'C' else 'C' for v in res.values())), len(new), OUT))
