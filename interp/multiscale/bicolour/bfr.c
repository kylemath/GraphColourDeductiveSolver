// bf2: same check as bf.c (straight degree-6 tube, circumference L) but batched: 64*W canonical a's per pass.
// Row index: r0 + 4*sum_{i>=1} d_i 3^{i-1}, d_i = rank of r[i] among colours != r[i-1].
// Usage: bf2 L w mode [maxprint]   checks C(w) only; prints counts and some bad pairs.
// mode 0: "level" = tau<=1 with the walk based at column 0 for BOTH rows (as in closing/round2/tm.py); canon by renaming only.
// mode 1: "level" = tau<=1 for SOME base point (A and B base points independent: the closing situation); canon by renaming,
//         rotation and reflection (DA, UB are then closed under all of these).
// mode 2: "level" = tau<=1 for EVERY base point (strongest notion); canon as mode 1.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
// bfp: copy of opus_attack/bandfill/bf2.c with mode 3 = Hodge pair: |t|<=2 and tau_H = continuous circumradius of
// {H_i-(i/L)t : 0<=i<L} <= TP (argv[5], default 1). Base-point free, so canon as mode 1.
static double TP=1.0; static int K0=99, COLLAR=0;
// bfr: bfp + seam-row filter maxrun<=K0 (argv[6]); COLLAR=1 (argv[7]) also caps every side row (depth 0..w).

#define W 4
typedef struct { uint64_t x[W]; } blk;
static int L; static uint64_t NI; static uint64_t p3[24];
static int P[24][4];
static uint8_t *valid;           // valid[idx]
static int rr[24], cur[24];
static inline int rk(int c,int prev){ return c<prev?c:c-1; }
static void decode(uint64_t idx,int *r){ r[0]=idx%4; uint64_t q=idx/4; for(int i=1;i<L;i++){ int d=q%3; q/=3; int c=d<r[i-1]?d:d+1; r[i]=c; } }
static uint64_t encode(const int *r){ uint64_t q=0; for(int i=L-1;i>=1;i--) q=q*3+rk(r[i],r[i-1]); return r[0]+4*q; }
// generic neighbour enumeration with callback via globals
static blk *SRC, *DST; static blk curv; static uint8_t *DSTB; static int MODE; // MODE 0: blk OR, 1: byte set
static void rec(int i, uint64_t acc, int up){
  if(i==L){ if(cur[L-1]!=cur[0]){ uint64_t idx=cur[0]+4*acc; if(MODE==0){ for(int k=0;k<W;k++) DST[idx].x[k]|=curv.x[k]; } else DSTB[idx]=1; } return; }
  for(int c=0;c<4;c++){
    if(up){ if(c==rr[i]||c==rr[(i+1)%L]) continue; } else { if(c==rr[i]||c==rr[(i-1+L)%L]) continue; }
    if(i>0 && c==cur[i-1]) continue;
    cur[i]=c; rec(i+1, i==0?0: acc + (uint64_t)rk(c,cur[i-1])*p3[i-1], up);
  }
}
static void stepb(uint8_t *in, uint8_t *out, int up){ memset(out,0,NI); MODE=1; DSTB=out;
  for(uint64_t k=0;k<NI;k++) if(in[k]){ decode(k,rr); rec(0,0,up);} }
static void stepw(blk *in, blk *out){ memset(out,0,NI*sizeof(blk)); MODE=0; DST=out;
  for(uint64_t k=0;k<NI;k++){ int nz=0; for(int j=0;j<W;j++) nz|=in[k].x[j]!=0; if(!nz) continue; curv=in[k]; decode(k,rr); rec(0,0,1);} }
static int nrm(int a,int b){return a*a+b*b-a*b;}
static int level0(const int *r){
  int H[25][2]; H[0][0]=H[0][1]=0;
  for(int i=0;i<L;i++){ int l=r[i]^r[(i+1)%L]; int dx= l==1?2:(l==2?0:-2), dy= l==1?0:(l==2?2:-2); H[i+1][0]=H[i][0]+dx; H[i+1][1]=H[i][1]+dy; }
  int mnx=1000,mxx=-1000,mny=1000,mxy=-1000; for(int i=0;i<=L;i++){ if(H[i][0]<mnx)mnx=H[i][0]; if(H[i][0]>mxx)mxx=H[i][0]; if(H[i][1]<mny)mny=H[i][1]; if(H[i][1]>mxy)mxy=H[i][1]; }
  if(mxx-mnx>4||mxy-mny>4) return 0;
  for(int px=mnx-2;px<=mxx+2;px++) for(int py=mny-2;py<=mxy+2;py++){ int ok=1; for(int i=0;i<=L&&ok;i++) if(nrm(H[i][0]-px,H[i][1]-py)>4) ok=0; if(ok) return 1; }
  return 0;
}

static int inC(double cx,double cy,double rr,double x,double y){ return (x-cx)*(x-cx)+(y-cy)*(y-cy)<=rr+1e-9; }
static double mec(double *X,double *Y,int n){ double cx=X[0],cy=Y[0],r2=0;
  for(int i=1;i<n;i++) if(!inC(cx,cy,r2,X[i],Y[i])){ cx=X[i];cy=Y[i];r2=0;
    for(int j=0;j<i;j++) if(!inC(cx,cy,r2,X[j],Y[j])){ cx=(X[i]+X[j])/2; cy=(Y[i]+Y[j])/2; r2=((X[i]-cx)*(X[i]-cx)+(Y[i]-cy)*(Y[i]-cy));
      for(int k=0;k<j;k++) if(!inC(cx,cy,r2,X[k],Y[k])){ double ax=X[i],ay=Y[i],bx=X[j],by=Y[j],qx=X[k],qy=Y[k];
        double d=2*(ax*(by-qy)+bx*(qy-ay)+qx*(ay-by));
        double ux=((ax*ax+ay*ay)*(by-qy)+(bx*bx+by*by)*(qy-ay)+(qx*qx+qy*qy)*(ay-by))/d;
        double uy=((ax*ax+ay*ay)*(qx-bx)+(bx*bx+by*by)*(ax-qx)+(qx*qx+qy*qy)*(bx-ax))/d;
        cx=ux;cy=uy;r2=(ax-cx)*(ax-cx)+(ay-cy)*(ay-cy); } } }
  return sqrt(r2); }
static int pairlevel(const int *r){
  int H[25][2]; H[0][0]=H[0][1]=0;
  for(int i=0;i<L;i++){ int l=r[i]^r[(i+1)%L]; int dx= l==1?2:(l==2?0:-2), dy= l==1?0:(l==2?2:-2); H[i+1][0]=H[i][0]+dx; H[i+1][1]=H[i][1]+dy; }
  int tx=H[L][0],ty=H[L][1]; if(nrm(tx,ty)>16) return 0;
  double X[24],Y[24]; for(int i=0;i<L;i++){ double hx=H[i][0]-(double)i*tx/L, hy=H[i][1]-(double)i*ty/L; X[i]=(hx-hy/2)/2; Y[i]=hy*sqrt(3.0)/4; }
  return mec(X,Y,L)<=TP+1e-9; }
static int maxrun(const int *r){ int all=1; for(int i=0;i<L;i++) if(r[i]!=r[(i+2)%L]) {all=0;break;}
  if(all) return L; int best=0; for(int s=0;s<L;s++){ if(r[s]==r[(s+2)%L]) continue; int m=0; for(int j=1;j<=L;j++){ int i=(s+j)%L; if(r[i]==r[(i+2)%L]) {m++; if(m>best) best=m;} else m=0; } break; }
  return best+2; }
static int MODEL;
static int level(const int *r){ if(MODEL==0) return level0(r); if(MODEL==3) return pairlevel(r); int q[24], any=0, all=1;
  for(int s=0;s<L;s++){ for(int i=0;i<L;i++) q[i]=r[(i+s)%L]; int v=level0(q); any|=v; all&=v; }
  return MODEL==1?any:all; }
static uint64_t canon(const int *r){ uint64_t best=~0ULL; int q[24];
  for(int f=0;f<(MODEL?2:1);f++) for(int s=0;s<(MODEL?L:1);s++) for(int p=0;p<24;p++){ for(int i=0;i<L;i++){ int j=f?((L-i)%L):i; q[i]=P[p][r[(j+s)%L]]; } uint64_t e=encode(q); if(e<best) best=e; }
  return best; }
static void prow(uint64_t idx){ int r[24]; decode(idx,r); for(int i=0;i<L;i++) printf("%d",r[i]); }
int main(int argc,char**argv){
  L=atoi(argv[1]); int w=atoi(argv[2]); MODEL=atoi(argv[3]); int maxprint=argc>4?atoi(argv[4]):3; if(argc>5) TP=atof(argv[5]); if(argc>6) K0=atoi(argv[6]); if(argc>7) COLLAR=atoi(argv[7]);
  p3[0]=1; for(int i=1;i<24;i++) p3[i]=p3[i-1]*3; NI=4*p3[L-1];
  int np=0; for(int a=0;a<4;a++)for(int b=0;b<4;b++)for(int c=0;c<4;c++)for(int d=0;d<4;d++) if(a!=b&&a!=c&&a!=d&&b!=c&&b!=d&&c!=d){P[np][0]=a;P[np][1]=b;P[np][2]=c;P[np][3]=d;np++;}
  valid=malloc(NI); uint8_t *lev=calloc(NI,1); uint8_t *cap=calloc(NI,1); uint64_t N=0,nl=0; int r[24];
  for(uint64_t k=0;k<NI;k++){ decode(k,r); valid[k]= r[L-1]!=r[0]; if(valid[k]){ N++; cap[k]= maxrun(r)<=K0; if(cap[k] && level(r)){lev[k]=1; nl++;} } }
  { uint64_t h[25]={0}; for(uint64_t k=0;k<NI;k++) if(valid[k]){ decode(k,r); if(level(r)) h[maxrun(r)]++; } printf("HIST level rows by maxrun:"); for(int i=0;i<=L;i++) if(h[i]) printf(" %d:%llu",i,(unsigned long long)h[i]); printf("\n"); }
  printf("L=%d N=%llu nlevel=%llu\n",L,(unsigned long long)N,(unsigned long long)nl); fflush(stdout);
  uint8_t *DA=malloc(NI),*UB=malloc(NI),*t=malloc(NI); memcpy(DA,lev,NI); memcpy(UB,lev,NI);
  if(w<0){ // extension analysis: greatest set of capped rows extendable forever by capped rows, in each direction
    uint64_t ncap=0; for(uint64_t k=0;k<NI;k++) ncap+=cap[k];
    { // one-sided transition on the admissible set A = cap AND level: does every A-row have an A-neighbour in each direction?
      for(int dir=0;dir<2;dir++){ stepb(lev,t,dir); uint64_t bad=0; for(uint64_t k=0;k<NI;k++) if(lev[k]&&!t[k]) bad++;
        printf("LEVEXT L=%d K0=%d mode=%d dir=%s admissible=%llu without_admissible_neighbour=%llu\n",L,K0,MODEL,dir?"succ":"pred",(unsigned long long)nl,(unsigned long long)bad); } }
    for(int dir=0;dir<2;dir++){ uint8_t *S=malloc(NI); memcpy(S,cap,NI); uint64_t prev=ncap, lost1=0, lostlev1=0;
      for(int it=0;it<200;it++){ stepb(S,t,dir); uint64_t n=0, nlv=0; for(uint64_t k=0;k<NI;k++){ S[k]=S[k]&t[k]; n+=S[k]; nlv+=S[k]&lev[k]; }
        if(it==0){ lost1=ncap-n; lostlev1=nl-nlv; }
        printf("EXT dir=%s it=%d |S|=%llu level_in_S=%llu/%llu\n",dir?"towards-seam(succ)":"away(pred)",it+1,(unsigned long long)n,(unsigned long long)nlv,(unsigned long long)nl);
        if(n==prev) break; prev=n; }
      printf("EXTSUM L=%d K0=%d dir=%d ncap=%llu no_capped_neighbour=%llu level_capped_without=%llu\n",L,K0,dir,(unsigned long long)ncap,(unsigned long long)lost1,(unsigned long long)lostlev1);
      free(S); }
    return 0; }
  for(int s=0;s<w;s++){ stepb(DA,t,0); memcpy(DA,t,NI); stepb(UB,t,1); memcpy(UB,t,NI); if(COLLAR) for(uint64_t k=0;k<NI;k++){ DA[k]&=cap[k]; UB[k]&=cap[k]; } }
  uint64_t nda=0,nub=0; for(uint64_t k=0;k<NI;k++){ nda+=DA[k]; nub+=UB[k]; }
  { int mx=0; for(uint64_t k=0;k<NI;k++) if(DA[k]){ decode(k,r); int m=maxrun(r); if(m>mx) mx=m; } printf("DEPTHRUN w=%d max_bicoloured_run_in_DA=%d\n",w,mx); if(argc>8) return 0; }
  // canonical a list
  uint8_t *seen=calloc(NI,1); uint64_t *can=malloc(8*nda); uint64_t ncan=0;
  for(uint64_t k=0;k<NI;k++) if(DA[k]){ decode(k,r); uint64_t c=canon(r); if(!seen[c]){ seen[c]=1; can[ncan++]=c; } }
  free(seen);
  // precompute permutation images of UB rows
  uint64_t *ub=malloc(8*nub*24); uint64_t nu=0;
  for(uint64_t k=0;k<NI;k++) if(UB[k]){ decode(k,r); for(int p=0;p<24;p++){ int q[24]; for(int i=0;i<L;i++) q[i]=P[p][r[i]]; ub[nu*24+p]=encode(q);} nu++; }
  printf("L=%d w=%d |DA|=%llu |UB|=%llu canonical_a=%llu\n",L,w,(unsigned long long)nda,(unsigned long long)nub,(unsigned long long)ncan); fflush(stdout);
  blk *X=malloc(NI*sizeof(blk)), *Y=malloc(NI*sizeof(blk));
  uint64_t nbadA=0, nbadpairs=0; int printed=0; uint64_t *badb=calloc(64*W,8);
  for(uint64_t b0=0;b0<ncan;b0+=64*W){
    memset(X,0,NI*sizeof(blk)); int nb=0;
    for(uint64_t j=b0;j<ncan&&j<b0+64*W;j++,nb++) X[can[j]].x[nb/64]|=1ULL<<(nb%64);
    for(int s=0;s<2*w+1;s++){ stepw(X,Y); blk*tt=X; X=Y; Y=tt; }
    memset(badb,0,64*W*8);
    for(uint64_t j=0;j<nu;j++){ blk o; memset(&o,0,sizeof o); for(int p=0;p<24;p++){ blk *q=&X[ub[j*24+p]]; for(int k=0;k<W;k++) o.x[k]|=q->x[k]; }
      for(int m=0;m<nb;m++) if(!((o.x[m/64]>>(m%64))&1)){ badb[m]++; if(printed<maxprint){ printf("  BAD w=%d a=",w); prow(can[b0+m]); printf(" b="); prow(ub[j*24]); printf("\n"); printed++; } } }
    for(int m=0;m<nb;m++) if(badb[m]){ nbadA++; nbadpairs+=badb[m]; }
    fprintf(stderr,"batch %llu/%llu bad_a so far %llu\n",(unsigned long long)b0,(unsigned long long)ncan,(unsigned long long)nbadA);
  }
  printf("K0=%d collar=%d T=%.4f L=%d w=%d mode=%d",K0,COLLAR,TP,L,w,MODEL); printf("  canonical_a=%llu bad_a=%llu bad_pairs=%llu  C(w)=%s\n",(unsigned long long)ncan,(unsigned long long)nbadA,(unsigned long long)nbadpairs,nbadA?"FALSE":"TRUE");
  return 0;
}
