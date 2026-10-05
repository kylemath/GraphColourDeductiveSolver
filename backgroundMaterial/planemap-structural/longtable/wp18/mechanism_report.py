"""Tables from mechanism-raw.json (written by mechanism_classify.py) -> mechanism-classify.txt."""
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.load(open(HERE / "mechanism-raw.json"))
agg = Counter()
for k, c in d["agg"]:
    agg[tuple(tuple(tuple(y) if isinstance(y, list) else y for y in x) if isinstance(x, list) else x for x in k)] += c
out = ["Move-word classification of shortest fills, orders 12-22 (961 graphs), distinct starts",
       "per degree-5 vertex (a start proper on several fans counted once; per-fan totals = 3x for",
       "every 4-colour start, because all three singleton-apex fans are legal there).", ""]
out.append("Fill length by gap flag (p13: bg-path 1~3 present; p14: bd-path 1~4 present):")
for k in sorted((k for k in agg if k[0] == "l"), key=str):
    out.append(f"  {k[1:]}: {agg[k]}")
out.append("")
out.append("l = 1 starts: which single moves fill (K = Kempe pair class, S = slide to middle/side):")
for k in sorted((k for k in agg if k[0] == "one"), key=str):
    out.append(f"  {k[2]}: {agg[k]}")
for l in (2, 3, 4):
    n = sum(c for k, c in agg.items() if k[0] == "words" and k[1] == l)
    out.append("")
    out.append(f"l = {l}: {n} starts")
    out.append("  starts admitting each word as a shortest fill:")
    for k in sorted((k for k in agg if k[0] == "word_any" and k[1] == l), key=lambda k: -agg[k]):
        out.append(f"    {k[2]}: {agg[k]}")
    allk = "K" * l
    nok = sum(c for k, c in agg.items() if k[0] == "words" and k[1] == l and allk not in k[2])
    out.append(f"  starts with NO all-Kempe shortest fill: {nok}")
    out.append("  final hole degree sets (over all shortest fills of a start):")
    for k in sorted((k for k in agg if k[0] == "finaldeg" and k[1] == l), key=lambda k: -agg[k]):
        out.append(f"    {list(k[2])}: {agg[k]}")
    out.append("  most common link-pattern sequences (deg:colour counts), starts admitting each:")
    for k in sorted((k for k in agg if k[0] == "patseq" and k[1] == l), key=lambda k: -agg[k])[:12]:
        out.append(f"    {' > '.join(k[2])}: {agg[k]}")
(HERE / "mechanism-classify.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
