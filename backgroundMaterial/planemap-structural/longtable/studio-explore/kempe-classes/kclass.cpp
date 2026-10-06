// [exploratory] Studio compute kclass.cpp: Kempe classes of the proper 4-colourings of G - h (or of G when h = -1).
// States are colourings up to colour renaming (canonical by first occurrence along a BFS order).
// Moves: swap colours on one whole two-colour component (singletons allowed), as in Studio intel's kempe.cpp.
// Union-find over all states. If a hole is given, "filled" = the hole's neighbours use <= 3 colours, and a class with
// no filled state is TARGETLESS (for a degree-5 hole: a class where R* fails).
// Input file: "n E" then E lines "a b" (undirected, labels 0..n-1). Usage: kclass FILE HOLE(-1 = none) [STATE_CAP]
// Output: one JSON line. Requires at most 64 vertices after deletion.
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
static std::vector<Key> S; static long long cap;
static inline Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static inline void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static inline u64 flood(u64 start, u64 M) { u64 comp = start, front = start;
    while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; }
    return comp; }
static void rec(int i, int used) {
    if (i == N) { S.push_back(keyof(col)); if ((long long)S.size() > cap) { printf("{\"inconclusive\": \"more than %lld states\"}\n", cap); exit(0); } return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4;
    for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); }
}
static std::vector<int> par;
static int find(int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; }
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: kclass FILE HOLE [STATE_CAP]\n"); return 2; }
    FILE *fp = fopen(argv[1], "r"); int n, E; if (fscanf(fp, "%d %d", &n, &E) != 2) return 2;
    int hole = atoi(argv[2]); cap = argc > 3 ? atoll(argv[3]) : 50000000LL;
    std::vector<std::vector<int>> adj(n);
    for (int e = 0; e < E; e++) { int a, b; if (fscanf(fp, "%d %d", &a, &b) != 2) return 2; if (a == b) continue; adj[a].push_back(b); adj[b].push_back(a); }
    for (auto &l : adj) { std::sort(l.begin(), l.end()); l.erase(std::unique(l.begin(), l.end()), l.end()); }
    int start = 0; if (hole >= 0) start = adj[hole][0]; else start = 0;
    std::vector<int> order{start}, idx(n, -1); idx[start] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (w != hole && idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); int expect = hole >= 0 ? n - 1 : n;
    if (N > 64 || N != expect) { printf("{\"error\": \"N=%d unsupported or disconnected\"}\n", N); return 0; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) if (w != hole) adjm[i] |= 1ULL << idx[w]; }
    nlink = 0; if (hole >= 0) for (int w : adj[hole]) linkv[nlink++] = idx[w];
    col[0] = 0; rec(1, 1);
    std::sort(S.begin(), S.end());
    size_t D = S.size(); par.resize(D); for (size_t i = 0; i < D; i++) par[i] = i;
    std::vector<char> filled(D, 0);
    int c[64], nc[64];
    for (size_t s = 0; s < D; s++) {
        unkey(S[s], c);
        if (hole >= 0) { int seen = 0; for (int t = 0; t < nlink; t++) seen |= 1 << c[linkv[t]]; filled[s] = __builtin_popcount(seen) <= 3; }
        u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) {
            u64 M = cm[p] | cm[q];
            while (M) {
                u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
                int mp[4] = {-1, -1, -1, -1}, nx = 0;
                for (int i = 0; i < N; i++) { int x = c[i]; if (K >> i & 1) x = (x == p) ? q : p; if (mp[x] < 0) mp[x] = nx++; nc[i] = mp[x]; }
                Key nk = keyof(nc); auto it = std::lower_bound(S.begin(), S.end(), nk);
                if (it == S.end() || !(*it == nk)) { printf("{\"error\": \"swap left the state space\"}\n"); return 0; }
                int a = find(s), b = find(it - S.begin()); if (a != b) par[a] = b;
            }
        }
    }
    std::map<int, long long> size; std::map<int, int> hasfill;
    for (size_t s = 0; s < D; s++) { int r = find(s); size[r]++; if (filled[s]) hasfill[r] = 1; }
    long long targetless = 0, nf = 0; for (auto &kv : size) if (!hasfill.count(kv.first)) targetless++;
    for (size_t s = 0; s < D; s++) nf += filled[s];
    std::vector<long long> sz; for (auto &kv : size) sz.push_back(kv.second); std::sort(sz.rbegin(), sz.rend());
    printf("{\"hole\": %d, \"hole_degree\": %d, \"n_states\": %zu, \"n_filled\": %lld, \"n_classes\": %zu, \"targetless_classes\": %lld, \"class_sizes\": [",
           hole, nlink, D, nf, size.size(), targetless);
    for (size_t i = 0; i < sz.size() && i < 10; i++) printf("%s%lld", i ? ", " : "", sz[i]);
    printf("]}\n");
    return 0;
}
