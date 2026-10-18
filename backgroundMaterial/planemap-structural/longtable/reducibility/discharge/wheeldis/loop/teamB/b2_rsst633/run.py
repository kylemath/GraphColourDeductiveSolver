#!/usr/bin/env python3
"""Round B2 driver: all 633 RSST configurations on kc and cfast, ring order (smallest first, then conf order).
Resumable: indices already in results.tsv are skipped.  At most 2 engine processes at a time.
C: cfast --fixed RSST_X (Gonthier admissibility; --nogonthier retry noted) and kc -x RSST_X (conservative; if adm=no,
kc -C2 -x, killed as soon as the X line is printed so the -C2 search does not run).  D: kc and cfast closures.
Usage: python3 run.py [MAXRING]"""
import os, re, sys, time, subprocess, threading
import conv
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(H, 'tmp'); os.makedirs(T, exist_ok=True)
OUT = os.path.join(H, 'results.tsv'); KC = os.path.join(H, 'kc'); CF = os.path.join(H, 'cfast')
COLS = ['idx', 'name', 'ring', 'label', 'rsst_ext', 'rsst_bad', 'X', 'kc_verdict', 'kc_mode', 'kc_leftover', 'kc_classes',
        'kc_ext', 'kc_reached', 'cf_verdict', 'cf_leftover', 'cf_classes', 'cf_ext', 'cf_reached', 'status', 'notes', 'secs']
MAXR = int(sys.argv[1]) if len(sys.argv) > 1 else 99
KV = re.compile(r'r=\d+ m=\d+ classes=(\d+) ext=(\d+) reached=(\d+) D=(\w+)')
CV = re.compile(r'r=\d+ m=\d+ classes=(\d+) ext=(\d+) reached=(\d+) bad=\d+ D=(\w+)')

def kc_run(c, inp, xf, broad=False):
    args = [KC] + (['-C2'] if broad else []) + (['-x', xf] if xf else []) + [inp]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, text=True); lines = []
    for ln in p.stdout:
        lines.append(ln.rstrip())
        if ln.startswith('  X='): break
    p.kill(); p.wait(); return lines

def cf_run(inp, X, gon=True):
    args = [CF, inp] + (['--fixed', X] if X else []) + ([] if gon else ['--nogonthier'])
    return subprocess.run(args, capture_output=True, text=True).stdout.splitlines()

def one(c):
    t0 = time.time(); inp = os.path.join(T, '%d.in' % c['idx']); open(inp, 'w').write(c['line'] + '\n')
    xf = None; notes = []
    if c['label'] == 'C': xf = os.path.join(T, '%d.x' % c['idx']); open(xf, 'w').write('%s {%s}\n' % (c['name'], c['X']))
    res = {}
    th = threading.Thread(target=lambda: res.__setitem__('cf', cf_run(inp, c['X'] or None))); th.start()
    kl = kc_run(c, inp, xf); th.join(); cl = res['cf']
    r = dict(idx=c['idx'], name=c['name'], ring=c['r'], label=c['label'], rsst_ext=c['ext'], rsst_bad=c['bad'], X=c['X'] or '-')
    m = KV.search(kl[0]) if kl else None
    r.update(kc_classes=m.group(1), kc_ext=m.group(2), kc_reached=m.group(3)) if m else notes.append('kc parse fail')
    kmode = 'D'; kleft = '-'
    if c['label'] == 'D': kv = 'D' if m and m.group(4) == 'true' else 'notD'
    else:
        xl = [l for l in kl if l.startswith('  X=')]
        if m and m.group(4) == 'true': kv, kleft = 'D', '0'; notes.append('kc D without contract')
        elif xl and 'adm=no' in xl[0]:
            kl2 = kc_run(c, inp, xf, broad=True); xl = [l for l in kl2 if l.startswith('  X=')]; kmode = 'C2'
        else: kmode = 'C'
        if not (m and m.group(4) == 'true'):
            if xl and 'adm=yes' in xl[0]:
                kleft = xl[0].split('leftover')[1].strip(); kv = 'C' if kleft == '0' else 'fail'
            else: kv = 'inadm'; notes.append('kc: ' + (xl[0].strip() if xl else 'no X line'))
    m2 = CV.search(cl[0]) if cl else None
    r.update(cf_classes=m2.group(1), cf_ext=m2.group(2), cf_reached=m2.group(3)) if m2 else notes.append('cfast parse fail')
    cleft = '-'
    if c['label'] == 'D': cv = 'D' if m2 and m2.group(4) == 'true' else 'notD'
    elif m2 and m2.group(4) == 'true': cv, cleft = 'D', '0'
    else:
        fl = [l for l in cl if 'fixed X=' in l]
        if fl and 'INADMISSIBLE' in fl[0]:
            notes.append('cfast Gonthier-inadmissible; --nogonthier'); cl2 = cf_run(inp, c['X'], gon=False)
            fl = [l for l in cl2 if 'fixed X=' in l]
        if fl and 'INADMISSIBLE' not in fl[0]:
            cleft = fl[0].rsplit('=', 1)[1].strip(); cv = 'C' if cleft == '0' else 'fail'
            ne = int(re.search(r'\((\d+) edges\)', fl[0]).group(1))
            if ne != c['k']: notes.append('cfast matched %d of %d X edges' % (ne, c['k'])); cv = 'xparse'
        else: cv = 'inadm'
    # status
    bad = []
    if c['label'] == 'D':
        if kv != 'D': bad.append('KILL:kc-notD')
        if cv != 'D': bad.append('cfast-notD')
    else:
        if kleft != '-' and cleft != '-' and kleft != cleft: bad.append('KILL:leftover-mismatch')
        if kv not in ('C', 'D') or cv not in ('C', 'D'): bad.append('unconfirmed')
        for e in ('kc', 'cf'):
            if e + '_reached' in r and int(r[e + '_classes']) - int(r[e + '_reached']) != c['bad']: notes.append(e + ' unreached!=rsst_bad')
    for e in ('kc', 'cf'):
        if e + '_ext' in r and int(r[e + '_ext']) != c['ext']: notes.append(e + ' ext!=rsst')
    if 'kc_ext' in r and 'cf_ext' in r and (r['kc_classes'], r['kc_ext'], r['kc_reached']) != (r['cf_classes'], r['cf_ext'], r['cf_reached']):
        notes.append('kc/cf classes-ext-reached differ')
    r.update(kc_verdict=kv, kc_mode=kmode, kc_leftover=kleft, cf_verdict=cv, cf_leftover=cleft,
             status=('|'.join(bad) if bad else 'OK'), notes=';'.join(notes) or '-', secs='%.1f' % (time.time() - t0))
    return r

def main():
    done = set()
    if os.path.exists(OUT):
        for ln in open(OUT):
            if ln.startswith('idx'): continue
            done.add(int(ln.split('\t')[0]))
    else: open(OUT, 'w').write('\t'.join(COLS) + '\n')
    cs = sorted(conv.load(), key=lambda c: (c['r'], c['idx']))
    for c in cs:
        if c['idx'] in done or c['r'] > MAXR: continue
        r = one(c)
        with open(OUT, 'a') as f: f.write('\t'.join(str(r.get(k, '-')) for k in COLS) + '\n'); f.flush()
        print(r['idx'], r['name'], r['ring'], r['label'], r['status'], r['secs'], flush=True)
    print('DONE', flush=True)

if __name__ == '__main__': main()
