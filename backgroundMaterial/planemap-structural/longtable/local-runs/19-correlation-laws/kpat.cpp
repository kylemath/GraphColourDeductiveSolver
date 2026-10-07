// [exploratory] Local compute item 19: per-class link-pattern counts at every hole of degree 5..7.
// Same enumeration, canonical form and Kempe moves as common/krad.cpp (states = proper 4-colourings of T-hole up to renaming,
// canonical by first occurrence along BFS from the hole's first neighbour; moves = swap on one whole 2-colour component).
// Input (stdin): n, then for each vertex: deg nb_1..nb_deg (rotation order, 0-based). Usage: kpat < graph  (all holes of degree 5..7)
// Output: one JSON line per hole: {"hole":h,"deg":d,"classes":[[size,{"01020":count,...}],...]}
// The pattern is the colour sequence of the link x_0..x_{d-1} (rotation order of the input), relabelled by first occurrence.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <map>
#include <string>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
             bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N; static u64 adjm[64]; static int col[64];
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
int main() {
    int n; if (scanf("%d", &n) != 1) return 2;
    std::vector<std::vector<int>> rot(n);
    for (int v = 0; v < n; v++) { int d; if (scanf("%d", &d) != 1) return 2; rot[v].resize(d); for (int t = 0; t < d; t++) if (scanf("%d", &rot[v][t]) != 1) return 2; }
    std::vector<std::vector<int>> adj = rot; for (auto &l : adj) std::sort(l.begin(), l.end());
    for (int hole = 0; hole < n; hole++) {
        int d = rot[hole].size(); if (d < 5 || d > 7) continue;
        int start = adj[hole][0];
        std::vector<int> order{start}, idx(n, -1); idx[start] = 0;
        for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (w != hole && idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
        N = order.size(); if (N != n - 1) { printf("{\"error\":\"disconnected\"}\n"); continue; }
        for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) if (w != hole) adjm[i] |= 1ULL << idx[w]; }
        int LP[8]; for (int t = 0; t < d; t++) LP[t] = idx[rot[hole][t]];
        S.clear(); col[0] = 0; rec(1, 1); std::sort(S.begin(), S.end());
        size_t D = S.size(); std::vector<std::vector<int>> G(D); int c[64], dd[64];
        for (size_t s = 0; s < D; s++) {
            unkey(S[s], c);
            u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) {
                u64 M = cm[p] | cm[q];
                while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
                    for (int i = 0; i < N; i++) { dd[i] = c[i]; if (K >> i & 1) dd[i] = (c[i] == p) ? q : p; }
                    long long t = lookup(dd); if (t < 0) { printf("{\"error\":\"left space\"}\n"); return 0; }
                    if (t != (long long)s) G[s].push_back(t); }
            }
        }
        std::vector<int> cl(D, -1); int ncl = 0;
        for (size_t s = 0; s < D; s++) if (cl[s] < 0) { std::vector<int> q{(int)s}; cl[s] = ncl;
            for (size_t h = 0; h < q.size(); h++) for (int t : G[q[h]]) if (cl[t] < 0) { cl[t] = ncl; q.push_back(t); } ncl++; }
        std::vector<long long> csize(ncl, 0); std::vector<std::map<std::string, long long>> pc(ncl);
        for (size_t s = 0; s < D; s++) { unkey(S[s], c); csize[cl[s]]++;
            int mp[4] = {-1, -1, -1, -1}, nx = 0; std::string pat;
            for (int t = 0; t < d; t++) { int x = c[LP[t]]; if (mp[x] < 0) mp[x] = nx++; pat += (char)('0' + mp[x]); }
            pc[cl[s]][pat]++; }
        printf("{\"hole\":%d,\"deg\":%d,\"states\":%zu,\"classes\":[", hole, d, D);
        for (int k = 0; k < ncl; k++) { printf("%s[%lld,{", k ? "," : "", csize[k]); bool first = true;
            for (auto &kv : pc[k]) { printf("%s\"%s\":%lld", first ? "" : ",", kv.first.c_str(), kv.second); first = false; } printf("}]"); }
        printf("]}\n"); fflush(stdout);
    }
    return 0;
}
