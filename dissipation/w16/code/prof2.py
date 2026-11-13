import sys, random, time, cProfile, pstats; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT, explore as X
W.init()
rng = random.Random(3); T = TT.lattice_torus(4, 1, 4); T.check()
cProfile.run('X.anneal(T, {5,6,7,8}, 3000, rng=rng, found={}, nmin=8)', '/tmp/swarm-W16/prof2.out')
p = pstats.Stats('/tmp/swarm-W16/prof2.out'); p.sort_stats('tottime').print_stats(14)
