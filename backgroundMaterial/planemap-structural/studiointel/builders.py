"""studiointel builders.py -- graph spec strings -> faces. specs: ico, A:<r>, GC:<k>, L(<spec>)"""
import graphs
def build(spec):
    if spec == 'ico': return graphs.icosahedron()
    if spec.startswith('A:'): return graphs.A_r(int(spec[2:]))
    if spec.startswith('GC:'): return graphs.GC(int(spec[3:]), 0)
    if spec.startswith('L(') and spec.endswith(')'): return graphs.leapfrog(build(spec[2:-1]))
    raise ValueError(spec)
