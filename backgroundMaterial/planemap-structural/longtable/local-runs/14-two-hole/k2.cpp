// [exploratory] Local compute k2.cpp: Kempe classes of T - v - w for pairs of degree-5 holes (v, w), with per-class counts for
// two-hole floor candidates. Same enumeration, canonical form and moves as krad.cpp / kclass.cpp (whole two-colour component swaps
// in T - v - w, states up to renaming).
// Per class: size; Fv = states whose v-link (the coloured neighbours of v) uses <= 3 colours; Fw likewise; Fboth; Fany;
// Fext = states that extend to a proper colouring of T (colour v and w; for adjacent v, w they must also differ);
// and, when v and w are NOT adjacent, the per-j counts at v and at w: F_i (filled, singleton at link position i) and
// U_j (unfilled, c(x_j) = c(x_{j+2})), links in rotation order.
// Input: "n E", E lines "a b", then "P", then P lines "v w v0 v1 v2 v3 v4 w0 w1 w2 w3 w4". Output: one JSON line per pair.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <algorithm>
#include <array>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N; static u64 adjm[64]; static int col[64]; static std::vector<Key> S;
static Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static u64 flood(u64 st, u64 M) { u64 comp = st, front = st; while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; } return comp; }
static void rec(int i, int used) { if (i == N) { S.push_back(keyof(col)); return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4; for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); } }
static long long lookup(const int *c) { int mp[4] = {-1, -1, -1, -1}, nx = 0, nc[64]; for (int i = 0; i < N; i++) { if (mp[c[i]] < 0) mp[c[i]] = nx++; nc[i] = mp[c[i]]; }
    Key k = keyof(nc); auto it = std::lower_bound(S.begin(), S.end(), k); return (it != S.end() && *it == k) ? it - S.begin() : -1; }
int main(int argc, char **argv) {
    FILE *fp = fopen(argv[1], "r"); int n, E; if (fscanf(fp, "%d %d", &n, &E) != 2) return 2;
    std::vector<std::vector<int>> adj(n);
    for (int e = 0; e < E; e++) { int a, b; if (fscanf(fp, "%d %d", &a, &b) != 2) return 2; adj[a].push_back(b); adj[b].push_back(a); }
    int P; if (fscanf(fp, "%d", &P) != 1) return 2;
    for (int pi = 0; pi < P; pi++) {
        int v, w, LV[5], LW[5]; if (fscanf(fp, "%d %d", &v, &w) != 2) return 2;
        for (int t = 0; t < 5; t++) if (fscanf(fp, "%d", &LV[t]) != 1) return 2;
        for (int t = 0; t < 5; t++) if (fscanf(fp, "%d", &LW[t]) != 1) return 2;
        bool adjvw = std::find(adj[v].begin(), adj[v].end(), w) != adj[v].end();
        int start = LV[0] != w ? LV[0] : LV[1];
        std::vector<int> order{start}, idx(n, -1); idx[start] = 0;
        for (size_t h = 0; h < order.size(); h++) for (int x : adj[order[h]]) if (x != v && x != w && idx[x] < 0) { idx[x] = order.size(); order.push_back(x); }
        N = order.size(); if (N != n - 2 || N > 64) { printf("{\"v\": %d, \"w\": %d, \"error\": \"size\"}\n", v, w); continue; }
        for (int i = 0; i < N; i++) { adjm[i] = 0; for (int x : adj[order[i]]) if (x != v && x != w) adjm[i] |= 1ULL << idx[x]; }
        int lv[5], lw[5]; for (int t = 0; t < 5; t++) { lv[t] = LV[t] == w ? -1 : idx[LV[t]]; lw[t] = LW[t] == v ? -1 : idx[LW[t]]; }
        S.clear(); col[0] = 0; rec(1, 1); std::sort(S.begin(), S.end());
        size_t D = S.size(); std::vector<int> par(D); for (size_t i = 0; i < D; i++) par[i] = i;
        auto find = [&](int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
        int c[64], d[64];
        // per-state attributes: bit0 Fv, bit1 Fw, bit2 ext; per-j codes
        std::vector<unsigned char> att(D); std::vector<signed char> fiv(D, -1), ujv(D, -1), fiw(D, -1), ujw(D, -1);
        for (size_t s = 0; s < D; s++) {
            unkey(S[s], c); u64 cm[4] = {0, 0, 0, 0}; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i;
            int sv = 0, sw = 0; for (int t = 0; t < 5; t++) { if (lv[t] >= 0) sv |= 1 << c[lv[t]]; if (lw[t] >= 0) sw |= 1 << c[lw[t]]; }
            bool fv = __builtin_popcount(sv) <= 3, fw = __builtin_popcount(sw) <= 3, ext;
            if (!adjvw) ext = fv && fw;
            else { ext = false; for (int a = 0; a < 4; a++) if (!(sv >> a & 1)) for (int b = 0; b < 4; b++) if (b != a && !(sw >> b & 1)) ext = true; }
            att[s] = fv | fw << 1 | ext << 2;
            if (!adjvw) {
                int a5[5], b5[5]; for (int t = 0; t < 5; t++) { a5[t] = c[lv[t]]; b5[t] = c[lw[t]]; }
                auto pj = [&](int *x, signed char &fi, signed char &uj) {
                    int seen = 0; for (int t = 0; t < 5; t++) seen |= 1 << x[t];
                    if (__builtin_popcount(seen) <= 3) { for (int i = 0; i < 5; i++) { int m = 0; for (int t = 0; t < 5; t++) m += x[t] == x[i]; if (m == 1) fi = i; } }
                    else for (int j = 0; j < 5; j++) if (x[j] == x[(j + 2) % 5]) uj = j; };
                pj(a5, fiv[s], ujv[s]); pj(b5, fiw[s], ujw[s]);
            }
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K;
                    for (int i = 0; i < N; i++) { d[i] = c[i]; if (K >> i & 1) d[i] = (c[i] == p) ? q : p; }
                    long long t = lookup(d); int a = find(s), b = find(t); if (a != b) par[a] = b; } }
        }
        std::vector<int> root(D); std::vector<int> cid(D, -1); int ncl = 0;
        for (size_t s = 0; s < D; s++) { int r = find(s); if (cid[r] < 0) cid[r] = ncl++; root[s] = cid[r]; }
        std::vector<std::array<long long, 26>> A(ncl); for (auto &a : A) a.fill(0);
        for (size_t s = 0; s < D; s++) { auto &a = A[root[s]]; a[0]++; a[1] += att[s] & 1; a[2] += att[s] >> 1 & 1; a[3] += (att[s] & 3) == 3; a[4] += (att[s] & 3) != 0; a[5] += att[s] >> 2 & 1;
            if (fiv[s] >= 0) a[6 + fiv[s]]++; if (ujv[s] >= 0) a[11 + ujv[s]]++; if (fiw[s] >= 0) a[16 + fiw[s]]++; if (ujw[s] >= 0) a[21 + ujw[s]]++; }
        printf("{\"v\": %d, \"w\": %d, \"adjacent\": %s, \"states\": %zu, \"classes\": [", v, w, adjvw ? "true" : "false", D);
        for (int k = 0; k < ncl; k++) { printf("%s[", k ? ", " : ""); for (int t = 0; t < 26; t++) printf("%s%lld", t ? ", " : "", A[k][t]); printf("]"); }
        printf("]}\n"); fflush(stdout);
    }
    return 0;
}
