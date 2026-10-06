"""Merge chunk outputs of one producer phase (same declaration, input and producer hashes) into one output.
usage: wp_merge.py OUT.json CHUNK1.json CHUNK2.json ...   (chunks given in any order)
A pure concatenation of graph records and witness lists; asserts the hashes agree and that graph indices are
contiguous from 0. The independent checker then recomputes the merged file from the plantri input."""
import json, sys
out_path, chunks = sys.argv[1], sys.argv[2:]
cs = [json.load(open(c)) for c in chunks]
for key in ("wp", "phase", "order", "declaration_sha256", "input_sha256", "producer_sha256", "truncated"):
    vals = {json.dumps(c[key], sort_keys=True) for c in cs}
    assert len(vals) == 1, f"chunks disagree on {key}: {vals}"
graphs = sorted((g for c in cs for g in c["graphs"]), key=lambda g: g["index"])
assert [g["index"] for g in graphs] == list(range(len(graphs))), "graph indices are not contiguous from 0"
wit = {k: [w for c in cs for w in c["witnesses"][k]] for k in ("sep_bad", "d1_kills", "p_kills")}
for k in wit:
    wit[k].sort(key=lambda w: (w["index"], w["x"], json.dumps(w["state"])))
o = dict(cs[0]); o["graphs"] = graphs; o["witnesses"] = wit
o["wall_seconds"] = round(sum(c.get("wall_seconds", 0) for c in cs), 1)
o["chunks"] = len(cs)
json.dump(o, open(out_path, "w"))
print("merged", len(cs), "chunks:", len(graphs), "graphs;", sum(len(v) for v in wit.values()), "witnesses")
