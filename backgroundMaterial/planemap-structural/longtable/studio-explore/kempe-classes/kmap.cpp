// [exploratory] Studio compute kmap.cpp: the class map from Kempe classes of 4-colourings of T to Kempe classes of
// 4-colourings of H, where H = T - v (vertex deletion) or H = T - e (edge deletion, e = uw kept as two vertices).
// Every proper colouring of T restricts to one of H; a class of H that contains no restriction is NEW (a created class).
// For H = T - v with v of degree 5 this is exactly a targetless class (given 4CT, R* at v <=> no new class).
// States: colourings up to colour renaming, canonical by first occurrence along a BFS order; moves: whole two-colour
// component swaps. Input: "n E" then E lines "a b". Usage: kmap FILE v VERTEX | kmap FILE e U W   [STATE_CAP]
// Output JSON: kT, kH, states, number of H classes hit by restrictions, new classes, merges (max T classes per H class).
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#include <functional>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
struct Space {
    int N; u64 adjm[64]; std::vector<Key> S; std::vector<int> par; int col[64]; long long cap;
    Key keyof(const int *c) const { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
    void unkey(const Key &k, int *c) const { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
    u64 flood(u64 st, u64 M) const { u64 comp = st, front = st;
        while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; } return comp; }
    void rec(int i, int used) {
        if (i == N) { S.push_back(keyof(col)); if ((long long)S.size() > cap) { printf("{\"inconclusive\": \"state cap\"}\n"); exit(0); } return; }
        u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
        int top = used + 1 < 4 ? used + 1 : 4;
        for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); }
    }
    int find(int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; }
    long long lookup(const int *c) const { int mp[4] = {-1, -1, -1, -1}, nx = 0, nc[64];
        for (int i = 0; i < N; i++) { if (mp[c[i]] < 0) mp[c[i]] = nx++; nc[i] = mp[c[i]]; }
        Key k = keyof(nc); auto it = std::lower_bound(S.begin(), S.end(), k); return (it != S.end() && *it == k) ? it - S.begin() : -1; }
    // build from vertex list `order` (BFS), adjacency predicate
    int build(const std::vector<std::vector<int>> &adj, const std::vector<int> &order, const std::vector<int> &idx, int skipu, int skipw) {
        N = order.size(); if (N > 64) return 0;
        for (int i = 0; i < N; i++) { adjm[i] = 0; int a = order[i];
            for (int w : adj[a]) { if (idx[w] < 0) continue; if ((a == skipu && w == skipw) || (a == skipw && w == skipu)) continue; adjm[i] |= 1ULL << idx[w]; } }
        col[0] = 0; rec(1, 1); std::sort(S.begin(), S.end()); par.resize(S.size()); for (size_t i = 0; i < S.size(); i++) par[i] = i;
        int c[64];
        for (size_t s = 0; s < S.size(); s++) { unkey(S[s], c); u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; int d[64];
                    for (int i = 0; i < N; i++) { d[i] = c[i]; if (K >> i & 1) d[i] = (c[i] == p) ? q : p; }
                    long long t = lookup(d); if (t < 0) { printf("{\"error\": \"swap left space\"}\n"); exit(0); }
                    int a = find(s), b = find(t); if (a != b) par[a] = b; } } }
        return 1;
    }
};
static Space T, Hs;
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: kmap FILE v V | kmap FILE e U W [CAP]\n"); return 2; }
    FILE *fp = fopen(argv[1], "r"); int n, E; if (fscanf(fp, "%d %d", &n, &E) != 2) return 2;
    std::vector<std::vector<int>> adj(n);
    for (int e = 0; e < E; e++) { int a, b; if (fscanf(fp, "%d %d", &a, &b) != 2) return 2; adj[a].push_back(b); adj[b].push_back(a); }
    for (auto &l : adj) { std::sort(l.begin(), l.end()); l.erase(std::unique(l.begin(), l.end()), l.end()); }
    bool vmode = argv[2][0] == 'v'; int hv = -1, eu = -1, ew = -1; std::vector<char> del(n, 0); int ndel = 0;
    if (vmode) { char *q = argv[3]; while (*q) { int x = strtol(q, &q, 10); if (!del[x]) { del[x] = 1; ndel++; } if (hv < 0) hv = x; if (*q == ',') q++; } } else { eu = atoi(argv[3]); ew = atoi(argv[4]); }
    long long cap = argc > (vmode ? 4 : 5) ? atoll(argv[vmode ? 4 : 5]) : 50000000LL; T.cap = Hs.cap = cap;
    int start = eu; if (vmode) { start = -1; for (int x = 0; x < n && start < 0; x++) if (!del[x]) start = x; }
    // T: BFS order from start over all vertices
    std::vector<int> oT{start}, iT(n, -1); iT[start] = 0;
    for (size_t h = 0; h < oT.size(); h++) for (int w : adj[oT[h]]) if (iT[w] < 0) { iT[w] = oT.size(); oT.push_back(w); }
    // H: BFS order skipping hv (and not using edge eu-ew)
    std::vector<int> oH{start}, iH(n, -1); iH[start] = 0;
    for (size_t h = 0; h < oH.size(); h++) { int a = oH[h]; for (int w : adj[a]) {
        if ((vmode && del[w]) || iH[w] >= 0) continue; if ((a == eu && w == ew) || (a == ew && w == eu)) continue; iH[w] = oH.size(); oH.push_back(w); } }
    if ((int)oT.size() != n || (int)oH.size() != (vmode ? n - ndel : n)) { printf("{\"error\": \"disconnected\"}\n"); return 0; }
    if (!T.build(adj, oT, iT, -1, -1) || !Hs.build(adj, oH, iH, eu, ew)) { printf("{\"error\": \"too large\"}\n"); return 0; }
    // class map
    std::map<int, std::set<int>> pre;  // H root -> set of T roots
    int cT[64], cH[64];
    for (size_t s = 0; s < T.S.size(); s++) { T.unkey(T.S[s], cT);
        for (int i = 0; i < Hs.N; i++) cH[i] = cT[iT[oH[i]]];
        long long t = Hs.lookup(cH); if (t < 0) { printf("{\"error\": \"restriction not found\"}\n"); return 0; }
        pre[Hs.find(t)].insert(T.find(s)); }
    std::set<int> rT, rH; for (size_t s = 0; s < T.S.size(); s++) rT.insert(T.find(s)); for (size_t s = 0; s < Hs.S.size(); s++) rH.insert(Hs.find(s));
    int maxpre = 0, merging = 0; for (auto &kv : pre) { maxpre = std::max(maxpre, (int)kv.second.size()); merging += kv.second.size() >= 2; }
    printf("{\"mode\": \"%s\", \"T_states\": %zu, \"kT\": %zu, \"H_states\": %zu, \"kH\": %zu, \"H_classes_hit\": %zu, \"new_classes\": %zu, \"merging_H_classes\": %d, \"max_T_classes_per_H_class\": %d}\n",
           vmode ? "vertex" : "edge", T.S.size(), rT.size(), Hs.S.size(), rH.size(), pre.size(), rH.size() - pre.size(), merging, maxpre);
    if (getenv("KMAP_REPS")) {  // one representative colouring of H per class, as original-label -> colour, plus the class size and whether it is hit
        std::map<int, long long> first, size; for (size_t s = 0; s < Hs.S.size(); s++) { int r = Hs.find(s); if (!first.count(r)) first[r] = s; size[r]++; }
        printf("{\"reps\": [");
        bool f1 = true;
        for (auto &kv : first) { int c[64]; Hs.unkey(Hs.S[kv.second], c);
            printf("%s{\"class_size\": %lld, \"hit_by_T\": %s, \"T_classes_mapping_here\": %zu, \"colouring\": {", f1 ? "" : ", ", size[kv.first], pre.count(kv.first) ? "true" : "false", pre.count(kv.first) ? pre[kv.first].size() : (size_t)0);
            for (int i = 0; i < Hs.N; i++) printf("%s\"%d\": %d", i ? ", " : "", oH[i], c[i]);
            printf("}}"); f1 = false; }
        printf("]}\n"); }
    if (getenv("KMAP_BRIDGE")) {
        // Conjecture M (Intern D): for every pair of T-classes merged in H, the fewest UNFILLED states on an H-Kempe path
        // from a restriction of C1 to a restriction of C2 whose interior is entirely unfilled (0 = a direct move between
        // restrictions). "unfilled" = not a restriction of any T-colouring. -1 = no such path (joined only through
        // restrictions of other T-classes).
        size_t D = Hs.S.size(); std::vector<int> tcls(D, -1);   // T root of the restriction, or -1 if unfilled
        for (size_t s = 0; s < T.S.size(); s++) { T.unkey(T.S[s], cT); for (int i = 0; i < Hs.N; i++) cH[i] = cT[iT[oH[i]]];
            tcls[Hs.lookup(cH)] = T.find(s); }
        auto nbrs = [&](size_t s, std::vector<long long> &out) { out.clear(); int c[64], d[64]; Hs.unkey(Hs.S[s], c);
            u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < Hs.N; i++) cm[c[i]] |= 1ULL << i;
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                while (M) { u64 K = Hs.flood(M & -M, cm[p] | cm[q]); M &= ~K;
                    for (int i = 0; i < Hs.N; i++) { d[i] = c[i]; if (K >> i & 1) d[i] = (c[i] == p) ? q : p; }
                    long long t = Hs.lookup(d); if (t != (long long)s) out.push_back(t); } } };
        std::map<std::pair<int,int>, int> best;  // (C1, C2) -> min unfilled count
        std::vector<long long> nb;
        for (int C1 : rT) {
            std::vector<int> dist(D, -1); std::vector<long long> q;
            for (size_t s = 0; s < D; s++) if (tcls[s] == C1) { dist[s] = 0; q.push_back(s); }
            for (size_t h = 0; h < q.size(); h++) { long long s = q[h]; nbrs(s, nb);
                for (long long t : nb) { if (tcls[t] >= 0) { if (tcls[t] != C1) { int k = dist[s]; auto key = std::make_pair(C1, tcls[t]);
                            if (!best.count(key) || k < best[key]) best[key] = k; } continue; }
                    if (dist[t] < 0) { dist[t] = dist[s] + 1; q.push_back(t); } } }
        }
        std::map<int, int> hist; int pairs = 0;
        for (auto &kv : pre) { std::vector<int> cl(kv.second.begin(), kv.second.end());
            for (size_t i = 0; i < cl.size(); i++) for (size_t j = i + 1; j < cl.size(); j++) { pairs++;
                auto k = std::make_pair(cl[i], cl[j]); hist[best.count(k) ? best[k] : -1]++; } }
        // weak form: within each merging H class, are the T-classes connected using only bridges with <= 1 unfilled state?
        int weak_ok = 0, weak_fail = 0, maxk_needed = 0;
        for (auto &kv : pre) { if (kv.second.size() < 2) continue; std::vector<int> cl(kv.second.begin(), kv.second.end());
            // smallest k such that bridges with <= k unfilled states connect all of cl
            int need = -1;
            for (int k = 0; k <= 64 && need < 0; k++) { std::map<int,int> u; for (int c : cl) u[c] = c;
                std::function<int(int)> fd = [&](int x) { return u[x] == x ? x : u[x] = fd(u[x]); };
                for (auto &b : best) if (b.second >= 0 && b.second <= k && u.count(b.first.first) && u.count(b.first.second)) u[fd(b.first.first)] = fd(b.first.second);
                std::set<int> roots; for (int c : cl) roots.insert(fd(c)); if (roots.size() == 1) need = k; }
            if (need >= 0 && need <= 1) weak_ok++; else weak_fail++; maxk_needed = std::max(maxk_needed, need); }
        printf("{\"merged_pairs\": %d, \"bridge_unfilled_hist\": {", pairs); bool f = true;
        for (auto &kv : hist) { printf("%s\"%d\": %d", f ? "" : ", ", kv.first, kv.second); f = false; }
        printf("}, \"merging_H_classes_connected_by_1_bridges\": %d, \"not\": %d, \"max_bridge_level_needed\": %d}\n", weak_ok, weak_fail, maxk_needed); }
    return 0;
}
