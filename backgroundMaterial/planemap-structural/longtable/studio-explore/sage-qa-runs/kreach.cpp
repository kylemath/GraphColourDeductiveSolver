// [exploratory] Sage QA run 2: Kempe moves on T - v restricted to components that MEET THE LINK of v (LINKONLY=1), or
// unrestricted (LINKONLY unset). Both move sets are symmetric. Reports classes, targetless classes (no filled state:
// link on <= 3 colours), and depth = max over states of the fewest moves to a filled state (-1 if some state cannot
// reach one). Input: "n E" then edges. Usage: kreach FILE HOLE
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <map>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N, nl; static u64 adjm[64], linkmask; static int linkv[64], col[64]; static std::vector<Key> S;
static Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static u64 flood(u64 st, u64 M) { u64 comp = st, front = st; while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; } return comp; }
static void rec(int i, int used) { if (i == N) { S.push_back(keyof(col)); return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4; for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); } }
static long long lookup(const int *c) { int mp[4] = {-1, -1, -1, -1}, nx = 0, nc[64]; for (int i = 0; i < N; i++) { if (mp[c[i]] < 0) mp[c[i]] = nx++; nc[i] = mp[c[i]]; }
    Key k = keyof(nc); auto it = std::lower_bound(S.begin(), S.end(), k); return (it != S.end() && *it == k) ? it - S.begin() : -1; }
static std::vector<int> par; static int find(int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; }
int main(int argc, char **argv) {
    FILE *fp = fopen(argv[1], "r"); int n, E; if (fscanf(fp, "%d %d", &n, &E) != 2) return 2; int hole = atoi(argv[2]);
    bool linkonly = getenv("LINKONLY") != nullptr;
    std::vector<std::vector<int>> adj(n); for (int e = 0; e < E; e++) { int a, b; if (fscanf(fp, "%d %d", &a, &b) != 2) return 2; adj[a].push_back(b); adj[b].push_back(a); }
    for (auto &l : adj) { std::sort(l.begin(), l.end()); l.erase(std::unique(l.begin(), l.end()), l.end()); }
    int start = adj[hole][0]; std::vector<int> order{start}, idx(n, -1); idx[start] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (w != hole && idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); if (N != n - 1 || N > 64) { printf("{\"error\": \"size\"}\n"); return 0; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) if (w != hole) adjm[i] |= 1ULL << idx[w]; }
    nl = 0; linkmask = 0; for (int w : adj[hole]) { linkv[nl++] = idx[w]; linkmask |= 1ULL << idx[w]; }
    col[0] = 0; rec(1, 1); std::sort(S.begin(), S.end());
    size_t D = S.size(); par.resize(D); for (size_t i = 0; i < D; i++) par[i] = i;
    std::vector<std::vector<int>> G(D); std::vector<char> filled(D); int c[64], d[64];
    for (size_t s = 0; s < D; s++) { unkey(S[s], c); int seen = 0; for (int t = 0; t < nl; t++) seen |= 1 << c[linkv[t]]; filled[s] = __builtin_popcount(seen) <= 3;
        u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
            while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; if (linkonly && !(K & linkmask)) continue;
                for (int i = 0; i < N; i++) { d[i] = c[i]; if (K >> i & 1) d[i] = (c[i] == p) ? q : p; }
                long long t = lookup(d); if (t < 0) { printf("{\"error\": \"swap\"}\n"); return 0; } if (t == (long long)s) continue;
                G[s].push_back(t); int a = find(s), b = find(t); if (a != b) par[a] = b; } } }
    std::vector<int> dist(D, -1), q; for (size_t s = 0; s < D; s++) if (filled[s]) { dist[s] = 0; q.push_back(s); }
    for (size_t h = 0; h < q.size(); h++) for (int t : G[q[h]]) if (dist[t] < 0) { dist[t] = dist[q[h]] + 1; q.push_back(t); }
    std::map<int, int> hasf, sz; for (size_t s = 0; s < D; s++) { int r = find(s); sz[r]++; if (filled[s]) hasf[r] = 1; }
    int targetless = 0; for (auto &kv : sz) if (!hasf.count(kv.first)) targetless++;
    int depth = 0, unreach = 0; for (size_t s = 0; s < D; s++) { if (dist[s] < 0) unreach++; else depth = std::max(depth, dist[s]); }
    printf("{\"hole\": %d, \"link_only\": %s, \"states\": %zu, \"classes\": %zu, \"targetless_classes\": %d, \"unreachable_states\": %d, \"depth\": %d}\n",
           hole, linkonly ? "true" : "false", D, sz.size(), targetless, unreach, depth);
    return 0;
}
