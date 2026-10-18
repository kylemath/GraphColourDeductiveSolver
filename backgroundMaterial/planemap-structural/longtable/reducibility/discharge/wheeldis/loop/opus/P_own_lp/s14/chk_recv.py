"""P2 s9: which cert receivers stay admissible under a registry. usage: python3 chk_recv.py CERT key=val... (pcheck options)"""
import sys, json, runpy, os, io, contextlib
cert = sys.argv[1]; opts = sys.argv[2:]
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['pcheck.py', 'none'] + opts
with contextlib.redirect_stdout(io.StringIO()): G = runpy.run_path(os.path.join(H, 'pcheck.py'))
G['load_patterns']()
for e in json.load(open(cert)):
    r = e['row']
    if r[0] == 'receiver':
        print(r[1], r[2], r[3], '->', G['admissible'](int(r[1]), r[2], r[3]) or 'ADMISSIBLE')
