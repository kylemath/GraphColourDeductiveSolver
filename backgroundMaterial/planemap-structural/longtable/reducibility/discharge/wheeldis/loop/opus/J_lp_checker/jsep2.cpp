// jsep2: faster exhaustive receiver-row separation (Opus J_lp_checker), same input/output contract as jsep.cpp.
// Differences from jsep (exactness preserved; the search space and pruning change, not the row semantics):
//  (1) rotation symmetry break: with pair value P_i = 5*w_i + s_i, only arrangements with P_0 = max_i P_i are
//      enumerated (every rotation class has such a representative; load, R5/R6 admissibility, RBIG and the
//      pattern instances -- pre-expanded over all 2d symmetries -- are rotation-invariant).  Flag: argv[4]=0 disables.
//  (2) tighter admissible bound: states A_i = (w_{i-1}, s_{i-1}, w_i, s_i, w_{i+1}) (3125), transition A_i -> A_{i+1}
//      carries H_i = max over (w_{i-2}, s_{i-2}) of WIN (jsep relaxed 4 letters, this relaxes 2).  For each fixed
//      A_1 (first five slots) backward max-plus vectors V_n[x] = best n-step path x -> A_1 are computed once.
//      Bound after w_k (k >= 2): H(window 1) + exact windows 2..k-2 + V_{d-k+2}[A_{k-1}].  Pruned only when
//      bound <= cut - 1e-12 (conservative against float reordering).
//  (3) threads (argv[3], default 1): the A_1 prefixes are a shared work queue (atomic claim flags).
// argv: hdr win [threads] [sym]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <string>
#include <set>
#include <algorithm>
#include <cmath>
#include <atomic>
#include <thread>
#include <mutex>
#include <chrono>
using namespace std;
static const double NEG = -1e300;
int d; double thr; long K; int mode; int SYM = 1; int NT = 1;
vector<double> WIN;            // 5^9, index a,b,c,e,f,p,q,r,s
vector<double> H;              // 5^7, index b,c,e,f,q,r,s  (max over a, p)
set<string> RBIG;
struct Inst { vector<pair<int,int>> sl; };
vector<vector<Inst>> byLast;
// bitset index: for list (last slot l, letter x) with N instances, BS[l*5+x][(j*5+y)*nw + w] has bit n set iff
// instance n allows letter y at slot j (j < l; unconstrained slots allow every letter).  An instance matches iff its
// bit survives the AND over j = l-1..0 of BS[.][(j*5+L[j])].
struct BList { int nw = 0; vector<uint64_t> B; };
vector<BList> BS;
atomic<long> found(0), totnodes(0), tasksdone(0);
atomic<int> stopflag(0);
vector<atomic<int>> *claimed;
int ntasks = 3125;
mutex outmx;
atomic<double> gbest(NEG); string gbw, gbs;
chrono::steady_clock::time_point T0;

static inline int st5(int b, int q, int c, int r, int e) { return (((b * 5 + q) * 5 + c) * 5 + r) * 5 + e; }
static inline double Hv(int b, int q, int c, int r, int e, int s, int f) { // transition (b,q,c,r,e) -> (c,r,e,s,f)
    return H[(((((b * 5 + c) * 5 + e) * 5 + f) * 5 + q) * 5 + r) * 5 + s];
}

struct Ctx {
    int L[64]; long nodes = 0; double exactsum = 0; double h1 = 0;
    vector<vector<double>> V; // V[n][x]
    double best = NEG; string bw, bs;
    int W(int k) const { return L[2 * (((k % d) + d) % d)]; }
    int S(int k) const { return L[2 * (((k % d) + d) % d) + 1]; }
    double win(int i) const {
        int idx = W(i - 2); idx = idx * 5 + W(i - 1); idx = idx * 5 + W(i); idx = idx * 5 + W(i + 1); idx = idx * 5 + W(i + 2);
        idx = idx * 5 + S(i - 2); idx = idx * 5 + S(i - 1); idx = idx * 5 + S(i); idx = idx * 5 + S(i + 1);
        return WIN[idx];
    }
    string canonlink() const {
        string w(d, '0'); for (int i = 0; i < d; i++) w[i] = char('5' + L[2 * i]);
        string b = w;
        for (int r = 0; r < d; r++) {
            string a = w.substr(r) + w.substr(0, r); if (a < b) b = a;
            string rv(a.rbegin(), a.rend()); if (rv < b) b = rv;
        }
        return b;
    }
    bool patok(int slot) const {
        const BList &bl = BS[slot * 5 + L[slot]];
        const int nw = bl.nw; if (!nw) return true;
        const uint64_t *B = bl.B.data();
        for (int w = 0; w < nw; w++) {
            uint64_t x = ~0ULL;
            for (int j = slot - 1; j >= 0 && x; j--) x &= B[(j * 5 + L[j]) * nw + w];
            if (x) return false;
        }
        return true;
    }
    double cut() const { return mode == 1 ? max(best, gbest.load(memory_order_relaxed)) : thr; }
    void computeV() { // target A_1 = (w0, s0, w1, s1, w2)
        int tgt = st5(L[0], L[1], L[2], L[3], L[4]);
        V.assign(d + 1, vector<double>(3125, NEG));
        V[0][tgt] = 0;
        for (int n = 1; n <= d; n++) {
            const vector<double> &P = V[n - 1]; vector<double> &Q = V[n];
            for (int x = 0; x < 3125; x++) {
                int e = x % 5, r = (x / 5) % 5, c = (x / 25) % 5, q = (x / 125) % 5, b = x / 625;
                double m = NEG;
                int ybase = ((c * 5 + r) * 5 + e) * 25;
                for (int s = 0; s < 5; s++) for (int f = 0; f < 5; f++) {
                    double p = P[ybase + s * 5 + f]; if (p <= NEG / 2) continue;
                    double h = Hv(b, q, c, r, e, s, f); if (h <= NEG / 2) continue;
                    if (h + p > m) m = h + p;
                }
                Q[x] = m;
            }
        }
    }
    void leaf() {
        double tot = 0;
        for (int i = 0; i < d; i++) { double v = win(i); if (v <= NEG / 2) return; tot += v; }
        double c = cut();
        if (!(tot > c)) return;
        if ((d == 7 || d == 8) && RBIG.count(canonlink())) return;
        string w(d, '0'), s(d, '0');
        for (int i = 0; i < d; i++) { w[i] = char('5' + L[2 * i]); s[i] = char('5' + L[2 * i + 1]); }
        if (mode == 1) {
            best = tot; bw = w; bs = s;
            double g = gbest.load();
            while (tot > g && !gbest.compare_exchange_weak(g, tot)) {}
            return;
        }
        lock_guard<mutex> lk(outmx);
        if (found >= K) { stopflag = 1; return; }
        printf("V %.12f %s %s\n", tot, w.c_str(), s.c_str()); found++;
        if (found >= K) stopflag = 1;
    }
    void rec(int slot) {
        if (stopflag) return;
        if (slot == 2 * d) { leaf(); return; }
        for (int ii = 0; ii < 5; ii++) {
            int l = (slot == 0 && SYM) ? 4 - ii : ii;   // w_0 is the max letter: try big ones first (good incumbent)
            L[slot] = l; nodes++;
            if (SYM && slot >= 2) {
                if (slot % 2 == 0) { if (l > L[0]) break; }               // w_i > w_0 -> P_i > P_0
                else if (L[slot - 1] == L[0] && l > L[1]) break;           // P_i > P_0
            }
            if (!patok(slot)) continue;
            if (slot == 4) {
                int id = st5(L[0], L[1], L[2], L[3], L[4]);
                int z = 0; if (!(*claimed)[id].compare_exchange_strong(z, 1)) continue;
                computeV();
            }
            double saved = exactsum, savedh = h1; bool ok = true;
            if (slot % 2 == 0) {
                int k = slot / 2;
                if (k >= 4 && k - 2 <= d - 3) { double v = win(k - 2); if (v <= NEG / 2) ok = false; else exactsum += v; }
                if (ok && k == 3) { h1 = Hv(L[0], L[1], L[2], L[3], L[4], L[5], L[6]); if (h1 <= NEG / 2) ok = false; }
                if (ok && k >= 2 && k <= d - 1) {
                    int x = st5(L[2 * (k - 2)], L[2 * (k - 2) + 1], L[2 * (k - 1)], L[2 * (k - 1) + 1], L[2 * k]);
                    double p = V[d - k + 2][x];
                    if (p <= NEG / 2) ok = false;
                    else {
                        double bnd = p + (k >= 3 ? h1 + exactsum : 0.0);
                        if (bnd <= cut() + (mode == 1 ? 1e-12 : -1e-12)) ok = false;   // mode 1: ties cannot raise the max
                    }
                }
            }
            if (ok) rec(slot + 1);
            exactsum = saved; h1 = savedh;
            if (slot == 4) {
                long t = ++tasksdone;
                if (t % 100 == 0) {
                    double el = chrono::duration<double>(chrono::steady_clock::now() - T0).count();
                    fprintf(stderr, "P tasks %ld nodes %ld found %ld best %.9f %.1fs\n", t, totnodes.load() + nodes, found.load(), max(best, gbest.load()), el);
                }
            }
            if (stopflag) return;
        }
    }
};

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    if (argc > 3) NT = atoi(argv[3]);
    if (argc > 4) SYM = atoi(argv[4]);
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
    BS.assign(10 * d, {});
    for (int ls = 0; ls < 2 * d; ls++) for (int x = 0; x < 5; x++) {
        auto &lst = byLast[ls * 5 + x]; BList &bl = BS[ls * 5 + x];
        int N = lst.size(); bl.nw = (N + 63) / 64; if (!N) continue;
        bl.B.assign((size_t)ls * 5 * bl.nw, 0);
        for (int n = 0; n < N; n++) {
            int mask[64]; for (int j = 0; j < ls; j++) mask[j] = 31;
            for (auto &pr : lst[n].sl) mask[pr.first] &= pr.second;
            for (int j = 0; j < ls; j++) for (int y = 0; y < 5; y++) if ((mask[j] >> y) & 1)
                bl.B[(size_t)(j * 5 + y) * bl.nw + n / 64] |= 1ULL << (n % 64);
        }
        // padding bits of the last word stay 0 at every (j, y): never match
        if (ls == 0 && N) { fprintf(stderr, "pattern with a single slot at slot 0\n"); }
    }
    WIN.resize(1953125);
    FILE *g = fopen(argv[2], "rb"); if (fread(WIN.data(), sizeof(double), WIN.size(), g) != WIN.size()) return 2; fclose(g);
    H.assign(78125, NEG);
    for (int a = 0; a < 5; a++) for (int b = 0; b < 5; b++) for (int c = 0; c < 5; c++) for (int e = 0; e < 5; e++) for (int ff = 0; ff < 5; ff++)
    for (int p = 0; p < 5; p++) for (int q = 0; q < 5; q++) for (int r = 0; r < 5; r++) for (int s = 0; s < 5; s++) {
        double v = WIN[((((((((a * 5 + b) * 5 + c) * 5 + e) * 5 + ff) * 5 + p) * 5 + q) * 5 + r) * 5 + s)];
        double &h = H[(((((b * 5 + c) * 5 + e) * 5 + ff) * 5 + q) * 5 + r) * 5 + s];
        if (v > h) h = v;
    }
    claimed = new vector<atomic<int>>(3125);
    for (auto &c : *claimed) c = 0;
    T0 = chrono::steady_clock::now();
    vector<Ctx> C(NT); vector<thread> th;
    for (int t = 0; t < NT; t++) th.emplace_back([&, t] { C[t].rec(0); totnodes += C[t].nodes; });
    for (auto &x : th) x.join();
    long nodes = totnodes;
    if (mode == 1) {
        int bi = -1; double bv = NEG;
        for (int t = 0; t < NT; t++) if (C[t].best > bv) { bv = C[t].best; bi = t; }
        printf("MAX %.12f %s %s %ld\n", bv, bi >= 0 ? C[bi].bw.c_str() : "-", bi >= 0 ? C[bi].bs.c_str() : "-", nodes);
    } else printf("END %ld %ld\n", found.load(), nodes);
    return 0;
}
