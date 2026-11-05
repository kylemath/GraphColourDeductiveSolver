import sys, os, json, time, uuid, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from lib import *
SRV = [S73 + 'srv/A', S73 + 'srv/B']
L, OFF = load_uni()
_free = list(range(len(SRV))); _lock = threading.Lock(); _ctr = [0]
def check_many(sets):
    """sets: list of id-collections -> list of (ok, msg). Runs on both servers in parallel."""
    out = [None] * len(sets); q = list(range(len(sets))); ql = threading.Lock()
    def worker(si):
        while True:
            with ql:
                if not q: return
                k = q.pop(0)
            with _lock: _ctr[0] += 1; name = 'j%d_%d' % (os.getpid(), _ctr[0])
            rp = S73 + 'tmp/%s.rules.json' % name; os.makedirs(S73 + 'tmp', exist_ok=True)
            write_rules(rp, L, sets[k])
            tmp = SRV[si] + '/.%s' % name; json.dump({'rules': rp}, open(tmp, 'w')); os.rename(tmp, SRV[si] + '/req_%s.json' % name)
            rf = SRV[si] + '/res_%s.txt' % name
            while not os.path.exists(rf): time.sleep(0.2)
            time.sleep(0.05); m = open(rf).read().strip(); os.remove(rf); os.remove(rp)
            out[k] = (m.startswith('OK'), m)
    th = [threading.Thread(target=worker, args=(i,)) for i in range(len(SRV))]
    [t.start() for t in th]; [t.join() for t in th]
    return out
if __name__ == '__main__':
    for f in sys.argv[1:]:
        s = json.load(open(f)); print(f, len(s), check_many([s])[0])
