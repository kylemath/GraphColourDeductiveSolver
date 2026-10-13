/* baseline.c -- exhaustive check of the polygon form of 4CT.
 * For every pair (T1,T2) of triangulations of the convex n-gon, the graph
 * C_n + diag(T1) + diag(T2) is 4-colourable.
 * Method: colourings normalised by c0=0,c1=1. G = proper colourings of C_n.
 * For T1 (one per dihedral orbit) list L(T1) = colourings of G proper on T1's
 * diagonals (exactly 2^(n-2) of them). For each possible chord (u,v) build a
 * bitmask over L(T1) of colourings with c(u)!=c(v). For every T2 the common
 * colourings are the AND of the masks of T2's diagonals. We record the count
 * (= P(G,4)/12) and its minimum / histogram.
 * Usage: baseline n   (4 <= n <= 14)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 16
static int n;
static int nT = 0, capT = 0;
static uint8_t (*Tdiag)[MAXN][2]; /* n-3 diagonals each */
static int cur[MAXN][2], ncur;

static void store(void) {
  if (nT == capT) { capT = capT ? 2 * capT : 1024; Tdiag = realloc(Tdiag, sizeof(*Tdiag) * capT); }
  for (int i = 0; i < ncur; i++) { Tdiag[nT][i][0] = cur[i][0]; Tdiag[nT][i][1] = cur[i][1]; }
  nT++;
}
/* enumerate triangulations of the polygon i..j (edge (i,j) present); a list
 * of pending sub-polygons is kept as a stack */
static int stk[64][2], sp;
static void rec(void) {
  if (sp == 0) { store(); return; }
  sp--; int i = stk[sp][0], j = stk[sp][1];
  if (j - i < 2) { rec(); sp++; stk[sp-1][0]=i; stk[sp-1][1]=j; return; }
  for (int k = i + 1; k < j; k++) {
    int s0 = sp, c0 = ncur;
    if (k - i >= 2) { cur[ncur][0]=i; cur[ncur][1]=k; ncur++; stk[sp][0]=i; stk[sp][1]=k; sp++; }
    if (j - k >= 2) { cur[ncur][0]=k; cur[ncur][1]=j; ncur++; stk[sp][0]=k; stk[sp][1]=j; sp++; }
    rec();
    sp = s0; ncur = c0;
  }
  stk[sp][0] = i; stk[sp][1] = j; sp++;
}
static int pidx(int u, int v) { if (u > v) { int t=u; u=v; v=t; } return v * (v - 1) / 2 + u; } /* < 128 for n<=16 */
typedef unsigned __int128 u128;
static u128 code(int t, int r, int refl) {
  u128 m = 0;
  for (int d = 0; d < n - 3; d++) {
    int u = Tdiag[t][d][0], v = Tdiag[t][d][1];
    if (refl) { u = (n - u) % n; v = (n - v) % n; }
    u = (u + r) % n; v = (v + r) % n;
    m |= (u128)1 << pidx(u, v);
  }
  return m;
}

int main(int argc, char **argv) {
  n = atoi(argv[1]);
  /* outer polygon 0..n-1 with root edge (0,n-1) */
  sp = 0; stk[sp][0] = 0; stk[sp][1] = n - 1; sp++; ncur = 0; rec();
  /* ground set: proper colourings of C_n with c0=0,c1=1 */
  int G = 0, capG = 1 << 20; uint32_t *gs = malloc(sizeof(uint32_t) * capG); /* 2 bits per vertex */
  int c[MAXN]; c[0]=0; c[1]=1;
  /* iterative enumeration */
  long total = 1; for (int i = 2; i < n; i++) total *= 4;
  for (long x = 0; x < total; x++) {
    long y = x; int ok = 1;
    for (int i = 2; i < n; i++) { c[i] = y & 3; y >>= 2; if (c[i] == c[i-1]) { ok = 0; break; } }
    if (!ok || c[n-1] == c[0]) continue;
    uint32_t w = 0; for (int i = 0; i < n; i++) w |= (uint32_t)c[i] << (2*i);
    gs[G++] = w;
  }
  int L = 1 << (n - 2); int W = (L + 63) / 64;
  uint64_t *mask = calloc((size_t)n * n * W, sizeof(uint64_t));
  uint32_t *lt = malloc(sizeof(uint32_t) * L);
  long hist[1 << 14]; memset(hist, 0, sizeof hist);
  long pairs = 0, fails = 0; long minc = 1L << 40; int minT1 = -1, minT2 = -1; int reps = 0;
  for (int t1 = 0; t1 < nT; t1++) {
    u128 m0 = code(t1, 0, 0); int canon = 1;
    for (int r = 0; r < n && canon; r++) for (int f = 0; f < 2; f++) if (code(t1, r, f) < m0) { canon = 0; break; }
    if (!canon) continue;
    reps++;
    int k = 0;
    for (int g = 0; g < G; g++) {
      uint32_t w = gs[g]; int ok = 1;
      for (int d = 0; d < n - 3; d++) { int u = Tdiag[t1][d][0], v = Tdiag[t1][d][1];
        if (((w >> 2*u) & 3) == ((w >> 2*v) & 3)) { ok = 0; break; } }
      if (ok) lt[k++] = w;
    }
    if (k != L) { fprintf(stderr, "|L(T)|=%d != %d\n", k, L); return 1; }
    memset(mask, 0, sizeof(uint64_t) * n * n * W);
    for (int u = 0; u < n; u++) for (int v = u + 2; v < n; v++) {
      uint64_t *M = mask + (size_t)(u * n + v) * W;
      for (int i = 0; i < L; i++) if (((lt[i] >> 2*u) & 3) != ((lt[i] >> 2*v) & 3)) M[i >> 6] |= 1ULL << (i & 63);
    }
    for (int t2 = 0; t2 < nT; t2++) {
      long cnt = 0;
      for (int w = 0; w < W; w++) {
        uint64_t a = ~0ULL;
        for (int d = 0; d < n - 3; d++) a &= mask[(size_t)(Tdiag[t2][d][0] * n + Tdiag[t2][d][1]) * W + w];
        cnt += __builtin_popcountll(a);
      }
      pairs++;
      if (cnt == 0) { fails++; if (fails < 5) printf("FAIL t1=%d t2=%d\n", t1, t2); }
      if (cnt < (1 << 14)) hist[cnt]++;
      if (cnt < minc) { minc = cnt; minT1 = t1; minT2 = t2; }
    }
  }
  printf("n=%d triangulations=%d dihedral_reps=%d ground|G|=%d |L(T)|=%d density=%.6g pairs=%ld fails=%ld min_common=%ld (P(G,4)=%ld)\n",
         n, nT, reps, G, L, (double)L / G, pairs, fails, minc, 12 * minc);
  printf("hist(common count : #pairs, T1 orbit reps x all T2):");
  for (int i = 0; i < (1 << 14); i++) if (hist[i]) printf(" %d:%ld", i, hist[i]);
  printf("\nexample min pair T1:");
  for (int d = 0; d < n - 3; d++) printf(" %d-%d", Tdiag[minT1][d][0], Tdiag[minT1][d][1]);
  printf(" | T2:");
  for (int d = 0; d < n - 3; d++) printf(" %d-%d", Tdiag[minT2][d][0], Tdiag[minT2][d][1]);
  printf("\n");
  return 0;
}
