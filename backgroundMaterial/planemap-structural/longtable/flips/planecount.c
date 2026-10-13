/* planecount.c -- exact P(G,4) for EVERY embedded spanning subgraph G of every sphere
 * triangulation on n vertices (every simple plane graph on n>=3 vertices arises this way).
 * Method: histogram h[M] over 4-colourings (c0=0) of the monochromatic edge set M, then a
 * subset-sum (zeta) transform: #colourings proper on S = g[~S].  P(G,4) = 4*g[~S].
 * Per subset: connectivity, 2-connectivity (no face walk repeats a vertex), 3-connectivity
 * (2-conn and any two faces meet in nothing, a vertex, or one common edge), face sizes.
 * Output: per (class, face signature) the minimum of P(G,4), with one witness.
 * Optional lemma test (argv[2]=1): for 2-connected G with a face of size >= 4, is there a chord
 * e=uw of a face (u,w non-adjacent) with P(G/e) >= P(G+e), i.e. #(c(u)=c(w)) >= P(G)/2 ?
 * Also the weak lemma W: some face chord e has P(G/e) >= 24*2^(miss-1) (half the bound), reported
 * for class 3 (2-connected, every 2-cut an edge) separately.
 * Usage: planecount [lemma] < tri-n.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXN 12
static int n, m, rot[MAXN][MAXN], deg[MAXN], eid[MAXN][MAXN], eu[40], ev[40];
typedef struct { uint64_t key; int cls; long minP; int tri; uint32_t S; long cnt; } Ent;
#define HS (1<<20)
static Ent *tab;
static Ent *get(uint64_t key, int cls) {
  uint64_t h = (key * 0x9E3779B97F4A7C15ULL ^ cls) & (HS - 1);
  while (tab[h].cnt && !(tab[h].key == key && tab[h].cls == cls)) h = (h + 1) & (HS - 1);
  if (!tab[h].cnt) { tab[h].key = key; tab[h].cls = cls; tab[h].minP = 1L << 62; }
  return &tab[h];
}
int main(int argc, char **argv) {
  int lemma = argc > 1 ? atoi(argv[1]) : 0;
  tab = calloc(HS, sizeof(Ent));
  char line[4096]; int t = 0;
  long w3_tested = 0, w3_fail = 0, s3_fail = 0; long lem_tested = 0, lem_fail = 0, lem_fail3 = 0, lem_tested3 = 0;
  long pfail[5] = {0}, tested[5] = {0}; /* bound P>=24*2^miss by class 1=conn,2=2conn,3=3conn */
  while (fgets(line, sizeof line, stdin)) {
    char *p = line; n = strtol(p, &p, 10);
    for (int v = 0; v < n; v++) { deg[v] = 0; while (*p == ' ') p++;
      while (1) { rot[v][deg[v]++] = strtol(p, &p, 10); if (*p == ',') p++; else break; } }
    m = 0; for (int u = 0; u < n; u++) for (int i = 0; i < deg[u]; i++) { int v = rot[u][i];
      if (u < v) { eid[u][v] = eid[v][u] = m; eu[m] = u; ev[m] = v; m++; } }
    uint32_t full = (m == 32) ? 0xffffffffu : ((1u << m) - 1);
    size_t NS = (size_t)1 << m;
    int32_t *g = calloc(NS, 4);
    int c[MAXN]; long ncol = 1; for (int i = 1; i < n; i++) ncol *= 4;
    for (long x = 0; x < ncol; x++) { long y = x; c[0] = 0; for (int i = 1; i < n; i++) { c[i] = y & 3; y >>= 2; }
      uint32_t M = 0; for (int e = 0; e < m; e++) if (c[eu[e]] == c[ev[e]]) M |= 1u << e; g[M]++; }
    for (int b = 0; b < m; b++) for (size_t X = 0; X < NS; X++) if (X >> b & 1) g[X] += g[X ^ ((size_t)1 << b)];
    int npair = n * (n - 1) / 2; int pu[80], pw[80], pidx[MAXN][MAXN], q = 0;
    for (int u = 0; u < n; u++) for (int w = u + 1; w < n; w++) { pu[q] = u; pw[q] = w; pidx[u][w] = pidx[w][u] = q; q++; }
    uint64_t *chm = lemma ? calloc(NS, 8) : NULL; uint8_t *ok = lemma ? calloc(NS, 1) : NULL;
    for (size_t S = 0; S < NS; S++) {
      int E = __builtin_popcount((uint32_t)S);
      /* connectivity */
      int par[MAXN]; for (int i = 0; i < n; i++) par[i] = i;
      for (int e = 0; e < m; e++) if (S >> e & 1) { int a = eu[e], b = ev[e]; while (par[a] != a) a = par[a]; while (par[b] != b) b = par[b]; par[a] = b; }
      int comps = 0; for (int i = 0; i < n; i++) if (par[i] == i) comps++;
      if (comps > 1) continue;
      /* faces: filtered rotations */
      int fr[MAXN][MAXN], fd[MAXN], pos[MAXN][MAXN];
      for (int v = 0; v < n; v++) { fd[v] = 0; for (int i = 0; i < deg[v]; i++) { int w = rot[v][i]; if (S >> eid[v][w] & 1) { pos[v][w] = fd[v]; fr[v][fd[v]++] = w; } } }
      static uint8_t used[MAXN][MAXN]; memset(used, 0, sizeof used);
      int nf = 0, fsz[64], fv[64][2 * MAXN * 3], twoc = 1;
      for (int v = 0; v < n; v++) for (int i = 0; i < fd[v]; i++) { int w = fr[v][i]; if (used[v][w]) continue;
        int a = v, b = w, len = 0; uint32_t seen = 0;
        while (!used[a][b]) { used[a][b] = 1; if (seen >> a & 1) twoc = 0; seen |= 1u << a; fv[nf][len++] = a;
          int j = pos[b][a]; int nx = fr[b][(j + 1) % fd[b]]; a = b; b = nx; }
        fsz[nf++] = len; }
      int miss = 3 * n - 6 - E;
      long P = 4L * g[full & ~(uint32_t)S];
      /* classes (nested): 1 connected, 2 2-connected, 3 2-connected and every 2-cut {x,y} is an
         edge of G (no two faces share a non-adjacent pair), 4 3-connected (any two faces meet in
         nothing, one vertex, or one common edge) */
      int cls = 1;
      if (twoc && n >= 3) { cls = 2; int c3 = 1, c4 = 1;
        for (int f1 = 0; f1 < nf; f1++) for (int f2 = f1 + 1; f2 < nf; f2++) {
          uint32_t A = 0, B = 0; for (int i = 0; i < fsz[f1]; i++) A |= 1u << fv[f1][i]; for (int i = 0; i < fsz[f2]; i++) B |= 1u << fv[f2][i];
          uint32_t I = A & B; int k = __builtin_popcount(I);
          if (k < 2) continue;
          /* every shared pair adjacent? */
          for (int x = 0; x < n; x++) if (I >> x & 1) for (int y = x + 1; y < n; y++) if (I >> y & 1) {
            int adjG = 0; for (int i = 0; i < fd[x]; i++) if (fr[x][i] == y) adjG = 1;
            if (!adjG) c3 = 0; }
          if (k >= 3) c4 = 0;
          else { int x = __builtin_ctz(I), y = 31 - __builtin_clz(I); int cons1 = 0, cons2 = 0;
            for (int i = 0; i < fsz[f1]; i++) { int a = fv[f1][i], b = fv[f1][(i + 1) % fsz[f1]]; if ((a == x && b == y) || (a == y && b == x)) cons1 = 1; }
            for (int i = 0; i < fsz[f2]; i++) { int a = fv[f2][i], b = fv[f2][(i + 1) % fsz[f2]]; if ((a == x && b == y) || (a == y && b == x)) cons2 = 1; }
            if (!(cons1 && cons2)) c4 = 0; } }
        if (c3) { cls = 3; if (c4 && n >= 4) cls = 4; } }
      /* bound test */
      for (int k = 1; k <= cls; k++) { tested[k]++; if (P < 24L << miss) pfail[k]++; }
      /* signature */
      uint64_t key = 0; for (int f = 0; f < nf; f++) if (fsz[f] >= 4) { int k = fsz[f]; if (k > 15) k = 15; key += 1ULL << (5 * (k - 4)); }
      for (int k = 1; k <= cls; k++) { Ent *en = get(key, k); en->cnt++; if (P < en->minP) { en->minP = P; en->tri = t; en->S = (uint32_t)S; } }
      if (lemma && cls >= 2 && miss > 0) {
        uint64_t cm = 0;
        for (int f = 0; f < nf; f++) if (fsz[f] >= 4) for (int i = 0; i < fsz[f]; i++) for (int j = i + 2; j < fsz[f]; j++) {
          if (i == 0 && j == fsz[f] - 1) continue; int u = fv[f][i], w = fv[f][j];
          int adj = 0; for (int r = 0; r < fd[u]; r++) if (fr[u][r] == w) adj = 1;
          if (!adj) cm |= 1ULL << pidx[u][w]; }
        chm[S] = cm; ok[S] = (uint8_t)cls; if (!cm) ok[S] = 0; }
    }
    if (lemma) {
      int32_t *h = malloc(NS * 4); uint8_t *good = calloc(NS, 1), *wgood = calloc(NS, 1);
      for (int pq = 0; pq < npair; pq++) {
        int u = pu[pq], w = pw[pq]; memset(h, 0, NS * 4);
        for (long x = 0; x < ncol; x++) { long y = x; c[0] = 0; for (int i = 1; i < n; i++) { c[i] = y & 3; y >>= 2; }
          if (c[u] != c[w]) continue;
          uint32_t M = 0; for (int e = 0; e < m; e++) if (c[eu[e]] == c[ev[e]]) M |= 1u << e; h[M]++; }
        for (int b = 0; b < m; b++) for (size_t X = 0; X < NS; X++) if (X >> b & 1) h[X] += h[X ^ ((size_t)1 << b)];
        for (size_t S = 0; S < NS; S++) if (ok[S] && (chm[S] >> pq & 1)) { long eq = h[full & ~(uint32_t)S], all = g[full & ~(uint32_t)S]; if (2 * eq >= all) good[S] = 1;
          int miss = 3 * n - 6 - __builtin_popcount((uint32_t)S); if (4 * eq >= (12L << miss)) wgood[S] = 1; }
      }
      for (size_t S = 0; S < NS; S++) if (ok[S] >= 3) { w3_tested++; if (ok[S] >= 3 && !good[S]) s3_fail++;
        if (!wgood[S]) { w3_fail++; if (w3_fail <= 6) { printf("WEAKFAIL3 tri=%d cls=%d P=%ld edges:", t, ok[S], 4L * g[full & ~(uint32_t)S]);
            for (int e = 0; e < m; e++) if (S >> e & 1) printf(" %d-%d", eu[e], ev[e]); printf("\n"); } } }
      for (size_t S = 0; S < NS; S++) if (ok[S]) { lem_tested++; if (ok[S] == 4) lem_tested3++;
        if (!good[S]) { lem_fail++; if (ok[S] == 4) lem_fail3++;
          if (lem_fail <= 6 || (ok[S] == 4 && lem_fail3 <= 6)) { printf("LEMMAFAIL tri=%d cls=%d P=%ld edges:", t, ok[S], 4L * g[full & ~(uint32_t)S]);
            for (int e = 0; e < m; e++) if (S >> e & 1) printf(" %d-%d", eu[e], ev[e]); printf("\n"); } } }
      free(h); free(good); free(wgood); free(chm); free(ok);
    }
    free(g); t++;
  }
  printf("n=%d triangulations=%d\n", n, t);
  for (int k = 1; k <= 4; k++) printf("class%d (1=connected,2=2-conn,3=2-cuts-adjacent,4=3-conn): graphs=%ld  P<24*2^miss: %ld\n", k, tested[k], pfail[k]);
  if (lemma) printf("class>=3: tested=%ld strongFail=%ld weakFail=%ld\n", w3_tested, s3_fail, w3_fail);
  if (lemma) printf("lemma(strong, class>=2): tested=%ld fails=%ld ; 3-conn tested=%ld fails=%ld\n", lem_tested, lem_fail, lem_tested3, lem_fail3);
  for (size_t i = 0; i < HS; i++) if (tab[i].cnt) { Ent *en = &tab[i];
    printf("SIG cls=%d faces>=4:", en->cls); for (int k = 4; k <= 15; k++) { int cc = (en->key >> (5 * (k - 4))) & 31; for (int r = 0; r < cc; r++) printf(" %d", k); }
    printf(" | minP=%ld count=%ld witness tri=%d edges:", en->minP, en->cnt, en->tri);
    for (int e = 0; e < 32; e++) if (en->S >> e & 1) printf(" %d", e); printf("\n"); }
  return 0;
}
