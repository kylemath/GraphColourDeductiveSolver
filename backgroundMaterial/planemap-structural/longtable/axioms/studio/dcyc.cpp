// dcyc.cpp -- Studio Job 5 (13 Oct 2026, exploratory): directed cycles of the PM digraph D at degree-5 holes.
//
// D (Long Table, axioms/proof/R0-ATTEMPT-1.md section 1): G = Tait dual of a triangulation T at a degree-5 vertex h
// (the five triangles at h merged into v; v has degree 5 with f_t = dual of link edge x_t x_{t+1}; all other vertices
// cubic).  Vertices of D = perfect matchings of G; arc M -> M' iff M n M' = 0 and k(M') = k(M) - 2 (mod 5), where
// k(M) = index of M's v-edge.  An arc is Hamiltonian iff M u M' is a single cycle.  G has a Hamiltonian cycle through
// two NON-adjacent v-edges iff D has a Hamiltonian arc (the cycle alternates into M, M').
// Conjecture R0*: planar G with a Hamiltonian arc => D acyclic.  R0: no Hamiltonian arc inside an SCC.
//
// Arcs are generated from Q = E - M: the out-neighbours of M are exactly the perfect matchings of Q containing
// f_{k-2} (enumerated directly), looked up in a hash of all PMs.
//
// Input (stdin), one graph per line:
//   rot  mode: "name n r0;r1;...;r_{n-1}"   (census frame-NN.txt; every degree-5 vertex is a hole)
//   g5   mode: "n m a0 b0 ... f0 f1 f2 f3 f4"  (TrackU graph lines; v = common end of f0, f1), name = line number
// Output: one JSON line per hole whose D has a cycle (and per hole with #PM over the cap), then a summary line.
// Usage: dcyc rot|g5 [--pmcap N] [--all]     (--all: a JSON line for every hole)
// Build: c++ -O2 -std=c++17 -o dcyc dcyc.cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <chrono>
#include <functional>
typedef unsigned __int128 u128;
struct H128 { size_t operator()(const u128 &x) const { return (size_t)(x ^ (x >> 64)) * 0x9E3779B97F4A7C15ULL; } };
static inline bool bit(u128 x, int i) { return (x >> i) & 1; }
static inline u128 one(int i) { return ((u128)1) << i; }

struct G5 {
    int n = 0, m = 0;
    std::vector<std::pair<int, int>> E;
    int fv[5];
    std::vector<std::vector<int>> inc;
    int fidx(int e) const { for (int s = 0; s < 5; s++) if (fv[s] == e) return s; return -1; }
    int other(int e, int x) const { return E[e].first == x ? E[e].second : E[e].first; }
    void build() {
        m = E.size(); inc.assign(n, {});
        for (int i = 0; i < m; i++) { inc[E[i].first].push_back(i); inc[E[i].second].push_back(i); }
    }
    bool ok() const {
        if (m > 128 || n > 128) return false;
        if ((int)inc[0].size() != 5) return false;
        for (int x = 1; x < n; x++) if (inc[x].size() != 3) return false;
        std::set<std::pair<int, int>> s;
        for (auto e : E) { if (e.first == e.second) return false; auto k = std::minmax(e.first, e.second); if (!s.insert(k).second) return false; }
        return true;
    }
};

// all perfect matchings of the edge set `allowed`, containing every edge of `forced` (vertex-disjoint, valid)
static void pms(const G5 &g, u128 allowed, u128 forced, std::vector<u128> &out, size_t cap) {
    u128 used = 0, cur = 0;
    for (int e = 0; e < g.m; e++) if (bit(forced, e)) { used |= one(g.E[e].first) | one(g.E[e].second); cur |= one(e); }
    std::vector<int> stk;
    // recursive lambda via explicit function
    struct R {
        const G5 &g; u128 allowed; std::vector<u128> &out; size_t cap;
        void rec(u128 used, u128 cur) {
            if (out.size() > cap) return;
            int best = -1, bc = 9;
            for (int x = 0; x < g.n; x++) {
                if (bit(used, x)) continue;
                int c = 0;
                for (int e : g.inc[x]) if (bit(allowed, e) && !bit(used, g.other(e, x))) c++;
                if (c < bc) { best = x; bc = c; }
                if (c == 0) return;
                if (c == 1) break;
            }
            if (best < 0) { out.push_back(cur); return; }
            for (int e : g.inc[best]) {
                if (!bit(allowed, e)) continue;
                int y = g.other(e, best);
                if (bit(used, y)) continue;
                rec(used | one(best) | one(y), cur | one(e));
            }
        }
    } r{g, allowed, out, cap};
    r.rec(used, cur);
}

static int kof(const G5 &g, u128 M) { for (int s = 0; s < 5; s++) if (bit(M, g.fv[s])) return s; return -1; }

static bool single_cycle(const G5 &g, u128 S) {  // S a 2-factor: connected spanning?
    std::vector<int> p(g.n); for (int i = 0; i < g.n; i++) p[i] = i;
    std::function<int(int)> f = [&](int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; };
    int comps = g.n;
    for (int e = 0; e < g.m; e++) if (bit(S, e)) { int a = f(g.E[e].first), b = f(g.E[e].second); if (a != b) { p[a] = b; comps--; } }
    return comps == 1;
}

static int ncomp(const G5 &g, u128 S) {  // components of (V, S)
    std::vector<int> p(g.n); for (int i = 0; i < g.n; i++) p[i] = i;
    std::function<int(int)> f = [&](int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; };
    int comps = g.n;
    for (int e = 0; e < g.m; e++) if (bit(S, e)) { int a = f(g.E[e].first), b = f(g.E[e].second); if (a != b) { p[a] = b; comps--; } }
    return comps;
}
// DL figure-eight test exactly as ax_lib.G5.dl: Q = E - M connected; the two v-loops pair {k-1,k+1} (X, even number of
// cubic vertices) and {k+2,k-2} (Y, odd).
static bool is_dl(const G5 &g, u128 M, int k, u128 all) {
    u128 Q = all & ~M;
    if (ncomp(g, Q) != 1) return false;
    u128 seen = 0; int nloops = 0; bool okX = false, okY = false;
    for (int s = 0; s < 5; s++) {
        int f = g.fv[s]; if (bit(M, f) || bit(seen, f)) continue;
        seen |= one(f); int x = g.other(f, 0), e = f, nv = 0;
        while (x != 0) { nv++; int nx = -1; for (int h : g.inc[x]) if (bit(Q, h) && h != e) { nx = h; break; } e = nx; seen |= one(e); x = g.other(e, x); }
        int s1 = g.fidx(e); nloops++;
        int a = ((s - k) % 5 + 5) % 5, b = ((s1 - k) % 5 + 5) % 5; if (a > b) std::swap(a, b);
        if (a == 1 && b == 4) { if (nv % 2 == 0) okX = true; else return false; }
        else if (a == 2 && b == 3) { if (nv % 2 == 1) okY = true; else return false; }
        else return false;
    }
    return nloops == 2 && okX && okY;
}

// Tait dual of triangulation rot at hole h
static bool tait_dual(const std::vector<std::vector<int>> &rot, int h, G5 &g) {
    int V = rot.size();
    std::map<std::vector<int>, int> tri; std::vector<std::vector<int>> T;
    for (int u = 0; u < V; u++) for (size_t i = 0; i < rot[u].size(); i++) {
        std::vector<int> t = {u, rot[u][i], rot[u][(i + 1) % rot[u].size()]}; std::sort(t.begin(), t.end());
        if (!tri.count(t)) { tri[t] = T.size(); T.push_back(t); }
    }
    std::map<std::pair<int, int>, std::vector<int>> ef;
    for (size_t t = 0; t < T.size(); t++) { auto &f = T[t]; ef[{f[0], f[1]}].push_back(t); ef[{f[0], f[2]}].push_back(t); ef[{f[1], f[2]}].push_back(t); }
    std::vector<int> vid(T.size(), -1); int nv = 1;
    for (size_t t = 0; t < T.size(); t++) { auto &f = T[t]; if (f[0] == h || f[1] == h || f[2] == h) vid[t] = 0; else vid[t] = nv++; }
    const std::vector<int> &x = rot[h];
    g = G5(); g.n = nv; for (int s = 0; s < 5; s++) g.fv[s] = -1;
    for (auto &kv : ef) {
        int u = kv.first.first, w = kv.first.second;
        if (u == h || w == h) continue;
        if (kv.second.size() != 2) return false;
        int k = g.E.size(); g.E.push_back({vid[kv.second[0]], vid[kv.second[1]]});
        for (int t = 0; t < 5; t++) { int a = x[t], b = x[(t + 1) % 5]; if ((a == u && b == w) || (a == w && b == u)) g.fv[t] = k; }
    }
    for (int s = 0; s < 5; s++) if (g.fv[s] < 0) return false;
    g.build();
    return g.ok();
}

struct Res { size_t P = 0, arcs = 0, ham = 0; bool capped = false; std::vector<std::vector<int>> sccs; std::vector<int> sccArcs, sccHam, sccGirth; std::vector<std::vector<int>> sccKs; std::vector<std::string> sccQ; int qcycles = 0, qham = 0; };

static Res analyse(const G5 &g, size_t cap) {
    Res R;
    std::vector<u128> P; pms(g, ~(u128)0 >> (128 - g.m), 0, P, cap);
    if (g.m == 128) {}  // shift above handles m <= 127; m = 128 not reached for degree 5 + cubic (m = (3n+2)/2)
    if (P.size() > cap) { R.capped = true; R.P = P.size(); return R; }
    R.P = P.size();
    std::unordered_map<u128, int, H128> idx; idx.reserve(P.size() * 2);
    for (size_t i = 0; i < P.size(); i++) idx[P[i]] = i;
    std::vector<std::vector<int>> adj(P.size());
    u128 all = ~(u128)0 >> (128 - g.m);
    std::vector<int> K(P.size());
    for (size_t i = 0; i < P.size(); i++) K[i] = kof(g, P[i]);
    std::vector<std::pair<int, int>> hamArcs;
    for (size_t i = 0; i < P.size(); i++) {
        int k2 = ((K[i] - 2) % 5 + 5) % 5;
        std::vector<u128> out; pms(g, all & ~P[i], one(g.fv[k2]), out, 1u << 20);
        for (u128 N : out) {
            auto it = idx.find(N); if (it == idx.end()) { fprintf(stderr, "PM lookup failed\n"); exit(2); }
            adj[i].push_back(it->second); R.arcs++;
            if (single_cycle(g, P[i] | N)) { R.ham++; hamArcs.push_back({(int)i, it->second}); }
        }
    }
    // Tarjan (iterative)
    int N = P.size(); std::vector<int> index(N, -1), low(N, 0), comp(N, -1); std::vector<char> on(N, 0); std::vector<int> st; int ix = 0, nc = 0;
    std::vector<std::pair<int, size_t>> cs;
    for (int s = 0; s < N; s++) {
        if (index[s] >= 0) continue;
        cs.push_back({s, 0}); index[s] = low[s] = ix++; st.push_back(s); on[s] = 1;
        while (!cs.empty()) {
            int v = cs.back().first; size_t &pi = cs.back().second;
            if (pi < adj[v].size()) {
                int w = adj[v][pi++];
                if (index[w] < 0) { index[w] = low[w] = ix++; st.push_back(w); on[w] = 1; cs.push_back({w, 0}); }
                else if (on[w]) low[v] = std::min(low[v], index[w]);
            } else {
                if (low[v] == index[v]) { while (true) { int w = st.back(); st.pop_back(); on[w] = 0; comp[w] = nc; if (w == v) break; } nc++; }
                cs.pop_back();
                if (!cs.empty()) { int u = cs.back().first; low[u] = std::min(low[u], low[v]); }
            }
        }
    }
    std::vector<std::vector<int>> members(nc);
    for (int i = 0; i < N; i++) members[comp[i]].push_back(i);
    for (int c = 0; c < nc; c++) {
        if (members[c].size() < 2) continue;  // no loops (advance -2 != 0)
        int a = 0, hcount = 0;
        for (int i : members[c]) for (int j : adj[i]) if (comp[j] == c) { a++; if (single_cycle(g, P[i] | P[j])) hcount++; }
        // girth inside the SCC by BFS from each member (SCCs are small)
        int girth = 1 << 30;
        if (members[c].size() <= 5000) for (int s : members[c]) {
            std::unordered_map<int, int> d; d[s] = 0; std::vector<int> q = {s};
            for (size_t qi = 0; qi < q.size(); qi++) { int x = q[qi]; for (int y : adj[x]) { if (comp[y] != c) continue; if (y == s) { girth = std::min(girth, d[x] + 1); continue; } if (!d.count(y)) { d[y] = d[x] + 1; q.push_back(y); } } }
        }
        std::vector<int> ks(5, 0); for (int i : members[c]) ks[K[i]]++;
        // (a) components of E - M at every state; (b) DL states and Q-cycles (directed cycles through DL states only;
        // a DL state has at most one out-arc, so these are cycles of a functional graph); (c) Hamiltonian arcs on them
        std::map<int, int> qh; std::map<int, int> nxt; std::set<int> dlset;
        for (int i : members[c]) { qh[ncomp(g, all & ~P[i])]++; if (is_dl(g, P[i], K[i], all)) dlset.insert(i); }
        for (int i : dlset) for (int j : adj[i]) if (comp[j] == c && dlset.count(j)) { nxt[i] = j; }
        std::string qs = "{\"Qcomps\": {"; bool fq = true;
        for (auto &kv : qh) { char b[48]; snprintf(b, sizeof b, "%s\"%d\": %d", fq ? "" : ", ", kv.first, kv.second); qs += b; fq = false; }
        char b2[64]; snprintf(b2, sizeof b2, "}, \"nDL\": %zu, \"Qcycles\": [", dlset.size()); qs += b2;
        std::map<int, int> state; bool fc = true;  // 0 new, 1 on stack, 2 done
        for (int s0 : dlset) {
            if (state[s0]) continue;
            std::vector<int> path; int x = s0;
            while (dlset.count(x) && state[x] == 0) { state[x] = 1; path.push_back(x); if (!nxt.count(x)) break; x = nxt[x]; }
            if (dlset.count(x) && state[x] == 1 && nxt.count(path.back())) {
                auto it = std::find(path.begin(), path.end(), x);
                std::vector<int> cy(it, path.end()); int L = cy.size(), hc = 0; std::string w;
                for (int t = 0; t < L; t++) { u128 U = P[cy[(t + L - 1) % L]] | P[cy[t]]; w += std::to_string(ncomp(g, U)); if (single_cycle(g, P[cy[t]] | P[cy[(t + 1) % L]])) hc++; }
                char b3[64]; snprintf(b3, sizeof b3, "%s{\"len\": %d, \"hamArcs\": %d, \"word\": \"", fc ? "" : ", ", L, hc); qs += b3; qs += w + "\"}"; fc = false;
                R.qcycles++; if (hc) R.qham++;
            }
            for (int y : path) state[y] = 2;
        }
        qs += "]}";
        R.sccQ.push_back(qs);
        R.sccs.push_back(members[c]); R.sccArcs.push_back(a); R.sccHam.push_back(hcount); R.sccGirth.push_back(girth); R.sccKs.push_back(ks);
    }
    return R;
}

// Hamiltonian cycles through v by v-edge pair (existence, DFS with budget) -- only for holes with a cyclic D
static std::string ham_pairs(const G5 &g, long budget) {
    std::string out = "{";
    for (int a = 0; a < 5; a++) for (int b = a + 1; b < 5; b++) {
        int s = g.other(g.fv[a], 0), t = g.other(g.fv[b], 0);
        std::vector<char> vis(g.n, 0); vis[0] = vis[s] = 1; long nodes = 0; int found = 0; bool cut = false;
        std::function<void(int, int)> dfs = [&](int x, int depth) {
            if (found || cut) return; if (++nodes > budget) { cut = true; return; }
            if (x == t) { if (depth == g.n - 1) found = 1; return; }
            for (int e : g.inc[x]) { int y = g.other(e, x); if (y == 0 || vis[y]) continue; vis[y] = 1; dfs(y, depth + 1); vis[y] = 0; }
        };
        dfs(s, 1);
        char buf[64]; snprintf(buf, sizeof buf, "%s\"%d%d\": %s", out.size() > 1 ? ", " : "", a, b, cut ? "\"?\"" : (found ? "1" : "0"));
        out += buf;
    }
    return out + "}";
}

int main(int argc, char **argv) {
    std::string mode = argc > 1 ? argv[1] : "rot";
    size_t cap = 2000000; bool all = false;
    for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "--pmcap")) cap = atol(argv[++i]); if (!strcmp(argv[i], "--all")) all = true; }
    std::string line; long holes = 0, cyc = 0, capped = 0, skipped = 0, lines = 0, hamHoles = 0, r0star = 0, r0 = 0, qcyc = 0, r0c = 0; size_t maxP = 0;
    auto t0 = std::chrono::steady_clock::now();
    auto report = [&](const std::string &name, int h, const G5 &g, const Res &R) {
        holes++; maxP = std::max(maxP, R.P);
        if (R.capped) { capped++; printf("{\"name\": \"%s\", \"hole\": %d, \"n\": %d, \"capped\": true, \"P\": %zu}\n", name.c_str(), h, g.n, R.P); fflush(stdout); return; }
        if (R.ham) hamHoles++;
        bool c = !R.sccs.empty(); if (c) cyc++;
        int hin = 0; for (int x : R.sccHam) hin += x;
        if (c && R.ham) r0star++;
        if (hin) r0++;
        if (R.qcycles) qcyc++;
        if (R.qham) r0c++;
        if (!c && !all) return;
        printf("{\"name\": \"%s\", \"hole\": %d, \"n\": %d, \"P\": %zu, \"arcs\": %zu, \"hamArcs\": %zu, \"cyclic\": %s, \"R0star_violation\": %s, \"R0_violation\": %s, \"Qcycles\": %d, \"R0c_violation\": %s, \"sccs\": [",
               name.c_str(), h, g.n, R.P, R.arcs, R.ham, c ? "true" : "false", (c && R.ham) ? "true" : "false", hin ? "true" : "false", R.qcycles, R.qham ? "true" : "false");
        for (size_t i = 0; i < R.sccs.size(); i++)
            printf("%s{\"size\": %zu, \"arcs\": %d, \"hamArcs\": %d, \"girth\": %d, \"k\": [%d,%d,%d,%d,%d], \"Q\": %s}", i ? ", " : "", R.sccs[i].size(), R.sccArcs[i], R.sccHam[i], R.sccGirth[i],
                   R.sccKs[i][0], R.sccKs[i][1], R.sccKs[i][2], R.sccKs[i][3], R.sccKs[i][4], R.sccQ[i].c_str());
        printf("]");
        if (c) printf(", \"hamPairs\": %s", ham_pairs(g, 20000000).c_str());
        printf("}\n"); fflush(stdout);
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue; lines++;
        std::istringstream ss(line);
        if (mode == "rot") {
            std::string name, rs; int V; ss >> name >> V >> rs;
            std::vector<std::vector<int>> rot; std::stringstream rr(rs); std::string tok;
            while (std::getline(rr, tok, ';')) { std::vector<int> r; std::stringstream t2(tok); std::string a; while (std::getline(t2, a, ',')) r.push_back(atoi(a.c_str())); rot.push_back(r); }
            for (int h = 0; h < (int)rot.size(); h++) {
                if (rot[h].size() != 5) continue;
                G5 g; if (!tait_dual(rot, h, g)) { skipped++; continue; }
                report(name, h, g, analyse(g, cap));
            }
        } else {
            int n, m; ss >> n >> m; G5 g; g.n = n;
            for (int i = 0; i < m; i++) { int a, b; ss >> a >> b; g.E.push_back({a, b}); }
            for (int s = 0; s < 5; s++) ss >> g.fv[s];
            auto [a, b] = g.E[g.fv[0]]; auto [c, d] = g.E[g.fv[1]]; int v = (a == c || a == d) ? a : b;
            for (auto &e : g.E) { auto sw = [&](int &x) { if (x == v) x = 0; else if (x == 0) x = v; }; sw(e.first); sw(e.second); }
            g.build(); if (!g.ok()) { skipped++; continue; }
            report("line" + std::to_string(lines - 1), -1, g, analyse(g, cap));
        }
    }
    double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    printf("{\"summary\": true, \"lines\": %ld, \"holes\": %ld, \"skipped\": %ld, \"capped\": %ld, \"cyclicD\": %ld, \"withHamArc\": %ld, \"R0star_violations\": %ld, \"R0_violations\": %ld, \"Qcycle_holes\": %ld, \"R0c_violations\": %ld, \"maxP\": %zu, \"sec\": %.1f}\n",
           lines, holes, skipped, capped, cyc, hamHoles, r0star, r0, qcyc, r0c, maxP, sec);
}
