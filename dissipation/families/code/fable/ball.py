"""Concrete hub 2-ball evaluator (all second-ring degrees assigned), built on behav.W2B/fit_part.
Third-ring vertices are 'open': upper reading = they fit anything, lower reading = they fit only FULL."""
import random, numpy as np
from common import *
from behav import W2B, fit_part, to3, npriv

class Ball(W2B):
    def __init__(self, d, link, asg, lower=False):
        super().__init__(d, link); self.asg = asg; self.lower = lower
    def deg_info(self, v):
        k, val = super().deg_info(v)
        if k == 'var': return ('dec', self.asg[val])
        if k == 'open' and self.lower: return ('dec', -1)
        return (k, val)

def variables(d, link):
    vs = [100 + i for i in range(d)]
    for i in range(d):
        for j in range(npriv(link[i])): vs.append(200 + 3 * i + j)
    return vs

class Rules:
    def __init__(self, P):
        self.P = P; self.S3 = [to3(p['slots']) for p in P]
        self.byhub = {}
        for k, p in enumerate(P): self.byhub.setdefault(p['hub'], []).append(k)
    def out(self, W, sel=None):
        """dict spoke index -> {pre: charge} sent by hub 0."""
        d = W.d; res = [dict() for _ in range(d)]
        for k in self.byhub.get(d, []):
            p = self.P[k]
            for a in range(d):
                if fit_part(W, 0, self.S3[k], a):
                    t = (a + 2) % d; pre = p['pre'][:2]
                    res[t][pre] = res[t].get(pre, 0) + p['w']
        return res
    def inn(self, W):
        """charge sent by each spoke into hub 0 (per template)."""
        d = W.d; res = [dict() for _ in range(d)]
        for i in range(d):
            L = W.link[i]
            if L > 8: continue
            for k in self.byhub.get(L, []):
                p = self.P[k]
                if fit_part(W, 1 + i, self.S3[k], L - 2):
                    pre = p['pre'][:2]; res[i][pre] = res[i].get(pre, 0) + p['w']
        return res

def ball_from_part(p, anchor_rot, rng):
    """random concrete hub ball inside the part's box. Returns (d, link, asg) with part slot j at link index j."""
    d = p['hub']; link = []; asg = {}
    for j, s in enumerate(p['slots']):
        link.append(rng.randint(s[0], s[1]))
    for j, s in enumerate(p['slots']):
        # hat of slot j = vertex between spokes j-1 and j = var 100+(j-1)
        asg[100 + (j - 1) % d] = rng.randint(s[2], s[3])
        k = npriv(link[j])
        for t in range(k):
            f = s[4][t] if len(s[4]) == k else (5, 9)
            asg[200 + 3 * j + t] = rng.randint(f[0], f[1])
    return d, tuple(link), asg

def random_ball(d, rng):
    link = tuple(rng.randint(5, 9) for _ in range(d))
    return d, link, {v: rng.randint(5, 9) for v in variables(d, link)}

def target_word(W, i):
    """first-ring degree word of spoke i (needs degree <= 8), or None."""
    if W.link[i] > 8: return None
    out = []
    for v in W.rot_w[i]:
        k, val = W.deg_info(v); out.append(val)
    return tuple(out)

def canon(w):
    d = len(w); o = []
    for r in range(d):
        x = w[r:] + w[:r]; o.append(x); o.append(x[::-1])
    return min(o)
