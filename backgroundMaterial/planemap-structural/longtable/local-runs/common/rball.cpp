// [exploratory] Local compute rball.cpp: exact Kempe radius of GIVEN states at a hole, by BFS from each state (no full
// enumeration, so it works on graphs too large for krad). Same move set as kclass.cpp/krad.cpp: swap two colours on one whole
// two-colour component of T - h; states up to renaming (canonical by first occurrence in vertex-index order).
// r(s) = fewest moves from s to a filled state (hole's neighbours on <= 3 colours). BFS stops at the first layer that holds a
// filled state, or reports r = -1 (inconclusive) if depth DMAX or CAP states are exceeded.
// Input: "n E", E lines "a b", then "hole Q", then Q lines of n colours (the hole's entry is ignored).
// Usage: rball FILE [DMAX=9] [CAP=20000000]. Output: one line per query "r visited".
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <unordered_set>
#include <algorithm>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
struct KH { size_t operator()(const Key&k) const { return k.hi * 0x9E3779B97F4A7C15ULL ^ (k.lo + 0x632BE59BD9B4E019ULL + (k.hi << 6)); } };
static int N, nlink; static u64 adjm[64]; static int linkv[64];
static Key keyof(const int *c) { int mp[4] = {-1, -1, -1, -1}, nx = 0; Key k{0, 0};
    for (int i = 0; i < N; i++) { if (mp[c[i]] < 0) mp[c[i]] = nx++; u64 x = mp[c[i]]; if (i < 32) k.hi |= x << (62 - 2 * i); else k.lo |= x << (62 - 2 * (i - 32)); } return k; }
static void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static u64 flood(u64 st, u64 M) { u64 comp = st, front = st; while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; } return comp; }
static bool filled(const int *c) { int seen = 0; for (int t = 0; t < nlink; t++) seen |= 1 << c[linkv[t]]; return __builtin_popcount(seen) <= 3; }
int main(int argc, char **argv) {
    FILE *fp = fopen(argv[1], "r"); int dmax = argc > 2 ? atoi(argv[2]) : 9; long long cap = argc > 3 ? atoll(argv[3]) : 20000000LL;
    int n, E; if (fscanf(fp, "%d %d", &n, &E) != 2) return 2;
    std::vector<std::vector<int>> adj(n);
    for (int e = 0; e < E; e++) { int a, b; if (fscanf(fp, "%d %d", &a, &b) != 2) return 2; adj[a].push_back(b); adj[b].push_back(a); }
    int hole, Q; if (fscanf(fp, "%d %d", &hole, &Q) != 2) return 2;
    std::vector<int> idx(n, -1), order; for (int u = 0; u < n; u++) if (u != hole) { idx[u] = order.size(); order.push_back(u); }
    N = order.size(); if (N > 64) { printf("error N>64\n"); return 0; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) if (w != hole) adjm[i] |= 1ULL << idx[w]; }
    nlink = 0; for (int w : adj[hole]) linkv[nlink++] = idx[w];
    std::vector<int> raw(n); int c[64], d[64];
    for (int qi = 0; qi < Q; qi++) {
        for (int u = 0; u < n; u++) if (fscanf(fp, "%d", &raw[u]) != 1) return 2;
        for (int i = 0; i < N; i++) c[i] = raw[order[i]];
        bool ok = true; for (int i = 0; i < N; i++) for (u64 f = adjm[i]; f; f &= f - 1) if (c[__builtin_ctzll(f)] == c[i]) ok = false;
        if (!ok) { printf("improper 0\n"); continue; }
        if (filled(c)) { printf("0 1\n"); continue; }
        std::unordered_set<Key, KH> seen; std::vector<Key> fr{keyof(c)}; seen.insert(fr[0]);
        int r = -1; long long vis = 1;
        for (int depth = 1; depth <= dmax && r < 0 && vis <= cap; depth++) {
            std::vector<Key> nx;
            for (const Key &k : fr) { unkey(k, c); u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
                for (int p = 0; p < 4 && r < 0; p++) for (int q = p + 1; q < 4 && r < 0; q++) { u64 M = cm[p] | cm[q];
                    while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
                        for (int i = 0; i < N; i++) { d[i] = c[i]; if (K >> i & 1) d[i] = (c[i] == p) ? q : p; }
                        Key nk = keyof(d); if (!seen.insert(nk).second) continue; vis++;
                        if (filled(d)) { r = depth; break; } nx.push_back(nk); } }
                if (r >= 0) break; }
            fr.swap(nx);
        }
        printf("%d %lld\n", r, vis); fflush(stdout);
    }
    return 0;
}
