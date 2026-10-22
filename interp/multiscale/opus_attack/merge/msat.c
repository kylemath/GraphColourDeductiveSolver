/* msat: small CDCL SAT solver (2-watched literals, 1UIP learning, VSIDS, phase saving, Luby restarts,
   activity-based learnt-clause reduction). Written for this attack because no python SAT binding is installed.
   usage: msat [conflict_budget] < file.cnf     prints "s SATISFIABLE" + "v ..." model, "s UNSATISFIABLE" or "s UNKNOWN" */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int nv, *val, *lev, *rsn, *trail, tsz, *tlim, nlev, qhead, *seen, *phase;
static double *act, inc = 1.0;
static int *heap, hsz, *hpos;
/* clause arena */
static int *ar; static long asz, acap;
/* clause: ar[c]=size, ar[c+1]=learnt, ar[c+2]=deleted, ar[c+3..] lits ; activity separate */
typedef struct { long *a; int n, cap; } vec;
static vec *wat; static long *learnts; static int nlearnts, caplearnts; static double *cact; static long cactcap;

static void vpush(vec *v, long x) { if (v->n == v->cap) { v->cap = v->cap ? 2*v->cap : 4; v->a = realloc(v->a, sizeof(long)*v->cap); } v->a[v->n++] = x; }
#define LVAL(l) (val[(l)>>1] < 0 ? -1 : (val[(l)>>1] ^ ((l)&1)))
static void hswap(int i, int j) { int a = heap[i], b = heap[j]; heap[i] = b; heap[j] = a; hpos[b] = i; hpos[a] = j; }
static void hup(int i) { while (i > 0) { int p = (i-1)/2; if (act[heap[p]] >= act[heap[i]]) break; hswap(i, p); i = p; } }
static void hdown(int i) { for (;;) { int l = 2*i+1, r = l+1, b = i; if (l < hsz && act[heap[l]] > act[heap[b]]) b = l; if (r < hsz && act[heap[r]] > act[heap[b]]) b = r; if (b == i) break; hswap(i, b); i = b; } }
static void hins(int v) { if (hpos[v] >= 0) return; heap[hsz] = v; hpos[v] = hsz; hsz++; hup(hsz-1); }
static int hpop(void) { int v = heap[0]; hsz--; hpos[v] = -1; if (hsz) { heap[0] = heap[hsz]; hpos[heap[0]] = 0; hdown(0); } return v; }
static void bump(int v) { act[v] += inc; if (act[v] > 1e100) { for (int i = 1; i <= nv; i++) act[i] *= 1e-100; inc *= 1e-100; } if (hpos[v] >= 0) hup(hpos[v]); }

static void assign(int l, long r) { int v = l>>1; val[v] = !(l&1); lev[v] = nlev; rsn[v] = (int)r; trail[tsz++] = l; }
static long addcl(int *ls, int n, int learnt) {
  if (asz + n + 3 > acap) { while (asz + n + 3 > acap) acap = acap ? 2*acap : 1<<20; ar = realloc(ar, sizeof(int)*acap); }
  long c = asz; ar[c] = n; ar[c+1] = learnt; ar[c+2] = 0; memcpy(ar+c+3, ls, sizeof(int)*n); asz += n+3;
  if (c >= cactcap) { long nc = cactcap ? cactcap : 1<<20; while (nc <= c) nc *= 2; cact = realloc(cact, sizeof(double)*nc); cactcap = nc; }
  cact[c] = 0;
  if (n >= 2) { vpush(&wat[ls[0]^1], c); vpush(&wat[ls[1]^1], c); }
  return c;
}
/* watches[x] holds clauses watching literal (x^1), i.e. to be visited when literal x becomes TRUE (its negation false) */
static long propagate(void) {
  while (qhead < tsz) {
    int p = trail[qhead++]; /* p true; clauses watching ~p */
    vec *ws = &wat[p]; int i = 0, j = 0; int fl = p^1;
    while (i < ws->n) {
      long c = ws->a[i++]; int *L = ar+c+3; int n = ar[c];
      if (ar[c+2]) continue;   /* deleted: drop watch */
      if (L[0] == fl) { L[0] = L[1]; L[1] = fl; }
      if (LVAL(L[0]) == 1) { ws->a[j++] = c; continue; }
      int k, found = 0;
      for (k = 2; k < n; k++) if (LVAL(L[k]) != 0) { L[1] = L[k]; L[k] = fl; vpush(&wat[L[1]^1], c); found = 1; break; }
      if (found) continue;
      ws->a[j++] = c;
      if (LVAL(L[0]) == 0) { while (i < ws->n) ws->a[j++] = ws->a[i++]; ws->n = j; qhead = tsz; return c; }
      assign(L[0], c);
    }
    ws->n = j;
  }
  return -1;
}
static void backtrack(int l) {
  if (nlev <= l) return;
  for (int i = tsz-1; i >= tlim[l]; i--) { int v = trail[i]>>1; phase[v] = trail[i]&1; val[v] = -1; rsn[v] = -1; hins(v); }
  tsz = tlim[l]; qhead = tsz; nlev = l;
}
static int *lbuf; static int lbn;
static int analyze(long confl) {
  int pathc = 0, p = -1, idx = tsz-1; lbn = 1;
  do {
    int *L = ar+confl+3, n = ar[confl];
    if (ar[confl+1]) cact[confl] += 1.0;
    for (int k = (p == -1 ? 0 : 1); k < n; k++) {
      int q = L[k], v = q>>1;
      if (!seen[v] && lev[v] > 0) { seen[v] = 1; bump(v); if (lev[v] >= nlev) pathc++; else lbuf[lbn++] = q; }
    }
    while (!seen[trail[idx]>>1]) idx--;
    p = trail[idx]; idx--; confl = rsn[p>>1]; seen[p>>1] = 0; pathc--;
    if (pathc > 0 && confl >= 0) { int *M = ar+confl+3; if (M[0] != p) { for (int k = 1; k < ar[confl]; k++) if (M[k] == p) { M[k] = M[0]; M[0] = p; break; } } }
  } while (pathc > 0);
  lbuf[0] = p^1;
  /* simple minimisation: drop literals whose reason is fully seen */
  int j = 1;
  for (int i = 1; i < lbn; i++) {
    int v = lbuf[i]>>1; long r = rsn[v]; int keep = 1;
    if (r >= 0) { keep = 0; int *M = ar+r+3; for (int k = 0; k < ar[r]; k++) { int u = M[k]>>1; if (u != v && !seen[u] && lev[u] > 0) { keep = 1; break; } } }
    if (keep) lbuf[j++] = lbuf[i]; else seen[v] = 0;
  }
  for (int i = 1; i < j; i++) seen[lbuf[i]>>1] = 0;
  lbn = j;
  int bl = 0, bi = 1;
  for (int i = 1; i < lbn; i++) if (lev[lbuf[i]>>1] > bl) { bl = lev[lbuf[i]>>1]; bi = i; }
  if (lbn > 1) { int t = lbuf[1]; lbuf[1] = lbuf[bi]; lbuf[bi] = t; }
  return bl;
}
static double luby(double y, int x) { int size, seq; for (size = 1, seq = 0; size < x+1; seq++, size = 2*size+1); while (size-1 != x) { size = (size-1)>>1; seq--; x = x % size; } double r = 1; while (seq-- > 0) r *= y; return r; }
static int cmpact(const void *a, const void *b) { double x = cact[*(const long*)a], y = cact[*(const long*)b]; return x < y ? -1 : x > y; }
static void reduce(void) {
  qsort(learnts, nlearnts, sizeof(long), cmpact);
  int j = 0;
  for (int i = 0; i < nlearnts; i++) {
    long c = learnts[i]; int *L = ar+c+3; int locked = (val[L[0]>>1] >= 0 && rsn[L[0]>>1] == c);
    if (i < nlearnts/2 && ar[c] > 2 && !locked) ar[c+2] = 1; else learnts[j++] = c;
  }
  nlearnts = j;
}
int main(int argc, char **argv) {
  long budget = argc > 1 ? atol(argv[1]) : -1;
  int ncl; char line[256];
  if (scanf(" p cnf %d %d", &nv, &ncl) != 2) { /* skip comments */
    while (fgets(line, sizeof line, stdin)) if (sscanf(line, " p cnf %d %d", &nv, &ncl) == 2) break; }
  val = malloc(sizeof(int)*(nv+1)); lev = calloc(nv+1, sizeof(int)); rsn = malloc(sizeof(int)*(nv+1)); trail = malloc(sizeof(int)*(nv+1));
  tlim = malloc(sizeof(int)*(nv+2)); seen = calloc(nv+1, sizeof(int)); phase = malloc(sizeof(int)*(nv+1)); act = calloc(nv+1, sizeof(double));
  heap = malloc(sizeof(int)*(nv+1)); hpos = malloc(sizeof(int)*(nv+1)); wat = calloc(2*nv+2, sizeof(vec)); lbuf = malloc(sizeof(int)*(nv+1));
  for (int v = 0; v <= nv; v++) { val[v] = -1; rsn[v] = -1; phase[v] = 1; hpos[v] = -1; }
  for (int v = 1; v <= nv; v++) hins(v);
  int *cl = malloc(sizeof(int)*(nv+1)); int cn = 0, x, unsat = 0;
  while (scanf("%d", &x) == 1) {
    if (x) { cl[cn++] = 2*abs(x) + (x < 0); continue; }
    /* dedupe / tautology */
    int taut = 0, m = 0;
    for (int i = 0; i < cn; i++) { int dup = 0; for (int k = 0; k < m; k++) { if (cl[k] == cl[i]) dup = 1; if (cl[k] == (cl[i]^1)) taut = 1; } if (!dup) cl[m++] = cl[i]; }
    cn = 0; if (taut) continue;
    if (m == 0) { unsat = 1; continue; }
    if (m == 1) { int l = cl[0]; if (LVAL(l) == 0) unsat = 1; else if (LVAL(l) < 0) assign(l, -1); continue; }
    addcl(cl, m, 0);
  }
  if (unsat || propagate() >= 0) { puts("s UNSATISFIABLE"); return 0; }
  long conflicts = 0; int rcount = 0; double rlim = luby(2, 0)*100; long nextred = 4000; int ret = 0;
  caplearnts = 1024; learnts = malloc(sizeof(long)*caplearnts);
  for (;;) {
    long confl = propagate();
    if (confl >= 0) {
      conflicts++;
      if (nlev == 0) { ret = 20; break; }
      int bl = analyze(confl);
      backtrack(bl);
      if (lbn == 1) assign(lbuf[0], -1);
      else { long c = addcl(lbuf, lbn, 1); cact[c] = 1; if (nlearnts == caplearnts) { caplearnts *= 2; learnts = realloc(learnts, sizeof(long)*caplearnts); } learnts[nlearnts++] = c; assign(lbuf[0], c); }
      inc *= 1.0/0.95;
      if (budget >= 0 && conflicts > budget) { ret = 0; break; }
      if (--rlim <= 0) { rcount++; rlim = luby(2, rcount)*100; backtrack(0); }
      if (nlearnts > nextred + tsz) { reduce(); nextred += 2000; }
    } else {
      int v = 0;
      while (hsz) { int u = hpop(); if (val[u] < 0) { v = u; break; } }
      if (!v) { ret = 10; break; }
      tlim[nlev++] = tsz; assign(2*v + phase[v], -1);
    }
  }
  if (ret == 10) {
    puts("s SATISFIABLE"); printf("v");
    for (int v = 1; v <= nv; v++) printf(" %d", val[v] ? v : -v);
    puts(" 0");
  } else if (ret == 20) puts("s UNSATISFIABLE"); else puts("s UNKNOWN");
  return 0;
}
