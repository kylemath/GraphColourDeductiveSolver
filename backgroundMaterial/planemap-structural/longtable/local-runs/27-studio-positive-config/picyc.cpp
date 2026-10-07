// picyc.cpp -- [exploratory] Mac Studio run 27: pi-cycles, windings, positive cycles versus configurations, and transport
// (lock-breaking exits) at every degree-5 hole. C++ port of the MacBook's Python (local-runs/22 escape.py, 23 scan.py,
// 26 lib26.py), same definitions:
//  state   = proper 4-colouring of T-v up to renaming; canonical by first occurrence along the BFS order of T-v from link[0]
//            (neighbours by ascending label), vertex 0 of that order gets colour 0;
//  link    = rotation order at the hole as listed in the input (planar-code orientation); x_t = link[t];
//  filled  = link uses 3 colours; unfilled: 4 colours, the repeat is c(x_j) = c(x_{j+2}), alpha = c(x_j), mu = c(x_{j+1}),
//            A = c(x_{j+3}), B = c(x_{j+4}), m = x_{j+1}, a = x_{j+3}, b = x_{j+4};
//  lock 1  = a in the {mu,A}-component of m; lock 2 = b in the {mu,B}-component of m; DL = both;
//  pi      = (unfilled) lock 2 ? R+3: swap the {alpha,A}-component of x_{j+2}, lambda +1
//                                   : phiB^-1: swap the {mu,B}-component of x_{j+4}, lambda -1
//            (filled, W unique at x_i, X = c(x_{i+1}), Y = c(x_{i+2}), Z the fourth colour)
//            x_{i+4} not in K = {Y,Z}-component of x_{i+2} ? phiA: swap K, lambda -1 : tau: swap the {W,X}-component of x_{i+3}, lambda -3;
//  winding of a pi-cycle = (sum of lambda)/5; Theorem W: 3F - U = -5 * sum of windings over a Kempe class (checked in --full mode);
//  move    = whole-component Kempe swap; link-free = the component misses all 5 link vertices; lock-breaking (at a DL state) =
//            the component meets K1 | K2 (the two lock chains); other-pair = colour pair is not {alpha,A} or {alpha,B};
//  transport variants from positive cycle Z to negative cycles: (a) DL states, any pair; (b) DL, other pair; (c) any state;
//            (d) DL, lock-breaking; (e) DL, other pair and lock-breaking. ok = max-flow routes the whole supply; Hall ratio =
//            min over subsets S of positive cycles (same bipartite component, <= 18) of cap(N(S)) / supply(S).
//  configurations: Birkhoff diamond (RSST 0.7322) = edge ab with face-neighbours c, d, all four of degree 5, c and d not adjacent;
//            RSST 2.122 = same with {deg a, deg b} = {5,6}, deg c = deg d = 5, c and d not adjacent. Counted once per edge ab.
// Input: text, one graph per line: "name n r0;r1;...;r_{n-1}", r_v = comma-separated 0-based neighbours in rotation order.
// --full also: per class clsig [size, F, sum w, DD, N0, E2, tau] (DD = DL with DL pi-image; N0 = unfilled with neither lock;
//   E2 = unfilled runs of length exactly 2 between filled states on a pi-cycle; tau = filled with lambda -3) and f5_bad = classes where
//   sum lambda != DD - 2 N0 - E2 - 3 tau (Theorem F5 identity, NightF5Review.md).
// --jobe: only (5,5,5,5,6)/(5,5,5,6,6) holes; per hole sigC (pi-cycles joined by sigma = {alpha,mu}-swap at m from every DD-step endpoint;
//   fail = a joined group with sum w > 0) and per all-DL pi-cycle (Gamma): R-types (w0 = A: R1; w0 = B, w3 = alpha: R2; w0 = B, w3 = mu: R3; else other),
//   [type, kmask (bit i = x_{j+i} has degree >= 6), count], R3 states whose sigma image is lockless (C1-Gamma), first R3 failure.
// --jobn rows: [pos in cycle, k, lockless, y~z in {c(y),c(z)}, pm bridge of G[{v}+c(p),c(m)], p, m, y, z (original labels), #m candidates, |K_{c(p),c(m)}(p)|, |K(y)|, |K(z)|, sigma fixed point]
// --jobo rows per state x of a Gamma-cycle (pi order): [pos, type, kmask, pairmask, compmask, |swapped comp|, y~z before, y~z after the step, |K(y)|, |K(z)| after]
//   (pairmask / compmask bits: p, m, y, z have a colour in the swapped pair / lie in the swapped component; the step x -> pi x is R+3: the {alpha,A}-swap at x_{j+2})
// Usage: picyc FILE [--full] [--mirror] [--cap M] [--holes h,h,...] [--cfree] [--adj5] [--graphonly]   (default --pi: no class union-find)
// Per hole also: linkdeg (degrees of x_0..x_4 in link order), vrole (bits: 1 diamond centre, 2 diamond tip, 4 2.122 deg-5 centre, 16 2.122 tip),
// dist_config (graph distance from v to the nearest vertex of any diamond or 2.122, -1 if none). Per graph: adj55 = edges between degree-5 vertices.
// Output: JSON lines: {"kind":"graph",...} once per graph, {"kind":"hole",...} per degree-5 hole. Requires n-1 <= 64.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <string>
#include <algorithm>
#include <functional>
#include <array>
typedef uint64_t u64;
struct Key { u64 hi, lo; bool operator<(const Key&o) const { return hi < o.hi || (hi == o.hi && lo < o.lo); }
                         bool operator==(const Key&o) const { return hi == o.hi && lo == o.lo; } };
static int N; static u64 adjm[64]; static int link_[5]; static u64 linkmask, ring2mask;
static std::vector<Key> ALL; static int col[64]; static long long capStates = 80000000LL; static bool capHit = false;
static bool FULL = false, MIRROR = false, CFREE = false, ADJ5 = false, GRAPHONLY = false, JOBE = false, SIGC = false, JOBG = false, JOBH = false, JOBI = false, JOBK = false, JOBM = false, JOBN = false, JOBO = false;
static std::vector<int> VROLE; static int ADJ55;
static int dist_config(int n, const std::vector<std::vector<int>> &rot, int v);

static inline u64 flood(u64 start, u64 M) {
    u64 comp = start, front = start;
    while (front) { u64 nb = 0, f = front; while (f) { int u = __builtin_ctzll(f); f &= f - 1; nb |= adjm[u]; } nb &= M & ~comp; comp |= nb; front = nb; }
    return comp;
}
static inline Key keyof(const int *c) { Key k{0, 0}; for (int i = 0; i < N; i++) { if (i < 32) k.hi |= (u64)c[i] << (62 - 2 * i); else k.lo |= (u64)c[i] << (62 - 2 * (i - 32)); } return k; }
static inline void unkey(const Key &k, int *c) { for (int i = 0; i < N; i++) c[i] = i < 32 ? (k.hi >> (62 - 2 * i)) & 3 : (k.lo >> (62 - 2 * (i - 32))) & 3; }
static inline void masks(const int *c, u64 *cm) { cm[0] = cm[1] = cm[2] = cm[3] = 0; for (int i = 0; i < N; i++) cm[c[i]] |= 1ULL << i; }
static void rec(int i, int used) {
    if (capHit) return;
    if (i == N) { ALL.push_back(keyof(col)); if ((long long)ALL.size() > capStates) capHit = true; return; }
    u64 forb = 0; for (u64 f = adjm[i] & ((1ULL << i) - 1); f; f &= f - 1) forb |= 1ULL << col[__builtin_ctzll(f)];
    int top = used + 1 < 4 ? used + 1 : 4;
    for (int c = 0; c < top; c++) if (!(forb >> c & 1)) { col[i] = c; rec(i + 1, c + 1 > used ? c + 1 : used); }
}
// swap component K of pair (p,q) in colouring c, canonicalise into nc, return state index
static inline long long swap_index(const int *c, u64 K, int p, int q, int *nc) {
    int mp[4] = {-1, -1, -1, -1}, nx = 0;
    for (int i = 0; i < N; i++) { int x = c[i]; if (K >> i & 1) x = (x == p) ? q : p; if (mp[x] < 0) mp[x] = nx++; nc[i] = mp[x]; }
    Key nk = keyof(nc); auto it = std::lower_bound(ALL.begin(), ALL.end(), nk);
    if (it == ALL.end() || !(*it == nk)) { fprintf(stderr, "state not found\n"); exit(3); }
    return it - ALL.begin();
}
struct StateInfo { int kind; int al, A, B; u64 lock; int l1, l2; };   // kind 0 filled, 1 unfilled non-DL, 2 DL
static inline StateInfo info_of(const int *c, const u64 *cm) {
    StateInfo r{0, -1, -1, -1, 0, 0, 0}; int lc[5]; int seen = 0; for (int t = 0; t < 5; t++) { lc[t] = c[link_[t]]; seen |= 1 << lc[t]; }
    if (__builtin_popcount(seen) <= 3) return r;
    int j = 0; for (; j < 5; j++) if (lc[j] == lc[(j + 2) % 5]) break;
    int m = link_[(j + 1) % 5], a = link_[(j + 3) % 5], b = link_[(j + 4) % 5];
    int mu = lc[(j + 1) % 5]; r.al = lc[j]; r.A = lc[(j + 3) % 5]; r.B = lc[(j + 4) % 5];
    u64 K1 = flood(1ULL << m, cm[mu] | cm[r.A]); u64 K2 = flood(1ULL << m, cm[mu] | cm[r.B]);
    r.l1 = (K1 >> a & 1) ? 1 : 0; r.l2 = (K2 >> b & 1) ? 1 : 0; r.kind = (r.l1 && r.l2) ? 2 : 1; r.lock = K1 | K2; return r;
}
// pi and lambda
static inline long long pi_of(const int *c, const u64 *cm, int *nc, int &lam) {
    int lc[5]; int seen = 0; for (int t = 0; t < 5; t++) { lc[t] = c[link_[t]]; seen |= 1 << lc[t]; }
    if (__builtin_popcount(seen) == 4) {
        int j = 0; for (; j < 5; j++) if (lc[j] == lc[(j + 2) % 5]) break;
        int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5];
        int m = link_[(j + 1) % 5], b = link_[(j + 4) % 5];
        u64 K2 = flood(1ULL << m, cm[mu] | cm[B]);
        if (K2 >> b & 1) { lam = 1; u64 K = flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]); return swap_index(c, K, al, A, nc); }
        lam = -1; u64 K = flood(1ULL << b, cm[mu] | cm[B]); return swap_index(c, K, mu, B, nc);
    }
    int cnt[4] = {0, 0, 0, 0}; for (int t = 0; t < 5; t++) cnt[lc[t]]++;
    int i = 0; for (; i < 5; i++) if (cnt[lc[i]] == 1) break;
    int W = lc[i], X = lc[(i + 1) % 5], Y = lc[(i + 2) % 5]; int Z = 0; for (int z = 0; z < 4; z++) if (z != W && z != X && z != Y) Z = z;
    int x2 = link_[(i + 2) % 5], x4 = link_[(i + 4) % 5];
    u64 K = flood(1ULL << x2, cm[Y] | cm[Z]);
    if (!(K >> x4 & 1)) { lam = -1; return swap_index(c, K, Y, Z, nc); }
    lam = -3; u64 K2 = flood(1ULL << link_[(i + 3) % 5], cm[W] | cm[X]); return swap_index(c, K2, W, X, nc);
}
// ---------- max flow / Hall on small bipartite graphs
struct Flow { bool ok; long long flow, supply, capreach; int nneg; double hall; std::vector<int> hallW; long long hallcap, hallsup; bool hallnone; };
static Flow flow_report(const std::vector<int> &pos, const std::map<int, long long> &W, const std::map<int, std::set<int>> &edges) {
    std::vector<int> sinks; { std::set<int> s; for (int z : pos) { auto it = edges.find(z); if (it != edges.end()) for (int n : it->second) s.insert(n); } sinks.assign(s.begin(), s.end()); }
    int P = pos.size(), Q = sinks.size(); std::map<int, int> sid; for (int i = 0; i < Q; i++) sid[sinks[i]] = i;
    // nodes: 0 = S, 1..P positives, P+1..P+Q sinks, P+Q+1 = T
    int V = P + Q + 2, T = V - 1; std::vector<std::vector<long long>> cap(V, std::vector<long long>(V, 0));
    long long supply = 0, capreach = 0;
    for (int i = 0; i < P; i++) { cap[0][1 + i] = W.at(pos[i]); supply += W.at(pos[i]); auto it = edges.find(pos[i]); if (it != edges.end()) for (int n : it->second) cap[1 + i][P + 1 + sid[n]] = 1000000000LL; }
    for (int j = 0; j < Q; j++) { cap[P + 1 + j][T] = -W.at(sinks[j]); capreach += -W.at(sinks[j]); }
    long long flow = 0;
    while (true) {
        std::vector<int> par(V, -1); par[0] = 0; std::vector<int> q{0};
        for (size_t h = 0; h < q.size() && par[T] < 0; h++) { int u = q[h]; for (int v = 0; v < V; v++) if (par[v] < 0 && cap[u][v] > 0) { par[v] = u; q.push_back(v); } }
        if (par[T] < 0) break;
        long long b = 1000000000LL; for (int v = T; v != 0; v = par[v]) b = std::min(b, cap[par[v]][v]);
        for (int v = T; v != 0; v = par[v]) { cap[par[v]][v] -= b; cap[v][par[v]] += b; }
        flow += b;
    }
    Flow r; r.ok = (flow == supply); r.flow = flow; r.supply = supply; r.capreach = capreach; r.nneg = Q; r.hall = 1e18; r.hallnone = true; r.hallcap = r.hallsup = 0;
    if (P <= 18) {
        r.hallnone = false;
        for (unsigned S = 1; S < (1u << P); S++) {
            std::set<int> Nn; long long s = 0; for (int i = 0; i < P; i++) if (S >> i & 1) { s += W.at(pos[i]); auto it = edges.find(pos[i]); if (it != edges.end()) Nn.insert(it->second.begin(), it->second.end()); }
            long long c = 0; for (int n : Nn) c += -W.at(n);
            double ratio = (double)c / (double)s;
            if (ratio < r.hall) { r.hall = ratio; r.hallW.clear(); for (int i = 0; i < P; i++) if (S >> i & 1) r.hallW.push_back(W.at(pos[i])); std::sort(r.hallW.begin(), r.hallW.end()); r.hallcap = c; r.hallsup = s; }
        }
    }
    return r;
}
static std::string flow_json(const Flow &f) {
    char buf[512]; std::string s = "{\"ok\": "; s += f.ok ? "true" : "false";
    snprintf(buf, sizeof buf, ", \"flow\": %lld, \"supply\": %lld, \"capreach\": %lld, \"nneg_reach\": %d", f.flow, f.supply, f.capreach, f.nneg); s += buf;
    if (f.hallnone) s += ", \"hall_ratio\": null, \"hall_set\": null";
    else { snprintf(buf, sizeof buf, ", \"hall_ratio\": %.4f, \"hall_set\": {\"W\": [", f.hall); s += buf; for (size_t i = 0; i < f.hallW.size(); i++) { snprintf(buf, sizeof buf, "%s%d", i ? ", " : "", f.hallW[i]); s += buf; }
           snprintf(buf, sizeof buf, "], \"cap\": %lld, \"supply\": %lld}", f.hallcap, f.hallsup); s += buf; }
    return s + "}";
}
// ---------- one hole
struct Exit { long long any = 0, dl = 0, alphaAB = 0, other = 0, lb = 0, nonlb = 0, other_lb = 0; };
static void analyse_hole(const std::string &name, int n, const std::vector<std::vector<int>> &rot, int hole) {
    std::vector<std::set<int>> adj(n); for (int v = 0; v < n; v++) for (int w : rot[v]) if (v != hole && w != hole) adj[v].insert(w);
    const std::vector<int> &L = rot[hole];
    std::string jpat;
    if (JOBE || SIGC || JOBG || JOBH) {   // JOBE: only (5,5,5,5,6) and (5,5,5,6,6) holes; SIGC: every hole (cyclic, up to reflection, degrees capped at 8)
        int d[5]; for (int t = 0; t < 5; t++) d[t] = std::min((int)rot[L[t]].size(), 8);
        std::vector<int> best; for (int rf = 0; rf < 2; rf++) for (int r = 0; r < 5; r++) { std::vector<int> v(5); for (int t = 0; t < 5; t++) v[t] = rf ? d[(r - t + 10) % 5] : d[(r + t) % 5]; if (best.empty() || v < best) best = v; }
        if (JOBI && !(best == std::vector<int>{5, 5, 5, 5, 6} || best == std::vector<int>{5, 5, 5, 6, 6})) return;
        if (SIGC || JOBG || JOBH) { for (int t = 0; t < 5; t++) { if (t) jpat += ","; jpat += best[t] >= 8 ? std::string("8+") : std::to_string(best[t]); } }
        else if (best == std::vector<int>{5, 5, 5, 5, 6}) jpat = "5,5,5,5,6"; else if (best == std::vector<int>{5, 5, 5, 6, 6}) jpat = "5,5,5,6,6"; else return;
    }
    std::vector<int> order{L[0]}, idx(n, -1); idx[L[0]] = 0;
    for (size_t h = 0; h < order.size(); h++) for (int w : adj[order[h]]) if (idx[w] < 0) { idx[w] = order.size(); order.push_back(w); }
    N = order.size(); if (N > 64 || N != n - 1) { printf("{\"kind\": \"hole\", \"name\": \"%s\", \"hole\": %d, \"error\": \"N=%d unsupported\"}\n", name.c_str(), hole, N); return; }
    for (int i = 0; i < N; i++) { adjm[i] = 0; for (int w : adj[order[i]]) adjm[i] |= 1ULL << idx[w]; }
    linkmask = 0; for (int t = 0; t < 5; t++) { link_[t] = idx[L[t]]; linkmask |= 1ULL << link_[t]; }
    ring2mask = 0; for (int t = 0; t < 5; t++) ring2mask |= adjm[link_[t]]; ring2mask &= ~linkmask;
    ALL.clear(); ALL.shrink_to_fit(); capHit = false; col[0] = 0; rec(1, 1);
    if (capHit) { printf("{\"kind\": \"hole\", \"name\": \"%s\", \"hole\": %d, \"inconclusive\": \"more than %lld states\"}\n", name.c_str(), hole, capStates); fflush(stdout); return; }
    for (size_t i = 1; i < ALL.size(); i++) if (!(ALL[i - 1] < ALL[i])) { fprintf(stderr, "not sorted\n"); exit(3); }
    long long S = ALL.size();
    std::vector<int32_t> pi(S); std::vector<int8_t> lam(S), kind(S), nolock(S, 0); std::vector<int32_t> cyc(S, -1);
    long long F = 0, nDL = 0;
    { int c[64], nc[64]; u64 cm[4];
      for (long long k = 0; k < S; k++) { unkey(ALL[k], c); masks(c, cm); int l; pi[k] = (int32_t)pi_of(c, cm, nc, l); lam[k] = (int8_t)l;
          StateInfo si = info_of(c, cm); kind[k] = (int8_t)si.kind; nolock[k] = (si.kind == 1 && !si.l1 && !si.l2); if (si.kind == 0) F++; if (si.kind == 2) nDL++; } }
    // permutation check and cycles
    { std::vector<char> hit(S, 0); for (long long k = 0; k < S; k++) { if (hit[pi[k]]) { fprintf(stderr, "pi not injective\n"); exit(3); } hit[pi[k]] = 1; } }
    std::vector<std::vector<int32_t>> cycles; std::vector<long long> wind;
    for (long long k = 0; k < S; k++) { if (cyc[k] >= 0) continue; std::vector<int32_t> z; long long x = k, sl = 0; int id = cycles.size();
        while (cyc[x] < 0) { cyc[x] = id; z.push_back((int32_t)x); sl += lam[x]; x = pi[x]; }
        if (x != k) { fprintf(stderr, "pi cycle closure failed\n"); exit(3); }
        if (sl % 5 != 0) { fprintf(stderr, "sum lambda not divisible by 5\n"); exit(3); }
        cycles.push_back(z); wind.push_back(sl / 5); }
    std::map<std::pair<long long, long long>, long long> hist; for (size_t i = 0; i < cycles.size(); i++) hist[{wind[i], (long long)cycles[i].size()}]++;
    std::vector<int> pos; for (size_t i = 0; i < cycles.size(); i++) if (wind[i] > 0) pos.push_back(i);
    // classes (full mode)
    std::vector<int32_t> par; long long nclasses = 0; std::map<int, int> cls_of_cycle;
    std::function<int(int)> find = [&](int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; };
    if (FULL) {
        par.resize(S); for (long long i = 0; i < S; i++) par[i] = i;
        int c[64], nc[64]; u64 cm[4];
        for (long long i = 0; i < S; i++) { unkey(ALL[i], c); masks(c, cm);
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; long long j = swap_index(c, K, p, q, nc); int a = find(i), b = find(j); if (a != b) par[a] = b; } } }
        std::set<int> roots; for (long long i = 0; i < S; i++) roots.insert(find(i)); nclasses = roots.size();
    }
    std::string clsig; long long cls_bad = 0, cyc_split = 0, f5_bad = 0;
    if (FULL) {   // per-class check: every pi-cycle inside one class; 3F - U = -5 * (sum of windings of the class's cycles)
        std::vector<int32_t> pinv(S); for (long long k = 0; k < S; k++) pinv[pi[k]] = (int32_t)k;
        std::map<int, std::array<long long, 3>> cs;   // root -> size, F, sum lambda
        std::map<int, std::array<long long, 4>> f5;   // root -> DD, N0, E2, tau   (Theorem F5 identity: sum lambda = DD - 2 N0 - E2 - 3 tau)
        for (long long k = 0; k < S; k++) { int r = find(k); auto &e = cs[r]; e[0]++; if (kind[k] == 0) e[1]++; e[2] += lam[k];
            auto &g = f5[r];
            if (kind[k] == 2 && kind[pi[k]] == 2) g[0]++;
            if (nolock[k]) g[1]++;
            if (kind[k] != 0 && kind[pinv[k]] == 0 && kind[pi[k]] != 0 && kind[pi[pi[k]]] == 0) g[2]++;
            if (kind[k] == 0 && lam[k] == -3) g[3]++; }
        for (auto &kv : f5) { auto &g = kv.second; if (cs[kv.first][2] != g[0] - 2 * g[1] - g[2] - 3 * g[3]) f5_bad++; }
        for (auto &z : cycles) { int r = find(z[0]); for (int32_t x : z) if (find(x) != r) { cyc_split++; break; } }
        std::vector<std::array<long long, 7>> sig;
        for (auto &kv : cs) { long long sz = kv.second[0], f = kv.second[1], sl = kv.second[2]; if (sl % 5 != 0 || 3 * f - (sz - f) != -sl) cls_bad++;
            auto &g = f5[kv.first]; sig.push_back({sz, f, sl / 5, g[0], g[1], g[2], g[3]}); }
        std::sort(sig.begin(), sig.end()); char b3[160];
        for (auto &t : sig) { snprintf(b3, sizeof b3, "%s[%lld, %lld, %lld, %lld, %lld, %lld, %lld]", clsig.empty() ? "" : ", ", t[0], t[1], t[2], t[3], t[4], t[5], t[6]); clsig += b3; }
    }
    // exits from positive cycles
    std::map<int, std::map<int, Exit>> exits;   // pos cycle -> target cycle -> counters
    struct LB { long long exits_DL = 0, exits_lb = 0, to_neg = 0, to_neg_lb = 0, nDL = 0, exits_any = 0, to_neg_any = 0; }; std::map<int, LB> lbs;
    { int c[64], nc[64]; u64 cm[4];
      for (int ci : pos) { LB &lb = lbs[ci];
        for (int32_t x : cycles[ci]) { unkey(ALL[x], c); masks(c, cm); StateInfo si = info_of(c, cm); bool dl = si.kind == 2; if (dl) lb.nDL++;
            for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; if (K & linkmask) continue;
                    long long t = swap_index(c, K, p, q, nc); if (t == x) continue; int cj = cyc[t]; if (cj == ci) continue;
                    Exit &e = exits[ci][cj]; e.any++; lb.exits_any++; if (wind[cj] < 0) lb.to_neg_any++;
                    if (dl) { e.dl++; lb.exits_DL++; bool ab = (p == si.al && (q == si.A || q == si.B)) || (q == si.al && (p == si.A || p == si.B));
                        if (ab) e.alphaAB++; else e.other++; bool isl = (K & si.lock) != 0; if (isl) { e.lb++; lb.exits_lb++; } else e.nonlb++;
                        if (!ab && isl) e.other_lb++; if (wind[cj] < 0) { lb.to_neg++; if (isl) lb.to_neg_lb++; } } } } } } }
    // transport per bipartite component of positive cycles (sinks = negative cycles)
    std::map<int, long long> Wm; for (size_t i = 0; i < cycles.size(); i++) Wm[i] = wind[i];
    auto edge_set = [&](int flag) { std::map<int, std::set<int>> E; for (int z : pos) { std::set<int> s; for (auto &kv : exits[z]) { const Exit &e = kv.second; if (wind[kv.first] >= 0) continue;
        long long v = flag == 0 ? e.dl : flag == 1 ? e.other : flag == 2 ? e.any : flag == 3 ? e.lb : e.other_lb; if (v) s.insert(kv.first); } E[z] = s; } return E; };
    std::map<int, std::set<int>> Eall = edge_set(2);
    // components of positive cycles via shared sinks (any-state edges give the coarsest grouping)
    std::map<int, int> comp; { std::map<int, std::vector<int>> by_sink; for (int z : pos) for (int s : Eall[z]) by_sink[s].push_back(z);
        std::map<int, int> up; for (int z : pos) up[z] = z; std::function<int(int)> f2 = [&](int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
        for (auto &kv : by_sink) for (size_t i = 1; i < kv.second.size(); i++) { int a = f2(kv.second[0]), b = f2(kv.second[i]); if (a != b) up[a] = b; }
        for (int z : pos) comp[z] = f2(z); }
    std::string jobe;
    if (JOBE || SIGC || JOBG || JOBH) {
        int widx[5]; for (int t = 0; t < 5; t++) { int a = L[t], b = L[(t + 1) % 5]; const std::vector<int> &ra = rot[a]; int da = ra.size(), p = std::find(ra.begin(), ra.end(), b) - ra.begin();
            int c1 = ra[(p + 1) % da], c2 = ra[(p + da - 1) % da]; widx[t] = idx[c1 == hole ? c2 : c1]; }
        int hi[5]; for (int t = 0; t < 5; t++) hi[t] = rot[L[t]].size() >= 6;
        std::vector<int32_t> pinv(S); for (long long k = 0; k < S; k++) pinv[pi[k]] = (int32_t)k;
        int c[64], nc[64]; u64 cm[4];
        auto frame = [&](long long k, int &j, int &type, int &kmask, long long &sig, int &sig_l1, int &sig_l2, int &sig_kind) {
            unkey(ALL[k], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]];
            for (j = 0; j < 5; j++) if (lc[j] == lc[(j + 2) % 5]) break;
            int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5];
            int w0 = c[widx[j]], w3 = c[widx[(j + 3) % 5]];
            type = (w0 == A) ? 1 : (w0 == B && w3 == al) ? 2 : (w0 == B && w3 == mu) ? 3 : 0;
            kmask = 0; for (int i = 0; i < 5; i++) if (hi[(j + i) % 5]) kmask |= 1 << i;
            u64 K = flood(1ULL << link_[(j + 1) % 5], cm[al] | cm[mu]); sig = swap_index(c, K, al, mu, nc);
            u64 cm2[4]; masks(nc, cm2); StateInfo si = info_of(nc, cm2); sig_l1 = si.l1; sig_l2 = si.l2; sig_kind = si.kind; };
        // sigma-joined groups over DD-step endpoints
        std::vector<int> up(cycles.size()); for (size_t i = 0; i < up.size(); i++) up[i] = i;
        std::function<int(int)> fu = [&](int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
        long long nedges = 0, nendpoints = 0;
        for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; bool ep = kind[pi[k]] == 2 || kind[pinv[k]] == 2; if (!ep) continue;
            int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); nendpoints++; int a = fu(cyc[k]), b = fu(cyc[sg]); if (cyc[k] != cyc[sg]) nedges++; if (a != b) up[a] = b; }
        std::map<int, std::pair<long long, int>> comp_sum; for (size_t i = 0; i < cycles.size(); i++) { auto &e = comp_sum[fu(i)]; e.first += wind[i]; e.second++; }
        long long nfail = 0, maxsum = -1000000000LL; int maxsize = 0; std::string firstfail;
        for (auto &kv : comp_sum) { maxsize = std::max(maxsize, kv.second.second); maxsum = std::max(maxsum, kv.second.first);
            if (kv.second.first > 0) { nfail++; if (firstfail.empty()) { char b4[128]; snprintf(b4, sizeof b4, "{\"sumw\": %lld, \"ncycles\": %d}", kv.second.first, kv.second.second); firstfail = b4; } } }
        char b5[512]; snprintf(b5, sizeof b5, ", \"pattern\": \"%s\", \"sigC\": {\"ncomp\": %zu, \"cross_edges\": %lld, \"endpoints\": %lld, \"max_ncycles\": %d, \"max_sumw\": %lld, \"fail\": %lld, \"first_fail\": %s}", jpat.c_str(), comp_sum.size(), nedges, nendpoints, maxsize, maxsum, nfail, firstfail.empty() ? "null" : firstfail.c_str());
        jobe += b5;
        if (JOBH) {   // Job H: sigma' = all link-free lock-breaking swaps (result not DL) from DD-step endpoints; H2 adds sigma at R3 endpoints
            std::vector<int> u1(cycles.size()), u2(cycles.size()); for (size_t i = 0; i < u1.size(); i++) u1[i] = u2[i] = i;
            auto fx = [](std::vector<int> &up, int x) { while (up[x] != x) { up[x] = up[up[x]]; x = up[x]; } return x; };
            long long nend = 0, nend_cross = 0;
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; if (!(kind[pi[k]] == 2 || kind[pinv[k]] == 2)) continue; nend++;
                unkey(ALL[k], c); masks(c, cm); bool cross = false;
                for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { u64 M = cm[p] | cm[q];
                    while (M) { u64 K = flood(M & -M, cm[p] | cm[q]); M &= ~K; if (K & linkmask) continue; long long t = swap_index(c, K, p, q, nc);
                        if (t == k || kind[t] == 2) continue; if (cyc[t] != cyc[k]) cross = true;
                        int a = fx(u1, cyc[k]), b = fx(u1, cyc[t]); if (a != b) u1[a] = b; a = fx(u2, cyc[k]); b = fx(u2, cyc[t]); if (a != b) u2[a] = b; } }
                if (cross) nend_cross++;
                int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd);
                if (ty == 3) { int a = fx(u2, cyc[k]), b = fx(u2, cyc[sg]); if (a != b) u2[a] = b; } }
            for (int v = 0; v < 2; v++) { std::vector<int> &up = v ? u2 : u1; std::map<int, std::pair<long long, int>> cs2;
                for (size_t i = 0; i < cycles.size(); i++) { auto &e = cs2[fx(up, i)]; e.first += wind[i]; e.second++; }
                long long nf = 0, mx = -1000000000LL; int ms = 0; std::string ff;
                for (auto &kv : cs2) { ms = std::max(ms, kv.second.second); mx = std::max(mx, kv.second.first); if (kv.second.first > 0) { nf++; if (ff.empty()) { char b4[96]; snprintf(b4, sizeof b4, "{\"sumw\": %lld, \"ncycles\": %d}", kv.second.first, kv.second.second); ff = b4; } } }
                char b5[400]; snprintf(b5, sizeof b5, ", \"%s\": {\"ncomp\": %zu, \"endpoints\": %lld, \"endpoints_with_cross_sigmap\": %lld, \"max_ncycles\": %d, \"max_sumw\": %lld, \"fail\": %lld, \"first_fail\": %s}",
                    v ? "H2_sigmap_plus_sigmaR3" : "H1_sigmap", cs2.size(), nend, nend_cross, ms, mx, nf, ff.empty() ? "null" : ff.c_str()); jobe += b5; } }
        if (JOBO) {   // Job O: per pi-step of Gamma-cycles at (5,5,5,5,6): p = degree-6 link vertex, y = w_{t-1}, z = w_t, m = p's third outer neighbour
            int t6 = -1, nhi = 0; for (int t = 0; t < 5; t++) if (rot[L[t]].size() >= 6) { t6 = t; nhi++; }
            if (nhi == 1) {
                int p = link_[t6], y = widx[(t6 + 4) % 5], z = widx[t6]; int mv = -1; for (int w : rot[L[t6]]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(t6 + 1) % 5] || wi == link_[(t6 + 4) % 5] || wi == y || wi == z) continue; mv = w; }
                int m = idx[mv]; int V4[4] = {p, m, y, z};
                std::string oo = ", \"jobo\": {\"pmyz\": ["; char b0[64]; snprintf(b0, sizeof b0, "%d, %d, %d, %d], \"cycles\": [", order[p], mv, order[y], order[z]); oo += b0; bool f1 = true;
                for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                    oo += f1 ? "[" : ", ["; f1 = false; bool f2 = true; int pos = 0;
                    for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd);
                        unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]]; int al = lc[j], A = lc[(j + 3) % 5];
                        u64 K = flood(1ULL << link_[(j + 2) % 5], cm[al] | cm[A]); int pairmask = 0, compmask = 0;
                        for (int i = 0; i < 4; i++) { if (c[V4[i]] == al || c[V4[i]] == A) pairmask |= 1 << i; if (K >> V4[i] & 1) compmask |= 1 << i; }
                        int csz = __builtin_popcountll(K);
                        int cc[64]; unkey(ALL[pi[x]], cc); u64 cm2[4]; masks(cc, cm2); u64 Ky = flood(1ULL << y, cm2[cc[y]] | cm2[cc[z]]); bool yz = Ky >> z & 1;
                        int sy = __builtin_popcountll(Ky), sz = __builtin_popcountll(flood(1ULL << z, cm2[cc[y]] | cm2[cc[z]]));
                        u64 K0 = flood(1ULL << y, cm[c[y]] | cm[c[z]]); bool yz0 = K0 >> z & 1;
                        char b[160]; snprintf(b, sizeof b, "%s[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d]", f2 ? "" : ", ", pos, ty, km, pairmask, compmask, csz, yz0 ? 1 : 0, yz ? 1 : 0, sy, sz); oo += b; f2 = false; pos++; }
                    oo += "]"; }
                oo += "]}"; jobe += oo; } }
        if (JOBN) {   // Job N (NightF6Flow 2.1): at R3@k in {3,4} on Gamma-cycles: p = x_{j+k}, y = w_{j+k-1}, z = w_{j+k}, m = p's third outer neighbour
            std::string nn = ", \"jobn\": ["; bool f1 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                nn += f1 ? "[" : ", ["; f1 = false; bool f2 = true; int pos = 0;
                for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); pos++;
                    if (ty != 3 || !(km == 8 || km == 16)) continue; int k = km == 8 ? 3 : 4;
                    int p = link_[(j + k) % 5], y = widx[(j + k + 4) % 5], z = widx[(j + k) % 5];
                    int pv = order[p]; int mv = -1, cntm = 0;
                    for (int w : rot[pv]) { if (w == hole) continue; int wi = idx[w]; if (wi == link_[(j + k + 1) % 5] || wi == link_[(j + k + 4) % 5] || wi == y || wi == z) continue; mv = w; cntm++; }
                    int m = idx[mv];
                    unkey(ALL[x], c); masks(c, cm);
                    bool lockless = (kd == 1 && !l1 && !l2);
                    u64 Kyz = flood(1ULL << y, cm[c[y]] | cm[c[z]]); bool yz = Kyz >> z & 1;
                    // bridge test of edge pm in G[H], H = {v} + vertices coloured c(p) or c(m)
                    u64 M = cm[c[p]] | cm[c[m]]; u64 seen = 1ULL << p; bool vseen = false; std::vector<int> st{p}; bool reached = false;
                    while (!st.empty() && !reached) { int u = st.back(); st.pop_back(); u64 nb = adjm[u] & M & ~seen; if (u == p) nb &= ~(1ULL << m);
                        if ((linkmask >> u & 1) && !vseen) { vseen = true; for (int t = 0; t < 5; t++) { int lv = link_[t]; if ((M >> lv & 1) && !(seen >> lv & 1) && !(u == p && lv == m)) { seen |= 1ULL << lv; st.push_back(lv); if (lv == m) reached = true; } } }
                        while (nb) { int w = __builtin_ctzll(nb); nb &= nb - 1; seen |= 1ULL << w; st.push_back(w); if (w == m) reached = true; } }
                    bool bridge = !reached;
                    int cp = __builtin_popcountll(flood(1ULL << p, M)), cy = __builtin_popcountll(Kyz), cz = __builtin_popcountll(flood(1ULL << z, cm[c[y]] | cm[c[z]]));
                    char b[256]; snprintf(b, sizeof b, "%s[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d]", f2 ? "" : ", ", pos - 1, k, lockless ? 1 : 0, yz ? 1 : 0, bridge ? 1 : 0, pv, mv, order[y], order[z], cntm, cp, cy, cz, (int)(sg == x));
                    nn += b; f2 = false; }
                nn += "]"; }
            nn += "]"; jobe += nn; }
        if (JOBM) {   // Job M: Gamma-cycles as ordered state sequences [type, kmask, exit, f]; exit L lockless, 1 Lock1-only, 2 Lock2-only, X fixed point, D other DL, F filled
            std::string mm = ", \"jobm\": ["; bool f1 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
                mm += f1 ? "[" : ", ["; f1 = false; bool f2 = true;
                for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); char ex = '-'; long long f = -1;
                    if (ty == 3) { if (kd == 1 && !l1 && !l2) { ex = 'L'; long long y = pi[sg]; f = 0; while (kind[y] == 0) { f++; y = pi[y]; } }
                        else if (kd == 1) ex = l1 ? '1' : '2'; else if (kd == 2) ex = (sg == x) ? 'X' : 'D'; else ex = 'F'; }
                    char b[48]; snprintf(b, sizeof b, "%s[%d, %d, \"%c\", %lld]", f2 ? "" : ", ", ty, km, ex, f); mm += b; f2 = false; }
                mm += "]"; }
            mm += "]"; jobe += mm; }
        if (JOBK) {   // Job K: Lemma R per target cycle; sigma-chain from positive cycles without lockless exits
            std::map<int, std::pair<long long, long long>> hit;   // target cycle -> (#hits, sum of excursion contributions 1 - 3f)
            std::vector<std::set<int>> sadj(cycles.size());
            for (long long k = 0; k < S; k++) { if (kind[k] != 2) continue; if (!(kind[pi[k]] == 2 || kind[pinv[k]] == 2)) continue;
                int j, ty, km, l1, l2, kd; long long sg; frame(k, j, ty, km, sg, l1, l2, kd); if (cyc[sg] != cyc[k]) { sadj[cyc[k]].insert(cyc[sg]); sadj[cyc[sg]].insert(cyc[k]); } }
            std::string kk = ", \"jobk_pos\": ["; bool fk2 = true;
            for (size_t ci = 0; ci < cycles.size(); ci++) { if (wind[ci] <= 0) continue; long long a = 0; bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) all = false;
                for (int32_t x : cycles[ci]) { if (kind[x] != 2) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (ty != 3) continue;
                    if (kd == 1 && !l1 && !l2) { a++; long long y = pi[sg], f = 0; while (kind[y] == 0) { f++; y = pi[y]; } auto &h = hit[cyc[sg]]; h.first++; h.second += 1 - 3 * f; } }
                // BFS over sigma-adjacency to the nearest cycle with w < 0
                std::map<int, int> dist; std::vector<int> q{(int)ci}; dist[ci] = 0; int found = -1, fw = 0; long long gsum = 0;
                for (size_t h = 0; h < q.size(); h++) { int z = q[h]; gsum += wind[z]; if (found < 0 && wind[z] < 0) { found = dist[z]; fw = wind[z]; } for (int y : sadj[z]) if (!dist.count(y)) { dist[y] = dist[z] + 1; q.push_back(y); } }
                char b6[300]; snprintf(b6, sizeof b6, "%s{\"gamma\": %s, \"L\": %zu, \"w\": %lld, \"a\": %lld, \"sigma_chain_to_negative\": %d, \"first_negative_w\": %d, \"group_ncycles\": %zu, \"group_sumw\": %lld}",
                    fk2 ? "" : ", ", all ? "true" : "false", cycles[ci].size(), wind[ci], a, found, fw, q.size(), gsum); kk += b6; fk2 = false; }
            kk += "], \"lemmaR\": ["; bool f3 = true; long long rbad = 0;
            for (auto &kv : hit) { long long rem = 5 * wind[kv.first] - kv.second.second; if (rem > 0) rbad++;
                char b7[200]; snprintf(b7, sizeof b7, "%s[%lld, %zu, %lld, %lld, %lld]", f3 ? "" : ", ", wind[kv.first], cycles[kv.first].size(), kv.second.first, kv.second.second, rem); kk += b7; f3 = false; }
            char b8[64]; snprintf(b8, sizeof b8, "], \"lemmaR_bad\": %lld", rbad); kk += b8; jobe += kk; }
        if (JOBG) {   // Job G (NightC1Gamma section 5): per Gamma-cycle exits of R3 states
            auto excursion = [&](long long x, long long &u, long long &f) {   // x unfilled: its unfilled run length u and the following filled run length f
                long long st = x, guard = 0; while (kind[pinv[st]] != 0 && guard < S) { st = pinv[st]; guard++; } if (guard >= S) { u = cycles[cyc[x]].size(); f = 0; return; }
                u = 0; long long y = st; while (kind[y] != 0) { u++; y = pi[y]; } f = 0; while (kind[y] == 0) { f++; y = pi[y]; } };
            std::string g = ", \"jobg\": ["; bool fg = true; std::map<int, int> target_owner; long long shared_targets = 0;
            for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all && !(JOBI && wind[ci] > 0)) continue;
                long long a = 0, b = 0, d = 0, credit = 0, s1bad = 0, s1n = 0; std::map<std::string, long long> h; std::set<int> tg;
                for (int32_t x : cycles[ci]) { if (kind[x] != 2) continue; int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); if (ty != 3) continue;
                    unkey(ALL[x], c); masks(c, cm); int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[link_[t]];
                    int al = lc[j], mu = lc[(j + 1) % 5], A = lc[(j + 3) % 5], B = lc[(j + 4) % 5]; int m = link_[(j + 1) % 5];
                    bool crit3 = flood(1ULL << m, cm[mu] | cm[B]) >> widx[(j + 2) % 5] & 1, crit4 = flood(1ULL << m, cm[mu] | cm[A]) >> widx[(j + 4) % 5] & 1;
                    bool lockless = (kd == 1 && !l1 && !l2); char key[160];
                    if (km == 8 || km == 16) { s1n++; bool crit = km == 8 ? crit3 : crit4; bool other_ok = km == 8 ? (l1 && !l2) : (!l1 && l2); if (crit != lockless || (!lockless && !(kd == 1 && other_ok))) s1bad++; }
                    if (lockless) { a++; long long u, f; excursion(sg, u, f); credit += 3 * f - 1; tg.insert(cyc[sg]); snprintf(key, sizeof key, "lockless_k%d_u%lld_f%lld_wT%lld", km, u, f, wind[cyc[sg]]); h[key]++; }
                    else if (kd == 2) { d++; snprintf(key, sizeof key, "DL_k%d_fixed%d_same%d_type%d", km, sg == x ? 1 : 0, cyc[sg] == (int)ci ? 1 : 0, [&]{ int j2, t2, k2, a1, a2, a3; long long s2; frame(sg, j2, t2, k2, s2, a1, a2, a3); return t2; }()); h[key]++; }
                    else if (kd == 1) { b++; long long u, f; excursion(sg, u, f); tg.insert(cyc[sg]); snprintf(key, sizeof key, "onelock_k%d_L%d%d_u%lld_f%lld_wT%lld", km, l1, l2, u, f, wind[cyc[sg]]); h[key]++; }
                    else { snprintf(key, sizeof key, "filled_k%d", km); h[key]++; } }
                for (int t : tg) { auto it = target_owner.find(t); if (it != target_owner.end() && it->second != (int)ci) shared_targets++; else target_owner[t] = ci; }
                char b1[300]; snprintf(b1, sizeof b1, "%s{\"gamma\": %s, \"L\": %zu, \"w\": %lld, \"a\": %lld, \"b\": %lld, \"d\": %lld, \"G_credit\": %lld, \"G_ok\": %s, \"s1_checked\": %lld, \"s1_bad\": %lld, \"exits\": {",
                    fg ? "" : ", ", all ? "true" : "false", cycles[ci].size(), wind[ci], a, b, d, credit, credit >= (long long)cycles[ci].size() ? "true" : "false", s1n, s1bad); g += b1; fg = false;
                bool f2 = true; for (auto &kv : h) { char b2[200]; snprintf(b2, sizeof b2, "%s\"%s\": %lld", f2 ? "" : ", ", kv.first.c_str(), kv.second); g += b2; f2 = false; }
                g += "}}"; }
            char b3[64]; snprintf(b3, sizeof b3, "], \"jobg_shared_targets\": %lld", shared_targets); g += b3;
            if (!fg) jobe += g; }
        if (JOBE) {
        // Gamma-cycles
        jobe += ", \"gamma\": [";
        bool fg = true;
        for (size_t ci = 0; ci < cycles.size(); ci++) { bool all = true; for (int32_t x : cycles[ci]) if (kind[x] != 2) { all = false; break; } if (!all) continue;
            long long ty_n[4] = {0, 0, 0, 0}; std::map<std::pair<int, int>, long long> tk; std::map<std::string, long long> fk; long long r3 = 0, r3ok = 0, r3same = 0; std::string ff;
            for (int32_t x : cycles[ci]) { int j, ty, km, l1, l2, kd; long long sg; frame(x, j, ty, km, sg, l1, l2, kd); ty_n[ty]++; tk[{ty, km}]++;
                if (ty == 3) { r3++; bool ok = (kd == 1 && !l1 && !l2); if (ok) r3ok++; if (cyc[sg] == (int)ci) r3same++;
                    if (!ok) { char kk[64]; snprintf(kk, sizeof kk, "k%d_kind%d_l1%d_l2%d_same%d_wsig%lld", km, kd, l1, l2, cyc[sg] == (int)ci ? 1 : 0, wind[cyc[sg]]); fk[kk]++; }
                    if (!ok && ff.empty()) { char b6[256]; snprintf(b6, sizeof b6, "{\"state_index\": %d, \"kmask\": %d, \"sigma_kind\": %d, \"sigma_lock1\": %d, \"sigma_lock2\": %d, \"sigma_same_cycle\": %s, \"sigma_cycle_w\": %lld}", x, km, kd, l1, l2, cyc[sg] == (int)ci ? "true" : "false", wind[cyc[sg]]); ff = b6; } } }
            char b7[512]; snprintf(b7, sizeof b7, "%s{\"L\": %zu, \"w\": %lld, \"R1\": %lld, \"R2\": %lld, \"R3\": %lld, \"other\": %lld, \"r3_sigma_lockless\": %lld, \"r3_sigma_same_cycle\": %lld, \"first_r3_fail\": %s, \"type_kmask\": [",
                fg ? "" : ", ", cycles[ci].size(), wind[ci], ty_n[1], ty_n[2], ty_n[3], ty_n[0], r3ok, r3same, ff.empty() ? "null" : ff.c_str()); jobe += b7; fg = false;
            bool f8 = true; for (auto &kv : tk) { char b8[64]; snprintf(b8, sizeof b8, "%s[%d, %d, %lld]", f8 ? "" : ", ", kv.first.first, kv.first.second, kv.second); jobe += b8; f8 = false; }
            jobe += "], \"r3_fail_kinds\": {"; bool f9 = true; for (auto &kv : fk) { char b9[128]; snprintf(b9, sizeof b9, "%s\"%s\": %lld", f9 ? "" : ", ", kv.first.c_str(), kv.second); jobe += b9; f9 = false; }
            jobe += "}}"; }
        jobe += "]";
        }
    }
    // ---- output
    std::string out = "{\"kind\": \"hole\", \"name\": \"" + name + "\""; char buf[1024];
    snprintf(buf, sizeof buf, ", \"n\": %d, \"hole\": %d, \"linkdeg\": [%zu, %zu, %zu, %zu, %zu], \"vrole\": %d, \"dist_config\": %d, \"states\": %lld, \"F\": %lld, \"U\": %lld, \"nDL\": %lld, \"ncyc\": %zu, \"npos\": %zu, \"sumw\": %lld, \"minw\": %lld, \"maxw\": %lld",
             n, hole, rot[L[0]].size(), rot[L[1]].size(), rot[L[2]].size(), rot[L[3]].size(), rot[L[4]].size(), VROLE[hole], dist_config(n, rot, hole), S, F, S - F, nDL, cycles.size(), pos.size(), [&]{ long long t = 0; for (long long w : wind) t += w; return t; }(), *std::min_element(wind.begin(), wind.end()), *std::max_element(wind.begin(), wind.end()));
    out += buf;
    if (FULL) { snprintf(buf, sizeof buf, ", \"nclasses\": %lld, \"cls_bad\": %lld, \"cyc_split\": %lld, \"f5_bad\": %lld, \"clsig\": [", nclasses, cls_bad, cyc_split, f5_bad); out += buf; out += clsig + "]"; }
    out += ", \"hist\": ["; bool first = true; for (auto &kv : hist) { snprintf(buf, sizeof buf, "%s[%lld, %lld, %lld]", first ? "" : ", ", kv.first.first, kv.first.second, kv.second); out += buf; first = false; } out += "]";
    if (!pos.empty()) {
        out += ", \"pos\": [";
        for (size_t i = 0; i < pos.size(); i++) { int z = pos[i]; LB &lb = lbs[z];
            std::map<long long, int> nbw; long long minnb = 0; for (auto &kv : exits[z]) { nbw[wind[kv.first]]++; minnb = std::min(minnb, wind[kv.first]); }
            snprintf(buf, sizeof buf, "%s{\"w\": %lld, \"L\": %zu, \"nDL\": %lld, \"exits_any\": %lld, \"exits_to_neg_any\": %lld, \"exits_DL\": %lld, \"exits_lockbreaking\": %lld, \"exits_to_neg\": %lld, \"exits_to_neg_lockbreaking\": %lld, \"exits_to_neg_nonlb\": %lld, \"minnb\": %lld, \"comp\": %d, \"nbw\": [",
                     i ? ", " : "", wind[z], cycles[z].size(), lb.nDL, lb.exits_any, lb.to_neg_any, lb.exits_DL, lb.exits_lb, lb.to_neg, lb.to_neg_lb, lb.to_neg - lb.to_neg_lb, minnb, comp[z]); out += buf;
            bool f1 = true; for (auto &kv : nbw) { snprintf(buf, sizeof buf, "%s[%lld, %d]", f1 ? "" : ", ", kv.first, kv.second); out += buf; f1 = false; }
            out += "]";
            if (FULL) { int r = find(cycles[z][0]); long long cs = 0, cf = 0, cu = 0; long long sw = 0; std::set<int> cc; // class stats (computed per positive cycle; cheap at these sizes)
                for (long long k = 0; k < S; k++) if (find(k) == r) { cs++; if (kind[k] == 0) cf++; else cu++; cc.insert(cyc[k]); }
                for (int ci : cc) sw += wind[ci];
                bool thmW = (3 * cf - cu == -5 * sw);
                if (!thmW) fprintf(stderr, "THEOREM W FAILS %s hole %d\n", name.c_str(), hole);
                snprintf(buf, sizeof buf, ", \"class\": {\"root\": %d, \"states\": %lld, \"F\": %lld, \"U\": %lld, \"ncyc\": %zu, \"sumw\": %lld, \"thmW\": %s}", r, cs, cf, cu, cc.size(), sw, thmW ? "true" : "false"); out += buf; }
            out += "}"; }
        out += "], \"transport\": [";
        std::set<int> comps; for (int z : pos) comps.insert(comp[z]); bool fc = true;
        const char *vn[5] = {"a_DL_allpairs", "b_DL_otherpair", "c_anystate", "d_DL_lockbreaking", "e_DL_otherpair_lockbreaking"};
        for (int cid : comps) { std::vector<int> P; for (int z : pos) if (comp[z] == cid) P.push_back(z);
            out += fc ? "{" : ", {"; fc = false; out += "\"posW\": ["; for (size_t i = 0; i < P.size(); i++) { snprintf(buf, sizeof buf, "%s%lld", i ? ", " : "", wind[P[i]]); out += buf; } out += "]";
            for (int v = 0; v < 5; v++) { std::map<int, std::set<int>> E = edge_set(v); Flow f = flow_report(P, Wm, E); out += std::string(", \"") + vn[v] + "\": " + flow_json(f); }
            out += "}"; }
        out += "]";
    }
    out += jobe;
    out += "}\n"; fputs(out.c_str(), stdout); fflush(stdout);
}
// per-vertex role bits: 1 diamond centre, 2 diamond tip, 4 2.122 degree-5 centre, 8 2.122 degree-6 centre, 16 2.122 tip
static void config_flags(int n, const std::vector<std::vector<int>> &rot, int &diamonds, int &c2122) {
    diamonds = c2122 = 0; ADJ55 = 0; VROLE.assign(n, 0); std::vector<std::set<int>> adj(n); for (int v = 0; v < n; v++) for (int w : rot[v]) adj[v].insert(w);
    for (int a = 0; a < n; a++) { int da = rot[a].size(); for (size_t p = 0; p < rot[a].size(); p++) { int b = rot[a][p]; if (b < a) continue; int db = rot[b].size();
        if (da == 5 && db == 5) ADJ55++;
        int c = rot[a][(p + 1) % da], d = rot[a][(p + da - 1) % da]; if (adj[c].count(d)) continue; if ((int)rot[c].size() != 5 || (int)rot[d].size() != 5) continue;
        if (da == 5 && db == 5) { diamonds++; VROLE[a] |= 1; VROLE[b] |= 1; VROLE[c] |= 2; VROLE[d] |= 2; }
        else if ((da == 5 && db == 6) || (da == 6 && db == 5)) { c2122++; VROLE[da == 5 ? a : b] |= 4; VROLE[da == 6 ? a : b] |= 8; VROLE[c] |= 16; VROLE[d] |= 16; } } }
}
static int dist_config(int n, const std::vector<std::vector<int>> &rot, int v) {
    std::vector<int> d(n, -1); d[v] = 0; std::vector<int> q{v};
    for (size_t h = 0; h < q.size(); h++) { int x = q[h]; if (VROLE[x]) return d[x]; for (int w : rot[x]) if (d[w] < 0) { d[w] = d[x] + 1; q.push_back(w); } }
    return -1;
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: picyc FILE [--full] [--mirror] [--cap M] [--holes h,h]\n"); return 2; }
    std::set<int> holesel; for (int i = 2; i < argc; i++) { std::string a = argv[i]; if (a == "--full") FULL = true; else if (a == "--mirror") MIRROR = true; else if (a == "--cfree") CFREE = true; else if (a == "--adj5") ADJ5 = true; else if (a == "--graphonly") GRAPHONLY = true; else if (a == "--jobe") JOBE = true; else if (a == "--sigc") SIGC = true; else if (a == "--jobg") JOBG = true; else if (a == "--jobh") JOBH = true; else if (a == "--jobi") { JOBI = true; JOBG = true; } else if (a == "--jobo") { JOBO = true; JOBI = true; JOBG = true; } else if (a == "--jobn") { JOBN = true; JOBI = true; JOBG = true; } else if (a == "--jobm") { JOBM = true; JOBI = true; JOBG = true; } else if (a == "--jobk") { JOBK = true; JOBI = true; JOBG = true; } else if (a == "--cap") capStates = atoll(argv[++i]);
        else if (a == "--holes") { std::string s = argv[++i]; size_t p = 0; while (p < s.size()) { size_t q = s.find(',', p); if (q == std::string::npos) q = s.size(); holesel.insert(atoi(s.substr(p, q - p).c_str())); p = q + 1; } } }
    FILE *fp = fopen(argv[1], "r"); if (!fp) { fprintf(stderr, "cannot open\n"); return 2; }
    char *line = nullptr; size_t cap = 0; ssize_t len;
    while ((len = getline(&line, &cap, fp)) > 0) {
        std::string s(line); while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back(); if (s.empty()) continue;
        size_t p1 = s.find(' '), p2 = s.find(' ', p1 + 1); std::string name = s.substr(0, p1); int n = atoi(s.substr(p1 + 1, p2 - p1 - 1).c_str());
        std::vector<std::vector<int>> rot; { std::string r = s.substr(p2 + 1); size_t p = 0; while (p <= r.size()) { size_t q = r.find(';', p); if (q == std::string::npos) q = r.size(); std::string seg = r.substr(p, q - p); std::vector<int> v; size_t a = 0;
            while (a < seg.size()) { size_t b = seg.find(',', a); if (b == std::string::npos) b = seg.size(); v.push_back(atoi(seg.substr(a, b - a).c_str())); a = b + 1; } rot.push_back(v); p = q + 1; } }
        if ((int)rot.size() != n) { fprintf(stderr, "bad line %s\n", name.c_str()); return 2; }
        if (MIRROR) for (auto &v : rot) std::reverse(v.begin(), v.end());
        int dia, c2; config_flags(n, rot, dia, c2); int d5 = 0; for (int v = 0; v < n; v++) if (rot[v].size() == 5) d5++;
        bool cf = (dia == 0 && c2 == 0); if (CFREE && !cf) continue; if (ADJ5 && ADJ55 == 0) continue;
        std::string ld; for (int v = 0; v < n; v++) if (rot[v].size() == 5) { char b2[64]; snprintf(b2, sizeof b2, "%s[%zu,%zu,%zu,%zu,%zu]", ld.empty() ? "" : ",", rot[rot[v][0]].size(), rot[rot[v][1]].size(), rot[rot[v][2]].size(), rot[rot[v][3]].size(), rot[rot[v][4]].size()); ld += b2; }
        printf("{\"kind\": \"graph\", \"name\": \"%s\", \"n\": %d, \"deg5\": %d, \"adj55\": %d, \"diamonds\": %d, \"c2122\": %d, \"cfree\": %s, \"linkdegs\": [%s]}\n", name.c_str(), n, d5, ADJ55, dia, c2, cf ? "true" : "false", ld.c_str()); fflush(stdout);
        if (GRAPHONLY) continue;
        for (int v = 0; v < n; v++) if (rot[v].size() == 5 && (holesel.empty() || holesel.count(v))) analyse_hole(name, n, rot, v);
    }
    return 0;
}
