#!/usr/bin/env python3
"""Round B4: independent re-check of explore round-43 kill batch (c5a71dc0, 382 windows: 184 D + 198 C) on Team B's
kc and cfast (loop/teamB/b2_rsst633).  Inputs (kills.txt, kills_kc.out, kills_cf.cfast) are `git show c5a71dc0:...`
copies in directory SRC.  At most 2 engine processes at once (2 workers, engines run sequentially per config).
D: kc (D closure) and cfast (D closure).  C: kc -x <claimed X> (kc -C2 -x if adm=no), kc -C (kc's own X search),
cfast --fixed <claimed X> (Gonthier; --nogonthier retry noted).  Resumable on OUT.
usage: python3 run.py SRC OUT"""
import os, re, sys, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
import threading
H = os.path.dirname(os.path.abspath(__file__)); BB = os.path.join(H, '..', 'b2_rsst633')
KC, CF = os.path.join(BB, 'kc'), os.path.join(BB, 'cfast')
SRC, OUT = sys.argv[1], sys.argv[2]
COLS = ['id', 'ring', 'm', 'claimed', 'claimed_X', 'kc_verdict', 'kc_detail', 'cfast_verdict', 'cfast_detail',
        'agree', 'counts_match_explore', 'notes', 'secs']
KV = re.compile(r'r=(\d+) m=(\d+) classes=(\d+) ext=(\d+) reached=(\d+) (?:bad=\d+ )?D=(\w+)')
lines = [l.rstrip('\n') for l in open(os.path.join(SRC, 'kills.txt')) if l.strip()]
def blocks(fn):
    out, cur = {}, None
    for l in open(os.path.join(SRC, fn)):
        if l.strip() and not l.startswith(' '): cur = l.split()[0]
        out.setdefault(cur, []).append(l.rstrip('\n'))
    return out
ekc, ecf = blocks('kills_kc.out'), blocks('kills_cf.cfast')
def claimed(nm):
    if 'D=true' in ekc[nm][0]: return 'D', '-'
    m = re.search(r'fixed X=\{([^}]*)\}', '\n'.join(ecf[nm])); return 'C', m.group(1)
def run(args, t=1800):
    try: return subprocess.run(args, capture_output=True, text=True, timeout=t).stdout.splitlines()
    except subprocess.TimeoutExpired: return ['TIMEOUT']
lock = threading.Lock()
def one(line):
    import time; t0 = time.time(); nm = line.split()[0]; typ, X = claimed(nm); notes = []
    d = tempfile.mkdtemp(); inp = os.path.join(d, 'c.txt'); open(inp, 'w').write(line + '\n')
    ek = KV.search(ekc[nm][0]).group(3, 4, 5)
    def counts(out, who):
        m = KV.search(out[0]) if out else None
        if not m: notes.append(who + ' parse fail'); return None
        return m
    if typ == 'D':
        k = run([KC, inp]); c = run([CF, inp]); km, cm = counts(k, 'kc'), counts(c, 'cfast')
        kv = 'D' if km and km.group(6) == 'true' and km.group(3) == km.group(5) else 'notD'
        cv = 'D' if cm and cm.group(6) == 'true' and cm.group(3) == cm.group(5) else 'notD'
        kd = 'reached=%s/%s' % (km.group(5), km.group(3)) if km else '-'
        cd = 'reached=%s/%s' % (cm.group(5), cm.group(3)) if cm else '-'
    else:
        xf = os.path.join(d, 'c.x'); open(xf, 'w').write('%s {%s}\n' % (nm, X))
        k = run([KC, '-x', xf, inp]); km = counts(k, 'kc'); xl = [l for l in k if l.startswith('  X=')]; mode = 'x'
        if xl and 'adm=no' in xl[0]:
            k = run([KC, '-C2', '-x', xf, inp]); xl = [l for l in k if l.startswith('  X=')]; mode = 'C2x'
        if km and km.group(6) == 'true': kv, kleft = 'D', '0'; notes.append('kc D without contraction')
        elif xl and 'adm=yes' in xl[0]:
            kleft = xl[0].split('leftover')[1].strip(); kv = 'C' if kleft == '0' else 'fail'
        else: kv, kleft = 'inadm', '-'; notes.append('kc: ' + (xl[0].strip() if xl else 'no X line'))
        ks = run([KC, '-C', inp]); sl = [l for l in ks if 'C-REDUCIBLE' in l or l.startswith('  ')]
        ms = re.search(r'C-REDUCIBLE X=\{([^}]*)\}', '\n'.join(ks))
        own = ms.group(1) if ms else ('none:' + (sl[0].strip()[:60] if sl else 'no line'))
        kd = 'mode=%s leftover=%s own_search_X={%s}' % (mode, kleft, own)
        if not ms: notes.append('kc -C own search found no X')
        c = run([CF, inp, '--fixed', X]); cm = counts(c, 'cfast'); fl = [l for l in c if 'fixed X=' in l]; gon = 'gonthier'
        if fl and 'INADMISSIBLE' in fl[0]:
            notes.append('cfast Gonthier-inadmissible; --nogonthier'); gon = 'nogonthier'
            c = run([CF, inp, '--fixed', X, '--nogonthier']); fl = [l for l in c if 'fixed X=' in l]
        if cm and cm.group(6) == 'true': cv, cleft = 'D', '0'; notes.append('cfast D without contraction')
        elif fl and 'INADMISSIBLE' not in fl[0]:
            cleft = fl[0].rsplit('=', 1)[1].strip(); cv = 'C' if cleft == '0' else 'fail'
            ne = int(re.search(r'\((\d+) edges\)', fl[0]).group(1))
            if ne != len(X.split(',')): cv = 'xparse'; notes.append('cfast matched %d of %d X edges' % (ne, len(X.split(','))))
        else: cv, cleft = 'inadm', '-'
        cd = '%s leftover=%s' % (gon, cleft)
    ok = (kv == typ and cv == typ)
    cmx = all(m is not None and m.group(3, 4, 5) == ek for m in (km, cm))
    if km and cm and km.group(3, 4, 5) != cm.group(3, 4, 5): notes.append('kc/cfast classes-ext-reached differ')
    for f in os.listdir(d): os.unlink(os.path.join(d, f))
    os.rmdir(d)
    return dict(id=nm, ring=line.split()[1], m=line.split()[2], claimed=typ, claimed_X=X, kc_verdict=kv, kc_detail=kd,
                cfast_verdict=cv, cfast_detail=cd, agree='yes' if ok else 'NO', counts_match_explore='yes' if cmx else 'no',
                notes=';'.join(notes) or '-', secs='%.1f' % (time.time() - t0))
done = set()
if os.path.exists(OUT): done = {l.split('\t')[0] for l in open(OUT) if not l.startswith('id\t')}
else: open(OUT, 'w').write('\t'.join(COLS) + '\n')
out = open(OUT, 'a')
def job(line):
    r = one(line)
    with lock:
        out.write('\t'.join(r[k] for k in COLS) + '\n'); out.flush()
        print(r['id'], r['claimed'], r['kc_verdict'], r['cfast_verdict'], r['agree'], r['secs'], flush=True)
with ThreadPoolExecutor(2) as ex:
    list(ex.map(job, [l for l in lines if l.split()[0] not in done]))
print('DONE', flush=True)
