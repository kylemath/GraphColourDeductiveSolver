/* sepcyc: for each graph line "name n rot;rot;... flags" (Census frame-NN.txt format) print
 *   name s4 s5 m5
 * s4 = number of separating 4-cycles, s5 = number of nontrivial separating 5-cycles (both sides >= 2 vertices),
 * m5 = smallest side over those 5-cycles (0 if none). A 5-cycle that is the link of one vertex is trivial.
 * Cycles are counted once (smallest vertex first, second vertex < last vertex).
 * Build: cc -O2 -o sepcyc sepcyc.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 128
static int n, deg[MAXN], adj[MAXN][16];
static unsigned char A[MAXN][MAXN];
static int cyc[6], inC[MAXN];
static long s4, s5; static int m5;

static void comps(int k) {             /* components of T - C; record */
  int seen[MAXN] = {0}, q[MAXN], sizes[MAXN], nc = 0;
  for (int s = 0; s < n; s++) {
    if (inC[s] || seen[s]) continue;
    int h = 0, t = 0; q[t++] = s; seen[s] = 1;
    while (h < t) { int u = q[h++]; for (int i = 0; i < deg[u]; i++) { int w = adj[u][i]; if (!inC[w] && !seen[w]) { seen[w] = 1; q[t++] = w; } } }
    sizes[nc++] = t;
  }
  if (nc < 2) return;
  if (k == 4) { s4++; return; }
  int mn = MAXN; for (int i = 0; i < nc; i++) if (sizes[i] < mn) mn = sizes[i];
  if (mn >= 2) { s5++; if (!m5 || mn < m5) m5 = mn; }
}
static void dfs(int depth, int k) {
  int u = cyc[depth - 1];
  if (depth == k) {
    if (!A[u][cyc[0]] || cyc[1] > cyc[k - 1]) return;
    for (int i = 0; i < k; i++) for (int j = i + 2; j < k; j++) if (!(i == 0 && j == k - 1) && A[cyc[i]][cyc[j]]) return;  /* chordless */
    for (int i = 0; i < k; i++) inC[cyc[i]] = 1;
    comps(k);
    for (int i = 0; i < k; i++) inC[cyc[i]] = 0;
    return;
  }
  for (int i = 0; i < deg[u]; i++) {
    int w = adj[u][i]; if (w <= cyc[0]) continue;
    int dup = 0; for (int j = 0; j < depth; j++) if (cyc[j] == w) dup = 1; if (dup) continue;
    cyc[depth] = w; dfs(depth + 1, k);
  }
}
int main(void) {
  static char line[1 << 16], name[256];
  while (fgets(line, sizeof line, stdin)) {
    char *p = line; int off;
    if (sscanf(p, "%255s %d %n", name, &n, &off) < 2) continue; p += off;
    memset(A, 0, sizeof A);
    for (int u = 0; u < n; u++) {
      deg[u] = 0;
      while (*p >= '0' && *p <= '9') { int w = (int)strtol(p, &p, 10); adj[u][deg[u]++] = w; A[u][w] = 1; if (*p == ',') p++; }
      if (*p == ';') p++;
    }
    s4 = s5 = 0; m5 = 0;
    for (int k = 4; k <= 5; k++) for (int s = 0; s < n; s++) { cyc[0] = s; dfs(1, k); }
    printf("%s %ld %ld %d\n", name, s4, s5, m5);
  }
  return 0;
}
