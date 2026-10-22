// BFS on the row graph of the straight degree-6 cylinder: rows = proper 4-colourings of C_L,
// r -> r' iff r'(i) not in {r(i), r(i+1)}.  For each source a: d(a,b) = min over 24 renamings pi of dist(a, pi b).
// stdin: L maxd nsrc nt ; nsrc rows ; nt rows (digits).  stdout per source: one line of chars '0'+dist (or 'x' if > maxd).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int L; static uint32_t P3[20]; static uint32_t NID;
static uint32_t rid(const int *r){ uint32_t id = r[0]*P3[L-1]; for(int i=1;i<L;i++){ int d = r[i] - (r[i] > r[i-1]); id += d*P3[L-1-i]; } return id; }
static uint8_t *dist; static uint32_t *fr, *nf; static uint32_t nfr, nnf; static int cur[20], nr[20]; static uint8_t D;
static void unrank(uint32_t id, int *r){ r[0] = id / P3[L-1]; for(int i=1;i<L;i++){ int d = (id / P3[L-1-i]) % 3; r[i] = d + (d >= r[i-1]); } }
static void gen(int i, uint32_t acc){
  if(i==L){ if(nr[L-1]==nr[0]) return; if(dist[acc]==255){ dist[acc]=D; nf[nnf++]=acc; } return; }
  int a = cur[i], b = cur[(i+1)%L];
  for(int c=0;c<4;c++){ if(c==a||c==b) continue; if(i>0 && c==nr[i-1]) continue;
    nr[i]=c; uint32_t add = (i==0)? c*P3[L-1] : (uint32_t)(c - (c > nr[i-1]))*P3[L-1-i]; gen(i+1, acc+add); }
}
int main(){
  int maxd, ns, nt; if(scanf("%d %d %d %d",&L,&maxd,&ns,&nt)!=4) return 1;
  P3[0]=1; for(int i=1;i<20;i++) P3[i]=P3[i-1]*3; NID = 4*P3[L-1];
  dist = malloc(NID); fr = malloc(sizeof(uint32_t)*NID); nf = malloc(sizeof(uint32_t)*NID);
  int (*S)[20] = malloc(sizeof(int[20])*ns); char buf[64];
  for(int s=0;s<ns;s++){ scanf("%s",buf); for(int i=0;i<L;i++) S[s][i]=buf[i]-'0'; }
  uint32_t *T = malloc(sizeof(uint32_t)*24*(size_t)nt); int perms[24][4]; int np=0;
  for(int a=0;a<4;a++)for(int b=0;b<4;b++)for(int c=0;c<4;c++)for(int d=0;d<4;d++) if(a!=b&&a!=c&&a!=d&&b!=c&&b!=d&&c!=d){perms[np][0]=a;perms[np][1]=b;perms[np][2]=c;perms[np][3]=d;np++;}
  for(int t=0;t<nt;t++){ scanf("%s",buf); int r[20], q[20]; for(int i=0;i<L;i++) r[i]=buf[i]-'0';
    for(int p=0;p<24;p++){ for(int i=0;i<L;i++) q[i]=perms[p][r[i]]; T[(size_t)t*24+p]=rid(q);} }
  char *out = malloc(nt+2); uint8_t *best = malloc(nt);
  for(int s=0;s<ns;s++){
    memset(dist,255,NID); uint32_t a = rid(S[s]); fr[0]=a; nfr=1;   // a itself not marked: paths have length >= 1
    int remaining = nt; memset(best,255,nt);
    for(D=1; D<=maxd && remaining>0 && nfr>0; D++){
      nnf=0;
      for(uint32_t f=0; f<nfr; f++){ unrank(fr[f], cur); gen(0,0); }
      for(int t=0;t<nt;t++) if(best[t]==255){ for(int p=0;p<24;p++) if(dist[T[(size_t)t*24+p]]==D){best[t]=D; remaining--; break;} }
      uint32_t *tmp=fr; fr=nf; nf=tmp; nfr=nnf;
    }
    for(int t=0;t<nt;t++) out[t] = best[t]==255 ? 'x' : '0'+best[t];
    out[nt]=0; printf("%s\n",out); fflush(stdout);
  }
  return 0;
}
