import sys, random, subprocess
sys.argv=['pfh.py','reg']
exec(open('pfh.py').read().split("if __name__ == '__main__':")[0])
SEPB.kill()
import os
SEPB = subprocess.Popen([os.path.join(HERE,'sepb'), os.path.join(HERE,'empty.txt'), os.path.join(HERE,'rbig7.txt')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
rng=random.Random(3)
# random x over all keys appearing in edges
for U in (7,8,9):
    for a,b,c in edges(U):
        for k in c:
            if k is not None: var(k)
prep7()
import time
for trial in range(2):
    x=np.array([rng.random() for _ in VARL])
    for d in (10,):
        W,K=edge_weights(min(d,9),x); v,_=best_cycle(W,K,d); t0=time.time()
        r=sepb_query(d,x,v-0.3,1)
        print(d,'dp',round(v,9),'sepb',round(r[0][0],9), 'rowsum', round(sum(sg*val(x,k) for sg,k in r[0][1]),9), round(time.time()-t0,1),'s', flush=True)
    v7=best7(x)[0]; r=sepb_query(7,x,v7-0.3,1)
    print(7,'best7',round(v7,9),'sepb',round(r[0][0],9),'rowsum', round(sum(sg*val(x,k) for sg,k in r[0][1]),9), flush=True)
