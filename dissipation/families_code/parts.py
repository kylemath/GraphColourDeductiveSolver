import re
def parse(fn):
    L = [l.split() for l in open(fn) if l.strip()]
    scale = int(L[0][1]); parts = []
    for t in L[2:]:
        tag, hub, w = t[0], int(t[1]), int(t[2]); x = list(map(int, t[3:])); slots = []; i = 0
        for s in range(hub):
            sp_lo, sp_hi, h_lo, h_hi, nf = x[i:i+5]; i += 5
            fans = tuple(tuple(x[i+2*k:i+2*k+2]) for k in range(nf)); i += 2*nf
            slots.append((sp_lo, sp_hi, h_lo, h_hi, fans))
        assert i == len(x), tag
        pre = re.match(r'[A-Za-z_]+', tag).group(0).rstrip('m') if not tag.startswith('drule') else 'drule'
        parts.append(dict(tag=tag, pre=pre, hub=hub, w=w, slots=tuple(slots)))
    return scale, parts
