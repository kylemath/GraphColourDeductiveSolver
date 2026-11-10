// W6r RSST-FP9: exact branch-and-bound for u of degree d = 9..14 (RSSTFP_SPEC addendum A).  Tables from d9_export.py.
//   final charge hi = 10(6-d) + #POSSIBLE fits at hubs w_i into u (u never sends at d >= 9); lo = same with SURE fits.
//   kills: RSST configurations (interior injective, exact degrees, induced) in the 2-ball; hosts = u (exact letter d) and every w / s /
//   private with an exact letter 5..8 (9 = 9+ is never a host).  Containment is monotone in the hosts, so a partial assignment that
//   already contains a configuration is killed for every completion.
// search: link words up to rotation + reflection (parts mirror-closed, matcher orientation-free); per word, the apexes and privates in
//   site order, each over its dominance-reduced domain ({9} + the letters 5..8 whose condition pattern differs from 9's: a letter with
//   9's pattern gives the same charge and more hosts, so it can never beat 9).  Bound: 10(6-d) + #fits not yet violated (c+ per link
//   window for unfinished link words).  Modes:
//     max  VARIANT : prune bound <= best (dynamic, start 0) -> exact max over unkilled states if > 0, else certifies max <= 0
//     enum VARIANT : prune bound <= 0; every surviving leaf is a positive state unkilled by VARIANT; leaves are tested against the 51
//                    'none' configurations and classified (killed only by none configs / genuinely positive)
//     eval FILE    : cross-check on xval.txt (hi, lo, contained configurations)
//   VARIANT: none | 582 | 633
// usage: d9bb TABLEDIR D MODE VARIANT [TIMELIMIT_S=3000] [CAP=200000] [START=0]   (max mode: states with hi > START)   |   d9bb TABLEDIR 0 eval XVAL
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 M;
static inline M bit(int i) { return ((M)1) << i; }
static inline int ctz128(M x) { uint64_t lo = (uint64_t)x; return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((uint64_t)(x >> 64)); }
struct Cond { int var, lo, hi; };
struct AltT { string tag; int open; vector<Cond> c; };
map<array<int, 3>, vector<AltT>> HUB;
int CPL[5][5][5][5][5];
struct Cfg {
    string name, verdict; int n, proved; vector<int> deg; vector<vector<char>> E; int dm[16];
    vector<vector<int>> ord; vector<vector<vector<pair<int, char>>>> prv;   // per start x0: order, and for each position the earlier positions + adjacency
};
vector<Cfg> CF;
int D, NV, Lw[16]; M A[80]; int hostL[80]; M byL[16]; int cntL[16]; bool ex[80];
inline int W(int j) { return 1 + ((j % D) + D) % D; }
inline int S(int j) { return 1 + D + ((j % D) + D) % D; }
inline int Pv(int j, int k) { return 1 + 2 * D + 3 * (((j % D) + D) % D) + (k - 1); }
void setHost(int v, int l) {   // l = exact letter or 0
    if (hostL[v]) { byL[hostL[v]] &= ~bit(v); cntL[hostL[v]]--; }
    hostL[v] = l;
    if (l) { byL[l] |= bit(v); cntL[l]++; }
}
void buildStructure() {
    NV = 1 + 5 * D;
    for (int v = 0; v < 80; v++) { A[v] = 0; hostL[v] = 0; ex[v] = false; }
    for (int l = 0; l < 16; l++) { byL[l] = 0; cntL[l] = 0; }
    auto e = [&](int a, int b) { A[a] |= bit(b); A[b] |= bit(a); };
    ex[0] = true;
    for (int j = 0; j < D; j++) {
        ex[W(j)] = ex[S(j)] = true;
        e(0, W(j)); e(W(j), W(j + 1)); e(W(j), S(j - 1)); e(W(j), S(j));
        int k = Lw[j] == 9 ? 3 : Lw[j] - 5;
        vector<int> seg = {S(j - 1)};
        for (int q = 1; q <= k; q++) { ex[Pv(j, q)] = true; seg.push_back(Pv(j, q)); e(W(j), Pv(j, q)); }
        seg.push_back(S(j));
        for (size_t q = 0; q + 1 < seg.size(); q++) e(seg[q], seg[q + 1]);
    }
    setHost(0, D);
    for (int j = 0; j < D; j++) if (Lw[j] <= 8) setHost(W(j), Lw[j]);
}
// ---------------- containment
int phi[16];
bool ext(const Cfg& c, int x0, int pos, M used) {
    if (pos == c.n) return true;
    int x = c.ord[x0][pos]; M cand = byL[c.deg[x] < 16 ? c.deg[x] : 0] & ~used;
    for (auto& pr : c.prv[x0][pos]) { if (pr.second) cand &= A[phi[pr.first]]; else cand &= ~A[phi[pr.first]]; if (!cand) return false; }
    while (cand) { int t = ctz128(cand); cand &= cand - 1; phi[pos] = t; if (ext(c, x0, pos + 1, used | bit(t))) return true; }
    return false;
}
bool prefilter(const Cfg& c) { for (int l = 5; l < 16; l++) if (c.dm[l] > cntL[l]) return false; return true; }
bool containsAt(const Cfg& c, int v) {    // an occurrence using host v
    if (!prefilter(c)) return false;
    int l = hostL[v];
    for (int x0 = 0; x0 < c.n; x0++) if (c.deg[x0] == l) { phi[0] = v; if (ext(c, x0, 1, bit(v))) return true; }
    return false;
}
bool containsAny(const Cfg& c) {
    if (!prefilter(c)) return false;
    // anchor the least frequent letter of the configuration
    int best = -1, bl = 0;
    for (int l = 5; l < 16; l++) if (c.dm[l] && (best < 0 || cntL[l] < best)) { best = cntL[l]; bl = l; }
    M hs = byL[bl];
    while (hs) { int v = ctz128(hs); hs &= hs - 1; for (int x0 = 0; x0 < c.n; x0++) if (c.deg[x0] == bl) { phi[0] = v; if (ext(c, x0, 1, bit(v))) return true; } }
    return false;
}
vector<int> ACT;   // active configurations, proved first
int killAt(int v) { for (int k : ACT) if (containsAt(CF[k], v)) return k; return -1; }
int killAny() { for (int k : ACT) if (containsAny(CF[k])) return k; return -1; }
// ---------------- charge
struct Inst { int hub, open, nviol; string tag; };
vector<Inst> I; vector<int> vars; vector<vector<int>> dom; vector<vector<Cond>> vc;   // vc[q]: (inst, lo, hi) as Cond{var = inst}
int UBc, SUc, BASE;
void buildCharge() {
    I.clear();
    vector<int> varpos(80, -1); vars.clear();
    for (int j = 0; j < D; j++) {
        vars.push_back(S(j));
        int k = Lw[j] == 9 ? 3 : Lw[j] - 5;
        for (int q = 1; q <= k; q++) if (!(Lw[j] == 9 && q == 2)) vars.push_back(Pv(j, q));
    }
    for (size_t q = 0; q < vars.size(); q++) varpos[vars[q]] = q;
    vc.assign(vars.size(), {});
    for (int i = 0; i < D; i++) {
        if (Lw[i] == 9) continue;
        auto& alts = HUB[{Lw[(i - 1 + D) % D], Lw[i], Lw[(i + 1) % D]}];
        for (auto& al : alts) {
            bool ok = true; vector<Cond> rest;
            for (auto& c : al.c) {
                int v = -1;
                switch (c.var) {
                    case 0: if (Lw[(i - 2 + 2 * D) % D] < c.lo || Lw[(i - 2 + 2 * D) % D] > c.hi) ok = false; break;
                    case 1: if (Lw[(i + 2) % D] < c.lo || Lw[(i + 2) % D] > c.hi) ok = false; break;
                    case 2: v = S(i - 2); break; case 3: v = S(i - 1); break; case 4: v = S(i); break; case 5: v = S(i + 1); break;
                    default: { int g = (c.var - 6) / 3, k = (c.var - 6) % 3 + 1; v = Pv(i - 1 + g, k); }
                }
                if (!ok) break;
                if (v >= 0) { if (varpos[v] < 0) { fprintf(stderr, "condition on a non-variable vertex %d\n", v); exit(3); } rest.push_back({v, c.lo, c.hi}); }
            }
            if (!ok) continue;
            int id = I.size(); I.push_back({i, al.open, 0, al.tag});
            for (auto& c : rest) vc[varpos[c.var]].push_back({id, c.lo, c.hi});
        }
    }
    UBc = I.size(); SUc = 0; for (auto& x : I) SUc += !x.open;
    BASE = 60 - 10 * D;
    dom.assign(vars.size(), {});
    for (size_t q = 0; q < vars.size(); q++) {
        auto pat = [&](int a) { vector<char> p; for (auto& c : vc[q]) p.push_back(a >= c.lo && a <= c.hi); return p; };
        auto p9 = pat(9);
        vector<pair<int, int>> vals;   // (#conditions satisfied, letter) ; order: more satisfied first, then 9 first
        vals.push_back({0, 9});
        for (int a = 5; a <= 8; a++) if (pat(a) != p9) vals.push_back({0, a});
        for (auto& pv : vals) { int s = 0; for (auto& c : vc[q]) s += pv.second >= c.lo && pv.second <= c.hi; pv.first = s; }
        stable_sort(vals.begin(), vals.end(), [](const pair<int, int>& x, const pair<int, int>& y) { return x.first > y.first; });
        for (auto& pv : vals) dom[q].push_back(pv.second);
    }
}
inline void assignV(int q, int a) {
    for (auto& c : vc[q]) if (a < c.lo || a > c.hi) { if (I[c.var].nviol++ == 0) { UBc--; if (!I[c.var].open) SUc--; } }
    setHost(vars[q], a <= 8 ? a : 0);
}
inline void unassignV(int q, int a) {
    for (auto& c : vc[q]) if (a < c.lo || a > c.hi) { if (--I[c.var].nviol == 0) { UBc++; if (!I[c.var].open) SUc++; } }
    setHost(vars[q], 0);
}
// ---------------- search
string MODE, VAR; int best = 0, START = 0; double TL; long CAP; chrono::steady_clock::time_point T0;
bool timeout = false; int skippedUB = INT_MIN; long nodes = 0, leaves = 0, words = 0, wordsKilled = 0;
vector<int> val;   // current assignment per var position
map<int, long> killEv;     // config -> # prune events (node bound > threshold)
map<int, long> linkKill;
struct Rec { int hi, lo; string link, sw, pv, note; };
vector<Rec> argmaxR; vector<Rec> modadm, genuine; long nModadm = 0, nGenuine = 0; int maxModadm = INT_MIN, maxGenuine = INT_MIN;
map<string, long> modadmBySet;
string linkStr() { string s; for (int j = 0; j < D; j++) s += char('0' + Lw[j]); return s; }
Rec curRec(int hi, int lo) {
    Rec r; r.hi = hi; r.lo = lo; r.link = linkStr(); r.sw = string(D, '9'); r.pv = string(3 * D, '9');
    for (size_t q = 0; q < vars.size(); q++) {
        int v = vars[q], a = val[q];
        if (v >= 1 + D && v < 1 + 2 * D) r.sw[v - 1 - D] = char('0' + a); else r.pv[v - 1 - 2 * D] = char('0' + a);
    }
    return r;
}
vector<int> NONE;
void leaf() {
    leaves++;
    int hi = BASE + UBc, lo = BASE + SUc;
    if (MODE == "max") {
        if (hi > best) { best = hi; argmaxR.clear(); }
        if (hi == best && argmaxR.size() < 5) argmaxR.push_back(curRec(hi, lo));
        return;
    }
    // enum: classify against the none configurations (variant 582) or record (variant 633 / none)
    string set;
    if (VAR == "582") for (int k : NONE) if (containsAny(CF[k])) set += (set.empty() ? "" : "+") + CF[k].name;
    if (!set.empty()) { nModadm++; modadmBySet[set]++; maxModadm = max(maxModadm, hi); if (modadm.size() < 100000000) { auto r = curRec(hi, lo); r.note = set; modadm.push_back(r); } }
    else { nGenuine++; maxGenuine = max(maxGenuine, hi); if (genuine.size() < 400) genuine.push_back(curRec(hi, lo)); }
}
void dfs(size_t q) {
    if (timeout) { skippedUB = max(skippedUB, BASE + UBc); return; }
    if ((++nodes & 0xFFFF) == 0 && chrono::duration<double>(chrono::steady_clock::now() - T0).count() > TL) timeout = true;
    if (q == vars.size()) { leaf(); return; }
    for (int a : dom[q]) {
        if (timeout) { skippedUB = max(skippedUB, BASE + UBc); return; }
        int thr = MODE == "max" ? best : 0;
        assignV(q, a); val[q] = a;
        if (BASE + UBc > thr) {
            int k = (a <= 8 && VAR != "none") ? killAt(vars[q]) : -1;
            if (k >= 0) killEv[k]++;
            else dfs(q + 1);
        }
        unassignV(q, a);
        if (MODE == "enum" && (nModadm + nGenuine) >= CAP) { timeout = true; skippedUB = max(skippedUB, BASE + UBc); return; }
    }
}
int cpl(int a, int b, int c, int d2, int e) { return CPL[a - 5][b - 5][c - 5][d2 - 5][e - 5]; }
int CMX[10] = {0, 0, 0, 0, 0, 6, 6, 6, 4, 0};
bool canonical() {
    for (int r = 0; r < D; r++) for (int dir = -1; dir <= 1; dir += 2) {
        if (r == 0 && dir == 1) continue;
        for (int j = 0; j < D; j++) {
            int x = Lw[((r + dir * j) % D + D) % D];
            if (x < Lw[j]) return false;
            if (x > Lw[j]) break;
        }
    }
    return true;
}
void processWord() {
    words++;
    // full c+ bound
    int ub = BASE; for (int i = 0; i < D; i++) ub += cpl(Lw[(i - 2 + 2 * D) % D], Lw[(i - 1 + D) % D], Lw[i], Lw[(i + 1) % D], Lw[(i + 2) % D]);
    int thr = MODE == "max" ? best : 0;
    if (ub <= thr) return;
    buildStructure();
    if (VAR != "none") { int k = killAny(); if (k >= 0) { wordsKilled++; linkKill[k]++; return; } }
    buildCharge(); val.assign(vars.size(), 9);
    if (BASE + UBc <= thr) return;
    dfs(0);
}
void wordDfs(int j, int partial) {   // partial = sum of c+ over hubs with complete windows inside 0..j-1 (i in 2..j-3) + optimistic rest
    if (j == D) { if (canonical()) processWord(); return; }
    for (int l = 5; l <= 9; l++) {
        Lw[j] = l;
        // optimistic bound: hubs i with window inside [0, j]: exact c+, others CMX by own letter (6 if unknown)
        int ub = BASE;
        for (int i = 0; i < D; i++) {
            if (i >= 2 && i + 2 <= j) ub += cpl(Lw[i - 2], Lw[i - 1], Lw[i], Lw[i + 1], Lw[i + 2]);
            else if (i <= j) ub += CMX[Lw[i]];
            else ub += 6;
        }
        int thr = MODE == "max" ? best : 0;
        if (ub <= thr) continue;
        if (timeout) { skippedUB = max(skippedUB, ub); continue; }
        if (j == 0 || Lw[j] >= Lw[0]) wordDfs(j + 1, 0);   // canonical words start with their least letter
    }
}
// ---------------- input
void readTables(const string& dir) {
    ifstream h(dir + "hubs.txt"); string line;
    while (getline(h, line)) {
        if (line.empty() || line[0] == '#') continue;
        istringstream is(line); int a, b, c, n; is >> a >> b >> c >> n; vector<AltT> v;
        for (int t = 0; t < n; t++) { getline(h, line); istringstream js(line); AltT al; int nc; js >> al.tag >> al.open >> nc; for (int q = 0; q < nc; q++) { Cond cc; js >> cc.var >> cc.lo >> cc.hi; al.c.push_back(cc); } v.push_back(al); }
        HUB[{a, b, c}] = v;
    }
    ifstream cp(dir + "cplus.txt");
    while (getline(cp, line)) { if (line.size() < 7) continue; int x = stoi(line.substr(6)); CPL[line[0] - '5'][line[1] - '5'][line[2] - '5'][line[3] - '5'][line[4] - '5'] = x; }
    ifstream cf(dir + "configs.txt");
    while (getline(cf, line)) {
        if (line.empty() || line[0] == '#') continue;
        Cfg c; int idx; istringstream is(line); is >> idx >> c.name >> c.verdict >> c.n;
        c.proved = c.verdict == "D2" || c.verdict == "C2cons";
        getline(cf, line); { istringstream ds(line); c.deg.resize(c.n); for (auto& x : c.deg) ds >> x; }
        c.E.assign(c.n, vector<char>(c.n, 0));
        getline(cf, line); { istringstream es(line); int ne; es >> ne; for (int q = 0; q < ne; q++) { int a, b; es >> a >> b; c.E[a][b] = c.E[b][a] = 1; } }
        getline(cf, line);
        memset(c.dm, 0, sizeof c.dm); for (int x : c.deg) c.dm[x < 16 ? x : 0]++;
        c.ord.resize(c.n); c.prv.resize(c.n);
        for (int x0 = 0; x0 < c.n; x0++) {     // BFS order from x0 (interiors are connected)
            vector<int> o = {x0}; vector<char> in(c.n, 0); in[x0] = 1;
            for (size_t q = 0; q < o.size(); q++) for (int y = 0; y < c.n; y++) if (c.E[o[q]][y] && !in[y]) { in[y] = 1; o.push_back(y); }
            if ((int)o.size() != c.n) { fprintf(stderr, "disconnected interior %s\n", c.name.c_str()); exit(4); }
            c.ord[x0] = o; c.prv[x0].resize(c.n);
            for (int p = 1; p < c.n; p++) for (int r = 0; r < p; r++) c.prv[x0][p].push_back({r, c.E[o[p]][o[r]]});
            // adjacency to earlier positions first (they restrict the candidates most)
            for (int p = 1; p < c.n; p++) stable_sort(c.prv[x0][p].begin(), c.prv[x0][p].end(), [](const pair<int, char>& a, const pair<int, char>& b) { return a.second > b.second; });
        }
        CF.push_back(c);
    }
}
int main(int argc, char** argv) {
    string dir = argv[1]; D = atoi(argv[2]); MODE = argv[3]; VAR = argc > 4 ? argv[4] : "633";
    TL = argc > 5 ? atof(argv[5]) : 3000; CAP = argc > 6 ? atol(argv[6]) : 200000; START = argc > 7 ? atoi(argv[7]) : 0; best = START;
    readTables(dir);
    for (int k = 0; k < (int)CF.size(); k++) if (CF[k].proved) ACT.push_back(k);
    for (int k = 0; k < (int)CF.size(); k++) if (!CF[k].proved) { NONE.push_back(k); if (VAR == "633") ACT.push_back(k); }
    if (VAR == "none") ACT.clear();
    if (getenv("EXCL")) {   // planted control: drop the named configurations (comma list) from the kill set
        string ex = getenv("EXCL"); set<string> drop; size_t p0 = 0;
        while (p0 <= ex.size()) { size_t q = ex.find(',', p0); if (q == string::npos) q = ex.size(); drop.insert(ex.substr(p0, q - p0)); p0 = q + 1; }
        vector<int> a2, n2; for (int k : ACT) if (!drop.count(CF[k].name)) a2.push_back(k); for (int k : NONE) if (!drop.count(CF[k].name)) n2.push_back(k);
        fprintf(stderr, "EXCL: %zu configurations dropped from the kill set\n", ACT.size() - a2.size()); ACT = a2; NONE = n2;
    }
    T0 = chrono::steady_clock::now();
    if (MODE == "eval") {   // argv[4] = xval file
        ACT.clear(); for (int k = 0; k < (int)CF.size(); k++) ACT.push_back(k);
        ifstream xf(argv[4]); string line; int nok = 0, nbad = 0;
        while (getline(xf, line)) {
            if (line.empty() || line[0] == '#') continue;
            istringstream is(line); int d; string lk, sw, pv; int ehi, elo, nc; is >> d >> lk >> sw >> pv >> ehi >> elo >> nc; set<int> ecfg; for (int q = 0; q < nc; q++) { int x; is >> x; ecfg.insert(x); }
            D = d; for (int j = 0; j < D; j++) Lw[j] = lk[j] - '0';
            buildStructure(); buildCharge(); val.assign(vars.size(), 9);
            for (size_t q = 0; q < vars.size(); q++) { int v = vars[q], a = (v < 1 + 2 * D) ? sw[v - 1 - D] - '0' : pv[v - 1 - 2 * D] - '0'; assignV(q, a); val[q] = a; }
            int hi = BASE + UBc, lo = BASE + SUc; set<int> got; for (int k = 0; k < (int)CF.size(); k++) if (containsAny(CF[k])) got.insert(k);
            if (hi == ehi && lo == elo && got == ecfg) nok++; else { nbad++; if (nbad <= 10) printf("MISMATCH %s: hi %d/%d lo %d/%d cfg %zu/%zu\n", line.substr(0, 60).c_str(), hi, ehi, lo, elo, got.size(), ecfg.size()); }
        }
        printf("eval: %d agree, %d mismatch\n", nok, nbad); return nbad ? 1 : 0;
    }
    wordDfs(0, 0);
    double secs = chrono::duration<double>(chrono::steady_clock::now() - T0).count();
    printf("{\"d\": %d, \"mode\": \"%s\", \"variant\": \"%s\", \"complete\": %s, \"seconds\": %.1f, \"words_searched\": %ld, \"words_killed_by_link_alone\": %ld, \"nodes\": %ld, \"leaves\": %ld,\n",
           D, MODE.c_str(), VAR.c_str(), timeout ? "false" : "true", secs, words, wordsKilled, nodes, leaves);
    string mxs = best > START ? to_string(best) : "\"<= " + to_string(START) + "\"";
    if (MODE == "max") printf(" \"start\": %d, \"max_hi\": %s, \"bound_if_incomplete\": %d,\n", START, mxs.c_str(), timeout ? max(best, skippedUB) : best);
    auto pr = [&](const char* nm, vector<Rec>& v) { printf(" \"%s\": [", nm); for (size_t q = 0; q < v.size(); q++) printf("%s{\"hi\": %d, \"lo\": %d, \"link\": \"%s\", \"sword\": \"%s\", \"privs\": \"%s\", \"note\": \"%s\"}", q ? ", " : "", v[q].hi, v[q].lo, v[q].link.c_str(), v[q].sw.c_str(), v[q].pv.c_str(), v[q].note.c_str()); printf("],\n"); };
    if (MODE == "max") pr("argmax", argmaxR);
    else { printf(" \"n_modadm_leaves\": %ld, \"max_modadm\": %d, \"n_genuine_leaves\": %ld, \"max_genuine\": %d, \"cap_hit\": %s,\n", nModadm, maxModadm, nGenuine, maxGenuine, timeout ? "true" : "false");
           printf(" \"modadm_by_none_set\": {"); int f = 0; for (auto& kv : modadmBySet) printf("%s\"%s\": %ld", f++ ? ", " : "", kv.first.c_str(), kv.second); printf("},\n");
           pr("modadm_examples", modadm); pr("genuine_examples", genuine); }
    printf(" \"kill_events\": {"); int f = 0;
    vector<pair<long, int>> ke; for (auto& kv : killEv) ke.push_back({-kv.second, kv.first}); sort(ke.begin(), ke.end());
    for (auto& kv : ke) printf("%s\"%s:%s\": %ld", f++ ? ", " : "", CF[kv.second].name.c_str(), CF[kv.second].verdict.c_str(), -kv.first); printf("},\n");
    printf(" \"link_kills\": {"); f = 0; for (auto& kv : linkKill) printf("%s\"%s:%s\": %ld", f++ ? ", " : "", CF[kv.first].name.c_str(), CF[kv.first].verdict.c_str(), kv.second); printf("}}\n");
    return 0;
}
