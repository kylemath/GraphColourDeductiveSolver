// MathNDiscSearch / test_N_fast.cpp  [exploratory, undeclared, post hoc]
// C++ port of test_N.py (same logic): reads DISC lines (stdin or file arg), tests locks at fans u1,u3,u4 by BFS over
// the Kempe class in G = T-xy (x coloured c(y)), and for locked discs tests nu_gamma c @u0, nu_beta c @u2.
// Output format matches test_N.py (tag n=.. sizes ... | DISC line) plus summary. Class cap 2,000,000.
// Early exit: fan classes stop at the first separating colouring (disc is not locked).
// Build: g++ -O2 -o test_N_fast test_N_fast.cpp     Usage: ./test_N_fast FILE [FILE...]
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <deque>
#include <unordered_set>
#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;
static const int CAP = 2000000;
typedef vector<int8_t> Col;
struct H { size_t operator()(const string&s) const { return hash<string>()(s); } };
static int n, x;
static vector<vector<int>> G;
static string canon(const Col&c){ int8_t m[4]={-1,-1,-1,-1}; int k=0; string s(c.size(),0);
  for(size_t i=0;i<c.size();i++){ if(m[(int)c[i]]<0) m[(int)c[i]]=k++; s[i]=m[(int)c[i]]; } return s; }
// returns 1 separable, 0 not (full class), -1 truncated. size out.
static int kempe(const vector<vector<int>>&Gr,int y,const Col&c0,long long&size){
  unordered_set<string> seen; deque<Col> q; seen.insert(canon(c0)); q.push_back(c0);
  vector<int> stk, comp; vector<char> vis(n);
  while(!q.empty()){
    Col st=q.front(); q.pop_front();
    if(st[x]!=st[y]){ size=seen.size(); return 1; }
    for(int a=0;a<4;a++) for(int b=a+1;b<4;b++){
      fill(vis.begin(),vis.end(),0);
      for(int s=0;s<n;s++){
        if((st[s]!=a&&st[s]!=b)||vis[s]) continue;
        comp.clear(); stk.clear(); comp.push_back(s); stk.push_back(s); vis[s]=1;
        while(!stk.empty()){ int u=stk.back(); stk.pop_back();
          for(int w:Gr[u]) if(!vis[w]&&(st[w]==a||st[w]==b)){ vis[w]=1; comp.push_back(w); stk.push_back(w);} }
        Col nc=st; for(int w:comp) nc[w]=(st[w]==a)?b:a;
        string k=canon(nc);
        if(!seen.count(k)){ if((long long)seen.size()>=CAP){ size=seen.size(); return -1; } seen.insert(k); q.push_back(nc); }
      }
    }
  }
  size=seen.size(); return 0;
}
int main(int argc,char**argv){
  long long discs=0,rigid=0,locked=0,holds=0,cand=0,trunc=0;
  for(int fi=1;fi<argc;fi++){
    ifstream in(argv[fi]); string line;
    while(getline(in,line)){
      if(line.compare(0,4,"DISC")) continue;
      discs++;
      size_t p1=line.find(';'), p2=line.find(';',p1+1);
      istringstream cs(line.substr(p1+1,p2-p1-1)); vector<int> colv; int t; while(cs>>t) colv.push_back(t);
      int V=colv.size(); n=V+1; x=V;
      vector<vector<int>> adj(n);
      { istringstream es(line.substr(p2+1)); string tok; while(es>>tok){ int u,v; sscanf(tok.c_str(),"%d-%d",&u,&v); adj[u].push_back(v); adj[v].push_back(u);} }
      for(int r=0;r<5;r++){ adj[x].push_back(r); adj[r].push_back(x); }
      size_t m=0; bool ok=true; for(auto&a:adj){ m+=a.size(); if(a.size()<5) ok=false; }
      if(m/2!=(size_t)(3*n-6)||!ok) continue;
      // rigid structure check: components per pair
      const int PR[6][2]={{0,1},{0,2},{0,3},{1,2},{1,3},{2,3}}; int want[6]={1,2,2,1,1,1}; bool good=true;
      for(int k=0;k<6&&good;k++){ int a=PR[k][0],b=PR[k][1]; int Vp=0,Ep=0,cc=0; vector<char> vis(n,0);
        for(int v=0;v<V;v++) if(colv[v]==a||colv[v]==b){ Vp++; for(int w:adj[v]) if(w<V&&w>v&&(colv[w]==a||colv[w]==b)) Ep++; }
        for(int s=0;s<V;s++) if((colv[s]==a||colv[s]==b)&&!vis[s]){ cc++; vector<int> st={s}; vis[s]=1; while(!st.empty()){int u=st.back();st.pop_back(); for(int w:adj[u]) if(w<V&&!vis[w]&&(colv[w]==a||colv[w]==b)){vis[w]=1;st.push_back(w);} } }
        if(Ep!=Vp-cc||cc!=want[k]) good=false; }
      if(!good) continue;
      rigid++;
      auto mkG=[&](int y){ vector<vector<int>> g=adj; auto rm=[&](int u,int v){ for(size_t i=0;i<g[u].size();i++) if(g[u][i]==v){ g[u].erase(g[u].begin()+i); break; } }; rm(x,y); rm(y,x); return g; };
      Col base(n); for(int v=0;v<V;v++) base[v]=colv[v];
      bool lockedAll=true, anyTrunc=false;
      for(int j: {1,3,4}){
        Col c=base; c[x]=colv[j]; long long sz; int r=kempe(mkG(j),j,c,sz);
        if(r!=0){ lockedAll=false; if(r<0) anyTrunc=true; break; }
      }
      if(!lockedAll){ if(anyTrunc) trunc++; continue; }
      locked++;
      // components of {D,g} containing u2, {D,b} containing u0 in T-x
      auto swapcomp=[&](int a,int b,int seed){ Col c=base; vector<char> vis(n,0); vector<int> st={seed}; vis[seed]=1;
        while(!st.empty()){int u=st.back();st.pop_back(); c[u]=(colv[u]==a)?b:a; for(int w:adj[u]) if(w<V&&!vis[w]&&(colv[w]==a||colv[w]==b)){vis[w]=1;st.push_back(w);} } return c; };
      Col cA=swapcomp(0,3,2); cA[x]=cA[0]; long long szA; int rA=kempe(mkG(0),0,cA,szA);
      Col cB=swapcomp(0,2,0); cB[x]=cB[2]; long long szB; int rB=kempe(mkG(2),2,cB,szB);
      const char*tag=(rA==1||rB==1)?"N-holds":((rA<0||rB<0)?"N-UNDECIDED(trunc)":"CAND");
      if(tag[0]=='N'&&tag[1]=='-'&&tag[2]=='h') holds++; else if(tag[0]=='C') cand++; else trunc++;
      int sz4[4]={0,0,0,0}; for(int v=0;v<V;v++) sz4[colv[v]]++;
      printf("%s n=%d sizes(D,a,b,g)=(%d, %d, %d, %d) nu_gamma@u0 sep=%s class=%lld; nu_beta@u2 sep=%s class=%lld | %s\n",tag,n,sz4[0],sz4[1],sz4[2],sz4[3],
        rA==1?"True":(rA==0?"False":"None"),szA,rB==1?"True":(rB==0?"False":"None"),szB,line.c_str());
      fflush(stdout);
    }
  }
  printf("[computed, exploratory, post hoc] summary discs=%lld rigid_ok=%lld locked3=%lld Nholds=%lld CAND=%lld trunc=%lld\n",discs,rigid,locked,holds,cand,trunc);
}
