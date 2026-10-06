// studiointel fast/kempe_classes.cpp -- [exploratory] Kempe classes of T-v: all canonical states stored, union-find over whole-component swaps;
// per class: size, #filled, #DL. Derived from kempe.cpp (same enumeration and canonical form). Exact Kempe radius at a degree-5 hole. Same definitions as ../radius.py:
//  state = proper 4-colouring of T-v, canonical by first occurrence along the BFS order of T-v from link[0] (neighbours by ascending label);
//  filled = link uses <= 3 colours; DL = lock1 (a in {c(m),c(a)}-comp of m) and lock2 (b in {c(m),c(b)}-comp of m), m=x_{j+1}, a=x_{j+3}, b=x_{j+4};
//  moves = whole-component Kempe swaps in T-v; r = 1 + d(s, NL) for DL states.
// Memory: only DL states are stored (sorted 128-bit keys); swap graph is recomputed on the fly (two expansions per DL state).
// Input file: "n F" then F lines "a b c" (counter-clockwise faces, labels 0..n-1). Usage: kempe FILE HOLE [CAP_DL] [TARGETLESS_OUT]
// Output: one JSON line. Requires n-1 <= 64.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <string>
#include <array>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N;                 // vertices of T-v
static u64 adjm[64];          // adjacency masks in BFS-order indices
static int link_[5];          // link positions in BFS-order indices
static std::vector<Key> DL; static std::vector<Key> ALL; static std::vector<char> KIND;
static long long n_states = 0, n_filled = 0, n_nondl = 0; static long long capDL;
static int col[64];

static inline u64 flood(u64 start, u64 M) {
    u64 comp = start, front = start;
    while (front) {
        u64 nb = 0, f = front;
        while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; }
        nb &= M & ~comp; comp |= nb; front = nb;
    }
    return comp;
}
static inline int filled_or_dl(const int *c, u64 *cm) {  // 0 filled, 1 nonDL, 2 DL
    int seen = 0; for (int t = 0; t < 5; t++) seen |= 1 << c[link_[t]];
    if (__builtin_popcount(seen) <= 3) return 0;
    int j = 0; for (; j < 5; j++) if (c[link_[j]] == c[link_[(j + 2) % 5]]) break;
    int m = link_[(j + 1) % 5], a = link_[(j + 3) % 5], b = link_[(j + 4) % 5];
    int mu = c[m];
    u64 K = flood(1ULL << m, cm[mu] | cm[c[a]]); if (!(K >> a & 1)) return 1;
    K = flood(1ULL << m, cm[mu] | cm[c[b]]); if (!(K >> b & 1)) return 1;
    return 2;
}
static inline Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static inline void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static void masks(const int *c, u64 *cm) { cm[0] = cm[1] = cm[2] = cm[3] = 0; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i; }

static void rec(int i, int used) {
    if (i == N) {
        n_states++; u64 cm[4]; masks(col, cm);
        int k = filled_or_dl(col, cm);
        if (k == 0) n_filled++; else if (k == 1) n_nondl++;
        ALL.push_back(keyof(col)); KIND.push_back(k); if ((long long)ALL.size() > capDL) { printf("{\"inconclusive\": \"more than %lld states\"}\n", capDL); exit(0); }
        return;
    }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4;
    for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); }
}
// enumerate swap neighbours of DL state idx; callback(isDL, index)
template <class F> static void neighbours(const Key &k, F cb) {
    int c[64], nc[64]; unkey(k, c); u64 cm[4]; masks(c, cm);
    for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) {
        u64 M = cm[p] | cm[q];
        while (M) {
            u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
            int mp[4] = {-1, -1, -1, -1}, nx = 0;
            for (int i = 0; i < N; i++) { int x = c[i]; if (K >> i & 1) x = (x == p) ? q : p; if (mp[x] < 0) mp[x] = nx++; nc[i] = mp[x]; }
            int seen = 0; for (int t = 0; t < 5; t++) seen |= 1 << nc[link_[t]];
            if (__builtin_popcount(seen) <= 3) { cb(false, -1); continue; }
            Key nk = keyof(nc);
            auto it = std::lower_bound(DL.begin(), DL.end(), nk);
            if (it != DL.end() && *it == nk) cb(true, (long long)(it - DL.begin())); else cb(false, -1);
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: kempe FILE HOLE [CAP_DL] [TARGETLESS_OUT]\n"); return 2; }
    FILE *fp = fopen(argv[1], "r"); int n, F; if (fscanf(fp, "%d %d", &n, &F) != 2) return 2;
    std::vector<std::array<int,3>> faces(F); for (auto &f : faces) if (fscanf(fp, "%d %d %d", &f[0], &f[1], &f[2]) != 3) return 2;
    int hole = atoi(argv[2]); capDL = argc > 3 ? atoll(argv[3]) : 200000000LL;
    std::vector<std::set<int>> adj(n); std::map<int,int> succ;
    for (auto &f : faces) for (int t = 0; t < 3; t++) {
        int a = f[t], b = f[(t + 1) % 3]; if (a == hole) succ[f[(t + 1) % 3]] = f[(t + 2) % 3];
        if (a != hole && b != hole) { adj[a].insert(b); adj[b].insert(a); } }
    if (succ.size() != 5) { printf("{\"error\": \"hole is not degree 5\"}\n"); return 0; }
    int L[5]; L[0] = succ.begin()->first; for (int t = 1; t < 5; t++) L[t] = succ[L[t - 1]];
    std::vector<int> order{L[0]}, idx(n, -1); idx[L[0]] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); if (N > 64 || N != n - 1) { printf("{\"error\": \"N=%d unsupported\"}\n", N); return 0; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) adjm[i] |= 1ULL << idx[w]; }
    for (int t = 0; t < 5; t++) link_[t] = idx[L[t]];
    col[0] = 0; rec(1, 1);
    // ALL is produced in lexicographic order of the colour tuple (vertex 0 most significant), i.e. sorted; check
    for (size_t i = 1; i < ALL.size(); i++) if (!(ALL[i-1] < ALL[i])) { fprintf(stderr, "not sorted\n"); return 3; }
    size_t S = ALL.size(); std::vector<long long> par(S); for (size_t i = 0; i < S; i++) par[i] = i;
    auto find = [&](long long x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    for (size_t i = 0; i < S; i++) {
        int c[64], nc[64]; unkey(ALL[i], c); u64 cm[4]; masks(c, cm);
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) {
            u64 M = cm[p] | cm[q];
            while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
                int mp[4] = {-1,-1,-1,-1}, nx = 0;
                for (int t = 0; t < N; t++) { int x = c[t]; if (K >> t & 1) x = (x == p) ? q : p; if (mp[x] < 0) mp[x] = nx++; nc[t] = mp[x]; }
                Key nk = keyof(nc); auto it = std::lower_bound(ALL.begin(), ALL.end(), nk);
                long long j = it - ALL.begin(); long long a = find(i), b = find(j); if (a != b) par[a] = b; } }
    }
    std::map<long long, std::array<long long,3>> cls;   // root -> size, filled, DL
    for (size_t i = 0; i < S; i++) { auto &e = cls[find(i)]; e[0]++; if (KIND[i] == 0) e[1]++; if (KIND[i] == 2) e[2]++; }
    long long nofill = 0; printf("{\"hole\": %d, \"n_states\": %zu, \"n_classes\": %zu, \"classes\": [", hole, S, cls.size());
    bool first = true; for (auto &kv : cls) { printf("%s[%lld, %lld, %lld]", first ? "" : ", ", kv.second[0], kv.second[1], kv.second[2]); first = false; if (kv.second[1] == 0) nofill++; }
    printf("], \"classes_without_filled_state\": %lld}\n", nofill);
    return 0;
}
