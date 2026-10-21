import re, sys, os, glob
def canon(lk, sv):
    d = len(lk); best = None
    for (l, s) in ((lk, sv), (lk[::-1], ''.join(sv[(-i-2) % d] for i in range(d)))):
        for r in range(d):
            k = (l[r:]+l[:r], s[r:]+s[:r])
            if best is None or k < best: best = k
    return best
def isface(lk, sv):
    d = len(lk)
    return any(lk[i]=='5' and lk[(i+1)%d]=='5' and sv[i]=='5' for i in range(d))
if __name__ == '__main__':
    rows = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
    files = sys.argv[2:]
    seen = {}
    pat1 = re.compile(r'(?<![0-9])([5-9]{7,17})/([5-9]{7,17})(?![0-9])')
    pat2 = re.compile(r'(?<![0-9])([5-9]{7,17})[ _]([5-9]{7,17})(?![0-9])')
    for f in files:
        try: txt = open(f, errors='replace').read()
        except Exception: continue
        for m in list(pat1.finditer(txt)) + list(pat2.finditer(txt)):
            a, b = m.group(1), m.group(2)
            if len(a) != len(b): continue
            seen.setdefault(canon(a, b), set()).add(os.path.relpath(f))
    for r in rows:
        w, d, lk, sv = r[0], r[1], r[2], r[3]
        k = canon(lk, sv)
        src = sorted(seen.get(k, []))
        print(w, d, lk, sv, 'FACE' if isface(lk, sv) else 'nonf', 'NEW' if not src else 'seen:' + ','.join(src[:4]) + ('...' if len(src) > 4 else ''))
