// jsep_ref (validation only): jsep.cpp unchanged except argv[3] = prefix of slot letters 0..4 (w0 s0 w1 s1 ...)
// restricting the DFS to that prefix.
// jsep: independent exhaustive receiver-row separation for the wheel-level discharging LP (Opus J_lp_checker).
// Written from the row definitions (README s0/s6, JOB28), not from sep3/sep3x.
//
// An arrangement of a receiver u of exact degree d is a cyclic word w_0..w_{d-1} (link) and s_0..s_{d-1}
// (s_i = apex of triangle w_i w_{i+1}), letters 0..4 = degrees 5,6,7,8,9+.
// Its load is sum_i WIN[w_{i-2},w_{i-1},w_i,w_{i+1},w_{i+2}, s_{i-2},s_{i-1},s_i,s_{i+1}] (a 5^9 table built by
// jcheck.py: y outflow, x transfers, rule-T terms; -inf = inadmissible locally).  Arrangements are also excluded when
// (a) a forbidden pattern instance (slot list with letter masks, all rotations/reflections pre-expanded) matches, or
// (b) d in {7,8} and the canonical link word is in RBIG.
// DFS assigns slots in order w_0, s_0, w_1, s_1, ... (slot index w_i = 2i, s_i = 2i+1).  Pruning bound: exact
// windows already complete + G-relaxation (max over unknown window letters) for the rest, closed by max-plus powers.
// Input (argv[1]): text header file; argv[2]: binary WIN table (5^9 doubles).
// Header: d thr K mode  | nrbig then words | ninst then per instance: m, then m pairs (slot mask)
// mode 0: report up to K admissible arrangements with load > thr (then END count nodes)
// mode 1: compute the max admissible load (branch and bound), print MAX load link s nodes
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <string>
#include <set>
#include <algorithm>
#include <cmath>
using namespace std;
static const double NEG = -1e300;
int d; double thr; long K; int mode;
vector<double> WIN;          // 5^9
double G[5][5][5][5][5];     // G[b][q][c][r][dd] = max over a,e,p,s of WIN
vector<vector<double>> Mpow; // Mpow[k] flattened 125x125
set<string> RBIG;
struct Inst { vector<pair<int,int>> sl; };
vector<vector<Inst>> byLast; // instances indexed by (last slot)*5 + letter allowed there; the last slot is not re-tested
int L[64]; string PREF;                   // slot letters
long nodes = 0, found = 0;
double best = NEG; string bestw, bests;
static inline int st(int wp, int sp, int wc) { return (wp * 5 + sp) * 5 + wc; }
static inline double win(int i) {
    auto W = [&](int k) { return L[2 * (((k % d) + d) % d)]; };
    auto S = [&](int k) { return L[2 * (((k % d) + d) % d) + 1]; };
    int idx = W(i - 2); idx = idx * 5 + W(i - 1); idx = idx * 5 + W(i); idx = idx * 5 + W(i + 1); idx = idx * 5 + W(i + 2);
    idx = idx * 5 + S(i - 2); idx = idx * 5 + S(i - 1); idx = idx * 5 + S(i); idx = idx * 5 + S(i + 1);
    return WIN[idx];
}
static string canonlink() {
    string w(d, '0'); for (int i = 0; i < d; i++) w[i] = char('5' + L[2 * i]);
    string b = w;
    for (int r = 0; r < d; r++) {
        string a = w.substr(r) + w.substr(0, r); if (a < b) b = a;
        string rv(a.rbegin(), a.rend()); if (rv < b) b = rv;
    }
    return b;
}
static bool patok(int slot) {
    for (const Inst &I : byLast[slot * 5 + L[slot]]) {
        bool m = true;
        for (auto &pr : I.sl) if (!((pr.second >> L[pr.first]) & 1)) { m = false; break; }
        if (m) return false;
    }
    return true;
}
static void leaf() {
    double tot = 0;
    for (int i = 0; i < d; i++) { double v = win(i); if (v <= NEG / 2) return; tot += v; }
    double cut = (mode == 1) ? best : thr;
    if (!(tot > cut)) return;
    if ((d == 7 || d == 8) && RBIG.count(canonlink())) return;
    string w(d, '0'), s(d, '0');
    for (int i = 0; i < d; i++) { w[i] = char('5' + L[2 * i]); s[i] = char('5' + L[2 * i + 1]); }
    if (mode == 1) { best = tot; bestw = w; bests = s; return; }
    printf("V %.12f %s %s\n", tot, w.c_str(), s.c_str()); found++;
}
static double exactsum = 0; // sum of exact windows i = 2..(k-2)
static bool rec(int slot) {   // returns false to abort
    if (slot == 2 * d) { leaf(); return !(mode == 0 && found >= K); }
    for (int l = 0; l < 5; l++) {
        if (slot < (int)PREF.size() && l != PREF[slot] - '0') continue;
        L[slot] = l; nodes++;
        if (!patok(slot)) continue;
        double saved = exactsum; bool ok = true;
        if (slot % 2 == 0) {
            int k = slot / 2;
            if (k >= 4) { // window k-2 now complete (needs w_k, s_{k-1}); exact for 2 <= i <= d-3
                int i = k - 2;
                if (i >= 2 && i <= d - 3) { double v = win(i); if (v <= NEG / 2) ok = false; else exactsum += v; }
            }
            if (ok && k >= 2) {
                // positions with G relaxation: 1, and every i in [max(2,k-3), k-1] not yet exact (exact only up to k-2... )
                double bnd = exactsum;
                // exact windows are i in [2, k-2] (and <= d-3); G for i = 1 and i = k-1 (if k-1 >= 2) and wrap ones in path
                auto Gt = [&](int i) { // transition at position i (needs w_{i-1}, s_{i-1}, w_i, s_i, w_{i+1})
                    int b = L[2 * ((i - 1 + d) % d)], q = L[2 * ((i - 1 + d) % d) + 1], c = L[2 * i], r = L[2 * i + 1], e = L[2 * ((i + 1) % d)];
                    return G[b][q][c][r][e]; };
                set<int> gpos; gpos.insert(1); if (k - 1 >= 1) gpos.insert(k - 1);
                for (int i = max(2, k - 2 + 1); i <= k - 1; i++) gpos.insert(i);
                for (int i = 2; i <= k - 2; i++) if (i > d - 3) gpos.insert(i); // late windows near the wrap: not exact
                for (int i : gpos) { double v = Gt(i); if (v <= NEG / 2) { ok = false; break; } bnd += v; }
                if (ok) {
                    int nk = d - k + 1; // transitions k..d-1, 0
                    if (k <= d - 1) {
                        int s1 = st(L[0], L[1], L[2]);
                        int sk = st(L[2 * (k - 1)], L[2 * (k - 1) + 1], L[2 * k]);
                        double p = Mpow[nk][sk * 125 + s1];
                        if (p <= NEG / 2) ok = false; else bnd += p;
                    }
                    double cut = (mode == 1) ? best : thr;
                    if (ok && k <= d - 1 && !(bnd > cut + 1e-12)) ok = false;
                }
            }
        }
        if (ok && !rec(slot + 1)) { exactsum = saved; return false; }
        exactsum = saved;
    }
    return true;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); if (argc > 3) PREF = argv[3];
    if (fscanf(f, "%d %lf %ld %d", &d, &thr, &K, &mode) != 4) return 1;
    int nr; if (fscanf(f, "%d", &nr) != 1) return 1;
    for (int i = 0; i < nr; i++) { char buf[64]; if (fscanf(f, "%63s", buf) != 1) return 1; RBIG.insert(buf); }
    long ni; if (fscanf(f, "%ld", &ni) != 1) return 1;
    byLast.assign(10 * d, {});
    for (long i = 0; i < ni; i++) {
        int m; if (fscanf(f, "%d", &m) != 1) return 1; Inst I; int last = -1;
        for (int j = 0; j < m; j++) { int s, k; if (fscanf(f, "%d %d", &s, &k) != 2) return 1; I.sl.push_back({s, k}); last = max(last, s); }
        int lm = 0; Inst J;
        for (auto &pr : I.sl) { if (pr.first == last) lm = pr.second; else J.sl.push_back(pr); }
        for (int l = 0; l < 5; l++) if ((lm >> l) & 1) byLast[last * 5 + l].push_back(J);
    }
    fclose(f);
    WIN.resize(1953125);
    FILE *g = fopen(argv[2], "rb"); if (fread(WIN.data(), sizeof(double), WIN.size(), g) != WIN.size()) return 2; fclose(g);
    for (int b = 0; b < 5; b++) for (int q = 0; q < 5; q++) for (int c = 0; c < 5; c++) for (int r = 0; r < 5; r++) for (int e = 0; e < 5; e++) {
        double mx = NEG;
        for (int a = 0; a < 5; a++) for (int ee = 0; ee < 5; ee++) for (int p = 0; p < 5; p++) for (int s = 0; s < 5; s++) {
            int idx = ((((((((a * 5 + b) * 5 + c) * 5 + e) * 5 + ee) * 5 + p) * 5 + q) * 5 + r) * 5 + s);
            mx = max(mx, WIN[idx]);
        }
        G[b][q][c][r][e] = mx;
    }
    // M[(b,q,c) -> (c,r,e)] = G[b][q][c][r][e]
    vector<double> M(125 * 125, NEG);
    for (int b = 0; b < 5; b++) for (int q = 0; q < 5; q++) for (int c = 0; c < 5; c++) for (int r = 0; r < 5; r++) for (int e = 0; e < 5; e++)
        M[st(b, q, c) * 125 + st(c, r, e)] = G[b][q][c][r][e];
    Mpow.assign(d + 2, vector<double>());
    Mpow[1] = M;
    for (int k = 2; k <= d + 1; k++) {
        vector<double> P(125 * 125, NEG);
        for (int a = 0; a < 125; a++) for (int m = 0; m < 125; m++) {
            double x = Mpow[k - 1][a * 125 + m]; if (x <= NEG / 2) continue;
            for (int b = 0; b < 125; b++) { double y = M[m * 125 + b]; if (y <= NEG / 2) continue; if (x + y > P[a * 125 + b]) P[a * 125 + b] = x + y; }
        }
        Mpow[k] = P;
    }
    rec(0);
    if (mode == 1) printf("MAX %.12f %s %s %ld\n", best, bestw.c_str(), bests.c_str(), nodes);
    else printf("END %ld %ld\n", found, nodes);
    return 0;
}
