import sys, os, json, collections, itertools, io, contextlib
eng, args, kill, cert, out = sys.argv[1:6]
root='/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis'
sys.argv = [os.path.join(eng,'pcheck.py'), 'none', 'xon','apexcls','filt16','hat5','killtab='+kill,'root='+root,'args='+args,'work=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/chk4/work']
__file__ = sys.argv[0]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(open(sys.argv[0]).read(), sys.argv[0], 'exec'))
# replicate R2_sender_rows without dedup (hat5 only: ZH, F5 off)
allc = collections.defaultdict(list)
for w in SENDERS:
    n = 5; sixes = [k for k in range(n) if w[k] == 6]
    allow = {k: {(a_, q, b_) for a_ in LET for q in LET for b_ in LET if not isR6((5, w[(k + 1) % n], a_, q, b_, w[(k - 1) % n]))} for k in sixes}
    base = collections.Counter()
    for j in range(n):
        if w[j] >= 7: base[('y', root(list(w), j))] += 1
    for hb in itertools.product((0, 1), repeat=5):
        H = dict(enumerate(hb))
        for fb in itertools.product((0, 1), repeat=len(sixes)):
            Fn = dict(zip(sixes, fb))
            if not all(any((a_, q, b_) in allow[k] for a_ in CLS2[H[k]] for q in CLS2[Fn[k]] for b_ in CLS2[H[(k - 1) % n]]) for k in sixes): continue
            cf = collections.Counter(base)
            for k in range(n):
                if H[k]: cf[('r', h5_sender(w, H, Fn, k))] += 1
            for k in sixes:
                L5 = lambda c: 7 if c else 5
                cf[('g', g2_of(w[(k + 1) % n], L5(H[k]), L5(Fn[k]), L5(H[(k - 1) % n]), w[(k - 1) % n], w[(k + 2) % n], w[(k - 2) % n]))] += 1
            allc[(''.join(map(str, w)), tuple(sorted(cf.items())))].append([list(hb), list(fb)])
SR = R2_sender_rows(); print('rows', len(SR), 'cf classes', len(allc))
C = json.load(open(cert)); res = []
for c in C:
    if c['row'][0] != 'senderR2': continue
    wd, bits = c['row'][1], c['row'][2]; j = bits.index('|')
    m = [cf for w_, cf, b in SR if w_ == wd and b == bits]; assert len(m) == 1
    key = (wd, tuple(sorted(m[0].items())))
    res.append({'word': wd, 'H': bits[:j], 'F': bits[j+1:], 'w': c['w'], 'ctx': allc[key]})
json.dump(res, open(out, 'w')); print('cert sender rows', len(res), 'with >1 context', sum(len(r['ctx']) > 1 for r in res))
