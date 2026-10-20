"""Append census-cache lines from FILE (imp54.py output) to G_res.txt whose key is not there yet.  Run only while no
census is running.  usage: python3 -I merge54.py FILE"""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); G = os.path.join(H, 'G_res.txt')
have = {l.rstrip('\n').split(' ', 2)[2] for l in open(G) if l.count(' ') >= 2}
new = [l for l in open(sys.argv[1]) if l.count(' ') >= 2 and l.rstrip('\n').split(' ', 2)[2] not in have]
open(G, 'a').write(''.join(new)); print('merged', len(new), 'lines into G_res.txt')
