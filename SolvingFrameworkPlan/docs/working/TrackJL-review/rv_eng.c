/* TrackJL-review: independent engine (written from scratch; no TrackJ/TrackL/TrackH code).
 *
 * Input (stdin): one graph per line: "name n adj0;adj1;...;adj_{n-1} [tokens]".
 *   adj[v] must list the neighbours of a hole vertex in cyclic (link) order; for other
 *   vertices the order is irrelevant.
 * Options:
 *   -E chi    : the graph is a triangulated closed surface of Euler characteristic chi;
 *               check Lemma E with constants (chi, chi+1, chi+1). Omit for general graphs.
 *   -H list   : comma-separated hole vertices to use (default: every degree-5 vertex whose
 *               neighbourhood is a 5-cycle in the given order).
 *   -k K      : use at most K holes per graph (first K in order of a per-graph shuffle).
 *   -c        : class mode (J5): Kempe classes of states on all-DL pi-cycles with N<=9.
 *   -s S      : star-identity sampling: check all Kempe moves at every S-th state (default 7).
 *   -M max    : cap on states per hole (default 3000000); holes over the cap are skipped.
 * States are proper 4-colourings of G-h up to renaming (canonical: colours by first occurrence
 * in a fixed BFS order).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 64
static int n, h, deg[MAXN], adj[MAXN][MAXN], isadj[MAXN][MAXN];
static int X[5];
static int m, ord[MAXN], pos[MAXN];
static int surf = 0, surfchi = 0, classmode = 0, starS = 7;
static long capM = 3000000;
static char gname[256];

/* ---------------- counters ---------------- */
#define MAXC 128
static const char *cname[MAXC];
static long ccheck[MAXC], cfail[MAXC];
static int nc = 0;
static int cid(const char *s) {
    for (int i = 0; i < nc; i++) if (strcmp(cname[i], s) == 0) return i;
    cname[nc] = s; return nc++;
}
static long nfailprint = 0;
static void CHECK(const char *s, int ok, const char *fmt, ...);
#include <stdarg.h>
static void CHECK(const char *s, int ok, const char *fmt, ...) {
    int i = cid(s); ccheck[i]++;
    if (!ok) {
        cfail[i]++;
        if (nfailprint < 200) {
            nfailprint++;
            va_list ap; va_start(ap, fmt);
            fprintf(stderr, "FAIL %s graph=%s h=%d : ", s, gname, h);
            vfprintf(stderr, fmt, ap); fprintf(stderr, "\n"); va_end(ap);
        }
    }
}
static void TALLY(const char *s) { int i = cid(s); ccheck[i]++; }

/* ---------------- states ---------------- */
typedef struct { uint64_t a, b; } Key;
typedef struct {
    int8_t unf, j, dl, inA, inB, l1, l2, D;
    int8_t cnt[6], chi[6], meet[6], N, extra; /* extra: role-pair index of the unique link-free comp if exactly one, else -1/-2 */
    int8_t nlinkfree;
    int pi, pinv;
} St;
static Key *keys; static St *st; static long ns, cap_ns;
static long *htab; static long hcap;

static inline uint64_t hk(Key k) { uint64_t x = k.a * 0x9E3779B97F4A7C15ULL ^ (k.b + 0x632BE59BD9B4E019ULL + (k.a >> 7));
    x ^= x >> 31; x *= 0xBF58476D1CE4E5B9ULL; x ^= x >> 29; return x; }
static Key pack(const int *col) {
    Key k = {0, 0};
    for (int i = 0; i < m; i++) { uint64_t c = (uint64_t)col[ord[i]];
        if (i < 32) k.a |= c << (2 * i); else k.b |= c << (2 * (i - 32)); }
    return k;
}
static void unpack(Key k, int *col) {
    for (int i = 0; i < m; i++) col[ord[i]] = (int)((i < 32 ? (k.a >> (2 * i)) : (k.b >> (2 * (i - 32)))) & 3);
    col[h] = -1;
}
static void canon(int *col) {
    int map[4] = {-1, -1, -1, -1}, nx = 0;
    for (int i = 0; i < m; i++) { int v = ord[i]; if (map[col[v]] < 0) map[col[v]] = nx++; }
    for (int i = 0; i < m; i++) { int v = ord[i]; col[v] = map[col[v]]; }
}
static long lookup(const int *col0) {
    int col[MAXN]; memcpy(col, col0, sizeof(int) * n); canon(col);
    Key k = pack(col); uint64_t x = hk(k) & (hcap - 1);
    while (htab[x] >= 0) { if (keys[htab[x]].a == k.a && keys[htab[x]].b == k.b) return htab[x]; x = (x + 1) & (hcap - 1); }
    return -1;
}
static void hinsert(long id) {
    uint64_t x = hk(keys[id]) & (hcap - 1);
    while (htab[x] >= 0) x = (x + 1) & (hcap - 1);
    htab[x] = id;
}

/* enumerate proper colourings of G-h up to renaming */
static int ecol[MAXN]; static int overflow;
static void addstate(void) {
    if (ns >= capM) { overflow = 1; return; }
    if (ns >= cap_ns) { cap_ns = cap_ns ? cap_ns * 2 : 4096; keys = realloc(keys, sizeof(Key) * cap_ns); }
    keys[ns++] = pack(ecol);
}
static void rec(int i, int maxu) {
    if (overflow) return;
    if (i == m) { addstate(); return; }
    int v = ord[i]; int lim = maxu + 1; if (lim > 3) lim = 3;
    for (int c = 0; c <= lim; c++) {
        int ok = 1;
        for (int t = 0; t < deg[v]; t++) { int w = adj[v][t]; if (w == h) continue; if (pos[w] < i && ecol[w] == c) { ok = 0; break; } }
        if (!ok) continue;
        ecol[v] = c; rec(i + 1, c > maxu ? c : maxu);
        if (overflow) return;
    }
}

/* components of the {p,q} pair graph of G-h */
static int comps(const int *col, int p, int q, int *comp, int *nedge) {
    int nc2 = 0, e = 0, stack[MAXN];
    for (int v = 0; v < n; v++) comp[v] = -1;
    for (int v = 0; v < n; v++) {
        if (v == h || (col[v] != p && col[v] != q) || comp[v] >= 0) continue;
        int sp = 0; stack[sp++] = v; comp[v] = nc2;
        while (sp) { int x = stack[--sp];
            for (int t = 0; t < deg[x]; t++) { int w = adj[x][t]; if (w == h) continue;
                if ((col[w] == p || col[w] == q) && col[w] != col[x]) {
                    if (x < w) e++;
                    if (comp[w] < 0) { comp[w] = nc2; stack[sp++] = w; } } } }
        nc2++;
    }
    if (nedge) *nedge = e;
    return nc2;
}
static int nverts(const int *col, int p, int q) { int k = 0; for (int v = 0; v < n; v++) if (v != h && (col[v] == p || col[v] == q)) k++; return k; }
static int chiof(const int *col, int p, int q) { int comp[MAXN], e; comps(col, p, q, comp, &e); return nverts(col, p, q) - e; }

/* frame data of a (not necessarily canonical) colouring */
typedef struct { int unf, j, al, mu, A, B; int pr[6][2]; } Frame;
static int frame(const int *col, Frame *f) {
    int used = 0; for (int t = 0; t < 5; t++) used |= 1 << col[X[t]];
    if (used != 15) { f->unf = 0; return 0; }
    int jj = -1, cntj = 0;
    for (int t = 0; t < 5; t++) if (col[X[t]] == col[X[(t + 2) % 5]]) { jj = t; cntj++; }
    if (cntj != 1) { fprintf(stderr, "frame error\n"); exit(2); }
    f->unf = 1; f->j = jj;
    f->al = col[X[jj]]; f->mu = col[X[(jj + 1) % 5]]; f->A = col[X[(jj + 3) % 5]]; f->B = col[X[(jj + 4) % 5]];
    int P[6][2] = {{f->al, f->mu}, {f->A, f->B}, {f->al, f->A}, {f->mu, f->B}, {f->al, f->B}, {f->mu, f->A}};
    memcpy(f->pr, P, sizeof P);
    return 1;
}
#define XJ(f, t) X[((f).j + (t)) % 5]

static void swapcomp(int *col, const int *comp, int k, int p, int q) {
    for (int v = 0; v < n; v++) if (comp[v] == k) col[v] = (col[v] == p) ? q : p;
}

/* full per-state analysis */
static void analyse(long i) {
    int col[MAXN]; unpack(keys[i], col);
    St *s = &st[i]; memset(s, 0, sizeof *s); s->pi = s->pinv = -1; s->extra = -1;
    Frame f;
    if (!frame(col, &f)) { s->unf = 0;
        /* N for filled states, for completeness */
        return; }
    s->unf = 1; s->j = f.j;
    int comp[6][MAXN], e[6], N = 0;
    for (int r = 0; r < 6; r++) {
        s->cnt[r] = comps(col, f.pr[r][0], f.pr[r][1], comp[r], &e[r]);
        s->chi[r] = nverts(col, f.pr[r][0], f.pr[r][1]) - e[r];
        N += s->cnt[r];
        CHECK("chi<=cnt", s->chi[r] <= s->cnt[r], "");
    }
    s->N = N;
    int x0 = XJ(f, 0), x1 = XJ(f, 1), x2 = XJ(f, 2), x3 = XJ(f, 3), x4 = XJ(f, 4);
    s->l1 = comp[5][x3] == comp[5][x1];      /* mu-A */
    s->l2 = comp[3][x4] == comp[3][x1];      /* mu-B */
    s->inA = comp[2][x0] == comp[2][x2];
    s->inB = comp[4][x2] == comp[4][x0];
    s->dl = s->l1 && s->l2;
    s->D = !s->inA && !s->inB;
    /* link-meeting components and link-free components per role pair */
    int nlf = 0, lfpair = -1, lfcomp = -1;
    for (int r = 0; r < 6; r++) {
        int seen[MAXN] = {0}, k = 0;
        for (int t = 0; t < 5; t++) { int v = X[t]; if (comp[r][v] >= 0 && !seen[comp[r][v]]) { seen[comp[r][v]] = 1; k++; } }
        s->meet[r] = k;
        for (int q = 0; q < s->cnt[r]; q++) if (!seen[q]) { nlf++; lfpair = r; lfcomp = q; }
    }
    (void)lfcomp;
    s->nlinkfree = nlf; s->extra = (nlf == 1) ? lfpair : (nlf == 0 ? -1 : -2);

    /* Lemma E */
    if (surf) {
        int a = s->chi[0] + s->chi[1], b = s->chi[2] + s->chi[3], c = s->chi[4] + s->chi[5];
        CHECK("LemmaE(Sum chi P1,P2,P3)", a == surfchi && b == surfchi + 1 && c == surfchi + 1, "got (%d,%d,%d)", a, b, c);
        if (surfchi == 2) {
            CHECK("TheoremD: Lock2<=>!inA (sphere)", s->l2 == !s->inA, "");
            CHECK("TheoremD: Lock1<=>!inB (sphere)", s->l1 == !s->inB, "");
        } else {
            TALLY("offsphere unfilled states"); if (s->l2 != !s->inA || s->l1 != !s->inB) TALLY("offsphere D-violations");
        }
    }
    /* sum of link-meeting components = 8 + ([!inA]-L2) + ([!inB]-L1) (any graph) */
    {
        int sm = 0; for (int r = 0; r < 6; r++) sm += s->meet[r];
        int pred = 8 + (!s->inA - s->l2) + (!s->inB - s->l1);
        CHECK("link-meeting total formula (any graph)", sm == pred, "sm=%d pred=%d", sm, pred);
    }
    /* J1 */
    if (s->dl && s->D) {
        int ok = s->meet[0] == 1 && s->meet[1] == 1 && s->meet[2] == 2 && s->meet[3] == 1 && s->meet[4] == 2 && s->meet[5] == 1;
        /* explicit membership */
        ok = ok && comp[0][x0] == comp[0][x1] && comp[0][x1] == comp[0][x2];
        ok = ok && comp[1][x3] == comp[1][x4];
        ok = ok && comp[2][x2] == comp[2][x3] && comp[2][x0] != comp[2][x2];
        ok = ok && comp[4][x0] == comp[4][x4] && comp[4][x0] != comp[4][x2];
        ok = ok && comp[3][x1] == comp[3][x4] && comp[5][x1] == comp[5][x3];
        CHECK("J1 link components (DL+D)", ok, "meet=%d%d%d%d%d%d", s->meet[0], s->meet[1], s->meet[2], s->meet[3], s->meet[4], s->meet[5]);
        CHECK("J1 N=8+#linkfree (DL+D)", s->N == 8 + nlf, "N=%d lf=%d", s->N, nlf);
    }
    if (s->dl && !s->D) TALLY("DL states without D");

    /* pi = swap K_{alpha A}(x_{j+2}) */
    if (!s->inA) {
        int u[MAXN]; memcpy(u, col, sizeof u);
        swapcomp(u, comp[2], comp[2][x2], f.al, f.A);
        Frame g; int uf = frame(u, &g);
        CHECK("pi(c) unfilled, frame j+3, roles (al,B,mu,A)", uf && g.j == (f.j + 3) % 5 && g.al == f.al && g.mu == f.B && g.A == f.mu && g.B == f.A, "");
        if (uf) {
            int cu[6][MAXN], eu[6], cntu[6], chiu[6];
            for (int r = 0; r < 6; r++) { cntu[r] = comps(u, g.pr[r][0], g.pr[r][1], cu[r], &eu[r]); chiu[r] = nverts(u, g.pr[r][0], g.pr[r][1]) - eu[r]; }
            /* J2: component-wise: alphaA of c == alpha_u B_u of u ; muB of c == mu_u A_u of u */
            int ok = 1;
            for (int v = 0; v < n; v++) for (int w = v + 1; w < n; w++) {
                if ((comp[2][v] >= 0) != (cu[4][v] >= 0)) ok = 0;
                if ((comp[3][v] >= 0) != (cu[5][v] >= 0)) ok = 0;
                if (comp[2][v] >= 0 && comp[2][w] >= 0 && ((comp[2][v] == comp[2][w]) != (cu[4][v] == cu[4][w]))) ok = 0;
                if (comp[3][v] >= 0 && comp[3][w] >= 0 && ((comp[3][v] == comp[3][w]) != (cu[5][v] == cu[5][w]))) ok = 0;
            }
            CHECK("J2 componentwise P2(c)=P3(pi c)", ok && cntu[4] == s->cnt[2] && cntu[5] == s->cnt[3], "");
            /* star identities across pi and the chi recursion of TrackL 2.1 (a=chi(c), b=chi(u), 1-indexed) */
            int *a = (int[6]){s->chi[0], s->chi[1], s->chi[2], s->chi[3], s->chi[4], s->chi[5]};
            int okr = chiu[4] == a[2] && chiu[5] == a[3] && chiu[1] + chiu[2] == a[0] + a[5] && chiu[0] + chiu[3] == a[1] + a[4];
            CHECK("TrackL 2.1 chi-recursion across pi", okr, "");
            /* star at mu: chi_u(mu al)+chi_u(mu A) == chi_c(mu al)+chi_c(mu A) */
            int lhs = chiof(u, f.mu, f.al) + chiof(u, f.mu, f.A), rhs = chiof(col, f.mu, f.al) + chiof(col, f.mu, f.A);
            CHECK("Star identity across pi (r=mu)", lhs == rhs, "");
            lhs = chiof(u, f.B, f.al) + chiof(u, f.B, f.A); rhs = chiof(col, f.B, f.al) + chiof(col, f.B, f.A);
            CHECK("Star identity across pi (r=B)", lhs == rhs, "");
            s->pi = lookup(u);
            CHECK("pi(c) found among states", s->pi >= 0, "");
        }
    }
    if (!s->inB) {
        int u[MAXN]; memcpy(u, col, sizeof u);
        swapcomp(u, comp[4], comp[4][x0], f.al, f.B);
        Frame g; int uf = frame(u, &g);
        CHECK("pinv(c) unfilled", uf, "");
        s->pinv = lookup(u);
    }
    /* generic star identity on all Kempe moves, sampled */
    if (starS > 0 && i % starS == 0) {
        for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) {
            int cp[MAXN]; int k = comps(col, p, q, cp, NULL);
            for (int r = 0; r < 4; r++) { if (r == p || r == q) continue;
                int base = chiof(col, r, p) + chiof(col, r, q);
                for (int t = 0; t < k; t++) {
                    int u[MAXN]; memcpy(u, col, sizeof u); swapcomp(u, cp, t, p, q);
                    CHECK("Star identity, every Kempe move (sampled states)", chiof(u, r, p) + chiof(u, r, q) == base, "");
                } }
        }
    }
}

static int isrigid(long i) { if (i < 0) return 0; St *s = &st[i];
    return s->unf && s->dl && s->cnt[0] == 1 && s->cnt[1] == 1 && s->cnt[2] == 2 && s->cnt[3] == 1 && s->cnt[4] == 2 && s->cnt[5] == 1; }

/* distinct Kempe neighbours (canonical indices, excluding i itself) */
static int kneigh(long i, long *out) {
    int col[MAXN]; unpack(keys[i], col); int k = 0;
    for (int p = 0; p < 4; p++) for (int q = p + 1; q < 4; q++) {
        int cp[MAXN]; int nk = comps(col, p, q, cp, NULL);
        for (int t = 0; t < nk; t++) { int u[MAXN]; memcpy(u, col, sizeof u); swapcomp(u, cp, t, p, q);
            long id = lookup(u); if (id < 0) { fprintf(stderr, "move not found\n"); exit(3); }
            if (id == i) continue; int dup = 0; for (int z = 0; z < k; z++) if (out[z] == id) dup = 1; if (!dup) out[k++] = id; }
    }
    return k;
}
/* swap the unique link-free component (in role pair r) of state i; return canonical index */
static long zmove(long i, int *zset) {
    int col[MAXN]; unpack(keys[i], col); Frame f; frame(col, &f);
    int r = st[i].extra; int comp[MAXN]; int k = comps(col, f.pr[r][0], f.pr[r][1], comp, NULL);
    int seen[MAXN] = {0}; for (int t = 0; t < 5; t++) if (comp[X[t]] >= 0) seen[comp[X[t]]] = 1;
    int z = -1; for (int q = 0; q < k; q++) if (!seen[q]) z = q;
    if (zset) for (int v = 0; v < n; v++) zset[v] = comp[v] == z;
    swapcomp(col, comp, z, f.pr[r][0], f.pr[r][1]);
    return lookup(col);
}

static long gstat_holes = 0, gstat_states = 0, gstat_skipped = 0;
static int g_maxrun = 0; static long g_Rcycles = 0, g_alldlcycles = 0;

static void second_pass(void) {
    long nbr[512];
    for (long i = 0; i < ns; i++) {
        St *s = &st[i]; if (!s->unf) continue;
        if (s->dl) TALLY("DL states");
        /* chain-parity law (sphere only) */
        if (surf && surfchi == 2 && s->dl && s->pi >= 0) {
            St *u = &st[s->pi];
            CHECK("chain-parity law N(pi c)-N(c) = [pi c DL] mod 2 (sphere)", ((u->N - s->N) & 1) == (u->dl ? 1 : 0), "");
        }
        if (s->pi >= 0) CHECK("pinv(pi(c)) = c", st[s->pi].pinv == i, "");
        int rig = isrigid(i);
        if (s->dl && s->D) CHECK("rigid(counts) <=> N=8 (DL+D)", rig == (s->N == 8), "");
        if (rig) {
            TALLY("rigid states");
            if (!s->D) TALLY("rigid states without D");
            /* Lemma E consequence: forests */
            if (surf && surfchi == 2) {
                int ok = 1; for (int r = 0; r < 6; r++) ok &= s->chi[r] == s->cnt[r];
                CHECK("sphere: rigid => all pair graphs forests", ok, "");
            }
            if (surf && surfchi != 2) { int ok = 1; for (int r = 0; r < 6; r++) ok &= s->chi[r] == s->cnt[r]; if (ok) TALLY("offsphere rigid forests"); }
            /* J4 rigid: neighbours = {pi, pinv} */
            if (s->D) {
                int k = kneigh(i, nbr);
                int ok = (k == 2) && ((nbr[0] == s->pi && nbr[1] == s->pinv) || (nbr[1] == s->pi && nbr[0] == s->pinv));
                CHECK("J4 rigid(+D): Kempe nbrs = {pi,pinv}", ok, "k=%d", k);
            }
            /* Lemma S, general form: u rigid, c=pi(u), P2(c)=(2,1), #P1(c)=3 */
            if (s->pi >= 0) {
                St *c = &st[s->pi];
                if (c->cnt[2] == 2 && c->cnt[3] == 1 && c->cnt[0] + c->cnt[1] == 3) {
                    CHECK("Lemma S: (#amu,#AB)(c)=(2,1)", c->cnt[0] == 2 && c->cnt[1] == 1, "cnt=%d,%d dl=%d", c->cnt[0], c->cnt[1], c->dl);
                    CHECK("Lemma S: chi_c(AB)=0 (AB chain unicyclic)", c->chi[1] == 0, "");
                    if (!c->dl) TALLY("Lemma S instances with c not DL");
                }
                if (surf && surfchi == 2 && c->cnt[2] == 2 && c->cnt[3] == 1)
                    CHECK("Lemma S step 5: u rigid, P2(c)=(2,1) => chi_c(AB)=0", c->chi[1] == 0, "");
                if (surf && surfchi != 2 && c->cnt[2] == 2 && c->cnt[3] == 1 && c->cnt[0] + c->cnt[1] == 3) {
                    TALLY("offsphere LemmaS-hyp instances"); if (!(c->cnt[0] == 2 && c->cnt[1] == 1)) TALLY("offsphere LemmaS conclusion FAILS");
                }
            }
        }
        /* N=9 DL states */
        if (s->dl && s->N == 9 && s->D) {
            TALLY("N=9 DL+D states");
            CHECK("N=9 DL+D: exactly one link-free comp", s->nlinkfree == 1, "");
            int pinR = isrigid(s->pinv), piR = isrigid(s->pi);
            int ex = s->extra;
            /* J4-type property for any N=9 DL+D state with extra in P1: Z(c) data */
            if (ex == 0 || ex == 1) {
                long z = zmove(i, NULL);
                CHECK("Z(c): same frame j", z >= 0 && st[z].unf && st[z].j == s->j, "");
                if (st[z].dl && st[z].D) CHECK("Z(c): N>=9 when Z(c) DL+D", st[z].N >= 9, "");
                else { TALLY("Z(c) not DL+D (from N=9, extra in P1)"); if (st[z].N < 9) TALLY("Z(c) not DL+D and N(Zc)<9"); }
                CHECK("Z(c): N(Zc)>=9 (unconditional)", st[z].N >= 9, "N=%d dl=%d D=%d", st[z].N, st[z].dl, st[z].D);
            }
            if (pinR && piR) {
                TALLY("in-shape states");
                CHECK("J3: in-shape => extra in P1", ex == 0 || ex == 1, "ex=%d", ex);
                CHECK("S1: in-shape => extra is alpha-mu", ex == 0, "ex=%d", ex);
                /* J4 in-shape neighbours */
                if (ex == 0 || ex == 1) {
                    long z = zmove(i, NULL);
                    int k = kneigh(i, nbr);
                    int ok = (k == 3);
                    for (int t = 0; t < k; t++) ok &= (nbr[t] == s->pi || nbr[t] == s->pinv || nbr[t] == z);
                    CHECK("J4 in-shape: Kempe nbrs = {pi,pinv,Z}", ok, "k=%d", k);
                    if (st[z].dl && st[z].N == 9) TALLY("in-shape with Z(c) DL N=9");
                    CHECK("J4 in-shape: N(Z c)>=9", st[z].N >= 9, "N=%d dl=%d D=%d", st[z].N, st[z].dl, st[z].D);
                    if (!(st[z].dl && st[z].D)) TALLY("in-shape: Z(c) not DL+D");
                    if (isrigid(st[z].pi) && isrigid(st[z].pinv) && st[z].dl && st[z].N == 9) TALLY("in-shape with in-shape Z-partner (NRI cex)");
                    /* TrackL 2.2 destruction: counts in u'=pi(c) of {al_c,mu_c} and {al_c,B_c} */
                    int col[MAXN]; unpack(keys[i], col); Frame f; frame(col, &f);
                    int cu[MAXN]; unpack(keys[s->pi], cu); /* canonical names differ: recompute via frame of u' */
                    Frame g; frame(cu, &g);
                    /* in u' roles: al_c = al_u', mu_c = A_u', B_c = mu_u' ; so {al_c,mu_c} = pair index 2 (alphaA) of u', {al_c,B_c} = pair 0 (alpha mu) of u' */
                    TALLY("TrackL2.2 destruction instances");
                    if (st[s->pi].cnt[2] != 1) TALLY("TrackL2.2: #{al_c,mu_c} at pi(c) != 1 (no merge into one)");
                    if (st[s->pi].cnt[0] == 1) TALLY("TrackL2.2: #{al_c,B_c} at pi(c) = 1 (al_c-B_c merge)");
                }
            }
            if (pinR) {
                if (ex != 2 && ex != 3) CHECK("S2: pinv rigid, extra not in P2 => alpha-mu", ex == 0, "ex=%d", ex);
                TALLY("S2 hyp (pinv rigid) any extra");
            }
            if (piR) {
                if (ex != 4 && ex != 5) CHECK("S2 mirror: pi rigid, extra not in P3 => alpha-mu", ex == 0, "ex=%d", ex);
            }
            if (piR && !pinR && ex == 1) TALLY("AB-extra next to rigid pi");
        }
    }
    /* NRC statistics: runs in R = {DL, N<=9}, cycles */
    char *vis = calloc(ns, 1);
    for (long i = 0; i < ns; i++) {
        St *s = &st[i]; if (!(s->unf && s->dl && s->N <= 9)) continue;
        long p = s->pinv; int startable = !(p >= 0 && st[p].unf && st[p].dl && st[p].N <= 9);
        if (startable) { int len = 0; long c = i; while (c >= 0 && st[c].unf && st[c].dl && st[c].N <= 9) { len++; c = st[c].pi; if (len > 100000) break; }
            if (len > g_maxrun) g_maxrun = len; }
    }
    /* cycles: all-DL pi-cycles and those inside R */
    for (long i = 0; i < ns; i++) {
        if (vis[i] || !st[i].unf || !st[i].dl) continue;
        long c = i; int len = 0, inR = 1, ok = 1;
        while (1) { if (!st[c].unf || !st[c].dl) { ok = 0; break; } if (st[c].N > 9) inR = 0; len++;
            c = st[c].pi; if (c < 0) { ok = 0; break; } if (c == i) break; if (len > 100000) { ok = 0; break; } }
        if (ok) { g_alldlcycles++; if (inR) g_Rcycles++;
            CHECK("all-DL pi-cycle length = 0 mod 5", len % 5 == 0, "");
            c = i; do { vis[c] = 1; c = st[c].pi; } while (c != i); }
    }
    free(vis);
}

/* -------- class mode (J5) -------- */
static void class_mode(void) {
    char *vis = calloc(ns, 1); long *cls = malloc(sizeof(long) * ns); long nbr[512];
    for (long i0 = 0; i0 < ns; i0++) {
        if (vis[i0] || !st[i0].unf || !st[i0].dl || st[i0].N > 9) continue;
        /* is i0 on an all-DL pi-cycle inside R? */
        long c = i0; int len = 0, ok = 1;
        while (1) { if (!st[c].unf || !st[c].dl || st[c].N > 9) { ok = 0; break; } len++; c = st[c].pi; if (c < 0) { ok = 0; break; } if (c == i0) break; if (len > 10000) { ok = 0; break; } }
        if (!ok) continue;
        /* BFS Kempe class */
        long nc2 = 0, qh = 0; cls[nc2++] = i0; vis[i0] = 1; int closed = 1;
        while (qh < nc2) { long x = cls[qh++]; int k = kneigh(x, nbr);
            for (int t = 0; t < k; t++) if (!vis[nbr[t]]) { vis[nbr[t]] = 1; cls[nc2++] = nbr[t]; if (nc2 > 200000) { closed = 0; break; } }
            if (!closed) break; }
        TALLY("J5: R-cycle classes examined");
        /* near-rigid closed? every state DL on an all-DL pi-cycle with N<=9 */
        int nr = closed;
        for (long t = 0; t < nc2 && nr; t++) { long x = cls[t]; if (!st[x].unf || !st[x].dl || st[x].N > 9) nr = 0;
            else { long y = x; int L = 0; while (1) { y = st[y].pi; L++; if (y < 0 || !st[y].dl || st[y].N > 9) { nr = 0; break; } if (y == x) break; if (L > 10000) { nr = 0; break; } } } }
        printf("CLASS %s h=%d size=%ld nearrigid=%d\n", gname, h, nc2, nr);
        if (!nr) continue;
        TALLY("J5: near-rigid closed classes");
        int lawall = 1;
        for (long t = 0; t < nc2; t++) { long x = cls[t]; if (((st[st[x].pi].N - st[x].N) & 1) != 1) lawall = 0; }
        printf("  law along class: %d\n", lawall);
        if (!lawall) { TALLY("J5: near-rigid classes violating the law (J5 hypothesis fails)"); continue; }
        for (long t = 0; t < nc2; t++) { long x = cls[t]; St *s = &st[x];
            /* cycle length and alternation */
            long y = x; int L = 0, alt = 1; do { long z = st[y].pi; if (st[z].N + st[y].N != 17) alt = 0; y = z; L++; } while (y != x);
            CHECK("J5.1 alternation 8/9 and length = 0 mod 10", alt && L % 10 == 0, "L=%d", L);
            int k = kneigh(x, nbr);
            if (s->N == 8) CHECK("J5.4 Kempe degree 2 at rigid", k == 2 && isrigid(x), "k=%d", k);
            else {
                CHECK("J5.2 9-state in-shape", isrigid(s->pi) && isrigid(s->pinv), "");
                CHECK("J5.2/J3 extra in P1", s->extra == 0 || s->extra == 1, "");
                if (s->extra == 0) TALLY("J5: extra alpha-mu"); else if (s->extra == 1) TALLY("J5: extra AB");
                long z = zmove(x, NULL);
                int inK = 0; for (long q = 0; q < nc2; q++) if (cls[q] == z) inK = 1;
                CHECK("J5.3 Z(c) in class, N=9, Z(Z(c))=c", inK && st[z].N == 9 && zmove(z, NULL) == x, "");
                CHECK("J5.4 Kempe degree 3 at 9-states", k == 3, "k=%d", k);
                /* J5.5 offset */
                long y2 = x; int d = 0, found = -1; do { if (y2 == z) found = d; y2 = st[y2].pi; d++; } while (y2 != x);
                if (found >= 0) { CHECK("J5.5 same-cycle offset d=0 mod 10, cycle>=20", found % 10 == 0 && found > 0 && L >= 20, "d=%d L=%d", found, L); TALLY("J5: Z on own cycle"); }
                else TALLY("J5: Z on other cycle");
            }
        }
        CHECK("J5.5 |K|>=20", nc2 >= 20, "");
    }
    free(vis); free(cls);
}

/* ---------------- driver ---------------- */
static int holelist[MAXN], nholelist = -1, maxholes = 1000;
static uint64_t rng = 88172645463325252ULL;
static uint64_t xr(void) { rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }

static void run_hole(void) {
    /* BFS order from X[0] */
    int seen[MAXN] = {0}; m = 0; int q[MAXN], qh = 0, qt = 0;
    for (int v = 0; v < n; v++) pos[v] = 1 << 20;
    seen[h] = 1; q[qt++] = X[0]; seen[X[0]] = 1;
    while (qh < qt) { int v = q[qh++]; pos[v] = m; ord[m++] = v; for (int t = 0; t < deg[v]; t++) { int w = adj[v][t]; if (!seen[w]) { seen[w] = 1; q[qt++] = w; } } }
    if (m != n - 1) { fprintf(stderr, "G-h disconnected in %s\n", gname); return; }
    ns = 0; overflow = 0; rec(0, -1);
    if (overflow) { gstat_skipped++; printf("SKIP %s h=%d (over cap)\n", gname, h); return; }
    hcap = 1; while (hcap < 2 * ns + 16) hcap <<= 1;
    htab = malloc(sizeof(long) * hcap); for (long i = 0; i < hcap; i++) htab[i] = -1;
    for (long i = 0; i < ns; i++) hinsert(i);
    st = malloc(sizeof(St) * ns);
    for (long i = 0; i < ns; i++) analyse(i);
    second_pass();
    if (classmode) class_mode();
    gstat_holes++; gstat_states += ns;
    free(htab); free(st);
}

int main(int argc, char **argv) {
    for (int a = 1; a < argc; a++) {
        if (!strcmp(argv[a], "-E")) { surf = 1; surfchi = atoi(argv[++a]); }
        else if (!strcmp(argv[a], "-c")) classmode = 1;
        else if (!strcmp(argv[a], "-s")) starS = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-M")) capM = atol(argv[++a]);
        else if (!strcmp(argv[a], "-k")) maxholes = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-H")) { nholelist = 0; char *p = strtok(argv[++a], ","); while (p) { holelist[nholelist++] = atoi(p); p = strtok(NULL, ","); } }
    }
    static char line[1 << 16];
    long ng = 0;
    while (fgets(line, sizeof line, stdin)) {
        char *sp = line; while (*sp == ' ') sp++;
        if (*sp == '#' || *sp == '\n' || !*sp) continue;
        char adjs[1 << 15];
        if (sscanf(line, "%255s %d %32767s", gname, &n, adjs) != 3) continue;
        if (n > MAXN) { fprintf(stderr, "n too big\n"); continue; }
        memset(isadj, 0, sizeof isadj);
        char *p = adjs; for (int v = 0; v < n; v++) { deg[v] = 0;
            while (*p && *p != ';') { adj[v][deg[v]++] = (int)strtol(p, &p, 10); if (*p == ',') p++; }
            if (*p == ';') p++; for (int t = 0; t < deg[v]; t++) isadj[v][adj[v][t]] = 1; }
        ng++;
        int cand[MAXN], nca = 0;
        if (nholelist >= 0) for (int t = 0; t < nholelist; t++) cand[nca++] = holelist[t];
        else for (int v = 0; v < n; v++) if (deg[v] == 5) cand[nca++] = v;
        for (int t = nca - 1; t > 0; t--) { int r = xr() % (t + 1); int tmp = cand[t]; cand[t] = cand[r]; cand[r] = tmp; }
        int used = 0;
        for (int t = 0; t < nca && used < maxholes; t++) {
            h = cand[t]; if (deg[h] != 5) continue;
            for (int s = 0; s < 5; s++) X[s] = adj[h][s];
            int cyc = 1; for (int s = 0; s < 5; s++) if (!isadj[X[s]][X[(s + 1) % 5]]) cyc = 0;
            if (!cyc) { fprintf(stderr, "link not a cycle in given order: %s h=%d\n", gname, h); continue; }
            used++; run_hole();
        }
    }
    printf("SUMMARY graphs=%ld holes=%ld states=%ld skipped=%ld maxRrun=%d Rcycles=%ld allDLcycles=%ld\n", ng, gstat_holes, gstat_states, gstat_skipped, g_maxrun, g_Rcycles, g_alldlcycles);
    for (int i = 0; i < nc; i++) printf("  %-75s checks=%ld fails=%ld\n", cname[i], ccheck[i], cfail[i]);
    return 0;
}
