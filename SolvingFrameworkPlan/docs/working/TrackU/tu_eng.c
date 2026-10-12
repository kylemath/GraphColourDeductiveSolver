/* Track U engine: closed orbits of the matching-form dynamics (TrackS S3/S4, TrackT tt_lib) on ABSTRACT graphs
   with one vertex v = 0 of degree 5 (edges cyclically labelled f0..f4) and all other vertices cubic.

   A perfect matching M is DL-good (frame k = index of its v-edge) iff Q = E - M is a connected figure-eight whose
   v-loops pair (f_{k-1} f_{k+1}) = X and (f_{k+2} f_{k-2}) = Y, with Y the odd loop.  Then Q has exactly two
   perfect matchings: pred(M) (contains f_{k+2}) and succ(M) (contains f_{k-2}); succ = pred xor Y.
   Orbit map: M -> succ(M) (when succ(M) is DL-good).  State = (pred(M), M); k(H) = #components of pred|M.
   Unlike TrackT's tt_abstract.py, ALL perfect matchings are enumerated, so closed orbits without any
   Hamiltonian state are seen too.

   Law (Tait form of the chain-parity law): k(H) changes parity at every step between states whose
   F12 = E - pred(M) is connected (pred DL-good).  T1-violation: closed orbit with k(H) word 1,2,1,2,...

   usage:
     tu_eng eval FILE                          all closed orbits (and longest law/R paths) of every graph line
     tu_eng anneal SEED N SECONDS MODE SIMPLE [SEEDFILE]
         MODE A: law-respecting closed orbits of any level;  B: push toward k(H) = 1,2,1,2 on closed orbits
   graph line:  n m a0 b0 ... a_{m-1} b_{m-1} f0 f1 f2 f3 f4                                              */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>

typedef unsigned __int128 msk;
#define MAXN 72
#define MAXM 110
#define MAXPM 300000
#define B1 ((msk)1)

static int n, m, EA[MAXM], EB[MAXM], fv[5];
static int inc[MAXN][5], deg[MAXN];
static msk ALL;

static void build_inc(void) {
    for (int x = 0; x < n; x++) deg[x] = 0;
    for (int e = 0; e < m; e++) { inc[EA[e]][deg[EA[e]]++] = e; inc[EB[e]][deg[EB[e]]++] = e; }
    ALL = (m >= 128) ? ~(msk)0 : ((B1 << m) - 1);
}
static inline int oth(int e, int x) { return EA[e] == x ? EB[e] : EA[e]; }

/* ---------- perfect matchings ---------- */
static msk pms[MAXPM]; static int npm, pm_over; static int covered[MAXN];
static void pm_rec(msk cur) {
    if (pm_over) return;
    int x = -1;
    for (int i = 0; i < n; i++) if (!covered[i]) { x = i; break; }
    if (x < 0) { if (npm < MAXPM) pms[npm++] = cur; else pm_over = 1; return; }
    covered[x] = 1;
    for (int i = 0; i < deg[x]; i++) {
        int e = inc[x][i], y = oth(e, x);
        if (covered[y]) continue;
        covered[y] = 1; pm_rec(cur | (B1 << e)); covered[y] = 0;
    }
    covered[x] = 0;
}

static int trace(msk Q, int e0, int *seq, int *len) {
    int k = e0, x = oth(e0, 0), L = 0; seq[L++] = e0;
    while (x != 0) {
        int nk = -1, c = 0;
        for (int i = 0; i < deg[x]; i++) { int t = inc[x][i]; if (t != k && (Q >> t & 1)) { nk = t; c++; } }
        if (c != 1) return -1;
        k = nk; seq[L++] = k; x = oth(k, x);
        if (L > m + 1) return -1;
    }
    *len = L; return k;
}

/* returns 1 if M is DL-good; sets pred, succ, frame */
static int dl(msk M, msk *pred, msk *succ, int *kk) {
    int k = -1;
    for (int s = 0; s < 5; s++) if (M >> fv[s] & 1) { k = s; break; }
    if (k < 0) return 0;
    msk Q = ALL & ~M;
    int sx[MAXM + 2], sy[MAXM + 2], lx, ly;
    if (trace(Q, fv[(k + 4) % 5], sx, &lx) != fv[(k + 1) % 5]) return 0;
    if (trace(Q, fv[(k + 2) % 5], sy, &ly) != fv[(k + 3) % 5]) return 0;
    msk X = 0, Y = 0;
    for (int i = 0; i < lx; i++) X |= B1 << sx[i];
    for (int i = 0; i < ly; i++) Y |= B1 << sy[i];
    if ((X | Y) != Q || (X & Y)) return 0;
    /* X: r inner vertices (r even) -> lx = r+1 odd; Y: s inner (odd) -> ly = s+1 even */
    if (lx % 2 != 1 || ly % 2 != 0) return 0;
    msk base = 0;
    for (int i = 1; i < lx - 1; i += 2) base |= B1 << sx[i];
    msk p = base, q = base;
    for (int i = 0; i < ly; i += 2) p |= B1 << sy[i];
    for (int i = 1; i < ly; i += 2) q |= B1 << sy[i];
    *pred = p; *succ = q; *kk = k; return 1;
}

static int kcomp(msk H) {   /* H a 2-factor */
    static int vis[MAXN]; int c = 0;
    for (int i = 0; i < n; i++) vis[i] = 0;
    for (int s = 0; s < n; s++) {
        if (vis[s]) continue;
        c++; int x = s, pe = -1;
        while (!vis[x]) {
            vis[x] = 1; int ne = -1;
            for (int i = 0; i < deg[x]; i++) { int t = inc[x][i]; if (t != pe && (H >> t & 1)) { ne = t; break; } }
            if (ne < 0) break;
            pe = ne; x = oth(ne, x);
        }
    }
    return c;
}

/* ---------- hash of DL-good matchings ---------- */
#define HS (1 << 20)
static msk hkey[HS]; static int hval[HS], hstamp[HS], stamp = 1;
static inline uint64_t hh(msk a) { uint64_t x = (uint64_t)a ^ ((uint64_t)(a >> 64) * 0x9E3779B97F4A7C15ULL);
    x ^= x >> 31; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 29; return x; }
static void hput(msk a, int v) { uint64_t i = hh(a) & (HS - 1);
    while (hstamp[i] == stamp && hkey[i] != a) i = (i + 1) & (HS - 1);
    hstamp[i] = stamp; hkey[i] = a; hval[i] = v; }
static int hget(msk a) { uint64_t i = hh(a) & (HS - 1);
    while (hstamp[i] == stamp) { if (hkey[i] == a) return hval[i]; i = (i + 1) & (HS - 1); } return -1; }

static msk gM[MAXPM], gP[MAXPM]; static int gS[MAXPM], gPr[MAXPM], gK[MAXPM], gF[MAXPM], ng;

/* ---------- evaluation ---------- */
typedef struct {
    double score; int ndl, ncyc, nlaw, t1; int bestL; char word[512]; int lawcyc_L[64]; char lawcyc_w[8][512];
    int bestcyc_start; int maxlawpath, maxrpath; int bestv; int lawn1, lawD, lawL; char lawword[512];
} Eval;

static char MODE = 'A';
static long hL[128], hLlaw[128], hLt1[128], hLham[128];

static int analyse(Eval *ev, int print, FILE *out) {
    npm = 0; pm_over = 0; for (int i = 0; i < n; i++) covered[i] = 0;
    pm_rec(0);
    stamp++; if (stamp > 2000000000) { memset(hstamp, 0, sizeof hstamp); stamp = 1; }
    ng = 0;
    static msk succm[MAXPM];
    for (int i = 0; i < npm; i++) {
        msk p, q; int k;
        if (dl(pms[i], &p, &q, &k)) { gM[ng] = pms[i]; gP[ng] = p; succm[ng] = q; gF[ng] = k; hput(pms[i], ng); ng++; }
    }
    for (int i = 0; i < ng; i++) { gS[i] = hget(succm[i]); gPr[i] = hget(gP[i]); gK[i] = kcomp(gP[i] | gM[i]); }
    ev->ndl = ng; ev->ncyc = 0; ev->nlaw = 0; ev->t1 = 0; ev->bestL = 0; ev->word[0] = 0; ev->maxlawpath = 0;
    ev->maxrpath = 0; ev->bestv = 99; ev->lawn1 = -1; ev->lawD = 99999; ev->lawL = 0; ev->lawword[0] = 0;
    double best = 0.001 * ng;
    static int col[MAXPM]; for (int i = 0; i < ng; i++) col[i] = 0;
    static int seq[MAXPM];
    /* cycles */
    for (int s = 0; s < ng; s++) {
        if (col[s]) continue;
        int x = s, L = 0;
        while (x >= 0 && col[x] == 0) { col[x] = 1; seq[L++] = x; x = gS[x]; }
        int cs = -1;
        if (x >= 0 && col[x] == 1) { for (int i = 0; i < L; i++) if (seq[i] == x) { cs = i; break; } }
        for (int i = 0; i < L; i++) col[seq[i]] = 2;
        if (cs < 0) continue;
        int CL = L - cs; int *c = seq + cs;
        ev->ncyc++;
        int v = 0, n1 = 0, D0 = 0, D1 = 0, kmax = 0;
        for (int i = 0; i < CL; i++) {
            int a = gK[c[i]], b = gK[c[(i + 1) % CL]];
            if (((a - b) & 1) == 0) v++;
            if (a == 1) n1++;
            if (a > kmax) kmax = a;
            int t0 = (i % 2 == 0) ? 1 : 2, t1 = 3 - t0;
            D0 += abs(a - t0); D1 += abs(a - t1);
        }
        int D = (CL % 2 == 0) ? (D0 < D1 ? D0 : D1) : 999;
        double sc;
        sc = 20 + 20.0 * (CL - v) / CL + 0.5 * (CL > 40 ? 40 : CL) - (v > 0 ? 5 : 0);
        if (CL % 2) sc = 12 + 0.1 * CL;
        if (MODE == 'B') { double fr = 2.0 * n1 / CL; if (fr > 1) fr = 1; double dd = (double)(D > 2 * CL ? 2 * CL : D) / CL;
            sc += 12.0 * fr - 8.0 * dd + (v == 0 && D == 0 ? 100 : 0); }
        { int li = CL < 127 ? CL : 127; hL[li]++; if (v == 0) hLlaw[li]++; if (v == 0 && D == 0) hLt1[li]++; if (n1 > 0) hLham[li]++; }
        if (v == 0) { ev->nlaw++;
            if (n1 > ev->lawn1 || (n1 == ev->lawn1 && D < ev->lawD)) { ev->lawn1 = n1; ev->lawD = D; ev->lawL = CL; int p = 0;
                for (int i = 0; i < CL && p < 500; i++) p += sprintf(ev->lawword + p, "%d", gK[c[i]] > 9 ? 9 : gK[c[i]]); } }
        if (v == 0 && D == 0) ev->t1++;
        if (v < ev->bestv) ev->bestv = v;
        if (print) {
            fprintf(out, "{\"event\":\"cycle\",\"L\":%d,\"viol\":%d,\"n1\":%d,\"D\":%d,\"kmax\":%d,\"word\":\"", CL, v, n1, D, kmax);
            for (int i = 0; i < CL; i++) fprintf(out, "%d%s", gK[c[i]], i + 1 < CL ? " " : "");
            fprintf(out, "\",\"frames\":\"");
            for (int i = 0; i < CL; i++) fprintf(out, "%d", gF[c[i]]);
            fprintf(out, "\",\"M\":[");
            for (int i = 0; i < CL; i++) {
                fprintf(out, "%s[", i ? "," : ""); int f = 1;
                for (int e = 0; e < m; e++) if (gM[c[i]] >> e & 1) { fprintf(out, "%s%d", f ? "" : ",", e); f = 0; }
                fprintf(out, "]");
            }
            fprintf(out, "]}\n");
        }
        if (sc > best) {
            best = sc; ev->bestL = CL; int p = 0;
            for (int i = 0; i < CL && p < 500; i++) p += sprintf(ev->word + p, "%d", gK[c[i]] > 9 ? 9 : gK[c[i]]);
            strcat(ev->word, "*");
        }
    }
    /* paths: start at nodes with no DL-good predecessor whose successor... (all maximal chains) */
    for (int s = 0; s < ng; s++) {
        if (gPr[s] >= 0 && gS[gPr[s]] == s) continue;   /* has a predecessor in the orbit graph */
        int L = 0, x = s;
        while (x >= 0 && L < MAXPM) { seq[L++] = x; x = gS[x]; if (x == s) break; }
        /* law stretch over states 1..L-1 (F12 connected) */
        int bl = 0, cur = 0, br = 0, cr = 0;
        for (int i = 1; i < L; i++) {
            int a = gK[seq[i]];
            if (i > 1 && ((a - gK[seq[i - 1]]) & 1)) cur++; else cur = 1;
            if (cur > bl) bl = cur;
            if ((a == 1 || a == 2) && i > 1 && gK[seq[i - 1]] + a == 3) cr++; else cr = (a == 1 || a == 2);
            if (cr > br) br = cr;
        }
        if (bl > ev->maxlawpath) ev->maxlawpath = bl;
        if (br > ev->maxrpath) ev->maxrpath = br;
        double sc = 0.8 * (bl > 20 ? 20 : bl) + 0.4 * (L > 30 ? 30 : L) + (MODE == 'A' ? 0 : 0.5 * (br > 20 ? 20 : br));
        if (sc > best) {
            best = sc; int p = 0;
            for (int i = 0; i < L && p < 500; i++) p += sprintf(ev->word + p, "%d", gK[seq[i]] > 9 ? 9 : gK[seq[i]]);
        }
    }
    ev->score = best;
    return 0;
}

/* ---------- stub representation for annealing ---------- */
static int NS, mate[3 * MAXN + 8];   /* stubs: 0..4 = v slots f0..f4 ; 5+3(x-1)+j for x>=1 */
static int stubv(int s) { return s < 5 ? 0 : 1 + (s - 5) / 3; }
static int simple_req = 1;

static int from_stubs(void) {   /* build EA/EB/fv; returns 0 if loop or (simple_req and multi-edge) */
    m = 0;
    for (int s = 0; s < NS; s++) {
        int t = mate[s]; if (t < s) continue;
        int a = stubv(s), b = stubv(t);
        if (a == b) return 0;
        EA[m] = a; EB[m] = b;
        if (s < 5) fv[s] = m;
        if (t < 5) fv[t] = m;
        m++;
    }
    build_inc();
    if (simple_req) {
        for (int x = 0; x < n; x++) for (int i = 0; i < deg[x]; i++) for (int j = i + 1; j < deg[x]; j++)
            if (oth(inc[x][i], x) == oth(inc[x][j], x)) return 0;
    }
    /* connected */
    int vis[MAXN] = {0}, st[MAXN], sp = 0, c = 1; vis[0] = 1; st[sp++] = 0;
    while (sp) { int x = st[--sp]; for (int i = 0; i < deg[x]; i++) { int y = oth(inc[x][i], x); if (!vis[y]) { vis[y] = 1; c++; st[sp++] = y; } } }
    return c == n;
}

static uint64_t rs = 88172645463325252ULL;
static inline uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }

static void random_stubs(void) {
    int perm[3 * MAXN + 8];
    do {
        for (int i = 0; i < NS; i++) perm[i] = i;
        for (int i = NS - 1; i > 0; i--) { int j = rnd() % (i + 1); int t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
        for (int i = 0; i < NS; i += 2) { mate[perm[i]] = perm[i + 1]; mate[perm[i + 1]] = perm[i]; }
    } while (!from_stubs());
}

static void stubs_from_graph(void) {   /* after reading EA/EB/fv */
    int nxt[MAXN]; for (int x = 1; x < n; x++) nxt[x] = 5 + 3 * (x - 1);
    int sa[MAXM], sb[MAXM];
    for (int e = 0; e < m; e++) {
        int a = EA[e], b = EB[e];
        sa[e] = -1; sb[e] = -1;
        if (a != 0) sa[e] = nxt[a]++;
        if (b != 0) sb[e] = nxt[b]++;
    }
    for (int s = 0; s < 5; s++) { int e = fv[s]; if (EA[e] == 0 && sa[e] < 0) sa[e] = s; else sb[e] = s; }
    for (int e = 0; e < m; e++) { mate[sa[e]] = sb[e]; mate[sb[e]] = sa[e]; }
    NS = 5 + 3 * (n - 1);
}

static int read_graph(FILE *f) {
    if (fscanf(f, "%d %d", &n, &m) != 2) return 0;
    for (int e = 0; e < m; e++) if (fscanf(f, "%d %d", &EA[e], &EB[e]) != 2) return 0;
    for (int s = 0; s < 5; s++) if (fscanf(f, "%d", &fv[s]) != 1) return 0;
    build_inc(); return 1;
}

static void print_graph(FILE *o) {
    fprintf(o, "\"n\":%d,\"edges\":[", n);
    for (int e = 0; e < m; e++) fprintf(o, "%s[%d,%d]", e ? "," : "", EA[e], EB[e]);
    fprintf(o, "],\"fv\":[%d,%d,%d,%d,%d]", fv[0], fv[1], fv[2], fv[3], fv[4]);
}

int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "eval")) {
        FILE *f = fopen(argv[2], "r"); int gi = 0;
        if (argc > 3) MODE = argv[3][0];
        while (read_graph(f)) {
            Eval ev; printf("{\"event\":\"graph\",\"gi\":%d,", gi); print_graph(stdout); printf("}\n");
            analyse(&ev, 1, stdout);
            printf("{\"event\":\"summary\",\"gi\":%d,\"npm\":%d,\"pm_over\":%d,\"ndl\":%d,\"ncyc\":%d,\"nlaw\":%d,\"t1\":%d,\"maxlawpath\":%d,\"maxrpath\":%d,\"score\":%.3f}\n",
                   gi, npm, pm_over, ev.ndl, ev.ncyc, ev.nlaw, ev.t1, ev.maxlawpath, ev.maxrpath, ev.score);
            gi++;
        }
        return 0;
    }
    if (argc < 7) { fprintf(stderr, "usage\n"); return 1; }
    uint64_t seed = strtoull(argv[2], 0, 10); n = atoi(argv[3]); double secs = atof(argv[4]);
    MODE = argv[5][0]; simple_req = atoi(argv[6]);
    rs ^= seed * 0x9E3779B97F4A7C15ULL; for (int i = 0; i < 20; i++) rnd();
    int seeded = 0;
    if (argc > 7) {
        FILE *f = fopen(argv[7], "r");
        int pick = argc > 8 ? atoi(argv[8]) : 0;
        for (int i = 0; i <= pick; i++) if (!read_graph(f)) { fprintf(stderr, "bad seed\n"); return 1; }
        fclose(f); stubs_from_graph(); seeded = 1;
        int sr = simple_req; simple_req = 0; from_stubs(); simple_req = sr;
    } else { NS = 5 + 3 * (n - 1); random_stubs(); }
    int bmate[3 * MAXN + 8], cmate[3 * MAXN + 8];
    memcpy(cmate, mate, sizeof mate);
    Eval ev; analyse(&ev, 0, 0);
    double cur = ev.score, rec = -1, T = 2.0; long cnt = 0, lastimp = 0;
    memcpy(bmate, mate, sizeof mate);
    time_t t0 = time(0);
    int nlawseen = 0, nt1seen = 0;
    /* log the seed itself */
    printf("{\"event\":\"start\",\"seeded\":%d,\"score\":%.3f,\"ndl\":%d,\"ncyc\":%d,\"nlaw\":%d,\"word\":\"%s\",", seeded, ev.score, ev.ndl, ev.ncyc, ev.nlaw, ev.word);
    print_graph(stdout); printf("}\n"); fflush(stdout);
    int rmode = 0; if (MODE == 'R') { rmode = 1; MODE = 'A'; }
    int wmode = 0; long nacc = 0, nham = 0; if (MODE == 'W') { wmode = 1; MODE = 'A'; cur = -1e9; rec = -1e9; }
    long gcyc = 0, glaw = 0, gt1 = 0;
    while (difftime(time(0), t0) < secs) {
        memcpy(mate, cmate, sizeof mate);
        double r = urand();
        if (rmode) {
            random_stubs(); analyse(&ev, 0, 0); cnt++;
            if (ev.ncyc) gcyc++;
            if (ev.nlaw) { glaw++; if (glaw <= 200 || ev.t1) {
                printf("{\"event\":\"lawcycle\",\"cnt\":%ld,\"nlaw\":%d,\"t1\":%d,\"word\":\"%s\",", cnt, ev.nlaw, ev.t1, ev.word);
                print_graph(stdout); printf("}\n"); fflush(stdout); } }
            if (ev.t1) gt1++;
            continue;
        }
        if (r < 0.08) {   /* permute v's rotation labels */
            int p[5] = {0, 1, 2, 3, 4};
            if (urand() < 0.5) { int i = rnd() % 5, j = rnd() % 5; int t = p[i]; p[i] = p[j]; p[j] = t; }
            else for (int i = 4; i > 0; i--) { int j = rnd() % (i + 1); int t = p[i]; p[i] = p[j]; p[j] = t; }
            int nm[3 * MAXN + 8]; memcpy(nm, mate, sizeof mate);
            for (int s = 0; s < 5; s++) { int t = mate[s]; int ps = p[s]; int pt = t < 5 ? p[t] : t; nm[ps] = pt; nm[pt] = ps; }
            memcpy(mate, nm, sizeof nm);
        } else {
            int nsw = 1 + (urand() < 0.35) + (urand() < 0.15);
            for (int q = 0; q < nsw; q++) {
                int a = rnd() % NS, c = rnd() % NS; int b = mate[a], d = mate[c];
                if (a == c || a == d) continue;
                mate[a] = d; mate[d] = a; mate[c] = b; mate[b] = c;
            }
        }
        if (!from_stubs()) continue;
        analyse(&ev, 0, 0); cnt++;
        if (wmode) {
            if (ev.nlaw > 0) {
                double sc = 10.0 * ev.lawn1 - ev.lawD;
                int acc = (sc >= cur) || urand() < exp((sc - cur) / 3.0);
                if (acc) { cur = sc; memcpy(cmate, mate, sizeof mate); nacc++; }
                if (sc > rec || ev.t1 || (nacc % 200 == 0 && acc)) {
                    if (sc > rec) rec = sc;
                    printf("{\"event\":\"walk\",\"cnt\":%ld,\"acc\":%ld,\"lawn1\":%d,\"lawD\":%d,\"lawL\":%d,\"t1\":%d,\"lawword\":\"%s\",", cnt, nacc, ev.lawn1, ev.lawD, ev.lawL, ev.t1, ev.lawword);
                    print_graph(stdout); printf("}\n"); fflush(stdout);
                }
                if (ev.lawn1 > 0) nham++;
            }
            continue;
        }
        if (ev.nlaw > 0 || ev.t1 > 0) {
            nlawseen++; if (ev.t1) nt1seen++;
            if (nlawseen <= 400 || (ev.t1 && nt1seen <= 300)) {
                printf("{\"event\":\"lawcycle\",\"cnt\":%ld,\"nlaw\":%d,\"t1\":%d,\"score\":%.3f,\"word\":\"%s\",", cnt, ev.nlaw, ev.t1, ev.score, ev.word);
                print_graph(stdout); printf("}\n"); fflush(stdout);
            }
        }
        if (ev.score > rec) {
            rec = ev.score; memcpy(bmate, mate, sizeof mate); lastimp = cnt;
            printf("{\"event\":\"record\",\"cnt\":%ld,\"t\":%.0f,\"score\":%.3f,\"ndl\":%d,\"ncyc\":%d,\"nlaw\":%d,\"t1\":%d,\"bestv\":%d,\"word\":\"%s\",",
                   cnt, difftime(time(0), t0), ev.score, ev.ndl, ev.ncyc, ev.nlaw, ev.t1, ev.bestv, ev.word);
            print_graph(stdout); printf("}\n"); fflush(stdout);
        }
        if (ev.score >= cur || urand() < exp((ev.score - cur) / T)) { cur = ev.score; memcpy(cmate, mate, sizeof mate); }
        T = T * 0.9999; if (T < 0.5) T = 0.5;
        if (cnt - lastimp > 60000) {   /* restart: from best (50%) or random */
            if (urand() < 0.5 || seeded) memcpy(cmate, bmate, sizeof mate);
            else { random_stubs(); memcpy(cmate, mate, sizeof mate); }
            memcpy(mate, cmate, sizeof mate); from_stubs(); analyse(&ev, 0, 0); cur = ev.score; T = 2.0; lastimp = cnt;
        }
    }
    if (wmode) printf("{\"event\":\"walkdone\",\"acc\":%ld,\"lawgraphs_with_ham\":%ld}\n", nacc, nham);
    printf("{\"event\":\"done\",\"cnt\":%ld,\"rec\":%.3f,\"lawgraphs\":%d,\"t1graphs\":%d,\"rand_graphs_with_cycle\":%ld,\"rand_graphs_law\":%ld,\"rand_graphs_t1\":%ld,\"hist\":{", cnt, rec, nlawseen, nt1seen, gcyc, glaw, gt1);
    int first = 1;
    for (int i = 0; i < 128; i++) if (hL[i]) { printf("%s\"%d\":[%ld,%ld,%ld,%ld]", first ? "" : ",", i, hL[i], hLham[i], hLlaw[i], hLt1[i]); first = 0; }
    printf("}}\n");
    return 0;
}
