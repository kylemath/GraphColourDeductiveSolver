// s86 p1r copy: jsepf_gk.cpp with the 7802 (payer-7 generic keys) header limit raised from 64 to 192 keys; nothing else changed.
//   (Mode-2 ids 1800000100 + k, k < 192, stay below the 7804 ids 1800000300 + k.)  Built: c++ -O3 -march=native -std=c++17 -pthread
// s85_edge56 (Opus): optional argv[15] = generic-key payee file (eng/edge56.py gkin_write, flag gkleaf), d = 7 only: int32 7804, int32 nk;
//   per key double amount >= 0, int32 payer-letter mask um (bit 0 = 5, 1 = 6, 2 = 7), int32 ncond, ncond x (int32 pos 0..9, int32 mask) in
//   KEYSPEC IN-slot order (S.L+1, S.L+2, S.L+3, S.L-1, S.L-2, S.L-3, S.A+1, S.A-1, R.L+2, R.L-2); then double UBW[5^9] = sum over the keys of
//   amount x (window bound of the key's IN slots, both chiralities), window centred at the payer (index as WIN; the Python side added UBW to
//   WIN).  Leaf: the exact payee credit (privates: 6 = KM & ~f2b extra6, 7 = l3q mask & ~f2b extra7, as K*) minus UBW at every link position
//   (every term <= 0; exit 97 if an exact credit is above its bound).
// s78_kstar (Team D): optional argv[13] = K* file (W6 round 3 deep key K* = EDGE(7->7)[S.L+1=B S.L-1=S S.L-2=5 S.L-3=5 S.A-1=B]), d = 7 only.
//   File (little endian): int32 7801; int32 d (= 7); double aK (K* amount, >= 0); uint8 KUB[2][5^9] (0/1, window index as WIN).
//   KUB[0][widx(k)] = 1 iff the window centred at k holds an upper bound of a K* payee slot with the payer at k-1 (c- = w_k, c+ = w_{k-2});
//   KUB[1][widx(k)] likewise with the payer at k+1 (c- = w_k, c+ = w_{k+2}).  The Python side added aK * (KUB[0] + KUB[1]) to WIN.
//   Leaf (after q7m, before EVAL): exact payer outflow -aK per firing (window-local, <= 0) and, per window k and side, aK * (exact - KUB) <= 0,
//   exact = the payee slot with the masks amask & ~extra6 (6-private = S.A-1 when c- = 6) and L3T & ~extra7 (payer private = S.L-3).
//   exact > KUB would be a positive term outside WIN: refused (exit 81).  Mode-2 ids: 1800000001 per payer firing, 1800000002 per payee firing.
//   Requires argv[7] (l3q file: MK) and argv[10] (f2b file: KM, R6B, R7B).
//   nc rebase (17:45Z): every K* leaf term is <= 0 (aK >= 0 refused otherwise, exact <= KUB enforced), so K* adds nothing to the nc SLACK;
//   the K* block sits after the f2b / q7m corrections and exits on the plain cut.
// s78 generic EDGE keys (19:00Z): optional argv[14] = edge file (eng/edgefam.py eg_write): int32 7802, int32 nkeys; per key double amount >= 0,
//   int32 payee-letter mask, int32 ncond, ncond x (int32 kind, int32 off, int32 mask).  d = 7 leaf: the centre's exact payer outflow, -amount
//   per (i, e) match (<= 0, plain cut, no slack); the payee credit is a window bound already in WIN (no leaf term).  Mode-2 id 1800000100+key.
// jsepf (s60_f2b): jsep7 + argv[10] = f2b file (outside team's full-wheel 2-ball private-letter exclusions), optional argv[11] = eval file.
//   f2b file (little endian), per degree d in 7..9: int32 d; uint8 KM[5^8] (allowed-private mask of a 6 spoke, 31 & ~kill6[U], index
//   (w-2,w-1,w+1,w+2,s-2,s-1,s0,s+1)); double V6M[625*4*32] (M value of the 6 spoke at (b,e,q,r,ca,cf,mask), 0 if no allowed key);
//   double QM[5*5*32] (payee Qeff(c,a,mask) of the d's l3q family, index (c*5+a)*32+mask); then buckets (uint32 count, count x 3 uint64 fw,fs,kill):
//   25 for R6B[(s-1)*5+s0], then 2 x 25 for R7B[sg][(s-1)*5+s0] (sg 0 = +1, 1 = -1). Rule fires at spoke i iff ((rw & fw) | (rs & fs)) == 0.
//   Leaf corrections (all <= 0, clamped, counted): link 6 spoke: V6M[mask & ~extra] - V6M[mask]; link 7 payee side (d = 7 with argv[7], d = 8 with argv[9]): QM[c][a][m & ~extra] - QM[c][a][m].
//   eval file (argv[11]): lines "w s" (letters 5..9 as digits), prints "E total" with every correction and no pruning (self-test).
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
double SLACK = 0, SLACKT = 0; long f2bPos = 0, qmPos = 0;   // nc: positive-correction slack (no clamp)
int d; double thr; long K; int mode; int SYM = 1; int NT = 1;
vector<double> WIN; vector<int> CLS; map<vector<int>, pair<double,pair<string,string>>> TOPS; multimap<double, vector<int>> TOPV; atomic<double> gkth(NEG);            // 5^9, index a,b,c,e,f,p,q,r,s
vector<double> H;              // 5^7, index b,c,e,f,q,r,s  (max over a, p)
vector<double> QX, PQ, MK; bool L3 = false;
vector<double> ZT; bool FY2 = false;
vector<double> QX8, PQ8, MK8; bool L3V = false;
struct F2BRule { uint64_t fw, fs, kill; };
bool F2B = false; vector<uint8_t> KM; vector<double> V6M; vector<double> QMT; vector<F2BRule> R6B[25], R7B[2][25];
atomic<long> f2bHits(0), f2bClamp(0); bool EVAL = false;
bool KS = false; double KSA = 0; vector<uint8_t> KUB; atomic<long> ksPay(0), ksRecv(0), ksUB(0);   // s78 K*
struct EgCond { int kind, off, mask; }; struct EgKey { double amt; int vm; vector<EgCond> cond; };   // s78 generic EDGE payer side (argv[14])
bool EGON = false; vector<EgKey> EGK; atomic<long> egPay(0);
struct GkIn { double amt; int um; vector<pair<int,int>> cond; }; bool GKION = false; vector<GkIn> GKI; vector<double> UBW; atomic<long> gkInHits(0), gkInUB(0);   // s85
bool F2B7 = false;   // s86: env JSEPF_F2B7=1
vector<double> QTM; bool QM = false; atomic<long> qmHits(0), qmClamp(0);   // s67 q7m: argv[12] = QT[625][32][32] for this d (masked payer credit); QM_ = leaf correction QT[m1,m2] - QT[31,31] <= 0
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

struct Ctx;
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
    uint64_t f2bExtra(const vector<F2BRule> &bk, int i) const {
        i = ((i % d) + d) % d;   // s85: callers pass k - 1 = -1 (K* payer j = k - e1, gkin neighbour priv(j - 1)); (i + off) % d was then -1 at off = 0 (read before L)
        uint64_t rw = 0, rs = 0;
        for (int off = 0; off < d; off++) { int p = (i + off) % d; rw |= 1ULL << (5 * off + L[2 * p]); rs |= 1ULL << (5 * off + L[2 * p + 1]); }
        uint64_t ex = 0;
        for (const auto &r : bk) if (((rw & r.fw) | (rs & r.fs)) == 0) ex |= r.kill;
        return ex;
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
        double c = EVAL ? NEG : cut();
        if (!(tot > c - SLACK)) return;
        if (!EVAL && (d == 7 || d == 8) && RBIG.count(canonlink())) return;
        vector<int> l3ids;
        if (!BONUS.empty()) { string cl = canonlink(); auto it = BONUS.find(cl); if (it != BONUS.end()) { tot -= it->second; if (!(tot > c - SLACK)) return; unsigned h = 2166136261u; for (char ch : cl) h = (h ^ (unsigned char)ch) * 16777619u; l3ids.push_back(1700000000 + (int)(h % 400000000u)); } }
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
            tot += corr; if (!(tot > c - SLACK)) return;
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
            tot += corr; if (!(tot > c - SLACK)) return;
        }
        if (F2B) {
            double dl = 0;
            for (int i = 0; i < d; i++) {
                int sm1 = S(i - 1), s0 = S(i);
                if (W(i) == 1) {
                    const auto &bk = R6B[sm1 * 5 + s0]; if (bk.empty()) continue;
                    uint64_t ex = f2bExtra(bk, i); if (!ex) continue;
                    int a = W(i - 2), b = W(i - 1), e = W(i + 1), f = W(i + 2), p0 = S(i - 2), s3 = S(i + 1);
                    long k8 = ((((((((long)a * 5 + b) * 5 + e) * 5 + f) * 5 + p0) * 5 + sm1) * 5 + s0) * 5 + s3);
                    int m0 = KM[k8]; if (!(m0 & ex)) continue;
                    int mk = m0 & ~(int)ex;
                    long ix = ((((((long)b * 5 + e) * 5 + sm1) * 5 + s0) * 4) + (a >= 2 ? 2 : 0) + (f >= 2 ? 1 : 0)) * 32;
                    double v = V6M[ix + mk] - V6M[ix + m0];
                    if (v > 1e-15) { f2bClamp++; f2bPos++; }
                    dl += v; f2bHits++; l3ids.push_back(1400000000 + widx(i) * 32 + mk);
                } else if (W(i) == 2 && (d == 7 || d == 8)) {
                    for (int sg = 0; sg < 2; sg++) {
                        int e1 = sg == 0 ? 1 : -1;
                        int cc = W(i + e1), a = sg == 0 ? s0 : sm1, o = sg == 0 ? sm1 : s0;
                        if (cc > 1 || a > 1) continue;
                        const auto &bk = R7B[sg][sm1 * 5 + s0]; if (bk.empty()) continue;
                        uint64_t ex = f2bExtra(bk, i); if (!ex) continue;
                        long q = (((((long)sg * 5 + cc) * 5 + W(i + 2 * e1)) * 5 + W(i + 3 * e1)) * 5 + W(i + 4 * e1)) * 25 + a * 5 + o;
                        double mkv = d == 7 ? (L3 ? MK[q] : -1) : (L3V ? MK8[q] : -1);
                        if (mkv < 0) { fprintf(stderr, "f2b: l3q mask table missing at d=%d\n", d); exit(70); }
                        int m0 = (int)mkv; if (!(m0 & ex)) continue;
                        int mk = m0 & ~(int)ex;
                        double v = QMT[(cc * 5 + a) * 32 + mk] - QMT[(cc * 5 + a) * 32 + m0];
                        if (v > 1e-15) { f2bClamp++; f2bPos++; }
                        dl += v; f2bHits++; l3ids.push_back(1500000000 + (cc * 5 + a) * 32 + mk);
                    }
                }
            }
            tot += dl; if (!(tot > c - SLACKT)) return;
        }
        if (QM && (d == 7 || d == 8)) {   // s67 q7m: payer credit Q(sig, masks) <= Q(sig) already in the window; exact masks = L3T/V8 mask & ~f2b extra7 on each side
            double dq = 0;
            for (int i = 0; i < d; i++) {
                if (W(i) != 2) continue;
                int sm1 = S(i - 1), s0 = S(i); int m[2] = {31, 31};
                for (int sg = 0; sg < 2; sg++) {
                    int e1 = sg == 0 ? 1 : -1;
                    int cc = W(i + e1), a = sg == 0 ? s0 : sm1, o = sg == 0 ? sm1 : s0;
                    if (cc > 1 || a > 1) {   // s86 f2b7: a 7-side has no L3T mask; with JSEPF_F2B7 the f2b d7_w7/d8_w7 rules still remove letters
                        if (F2B7 && F2B) { const auto &bk = R7B[sg][sm1 * 5 + s0]; if (!bk.empty()) m[sg] = 31 & ~(int)f2bExtra(bk, i); }
                        continue;
                    }
                    long q = (((((long)sg * 5 + cc) * 5 + W(i + 2 * e1)) * 5 + W(i + 3 * e1)) * 5 + W(i + 4 * e1)) * 25 + a * 5 + o;
                    double mkv = d == 7 ? (L3 ? MK[q] : -1) : (L3V ? MK8[q] : -1);
                    if (mkv < 0) { fprintf(stderr, "q7m: l3q mask table missing at d=%d\n", d); exit(71); }
                    uint64_t ex = 0; if (F2B) { const auto &bk = R7B[sg][sm1 * 5 + s0]; if (!bk.empty()) ex = f2bExtra(bk, i); }
                    m[sg] = (int)mkv & ~(int)ex;
                }
                if (m[0] == 31 && m[1] == 31) continue;
                long ix = (((long)(W(i - 1) * 5 + W(i + 1)) * 5 + sm1) * 5 + s0) * 1024;
                double v = QTM[ix + m[0] * 32 + m[1]] - QTM[ix + 31 * 32 + 31];
                if (v > 1e-15) { qmClamp++; qmPos++; }
                dq += v; qmHits++; l3ids.push_back(1600000000 + (int)(ix + m[0] * 32 + m[1]));
            }
            tot += dq; if (!(tot > c)) return;
        }
        if (KS && d == 7) {   // s78 K*: exact payer outflow + exact payee credit minus the window upper bound (every term <= 0)
            double dk = 0;
            for (int i = 0; i < d; i++) {   // centre pays its link 7 at i; c- = w_{i+e1}, c+ = w_{i-e1}, S.L-2 = w_{i+2e1}, S.L-3 = w_{i+3e1}, S.A-1 = apex(i+e1, i+2e1)
                if (W(i) != 2) continue;
                for (int e1 = 1; e1 >= -1; e1 -= 2)
                    if (W(i - e1) >= 2 && W(i + e1) <= 1 && W(i + 2 * e1) == 0 && W(i + 3 * e1) == 0 && (e1 > 0 ? S(i + 1) : S(i - 2)) >= 2) {
                        dk -= KSA; ksPay++; l3ids.push_back(1800000001);
                    }
            }
            for (int k = 0; k < d; k++) {   // centre is paid by its link 7 at j = k - e1; c- = w_k
                const long ix = widx(k);
                for (int sgi = 0; sgi < 2; sgi++) {
                    const int e1 = sgi == 0 ? 1 : -1, j = k - e1;
                    const int ub = KUB[(size_t)sgi * 1953125 + ix];
                    int ex = 0;
                    const int a = e1 > 0 ? S(j) : S(j - 1), o = e1 > 0 ? S(j - 1) : S(j);   // a = apex(j, k) = S.L-2, o = j's other apex
                    if (W(j) == 2 && W(j - e1) >= 2 && W(k) <= 1 && a == 0) {
                        bool sa;
                        if (W(k) == 0) sa = (e1 > 0 ? S(k) : S(k - 1)) >= 2;          // c- = 5: S.A-1 = c-'s other apex
                        else {                                                          // c- = 6: S.A-1 = the 6's private
                            long k8 = ((((((((long)W(k - 2) * 5 + W(k - 1)) * 5 + W(k + 1)) * 5 + W(k + 2)) * 5 + S(k - 2)) * 5 + S(k - 1)) * 5 + S(k)) * 5 + S(k + 1));
                            int m6 = KM[k8]; const auto &bk6 = R6B[S(k - 1) * 5 + S(k)];
                            if (!bk6.empty()) m6 &= ~(int)f2bExtra(bk6, k);
                            sa = (m6 & 28) != 0;
                        }
                        long q = (((((long)sgi * 5 + W(j + e1)) * 5 + W(j + 2 * e1)) * 5 + W(j + 3 * e1)) * 5 + W(j + 4 * e1)) * 25 + a * 5 + o;
                        if (MK[q] < 0) { fprintf(stderr, "kstar: l3q mask missing at q=%ld\n", q); exit(82); }
                        int m7 = (int)MK[q]; const auto &bk7 = R7B[sgi][S(j - 1) * 5 + S(j)];
                        if (!bk7.empty()) m7 &= ~(int)f2bExtra(bk7, j);
                        ex = (sa && (m7 & 1)) ? 1 : 0;                                    // S.L-3 = 5 possible
                    }
                    if (ex > ub) { fprintf(stderr, "kstar: exact payee slot above the window bound at k=%d sg=%d (window %ld)\n", k, e1, ix); exit(81); }
                    if (ub) { dk += KSA * (ex - ub); ksUB++; }
                    if (ex) { ksRecv++; l3ids.push_back(1800000002); }
                }
            }
            tot += dk; if (!(tot > c)) return;
        }
        if (EGON && d == 7) {   // s78 generic EDGE keys: exact payer outflow of the d = 7 centre (every term <= 0); payee credit is in WIN
            double dg = 0;
            for (size_t kk = 0; kk < EGK.size(); kk++) {
                const EgKey &K = EGK[kk]; if (K.amt == 0) continue;
                for (int i = 0; i < d; i++) {
                    if (!((K.vm >> W(i)) & 1)) continue;
                    for (int e = 1; e >= -1; e -= 2) {
                        bool ok = true;
                        for (const EgCond &q : K.cond) {   // kind 0: w_{i+off e}; kind 1: apex between orientation offsets off, off+1
                            const int L = q.kind == 0 ? W(i + q.off * e) : (e > 0 ? S(i + q.off) : S(i - q.off - 1));
                            if (!((q.mask >> L) & 1)) { ok = false; break; }
                        }
                        if (ok) { dg -= K.amt; egPay++; l3ids.push_back(1800000100 + (int)kk); }
                    }
                }
            }
            tot += dg; if (!(tot > c)) return;
        }
        if (GKION && d == 7) {   // s85 generic keys, payee side: exact credit minus the window bound UBW (every term <= 0)
            auto priv = [&](int k, int side) -> int {   // W(k)'s vertex beyond its apex, seen from the centre: side 0 next to S(k-1), side 1 next to S(k)
                const int x = W(k);
                if (x == 0) return side == 0 ? (1 << S(k)) : (1 << S(k - 1));   // a 5: the other apex
                if (x == 1) {
                    long k8 = ((((((((long)W(k - 2) * 5 + W(k - 1)) * 5 + W(k + 1)) * 5 + W(k + 2)) * 5 + S(k - 2)) * 5 + S(k - 1)) * 5 + S(k)) * 5 + S(k + 1));
                    int m6 = KM[k8]; const auto &bk6 = R6B[S(k - 1) * 5 + S(k)];
                    if (!bk6.empty()) m6 &= ~(int)f2bExtra(bk6, k);
                    return m6;
                }
                if (x == 2) {
                    const int sgi = side == 1 ? 0 : 1, e1 = side == 1 ? 1 : -1;
                    const int cc = W(k + e1), a = side == 1 ? S(k) : S(k - 1), o = side == 1 ? S(k - 1) : S(k);
                    if (cc > 1 || a > 1) return 31;
                    long q = (((((long)sgi * 5 + cc) * 5 + W(k + 2 * e1)) * 5 + W(k + 3 * e1)) * 5 + W(k + 4 * e1)) * 25 + a * 5 + o;
                    if (MK[q] < 0) { fprintf(stderr, "gkin: l3q mask missing at q=%ld\n", q); exit(98); }
                    int m7 = (int)MK[q]; const auto &bk7 = R7B[sgi][S(k - 1) * 5 + S(k)];
                    if (!bk7.empty()) m7 &= ~(int)f2bExtra(bk7, k);
                    return m7;
                }
                return 31;
            };
            double dg = 0;
            for (int j = 0; j < d; j++) {
                const long ix = widx(j); const double ub = UBW[ix]; const int u = W(j);
                double ex = 0;
                if (u <= 2) {
                    const int wm1 = 1 << W(j - 1), wp1 = 1 << W(j + 1), wm2 = 1 << W(j - 2), wp2 = 1 << W(j + 2), am1 = 1 << S(j - 1), a0 = 1 << S(j);
                    const int p0 = priv(j, 0), p1 = priv(j, 1), qm = priv(j - 1, 1), qp = priv(j + 1, 0);
                    const int V[2][10] = {{wm1, am1, p0, wp1, a0, p1, qm, qp, wm2, wp2}, {wp1, a0, p1, wm1, am1, p0, qp, qm, wp2, wm2}};
                    for (size_t kk = 0; kk < GKI.size(); kk++) {
                        const GkIn &K = GKI[kk]; if (K.amt == 0 || !((K.um >> u) & 1)) continue;
                        for (int sg = 0; sg < 2; sg++) {
                            bool ok = true;
                            for (const auto &pc : K.cond) if (!(V[sg][pc.first] & pc.second)) { ok = false; break; }
                            if (ok) { ex += K.amt; gkInHits++; l3ids.push_back(1800000300 + (int)kk); }
                        }
                    }
                }
                if (EVAL && getenv("GKDBG")) fprintf(stderr, "jsepf GKDBG j=%d u=%d ex=%.12f ub=%.12f\n", j, u, ex, ub);
                if (ex > ub + 1e-9) { fprintf(stderr, "gkin: exact payee credit %.12g above the window bound %.12g at j=%d (window %ld)\n", ex, ub, j, ix); exit(97); }
                if (ub != 0) { dg += ex - ub; gkInUB++; }
            }
            tot += dg; if (!(tot > c)) return;
        }
        if (EVAL) { printf("E %.12f\n", tot); return; }
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
                        if (bnd + SLACK <= cut() + (mode == 1 ? 1e-12 : -1e-12)) ok = false;   // mode 1: ties cannot raise the max
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
    F2B7 = getenv("JSEPF_F2B7") && getenv("JSEPF_F2B7")[0] == '1';
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
    if (argc > 10 && strcmp(argv[10], "none") != 0) {
        FILE *g = fopen(argv[10], "rb"); if (!g) return 60;
        int32_t dd; if (fread(&dd, 4, 1, g) != 1 || dd != d) { fprintf(stderr, "f2b file is for d=%d, run d=%d\n", dd, d); return 61; }
        KM.resize(390625); V6M.resize(625 * 4 * 32); QMT.resize(800);
        if (fread(KM.data(), 1, KM.size(), g) != KM.size()) return 62;
        if (fread(V6M.data(), sizeof(double), V6M.size(), g) != V6M.size()) return 63;
        if (fread(QMT.data(), sizeof(double), 800, g) != 800) return 64;
        auto rd = [&](vector<F2BRule> &v) { uint32_t cnt = 0; if (fread(&cnt, 4, 1, g) != 1) exit(65); v.resize(cnt); if (cnt && fread(v.data(), sizeof(F2BRule), cnt, g) != cnt) exit(66); return (long)cnt; };
        long nr = 0;
        for (int b = 0; b < 25; b++) nr += rd(R6B[b]);
        for (int sg = 0; sg < 2; sg++) for (int b = 0; b < 25; b++) nr += rd(R7B[sg][b]);
        fclose(g); F2B = true; fprintf(stderr, "jsepf: f2b tables loaded for d=%d, %ld bucketed rule entries\n", d, nr);
    }
    claimed = new vector<atomic<int>>(3125);
    for (auto &c : *claimed) c = 0;
    T0 = chrono::steady_clock::now();
    if (argc > 12 && strcmp(argv[12], "none") != 0) {
        FILE *qf = fopen(argv[12], "rb"); if (!qf) return 72; QTM.resize(625 * 1024);
        if (fread(QTM.data(), sizeof(double), QTM.size(), qf) != QTM.size()) return 73; fclose(qf); QM = true;
        fprintf(stderr, "jsepf: q7m table loaded for d=%d%s\n", d, F2B7 ? " (f2b7: 7-side masks on)" : "");
    }
    {   // nc: largest positive leaf correction per kind -> slack
        double dV = 0, dQ = 0, dT = 0;
        if (F2B) {
            for (int ix = 0; ix < 625 * 4; ix++) for (int m = 0; m < 32; m++) for (int sb = m; ; sb = (sb - 1) & m) { dV = max(dV, V6M[ix * 32 + sb] - V6M[ix * 32 + m]); if (!sb) break; }
            for (int ix = 0; ix < 25; ix++) for (int m = 0; m < 32; m++) for (int sb = m; ; sb = (sb - 1) & m) { dQ = max(dQ, QMT[ix * 32 + sb] - QMT[ix * 32 + m]); if (!sb) break; }
        }
        if (QM) for (int ix = 0; ix < 625; ix++) for (int m = 0; m < 1024; m++) dT = max(dT, QTM[ix * 1024 + m] - QTM[ix * 1024 + 1023]);
        SLACKT = d * dT + (dT > 0 ? 1e-12 : 0); SLACK = d * dV + 2 * d * dQ + SLACKT + ((dV > 0 || dQ > 0) ? 1e-12 : 0);
        fprintf(stderr, "jsepf_nc: max positive deltas V6M %.6g QM %.6g QT %.6g -> slack %.6g (q7m slack %.6g)\n", dV, dQ, dT, SLACK, SLACKT);
    }
    if (argc > 13 && strcmp(argv[13], "none") != 0) {   // s78 K*
        FILE *kf = fopen(argv[13], "rb"); if (!kf) return 83;
        int32_t mg = 0, dd = 0;
        if (fread(&mg, 4, 1, kf) != 1 || mg != 7801 || fread(&dd, 4, 1, kf) != 1 || dd != d) { fprintf(stderr, "kstar file: bad magic or d\n"); return 84; }
        if (fread(&KSA, sizeof(double), 1, kf) != 1) return 85;
        KUB.resize((size_t)2 * 1953125); if (fread(KUB.data(), 1, KUB.size(), kf) != KUB.size()) return 86;
        fclose(kf);
        if (!(KSA >= 0) || KSA > 1e6) { fprintf(stderr, "kstar: amount %g refused (must be >= 0)\n", KSA); return 87; }
        for (uint8_t u : KUB) if (u > 1) return 88;
        if (d != 7) { fprintf(stderr, "kstar file passed at d=%d (d = 7 only)\n", d); return 89; }
        if (!L3 || !F2B) { fprintf(stderr, "kstar needs the l3q file (argv[7]) and the f2b file (argv[10])\n"); return 90; }
        KS = true; fprintf(stderr, "jsepf: kstar table loaded, aK = %.12g\n", KSA);
    }
    if (argc > 14 && strcmp(argv[14], "none") != 0) {   // s78 generic EDGE keys (payer side, d = 7)
        FILE *gf = fopen(argv[14], "rb"); if (!gf) return 91;
        int32_t mg = 0, nk = 0; if (fread(&mg, 4, 1, gf) != 1 || mg != 7802 || fread(&nk, 4, 1, gf) != 1 || nk < 0 || nk > 192) { fprintf(stderr, "edge file: bad header\n"); return 92; }
        for (int kk = 0; kk < nk; kk++) {
            EgKey K; int32_t vm, nc; if (fread(&K.amt, sizeof(double), 1, gf) != 1 || fread(&vm, 4, 1, gf) != 1 || fread(&nc, 4, 1, gf) != 1 || nc < 0 || nc > 16) return 93;
            if (!(K.amt >= 0) || K.amt > 1e6) { fprintf(stderr, "edge: amount %g refused (must be >= 0)\n", K.amt); return 94; }
            K.vm = vm; for (int q = 0; q < nc; q++) { int32_t a3[3]; if (fread(a3, 4, 3, gf) != 3 || a3[0] < 0 || a3[0] > 1 || a3[1] < -3 || a3[1] > 3) return 95; K.cond.push_back({a3[0], a3[1], a3[2]}); }
            EGK.push_back(K);
        }
        fclose(gf);
        if (d != 7) { fprintf(stderr, "edge file passed at d=%d (d = 7 only)\n", d); return 96; }
        EGON = true; fprintf(stderr, "jsepf: edge keys loaded: %d\n", nk);
    }
    if (argc > 15 && strcmp(argv[15], "none") != 0) {   // s85 generic keys, payee side (d = 7)
        FILE *gf = fopen(argv[15], "rb"); if (!gf) return 101;
        int32_t mg = 0, nk = 0; if (fread(&mg, 4, 1, gf) != 1 || mg != 7804 || fread(&nk, 4, 1, gf) != 1 || nk < 0 || nk > 4096) { fprintf(stderr, "gkin file: bad header\n"); return 102; }
        for (int kk = 0; kk < nk; kk++) {
            GkIn K; int32_t um, nc; if (fread(&K.amt, sizeof(double), 1, gf) != 1 || fread(&um, 4, 1, gf) != 1 || fread(&nc, 4, 1, gf) != 1 || nc < 0 || nc > 10) return 103;
            if (!(K.amt >= 0) || K.amt > 1e6) { fprintf(stderr, "gkin: amount %g refused (must be >= 0)\n", K.amt); return 104; }
            if (um <= 0 || um > 7) { fprintf(stderr, "gkin: payer mask %d refused (letters 5, 6, 7 only)\n", um); return 105; }
            K.um = um; for (int q = 0; q < nc; q++) { int32_t a2[2]; if (fread(a2, 4, 2, gf) != 2 || a2[0] < 0 || a2[0] > 9 || a2[1] <= 0 || a2[1] >= 31) return 106; K.cond.push_back({a2[0], a2[1]}); }
            GKI.push_back(K);
        }
        UBW.resize(1953125); if (fread(UBW.data(), sizeof(double), UBW.size(), gf) != UBW.size()) return 107;
        fclose(gf);
        if (d != 7) { fprintf(stderr, "gkin file passed at d=%d (d = 7 only)\n", d); return 108; }
        if (!L3 || !F2B) { fprintf(stderr, "gkin needs the l3q file (argv[7]) and the f2b file (argv[10])\n"); return 109; }
        for (double v : UBW) if (!(v >= 0)) { fprintf(stderr, "gkin: negative window bound\n"); return 110; }
        GKION = true; fprintf(stderr, "jsepf: gkin payee keys loaded: %d\n", nk);
    }
    if (argc > 11 && strcmp(argv[11], "none") != 0) {
        EVAL = true; Ctx c0; FILE *ef = fopen(argv[11], "r"); char wb[64], sb[64];
        while (ef && fscanf(ef, "%63s %63s", wb, sb) == 2) { for (int i = 0; i < d; i++) { c0.L[2 * i] = wb[i] - '5'; c0.L[2 * i + 1] = sb[i] - '5'; } c0.leaf(); }
        return 0;
    }
    vector<Ctx> C(NT); vector<thread> th;
    for (int t = 0; t < NT; t++) th.emplace_back([&, t] { C[t].rec(0); totnodes += C[t].nodes; });
    for (auto &x : th) x.join();
    long nodes = totnodes;
    if (QM) fprintf(stderr, "jsepf: q7m leaf hits %ld, clamped %ld\n", qmHits.load(), qmClamp.load());
    if (EGON) fprintf(stderr, "jsepf: edge leaf payer firings %ld\n", egPay.load());
    if (GKION) fprintf(stderr, "jsepf: gkin leaf exact payee firings %ld, window bounds corrected %ld\n", gkInHits.load(), gkInUB.load());
    if (KS) fprintf(stderr, "jsepf: kstar leaf payer firings %ld, payee firings %ld, window bounds corrected %ld\n", ksPay.load(), ksRecv.load(), ksUB.load());
    fprintf(stderr, "jsepf_nc: positive corrections kept (not clamped): f2b %ld, q7m %ld\n", f2bPos, qmPos);
    if (F2B) fprintf(stderr, "jsepf: f2b leaf hits %ld, clamped %ld\n", f2bHits.load(), f2bClamp.load());
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
