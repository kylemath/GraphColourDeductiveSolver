# Soft (differentiable) version of the network, trained by Adam on a smooth maximum of the row bounds.
# Same bound structure as net.exact (max over hidden letters, max over neighbour rows per view), with softmax attention.
import pickle, time, sys, os, numpy as np, torch
import net as NT
torch.set_num_threads(4)   # leave the machine usable

def tensors(B, dev):
    T = lambda a, dt=torch.long: torch.as_tensor(np.asarray(a), dtype=dt, device=dev)
    live = ~B['excused']
    return dict(P7=T(B['P7']), is7=T(B['is7'], torch.bool), vX=T(np.where(B['is7'], B['vX'], 0)), cX=T(np.where(B['is7'], B['cX'], 0)),
                srow=T(B['srow']), sslot=T(B['sslot']), sview=T(B['sview']), F=T(B['F'], torch.float32), P5=T(B['P5']), O6=T(B['O6']),
                I6=T(B['I6']), has7=T(B['has7'], torch.bool), live=T(live, torch.bool), nview=B['nview'])

def forward(D, Praw, theta, W, tau):
    Pf = torch.cat([torch.relu(Praw), Praw.new_zeros(1)])
    c1 = -60 + Pf[D['P7']].amax(2).sum(1)
    sc = (D['F'] @ W)[D['cX']] / tau
    sc = sc.masked_fill(~D['is7'], -1e9)
    sh = torch.softmax(sc, 1) * D['is7']
    sur = torch.relu(c1 - theta) * D['has7']
    fwd = sur[:, None] * sh
    vals = fwd[D['srow'], D['sslot']]
    M = vals.new_zeros(D['nview']).scatter_reduce(0, D['sview'], vals, reduce='amax', include_self=True)
    own = torch.where(D['has7'], torch.minimum(c1, theta), c1)
    f7 = own + (M[D['vX']] * D['is7']).sum(1)
    f5 = 60 - Pf[D['P5']].sum(1)
    f6 = -Pf[D['O6']].sum(1) + Pf[D['I6']].amax(2).sum(1)
    return f7[D['live']], f5, f6, sh

def train(B, P0, theta0, steps=3000, dev='cpu', lr=0.05, l1=1e-4, seed=0, log=print):
    torch.manual_seed(seed)
    D = tensors(B, dev)
    Praw = torch.tensor(np.asarray(P0, dtype=np.float32), device=dev, requires_grad=True)
    theta = torch.tensor(float(theta0), device=dev, requires_grad=True)
    W = (0.01 * torch.randn(B['F'].shape[1], device=dev)).requires_grad_(True)
    opt = torch.optim.Adam([{'params': [Praw], 'lr': lr}, {'params': [theta], 'lr': lr}, {'params': [W], 'lr': lr}])
    best = (1e9, None); T0 = time.time()
    for it in range(steps):
        frac = it / max(steps - 1, 1)
        beta = 0.2 * (50 ** frac)          # temperature of the smooth max: 0.2 -> 10
        tau = 1.0 * (0.05 ** frac)         # attention temperature 1 -> 0.05 (towards hard top sets)
        f7, f5, f6, _ = forward(D, Praw, theta, W, tau)
        allf = torch.cat([f7, f5, f6])
        loss = torch.logsumexp(beta * allf, 0) / beta + l1 * (torch.relu(Praw).sum() + W.abs().sum())
        opt.zero_grad(); loss.backward(); opt.step()
        mx = float(allf.max())
        if mx < best[0]: best = (mx, (Praw.detach().cpu().numpy().copy(), float(theta), W.detach().cpu().numpy().copy(), tau))
        if it % 250 == 0 or it == steps - 1:
            log('  step %5d beta %.2f tau %.3f  soft max final %.4f  theta %.2f  |W|1 %.2f [%.0fs]' % (it, beta, tau, mx, float(theta), float(W.abs().sum()), time.time() - T0))
    return best
