# s86 OP-23 repair ladder.  usage: python3 repladder.py <runtag> <in-point sol> [poll seconds]
# Watches eng/sol_<runtag>_lp.json (the K run's per-iteration LP point).  For each new LP point x_LP and the best feasible point x_in
# (t_in), evaluates the repaired blend t_rep(l) = t(blend) + max excess over every violated row (exact upperR2 + vfile, conservation
# worst excess included; any violated sender row or Karp-tail row makes l invalid) on a lambda grid, refines around the best, and if
# t_rep < t_in builds the point at t_rep + 2e-9, rechecks it (upperR2 must say FEASIBLE) and makes it the new x_in.
# Raising t relaxes every window / conservation row, so the repaired blend is feasible once its own recheck passes.
import json, os, re, subprocess, sys, time, hashlib
N = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(N)
TAG = sys.argv[1]; POLL = int(sys.argv[3]) if len(sys.argv) > 3 else 60
R = os.path.join(N, 'repl_' + TAG + os.environ.get('REPL_FAM', '')); os.makedirs(R, exist_ok=True)
SWARM = '/mnt/project-files/swarm/round6/W12-studio-K/from_opus/s86_' + TAG
LPF = os.path.join(N, 'eng', 'sol_%s_lp.json' % TAG)
FAM = ['c6le', 'f2b7', 'f2b=%s/rules/A5final/rules_c67fa1d1_plus_A5_twins.json' % N, 'rpatN=' + os.environ.get('REPL_RPATN', '%s/rpat/rpatN3_rotation_justified.txt' % N)]   # s86: REPL_RPATN=A,B adds offc for GS4
ENV = dict(os.environ, STACK='s77', ARGS=os.environ.get('REPL_ARGS', os.path.join(N, 'args_A97_F_W13K3c.txt')), KEYS=os.environ.get('REPL_KEYS', os.path.join(B, 's85_edge56', 'keys', 'cg_keys_r13.txt')))
def log(s):
    line = '%s [s86REP-%s] %s' % (time.strftime('%H:%M:%SZ', time.gmtime()), TAG, s)
    print(line, flush=True); open(os.path.join(N, 'run.log'), 'a').write(line + '\n')
def md5(fn): return hashlib.md5(open(fn, 'rb').read()).hexdigest()[:8]
def blend(fin, flp, lam, fout):
    a = json.load(open(fin)); b = json.load(open(flp)); o = dict(b)
    for k in set(a) | set(b):
        va, vb = a.get(k), b.get(k)
        if k == 't': o[k] = (1 - lam) * va + lam * vb; continue
        if isinstance(va, dict) or isinstance(vb, dict):
            va = va or {}; vb = vb or {}
            if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in list(va.values()) + list(vb.values())): o[k] = vb; continue
            o[k] = {kk: (1 - lam) * va.get(kk, 0.0) + lam * vb.get(kk, 0.0) for kk in set(va) | set(vb)}
        elif isinstance(va, list) or isinstance(vb, list):
            da = {json.dumps(x[0]): x[1] for x in (va or [])}; db = {json.dumps(x[0]): x[1] for x in (vb or [])}
            o[k] = [[json.loads(kk), (1 - lam) * da.get(kk, 0.0) + lam * db.get(kk, 0.0)] for kk in sorted(set(da) | set(db))]
    o.pop('note', None); json.dump(o, open(fout, 'w')); return o['t']
def check(tag, sol, vfile=True, th=1):
    vf = os.path.join(N, 'logs', 'viol_%s.txt' % tag)
    if os.path.exists(vf): os.remove(vf)
    while int(open('/proc/meminfo').read().split('MemAvailable:')[1].split()[0]) // 1024 < int(os.environ.get('REPL_MINMEM', '4500')): time.sleep(20)   # s86: memory gate (8 Nov crash)
    subprocess.run(['bash', os.path.join(N, 'U86.sh'), tag, sol, str(th)] + FAM + (['vK=1000000', 'vfile=' + vf] if vfile else []), env=ENV, cwd=N,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    L = open(os.path.join(N, 'logs', 'upper_%s.log' % tag)).read()
    if 'Traceback' in L or 'UPPER-R2' not in L: return None, L
    return vf, L
def t_rep(tag, sol):
    vf, L = check(tag, sol)
    if vf is None: return float('inf'), 'no verdict'
    t = float(re.search(r'at t = ([0-9.e-]+)', L).group(1))
    if 'UPPER-R2: FEASIBLE' in L: return t, 'feasible as is'
    if int(re.search(r'sender rows violated: (\d+)', L).group(1)): return float('inf'), 'senders'
    if re.search(r'exact pattern-free: [1-9]', L): return float('inf'), 'tail'
    c = re.search(r'worst excess ([0-9.e+-]+)\)', L); ce = float(c.group(1)) if c else 0.0
    we = max([float(l.split()[2]) for l in open(vf)] or [0.0]) if os.path.exists(vf) else 0.0
    nv = re.search(r'INFEASIBLE \((\d+)\)', L)
    if nv and not os.path.exists(vf) and int(nv.group(1)): return float('inf'), 'no vfile'
    return t + max(ce, we), 'cons %.3g win %.3g' % (ce, we)
def search(xin, xlp, k):
    res = {}
    def ev(lams):
        ps = []
        for lam in lams:
            if lam in res: continue
            sol = os.path.join(R, 'b%d_%g.json' % (k, lam)); blend(xin, xlp, lam, sol)
            tg = 'REP%s_%s_%d_%g' % (TAG, os.environ.get('REPL_FAM', ''), k, lam)
            ps.append((lam, tg, sol))
        PAR = int(os.environ.get('REPL_PAR', '2'))
        for i in range(0, len(ps), PAR):   # PAR checks at a time (1 thread each)
            out = {}
            import threading
            def run(lam, tg, sol): out[lam] = t_rep(tg, sol)
            th = [threading.Thread(target=run, args=p) for p in ps[i:i + PAR]]
            [x.start() for x in th]; [x.join() for x in th]
            res.update(out)
    ev([0.02, 0.05, 0.1, 0.2])
    best = min(res, key=lambda l: res[l][0])
    ev([round(best / 1.5, 5), round(min(best * 1.5, 0.95), 5)] if best < 0.2 else [0.3, 0.45])
    best = min(res, key=lambda l: res[l][0])
    ev([round(best / 1.2, 5), round(best * 1.2, 5)])
    best = min(res, key=lambda l: res[l][0])
    # E(l) = t_rep(l) - t_blend(l) is convex piecewise linear with E(0) = 0.  When the best is the smallest l tried, the minimum is
    # usually the kink where E leaves 0: extend the secant through the two smallest l to E = 0 (it lies below E there, so the zero
    # found is >= the true one); evaluate, and repeat from the new point.
    ti = json.load(open(xin))['t']; tl = json.load(open(xlp))['t']
    for _ in range(3):
        ls = sorted(res)
        if best != ls[0] or len(ls) < 2: break
        E1 = res[ls[0]][0] - ((1 - ls[0]) * ti + ls[0] * tl); E2 = res[ls[1]][0] - ((1 - ls[1]) * ti + ls[1] * tl)
        if not (1e-12 < E1 < E2 < 1e9): break
        l0 = round(ls[0] - E1 * (ls[1] - ls[0]) / (E2 - E1), 6)
        if not (1e-5 < l0 < ls[0]) or l0 in res: break
        ev([l0]); best = min(res, key=lambda l: res[l][0])
    # interior best: t_rep is convex piecewise linear, so the secant through (left neighbour, best) and the secant through the two
    # finite points right of best both lie below t_rep between best and its right neighbour (likewise mirrored); evaluate at their
    # crossing, which is near the kink the grid straddles.
    for _ in range(2):
        ls = [l for l in sorted(res) if res[l][0] < 1e9]; i = ls.index(best) if best in ls else -1
        if i < 1 or i + 1 >= len(ls): break
        cands = []
        for a, b, c, d in ((ls[i - 1], best, ls[i + 1], ls[i + 2] if i + 2 < len(ls) else None), (ls[i - 2] if i >= 2 else None, ls[i - 1], best, ls[i + 1])):
            if a is None or d is None: continue
            s1 = (res[b][0] - res[a][0]) / (b - a); s2 = (res[d][0] - res[c][0]) / (d - c)
            if s2 - s1 <= 1e-12: continue
            x = round((res[c][0] - s2 * c - res[b][0] + s1 * b) / (s1 - s2), 6)
            if b < x < c and x not in res: cands.append(x)
        if not cands: break
        ev(cands[:2]); nb = min(res, key=lambda l: res[l][0])
        if nb == best: break
        best = nb
    log('it-point %d: ' % k + ' '.join('l=%g:%s' % (l, ('%.6f' % res[l][0]) if res[l][0] < 1e9 else res[l][1]) for l in sorted(res)) + ' -> best l=%g t_rep %.9f' % (best, res[best][0]))
    return best, res[best][0]
def main():
    xin = os.path.abspath(sys.argv[2]); tin = json.load(open(xin))['t']; k = int(os.environ.get('REPL_K0', '0'))
    last = os.path.getmtime(LPF) if os.path.exists(LPF) and os.environ.get('REPL_SKIPCUR') else None   # skip the LP point already processed by hand
    log('start: in-point %s (md5 %s) t = %.12f; watching %s; family %s (md5 %s), keys %s (md5 %s)' % (os.path.basename(xin), md5(xin), tin, os.path.basename(LPF), os.path.basename(ENV['ARGS']), md5(ENV['ARGS']), os.path.basename(ENV['KEYS']), md5(ENV['KEYS'])))
    init = [f for f in os.environ.get('REPL_INIT', '').split(',') if f]
    while True:
        if init:
            src = init.pop(0); k += 1; xlp = os.path.join(R, 'lp_%02d.json' % k); open(xlp, 'wb').write(open(src, 'rb').read())
            tl = json.load(open(xlp))['t']; log('initial LP point %d = %s (t %.9f)' % (k, src, tl))
            xin, tin = step(xin, tin, xlp, tl, k); continue
        alive = subprocess.run(['pgrep', '-f', 'tag=%s ' % TAG], stdout=subprocess.DEVNULL).returncode == 0
        if os.path.exists(LPF) and os.path.getmtime(LPF) != last:
            time.sleep(20); last = os.path.getmtime(LPF); k += 1
            xlp = os.path.join(R, 'lp_%02d.json' % k); open(xlp, 'wb').write(open(LPF, 'rb').read())
            tl = json.load(open(xlp))['t']
            xin, tin = step(xin, tin, xlp, tl, k)
        elif not alive:
            log('run %s gone; stopping' % TAG); return
        time.sleep(POLL)
def step(xin, tin, xlp, tl, k):
            if tl >= tin: log('LP point %d t %.9f >= t_in, skipped' % (k, tl)); return xin, tin
            lam, tr = search(xin, xlp, k)
            if tr < tin - 1e-7:
                o = json.load(open(os.path.join(R, 'b%d_%g.json' % (k, lam)))); tb = o['t']; o['t'] = tr + 2e-9
                o['note'] = 's86 OP-23 repaired blend: (1-%g) * %s (md5 %s, t %.12f) + %g * %s LP point %d (t %.9f); t = blend t %.12f + max excess, + 2e-9' % (lam, os.path.basename(xin), md5(xin), tin, lam, TAG, k, tl, tb)
                cand = os.path.join(N, 'cand', 'sol_rep%s%s_%02d.json' % (TAG[-2:], os.environ.get('REPL_FAM', ''), k)); json.dump(o, open(cand, 'w'))
                tg = 'F_rep%s%s_%02d' % (TAG[-2:], os.environ.get('REPL_FAM', ''), k); vf, L = check(tg, cand, vfile=False, th=2)
                if vf is not None and 'UPPER-R2: FEASIBLE' in L:
                    log('NEW IN-POINT %s (md5 %s) FEASIBLE at t = %.12f (was %.12f)' % (os.path.basename(cand), md5(cand), o['t'], tin))
                    xin, tin = cand, o['t']
                    ij = os.path.join(N, 'eng', 'inject_%s.json' % TAG); open(ij + '.tmp', 'wb').write(open(cand, 'rb').read()); os.replace(ij + '.tmp', ij)   # the K run (inject_in) takes it as its in-point
                    if os.environ.get('REPL_ARGS2'):
                        e2 = dict(ENV, ARGS=os.environ['REPL_ARGS2']); tg2 = tg + '_sub'
                        subprocess.run(['bash', os.path.join(N, 'U86.sh'), tg2, cand, '1'] + FAM, env=e2, cwd=N, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        L2 = open(os.path.join(N, 'logs', 'upper_%s.log' % tg2)).read()
                        log('  same point on %s: %s' % (os.path.basename(os.environ['REPL_ARGS2']), (re.findall(r'UPPER-R2.*', L2) or ['no verdict'])[-1]))
                    if os.path.isdir(SWARM):
                        for f in (cand, os.path.join(N, 'logs', 'upper_%s.log' % tg)): subprocess.run(['cp', f, SWARM])
                        open(os.path.join(SWARM, 'REPLADDER.txt'), 'a').write('%s %s md5 %s t %.12f FEASIBLE (OP-23 repaired blend, l = %g of LP point %d)\n' % (time.strftime('%H:%M:%SZ', time.gmtime()), os.path.basename(cand), md5(cand), tin, lam, k))
                else: log('recheck of %s did NOT pass: %s' % (os.path.basename(cand), (re.findall(r'UPPER-R2.*', L) or ['no verdict'])[-1]))
            for f in os.listdir(R):
                if f.startswith('b%d_' % k): os.remove(os.path.join(R, f))
            return xin, tin
main()
