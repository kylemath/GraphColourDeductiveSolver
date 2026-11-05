# map a kill window (slots of row r + optional apex t at a 5-5-5 face) onto every d=7 receiver row of the certificate:
# a row is hit when, for some face placement (rotation/reflection), the same slot set + t builds a window with the same canonical code.
import sys, json, re
from fractions import Fraction as F
from gen3 import build, ring3_candidates, ringcycle, kcline
from kcanon import code
CERT = '/mnt/project-files/swarm/round6/W7-lower-k95f/certs/cert_k95f_best_0.0256781.json'
C = json.load(open(CERT))
RECV = [(-F(e['w']), e['row']) for e in C if e['row'][0] == 'receiverR2']
RM = sum(w for w, _ in RECV)
def parse_name(nm):
    m = re.match(r'b7_([u-])([0-9.]{7})_([0-9.]{7})(?:_t(\d+?)(\d))?$', nm)
    if not m: return None
    u, lk, sv, tk, td = m.groups()
    return u == 'u', lk, sv, (int(tk) if tk else None), (int(td) if td else None)
def window_code(LK, SV, slots, face, td):
    """slots: set of names (('u',), ('w',j), ('s',j)); face: index i' of the 5-5-5 face whose apex t (degree td) is added (or None)"""
    tdeg = None; S = set(slots)
    if face is not None:
        ks = [k for k, nb in ring3_candidates(LK, SV) if ('s', face) in nb]
        if len(ks) != 1: return None
        tdeg = {ks[0]: td}; S.add(('t', ks[0]))
    try: adj, rot, name, deg, Z3, inv = build(LK, SV, tdeg=tdeg)
    except (AssertionError, ValueError): return None
    if any(x not in inv for x in S): return None
    Is = set(inv[x] for x in S); order = ringcycle(adj, Is)
    if order is None: return None
    return code(kcline('x', adj, Is, order))
def placements(i, ip):
    for refl in (0, 1):
        if not refl: phw = lambda j: (j - i + ip) % 7; phs = lambda j: (j - i + ip) % 7
        else: phw = lambda j: (ip + 1 - (j - i)) % 7; phs = lambda j: (ip - (j - i)) % 7
        yield phw, phs
def hits_for(nm, kline, face):
    pn = parse_name(nm); uin, lk, sv, tk, td = pn
    slots = ({('u',)} if uin else set()) | {('w', j) for j in range(7) if lk[j] != '.'} | {('s', j) for j in range(7) if sv[j] != '.'}
    target = code(kline); out = []
    for w, r in RECV:
        if r[1] != 7: continue
        LK, SV = r[2], r[3]; found = None
        faces = [ip for ip in range(7) if LK[ip] == '5' and LK[(ip + 1) % 7] == '5' and SV[ip] == '5'] if face is not None else [0]
        for ip in faces:
            iref = face if face is not None else 0
            for phw, phs in placements(iref, ip):
                S2 = set()
                for x in slots:
                    S2.add(x if x[0] == 'u' else (('w', phw(x[1])) if x[0] == 'w' else ('s', phs(x[1]))))
                if face is None:
                    pass
                c = window_code(LK, SV, S2, ip if face is not None else None, td)
                if c == target: found = (ip, phw(0)); break
            if found: break
        if found: out.append((w, LK, SV, found))
    return out
if __name__ == '__main__':
    # args: name kcline-file-line face   (reads lines "name<TAB>face<TAB>kcline")
    for l in open(sys.argv[1]):
        nm, face, kl = l.rstrip('\n').split('\t'); face = int(face) if face != '-' else None
        h = hits_for(nm, kl, face)
        print('%s face=%s rows=%d receiver-mass-share=%.4f :: %s' % (nm, face, len(h), float(sum(x[0] for x in h) / RM), ' '.join('%s/%s(%.4f)' % (x[1], x[2], float(x[0] / RM)) for x in sorted(h, key=lambda y: -y[0])[:8])), flush=True)
