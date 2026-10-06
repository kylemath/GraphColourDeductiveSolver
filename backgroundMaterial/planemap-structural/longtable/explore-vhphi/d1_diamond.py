"""EXPLORATORY (D1-test, 2026-10-05). Split existing sep-c4-<n>.json records by whether the graph
(plantri -c4m4 n -a, index = line number) contains a Birkhoff diamond: degree-5 a,b,c,d, b~d,
a,c both adjacent to b and d, a not adjacent to c.  Usage: python3 d1_diamond.py PLANTRI OUT.json N [N...]"""
import json, subprocess, sys
import tilley_apex as TA

def has_diamond(rot):
    adj = [set(r) for r in rot]
    for b in range(len(rot)):
        if len(rot[b]) != 5: continue
        for d in adj[b]:
            if d < b or len(rot[d]) != 5: continue
            com = [v for v in adj[b] & adj[d] if len(rot[v]) == 5]
            for i in range(len(com)):
                for j in range(i + 1, len(com)):
                    if com[j] not in adj[com[i]]: return True
    return False

def main():
    plantri, out = sys.argv[1], sys.argv[2]
    res = {}
    for n in map(int, sys.argv[3:]):
        lines = subprocess.run([plantri, "-c4m4", str(n), "-a"], capture_output=True, text=True).stdout.splitlines()
        dia = {i for i, l in enumerate(lines) if has_diamond(TA.parse(l))}
        recs = json.load(open("sep-c4-%d.json" % n))["records"]
        row = {}
        for name, pick in (("diamond", lambda i: i in dia), ("no_diamond", lambda i: i not in dia)):
            rs = [r for r in recs if pick(r["idx"])]
            gs = len(dia) if name == "diamond" else len(lines) - len(dia)
            row[name] = {"graphs": gs, "deg5_vertices": len(rs), "states": sum(r["states"] for r in rs),
                         "bad_states": sum(r["bad_states"] for r in rs)}
        row["diamond_indices"] = sorted(dia)
        res[n] = row
        print(n, {k: v for k, v in row.items() if k != "diamond_indices"}, flush=True)
    json.dump(res, open(out, "w"))
if __name__ == "__main__":
    main()
