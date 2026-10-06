// [exploratory] Conjecture K3 test (coordinator, from the sage's k-step idea). Hole v of degree 5 in a triangulation T.
// States: 4-colourings of T - v up to renaming; moves: whole two-colour component swaps. For an UNFILLED state (link on 4
// colours) with repeat c(x_j) = c(x_{j+2}), m = x_{j+1}, a = x_{j+3}, b = x_{j+4}, mu = c(m), A = c(a), B = c(b):
//   lock_size = |{mu,A}-component of m| + |{mu,B}-component of m|        (same as potentials2.py, run 5)
//   lock_dist = (BFS path length m -> a inside the first, 0 if a not in it) + (same for m -> b in the second)
//   Phi = (lock_size, lock_dist) in lex order.
// dist = fewest moves to a filled state. For every unfilled state with dist >= DMIN, least k = fewest moves to a state that
// is filled or has strictly smaller Phi. Output JSON: counts, histogram of least k, max k, and the first state with k >= 4.
// Input: "n F" then F lines "a b c" (faces). Usage: k3 FILE HOLE [DMIN=4]
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <map>
#include <set>
#include <array>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N; static u64 adjm[64]; static int link_[5], col[64]; static std::vector<Key> S;
static Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static u64 flood(u64 st, u64 M) { u64 comp = st, front = st; while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; } return comp; }
static int pathlen(int s, int t, u64 M) { if (!(M >> t & 1)) return 0; u64 seen = 1ULL << s, front = 1ULL << s; int d = 0;
    while (front) { if (front >> t & 1) return d; u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~seen; seen |= nb; front = nb; d++; } return 0; }
static void rec(int i, int used) { if (i == N) { S.push_back(keyof(col)); return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4; for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); } }
static long long lookup(const int *c) { int mp[4] = {-1, -1, -1, -1}, nx = 0, nc[64]; for (int i = 0; i < N; i++) { if (mp[c[i]] < 0) mp[c[i]] = nx++; nc[i] = mp[c[i]]; }
    Key k = keyof(nc); auto it = std::lower_bound(S.begin(), S.end(), k); return (it != S.end() && *it == k) ? it - S.begin() : -1; }
int main(int argc, char **argv) {
    FILE *fp = fopen(argv[1], "r"); int n, F; if (fscanf(fp, "%d %d", &n, &F) != 2) return 2; int hole = atoi(argv[2]); int dmin = argc > 3 ? atoi(argv[3]) : 4;
    std::vector<std::array<int,3>> faces(F); for (auto &f : faces) if (fscanf(fp, "%d %d %d", &f[0], &f[1], &f[2]) != 3) return 2;
    std::vector<std::set<int>> adj(n); std::map<int,int> succ;
    for (auto &f : faces) for (int t = 0; t < 3; t++) { int a = f[t], b = f[(t + 1) % 3]; if (a == hole) succ[b] = f[(t + 2) % 3];
        if (a != hole && b != hole) { adj[a].insert(b); adj[b].insert(a); } }
    if (succ.size() != 5) { printf("{\"error\": \"hole not degree 5\"}\n"); return 0; }
    int L[5]; L[0] = succ.begin()->first; for (int t = 1; t < 5; t++) L[t] = succ[L[t - 1]];
    std::vector<int> order{L[0]}, idx(n, -1); idx[L[0]] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); if (N > 64 || N != n - 1) { printf("{\"error\": \"size\"}\n"); return 0; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) adjm[i] |= 1ULL << idx[w]; }
    for (int t = 0; t < 5; t++) link_[t] = idx[L[t]];
    col[0] = 0; rec(1, 1); std::sort(S.begin(), S.end());
    size_t D = S.size(); std::vector<std::vector<int>> G(D); std::vector<char> unf(D); std::vector<long long> phi(D, -1); int c[64], d[64];
    for (size_t s = 0; s < D; s++) { unkey(S[s], c); u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
        int seen = 0; for (int t = 0; t < 5; t++) seen |= 1 << c[link_[t]]; unf[s] = __builtin_popcount(seen) == 4;
        if (unf[s]) { int j = 0; for (; j < 5; j++) if (c[link_[j]] == c[link_[(j + 2) % 5]]) break;
            int m = link_[(j + 1) % 5], a = link_[(j + 3) % 5], b = link_[(j + 4) % 5], mu = c[m];
            u64 Ka = flood(1ULL << m, cm[mu] | cm[c[a]]), Kb = flood(1ULL << m, cm[mu] | cm[c[b]]);
            long long size = __builtin_popcountll(Ka) + __builtin_popcountll(Kb), dd = pathlen(m, a, Ka) + pathlen(m, b, Kb);
            phi[s] = size * 1000 + dd; }
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
            while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
                for (int i = 0; i < N; i++) { d[i] = c[i]; if (K >> i & 1) d[i] = (c[i] == p) ? q : p; }
                long long t = lookup(d); if (t >= 0 && t != (long long)s) G[s].push_back(t); } } }
    std::vector<int> dist(D, -1), qq; for (size_t s = 0; s < D; s++) if (!unf[s]) { dist[s] = 0; qq.push_back(s); }
    for (size_t h = 0; h < qq.size(); h++) for (int t : G[qq[h]]) if (dist[t] < 0) { dist[t] = dist[qq[h]] + 1; qq.push_back(t); }
    std::map<int, long long> hist; int maxk = 0, maxdist = 0; long long tested = 0, ge4 = 0; long long first = -1; int firstk = 0;
    std::vector<int> mark(D, -1), lev(D);
    for (size_t s0 = 0; s0 < D; s0++) { maxdist = std::max(maxdist, dist[s0]); if (!unf[s0] || dist[s0] < dmin) continue; tested++;
        std::vector<int> fr{(int)s0}; mark[s0] = s0; int k = 0, found = -1;
        while (!fr.empty() && found < 0) { k++; std::vector<int> nx;
            for (int x : fr) { for (int t : G[x]) { if (mark[t] == (int)s0) continue; mark[t] = s0;
                    if (!unf[t] || phi[t] < phi[s0]) { found = k; break; } nx.push_back(t); } if (found >= 0) break; }
            fr.swap(nx); }
        hist[found]++; maxk = std::max(maxk, found); if (found >= 4) { ge4++; if (first < 0) { first = s0; firstk = found; } } }
    printf("{\"hole\": %d, \"states\": %zu, \"max_dist\": %d, \"tested_states\": %lld, \"leastk_hist\": {", hole, D, maxdist, tested);
    bool f1 = true; for (auto &kv : hist) { printf("%s\"%d\": %lld", f1 ? "" : ", ", kv.first, kv.second); f1 = false; }
    printf("}, \"max_k\": %d, \"k_ge4\": %lld", maxk, ge4);
    if (first >= 0) { unkey(S[first], c); printf(", \"first_k_ge4\": {\"k\": %d, \"dist\": %d, \"colouring\": {", firstk, dist[first]);
        for (int i = 0; i < N; i++) printf("%s\"%d\": %d", i ? ", " : "", order[i], c[i]); printf("}}"); }
    printf("}\n"); return 0;
}
