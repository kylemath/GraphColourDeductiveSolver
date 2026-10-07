#!/usr/bin/env python3
"""[exploratory] Local intel's 800-cycle (studiointel/path3-local/run_dd/best-A7_exc.json, hole 22): run qf.analyse (same code
as the census) and print the class records that carry DL cycles, with the DD-locality fields and the room decomposition.
usage: a7_cycle.py [HOLE=22] > a7-hole22.json"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, "..", "8-quarter-identities")); sys.path.insert(0, os.path.join(H, "..", "5-glue-radius5")); sys.argv += [] if len(sys.argv) > 1 else []
hole = int(sys.argv[1]) if len(sys.argv) > 1 else 22
sys.argv = ["x"]
from glue import rot_from_faces
from qf import analyse
F = json.load(open(os.path.join(H, "..", "..", "..", "studiointel", "path3-local", "run_dd", "best-A7_exc.json")))["faces"]
rot = rot_from_faces(F)
r = analyse(rot, hole)
out = {"graph": "best-A7_exc.json", "n": len(rot), "hole": hole, "states": r["states"], "C2_bad": r["C2_bad"], "classes": []}
for k in r["classes"]:
    room = [pj[1] + pj[2] + pj[3] + pj[4] for pj in k["perj"]]
    out["classes"].append({**{a: k[a] for a in ("size", "F", "U", "N0", "N1", "D", "D_cyc", "L_F", "paths", "dP_hist", "identity_ok", "perj_bad", "DD", "DDloc")},
                           "room_per_j": room, "room_parts_summed_over_j": {"L_j": sum(pj[1] for pj in k["perj"]), "Uff_j+Uff_{j+3}": sum(pj[2] + pj[3] for pj in k["perj"]),
                                                                           "E_j": sum(pj[4] for pj in k["perj"])}})
print(json.dumps(out, indent=1))
