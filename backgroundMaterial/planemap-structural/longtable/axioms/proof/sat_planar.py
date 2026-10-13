"""Planar version of the T1-v SAT search (Long Table PROOF-ATTEMPT-1).

In the Hamiltonian normal form (sat_t1v.Enc, mode 'ham') G = H + C, with H = 0,1,...,n-1 and v = 0.
G is planar with the rotation f0..f4 at v (up to mirror) iff the chord diagram on the circle
  1, 2, ..., n-1, [f4], [f1], [f3]        (v blown up between n-1 and 1; f0 = (0,n-1), f2 = (0,1))
admits a side 2-colouring with no two same-side chords crossing and side(f1) != side(f3) = side(f4).
(Derivation in PROOF-ATTEMPT-1.md, section 1.)  We add exactly these clauses.  On a plane graph A5v and the
chain-parity law hold automatically, so a planar window/orbit is a genuine NRC-M object (sphere).
usage: sat_planar.py closed n L [tlimit]  |  sat_planar.py window n W [tlimit] [--enum]"""
import sys, json, time
from sat_t1v import Enc, run, to_line
from pysat.solvers import Cadical153

VPOS = {4: 0.25, 1: 0.50, 3: 0.75}


class PEnc(Enc):
    def __init__(self, n, L, axv=1, closed=True, **kw):
        super().__init__(n, L, axv, eager=1, closed=closed, **kw)
        self._planar()

    def _planar(self):
        n, P = self.n, self.pool
        side = {}
        items = []   # (pos_a, pos_b, presence-literals, side literal)
        for e, (a, b) in enumerate(self.edges):
            if e in self.H or a == 0 or b == 0: continue
            sv = P.id(('side', e)); side[e] = sv
            items.append((a, b, [self.X[e]], sv))
        sl = {s: P.id(('vside', s)) for s in (1, 3, 4)}
        # side(f1) != side(f3) = side(f4)
        self.add([sl[1], sl[3]]); self.add([-sl[1], -sl[3]])
        self.add([-sl[3], sl[4]]); self.add([sl[3], -sl[4]])
        for e in self.vedges:
            if e in self.H: continue
            a, b = self.edges[e]; j = b if a == 0 else a
            for s in (1, 3, 4):
                items.append((j, n + VPOS[s], [self.lab[s][e]], sl[s]))
        def cross(c, d):
            a1, b1 = sorted(c); a2, b2 = sorted(d)
            return (a1 < a2 < b1) != (a1 < b2 < b1)
        cnt = 0
        for i in range(len(items)):
            a1, b1, l1, s1 = items[i]
            for j in range(i + 1, len(items)):
                a2, b2, l2, s2 = items[j]
                if len({a1, b1, a2, b2}) < 4: continue
                if not cross((a1, b1), (a2, b2)): continue
                if s1 == s2: 
                    self.add([-x for x in l1 + l2]); continue
                pre = [-x for x in l1 + l2]
                self.add(pre + [s1, s2]); self.add(pre + [-s1, -s2]); cnt += 1
        self.ncross = cnt


if __name__ == '__main__':
    mode, n, L = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 550
    enc = PEnc(n, L, 1, closed=(mode == 'closed'), word='1212')
    t0 = time.time()
    if '--enum' not in sys.argv:
        st, sols, stats = run(enc, tl, verbose=False)
        print(json.dumps(dict(mode=mode, n=n, L=L, status=st, **stats)), flush=True)
        for E, M, fv, info in sols: print('SOL', to_line(enc, E, fv), info)
    else:
        s = Cadical153(bootstrap_with=enc.cl); nsol = 0; status = 'DONE'
        while True:
            if time.time() - t0 > tl: status = 'TIMEOUT'; break
            if not s.solve(): break
            E, M, fv = enc.decode(s.get_model())
            cuts, info = enc.check(E, M, fv)
            if cuts:
                for c in cuts: s.add_clause(c)
                continue
            ch = [enc.edges[e] for e in E if enc.X[e] is not None]
            print(json.dumps(dict(n=n, W=L, chords=ch, fv=[enc.edges[e] for e in fv],
                                  M=[sorted(enc.edges[e] for e in M[t]) for t in range(L)], word=info['word'])), flush=True)
            nsol += 1
            s.add_clause([-enc.X[e] for e in E if enc.X[e] is not None] + [-enc.lab[sv][fv[sv]] for sv in (1, 3, 4)])
        print(json.dumps(dict(mode='enum', n=n, W=L, nsol=nsol, status=status, sec=round(time.time() - t0, 1))), file=sys.stderr)
