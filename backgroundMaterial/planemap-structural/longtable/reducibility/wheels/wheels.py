import sys, time, io, contextlib
sys.path.insert(0, '..')
import dred
def wheel(word):
    # interior: 0 = hole v, 1..5 = neighbours x_0..x_4 with degrees word[i]; ring: per x_i: shared s_{i-1}, (d_i-5) privates, then s_i
    ring = []; sidx = {}
    for i, d in enumerate(word):
        for p in range(d - 5): ring.append(('p', i, p))
        ring.append(('s', i))                # s_i shared by x_i and x_{i+1}
    pos = {v: k for k, v in enumerate(ring)}
    r = len(ring); m = 6
    ringadj = [[] for _ in range(m)]; intadj = [[] for _ in range(m)]
    for i, d in enumerate(word):
        a = 1 + i
        ringadj[a] = [pos[('s', (i - 1) % 5)]] + [pos[('p', i, p)] for p in range(d - 5)] + [pos[('s', i)]]
        intadj[a] = [0, 1 + (i + 1) % 5, 1 + (i - 1) % 5]
    intadj[0] = [1, 2, 3, 4, 5]
    return r, ringadj, intadj, m
words = ['55555', '55556', '55566', '55656', '55666', '56566', '56666', '66666', '55557', '55567', '66667']
for w in words:
    W = [int(c) for c in w]
    r, ra, ia, m = wheel(W)
    t = time.time()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = dred.closure(r, ra, ia, m, verbose=False)
    allc, good, lev = res; print(w, "ring", r, "ring colourings", len(allc), "extend directly", len(lev[0]), "fixable vs every outside", len(good), "levels", len(lev), "D-REDUCIBLE" if len(good) == len(allc) else "not D-reducible", "%.1fs" % (time.time() - t), flush=True)
