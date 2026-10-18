import sys; sys.argv=['mcheck']; src=open('mcheck.py').read().split("if __name__ == '__main__':")[0]
src=src.replace("if rot_ok(1) or rot_ok(-1):","CNT[0]+=1\n            if rot_ok(1) or rot_ok(-1):")
CNT=[0]; exec(src)
n=0
for w,z in rows()[:3000]:
    if w not in MODELS: MODELS[w]=model(w)
    let={'v':5}; let.update({('a',k):w[k] for k in range(5)}); let.update(dict(z))
    for K in KS: n+=len(embeddings(K,w,MODELS[w],let))
print('passed tri',CNT[0],'passed rot',n)
