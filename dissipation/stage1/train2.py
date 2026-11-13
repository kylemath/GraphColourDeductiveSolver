# Soft three-round model (net2) trained by Adam on a smooth max of every live row bound. Same bound structure as net2.exact.
# usage: python3 train2.py SEED STEPS [init.pkl with P/th7/th6 from an LP solution]
import pickle, sys, time, numpy as np, torch
import net2 as N2
torch.set_num_threads(2)

def T(a, dt=torch.long): return torch.as_tensor(np.asarray(a), dtype=dt)
def prep(B):
    A7, A6 = B['A7'], B['A6']
    D = dict(IN7=T(A7['IN']), IN6=T(A6['IN']), OUT6=T(A6['OUT']), P5=T(B['P5']),
             t2m=T(A7['tgt2'] >= 0, torch.bool), t2c=T(np.maximum(A7['tgt2'], 0)), t3m=T(A6['tgt3'] >= 0, torch.bool), t3c=T(np.maximum(A6['tgt3'], 0)),
             r2v7m=T(A7['r2v'] >= 0, torch.bool), r2v7=T(np.maximum(A7['r2v'], 0)), r3v7m=T(A7['r3v'] >= 0, torch.bool), r3v7=T(np.maximum(A7['r3v'], 0)),
             r2v6m=T(A6['r2v'] >= 0, torch.bool), r2v6=T(np.maximum(A6['r2v'], 0)),
             s7=T(A7['src']), s6=T(A6['src']), F2=T(B['F2'], torch.float32), F3=T(B['F3'], torch.float32),
             live7=T(~A7['excused'], torch.bool), live6=T(~A6['excused'], torch.bool), nV2=B['nV2'], nV3=B['nV3'])
    D['has2'] = D['t2m'].any(1); D['has3'] = D['t3m'].any(1)
    return D

def smax(sc, mask, tau):
    return torch.softmax((sc / tau).masked_fill(~mask, -1e9), 1) * mask

def forward(D, Praw, th7, th6, W2, W3, tau):
    Pf = torch.cat([torch.relu(Praw), Praw.new_zeros(1)])
    c7 = -60 + Pf[D['IN7']].amax(2).sum(1)
    c6 = Pf[D['IN6']].amax(2).sum(1) - Pf[D['OUT6']].sum(1)
    sh2 = smax((D['F2'] @ W2)[D['t2c']], D['t2m'], tau)
    f2 = torch.relu(c7 - th7)[:, None] * sh2 * D['has2'][:, None]
    s = D['s7']; M2 = f2.new_zeros(D['nV2']).scatter_reduce(0, s[:, 2], f2[s[:, 0], s[:, 1]], 'amax', include_self=True)
    c26 = c6 + (M2[D['r2v6']] * D['r2v6m']).sum(1)
    sh3 = smax((D['F3'] @ W3)[D['t3c']], D['t3m'], tau)
    f3 = torch.relu(c26 - th6)[:, None] * sh3 * D['has3'][:, None]
    s = D['s6']; M3 = f3.new_zeros(D['nV3']).scatter_reduce(0, s[:, 2], f3[s[:, 0], s[:, 1]], 'amax', include_self=True)
    f7 = torch.where(D['has2'], torch.minimum(c7, th7), c7) + (M2[D['r2v7']] * D['r2v7m']).sum(1) + (M3[D['r3v7']] * D['r3v7m']).sum(1)
    f6 = torch.where(D['has3'], torch.minimum(c26, th6), c26)
    f5 = 60 - Pf[D['P5']].sum(1)
    return torch.cat([f7[D['live7']], f6[D['live6']], f5])

def train(B, P0, th70, th60, steps, seed, l1=1e-4, lr=0.05, log=print):
    torch.manual_seed(seed); D = prep(B)
    Praw = T(P0, torch.float32).clone().requires_grad_(True)
    th7 = torch.tensor(float(th70), requires_grad=True); th6 = torch.tensor(float(th60), requires_grad=True)
    W2 = (0.01 * torch.randn(B['F2'].shape[1])).requires_grad_(True); W3 = (0.01 * torch.randn(B['F3'].shape[1])).requires_grad_(True)
    opt = torch.optim.Adam([Praw, th7, th6, W2, W3], lr=lr)
    best = (1e9, None); T0 = time.time()
    for it in range(steps):
        fr = it / max(steps - 1, 1); beta = 0.2 * 50 ** fr; tau = 0.05 ** fr
        f = forward(D, Praw, th7, th6, W2, W3, tau)
        loss = torch.logsumexp(beta * f, 0) / beta + l1 * (torch.relu(Praw).sum() + W2.abs().sum() + W3.abs().sum())
        opt.zero_grad(); loss.backward(); opt.step()
        mx = float(f.max())
        if mx < best[0]: best = (mx, dict(P=Praw.detach().numpy().copy(), th7=float(th7), th6=float(th6), W2=W2.detach().numpy().copy(), W3=W3.detach().numpy().copy(), tau=tau))
        if it % 250 == 0 or it == steps - 1: log('  step %5d beta %.2f tau %.3f soft max %.4f th7 %.2f th6 %.2f [%.0fs]' % (it, beta, tau, mx, float(th7), float(th6), time.time() - T0), flush=True)
    return best

if __name__ == '__main__':
    B = pickle.load(open('cache_B2.pkl', 'rb'))
    seed, steps = int(sys.argv[1]), int(sys.argv[2])
    if len(sys.argv) > 3: I = pickle.load(open(sys.argv[3], 'rb')); P0, a, b = I['P'], I['th7'], I['th6']
    else: P0, a, b = np.full(N2.NPAR, 6.0), 6.0, 6.0
    best = train(B, P0, a, b, steps, seed)
    print('seed %d: best soft max %.4f' % (seed, best[0]), flush=True)
    pickle.dump(best, open('runs2/soft2_s%d_%d.pkl' % (seed, steps), 'wb'))
