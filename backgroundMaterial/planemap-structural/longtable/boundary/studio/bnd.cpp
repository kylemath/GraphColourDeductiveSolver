// bnd.cpp -- Studio Job 7 (13-14 Oct 2026, exploratory): boundary solvability (plan item A2) at degree-5 holes.
//
// Same game as 4square kempe_engine.HoleGame (the Python reference, boundary/ring_levels.py):
//   states  = proper 4-colourings of T - h up to renaming (enumerated once each in first-occurrence normal form along
//             a BFS order of T - h);
//   moves   = swap one Kempe chain (component of a 2-colour subgraph of T - h), excluding "webs" (the only chain of its
//             colour pair, whose swap is a renaming);
//   filled  = the link of h uses <= 3 colours.
// A move is R-restricted if its chain meets the vertex set R.  Moves are involutions (the swapped chain is again a
// chain of the result, with the same vertex set), so BFS from the filled states over R-moves gives the restricted
// distance dR of every state; dF is the unrestricted distance.
// Regions R tested at each hole (d = BFS distance from h in T, dmax = max d):
//   faceMax : each face whose minimum vertex distance is maximal ("the far face"), tested separately
//   face3   : each face with minimum vertex distance >= 3, tested separately
//   shell1  : {d = dmax};   shell2 : {d >= dmax - 1};   dist3 : {d >= 3}
// Per region: fail = number of unfilled states with no R-path to a fill (while every state has an unrestricted one);
//             maxdR = restricted distance of the deepest state; extra = max over unfilled states of dR - dF.
// faceMaxRim (Long Table, leverage question): summed over the faceMax regions of the hole, [states with dR > 0,
//   dR-lowering R-moves, of them whose chain meets the link of h, states whose every dR-lowering R-move misses the link,
//   all R-moves from unfilled states, of them meeting the link].
// Input: census lines "name n r0;r1;..." on stdin.  Output: one JSON line per hole.  n <= 64.
// --distscan adds R = {d >= r} for every r = 2..dmax, output key "ge<r>_<|R|>" (Long Table: smallest far threshold).
// Usage: bnd [--maxS N] [--hole h] [--dump-fail] [--distscan]     Build: c++ -O2 -std=c++17 -o bnd bnd.cpp
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <unordered_map>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <deque>
#include <functional>
typedef unsigned __int128 u128;
typedef uint64_t u64;
struct H128 { size_t operator()(const u128 &x) const { return (size_t)((x ^ (x >> 64)) * 0x9E3779B97F4A7C15ULL); } };

static int N;                       // vertices of T
static std::vector<std::vector<int>> rot;
static int hole;
static std::vector<int> ord, pos;   // BFS order of T - h (positions 0..m-1), pos[v]
static std::vector<u64> nbm;        // neighbour masks over positions (T - h)
static int M;                       // m = n - 1

static inline int colAt(u128 c, int p) { return (int)((c >> (2 * p)) & 3); }

static u128 canon(u128 c) {
    int mp[4] = {-1, -1, -1, -1}, nx = 0; u128 out = 0;
    for (int p = 0; p < M; p++) { int x = colAt(c, p); if (mp[x] < 0) mp[x] = nx++; out |= (u128)mp[x] << (2 * p); }
    return out;
}

struct Move { int to; u64 mask; };

int main(int argc, char **argv) {
    size_t maxS = 3000000; int onlyHole = -1; bool dumpFail = false, distScan = false;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--maxS")) maxS = atol(argv[++i]);
        else if (!strcmp(argv[i], "--hole")) onlyHole = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--dump-fail")) dumpFail = true;
        else if (!strcmp(argv[i], "--distscan")) distScan = true;
    }
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream ss(line); std::string name, rs; int n; if (!(ss >> name >> n >> rs)) continue;
        rot.assign(0, {}); std::stringstream rr(rs); std::string tok;
        while (std::getline(rr, tok, ';')) { std::vector<int> r; std::stringstream t2(tok); std::string a; while (std::getline(t2, a, ',')) r.push_back(atoi(a.c_str())); rot.push_back(r); }
        N = rot.size(); if (N > 65) { printf("{\"name\":\"%s\",\"skip\":\"n>65\"}\n", name.c_str()); continue; }
        // faces
        std::set<std::vector<int>> F;
        for (int u = 0; u < N; u++) for (size_t i = 0; i < rot[u].size(); i++) { std::vector<int> f = {u, rot[u][i], rot[u][(i + 1) % rot[u].size()]}; std::sort(f.begin(), f.end()); F.insert(f); }
        for (int h = 0; h < N; h++) {
            if (rot[h].size() != 5 || (onlyHole >= 0 && h != onlyHole)) continue;
            hole = h;
            // BFS distances in T
            std::vector<int> d(N, -1); d[h] = 0; std::deque<int> q{h};
            while (!q.empty()) { int u = q.front(); q.pop_front(); for (int w : rot[u]) if (d[w] < 0) { d[w] = d[u] + 1; q.push_back(w); } }
            int dmax = *std::max_element(d.begin(), d.end());
            // BFS order of T - h from link[0]
            ord.clear(); pos.assign(N, -1); { std::deque<int> q2{rot[h][0]}; pos[rot[h][0]] = 0; ord.push_back(rot[h][0]);
                while (!q2.empty()) { int u = q2.front(); q2.pop_front(); std::vector<int> nb = rot[u]; std::sort(nb.begin(), nb.end());
                    for (int w : nb) if (w != h && pos[w] < 0) { pos[w] = ord.size(); ord.push_back(w); q2.push_back(w); } } }
            M = ord.size();
            nbm.assign(M, 0);
            for (int p = 0; p < M; p++) for (int w : rot[ord[p]]) if (w != h) nbm[p] |= (u64)1 << pos[w];
            std::vector<int> linkp; for (int x : rot[h]) linkp.push_back(pos[x]);
            // enumerate states (first-occurrence normal form)
            std::vector<u128> S; bool over = false;
            {
                std::vector<int> c(M, -1);
                std::vector<u64> back(M, 0); for (int p = 0; p < M; p++) back[p] = nbm[p] & (((u64)1 << p) - 1);
                std::function<void(int, int)> rec = [&](int p, int used) {
                    if (over) return;
                    if (p == M) { u128 x = 0; for (int i = 0; i < M; i++) x |= (u128)c[i] << (2 * i); S.push_back(x); if (S.size() > maxS) over = true; return; }
                    int bad = 0; u64 b = back[p]; while (b) { int i = __builtin_ctzll(b); b &= b - 1; bad |= 1 << c[i]; }
                    for (int x = 0; x < std::min(4, used + 1); x++) if (!(bad >> x & 1)) { c[p] = x; rec(p + 1, std::max(used, x + 1)); }
                    c[p] = -1;
                };
                rec(0, 0);
            }
            if (over) { printf("{\"name\":\"%s\",\"hole\":%d,\"n\":%d,\"skip\":\"S>%zu\"}\n", name.c_str(), h, N, maxS); fflush(stdout); continue; }
            size_t NS = S.size();
            std::unordered_map<u128, int, H128> idx; idx.reserve(NS * 2);
            for (size_t i = 0; i < NS; i++) idx[S[i]] = i;
            std::vector<char> filled(NS);
            for (size_t i = 0; i < NS; i++) { int m = 0; for (int p : linkp) m |= 1 << colAt(S[i], p); filled[i] = __builtin_popcount(m) <= 3; }
            // moves
            std::vector<std::vector<Move>> mv(NS);
            for (size_t i = 0; i < NS; i++) {
                u128 c = S[i]; u64 cm[4] = {0, 0, 0, 0};
                for (int p = 0; p < M; p++) cm[colAt(c, p)] |= (u64)1 << p;
                for (int a = 0; a < 4; a++) for (int b = a + 1; b < 4; b++) {
                    u64 sub = cm[a] | cm[b], left = sub; std::vector<u64> comps;
                    while (left) {
                        u64 comp = left & (~left + 1), fr = comp;
                        while (fr) { u64 nf = 0, f = fr; while (f) { int p = __builtin_ctzll(f); f &= f - 1; nf |= nbm[p]; } nf &= sub & ~comp; comp |= nf; fr = nf; }
                        comps.push_back(comp); left &= ~comp;
                    }
                    if (comps.size() < 2) continue;  // web (or empty pair)
                    for (u64 K : comps) {
                        u128 x = c; u64 f = K;
                        while (f) { int p = __builtin_ctzll(f); f &= f - 1; int y = colAt(c, p); int z = (y == a) ? b : a; x &= ~((u128)3 << (2 * p)); x |= (u128)z << (2 * p); }
                        auto it = idx.find(canon(x)); if (it == idx.end()) { fprintf(stderr, "lookup failed\n"); return 2; }
                        u64 Kv = 0; { u64 g = K; while (g) { int p = __builtin_ctzll(g); g &= g - 1; Kv |= (u64)1 << p; } }
                        mv[i].push_back({it->second, Kv});
                    }
                }
            }
            auto bfs = [&](u64 Rmask, std::vector<int> &dist) {
                dist.assign(NS, -1); std::deque<int> qq;
                for (size_t i = 0; i < NS; i++) if (filled[i]) { dist[i] = 0; qq.push_back(i); }
                while (!qq.empty()) { int k = qq.front(); qq.pop_front(); for (auto &m : mv[k]) if ((m.mask & Rmask) && dist[m.to] < 0) { dist[m.to] = dist[k] + 1; qq.push_back(m.to); } }
            };
            std::vector<int> dF; bfs(~(u64)0, dF);
            long unfilled = 0, unreachF = 0; int dFmax = 0;
            for (size_t i = 0; i < NS; i++) if (!filled[i]) { unfilled++; if (dF[i] < 0) unreachF++; else dFmax = std::max(dFmax, dF[i]); }
            auto toMask = [&](const std::vector<int> &vs) { u64 m = 0; for (int v : vs) if (v != h && pos[v] >= 0) m |= (u64)1 << pos[v]; return m; };
            struct RR { std::string kind; std::vector<int> verts; int fd; };
            std::vector<RR> regions;
            int fmax = -1; for (auto &f : F) { int fd = std::min({d[f[0]], d[f[1]], d[f[2]]}); fmax = std::max(fmax, fd); }
            for (auto &f : F) { int fd = std::min({d[f[0]], d[f[1]], d[f[2]]}); if (fd == fmax) regions.push_back({"faceMax", f, fd}); else if (fd >= 3) regions.push_back({"face3", f, fd}); }
            { std::vector<int> s1, s2, s3; for (int v = 0; v < N; v++) { if (d[v] == dmax) s1.push_back(v); if (d[v] >= dmax - 1) s2.push_back(v); if (d[v] >= 3) s3.push_back(v); }
              if (distScan) for (int r = 2; r <= dmax; r++) { std::vector<int> sr; for (int v = 0; v < N; v++) if (d[v] >= r) sr.push_back(v); regions.push_back({"ge" + std::to_string(r) + "_" + std::to_string(sr.size()), sr, r}); }
              regions.push_back({"shell1", s1, dmax}); regions.push_back({"shell2", s2, dmax - 1}); if (!s3.empty()) regions.push_back({"dist3", s3, 3}); }
            // evaluate
            std::map<std::string, std::vector<long>> agg;  // kind -> [tested, failingRegions, worstFail, maxdR, maxExtra]
            std::string fails;
            std::vector<int> dR;
            u64 rimM = 0; for (int p : linkp) rimM |= (u64)1 << p;
            // rim statistic over faceMax regions: [states with dR>0, dR-lowering R-moves, of them meeting the rim,
            //  states whose every dR-lowering R-move misses the rim, all R-moves from unfilled states, of them meeting the rim]
            long rim[6] = {0, 0, 0, 0, 0, 0};
            for (auto &R : regions) {
                bfs(toMask(R.verts), dR);
                long fail = 0; int mdr = 0, ext = 0;
                for (size_t i = 0; i < NS; i++) if (!filled[i] && dF[i] >= 0) { if (dR[i] < 0) fail++; else { mdr = std::max(mdr, dR[i]); ext = std::max(ext, dR[i] - dF[i]); } }
                if (R.kind == "faceMax") {
                    u64 Rm = toMask(R.verts);
                    for (size_t i = 0; i < NS; i++) {
                        if (filled[i]) continue;
                        for (auto &m : mv[i]) if (m.mask & Rm) { rim[4]++; if (m.mask & rimM) rim[5]++; }
                        if (dR[i] <= 0) continue;
                        rim[0]++; long low = 0, lowRim = 0;
                        for (auto &m : mv[i]) if ((m.mask & Rm) && dR[m.to] == dR[i] - 1) { low++; if (m.mask & rimM) lowRim++; }
                        rim[1] += low; rim[2] += lowRim; if (lowRim == 0) rim[3]++;
                    }
                }
                auto &a = agg[R.kind]; if (a.empty()) a = {0, 0, 0, 0, 0};
                a[0]++; if (fail) a[1]++; a[2] = std::max(a[2], fail); a[3] = std::max<long>(a[3], mdr); a[4] = std::max<long>(a[4], ext);
                if (fail && dumpFail) {
                    char b[256]; snprintf(b, sizeof b, "%s{\"kind\":\"%s\",\"R\":[", fails.empty() ? "" : ",", R.kind.c_str()); fails += b;
                    for (size_t j = 0; j < R.verts.size(); j++) { snprintf(b, sizeof b, "%s%d", j ? "," : "", R.verts[j]); fails += b; }
                    for (size_t i = 0; i < NS; i++) if (!filled[i] && dF[i] >= 0 && dR[i] < 0) {
                        std::string st; for (int v = 0; v < N; v++) st += (v == h) ? '.' : char('0' + colAt(S[i], pos[v]));
                        snprintf(b, sizeof b, "],\"fail\":%ld,\"state\":\"%s\",\"dF\":%d}", fail, st.c_str(), dF[i]); fails += b; break;
                    }
                }
            }
            printf("{\"name\":\"%s\",\"hole\":%d,\"n\":%d,\"S\":%zu,\"unfilled\":%ld,\"unreachF\":%ld,\"dFmax\":%d,\"dmax\":%d,\"fmax\":%d",
                   name.c_str(), h, N, NS, unfilled, unreachF, dFmax, dmax, fmax);
            for (auto &kv : agg) printf(",\"%s\":[%ld,%ld,%ld,%ld,%ld]", kv.first.c_str(), kv.second[0], kv.second[1], kv.second[2], kv.second[3], kv.second[4]);
            printf(",\"faceMaxRim\":[%ld,%ld,%ld,%ld,%ld,%ld]", rim[0], rim[1], rim[2], rim[3], rim[4], rim[5]);
            if (dumpFail && !fails.empty()) printf(",\"fails\":[%s]", fails.c_str());
            printf("}\n"); fflush(stdout);
        }
    }
}
