import sys
from win_lib import load
for path in sys.argv[1:]:
    for w in load(path)[:12]:
        print('n', w.n, 'chords', [c for c in w.E[w.n:]], 'fv', w.fv)
        for t in range(w.W):
            s = w.state(t)
            line = f"  t={t} k={s['k']} |X|={s['X']} |Y|={s['Y']} a5v={int(s['a5v'])}"
            if t % 2 == 1:
                seq, pos, p = w.ham_positions(t)
                line += f"  HAM p0={p[0]} p1={p[1]} p3={p[3]} {'e0e1-uncrossed' if p[1] < p[0] else 'CROSSED'}"
            print(line)
