// path3-local/kempe_dd.cpp -- [exploratory] Local intel, 6 Oct 2026. Math C6 objective: DL rotation chains and per-j excess.
// Enumeration, canonical form and Kempe classes exactly as ../fast/kempe_classes3.cpp (union-find over whole-component swaps of all
// canonical proper 4-colourings of T - v; canonical = first occurrence along the BFS order of T - v from link[0]).
// Per state, with the notation of SolvingFrameworkPlan/docs/working/MathQuarterFloorBijections.md (link x_0..x_4 in rotation order):
//   filled f in F_i (singleton colour W at x_i; X at x_{i+1},x_{i+3}; Y at x_{i+2},x_{i+4}; Z absent):
//     M3 long <=> x_{i+2} ~ x_{i+4} in {Y,Z};  M2 long <=> x_{i+1} ~ x_{i+3} in {X,Z};  L_F = number of long bits.
//   unfilled s in U_j (alpha at x_j, x_{j+2}; mu at m = x_{j+1}; A at a = x_{j+3}; B at b = x_{j+4}):
//     lock1 <=> a in comp_{mu,A}(m);  lock2 <=> b in comp_{mu,B}(m);  R+3 (defined iff lock2): swap comp_{alpha,A}(x_{j+2}).
// Gamma = edges s -> R+3 s.  Paths (from lock1-fails/lock2-holds starts), d(P) = #DL interior; cycles = all-DL.
// Per class: F, U, N0, N1, D, L_F, #paths, max d(P), D_cyc, #cycles, max cycle length, identity check
//   3F - U == 2 N0 + 1.5 L_F + sum_P (1 - d(P)) - D_cyc;
// per j: DD_j = {d in D_j : R+3 d in D_{j+3}}, room_j = L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j|,
//   L_j = |F_{j+4}^{M3 long}| + |F_{j+3}^{M2 long}| + |F_{j+1}^{M2 long}|, E_j = {s in U_j: lock1 fails, lock2 holds, R+3 s not DL};
//   per-j identity check F_{j+1} + F_{j+3} + F_{j+4} - U_j == room_j - |DD_j|;  excess_j = |DD_j| - room_j.
// Sanity checks counted over all states: C2 dichotomies (M3, M2 for filled; "R+3 defined <=> lock2", "R+2 defined <=> lock1"),
//   R+3 image has lock1 (pd2 Corollary), R+3 image lies in the same class (it is a swap) and at index j+3.
// If some class has 3F < U (filled fraction < 1/4) or F = 0, all its states are dumped to argv[4].
// Usage: kempe_dd FILE HOLE [CAP] [DUMP]. Output: one JSON line.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <array>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N; static u64 adjm[64]; static int L5[5];
static std::vector<Key> ALL; static long long cap; static int col[64];
static inline u64 flood(u64 start, u64 M) { u64 comp = start, front = start;
    while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; }
    return comp; }
static inline Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static inline void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static void masks(const int *c, u64 *cm) { cm[0] = cm[1] = cm[2] = cm[3] = 0; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i; }
static void rec(int i, int used) {
    if (i == N) { ALL.push_back(keyof(col)); if ((long long)ALL.size() > cap) { printf("{\"inconclusive\": \"more than %lld states\"}\n", cap); exit(0); } return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4;
    for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); }
}
static inline long long lookup(const int *nc) { Key nk = keyof(nc); return std::lower_bound(ALL.begin(), ALL.end(), nk) - ALL.begin(); }
static inline void swapcanon(const int *c, u64 K, int p, int q, int *nc) {
    int mp[4] = {-1, -1, -1, -1}, nx = 0;
    for (int t = 0; t < N; t++) { int x = c[t]; if (K >> t & 1) x = (x == p) ? q : p; if (mp[x] < 0) mp[x] = nx++; nc[t] = mp[x]; } }
struct St { signed char filled, idx, lock1, lock2, m3long, m2long; long long r3; };   // idx = i (filled) or j (unfilled)

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: kempe_dd FILE HOLE [CAP] [DUMP]\n"); return 2; }
    FILE *fp = fopen(argv[1], "r"); int n, F; if (fscanf(fp, "%d %d", &n, &F) != 2) return 2;
    std::vector<std::array<int,3>> faces(F); for (auto &f : faces) if (fscanf(fp, "%d %d %d", &f[0], &f[1], &f[2]) != 3) return 2;
    int hole = atoi(argv[2]); cap = argc > 3 ? atoll(argv[3]) : 30000000LL;
    std::vector<std::set<int>> adj(n); std::map<int,int> succ;
    for (auto &f : faces) for (int t = 0; t < 3; t++) { int a = f[t], b = f[(t + 1) % 3]; if (a == hole) succ[f[(t + 1) % 3]] = f[(t + 2) % 3];
        if (a != hole && b != hole) { adj[a].insert(b); adj[b].insert(a); } }
    if (succ.size() != 5) { printf("{\"error\": \"hole is not degree 5\"}\n"); return 0; }
    int L[5]; L[0] = succ.begin()->first; for (int t = 1; t < 5; t++) L[t] = succ[L[t - 1]];
    std::vector<int> order{L[0]}, idx(n, -1); idx[L[0]] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); if (N > 64 || N != n - 1) { printf("{\"error\": \"N=%d unsupported\"}\n", N); return 0; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) adjm[i] |= 1ULL << idx[w]; }
    for (int t = 0; t < 5; t++) L5[t] = idx[L[t]];
    col[0] = 0; rec(1, 1);
    size_t S = ALL.size(); std::vector<long long> par(S); for (size_t i = 0; i < S; i++) par[i] = i;
    auto find = [&](long long x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    for (size_t i = 0; i < S; i++) { int c[64], nc[64]; unkey(ALL[i], c); u64 cm[4]; masks(c, cm);
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
            while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; swapcanon(c, K, p, q, nc);
                long long a = find(i), b = find(lookup(nc)); if (a != b) par[a] = b; } } }
    // per-state structure
    std::vector<St> st(S); long long bad_m3 = 0, bad_m2 = 0, bad_r3def = 0, bad_r2def = 0, bad_r3lock1 = 0, bad_r3idx = 0, bad_r3class = 0;
    auto x = [&](int t) { return L5[((t % 5) + 5) % 5]; };
    for (size_t s = 0; s < S; s++) {
        int c[64], nc[64]; unkey(ALL[s], c); u64 cm[4]; masks(c, cm); St &e = st[s]; e.r3 = -1; e.m3long = e.m2long = e.lock1 = e.lock2 = 0;
        int seen = 0; for (int t = 0; t < 5; t++) seen |= 1 << c[L5[t]];
        if (__builtin_popcount(seen) <= 3) {
            e.filled = 1; int i = 0;
            for (; i < 5; i++) { int w = c[x(i)], k = 0; for (int t = 0; t < 5; t++) k += c[L5[t]] == w; if (k == 1) break; }
            e.idx = i; int W = c[x(i)], X = c[x(i + 1)], Y = c[x(i + 2)], Z = 6 - W - X - Y;
            u64 K = flood(1ULL << x(i + 2), cm[Y] | cm[Z]); bool yz = K >> x(i + 4) & 1; e.m3long = yz;
            K = flood(1ULL << x(i + 3), cm[W] | cm[X]); bool wx = K >> x(i) & 1;
            if (!((!yz) ^ (!wx))) bad_m3++;
            K = flood(1ULL << x(i + 1), cm[X] | cm[Z]); bool xz = K >> x(i + 3) & 1; e.m2long = xz;
            K = flood(1ULL << x(i + 2), cm[W] | cm[Y]); bool wy = K >> x(i) & 1;      // M2: x_i ~ x_{i+2} in {W,Y} <=> short
            if (!((!xz) ^ (!wy))) bad_m2++;
        } else {
            e.filled = 0; int j = 0; for (; j < 5; j++) if (c[x(j)] == c[x(j + 2)]) break; e.idx = j;
            int al = c[x(j)], mu = c[x(j + 1)], A = c[x(j + 3)], B = c[x(j + 4)];
            e.lock1 = flood(1ULL << x(j + 1), cm[mu] | cm[A]) >> x(j + 3) & 1;
            e.lock2 = flood(1ULL << x(j + 1), cm[mu] | cm[B]) >> x(j + 4) & 1;
            u64 K3 = flood(1ULL << x(j + 2), cm[al] | cm[A]); bool r3def = !(K3 >> x(j) & 1);
            u64 K2 = flood(1ULL << x(j), cm[al] | cm[B]); bool r2def = !(K2 >> x(j + 2) & 1);
            if (r3def != (bool)e.lock2) bad_r3def++;
            if (r2def != (bool)e.lock1) bad_r2def++;
            if (e.lock2 && r3def) { swapcanon(c, K3, al, A, nc); e.r3 = lookup(nc); }
        }
    }
    // check R+3 images: same class, unfilled at index j+3, with lock1
    for (size_t s = 0; s < S; s++) if (st[s].r3 >= 0) { const St &t = st[st[s].r3];
        if (find(s) != find(st[s].r3)) bad_r3class++;
        if (t.filled || t.idx != (st[s].idx + 3) % 5) bad_r3idx++; else if (!t.lock1) bad_r3lock1++; }
    // per-class aggregation
    struct Cl { long long size = 0, Fn = 0, Un = 0, N0 = 0, N1 = 0, D = 0, LF = 0, npaths = 0, maxd = -1, sum1md = 0, Dcyc = 0, ncyc = 0, maxcyc = 0;
                long long Fi[5] = {0}, Uj[5] = {0}, F3L[5] = {0}, F2L[5] = {0}, Uff[5] = {0}, Ej[5] = {0}, DDj[5] = {0}; };
    std::map<long long, Cl> cls;
    auto isDL = [&](long long s) { return !st[s].filled && st[s].lock1 && st[s].lock2; };
    for (size_t s = 0; s < S; s++) { Cl &k = cls[find(s)]; const St &e = st[s]; k.size++;
        if (e.filled) { k.Fn++; k.Fi[e.idx]++; k.LF += e.m3long + e.m2long; if (e.m3long) k.F3L[e.idx]++; if (e.m2long) k.F2L[e.idx]++; continue; }
        k.Un++; k.Uj[e.idx]++; int nl = e.lock1 + e.lock2;
        if (nl == 0) { k.N0++; k.Uff[e.idx]++; } else if (nl == 1) k.N1++; else k.D++;
        if (!e.lock1 && e.lock2 && e.r3 >= 0 && !isDL(e.r3)) k.Ej[e.idx]++;
        if (nl == 2 && e.r3 >= 0 && isDL(e.r3)) k.DDj[e.idx]++; }
    // Gamma paths and cycles
    std::vector<char> vis(S, 0);
    for (size_t s = 0; s < S; s++) { if (st[s].filled || !( !st[s].lock1 && st[s].lock2)) continue;   // path start e-
        Cl &k = cls[find(s)]; long long d = 0, cur = s; vis[cur] = 1;
        while (st[cur].lock2 && st[cur].r3 >= 0) { cur = st[cur].r3; vis[cur] = 1; if (st[cur].lock2) d++; }
        k.npaths++; k.sum1md += 1 - d; if (d > k.maxd) k.maxd = d; }
    long long unvis_dl = 0;
    for (size_t s = 0; s < S; s++) if (!vis[s] && isDL(s)) {   // cycle (all DL)
        Cl &k = cls[find(s)]; long long len = 0, cur = s; while (!vis[cur]) { vis[cur] = 1; len++; if (st[cur].r3 < 0 || !isDL(st[cur].r3)) { unvis_dl++; break; } cur = st[cur].r3; }
        k.ncyc++; k.Dcyc += len; if (len > k.maxcyc) k.maxcyc = len; }
    // output
    long long id_bad = 0, perj_bad = 0, below = 0, maxexc = -(1LL << 60), maxchain = 0, maxDD = 0, maxddsum = 0, ex_size = 0, ex_F = 0, ex_chain = 0; double minfrac = 2, minfrac_long = 2;
    printf("{\"hole\": %d, \"n_states\": %zu, \"n_classes\": %zu, \"classes\": [", hole, S, cls.size());
    bool first = true; std::vector<long long> dumpcls;
    for (auto &kv : cls) { Cl &k = kv.second;
        long long lhs2 = 2 * (3 * k.Fn - k.Un), rhs2 = 2 * (2 * k.N0 + k.sum1md - k.Dcyc) + 3 * k.LF; bool idok = lhs2 == rhs2; if (!idok) id_bad++;
        long long exc[5], room[5]; long long cmax = -(1LL << 60);
        for (int j = 0; j < 5; j++) { long long Lj = k.F3L[(j + 4) % 5] + k.F2L[(j + 3) % 5] + k.F2L[(j + 1) % 5];
            room[j] = Lj + k.Uff[j] + k.Uff[(j + 3) % 5] + k.Ej[j]; exc[j] = k.DDj[j] - room[j];
            if (k.Fi[(j + 1) % 5] + k.Fi[(j + 3) % 5] + k.Fi[(j + 4) % 5] - k.Uj[j] != room[j] - k.DDj[j]) perj_bad++;
            if (exc[j] > cmax) cmax = exc[j]; if (k.DDj[j] > maxDD) maxDD = k.DDj[j]; }
        long long chain = std::max(k.maxd, k.maxcyc); double fr = (double)k.Fn / k.size;
        if (3 * k.Fn < k.Un || k.Fn == 0) { below++; dumpcls.push_back(kv.first); }
        long long ddsum = k.DDj[0] + k.DDj[1] + k.DDj[2] + k.DDj[3] + k.DDj[4]; if (ddsum > maxddsum) maxddsum = ddsum;
        if (cmax > maxexc || (cmax == maxexc && std::max(k.maxd, k.maxcyc) > ex_chain)) { maxexc = cmax; ex_size = k.size; ex_F = k.Fn; ex_chain = std::max(k.maxd, k.maxcyc); } if (chain > maxchain) maxchain = chain; if (fr < minfrac) minfrac = fr; if (chain >= 2 && fr < minfrac_long) minfrac_long = fr;
        printf("%s{\"size\": %lld, \"F\": %lld, \"U\": %lld, \"N0\": %lld, \"N1\": %lld, \"D\": %lld, \"LF\": %lld, \"paths\": %lld, \"max_d\": %lld, \"Dcyc\": %lld, \"cycles\": %lld, \"max_cycle\": %lld, \"id_ok\": %s, \"DD\": [%lld,%lld,%lld,%lld,%lld], \"room\": [%lld,%lld,%lld,%lld,%lld], \"max_excess\": %lld}",
               first ? "" : ", ", k.size, k.Fn, k.Un, k.N0, k.N1, k.D, k.LF, k.npaths, k.maxd, k.Dcyc, k.ncyc, k.maxcyc, idok ? "true" : "false",
               k.DDj[0], k.DDj[1], k.DDj[2], k.DDj[3], k.DDj[4], room[0], room[1], room[2], room[3], room[4], cmax); first = false; }
    printf("], \"summary\": {\"max_DDsum\": %lld, \"excess_class\": [%lld, %lld, %lld], \"max_excess\": %lld, \"max_chain\": %lld, \"max_DD\": %lld, \"min_frac\": %.6f, \"min_frac_chain2\": %.6f, \"below_quarter\": %lld}", maxddsum, ex_size, ex_F, ex_chain, maxexc, maxchain, maxDD, minfrac, minfrac_long > 1 ? -1.0 : minfrac_long, below);
    printf(", \"checks\": {\"identity_bad\": %lld, \"perj_bad\": %lld, \"M3_bad\": %lld, \"M2_bad\": %lld, \"R3def_bad\": %lld, \"R2def_bad\": %lld, \"R3_lock1_bad\": %lld, \"R3_idx_bad\": %lld, \"R3_class_bad\": %lld, \"open_DL_chain\": %lld}",
           id_bad, perj_bad, bad_m3, bad_m2, bad_r3def, bad_r2def, bad_r3lock1, bad_r3idx, bad_r3class, unvis_dl);
    if (argc > 4 && !dumpcls.empty()) { FILE *fo = fopen(argv[4], "w");
        fprintf(fo, "# hole %d; order (T-v vertices, original labels):", hole); for (int t = 0; t < N; t++) fprintf(fo, " %d", order[t]); fprintf(fo, "\n");
        fprintf(fo, "# one line per state of every class with 3F < U: class_root filled colours-in-order\n");
        for (size_t s = 0; s < S; s++) { long long r = find(s); if (std::find(dumpcls.begin(), dumpcls.end(), r) == dumpcls.end()) continue;
            int c[64]; unkey(ALL[s], c); fprintf(fo, "%lld %d", r, (int)st[s].filled); for (int t = 0; t < N; t++) fprintf(fo, " %d", c[t]); fprintf(fo, "\n"); }
        fclose(fo); printf(", \"dumped\": \"%s\"", argv[4]); }
    printf("}\n"); return 0;
}
