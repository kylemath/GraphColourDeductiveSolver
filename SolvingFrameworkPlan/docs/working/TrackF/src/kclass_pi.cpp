// kclass_pi.cpp -- Track F [exploratory]: kclass.cpp + pi-orbit (R+3) structure of DL states and of targetless classes.
// Extra output per hole: allDLcyc = lengths of all-DL pi-cycles; per class (extra tuple piC): [#states on all-DL pi-cycles, #pi-path ends, #filled].
// Original header follows.
// kclass.cpp: Kempe classes of 4-colourings of T - h (independent of picyc / studiointel kempe_classes).
// States = proper 4-colourings of T - h up to renaming (first-occurrence normal form along a BFS order from the link).
// Moves = swap of any Kempe component (any of the 6 colour pairs). Union-find over all moves.
// Per class: size, #filled (link uses <= 3 colours), #DL, and for each class the restriction "frozen-ness":
//   kempe-degree = number of distinct neighbour states (min/max over the class).
// Also reports, for each class, whether any of its filled states extends to a colouring of T whose ALL three
// Tait 2-factors (in the fullerene) are Hamiltonian -- not computed here (see tait_frozen.py).
// Input: "name n rot" lines; args: FILE HOLE(s comma) ; n <= 64.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
typedef uint64_t u64; typedef unsigned __int128 u128;
static int N, H; static std::vector<std::vector<int>> rot; static u64 adj[64]; static std::vector<int> order; static std::vector<std::vector<int>> prevn;
static std::vector<u128> ALL; static int col[64]; static int X[5];
static inline u128 keyof(const int *c) { u128 k = 0; for (int v = 0; v < N; v++) if (v != H) k |= (u128)c[v] << (2 * v); return k; }
static inline void unkey(u128 k, int *c) { for (int v = 0; v < N; v++) c[v] = v == H ? -1 : (int)((k >> (2 * v)) & 3); }
static void normal(int *c) { int mp[4] = {-1, -1, -1, -1}, nx = 0; for (int v : order) { if (mp[c[v]] < 0) mp[c[v]] = nx++; } for (int v = 0; v < N; v++) if (v != H) c[v] = mp[c[v]]; }
static void rec(size_t i, int used) {
    if (i == order.size()) { ALL.push_back(keyof(col)); return; }
    int v = order[i]; int forb = 0; for (int u : prevn[i]) forb |= 1 << col[u];
    int top = std::min(used + 1, 4); for (int a = 0; a < top; a++) if (!(forb >> a & 1)) { col[v] = a; rec(i + 1, std::max(used, a + 1)); }
}
static inline u64 flood(int s, u64 M) { u64 comp = 1ULL << s, fr = comp; while (fr) { u64 nb = 0; for (u64 f = fr; f; f &= f - 1) nb |= adj[__builtin_ctzll(f)]; nb &= M & ~comp; comp |= nb; fr = nb; } return comp; }
static std::vector<int> par; static int fnd(int x) { while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; } return x; }
int main(int argc, char **argv) {
    FILE *in = fopen(argv[1], "r"); static char line[1 << 20]; std::string want = argc > 3 ? argv[3] : "";
    while (fgets(line, sizeof line, in)) {
        char name[256]; int n, off; if (sscanf(line, "%255s %d %n", name, &n, &off) < 2) continue; if (!want.empty() && want != name) continue; if (n > 64) continue;
        N = n; rot.assign(N, {}); char *p = line + off; for (int v = 0; v < N; v++) { while (*p && *p != ';' && *p != '\n' && *p != ' ' && *p != '\r') { rot[v].push_back(strtol(p, &p, 10)); if (*p == ',') p++; } if (*p == ';') p++; }
        for (int v = 0; v < N; v++) { adj[v] = 0; for (int w : rot[v]) adj[v] |= 1ULL << w; }
        std::vector<int> holes; { char *q = argv[2]; if (!strcmp(q, "5")) { for (int v = 0; v < N; v++) if (rot[v].size() == 5) holes.push_back(v); } else if (!strcmp(q, "none")) holes.push_back(-1); else while (*q) { holes.push_back(strtol(q, &q, 10)); if (*q == ',') q++; } }
        for (int h : holes) {
            H = h; std::vector<int> seen(N, 0); order.clear();
            if (h >= 0) { for (int t = 0; t < 5; t++) X[t] = rot[h][t]; seen[h] = 1; for (int t = 0; t < 5; t++) { order.push_back(X[t]); seen[X[t]] = 1; } } else { order.push_back(0); seen[0] = 1; }
            for (size_t q = 0; q < order.size(); q++) for (int w : rot[order[q]]) if (!seen[w]) { seen[w] = 1; order.push_back(w); }
            std::vector<int> pos(N, -1); for (size_t q = 0; q < order.size(); q++) pos[order[q]] = q;
            prevn.assign(order.size(), {}); for (size_t q = 0; q < order.size(); q++) for (int w : rot[order[q]]) if (w != h && pos[w] < (int)q) prevn[q].push_back(w);
            ALL.clear(); for (int v = 0; v < N; v++) col[v] = -1; rec(0, 0); std::sort(ALL.begin(), ALL.end());
            long long S = ALL.size(); par.resize(S); for (long long i = 0; i < S; i++) par[i] = i;
            long long pidBad[3] = {0, 0, 0}, dualBad[2] = {0, 0}; std::vector<int> kind(S), kdeg(S), viol(S, 0); std::vector<long long> pim(S, -1); u64 oddm = 0; for (int v = 0; v < N; v++) if (v != h && (rot[v].size() & 1)) oddm |= 1ULL << v;
            u64 allm = 0; for (int v = 0; v < N; v++) if (v != h) allm |= 1ULL << v;
            int c[64], nc[64];
            for (long long i = 0; i < S; i++) {
                unkey(ALL[i], c); u64 cm[4] = {0, 0, 0, 0}; for (int v = 0; v < N; v++) if (v != h) cm[c[v]] |= 1ULL << v;
                int seenc = 0; if (h >= 0) for (int t = 0; t < 5; t++) seenc |= 1 << c[X[t]];
                if (h < 0 || __builtin_popcount(seenc) <= 3) kind[i] = 0; else {
                    int j = 0; for (; j < 5; j++) if (c[X[j]] == c[X[(j + 2) % 5]]) break;
                    int m = X[(j + 1) % 5], a = X[(j + 3) % 5], b = X[(j + 4) % 5];
                    bool l1 = flood(m, cm[c[m]] | cm[c[a]]) >> a & 1, l2 = flood(m, cm[c[m]] | cm[c[b]]) >> b & 1; kind[i] = (l1 && l2) ? 2 : 1;
                    int x2 = X[(j + 2) % 5]; int al = c[x2];
                    int pA = __builtin_popcountll(flood(x2, cm[al] | cm[c[a]]) & oddm) & 1, pB = __builtin_popcountll(flood(x2, cm[al] | cm[c[b]]) & oddm) & 1;
                    if (pA != (int)l2 || pB != (int)l1) viol[i] = 1;
                    // combinatorial parity identity (any surface): eps(K_aA(x2)) = [x_j notin K], eps(K_aB(x2)) = [x_j notin K], eps(K_amu(x2)) = 1
                    u64 KA = flood(x2, cm[al] | cm[c[a]]), KB = flood(x2, cm[al] | cm[c[b]]), KM = flood(x2, cm[al] | cm[c[m]]);
                    int inA = KA >> X[j] & 1, inB = KB >> X[j] & 1, pM = __builtin_popcountll(KM & oddm) & 1;
                    if (pA != !inA) pidBad[0]++; if (pB != !inB) pidBad[1]++; if (!pM) pidBad[2]++;
                    if ((int)l2 != !inA) dualBad[0]++; if ((int)l1 != !inB) dualBad[1]++;
                    if (!inA) { for (int v = 0; v < N; v++) { if (v == h) { nc[v] = -1; continue; } int x = c[v]; if (KA >> v & 1) x = x == al ? c[a] : al; nc[v] = x; }
                        normal(nc); u128 k = keyof(nc); long long jx = std::lower_bound(ALL.begin(), ALL.end(), k) - ALL.begin(); if (jx >= S || ALL[jx] != k) { fprintf(stderr, "missing pi\n"); return 4; } pim[i] = jx; } }
                std::vector<long long> nbrs;
                for (int p1 = 0; p1 < 4; p1++) for (int q1 = p1 + 1; q1 < 4; q1++) { u64 M = cm[p1] | cm[q1];
                    while (M) { u64 K = flood(__builtin_ctzll(M), cm[p1] | cm[q1]); M &= ~K;
                        for (int v = 0; v < N; v++) { if (v == h) { nc[v] = -1; continue; } int x = c[v]; if (K >> v & 1) x = x == p1 ? q1 : p1; nc[v] = x; }
                        normal(nc); u128 k = keyof(nc); long long jx = std::lower_bound(ALL.begin(), ALL.end(), k) - ALL.begin();
                        if (jx >= S || ALL[jx] != k) { fprintf(stderr, "missing state\n"); return 3; }
                        if (jx != i) nbrs.push_back(jx); int ra = fnd(i), rb = fnd(jx); if (ra != rb) par[ra] = rb; } }
                std::sort(nbrs.begin(), nbrs.end()); kdeg[i] = std::unique(nbrs.begin(), nbrs.end()) - nbrs.begin();
            }
            // all-DL pi-cycles: follow pi through DL states
            std::vector<int> onc(S, 0), mark(S, 0); std::vector<long long> cyc;
            for (long long i = 0; i < S; i++) { if (kind[i] != 2 || mark[i]) continue; std::vector<long long> path; long long k = i;
                while (k >= 0 && kind[k] == 2 && !mark[k]) { mark[k] = 2; path.push_back(k); k = pim[k]; }
                if (k >= 0 && kind[k] == 2 && mark[k] == 2) { long long L = 0; for (long long t = path.size() - 1; t >= 0; t--) { onc[path[t]] = 1; L++; if (path[t] == k) break; } cyc.push_back(L); }
                for (long long t : path) mark[t] = 1; }
            // longest pi-run through DL states not on a cycle (number of consecutive DL states)
            long long maxrun = 0; { std::vector<long long> run(S, 0);
                for (long long i = 0; i < S; i++) { if (kind[i] != 2 || onc[i] || run[i]) continue; std::vector<long long> st; long long k = i;
                    while (k >= 0 && kind[k] == 2 && !onc[k] && !run[k]) { st.push_back(k); k = pim[k]; }
                    long long base = (k >= 0 && kind[k] == 2 && !onc[k]) ? run[k] : 0;
                    for (long long t = st.size() - 1; t >= 0; t--) { run[st[t]] = ++base; } }
                for (long long i = 0; i < S; i++) maxrun = std::max(maxrun, run[i]); }
            std::vector<int> hasPre(S, 0); for (long long i = 0; i < S; i++) if (pim[i] >= 0) hasPre[pim[i]] = 1;
            std::map<int, std::vector<long long>> pc; for (long long i = 0; i < S; i++) { auto &e = pc[fnd(i)]; if (e.empty()) e = {0, 0, 0}; e[0] += onc[i]; if (kind[i] == 2 && (pim[i] < 0 || !hasPre[i])) e[1]++; if (kind[i] == 0) e[2]++; }
            std::string sc; for (auto &kv : pc) if (kv.second[0]) { char b[96]; snprintf(b, sizeof b, "%s[%lld,%lld,%lld]", sc.empty() ? "" : ",", kv.second[0], kv.second[1], kv.second[2]); sc += b; }
            std::string sy; for (long long L : cyc) { char b[32]; snprintf(b, sizeof b, "%s%lld", sy.empty() ? "" : ",", L); sy += b; }
            std::map<int, std::vector<long long>> cl; for (long long i = 0; i < S; i++) { auto &e = cl[fnd(i)]; if (e.empty()) e = {0, 0, 0, 0, 1 << 30, 0, 0}; e[0]++; e[6] += viol[i]; if (kind[i] == 0) e[1]++; if (kind[i] == 2) e[2]++; if (kind[i] == 1) e[3]++; e[4] = std::min<long long>(e[4], kdeg[i]); e[5] = std::max<long long>(e[5], kdeg[i]); }
            std::string s; for (auto &kv : cl) { char b[128]; snprintf(b, sizeof b, "%s[%lld,%lld,%lld,%lld,%lld,%lld,%lld]", s.empty() ? "" : ",", kv.second[0], kv.second[1], kv.second[2], kv.second[3], kv.second[4], kv.second[5], kv.second[6]); s += b; }
            printf("{\"graph\":\"%s\",\"hole\":%d,\"pid_bad\":[%lld,%lld,%lld],\"dual_bad\":[%lld,%lld],\"maxDLrun\":%lld,\"allDLcyc\":[%s],\"cycClasses[onCycles,pathEnds,filled]\":[%s],\"states\":%lld,\"classes\":%zu,\"cls[size,filled,DL,unfilledNonDL,minKdeg,maxKdeg,lockParityViolations]\":[%s]}\n", name, h, pidBad[0], pidBad[1], pidBad[2], dualBad[0], dualBad[1], maxrun, sy.c_str(), sc.c_str(), S, cl.size(), s.c_str()); fflush(stdout);
        }
    }
}
