# Stage 1 dissipation network: row set for the 5/6/7 world (degrees 5, 6, 7 only).
# Source of the kill mask:
#  - degree-7 rows: w16/data/world_567_7_std.pkl (W16, 5 Nov 2026, "Studio-full" stack = keep95p131f + l3q V7/V8 + rpatN3 +
#    A111 C patterns + RBIG; 110,087 admissible receivers (link w, hats s) whose letters are all in {5,6,7}).
#  - degree-5 and degree-6 links: R5 / R6 / FANS exactly as spec 4.4 in w16/code/st21_w10.py (SPEC_R5, SPEC_R6, SPEC_FANS,
#    plus "three consecutive 5s" in a 6-link). These are wheel-level kills only (fewer kills = conservative).
# Charge unit: a vertex of degree d starts with 60 (6 - d).
import pickle, itertools, os, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
PKL = os.path.join(HERE, '..', 'w16', 'data', 'world_567_7_std.pkl')
LET = (5, 6, 7)

def canon(w):
    w = tuple(w); n = len(w); rots = [w[k:] + w[:k] for k in range(n)]; r = w[::-1]
    return min(rots + [r[k:] + r[:k] for k in range(n)])
SPEC_R5 = '55555 55556 55557 55558 55566 55567 55568 55577 55578 55588 55656 55657 55658 55666 56566 56567 56568 56577 56578 56588 56657 56658 56666 66666'.split()
SPEC_R6 = ('555555 555556 555557 555566 555567 555577 555656 555657 555666 555667 555676 555677 555757 555767 555777 556556 '
           '556557 556566 556567 556576 556577 556657 556666 565656 565657 565666 566566 566567 566577 566657 566666').split()
SPEC_FANS = 'F5565 F5656 F5555 F5665 FF555 F5556 FF565'.split()
R5 = {canon(tuple(int(c) for c in x)) for x in SPEC_R5}
R6 = {canon(tuple(int(c) for c in x)) for x in SPEC_R6}
FANS = [tuple(None if c == 'F' else int(c) for c in x) for x in SPEC_FANS]
def fanmatch(w, p):
    n = len(w)
    for r in range(n):
        for refl in (False, True):
            if all(pc is None or pc == (w[(r - i) % n] if refl else w[(r + i) % n]) for i, pc in enumerate(p)): return True
    return False
def isR5(w): return canon(w) in R5 or any(fanmatch(tuple(w), p) for p in FANS)
def isR6(w):
    w = tuple(w); return canon(w) in R6 or any(w[i] == w[(i + 1) % 6] == w[(i + 2) % 6] == 5 for i in range(6))

def md5(fn): return hashlib.md5(open(fn, 'rb').read()).hexdigest()

def load():
    L = pickle.load(open(PKL, 'rb'))
    R7 = [(l[2], l[3]) for l in L if l[0] == 'R' and l[1] == 7]
    W5 = sorted({canon(w) for w in itertools.product(LET, repeat=5) if not isR5(w)})
    W6 = sorted({canon(w) for w in itertools.product(LET, repeat=6) if not isR6(w)})
    # cross-checks against the W16 pickle
    S5 = sorted({l[1] for l in L if l[0] == 'S'}); C6 = sorted({l[1] for l in L if l[0] == 'C'})
    return dict(R7=R7, W5=W5, W6=W6, S5=S5, C6=C6, pkl_md5=md5(PKL), nlab=len(L))

if __name__ == '__main__':
    D = load()
    print('pkl md5', D['pkl_md5'], 'labels', D['nlab'])
    print('7-rows', len(D['R7']))
    print('admissible 5-links', len(D['W5']), 'same as W16 sender words:', D['W5'] == D['S5'])
    print('admissible 6-links', len(D['W6']), 'W16 cons2 words', len(D['C6']), 'extra:', sorted(set(D['W6']) - set(D['C6'])), 'missing:', sorted(set(D['C6']) - set(D['W6'])))
