// Independent exact band-filling check on the straight degree-6 tube of circumference L.
// Rows: proper 4-colourings of the cycle C_L (code = sum r[i]*4^i).
// Tube adjacency: row k+1 vertex i is adjacent to row k vertices i and i+1 (plus row-cycle edges).
// Level row: boundary walk H (constant sign; label r[i]^r[i+1] -> e1,e2,e3) has circumradius <= 1
//   about some half-lattice centre (doubled coordinates: e1=(2,0), e2=(0,2), e3=(-2,-2), N(a,b)=a^2+b^2-ab, level iff N<=4).
// DA_w = rows a with a path a -> ... -> s (w steps up) to a level row s   (A side, below the seam)
// UB_w = rows b with a path s -> ... -> b (w steps up) from a level row s (B side, above the seam)
// C(w): for all a in DA_w, b in UB_w there is a renaming pi with a path a -> x1 -> ... -> x_{2w} -> pi(b).
// Usage: bf L wmin wmax [maxbadprint]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static int L; static uint64_t NC; static uint32_t *rows; static uint64_t N;
static int P[24][4];
typedef uint64_t word;
static inline int get(word *b, uint64_t i){return (b[i>>6]>>(i&63))&1;}
static inline void set(word *b, uint64_t i){b[i>>6]|=(1ULL<<(i&63));}
static word *newbs(){return calloc((NC+63)/64,8);}
static inline int dig(uint32_t c,int i){return (c>>(2*i))&3;}
static uint32_t pw4[20];
// enumerate successors (up=1) or predecessors (up=0) of row r, setting bits in out
static int rr[20], cur[20];
static word *OUT; static uint64_t cnt;
static void rec(int i, uint32_t code, int up){
  if(i==L){ if(cur[L-1]!=cur[0]){ if(OUT) set(OUT,code); cnt++; } return; }
  for(int c=0;c<4;c++){
    if(up){ if(c==rr[i]||c==rr[(i+1)%L]) continue; }
    else { if(c==rr[i]||c==rr[(i-1+L)%L]) continue; }
    if(i>0 && c==cur[i-1]) continue;
    cur[i]=c; rec(i+1, code + c*pw4[i], up);
  }
}
static void nbrs(uint32_t r, int up, word *out){ for(int i=0;i<L;i++) rr[i]=dig(r,i); OUT=out; rec(0,0,up); }
static word *step(word *in, int up){ word *o=newbs(); for(uint64_t k=0;k<N;k++) if(get(in,rows[k])) nbrs(rows[k],up,o); return o; }
static uint64_t count(word *b){ uint64_t s=0; for(uint64_t k=0;k<N;k++) s+=get(b,rows[k]); return s; }
static uint32_t perm(uint32_t r,int p){ uint32_t o=0; for(int i=0;i<L;i++) o+=P[p][dig(r,i)]*pw4[i]; return o; }
static uint32_t rot(uint32_t r,int s){ uint32_t o=0; for(int i=0;i<L;i++) o+=dig(r,(i+s)%L)*pw4[i]; return o; }
static uint32_t refl(uint32_t r){ uint32_t o=0; for(int i=0;i<L;i++) o+=dig(r,(L-i)%L)*pw4[i]; return o; }
static uint32_t canon(uint32_t r){ uint32_t best=0xffffffff;
  for(int f=0;f<2;f++){ uint32_t q=f?refl(r):r; for(int s=0;s<L;s++){ uint32_t q2=rot(q,s); for(int p=0;p<24;p++){ uint32_t q3=perm(q2,p); if(q3<best) best=q3; }}} return best; }
static int nrm(int a,int b){return a*a+b*b-a*b;}
static int level(uint32_t r, int *tx, int *ty){
  int H[21][2]; H[0][0]=H[0][1]=0;
  for(int i=0;i<L;i++){ int l=dig(r,i)^dig(r,(i+1)%L); int dx= l==1?2:(l==2?0:-2), dy= l==1?0:(l==2?2:-2);
    H[i+1][0]=H[i][0]+dx; H[i+1][1]=H[i][1]+dy; }
  *tx=H[L][0]; *ty=H[L][1];
  int mnx=1000,mxx=-1000,mny=1000,mxy=-1000; for(int i=0;i<=L;i++){ if(H[i][0]<mnx)mnx=H[i][0]; if(H[i][0]>mxx)mxx=H[i][0]; if(H[i][1]<mny)mny=H[i][1]; if(H[i][1]>mxy)mxy=H[i][1]; }
  for(int px=mnx-2;px<=mxx+2;px++) for(int py=mny-2;py<=mxy+2;py++){ int ok=1; for(int i=0;i<=L&&ok;i++) if(nrm(H[i][0]-px,H[i][1]-py)>4) ok=0; if(ok) return 1; }
  return 0;
}
static void prow(uint32_t r){ for(int i=0;i<L;i++) printf("%d",dig(r,i)); }
int main(int argc,char**argv){
  L=atoi(argv[1]); int wmin=atoi(argv[2]), wmax=atoi(argv[3]); int maxprint=argc>4?atoi(argv[4]):3;
  pw4[0]=1; for(int i=1;i<20;i++) pw4[i]=pw4[i-1]*4; NC=(uint64_t)pw4[L];
  int np=0; for(int a=0;a<4;a++)for(int b=0;b<4;b++)for(int c=0;c<4;c++)for(int d=0;d<4;d++) if(a!=b&&a!=c&&a!=d&&b!=c&&b!=d&&c!=d){P[np][0]=a;P[np][1]=b;P[np][2]=c;P[np][3]=d;np++;}
  rows=malloc(sizeof(uint32_t)*(3*pw4[L>16?16:L]/4+16)); N=0;
  for(uint64_t c=0;c<NC;c++){ int ok=1; for(int i=0;i<L&&ok;i++) if(dig(c,i)==dig(c,(i+1)%L)) ok=0; if(ok) rows[N++]=c; }
  word *lev=newbs(); uint64_t nl=0; int tset[64][2]; int nt=0;
  for(uint64_t k=0;k<N;k++){ int tx,ty; if(level(rows[k],&tx,&ty)){ set(lev,rows[k]); nl++; int f=0; for(int j=0;j<nt;j++) if(tset[j][0]==tx&&tset[j][1]==ty) f=1; if(!f&&nt<64){tset[nt][0]=tx;tset[nt][1]=ty;nt++;} } }
  // average out-degree
  cnt=0; for(uint64_t k=0;k<N;k+= (N/2000+1)) nbrs(rows[k],1,NULL);
  printf("L=%d N=%llu nlevel=%llu avgsucc~%.1f level_t:",L,(unsigned long long)N,(unsigned long long)nl,(double)cnt/((N-1)/(N/2000+1)+1));
  for(int j=0;j<nt;j++) printf(" (%d,%d)",tset[j][0],tset[j][1]); printf("\n"); fflush(stdout);
  word *DA=newbs(), *UB=newbs(); memcpy(DA,lev,(NC+63)/64*8); memcpy(UB,lev,(NC+63)/64*8);
  for(int w=0;w<=wmax;w++){
    if(w>0){ word *t=step(DA,0); free(DA); DA=t; t=step(UB,1); free(UB); UB=t; }
    if(w<wmin) continue;
    uint64_t nda=count(DA), nub=count(UB);
    uint32_t *ublist=malloc(4*nub); uint64_t nu=0; for(uint64_t k=0;k<N;k++) if(get(UB,rows[k])) ublist[nu++]=rows[k];
    // canonical a's
    uint64_t ncan=0, nbadA=0, nbadpairs=0; int printed=0;
    word *seen=newbs();
    for(uint64_t k=0;k<N;k++){ uint32_t a=rows[k]; if(!get(DA,a)) continue; uint32_t ca=canon(a); if(get(seen,ca)) continue; set(seen,ca); ncan++;
      word *X=newbs(); set(X,ca);
      for(int s=0;s<2*w+1;s++){ word *t=step(X,1); free(X); X=t; }
      uint64_t bad=0;
      for(uint64_t j=0;j<nu;j++){ int ok=0; for(int p=0;p<24&&!ok;p++) if(get(X,perm(ublist[j],p))) ok=1;
        if(!ok){ bad++; if(printed<maxprint){ printf("  BAD w=%d a=",w); prow(ca); printf(" b="); prow(ublist[j]); printf("\n"); printed++; } } }
      if(bad){ nbadA++; nbadpairs+=bad; }
      free(X);
    }
    printf("L=%d w=%d |DA|=%llu |UB|=%llu canonical_a=%llu bad_a=%llu bad_pairs(canon a x b)=%llu  C(w)=%s\n",L,w,(unsigned long long)nda,(unsigned long long)nub,(unsigned long long)ncan,(unsigned long long)nbadA,(unsigned long long)nbadpairs, nbadA?"FALSE":"TRUE");
    fflush(stdout); free(ublist); free(seen);
  }
  return 0;
}
