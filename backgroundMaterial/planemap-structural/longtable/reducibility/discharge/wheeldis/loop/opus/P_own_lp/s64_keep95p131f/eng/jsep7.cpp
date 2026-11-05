// jsep7 (s47, RELAY_SPEC_s47 47.3): jsep6 + argv[9] = l3qV = 8 file, same layout as argv[7] (QX8[2*5^6] <= 0, PQ8[125] >= 0,
//   MK8[2*5^6]). Leaf, after the V = 7 correction: d = 7: tot -= PQ8[(c, a, a2)] at every link 8 i, sides sg (c, a, a2 =
//   W(i+sg), W(i+2sg), W(i+3sg)); d = 8: tot += QX8[(sg, c, w2, w3, w4, a, o)] at every link 7 (read as the V = 7 payee).
//   Every correction <= 0, so all bounds stay sound. Mode-2 row ids: 1200000000 + payer index, 1300000000 + (c*5+a)*32 + mask.
// jsep6 (Opus s43, RELAY_SPEC_s43 43.3): jsep5 + argv[7] may be 'none' + argv[8] = fy2 face file ZT[2*5^9] doubles
//   (z of a vis2 five window for t-class 0/1, -1e300 if not a vis2 five or class not allowed). Leaf: for every face i
//   (W(i) = W(i+1) = S(i) = 0) tot += max_t (ZT_i[t] + ZT_i1[t]) - max_t ZT_i[t] - max_t ZT_i1[t] (<= 0; WIN holds the UBs).
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
// jsep5 (stage 28, Opus s28q): jsep4 + argv[7] = l3q file (RELAY_SPEC_s21 21.6). d = 7 only. Binary doubles:
//   QX[2*5^6] (exact Q minus the window upper bound UB already in WIN, <= 0), PQ[125] (payer q, >= 0), MK[2*5^6] (mask or -1).
//   Leaf: tot += sum over link 7s i, sides sg of QX[...] - PQ[...] (every correction <= 0, so all bounds stay sound).
//   argv[5] / argv[6] may be 'none'.
// jsep4 (stage 14): jsep3 + argv[6] = bonus file (canonical d-link -> value subtracted from the leaf load)
// jsep3 (Opus P_own_lp): jsep2 + mode 2 = the K MOST violated DISTINCT rows (exhaustive: a row above thr is
// missed only if K rows with larger load exist).  Distinctness by the sorted multiset of per-position class ids
// (argv[5], int32 table over the 5^9 window index; class 0 = no contribution), so fillings of slots that no
// coefficient reads collapse to one row.  Pruning cut = max(thr, K-th best load).
// argv: hdr win [threads] [sym] [classfile]
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
#include <map>
using namespace std;
static const double NEG = -1e300;
int d; double thr; long K; int mode; int SYM = 1; int NT = 1;
vector<double> WIN; vector<int> CLS; map<vector<int>, pair<double,pair<string,string>>> TOPS; multimap<double, vector<int>> TOPV; atomic<double> gkth(NEG);            // 5^9, index a,b,c,e,f,p,q,r,s
vector<double> H;              // 5^7, index b,c,e,f,q,r,s  (max over a, p)
vector<double> QX, PQ, MK; bool L3 = false;
vector<double> ZT; bool FY2 = false;
vector<double> QX8, PQ8, MK8; bool L3V = false;
set<string> RBIG; map<string,double> BONUS;   // jsep4: d = 7 link inflow subtracted at the leaf (sound: bounds ignore it)
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
    double cut() const { return mode == 1 ? max(best, gbest.load(memory_order_relaxed)) : (mode == 2 ? max(thr, gkth.load(memory_order_relaxed)) : thr); }
    int widx(int i) const {
        int idx = W(i - 2); idx = idx * 5 + W(i - 1); idx = idx * 5 + W(i); idx = idx * 5 + W(i + 1); idx = idx * 5 + W(i + 2);
        idx = idx * 5 + S(i - 2); idx = idx * 5 + S(i - 1); idx = idx * 5 + S(i); idx = idx * 5 + S(i + 1);
        return idx;
    }
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
        if (!BONUS.empty()) { auto it = BONUS.find(canonlink()); if (it != BONUS.end()) { tot -= it->second; if (!(tot > c)) return; } }
        vector<int> l3ids;
        if (L3 && d == 7) {
            double corr = 0;
            for (int i = 0; i < d; i++) {
                if (W(i) != 2) continue;
                for (int sg = 1; sg >= -1; sg -= 2) {
                    int cc = W(i + sg), w2 = W(i + 2 * sg), w3 = W(i + 3 * sg), w4 = W(i + 4 * sg);
                    int a = sg > 0 ? S(i) : S(i - 1), o = sg > 0 ? S(i - 1) : S(i);
                    int qi = (((((sg > 0 ? 0 : 1) * 5 + cc) * 5 + w2) * 5 + w3) * 5 + w4) * 25 + a * 5 + o;
                    int pi = (cc * 5 + w2) * 5 + w3;
                    corr += QX[qi] - PQ[pi];
                    if (cc <= 1 && w2 <= 1) l3ids.push_back(1000000000 + pi);
                    if (MK[qi] >= 0) l3ids.push_back(1100000000 + (cc * 5 + a) * 32 + (int)MK[qi]);
                }
            }
            tot += corr; if (!(tot > c)) return;
        }
        if (L3V && (d == 7 || d == 8)) {   // jsep7: l3qV = 8
            double corr = 0;
            for (int i = 0; i < d; i++) {
                if (d == 7 && W(i) == 3) {
                    for (int sg = 1; sg >= -1; sg -= 2) {
                        int cc = W(i + sg), w2 = W(i + 2 * sg), w3 = W(i + 3 * sg);
                        int pi = (cc * 5 + w2) * 5 + w3;
                        corr -= PQ8[pi];
                        if (cc <= 1 && w2 <= 1) l3ids.push_back(1200000000 + pi);
                    }
                }
                if (d == 8 && W(i) == 2) {
                    for (int sg = 1; sg >= -1; sg -= 2) {
                        int cc = W(i + sg), w2 = W(i + 2 * sg), w3 = W(i + 3 * sg), w4 = W(i + 4 * sg);
                        int a = sg > 0 ? S(i) : S(i - 1), o = sg > 0 ? S(i - 1) : S(i);
                        int qi = (((((sg > 0 ? 0 : 1) * 5 + cc) * 5 + w2) * 5 + w3) * 5 + w4) * 25 + a * 5 + o;
                        corr += QX8[qi];
                        if (MK8[qi] >= 0) l3ids.push_back(1300000000 + (cc * 5 + a) * 32 + (int)MK8[qi]);
                    }
                }
            }
            tot += corr; if (!(tot > c)) return;
        }
        if (FY2) {
            double corr = 0;
            for (int i = 0; i < d; i++) {
                if (W(i) != 0 || W(i + 1) != 0 || S(i) != 0) continue;
                const double *A = &ZT[2 * (size_t)widx(i)], *B = &ZT[2 * (size_t)widx(i + 1)];
                double ua = max(A[0], A[1]), ub = max(B[0], B[1]);
                if (ua <= NEG / 2 || ub <= NEG / 2) { fprintf(stderr, "fy2: face %d without a vis2 entry\n", i); exit(7); }
                double ex = NEG;
                for (int t = 0; t < 2; t++) if (A[t] > NEG / 2 && B[t] > NEG / 2) ex = max(ex, A[t] + B[t]);
                if (ex <= NEG / 2) { fprintf(stderr, "fy2: face %d with disjoint allowed sets\n", i); exit(8); }
                corr += ex - ua - ub;
            }
            if (corr > 1e-12) { fprintf(stderr, "fy2: positive correction\n"); exit(9); }
            tot += corr; if (!(tot > c)) return;
        }
        string w(d, '0'), s(d, '0');
        for (int i = 0; i < d; i++) { w[i] = char('5' + L[2 * i]); s[i] = char('5' + L[2 * i + 1]); }
        if (mode == 1) {
            best = tot; bw = w; bs = s;
            double g = gbest.load();
            while (tot > g && !gbest.compare_exchange_weak(g, tot)) {}
            return;
        }
        if (mode == 2) {
            vector<int> sig; for (int i = 0; i < d; i++) { int c = CLS[widx(i)]; if (c) sig.push_back(c); }
            for (int x : l3ids) sig.push_back(x);
            sort(sig.begin(), sig.end());
            lock_guard<mutex> lk(outmx);
            if (!(tot > cut())) return;
            if (TOPS.count(sig)) return;
            TOPS[sig] = {tot, {w, s}}; TOPV.insert({tot, sig});
            if ((long)TOPV.size() > K) { auto it = TOPV.begin(); TOPS.erase(it->second); TOPV.erase(it); }
            if ((long)TOPV.size() >= K) gkth.store(TOPV.begin()->first);
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
    if (mode == 2) {
        CLS.resize(1953125);
        FILE *h = fopen(argv[5], "rb"); if (fread(CLS.data(), sizeof(int), CLS.size(), h) != CLS.size()) return 3; fclose(h);
    }
    if (argc > 7 && strcmp(argv[7], "none") != 0) {
        QX.resize(31250); PQ.resize(125); MK.resize(31250);
        FILE *lf = fopen(argv[7], "rb");
        if (fread(QX.data(), sizeof(double), 31250, lf) != 31250 || fread(PQ.data(), sizeof(double), 125, lf) != 125 || fread(MK.data(), sizeof(double), 31250, lf) != 31250) return 4;
        fclose(lf); L3 = true;
        for (double v : QX) if (v > 1e-15) return 5;
        for (double v : PQ) if (v < -1e-15) return 6;
    }
    if (argc > 8 && strcmp(argv[8], "none") != 0) {
        ZT.resize(2 * 1953125);
        FILE *zf = fopen(argv[8], "rb"); if (!zf || fread(ZT.data(), sizeof(double), ZT.size(), zf) != ZT.size()) return 10;
        fclose(zf); FY2 = true;
    }
    if (argc > 9 && strcmp(argv[9], "none") != 0) {
        QX8.resize(31250); PQ8.resize(125); MK8.resize(31250);
        FILE *lf = fopen(argv[9], "rb");
        if (!lf || fread(QX8.data(), sizeof(double), 31250, lf) != 31250 || fread(PQ8.data(), sizeof(double), 125, lf) != 125 || fread(MK8.data(), sizeof(double), 31250, lf) != 31250) return 11;
        fclose(lf); L3V = true;
        for (double v : QX8) if (v > 1e-15) return 12;
        for (double v : PQ8) if (v < -1e-15) return 13;
    }
    if (argc > 6 && strcmp(argv[6], "none") != 0) { FILE *bf = fopen(argv[6], "r"); char buf[64]; double v; while (fscanf(bf, "%63s %lf", buf, &v) == 2) BONUS[buf] = v; fclose(bf); }
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
    } else if (mode == 2) {
        for (auto it = TOPV.rbegin(); it != TOPV.rend(); ++it) { auto &e = TOPS[it->second]; printf("V %.12f %s %s\n", e.first, e.second.first.c_str(), e.second.second.c_str()); }
        printf("END %ld %ld\n", (long)TOPV.size(), nodes);
    } else printf("END %ld %ld\n", found.load(), nodes);
    return 0;
}
