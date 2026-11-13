import sys; sys.path.insert(0,'code'); from parts import parse
def mirror(p, t=2, hs=-1, fan='rev_with_hat'):
    h = p['hub']; S = p['slots']; out = []
    for i in range(h):
        j = (2*t - i) % h          # spoke source
        k = (2*t - i + hs) % h     # hat/fan source
        sp = S[j][:2]; hat = S[k][2:4]; fans = S[k][4]
        if fan == 'rev_with_hat': fans = tuple(reversed(fans))
        elif fan == 'with_spoke': fans = tuple(reversed(S[j][4]))
        elif fan == 'keep_hat': pass
        out.append(sp + hat + (fans,))
    return tuple(out)
def key(p, slots=None): return (p['hub'], p['w'], slots if slots is not None else p['slots'])
