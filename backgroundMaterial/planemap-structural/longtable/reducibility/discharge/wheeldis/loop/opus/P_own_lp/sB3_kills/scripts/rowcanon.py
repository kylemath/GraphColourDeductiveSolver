def rowcanon(LK, SV):
    n = len(LK); best = None
    for r in range(n):
        for refl in (0, 1):
            if not refl: w = ''.join(LK[(i + r) % n] for i in range(n)); s = ''.join(SV[(i + r) % n] for i in range(n))
            else: w = ''.join(LK[(r - i) % n] for i in range(n)); s = ''.join(SV[(r - i - 1) % n] for i in range(n))
            if best is None or (w, s) < best: best = (w, s)
    return best
