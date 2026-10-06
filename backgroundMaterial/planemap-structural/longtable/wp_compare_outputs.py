"""Content digest and comparison of producer outputs (ignores timing fields).
  wp_compare_outputs.py digest OUT.json [--block 2539]   prints JSON: per-block digests of graph records, witness digest, overall
  wp_compare_outputs.py compare A.json B.json            exit 0 iff the graph records and witnesses are identical
Used to compare an independent replay on another machine with the original run without shipping the file."""
import hashlib, json, sys
def digest(path, block):
    o = json.load(open(path))
    gs = sorted(o["graphs"], key=lambda g: g["index"])
    blocks, h, n = [], hashlib.sha256(), 0
    for g in gs:
        h.update(json.dumps(g, sort_keys=True).encode()); n += 1
        if n % block == 0: blocks.append(h.hexdigest()); h = hashlib.sha256()
    if n % block: blocks.append(h.hexdigest())
    w = {k: sorted(json.dumps(x, sort_keys=True) for x in o["witnesses"][k]) for k in ("sep_bad", "d1_kills", "p_kills")}
    wd = hashlib.sha256(json.dumps(w, sort_keys=True).encode()).hexdigest()
    meta = {k: o.get(k) for k in ("wp", "phase", "order", "declaration_sha256", "input_sha256", "producer_sha256")}
    overall = hashlib.sha256((",".join(blocks) + wd).encode()).hexdigest()
    return {"graphs": n, "block": block, "blocks": blocks, "witness_sha256": wd, "overall_sha256": overall, "meta": meta}
if __name__ == "__main__":
    if sys.argv[1] == "digest":
        b = int(sys.argv[sys.argv.index("--block") + 1]) if "--block" in sys.argv else 2539
        print(json.dumps(digest(sys.argv[2], b)))
    else:
        a, b = digest(sys.argv[2], 2539), digest(sys.argv[3], 2539)
        same = a["overall_sha256"] == b["overall_sha256"] and a["meta"] == b["meta"]
        diffs = [i for i, (x, y) in enumerate(zip(a["blocks"], b["blocks"])) if x != y]
        print("IDENTICAL" if same else f"DIFFERENT: graphs {a['graphs']} vs {b['graphs']}, differing blocks {diffs}, witnesses equal {a['witness_sha256']==b['witness_sha256']}, meta equal {a['meta']==b['meta']}")
        sys.exit(0 if same else 1)
