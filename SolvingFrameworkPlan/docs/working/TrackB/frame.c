/* [Track B] frame-class filter.
   Reads triangulations (plantri planar code on stdin, or text lines "name n r0;r1;..." with 0-based rotation lists)
   and decides, for each one:
     occfree : no Occ of DiamondP, DiamondM, C2122P, C2122M (Lean structures, via occ_sched.h generated from the .lean files)
     appfree : every Appears ![5,5,5,5] / ![6,5,5,5] has unclean tips (AppearFree, FrameAppears.lean) -- graph-only, no rotation
     rsstfree: no appearance at all (RSST class)
     nosep   : number of triangles == number of faces (2n-4), i.e. every triangle is facial
     mindeg5 : minimum degree >= 5
   Writes the frame-class graphs (mindeg5 && nosep && occfree) to stdout as "name n lists flags", and per-run counts to stderr.
   With NoSep, Lean proves occfree <=> appfree (appearFree_of_free and Occ => clean appearance); we compute both independently.
   Build: cc -O2 -o frame frame.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "occ_sched.h"
#define MAXN 128
#define MAXD 64
static int n, deg[MAXN], adj[MAXN][MAXD], pos[MAXN][MAXN];
static unsigned char A[MAXN][MAXN];
static char name[256];

static int nxt(int x, int y) { int p = pos[x][y]; return adj[x][(p + 1) % deg[x]]; }
static int prv(int x, int y) { int p = pos[x][y]; return adj[x][(p + deg[x] - 1) % deg[x]]; }

static int has_occ(const conf_t *c) {
  int asg[16];
  for (int i0 = 0; i0 < n; i0++) {
    if (deg[i0] != c->deg[0]) continue;
    for (int k = 0; k < deg[i0]; k++) {
      int i1 = adj[i0][k];
      if (deg[i1] != c->deg[1]) continue;
      for (int j = 0; j < 16; j++) asg[j] = -1;
      asg[0] = i0; asg[1] = i1; int ok = 1;
      for (int s = 0; s < c->nsteps && ok; s++) {
        int t = c->steps[s][0], x = asg[c->steps[s][1]], a = asg[c->steps[s][2]];
        if (!A[x][a]) { ok = 0; break; }
        asg[c->steps[s][3]] = t == 0 ? nxt(x, a) : prv(x, a);
      }
      if (!ok) continue;
      for (int f = 0; f < c->nfacts && ok; f++) {
        int x = asg[c->facts[f][0]], y = asg[c->facts[f][1]], z = asg[c->facts[f][2]];
        if (!A[x][y] || nxt(x, y) != z) ok = 0;
      }
      if (!ok) continue;
      for (int a = 0; a < 4 && ok; a++) if (deg[asg[a]] != c->deg[a]) ok = 0;
      for (int a = 0; a < c->L && ok; a++) for (int b = a + 1; b < c->L; b++) if (asg[a] == asg[b]) { ok = 0; break; }
      if (ok) return 1;
    }
  }
  return 0;
}

/* appearances: returns bit0 = some appearance, bit1 = some appearance with clean tips */
static int appear(int dc) { /* dc = degree of int 0 (5 diamond, 6 for 2.122) */
  int r = 0;
  for (int c0 = 0; c0 < n; c0++) {
    if (deg[c0] != dc) continue;
    for (int k = 0; k < deg[c0]; k++) {
      int c2 = adj[c0][k]; if (deg[c2] != 5) continue;
      int cm[MAXD], m = 0;
      for (int j = 0; j < deg[c0]; j++) { int t = adj[c0][j]; if (t != c2 && A[t][c2]) cm[m++] = t; }
      for (int a = 0; a < m; a++) for (int b = 0; b < m; b++) {
        int t1 = cm[a], t3 = cm[b];
        if (t1 == t3 || A[t1][t3] || deg[t1] != 5 || deg[t3] != 5) continue;
        r |= 1;
        int clean = 1;
        for (int j = 0; j < deg[t1]; j++) { int x = adj[t1][j]; if (A[t3][x] && x != c0 && x != c2) { clean = 0; break; } }
        if (clean) r |= 2;
      }
    }
  }
  return r;
}

static int ntriangles(void) {
  int t = 0;
  for (int a = 0; a < n; a++) for (int j = 0; j < deg[a]; j++) { int b = adj[a][j]; if (b <= a) continue;
    for (int l = 0; l < deg[b]; l++) { int c = adj[b][l]; if (c <= b) continue; if (A[a][c]) t++; } }
  return t;
}

static long cnt[MAXN][8]; /* per n: total, mindeg5, nosep, occfree(in mindeg5&nosep), appfree, rsstfree, mismatch */

static void process(void) {
  memset(A, 0, sizeof A);
  int md = 1000, s = 0;
  for (int v = 0; v < n; v++) { s += deg[v]; if (deg[v] < md) md = deg[v];
    for (int j = 0; j < deg[v]; j++) { A[v][adj[v][j]] = 1; pos[v][adj[v][j]] = j; } }
  if (s != 6 * n - 12) { fprintf(stderr, "not a triangulation: %s\n", name); exit(1); }
  for (int v = 0; v < n; v++) for (int j = 0; j < deg[v]; j++) if (!A[adj[v][j]][v]) { fprintf(stderr, "asym %s\n", name); exit(1); }
  cnt[n][0]++;
  if (md < 5) return; cnt[n][1]++;
  int nosep = ntriangles() == 2 * n - 4; if (!nosep) return; cnt[n][2]++;
  int occ = 0; for (int c = 0; c < NCONF && !occ; c++) occ |= has_occ(&CONFS[c]);
  int a5 = appear(5), a6 = appear(6);
  int appfree = !((a5 | a6) & 2), rsstfree = !((a5 | a6) & 1);
  if (!occ) cnt[n][3]++;
  if (appfree) cnt[n][4]++;
  if (rsstfree) cnt[n][5]++;
  if (appfree != !occ) { cnt[n][6]++; fprintf(stderr, "MISMATCH occ/app %s\n", name); }
  if (!occ) {
    printf("%s %d ", name, n);
    for (int v = 0; v < n; v++) { for (int j = 0; j < deg[v]; j++) printf(j ? ",%d" : "%d", adj[v][j]); if (v < n - 1) putchar(';'); }
    printf(" appfree=%d rsstfree=%d\n", appfree, rsstfree);
  }
}

int main(int argc, char **argv) {
  const char *tag = argc > 1 ? argv[1] : "pc";
  int c = getchar(); ungetc(c, stdin);
  if (c == '>') {
    char hdr[16]; if (fread(hdr, 1, 15, stdin) != 15 || memcmp(hdr, ">>planar_code<<", 15)) { fprintf(stderr, "bad header\n"); return 1; }
    long gi = 0;
    while ((c = getchar()) != EOF) {
      n = c; if (n == 0) { fprintf(stderr, "n>255 unsupported\n"); return 1; }
      for (int v = 0; v < n; v++) { deg[v] = 0; int x; while ((x = getchar()) != 0) adj[v][deg[v]++] = x - 1; }
      gi++; snprintf(name, sizeof name, "%s#%ld", tag, gi); process();
    }
  } else {
    static char line[1 << 16];
    while (fgets(line, sizeof line, stdin)) {
      char lists[1 << 16]; int nn;
      if (sscanf(line, "%255s %d %65535s", name, &nn, lists) != 3) continue;
      n = nn; for (int v = 0; v < n; v++) deg[v] = 0;
      int v = 0; char *p = lists;
      while (*p) { if (*p == ';') { v++; p++; continue; } if (*p == ',') { p++; continue; }
        adj[v][deg[v]++] = (int)strtol(p, &p, 10); }
      if (v != n - 1) { fprintf(stderr, "parse %s\n", name); return 1; }
      process();
    }
  }
  for (int k = 0; k < MAXN; k++) if (cnt[k][0])
    fprintf(stderr, "COUNT n=%d total=%ld mindeg5=%ld nosep=%ld occfree=%ld appfree=%ld rsstfree=%ld mismatch=%ld\n",
            k, cnt[k][0], cnt[k][1], cnt[k][2], cnt[k][3], cnt[k][4], cnt[k][5], cnt[k][6]);
  return 0;
}
