/* lemmaA.c -- (copy of dissect.c) tests one-chord induction lemmas for A' inside the A' class.
 * For H = C_n + T1 + D (k = |D \ T1| < n-3) and an admissible outside chord e (not in T1 u D,
 * crossing no chord of D):  eq(e) = #colourings of H with c(u)=c(w) = P(H/e)/12 (normalised),
 * ne(e) = #colourings with c(u)!=c(w) = P(H+e)/12.
 *   Lemma S (strong):  some e has eq(e) >= ne(e)   [P(H/e) >= P(H+e); then P(H) >= 2 P(H+e)]
 *   Lemma W (weak):    some e has eq(e) >= 2^(n-3-k) [P(H/e) >= half the A' bound for H]
 * Either lemma + A' for H+e (induction on k, base k=n-3 is the 4CT) gives A' for H.
 * Original header of dissect.c follows.
 * dissect.c -- check of the dissection bound A':
 *   for every triangulation T1 of the n-gon and every dissection D (set of
 *   pairwise non-crossing chords, drawn outside), the number of 4-colourings of
 *   C_n + T1 + D normalised by c0=0,c1=1 is >= 2^(n-2-k), k = |D \ T1|.
 * (k = n-3 with D a triangulation disjoint from T1 is the 4CT itself.)
 * T1 ranges over dihedral orbit representatives; D over all dissections (DFS).
 * Usage: dissect n   (n <= 12 runs in seconds-minutes)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 14
static int n, nT, capT;
static uint8_t (*Td)[MAXN][2];
static int cur[MAXN][2], ncur, stk[64][2], sp;
static void store(void) {
  if (nT == capT) { capT = capT ? 2 * capT : 1024; Td = realloc(Td, sizeof(*Td) * capT); }
  for (int i = 0; i < ncur; i++) { Td[nT][i][0] = cur[i][0]; Td[nT][i][1] = cur[i][1]; }
  nT++;
}
static void rec(void) {
  if (sp == 0) { store(); return; }
  sp--; int i = stk[sp][0], j = stk[sp][1];
  for (int k = i + 1; k < j; k++) {
    int s0 = sp, c0 = ncur;
    if (k - i >= 2) { cur[ncur][0]=i; cur[ncur][1]=k; ncur++; stk[sp][0]=i; stk[sp][1]=k; sp++; }
    if (j - k >= 2) { cur[ncur][0]=k; cur[ncur][1]=j; ncur++; stk[sp][0]=k; stk[sp][1]=j; sp++; }
    rec(); sp = s0; ncur = c0;
  }
  stk[sp][0] = i; stk[sp][1] = j; sp++;
}
typedef unsigned __int128 u128;
static int tri(int u, int v) { if (u > v) { int t=u; u=v; v=t; } return v * (v - 1) / 2 + u; }
static u128 code(int t, int r, int f) {
  u128 m = 0;
  for (int d = 0; d < n - 3; d++) { int u = Td[t][d][0], v = Td[t][d][1];
    if (f) { u = (n - u) % n; v = (n - v) % n; } u = (u + r) % n; v = (v + r) % n; m |= (u128)1 << tri(u, v); }
  return m;
}
static int nch, ch[128][2], W, L;
static uint64_t *cmask; /* per chord, W words */
static int inT1[128];
static long nodes, fails, tight, minslack = 1 << 30, ltested, sfail, wfail; static int curT;
static int chosen[64], nchosen;
static int crosses(int e, int f) {
  int a = ch[e][0], b = ch[e][1], c = ch[f][0], d = ch[f][1];
  if (a == c || a == d || b == c || b == d) return 0;
  return ((a < c && c < b) != (a < d && d < b));
}
static void dfs(int start, uint64_t *m, int k) {
  nodes++;
  long cnt = 0; for (int w = 0; w < W; w++) cnt += __builtin_popcountll(m[w]);
  long need = 1L << (n - 2 - k);
  if (cnt < need) { fails++; if (fails < 5) { printf("FAIL k=%d cnt=%ld D:", k, cnt); for (int i = 0; i < nchosen; i++) printf(" %d-%d", ch[chosen[i]][0], ch[chosen[i]][1]); printf("\n"); } }
  if (cnt == need) tight++;
  { int any = 0, sok = 0, wok = 0; long besteq = -1; int beste = -1;
    for (int e = 0; e < nch; e++) { if (inT1[e]) continue; int bad = 0;
      for (int i = 0; i < nchosen; i++) if (chosen[i] == e || crosses(e, chosen[i])) { bad = 1; break; }
      if (bad) continue; any = 1;
      long eq = 0; for (int w = 0; w < W; w++) eq += __builtin_popcountll(m[w] & ~cmask[e * W + w]);
      if (2 * eq >= cnt) sok = 1; if (eq >= need / 2) wok = 1; if (eq > besteq) { besteq = eq; beste = e; } }
    if (any) { ltested++; if (!sok) { sfail++; if (sfail <= 4) { printf("SFAIL k=%d cnt=%ld besteq=%ld (chord %d-%d) T1:", k, cnt, besteq, ch[beste][0], ch[beste][1]);
          for (int d = 0; d < n - 3; d++) printf(" %d-%d", Td[curT][d][0], Td[curT][d][1]); printf(" D:"); for (int i = 0; i < nchosen; i++) printf(" %d-%d", ch[chosen[i]][0], ch[chosen[i]][1]); printf("\n"); } }
      if (!wok) { wfail++; if (wfail <= 4) { printf("WFAIL k=%d cnt=%ld need=%ld besteq=%ld T1:", k, cnt, need, besteq);
          for (int d = 0; d < n - 3; d++) printf(" %d-%d", Td[curT][d][0], Td[curT][d][1]); printf(" D:"); for (int i = 0; i < nchosen; i++) printf(" %d-%d", ch[chosen[i]][0], ch[chosen[i]][1]); printf("\n"); } } } }
  uint64_t m2[64];
  for (int e = start; e < nch; e++) {
    int ok = 1; for (int i = 0; i < nchosen; i++) if (crosses(e, chosen[i])) { ok = 0; break; }
    if (!ok) continue;
    for (int w = 0; w < W; w++) m2[w] = m[w] & cmask[e * W + w];
    chosen[nchosen++] = e;
    dfs(e + 1, m2, k + !inT1[e]);
    nchosen--;
  }
}
int main(int argc, char **argv) {
  n = atoi(argv[1]);
  sp = 0; stk[0][0] = 0; stk[0][1] = n - 1; sp = 1; rec();
  for (int u = 0; u < n; u++) for (int v = u + 2; v < n; v++) if (!(u == 0 && v == n - 1)) { ch[nch][0] = u; ch[nch][1] = v; nch++; }
  L = 1 << (n - 2); W = (L + 63) / 64;
  uint32_t *lt = malloc(4 * L); cmask = malloc(8 * (size_t)nch * W);
  int reps = 0; long totnodes = 0;
  for (int t = 0; t < nT; t++) {
    u128 m0 = code(t, 0, 0); int canon = 1;
    for (int r = 0; r < n && canon; r++) for (int f = 0; f < 2; f++) if (code(t, r, f) < m0) { canon = 0; break; }
    if (!canon) continue;
    reps++; curT = t;
    /* colourings of T1: brute force over 4^(n-2) is too slow for n=12 -> build by
       peeling: generate all cycle colourings with c0=0,c1=1 recursively, prune on chords */
    int k = 0, c[MAXN]; c[0] = 0; c[1] = 1;
    /* adjacency of T1 restricted to lower-index neighbours */
    int lowadj[MAXN][MAXN], nlow[MAXN]; memset(nlow, 0, sizeof nlow);
    for (int v = 2; v < n; v++) lowadj[v][nlow[v]++] = v - 1;
    lowadj[n - 1][nlow[n - 1]++] = 0;
    for (int d = 0; d < n - 3; d++) { int u = Td[t][d][0], v = Td[t][d][1]; lowadj[v][nlow[v]++] = u; }
    /* iterative DFS */
    int pos = 2; c[2] = -1;
    while (pos >= 2) {
      c[pos]++;
      if (c[pos] > 3) { pos--; continue; }
      int ok = 1; for (int i = 0; i < nlow[pos]; i++) if (c[lowadj[pos][i]] == c[pos]) { ok = 0; break; }
      if (!ok) continue;
      if (pos == n - 1) { uint32_t w = 0; for (int i = 0; i < n; i++) w |= (uint32_t)c[i] << 2 * i; lt[k++] = w; }
      else { pos++; c[pos] = -1; }
    }
    if (k != L) { fprintf(stderr, "bad L %d\n", k); return 1; }
    memset(cmask, 0, 8 * (size_t)nch * W);
    for (int e = 0; e < nch; e++) {
      int u = ch[e][0], v = ch[e][1]; inT1[e] = 0;
      for (int d = 0; d < n - 3; d++) if (Td[t][d][0] == u && Td[t][d][1] == v) inT1[e] = 1;
      for (int i = 0; i < L; i++) if (((lt[i] >> 2 * u) & 3) != ((lt[i] >> 2 * v) & 3)) cmask[e * W + (i >> 6)] |= 1ULL << (i & 63);
    }
    uint64_t m[64]; for (int w = 0; w < W; w++) m[w] = ~0ULL;
    if (L < 64) m[0] = (1ULL << L) - 1;
    nodes = 0; nchosen = 0; dfs(0, m, 0); totnodes += nodes;
  }
  printf("lemma: tested=%ld  strongFail=%ld  weakFail=%ld\n", ltested, sfail, wfail);
  printf("n=%d T1_reps=%d dissections_per_T1=%ld checks=%ld fails=%ld tight=%ld\n", n, reps, totnodes / reps, totnodes, fails, tight);
  return 0;
}
