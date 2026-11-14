"""Idea C (receiver level): do the SP/ST parts act as a relaxation of the RSST charge?
For each receiver class: E0 = 60(6-d) + RSST(drule) net inflow (expected), S = SP net inflow, T = ST net."""
import numpy as np, collections as C
from common import *
P = load()
pre = np.array([p['pre'] for p in P])
dr = pre == 'drule'; sp = pre == 'SP_'; st = (pre == 'STm_') | (pre == 'STp_')
A = np.load('../real58.npz'); B = np.load('../real911.npz')
for z, ds in ((A, (5, 6, 7, 8)), (B, (9, 10, 11))):
    for d in ds:
        M = z[f'M{d}'].astype(float); O = z[f'O{d}'].astype(float)
        E0 = 60 * (6 - d) + M[:, dr].sum(1); S = M[:, sp].sum(1); T = M[:, st].sum(1)
        F = E0 + S + T
        w = O / O.sum()
        def cor(a, b):
            a = a - (w * a).sum(); b = b - (w * b).sum()
            den = np.sqrt((w * a * a).sum() * (w * b * b).sum())
            return (w * a * b).sum() / den if den > 0 else float('nan')
        print(f'd={d} classes={len(O)}  E0>0: {int((E0>1e-6).sum())}  final>0: {int((F>1e-6).sum())}  max E0 {E0.max():.1f} max final {F.max():.1f}'
              f'  SP touched {int((np.abs(S)>1e-6).sum())}  corr(E0,S)={cor(E0,S):.3f}  corr(E0,T)={cor(E0,T):.3f}')
        if d in (7, 8):
            # bucket E0
            for lo, hi in ((-1e9, -30), (-30, -12), (-12, -3), (-3, 3), (3, 12), (12, 1e9)):
                m = (E0 > lo) & (E0 <= hi)
                if m.sum(): print(f'    E0 in ({lo},{hi}]: n={int(m.sum())} mean SP net {S[m].mean():+.2f}  share with SP<0 {np.mean(S[m]<-1e-6):.2f}  SP>0 {np.mean(S[m]>1e-6):.2f} mean final {F[m].mean():+.2f}')
