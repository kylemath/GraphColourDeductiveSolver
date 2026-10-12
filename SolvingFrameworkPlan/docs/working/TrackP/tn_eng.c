/* Track N engine = Track J engine tj_eng.c (copied) + Track N additions (Lemma E dev per state, constrained runs/cycles,
 * a second JSON line per hole with {"tn":1,...}).
 * Track J engine (independent C code).  Kempe classes of G - h at a degree-5 hole h, with the
 * total Kempe-chain count N(s) of every state.
 *
 * Input (stdin): lines "name n adj0;adj1;...;adj_{n-1}" (TrackF format; for spheres adj = rotation).
 * The link of h is adj[h] in the given cyclic order.  Holes: --hole H (default 0) or --allholes (every degree-5 vertex).
 * States: proper 4-colourings of G - h up to renaming (first-occurrence normal form).  Moves: swap of any component of
 * any of the six pair graphs of G - h.
 * Per unfilled state (link (alpha,mu,alpha,A,B) at x_j..x_{j+4}): L1 = x_{j+3} in K_{muA}(x_{j+1}),
 * L2 = x_{j+4} in K_{muB}(x_{j+1}), inA = x_j in K_{alphaA}(x_{j+2}), inB = x_j in K_{alphaB}(x_{j+2}),
 * pi = swap K_{alphaA}(x_{j+2}) (defined iff !inA).  Kinds: F (filled), DL, S (one lock), Z (no lock).
 * Component counts in role order (am, AB, aA, mB, aB, mA); N = their sum.
 * H3 edge counts E_k (k = P1 {am|AB}, P2 {aA|mB}, P3 {aB|mA}).
 * Output: one JSON line per (graph, hole): totals and, for every class containing a state on an all-DL pi-cycle,
 *   [size, filled, DL, onCyc, n8, n9, n10plus, lawFail, r7Fail, h3Fail, minKdeg, maxKdeg, nonDLunfilled, excess, h3imb, root]
 *   h3imb = sum over unfilled class states of |E1-E2-1| + |E2-E3|
 *   excess = sum over on-cycle states of max(0, N - 9)
 *   lawFail = # DL states c of the class with pi defined and (N(pi c)-N(c)) mod 2 != [pi c DL]
 *   r7Fail  = # link-free moves between unfilled states of the class with N+L1+L2 parity changed
 *   h3Fail  = # unfilled states of the class with NOT (E1 == E2+1 == E3+1)
 * --dump: also one line per state "S idx cls kind j L1 L2 inA inB pi N c6[6] onCyc E1 E2 E3 | moves" where each move
 *   is target:rolepair:linkmask (rolepair index 0..5 in role order, or pq for filled states), deduplicated by target+pair.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 64
typedef unsigned __int128 u128;
static int n, nv, h;
static int adjG[MAXN][MAXN], degG[MAXN];
static int vid[MAXN], orig[MAXN];  /* G vertex -> G-h index in BFS order; inverse */
static uint64_t nb[MAXN];
static int nedge; static int eu[4096], ev[4096];
static long maxstates = 400000;

static u128 *st; static long ns, cap;
static long *ht; static long hcap;
static uint64_t hash128(u128 x) { uint64_t a = (uint64_t)x, b = (uint64_t)(x >> 64); a ^= b * 0x9E3779B97F4A7C15ULL; a ^= a >> 29; a *= 0xBF58476D1CE4E5B9ULL; a ^= a >> 32; return a; }
static long lookup(u128 x) { uint64_t k = hash128(x) & (hcap - 1); while (ht[k] >= 0) { if (st[ht[k]] == x) return ht[k]; k = (k + 1) & (hcap - 1); } return -1; }
static void insert(u128 x) { if (ns >= cap) { cap *= 2; st = realloc(st, cap * sizeof(u128)); } st[ns] = x; uint64_t k = hash128(x) & (hcap - 1); while (ht[k] >= 0) k = (k + 1) & (hcap - 1); ht[k] = ns++; }
static int getc_(u128 s, int v) { return (int)((s >> (2 * v)) & 3); }

static int col[MAXN]; static int overflow;
static long reccalls, reclimit = 20000000;
static void rec(int i, int used) {
  if (overflow) return;
  if (++reccalls > reclimit) { overflow = 1; return; }
  if (i == nv) { u128 s = 0; for (int v = 0; v < nv; v++) s |= ((u128)col[v]) << (2 * v); if (ns >= maxstates) { overflow = 1; return; } insert(s); return; }
  int forb = 0; uint64_t m = nb[i] & ((i == 64) ? ~0ULL : ((1ULL << i) - 1));
  while (m) { int w = __builtin_ctzll(m); m &= m - 1; forb |= 1 << col[w]; }
  int lim = used + 1 < 4 ? used + 1 : 4;
  for (int a = 0; a < lim; a++) if (!(forb >> a & 1)) { col[i] = a; rec(i + 1, used > a + 1 ? used : a + 1); }
}
static u128 normalise(int *c) { int mp[4] = {-1, -1, -1, -1}, k = 0; u128 s = 0; for (int v = 0; v < nv; v++) { if (mp[c[v]] < 0) mp[c[v]] = k++; s |= ((u128)mp[c[v]]) << (2 * v); } return s; }
static uint64_t flood(uint64_t seed, uint64_t P) { uint64_t comp = seed, fr = seed; while (fr) { uint64_t nx = 0; uint64_t f = fr; while (f) { int v = __builtin_ctzll(f); f &= f - 1; nx |= nb[v]; } nx &= P & ~comp; comp |= nx; fr = nx; } return comp; }

typedef struct { int kind, j, L1, L2, inA, inB, N, c6[6], E[3]; long pi; int cls; int oncyc; int nmv; int dev; } Info;
static Info *inf; static long *par;
static long fnd(long a) { while (par[a] != a) { par[a] = par[par[a]]; a = par[a]; } return a; }
/* moves storage */
typedef struct { long tgt; int pr; int lmask; } Mv;
static Mv *mv; static long nmvtot, mvcap; static long *mvstart;

static int dump = 0; static int reff = 3; static long wst[16]; static int nwst;
static const int PA[6][2] = {{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}};

static void analyse(const char *name) {
  /* BFS order from link */
  int lk[5]; for (int t = 0; t < 5; t++) lk[t] = adjG[h][t];
  for (int v = 0; v < n; v++) vid[v] = -1;
  nv = 0; for (int t = 0; t < 5; t++) { vid[lk[t]] = nv; orig[nv++] = lk[t]; }
  for (int q = 0; q < nv; q++) { int u = orig[q]; for (int k = 0; k < degG[u]; k++) { int w = adjG[u][k]; if (w != h && vid[w] < 0) { vid[w] = nv; orig[nv++] = w; } } }
  for (int v = 0; v < n; v++) if (v != h && vid[v] < 0) { vid[v] = nv; orig[nv++] = v; }
  if (nv > 63) { printf("{\"name\":\"%s\",\"hole\":%d,\"err\":\"too big\"}\n", name, h); return; }
  for (int i = 0; i < nv; i++) { nb[i] = 0; int u = orig[i]; for (int k = 0; k < degG[u]; k++) { int w = adjG[u][k]; if (w != h) nb[i] |= 1ULL << vid[w]; } }
  nedge = 0; for (int i = 0; i < nv; i++) { uint64_t m = nb[i]; while (m) { int w = __builtin_ctzll(m); m &= m - 1; if (w > i) { eu[nedge] = i; ev[nedge++] = w; } } }
  /* link must be a cycle */
  for (int t = 0; t < 5; t++) if (!(nb[t] >> ((t + 1) % 5) & 1)) { printf("{\"name\":\"%s\",\"hole\":%d,\"err\":\"link not cycle\"}\n", name, h); return; }
  ns = 0; overflow = 0; reccalls = 0; for (long k = 0; k < hcap; k++) ht[k] = -1;
  rec(0, 0);
  if (overflow) { printf("{\"name\":\"%s\",\"hole\":%d,\"err\":\"overflow\",\"states\":%ld}\n", name, h, ns); fflush(stdout); return; }
  inf = realloc(inf, (ns + 1) * sizeof(Info)); par = realloc(par, (ns + 1) * sizeof(long)); mvstart = realloc(mvstart, (ns + 2) * sizeof(long));
  for (long i = 0; i < ns; i++) par[i] = i;
  nmvtot = 0; long filledTot = 0;
  for (long i = 0; i < ns; i++) {
    int c[MAXN]; uint64_t M[4] = {0, 0, 0, 0};
    for (int v = 0; v < nv; v++) { c[v] = getc_(st[i], v); M[c[v]] |= 1ULL << v; }
    Info *I = &inf[i]; memset(I, 0, sizeof(Info)); I->pi = -1; I->j = -1;
    int lc[5]; for (int t = 0; t < 5; t++) lc[t] = c[t];
    int used = 0; for (int t = 0; t < 5; t++) used |= 1 << lc[t];
    int al = -1, mu = -1, A = -1, B = -1, j = -1;
    if (__builtin_popcount(used) < 4) { I->kind = 0; filledTot++; }
    else {
      for (int t = 0; t < 5; t++) if (lc[t] == lc[(t + 2) % 5]) j = t;
      I->j = j; al = lc[j]; mu = lc[(j + 1) % 5]; A = lc[(j + 3) % 5]; B = lc[(j + 4) % 5];
      int x0 = j, x1 = (j + 1) % 5, x2 = (j + 2) % 5, x3 = (j + 3) % 5, x4 = (j + 4) % 5;
      uint64_t KmA = flood(1ULL << x1, M[mu] | M[A]), KmB = flood(1ULL << x1, M[mu] | M[B]);
      uint64_t KA = flood(1ULL << x2, M[al] | M[A]), KB = flood(1ULL << x2, M[al] | M[B]);
      I->L1 = (KmA >> x3) & 1; I->L2 = (KmB >> x4) & 1; I->inA = (KA >> x0) & 1; I->inB = (KB >> x0) & 1;
      I->kind = (I->L1 && I->L2) ? 1 : ((I->L1 || I->L2) ? 2 : 3);
      if (!I->inA) { int d[MAXN]; memcpy(d, c, sizeof(int) * nv); uint64_t m = KA; while (m) { int v = __builtin_ctzll(m); m &= m - 1; d[v] = (c[v] == al) ? A : al; } I->pi = lookup(normalise(d)); }
      /* H3 */
      for (int e = 0; e < nedge; e++) { int p = c[eu[e]], q = c[ev[e]]; int s = (1 << p) | (1 << q);
        if (s == ((1 << al) | (1 << mu)) || s == ((1 << A) | (1 << B))) I->E[0]++; else if (s == ((1 << al) | (1 << A)) || s == ((1 << mu) | (1 << B))) I->E[1]++; else I->E[2]++; }
    }
    { /* Track N: sphere constants of Lemma E (general form, every state): E_m = nv - 1 - (5 - l_m)/2 for the three
         perfect matchings m of K4 ({01|23},{02|13},{03|12}); l_m = link edges in m.  dev = sum |E_m - target_m|. */
      int Em[3] = {0, 0, 0}, lm[3] = {0, 0, 0}; static const int MT[4][4] = {{-1,0,1,2},{0,-1,2,1},{1,2,-1,0},{2,1,0,-1}};
      for (int e = 0; e < nedge; e++) Em[MT[c[eu[e]]][c[ev[e]]]]++;
      for (int t = 0; t < 5; t++) lm[MT[lc[t]][lc[(t + 1) % 5]]]++;
      int dv = 0; for (int m = 0; m < 3; m++) { int tg2 = 2 * (nv - 1) - (5 - lm[m]); dv += abs(2 * Em[m] - tg2); } I->dev = dv / 2 + (dv & 1);
    }
    /* role index of colour pair */
    int roleof[4][4]; memset(roleof, -1, sizeof roleof);
    if (I->kind) { int R[6][2] = {{al, mu}, {A, B}, {al, A}, {mu, B}, {al, B}, {mu, A}}; for (int r = 0; r < 6; r++) { roleof[R[r][0]][R[r][1]] = r; roleof[R[r][1]][R[r][0]] = r; } }
    mvstart[i] = nmvtot; int Ntot = 0;
    for (int pp = 0; pp < 6; pp++) {
      int p = PA[pp][0], q = PA[pp][1]; uint64_t P = M[p] | M[q], left = P; int cnt = 0;
      while (left) { uint64_t K = flood(left & -left, P); left &= ~K; cnt++;
        int d[MAXN]; memcpy(d, c, sizeof(int) * nv); uint64_t m = K; while (m) { int v = __builtin_ctzll(m); m &= m - 1; d[v] = (c[v] == p) ? q : p; }
        long k = lookup(normalise(d));
        long a = fnd(i), b = fnd(k); if (a != b) par[a] = b;
        if (nmvtot >= mvcap) { mvcap *= 2; mv = realloc(mv, mvcap * sizeof(Mv)); }
        mv[nmvtot].tgt = k; mv[nmvtot].pr = I->kind ? roleof[p][q] : pp; mv[nmvtot].lmask = (int)(K & 31); nmvtot++; }
      Ntot += cnt; if (I->kind) I->c6[roleof[p][q]] = cnt;
    }
    I->N = Ntot;
  }
  mvstart[ns] = nmvtot;
  for (long i = 0; i < ns; i++) inf[i].cls = (int)fnd(i);
  /* all-DL pi cycles */
  char *mark = calloc(ns, 1); long *path = malloc(ns * sizeof(long)); long *pos = malloc(ns * sizeof(long)); for (long i = 0; i < ns; i++) pos[i] = -1;
  int ncyc = 0; int cyclen[4096];
  for (long i = 0; i < ns; i++) {
    if (inf[i].kind != 1 || mark[i]) continue;
    long L = 0, k = i;
    while (k >= 0 && inf[k].kind == 1 && pos[k] < 0 && !mark[k]) { pos[k] = L; path[L++] = k; k = inf[k].pi; }
    if (k >= 0 && pos[k] >= 0) { for (long t = pos[k]; t < L; t++) { inf[path[t]].oncyc = 1; } if (ncyc < 4096) cyclen[ncyc] = (int)(L - pos[k]); ncyc++; }
    for (long t = 0; t < L; t++) { mark[path[t]] = 1; pos[path[t]] = -1; }
  }
  /* class stats */
  long *cs = calloc(ns, sizeof(long) * 15); /* indexed by root */
  long *kmin = malloc(ns * sizeof(long)), *kmax = calloc(ns, sizeof(long)); for (long i = 0; i < ns; i++) kmin[i] = 1 << 30;
  for (long i = 0; i < ns; i++) {
    Info *I = &inf[i]; long *s = cs + 15 * I->cls;
    s[0]++; if (I->kind == 0) s[1]++; if (I->kind == 1) s[2]++; if (I->oncyc) { s[3]++; if (I->N > 9) s[13] += I->N - 9; if (I->N == 8) s[4]++; else if (I->N == 9) s[5]++; else s[6]++; }
    if (I->kind == 1 && I->pi >= 0) { int d = (inf[I->pi].N - I->N) & 1; if (d != (inf[I->pi].kind == 1)) s[7]++; }
    if (I->kind) {
      for (long m = mvstart[i]; m < mvstart[i + 1]; m++) if (mv[m].lmask == 0) { Info *T = &inf[mv[m].tgt]; if (T->kind) { int a = (I->N + (I->kind == 1 || I->kind == 2 ? 0 : 0) + I->L1 + I->L2) & 1, b = (T->N + T->L1 + T->L2) & 1; if (a != b) s[8]++; } }
      if (!(I->E[0] == I->E[1] + 1 && I->E[1] == I->E[2])) s[9]++;
      s[14] += abs(I->E[0] - I->E[1] - 1) + abs(I->E[1] - I->E[2]);
      if (I->kind >= 2) s[12]++;
    }
    /* Kempe degree = distinct targets other than self */
    int deg = 0; for (long m = mvstart[i]; m < mvstart[i + 1]; m++) { long t = mv[m].tgt; if (t == i) continue; int dup = 0; for (long m2 = mvstart[i]; m2 < m; m2++) if (mv[m2].tgt == t) { dup = 1; break; } if (!dup) deg++; }
    if (deg < kmin[I->cls]) kmin[I->cls] = deg; if (deg > kmax[I->cls]) kmax[I->cls] = deg;
  }
  /* near-rigid set R = {DL, N <= 9}: longest pi-run inside R, pi-cycle inside R, in-shape N=9 states and in-shape P1 swap pairs */
  long *pre = malloc(ns * sizeof(long)); for (long i = 0; i < ns; i++) pre[i] = -1;
  for (long i = 0; i < ns; i++) if (inf[i].kind == 1 && inf[i].pi >= 0) pre[inf[i].pi] = i;
  #define INR(x) ((x) >= 0 && inf[x].kind == 1 && inf[x].N <= 9)
  #define RIG(x) ((x) >= 0 && inf[x].kind == 1 && inf[x].N == 8)
  long Rrun = 0, Rstates = 0; int Rcyc = 0; long inshape = 0, inpairs = 0, inshapeAB = 0, inshapeP23 = 0;
  for (long i = 0; i < ns; i++) { if (!INR(i)) continue; Rstates++;
    if (INR(pre[i])) { /* not a run start unless on a cycle: detect by walking back bounded */ long x = pre[i], L = 0; while (INR(x) && x != i && L <= ns) { x = pre[x]; L++; } if (x != i) continue; }
    long L = 1, x = inf[i].pi; while (INR(x) && x != i && L <= ns) { L++; x = inf[x].pi; }
    if (x == i) Rcyc = 1;
    if (L > Rrun) Rrun = L; }
  char *shp = calloc(ns, 1);
  for (long i = 0; i < ns; i++) if (inf[i].kind == 1 && inf[i].N == 9 && RIG(inf[i].pi) && RIG(pre[i])) { shp[i] = 1; inshape++; if (inf[i].c6[1] == 2) inshapeAB++; if (inf[i].c6[2] + inf[i].c6[3] + inf[i].c6[4] + inf[i].c6[5] != 6) inshapeP23++; }
  for (long i = 0; i < ns; i++) if (shp[i]) { int ok = 0; for (long m = mvstart[i]; m < mvstart[i + 1]; m++) if (mv[m].lmask == 0 && (mv[m].pr == 0 || mv[m].pr == 1) && mv[m].tgt != i && shp[mv[m].tgt]) ok = 1; inpairs += ok; }
  /* ---- Track N additions ---- */
  { long *pr2 = malloc(ns * sizeof(long)); for (long i = 0; i < ns; i++) pr2[i] = -1;
    for (long i = 0; i < ns; i++) if (inf[i].kind == 1 && inf[i].pi >= 0) pr2[inf[i].pi] = i;
    char *vis = malloc(ns);
    long runL[4] = {0, 0, 0, 0}, runRoot[4] = {-1, -1, -1, -1}; long cycL[4] = {0, 0, 0, 0}; long cycRoot[4] = {-1, -1, -1, -1};
    for (int f = 0; f < 4; f++) {
      int useL = f & 1, useE = (f >> 1) & 1;
      #define GOOD(x) ((x) >= 0 && inf[x].kind == 1 && inf[x].N <= 9 && (!useE || inf[x].dev == 0))
      #define LAWOK(x) ((((inf[inf[x].pi].N - inf[x].N) & 1) == (inf[inf[x].pi].kind == 1)))
      #define EDGE(x) (GOOD(x) && inf[x].pi >= 0 && GOOD(inf[x].pi) && (!useL || LAWOK(x)))
      memset(vis, 0, ns);
      for (long i = 0; i < ns; i++) { if (!GOOD(i)) continue; long p = pr2[i]; if (p >= 0 && EDGE(p)) continue;
        long L = 1, x = i; vis[x] = 1; while (EDGE(x)) { x = inf[x].pi; vis[x] = 1; L++; }
        if (L > runL[f]) { runL[f] = L; runRoot[f] = i; } }
      for (long i = 0; i < ns; i++) { if (!GOOD(i) || vis[i]) continue; /* remaining good states lie on cycles of EDGE */
        long L = 0, x = i; while (!vis[x]) { vis[x] = 1; L++; if (!EDGE(x)) { L = -1; break; } x = inf[x].pi; }
        if (L > 0 && x == i) { if (L > cycL[f]) { cycL[f] = L; cycRoot[f] = i; } if (L > runL[f]) { runL[f] = L; runRoot[f] = i; } } }
    }
    /* class-wide dev */
    long *cdev = calloc(ns, sizeof(long)), *cviol = calloc(ns, sizeof(long)), *csz = calloc(ns, sizeof(long));
    for (long i = 0; i < ns; i++) { cdev[inf[i].cls] += inf[i].dev; cviol[inf[i].cls] += inf[i].dev > 0; csz[inf[i].cls]++; }
    /* best all-DL cycle by penalty P_f = excess + [f&2] dev + [f&1] lawfail, for f = 0..3 */
    long bc[4][8]; for (int f = 0; f < 4; f++) bc[f][0] = -1; char prof[4][4200];
    memset(vis, 0, ns);
    for (long i = 0; i < ns; i++) { if (!inf[i].oncyc || vis[i]) continue;
      long L = 0, exc = 0, dv = 0, lw = 0, x = i;
      do { vis[x] = 1; L++; if (inf[x].N > 9) exc += inf[x].N - 9; dv += inf[x].dev; if (!LAWOK(x)) lw++; x = inf[x].pi; } while (x != i && L <= ns);
      for (int f = 0; f < 4; f++) { long P = exc + ((f & 2) ? dv : 0) + ((f & 1) ? lw : 0);
        if (bc[f][0] < 0 || P < bc[f][0]) { long c = inf[i].cls; bc[f][0] = P; bc[f][1] = L; bc[f][2] = exc; bc[f][3] = dv; bc[f][4] = lw; bc[f][5] = csz[c]; bc[f][6] = cdev[c]; bc[f][7] = cviol[c];
          int k = 0; x = i; do { if (k < 4000) { int Nn = inf[x].N; prof[f][k++] = Nn < 10 ? '0' + Nn : (Nn < 36 ? 'a' + Nn - 10 : '+'); } x = inf[x].pi; } while (x != i); prof[f][k] = 0; } } }
    /* window penalty: all-DL pi-paths (maximal) and cycles; best window of W = 10 consecutive states,
       P = sum max(0,N-9) + [E] dev + [L] law fails on the W-1 internal steps + 3 per missing state (path shorter than W) */
    long win[4] = {-1, -1, -1, -1}; long winL[4] = {0, 0, 0, 0}; nwst = 0;
    { const int W = 10; long *seq = malloc((ns + W + 1) * sizeof(long)); memset(vis, 0, ns);
      #define ISDL(x) ((x) >= 0 && inf[x].kind == 1)
      for (int pass = 0; pass < 2; pass++)
      for (long i = 0; i < ns; i++) { if (!ISDL(i) || vis[i]) continue;
        long p = pr2[i]; if (pass == 0 && ISDL(p)) continue; /* pass 0: path starts; pass 1: leftover = cycles */
        long L = 0, x = i; int cyc = 0;
        while (ISDL(x) && !vis[x]) { vis[x] = 1; seq[L++] = x; x = inf[x].pi; }
        if (x == i && L > 0) cyc = 1;
        if (cyc) { for (long t = 0; t < W && t < L; t++) seq[L + t] = seq[t]; }
        for (int f = 0; f < 4; f++) {
          long best = -1, bestlen = 0, bs0 = 0;
          long starts = (cyc ? L : (L >= W ? L - W + 1 : 1));
          for (long s0 = 0; s0 < starts; s0++) {
            long len = cyc ? (L < W ? L : W) : (L - s0 < W ? L - s0 : W); long P = 0;
            for (long t = 0; t < len; t++) { long y = seq[s0 + t]; if (inf[y].N > 9) P += inf[y].N - 9; if (f & 2) P += inf[y].dev;
              if ((f & 1) && (t < len - 1 || (cyc && L <= W)) && !LAWOK(y)) P++; }
            if (!cyc) P += 3 * (W - len);
            if (best < 0 || P < best) { best = P; bestlen = len; bs0 = s0; } }
          if (win[f] < 0 || best < win[f]) { win[f] = best; winL[f] = bestlen; if (f == reff) { nwst = (int)bestlen; for (int t = 0; t < bestlen; t++) wst[t] = seq[bs0 + t]; } } } }
      free(seq); }
    printf("{\"tn\":1,\"win\":[%ld,%ld,%ld,%ld],\"nedge\":%d,", win[0], win[1], win[2], win[3], nedge);
    printf("\"winL\":[%ld,%ld,%ld,%ld],\"run\":[%ld,%ld,%ld,%ld],\"cyc\":[%ld,%ld,%ld,%ld]", winL[0], winL[1], winL[2], winL[3], runL[0], runL[1], runL[2], runL[3], cycL[0], cycL[1], cycL[2], cycL[3]);
    for (int f = 0; f < 4; f++) { long r = cycL[f] ? cycRoot[f] : runRoot[f]; if (r >= 0) { long c = inf[r].cls; printf(",\"cls%d\":[%ld,%ld,%ld,%ld]", f, r, csz[c], cdev[c], cviol[c]); } }
    if (bc[0][0] >= 0) { printf(",\"bc\":["); for (int f = 0; f < 4; f++) printf("%s[%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,\"%s\"]", f ? "," : "", bc[f][0], bc[f][1], bc[f][2], bc[f][3], bc[f][4], bc[f][5], bc[f][6], bc[f][7], prof[f]); printf("]"); }
    /* colourings (by original vertex index, h = '-') of the states of the best window for f = reff */
    printf(",\"ref\":[");
    for (int t = 0; t < nwst; t++) { char buf[MAXN + 1]; for (int v = 0; v < n; v++) buf[v] = '-';
      for (int v = 0; v < nv; v++) buf[orig[v]] = '0' + getc_(st[wst[t]], v); buf[n] = 0; printf("%s\"%s\"", t ? "," : "", buf); }
    printf("]}\n");
    free(pr2); free(vis); free(cdev); free(cviol); free(csz);
  }
  free(pre); free(shp);
  printf("{\"name\":\"%s\",\"hole\":%d,\"n\":%d,\"states\":%ld,\"filled\":%ld,\"R\":%ld,\"Rrun\":%ld,\"Rcyc\":%d,\"inshape\":%ld,\"inshape_sigma_closed\":%ld,\"inshape_extraAB\":%ld,\"inshape_extraP23\":%ld,\"ncyc\":%d,\"cyclens\":[", name, h, n, ns, filledTot, Rstates, Rrun, Rcyc, inshape, inpairs, inshapeAB, inshapeP23, ncyc);
  for (int t = 0; t < ncyc && t < 4096; t++) printf("%s%d", t ? "," : "", cyclen[t]);
  printf("],\"cls\":[");
  int first = 1;
  for (long r = 0; r < ns; r++) { long *s = cs + 15 * r; if (s[0] == 0 || s[3] == 0) continue;
    printf("%s[%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld]", first ? "" : ",", s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], kmin[r], kmax[r], s[12], s[13], s[14], r); first = 0; }
  printf("]}\n");
  if (dump) {
    for (long i = 0; i < ns; i++) { Info *I = &inf[i];
      printf("S %ld %d %d %d %d %d %d %d %ld %d %d,%d,%d,%d,%d,%d %d %d,%d,%d %d", i, I->cls, I->kind, I->j, I->L1, I->L2, I->inA, I->inB, I->pi, I->N,
             I->c6[0], I->c6[1], I->c6[2], I->c6[3], I->c6[4], I->c6[5], I->oncyc, I->E[0], I->E[1], I->E[2], I->dev);
      { char buf[MAXN + 1]; for (int v = 0; v < n; v++) buf[v] = '-'; for (int v = 0; v < nv; v++) buf[orig[v]] = '0' + getc_(st[i], v); buf[n] = 0; printf(" %s", buf); }
      printf(" |");
      for (long m = mvstart[i]; m < mvstart[i + 1]; m++) printf(" %ld:%d:%d", mv[m].tgt, mv[m].pr, mv[m].lmask);
      printf("\n"); }
    printf("END\n");
  }
  fflush(stdout);
  free(mark); free(path); free(pos); free(cs); free(kmin); free(kmax);
}

int main(int argc, char **argv) {
  int allholes = 0, hole = 0;
  for (int a = 1; a < argc; a++) { if (!strcmp(argv[a], "--dump")) dump = 1; else if (!strcmp(argv[a], "--allholes")) allholes = 1; else if (!strcmp(argv[a], "--hole")) hole = atoi(argv[++a]); else if (!strcmp(argv[a], "--reff")) reff = atoi(argv[++a]); else if (!strcmp(argv[a], "--maxstates")) maxstates = atol(argv[++a]); }
  cap = 1 << 16; st = malloc(cap * sizeof(u128)); hcap = 1; while (hcap < 2 * maxstates + 16) hcap <<= 1; ht = malloc(hcap * sizeof(long));
  mvcap = 1 << 16; mv = malloc(mvcap * sizeof(Mv));
  static char line[1 << 20];
  while (fgets(line, sizeof line, stdin)) {
    char name[256]; int nn; char *p = line; int off;
    if (sscanf(p, "%255s %d %n", name, &nn, &off) < 2) continue;
    p += off; n = nn; memset(degG, 0, sizeof degG);
    for (int v = 0; v < n; v++) { while (*p && *p != ';' && *p != ' ' && *p != '\n') { int x, o2; if (sscanf(p, "%d%n", &x, &o2) < 1) break; adjG[v][degG[v]++] = x; p += o2; if (*p == ',') p++; } if (*p == ';') p++; }
    if (allholes) { for (int v = 0; v < n; v++) if (degG[v] == 5) { h = v; analyse(name); } }
    else { h = hole; if (degG[h] == 5) analyse(name); else { printf("{\"name\":\"%s\",\"err\":\"hole deg\"}\n", name); fflush(stdout); } }
  }
  return 0;
}
