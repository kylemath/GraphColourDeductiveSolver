"""WP21 phase A input: the rule-selected lines of a full plantri stdout file.
usage: wp21_sample.py FULL.txt OUT.txt [--tag WP21-A] [--mod 20]
Selected: line index i (0-based) with int(sha256(tag + '-' + str(i)).hexdigest()[:8], 16) % mod == 0."""
import argparse, hashlib
ap = argparse.ArgumentParser(); ap.add_argument("full"); ap.add_argument("out")
ap.add_argument("--tag", default="WP21-A"); ap.add_argument("--mod", type=int, default=20)
a = ap.parse_args()
lines = [l.strip() for l in open(a.full) if l.strip()]
sel = [l for i, l in enumerate(lines) if int(hashlib.sha256((a.tag + "-" + str(i)).encode()).hexdigest()[:8], 16) % a.mod == 0]
open(a.out, "w").write("\n".join(sel) + "\n")
print(len(sel), "of", len(lines), "selected; sha256 of selection:", hashlib.sha256(open(a.out, "rb").read()).hexdigest())
