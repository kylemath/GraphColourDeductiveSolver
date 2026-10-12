/* TrackO engine (written for Track O; patterns follow TrackJL-review/rv_eng.c but no code is shared).
 *
 * pi-run bound measurement (TrackM candidate lemma R <= 5).
 *
 * Input (stdin): one graph per line "name n adj0;adj1;...;adj_{n-1}" with adj[h] in cyclic (link) order at holes.
 * Options:
 *   -H list   holes to use (comma separated); default every degree-5 vertex
 *   -M max    cap on states per hole (default 4000000); holes over the cap are reported as skipped
 *   -L k      dump detail of every maximal interior pi-run of length >= k (default 4)
 *   -k K      use only the first K degree-5 vertices (by index) as holes
 *   -D k      dump at most k long runs per hole (default 20; all are counted in longAll/longNR/runs/runsNR)
 *   -q        quick mode: one line per graph "name maxR nHolesAtMax sumInterior maxNR skipped W" (W = sum over maximal
 *             interior runs of 4^L; used by the search)
 *
 * States: proper 4-colourings of G-h up to renaming.  Representation: vertices of G-h are indexed 0..m-1 with the
 * link x_0..x_4 = indices 0..4, then BFS order; a state is the triple of colour-class bitmasks of canonical labels
 * 1,2,3 (labels by first occurrence in index order; label 0 = the rest).  Moves: swap of any component of any of
 * the six pair graphs of G-h.
 * Frame of an unfilled state: link (alpha,mu,alpha,A,B) at x_j..x_{j+4}; L1 = x_{j+3} in K_{muA}(x_{j+1}),
 * L2 = x_{j+4} in K_{muB}(x_{j+1}); DL = L1 && L2.  pi = swap K_{alphaA}(x_{j+2}) (defined iff x_j not in it),
 * pinv = swap K_{alphaB}(x_j) (defined iff x_{j+2} not in it).  N = total number of components of the six pair graphs.
 * Interior state = DL state all of whose Kempe neighbours (other than itself) are DL.
 * R = longest run of consecutive interior states along pi (-1 if some pi-cycle consists of interior states).
 * NR = longest run of consecutive DL states with N <= 9 along pi (TrackJ NRC quantity; -1 if a cycle).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 64
typedef struct { uint64_t a, b, c; } Key;
static int n, h, m, deg[MAXN], adj[MAXN][MAXN];
static int idx_of[MAXN], vert_of[MAXN];
static uint64_t nb[MAXN], prevnb[MAXN];
static long capM = 4000000; static int Ldump = 4, quick = 0, Dcap = 20;
static char gname[512];

static Key *keys; static long ns, capns;
static long *htab; static long hcap;
static int8_t *unf, *dl, *Nn, *intr, *kdeg, *jj; static int *pi, *pinv, *pred;
static int overflow;

static inline uint64_t hk(Key k) { uint64_t x = k.a * 0x9E3779B97F4A7C15ULL ^ (k.b * 0xC2B2AE3D27D4EB4FULL) ^ (k.c + 0x165667B19E3779F9ULL);
  x ^= x >> 31; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 29; x *= 0x94D049BB133111EBULL; x ^= x >> 32; return x; }
static long lookupk(Key k) { uint64_t x = hk(k) & (hcap - 1);
  while (htab[x] >= 0) { Key *q = &keys[htab[x]]; if (q->a == k.a && q->b == k.b && q->c == k.c) return htab[x]; x = (x + 1) & (hcap - 1); }
  return -1; }
static void hins(long id) { uint64_t x = hk(keys[id]) & (hcap - 1); while (htab[x] >= 0) x = (x + 1) & (hcap - 1); htab[x] = id; }

/* canonical key from 4 colour masks */
static Key canon(const uint64_t *cm) {
  int o[4] = {0, 1, 2, 3}; int lo[4];
  for (int c = 0; c < 4; c++) lo[c] = cm[c] ? __builtin_ctzll(cm[c]) : 1000 + c;
  for (int a = 0; a < 4; a++) for (int b = a + 1; b < 4; b++) if (lo[o[b]] < lo[o[a]]) { int t = o[a]; o[a] = o[b]; o[b] = t; }
  Key k = {cm[o[1]], cm[o[2]], cm[o[3]]}; return k;
}
static void masks(long i, uint64_t *cm) { uint64_t all = (m == 64) ? ~0ULL : ((1ULL << m) - 1);
  cm[1] = keys[i].a; cm[2] = keys[i].b; cm[3] = keys[i].c; cm[0] = all & ~(cm[1] | cm[2] | cm[3]); }
static inline uint64_t flood(uint64_t seed, uint64_t P) { uint64_t comp = seed, fr = seed;
  while (fr) { uint64_t nx = 0, f = fr; while (f) { int v = __builtin_ctzll(f); f &= f - 1; nx |= nb[v]; } nx &= P & ~comp; comp |= nx; fr = nx; }
  return comp; }
static inline int colour_of(const uint64_t *cm, int v) { for (int c = 0; c < 4; c++) if (cm[c] >> v & 1) return c; return -1; }
static long swaplook(const uint64_t *cm, uint64_t K, int p, int q) {
  uint64_t w[4] = {cm[0], cm[1], cm[2], cm[3]};
  w[p] = (cm[p] & ~K) | (cm[q] & K); w[q] = (cm[q] & ~K) | (cm[p] & K);
  return lookupk(canon(w)); }

/* enumeration */
static uint64_t ecm[4];
static void rec(int i, int maxu) {
  if (overflow) return;
  if (i == m) {
    if (ns >= capM) { overflow = 1; return; }
    if (ns >= capns) { capns = capns ? capns * 2 : 65536; keys = realloc(keys, sizeof(Key) * capns); }
    Key k = {ecm[1], ecm[2], ecm[3]}; keys[ns++] = k; return; }
  int lim = maxu + 1; if (lim > 3) lim = 3;
  for (int c = 0; c <= lim; c++) {
    if (ecm[c] & prevnb[i]) continue;
    ecm[c] |= 1ULL << i; rec(i + 1, c > maxu ? c : maxu); ecm[c] &= ~(1ULL << i);
    if (overflow) return;
  }
}

static int ncomp_total(const uint64_t *cm) { int N = 0;
  for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { uint64_t P = cm[p] | cm[q];
    while (P) { uint64_t K = flood(P & -P, P); P &= ~K; N++; } }
  return N; }

/* result per hole */
typedef struct { int R, Rcyc, NR, NRcyc, ninter, ndl, nunf, noPiDL; long runs[64]; long runsNR[64]; long nint_byN[32]; long longNR, longAll; int maxRunMaxN; double W; } Res;

static int analyse_hole(Res *res, FILE *out) {
  /* index order: link first, then BFS */
  for (int v = 0; v < n; v++) idx_of[v] = -1;
  m = 0;
  for (int t = 0; t < 5; t++) { int v = adj[h][t]; idx_of[v] = m; vert_of[m++] = v; }
  for (int qi = 0; qi < m; qi++) { int v = vert_of[qi];
    for (int t = 0; t < deg[v]; t++) { int w = adj[v][t]; if (w == h || idx_of[w] >= 0) continue; idx_of[w] = m; vert_of[m++] = w; } }
  if (m != n - 1) { fprintf(stderr, "disconnected G-h %s\n", gname); return -2; }
  for (int i = 0; i < m; i++) { nb[i] = 0; int v = vert_of[i];
    for (int t = 0; t < deg[v]; t++) { int w = adj[v][t]; if (w != h) nb[i] |= 1ULL << idx_of[w]; }
    prevnb[i] = nb[i] & ((i == 0) ? 0 : ((1ULL << i) - 1)); }
  /* link must be a 5-cycle in the given order */
  for (int t = 0; t < 5; t++) if (!(nb[t] >> ((t + 1) % 5) & 1)) { fprintf(stderr, "link not a cycle %s h=%d\n", gname, h); return -2; }
  ns = 0; overflow = 0; memset(ecm, 0, sizeof ecm);
  rec(0, -1);
  if (overflow) return -1;
  hcap = 1; while (hcap < 2 * ns + 16) hcap <<= 1;
  htab = realloc(htab, sizeof(long) * hcap); memset(htab, 0xff, sizeof(long) * hcap);
  for (long i = 0; i < ns; i++) hins(i);
  unf = realloc(unf, ns); dl = realloc(dl, ns); Nn = realloc(Nn, ns); intr = realloc(intr, ns); kdeg = realloc(kdeg, ns); jj = realloc(jj, ns);
  pi = realloc(pi, sizeof(int) * ns); pinv = realloc(pinv, sizeof(int) * ns); pred = realloc(pred, sizeof(int) * ns);
  memset(res, 0, sizeof *res);
  for (long i = 0; i < ns; i++) {
    uint64_t cm[4]; masks(i, cm); pi[i] = pinv[i] = pred[i] = -1; intr[i] = 0; kdeg[i] = 0; Nn[i] = 0; dl[i] = 0; jj[i] = -1;
    int c[5]; int used = 0; for (int t = 0; t < 5; t++) { c[t] = colour_of(cm, t); used |= 1 << c[t]; }
    if (used != 15) { unf[i] = 0; continue; }
    unf[i] = 1; res->nunf++;
    int j = -1; for (int t = 0; t < 5; t++) if (c[t] == c[(t + 2) % 5]) j = t;
    jj[i] = j;
    int x0 = j, x1 = (j + 1) % 5, x2 = (j + 2) % 5, x3 = (j + 3) % 5, x4 = (j + 4) % 5;
    int al = c[x0], mu = c[x1], A = c[x3], B = c[x4];
    int L1 = flood(1ULL << x1, cm[mu] | cm[A]) >> x3 & 1;
    int L2 = flood(1ULL << x1, cm[mu] | cm[B]) >> x4 & 1;
    if (!(L1 && L2)) continue;
    dl[i] = 1; res->ndl++;
    Nn[i] = ncomp_total(cm);
    uint64_t KAA = flood(1ULL << x2, cm[al] | cm[A]);
    if (!(KAA >> x0 & 1)) pi[i] = swaplook(cm, KAA, al, A); else res->noPiDL++;
    uint64_t KBj = flood(1ULL << x0, cm[al] | cm[B]);
    if (!(KBj >> x2 & 1)) pinv[i] = swaplook(cm, KBj, al, B);
  }
  /* interior + Kempe degree of DL states */
  int nbr[512];
  for (long i = 0; i < ns; i++) {
    if (!dl[i]) continue;
    uint64_t cm[4]; masks(i, cm); int k = 0, allDL = 1;
    for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) { uint64_t P = cm[p] | cm[q], R0 = P;
      while (R0) { uint64_t K = flood(R0 & -R0, P); R0 &= ~K; if (K == P) continue;
        long t = swaplook(cm, K, p, q); if (t < 0) { fprintf(stderr, "move not found %s\n", gname); exit(3); }
        if (t == i) continue; int dup = 0; for (int z = 0; z < k; z++) if (nbr[z] == t) { dup = 1; break; }
        if (!dup && k < 512) nbr[k++] = (int)t; if (!dl[t]) allDL = 0; } }
    kdeg[i] = k > 127 ? 127 : k; intr[i] = allDL;
    if (allDL) { res->ninter++; int N = Nn[i] < 31 ? Nn[i] : 31; res->nint_byN[N]++; }
  }
  for (long i = 0; i < ns; i++) if (dl[i] && pi[i] >= 0) { if (pred[pi[i]] >= 0) { fprintf(stderr, "pi not injective %s\n", gname); } pred[pi[i]] = (int)i; }
  /* interior runs */
  char *vis = calloc(ns, 1); res->R = 0; res->maxRunMaxN = 0;
  for (long i = 0; i < ns; i++) {
    if (!intr[i]) continue; int p = pred[i]; if (p >= 0 && intr[p]) continue;
    int L = 0, maxN = 0, allNR = 1; long y = i;
    while (y >= 0 && intr[y]) { vis[y] = 1; L++; if (Nn[y] > maxN) maxN = Nn[y]; if (Nn[y] > 9) allNR = 0; y = pi[y]; }
    res->runs[L < 63 ? L : 63]++; if (allNR) res->runsNR[L < 63 ? L : 63]++; { double w = 1; for (int z = 0; z < L; z++) w *= 4; res->W += w; }
    if (L > res->R) { res->R = L; res->maxRunMaxN = maxN; } else if (L == res->R && maxN > res->maxRunMaxN) res->maxRunMaxN = maxN;
    if (L >= Ldump) { res->longAll++; if (allNR) res->longNR++;
      if (out && !quick && res->longAll <= Dcap) {
        fprintf(out, "{\"run\":1,\"g\":\"%s\",\"n\":%d,\"h\":%d,\"L\":%d,\"N\":[", gname, n, h, L);
        long z = i; int first = 1; while (z >= 0 && intr[z]) { fprintf(out, "%s%d", first ? "" : ",", Nn[z]); first = 0; z = pi[z]; }
        fprintf(out, "],\"kd\":["); z = i; first = 1; while (z >= 0 && intr[z]) { fprintf(out, "%s%d", first ? "" : ",", kdeg[z]); first = 0; z = pi[z]; }
        int pN = (p >= 0) ? Nn[p] : -1, pk = (p >= 0) ? kdeg[p] : -1;
        fprintf(out, "],\"before\":[%d,%d,%d],\"after\":[%ld,%d,%d],\"start\":%ld}\n", p, pN, pk, y, y >= 0 ? Nn[y] : -1, y >= 0 ? kdeg[y] : -1, i);
      } }
  }
  res->Rcyc = 0; for (long i = 0; i < ns; i++) if (intr[i] && !vis[i]) res->Rcyc++;
  if (res->Rcyc) res->R = -1;
  /* near-rigid runs */
  memset(vis, 0, ns); res->NR = 0;
#define NRS(x) (dl[x] && Nn[x] <= 9)
  for (long i = 0; i < ns; i++) {
    if (!NRS(i)) continue; int p = pred[i]; if (p >= 0 && NRS(p)) continue;
    int L = 0; long y = i; while (y >= 0 && NRS(y)) { vis[y] = 1; L++; y = pi[y]; }
    if (L > res->NR) res->NR = L;
  }
  res->NRcyc = 0; for (long i = 0; i < ns; i++) if (NRS(i) && !vis[i]) res->NRcyc++;
  if (res->NRcyc) res->NR = -1;
  free(vis);
  return 0;
}

static int parse(char *line) {
  char *p = strtok(line, " \t\n"); if (!p) return 0; snprintf(gname, sizeof gname, "%s", p);
  p = strtok(NULL, " \t\n"); if (!p) return 0; n = atoi(p);
  p = strtok(NULL, " \t\n"); if (!p) return 0;
  if (n > MAXN) { fprintf(stderr, "n too big %s\n", gname); return 0; }
  char *s = p; for (int v = 0; v < n; v++) { deg[v] = 0; char *e = strchr(s, ';'); if (e) *e = 0;
    char *q = s; while (*q) { adj[v][deg[v]++] = (int)strtol(q, &q, 10); if (*q == ',') q++; }
    if (e) s = e + 1; else if (v < n - 1) { fprintf(stderr, "short adj %s\n", gname); return 0; } }
  return 1;
}

int main(int argc, char **argv) {
  char *holes = NULL; int kmax = 0;
  for (int a = 1; a < argc; a++) {
    if (!strcmp(argv[a], "-H")) holes = argv[++a];
    else if (!strcmp(argv[a], "-M")) capM = atol(argv[++a]);
    else if (!strcmp(argv[a], "-L")) Ldump = atoi(argv[++a]);
    else if (!strcmp(argv[a], "-q")) quick = 1;
    else if (!strcmp(argv[a], "-D")) Dcap = atoi(argv[++a]);
    else if (!strcmp(argv[a], "-k")) kmax = atoi(argv[++a]);
  }
  static char line[1 << 20];
  while (fgets(line, sizeof line, stdin)) {
    if (!parse(line)) continue;
    int hl[MAXN], nh = 0;
    if (holes) { char tmp[4096]; snprintf(tmp, sizeof tmp, "%s", holes); for (char *t = strtok(tmp, ","); t; t = strtok(NULL, ",")) hl[nh++] = atoi(t); }
    else for (int v = 0; v < n; v++) if (deg[v] == 5 && (!kmax || nh < kmax)) hl[nh++] = v;
    int gmax = 0, gcount = 0, gmaxNR = 0, skipped = 0; long gint = 0; double gW = 0;
    for (int k = 0; k < nh; k++) {
      h = hl[k]; if (deg[h] != 5) continue;
      Res r; int st = analyse_hole(&r, stdout);
      if (st == -1) { skipped++; if (!quick) printf("{\"g\":\"%s\",\"n\":%d,\"h\":%d,\"skip\":%ld}\n", gname, n, h, capM); continue; }
      if (st < 0) continue;
      int Rv = r.R < 0 ? 999 : r.R, NRv = r.NR < 0 ? 999 : r.NR;
      if (Rv > gmax) { gmax = Rv; gcount = 1; } else if (Rv == gmax) gcount++;
      if (NRv > gmaxNR) gmaxNR = NRv; gint += r.ninter; gW += r.W;
      if (!quick) {
        printf("{\"g\":\"%s\",\"n\":%d,\"h\":%d,\"S\":%ld,\"U\":%d,\"DL\":%d,\"I\":%d,\"R\":%d,\"Rcyc\":%d,\"NR\":%d,\"NRcyc\":%d,\"noPiDL\":%d,\"RmaxN\":%d,\"longAll\":%ld,\"longNR\":%ld,\"runs\":[",
               gname, n, h, ns, r.nunf, r.ndl, r.ninter, r.R, r.Rcyc, r.NR, r.NRcyc, r.noPiDL, r.maxRunMaxN, r.longAll, r.longNR);
        int top = 63; while (top > 1 && !r.runs[top]) top--; for (int L = 1; L <= top; L++) printf("%s%ld", L > 1 ? "," : "", r.runs[L]);
        printf("],\"runsNR\":["); top = 63; while (top > 1 && !r.runs[top]) top--; for (int L = 1; L <= top; L++) printf("%s%ld", L > 1 ? "," : "", r.runsNR[L]);
        printf("],\"intN\":["); top = 31; while (top > 8 && !r.nint_byN[top]) top--; for (int N = 8; N <= top; N++) printf("%s%ld", N > 8 ? "," : "", r.nint_byN[N]);
        printf("]}\n");
      }
    }
    if (quick) printf("%s %d %d %ld %d %d %.0f\n", gname, gmax, gcount, gint, gmaxNR, skipped, gW);
    fflush(stdout);
  }
  return 0;
}
