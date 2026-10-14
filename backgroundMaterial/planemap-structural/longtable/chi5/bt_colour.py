"""Independent check (no SAT): k-colourability by DSATUR-ordered backtracking.  bt_colourable(adj, k, skip)."""
def bt_colourable(adj, k=4, skip=None):
    V = [v for v in range(len(adj)) if v != skip]
    col = {}
    def pick():
        best = None; bs = (-1, -1)
        for v in V:
            if v in col: continue
            sat = len({col[w] for w in adj[v] if w in col}); d = sum(1 for w in adj[v] if w != skip and w not in col)
            if (sat, d) > bs: bs = (sat, d); best = v
        return best
    def rec():
        v = pick()
        if v is None: return True
        used = {col[w] for w in adj[v] if w in col}
        top = max(col.values(), default=-1)
        for c in range(min(k, top + 2)):   # symmetry: new colours in order
            if c in used: continue
            col[v] = c
            if rec(): return True
            del col[v]
        return False
    return rec()
