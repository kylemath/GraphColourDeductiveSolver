"""Python wrapper for the C engine macro2.c (compiled to ./macro2)."""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
FEATURES = ["q", "lin", "L", "Lall", "links", "shortLinks", "repMass", "hubToggles"]
E = {name: [1 if j == i else 0 for j in range(8)] for i, name in enumerate(FEATURES)}


def build():
    exe = HERE / "macro2"
    src = HERE / "macro2.c"
    if not exe.exists() or exe.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["cc", "-O3", "-march=native", "-Wall", "-o", str(exe), str(src), "-lpthread"], check=True)
    return exe


def run_engine(rot, r, weights, threads=1):
    exe = build()
    lines = [f"{len(rot)} {r} {len(weights)}"]
    lines += [" ".join(map(str, [len(ns)] + list(ns))) for ns in rot]
    lines += [" ".join(map(str, w)) for w in weights]
    out = subprocess.run([str(exe), str(threads)], input="\n".join(lines) + "\n",
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def run_batch(jobs, weights, threads=1):
    """jobs = [(rot, r), ...]; one engine process; returns list of result dicts in order."""
    exe = build()
    lines = []
    for rot, r in jobs:
        lines.append(f"{len(rot)} {r} {len(weights)}")
        lines += [" ".join(map(str, [len(ns)] + list(ns))) for ns in rot]
        lines += [" ".join(map(str, w)) for w in weights]
    out = subprocess.run([str(exe), str(threads)], input="\n".join(lines) + "\n",
                         capture_output=True, text=True, check=True)
    res = [json.loads(x) for x in out.stdout.splitlines()]
    assert len(res) == len(jobs)
    return res
