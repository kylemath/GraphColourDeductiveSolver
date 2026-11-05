from kcanon import parse
def score(line):
    nm, r, m, ra, ia = parse(line); dg = [len(a) + len(b) for a, b in zip(ra, ia)]
    return sum(1 for x in dg if x == 5) - sum(1 for x in dg if x >= 7)
