# Necklace geometry: A = chain of k+1 blobs P0..Pk hanging from the top edge of U, consecutive blobs joined by a
# single internal chord (a neck); B = U \ A wraps around the necklace.  The seam (= dA cap dB) crosses
# 2k+1 pocket stretches of A.  Everything lives in the flat triangular lattice (all interior degrees 6).
import math
from lat import Lat, disc_info

def build(k, h=3, M=3.0, mside=6, mbot=6, top=None):
    """k = number of necks (chords).  Neck n (n=1..k) on row 2hn.  Blob n occupies rows 2hn .. 2h(n+1);
       P0 occupies rows 0..2h (row 0 = top row of U).  Half-width at distance d from the nearest neck:
       min(0.5+0.5d, M).  Rows increase downward in the picture (j is the lattice row)."""
    X0 = 0.5
    J = 2*h*(k+1)                     # last row of the tip blob
    Jbot = J + mbot
    W = M + mside
    def hw_A(j):
        if j < 0 or j > J: return None
        if j <= 2*h:                  # P0: widen from neck 1 upward
            d = 2*h - j
        else:
            n = j // (2*h)
            if j == 2*h*n: d = 0
            else: d = min(j - 2*h*n, 2*h*(n+1) - j)
            if n == k:                # tip blob: taper only toward neck k and toward the tip row J
                d = min(j - 2*h*k, J - j)
        return min(0.5 + 0.5*d, M)
    pts = []; Apts = set(); Upts = set()
    for j in range(-2, Jbot + 3):
        for i in range(math.floor(X0 - W - 4 - j/2.0), math.ceil(X0 + W + 4 - j/2.0) + 1):
            x = i + j/2.0
            if abs(x - X0) > W + 3: continue
            pts.append((i, j))
            if 0 <= j <= Jbot and abs(x - X0) <= W + 1e-9:
                Upts.add((i, j))
                hw = hw_A(j)
                if hw is not None and abs(x - X0) <= hw + 1e-9: Apts.add((i, j))
    g = Lat(pts)
    A = set(g.id[p] for p in Apts); U = set(g.id[p] for p in Upts); B = U - A
    # blob label: row-based (neck rows belong to both blobs; label them with the upper blob)
    blob = {}
    for p in Apts:
        j = p[1]; blob[g.id[p]] = 0 if j <= 2*h else min(k, (j - 1)//(2*h))
    return g, A, B, U, blob

if __name__ == '__main__':
    import sys
    import pysat_stub, wk
    for k in (1, 2, 4):
        g, A, B, U, blob = build(k)
        dA, dB, dU = disc_info(g, A), disc_info(g, B), disc_info(g, U)
        DA = wk.Disc(g, A); DB = wk.Disc(g, B); DU = wk.Disc(g, U)
        print(k, 'nA', len(A), 'nB', len(B), 'nU', len(U), 'chordsA', len(dA['chords']), len(DA.chords),
              'pocketsA', len(DA.pockets), 'chordsB', len(DB.chords), 'chordsU', len(DU.chords))
