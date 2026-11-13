import sys, random, time, cProfile, pstats; sys.path.insert(0, '/tmp/swarm-W16/code')
import w16lib as W, torus as TT, explore as X
W.init()
rng = random.Random(3); T = TT.lattice_torus(4, 1, 5); T.check()
cProfile.run('X.anneal(T, {5,6,7,8,9}, 1500, rng=rng, found={})', '/tmp/swarm-W16/prof.out')
p = pstats.Stats('/tmp/swarm-W16/prof.out'); p.sort_stats('cumulative').print_stats(18)
print(len(W._ADM))
