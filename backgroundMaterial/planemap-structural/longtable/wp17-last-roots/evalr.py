from engine import *
G = load_all()
def badroots(rankf, macro=2, orders=None):
    out = []
    for (o, gi), g in sorted(G.items()):
        if orders and o not in orders: continue
        for r, R in g["roots"].items():
            if stuck_states(R, rankf, macro):
                out.append((o, gi, r))
    return out
