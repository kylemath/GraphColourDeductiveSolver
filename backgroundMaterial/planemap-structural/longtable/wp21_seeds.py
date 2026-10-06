"""WP21 phase B seeds, by the rule in WP21-declaration.md: the 12 graphs of phase A with the greatest
objective, ties broken by smaller index in the selection file; if fewer than 12 have positive
objective, the remaining seeds are the lowest-index graphs of the selection.
usage: wp21_seeds.py A_OUTPUT.json SELECTION.txt OUT_SEEDS.txt"""
import hashlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wp21_search as S
import json
out = json.load(open(sys.argv[1]))
lines = [l.strip() for l in open(sys.argv[2]) if l.strip()]
scored = [(S.objective(g), g["index"]) for g in out["graphs"] if g["status"] != "interrupted"]
pos = sorted([t for t in scored if t[0] > 0], key=lambda t: (-t[0], t[1]))[:12]
chosen = [i for _, i in pos]
for i in range(len(lines)):
    if len(chosen) >= 12:
        break
    if i not in chosen:
        chosen.append(i)
open(sys.argv[3], "w").write("\n".join(lines[i] for i in chosen) + "\n")
print("seeds (selection-file indices):", chosen, "objectives:", [t[0] for t in pos],
      "seeds file sha256:", hashlib.sha256(open(sys.argv[3], "rb").read()).hexdigest())
