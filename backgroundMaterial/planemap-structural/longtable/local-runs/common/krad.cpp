// [exploratory] Local compute krad.cpp: Kempe classes AND radius at a hole. Derived from studio-explore/kempe-classes/kclass.cpp
// (same enumeration, canonical form and moves); adds the explicit move graph, multi-source BFS distance to the filled set,
// per-class radius, and an optional query colouring.
// States: proper 4-colourings of G - h up to renaming (canonical by first occurrence along BFS order from the hole's
// smallest neighbour, or from vertex 0 when h = -1). Moves: swap two colours on one whole two-colour component.
// filled = hole's neighbours use <= 3 colours. dist = fewest moves to a filled state. A class with no filled state is
// TARGETLESS. rho = max dist over all states (reported as -1 if some class is targetless).
// Input: "n E" then E lines "a b". Usage: krad FILE HOLE [QUERYFILE]   (QUERYFILE: lines "vertex colour")
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <map>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N, nlink; static u64 adjm[64]; static int linkv[64]; static int col[64];
static std::vector<Key> S;
static inline Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static inline void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static inline u64 flood(u64 start, u64 M) { u64 comp = start, front = start;
    while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; }
    return comp; }
static void rec(int i, int used) {
    if (i == N) { S.push_back(keyof(col)); return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4;
    for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); }
}
static long long lookup(const int *c) { int mp[4] = {-1, -1, -1, -1}, nx = 0, nc[64]; for (int i = 0; i < N; i++) { if (mp[c[i]] < 0) mp[c[i]] = nx++; nc[i] = mp[c[i]]; }
    Key k = keyof(nc); auto it = std::lower_bound(S.begin(), S.end(), k); return (it != S.end() && *it == k) ? it - S.begin() : -1; }
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: krad FILE HOLE [QUERYFILE]\n"); return 2; }
    FILE *fp = fopen(argv[1], "r"); int n, E; if (fscanf(fp, "%d %d", &n, &E) != 2) return 2;
    int hole = atoi(argv[2]);
    std::vector<std::vector<int>> adj(n);
    for (int e = 0; e < E; e++) { int a, b; if (fscanf(fp, "%d %d", &a, &b) != 2) return 2; if (a == b) continue; adj[a].push_back(b); adj[b].push_back(a); }
    for (auto &l : adj) { std::sort(l.begin(), l.end()); l.erase(std::unique(l.begin(), l.end()), l.end()); }
    int start = hole >= 0 ? adj[hole][0] : 0;
    std::vector<int> order{start}, idx(n, -1); idx[start] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (w != hole && idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); int expect = hole >= 0 ? n - 1 : n;
    if (N > 64 || N != expect) { printf("{\"error\": \"N=%d unsupported or disconnected\"}\n", N); return 0; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) if (w != hole) adjm[i] |= 1ULL << idx[w]; }
    nlink = 0; if (hole >= 0) for (int w : adj[hole]) linkv[nlink++] = idx[w];
    col[0] = 0; rec(1, 1);
    std::sort(S.begin(), S.end());
    size_t D = S.size(); std::vector<std::vector<int>> G(D); std::vector<char> filled(D, 0);
    int c[64], d[64];
    for (size_t s = 0; s < D; s++) {
        unkey(S[s], c);
        if (hole >= 0) { int seen = 0; for (int t = 0; t < nlink; t++) seen |= 1 << c[linkv[t]]; filled[s] = __builtin_popcount(seen) <= 3; }
        u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) {
            u64 M = cm[p] | cm[q];
            while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
                for (int i = 0; i < N; i++) { d[i] = c[i]; if (K >> i & 1) d[i] = (c[i] == p) ? q : p; }
                long long t = lookup(d); if (t < 0) { printf("{\"error\": \"swap left the state space\"}\n"); return 0; }
                if (t != (long long)s) G[s].push_back(t); }
        }
    }
    // classes
    std::vector<int> cl(D, -1); int ncl = 0;
    for (size_t s = 0; s < D; s++) if (cl[s] < 0) { std::vector<int> q{(int)s}; cl[s] = ncl;
        for (size_t h = 0; h < q.size(); h++) for (int t : G[q[h]]) if (cl[t] < 0) { cl[t] = ncl; q.push_back(t); } ncl++; }
    // distances
    std::vector<int> dist(D, -1), qq; for (size_t s = 0; s < D; s++) if (filled[s]) { dist[s] = 0; qq.push_back(s); }
    for (size_t h = 0; h < qq.size(); h++) for (int t : G[qq[h]]) if (dist[t] < 0) { dist[t] = dist[qq[h]] + 1; qq.push_back(t); }
    std::vector<long long> csize(ncl, 0), cfill(ncl, 0); std::vector<int> crad(ncl, 0);
    long long nf = 0; for (size_t s = 0; s < D; s++) { csize[cl[s]]++; cfill[cl[s]] += filled[s]; nf += filled[s]; crad[cl[s]] = std::max(crad[cl[s]], dist[s]); }
    int targetless = 0, rho = 0; for (int k = 0; k < ncl; k++) { if (!cfill[k]) { targetless++; crad[k] = -1; } else rho = std::max(rho, crad[k]); }
    if (hole >= 0 && targetless) rho = -1;
    printf("{\"hole\": %d, \"hole_degree\": %d, \"n_states\": %zu, \"n_filled\": %lld, \"n_classes\": %d, \"targetless_classes\": %d, \"rho\": %d, \"classes\": [",
           hole, nlink, D, nf, ncl, targetless, hole >= 0 ? rho : -1);
    for (int k = 0; k < ncl; k++) printf("%s{\"size\": %lld, \"filled\": %lld, \"radius\": %d}", k ? ", " : "", csize[k], cfill[k], crad[k]);
    printf("]");
    if (argc > 3) { FILE *qf = fopen(argv[3], "r"); int v, x; int qc[64]; for (int i = 0; i < N; i++) qc[i] = -1;
        while (fscanf(qf, "%d %d", &v, &x) == 2) if (v != hole && idx[v] >= 0) qc[idx[v]] = x;
        long long s = lookup(qc);
        if (s < 0) printf(", \"query\": {\"error\": \"not a state\"}");
        else printf(", \"query\": {\"class_size\": %lld, \"class_filled\": %lld, \"class_radius\": %d, \"dist\": %d}", csize[cl[s]], cfill[cl[s]], crad[cl[s]], dist[s]);
    }
    printf("}\n");
    return 0;
}
