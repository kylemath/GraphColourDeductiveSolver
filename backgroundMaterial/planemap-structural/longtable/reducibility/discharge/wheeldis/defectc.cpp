// defectc.cpp -- README §7, test G (exploratory): C++ port of defect.py's ring DFS for isolated positive defects.
// Disc around a centre (degree C0), ring k vertices get degrees in {5,6,7} for k < K, ring K and later all 6.
// A vertex is rejected as soon as its link is complete and its wheel is in R_opt (tables from defect_tables.py).
// Output: one line per leaf with charge >= CMIN: "c=<c> sig=<ring0>|<ring1>|...|<ringK>".
// Build: g++ -O2 -o bin/defectc defectc.cpp      Usage: bin/defectc TABLES C0 K CMIN [MAXLEAVES] [MAXRING]
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
static vector<char> bad5, bad6, d7, t7;
static vector<char> feas[8];   // feas[d][pattern base 4: 0,1,2 = 5,6,7, 3 = unknown]: some completion is not bad
static long npruned = 0;
static int C0, K, CMIN; static long MAXLEAVES = 1000000000L, leaves = 0, nodes = 0; static int MAXRING = 60;
struct Ring { int a; vector<int> deg; vector<vector<int>> inb, outb; };
static vector<Ring> R;
static int encode(const vector<int>& w) { int x = 0; for (int d : w) x = x * 3 + (d - 5); return x; }
static void build_feas() {
    for (int d = 5; d <= 7; d++) {
        int n = 1; for (int i = 0; i < d; i++) n *= 4;
        feas[d].assign(n, 0);
        vector<char>& B = d == 5 ? bad5 : d == 6 ? bad6 : d7;
        for (int x = 0; x < n; x++) {
            int dig[8], y = x; for (int i = d - 1; i >= 0; i--) { dig[i] = y % 4; y /= 4; }
            int nu = 0; for (int i = 0; i < d; i++) if (dig[i] == 3) nu++;
            int m = 1; for (int i = 0; i < nu; i++) m *= 3; bool ok = false;
            for (int c = 0; c < m && !ok; c++) {
                int cc = c, code = 0;
                for (int i = 0; i < d; i++) { int v = dig[i]; if (v == 3) { v = cc % 3; cc /= 3; } code = code * 3 + v; }
                if (!B[code]) ok = true;
            }
            feas[d][x] = ok;
        }
    }
}
// letters 5,6,7 known, 0 = unknown
static bool feasible(int deg, const vector<int>& w) {
    if (deg < 5 || deg > 7) return false;
    int x = 0; for (int d : w) x = x * 4 + (d == 0 ? 3 : d - 5);
    return feas[deg][x];
}
static void linkword(int k, int j, vector<int>& w) {
    w.clear();
    if (k == 0) { for (int i = 0; i < R[1].a; i++) w.push_back(R[1].deg[i]); return; }
    Ring& r = R[k]; int a = r.a;
    w.push_back(r.deg[(j - 1 + a) % a]);
    if (k == 1) w.push_back(C0); else for (int p : r.inb[j]) w.push_back(R[k - 1].deg[p]);
    w.push_back(r.deg[(j + 1) % a]);
    const vector<int>& ob = r.outb[j];
    for (int i = (int)ob.size() - 1; i >= 0; i--) w.push_back(R[k + 1].deg[ob[i]]);
}
static bool badw(int deg, const vector<int>& w) {
    for (int d : w) if (d < 5 || d > 7) return true;
    if ((int)w.size() != deg) return true;
    int x = encode(w);
    if (deg == 5) return bad5[x]; if (deg == 6) return bad6[x]; if (deg == 7) return d7[x];
    return true;
}
// build ring k+1 structure from ring k degrees; false if impossible
static bool grow(int k) {
    Ring& r = R[k]; int a = r.a; vector<int> out(a); int b = 0;
    for (int j = 0; j < a; j++) {
        int in = (k == 0) ? 0 : (k == 1 ? 1 : (int)r.inb[j].size());
        out[j] = r.deg[j] - in - 2; if (out[j] < 1) return false; b += out[j] - 1;
    }
    if (k == 0) { return true; }
    if (b < 3 || b > MAXRING) return false;
    if ((int)R.size() <= k + 1) R.resize(k + 2);
    Ring& z = R[k + 1]; z.a = b; z.deg.assign(b, 0); z.inb.assign(b, {}); z.outb.assign(b, {});
    r.outb.assign(a, {}); int t = 0;
    for (int j = 0; j < a; j++) {
        for (int i = 0; i < out[j]; i++) { int q = (t + i) % b; r.outb[j].push_back(q); z.inb[q].push_back(j); }
        t += out[j] - 1;
    }
    // cyclic order of Z[0]'s in-block: R[a-1] first
    vector<int>& i0 = z.inb[0];
    if (find(i0.begin(), i0.end(), a - 1) != i0.end() && i0.size() > 1) {
        vector<int> o; o.push_back(a - 1); for (int x : i0) if (x != a - 1) o.push_back(x); i0 = o;
    }
    return true;
}
static void emit() {
    int c = 0; for (int k = 0; k < K; k++) for (int d : R[k].deg) c += 6 - d;
    if (c < CMIN) return;
    leaves++;
    printf("c=%d sig=", c);
    for (int k = 0; k <= K; k++) { if (k) putchar('|'); for (int d : R[k].deg) putchar('0' + d); }
    putchar('\n'); fflush(stdout);
}
static void ring_dfs(int k);
static void finish(int k) {
    if (k < K) { if (!grow(k)) return; ring_dfs(k + 1); return; }
    // ring K complete and ring K-1 checked; add all-6 rings and check ring K, then validate growth
    if (!grow(K)) return;
    for (int i = 0; i < R[K + 1].a; i++) R[K + 1].deg[i] = 6;
    vector<int> w;
    for (int j = 0; j < R[K].a; j++) { linkword(K, j, w); if (badw(6, w)) return; }
    for (int e = K + 1; e < K + 4; e++) {
        if (!grow(e)) return;
        for (int i = 0; i < R[e + 1].a; i++) R[e + 1].deg[i] = 6;
    }
    emit();
}
static void ring_dfs(int k) {
    if (leaves >= MAXLEAVES) return;
    Ring& r = R[k]; int a = r.a; Ring& p = R[k - 1];
    vector<vector<int>> done_at(a);
    if (k >= 2) for (int j = 0; j < p.a; j++) {
        const vector<int>& ob = p.outb[j]; int last;
        if (ob.size() > 1 && ob.back() == 0 && ob.front() != 0) last = a - 1;
        else last = *max_element(ob.begin(), ob.end());
        done_at[last].push_back(j);
    }
    vector<vector<int>> ch(a);
    for (int j = 0; j < a; j++) {
        int in = (k == 1) ? 1 : (int)r.inb[j].size(); int lo = in + 3;
        if (k < K) { for (int d = 5; d <= 7; d++) if (d >= lo) ch[j].push_back(d); }
        else if (6 >= lo) ch[j].push_back(6);
    }
    vector<int> w;
    int cfix = 0; for (int kk = 0; kk < k && kk < K; kk++) for (int d : R[kk].deg) cfix += 6 - d;
    // partial word of ring-k vertex j (left/right ring neighbours may be 0 = unknown; out-block unknown unless k+1 >= K)
    auto partial_k = [&](int j, vector<int>& pw) {
        pw.clear(); pw.push_back(r.deg[(j - 1 + a) % a]);
        if (k == 1) pw.push_back(C0); else for (int q : r.inb[j]) pw.push_back(p.deg[q]);
        pw.push_back(r.deg[(j + 1) % a]);
        int in = (k == 1) ? 1 : (int)r.inb[j].size(); int out = r.deg[j] - in - 2;
        for (int i = 0; i < out; i++) pw.push_back(k + 1 >= K ? 6 : 0);
    };
    // partial word of ring-(k-1) vertex j: out-block letters from ring k (0 if not yet assigned)
    auto partial_p = [&](int j, vector<int>& pw) {
        int pa = p.a; pw.clear(); pw.push_back(p.deg[(j - 1 + pa) % pa]);
        if (k - 1 == 1) pw.push_back(C0); else for (int q : p.inb[j]) pw.push_back(R[k - 2].deg[q]);
        pw.push_back(p.deg[(j + 1) % pa]);
        const vector<int>& ob = p.outb[j];
        for (int i = (int)ob.size() - 1; i >= 0; i--) pw.push_back(r.deg[ob[i]]);
    };
    // which ring-(k-1) vertices see position t
    vector<vector<int>> sees(a);
    if (k >= 2) for (int j = 0; j < p.a; j++) for (int q : p.outb[j]) sees[q].push_back(j);
    // iterative DFS over positions
    vector<int> idx(a + 1, -1); int t = 0;
    while (t >= 0) {
        if (leaves >= MAXLEAVES) return;
        if (t == a) { nodes++; finish(k); t--; continue; }
        idx[t]++;
        if (idx[t] >= (int)ch[t].size()) { idx[t] = -1; r.deg[t] = 0; t--; continue; }
        r.deg[t] = ch[t][idx[t]]; nodes++;
        bool ok = true;
        for (int j : done_at[t]) { linkword(k - 1, j, w); if (badw(p.deg[j], w)) { ok = false; break; } }
        if (ok) for (int j : sees[t]) { partial_p(j, w); if (!feasible(p.deg[j], w)) { ok = false; break; } }
        if (ok) { partial_k(t, w); if (!feasible(r.deg[t], w)) ok = false; }
        if (ok && t > 0) { partial_k(t - 1, w); if (!feasible(r.deg[t - 1], w)) ok = false; }
        if (ok && t == a - 1) { partial_k(0, w); if (!feasible(r.deg[0], w)) ok = false; }
        if (ok && k == K - 1) {   // charge bound: remaining ring-(K-1) positions add at most 1 each
            int cp = cfix; for (int i = 0; i <= t; i++) cp += 6 - r.deg[i];
            if (cp + (a - 1 - t) < CMIN) ok = false;
        }
        if (!ok) npruned++;
        if (ok) { t++; if (t < a) idx[t] = -1; }
    }
}
int main(int argc, char** argv) {
    FILE* f = fopen(argv[1], "r"); C0 = atoi(argv[2]); K = atoi(argv[3]); CMIN = atoi(argv[4]);
    if (argc > 5) MAXLEAVES = atol(argv[5]); if (argc > 6) MAXRING = atoi(argv[6]);
    int sz[4] = {243, 729, 2187, 2187}; vector<char>* T[4] = {&bad5, &bad6, &d7, &t7};
    for (int i = 0; i < 4; i++) { T[i]->resize(sz[i]); for (int j = 0; j < sz[i]; j++) { int x; if (fscanf(f, "%d", &x) != 1) return 1; (*T[i])[j] = x; } }
    build_feas();
    R.resize(K + 6);
    R[0].a = 1; R[0].deg = {C0};
    R[1].a = C0; R[1].deg.assign(C0, 0); R[1].inb.assign(C0, {}); R[1].outb.assign(C0, {});
    // ring 1 up to rotation/reflection
    vector<int> w(C0);
    int tot = 1; for (int i = 0; i < C0; i++) tot *= (K > 1 ? 3 : 1);
    for (int code = 0; code < tot; code++) {
        int x = code; for (int i = C0 - 1; i >= 0; i--) { w[i] = (K > 1 ? 5 + x % 3 : 6); x /= 3; }
        // canonical (min over dihedral)
        bool canon = true;
        for (int s = 0; s < 2 && canon; s++) for (int rot = 0; rot < C0; rot++) {
            vector<int> v(C0); for (int i = 0; i < C0; i++) v[i] = s ? w[(rot - i + 2 * C0) % C0] : w[(rot + i) % C0];
            if (v < w) { canon = false; break; }
        }
        if (!canon) continue;
        if (badw(C0, w)) continue;
        R[1].deg = w;
        if (!grow(1)) continue;
        ring_dfs(2);
        if (leaves >= MAXLEAVES) break;
    }
    fprintf(stderr, "centre %d K %d nodes %ld pruned %ld leaves %ld\n", C0, K, nodes, npruned, leaves);
}
