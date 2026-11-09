# W17: apply an exname hold-out list to a pattern args file by writing filtered copies of the cpat (cfast) files, so that every
# loader (st21_w17.py's spec loader and the Studio wlp3 / wlp3r6 separator builder exec'd from it) sees the same C patterns.
# usage: python3 -I exname_filter17.py EXNAME ARGS_IN ARGS_OUT OUTDIR HERE
#   EXNAME: one name per line ('#' comments).  For each cpat=F of ARGS_IN (F absolute or relative to HERE):
#     F missing        -> the entry is dropped from ARGS_OUT (Opus's run: "N files read, 2 missing"; the Studio loaders would crash);
#     F holds a block whose header name is held out -> OUTDIR/<F with / -> __>.exn.cfast is written without those blocks (a block =
#       its header line, i.e. a line with ' r=' that does not start with a space, plus every line up to the next header), and
#       ARGS_OUT points to it;
#     otherwise F is kept as it is.
#   pat= (D), rpat=, w7plus and every other entry are copied unchanged (exname holds out C entries only).
import sys, os, re, collections, hashlib
EXF, AIN, AOUT, OUTD, HERE = sys.argv[1:6]; OUTD = os.path.abspath(OUTD)   # the args must name the copies by absolute path (loaders resolve relative paths against HERE)
EXN = {l.split()[0] for l in open(EXF) if l.strip() and not l.startswith('#')}
os.makedirs(OUTD, exist_ok=True)
out = []; tot = collections.Counter()
def is_hdr(l): return ' r=' in l and not l.startswith(' ')
for a in open(AIN).read().split():
    if not a.startswith('cpat='): out.append(a); continue
    fn = a[5:]; p = fn if os.path.isabs(fn) else os.path.join(HERE, fn)
    if not os.path.exists(p): print('missing (dropped from the args): %s' % fn); tot['missing files'] += 1; continue
    lines = open(p).read().splitlines(True); keep = []; cur_drop = False; nb = nc = 0; cur = None; names = set()
    for l in lines:
        if is_hdr(l):
            cur = l.split()[0]; cur_drop = cur in EXN
            if cur_drop: nb += 1; names.add(cur)
        elif cur_drop and 'C-REDUCIBLE' in l: nc += 1
        if not cur_drop: keep.append(l)
    if nb == 0: out.append(a); continue
    base = fn.lstrip('/').replace('/', '__'); base = base[:-6] if base.endswith('.cfast') else base
    q = os.path.join(OUTD, base + '.exn.cfast')
    open(q, 'w').write(''.join(keep)); out.append('cpat=' + q)
    tot['blocks'] += nb; tot['C entries'] += nc; tot['names'] += len(names)
    print('%s: %d held-out blocks removed (%d C-REDUCIBLE entries, %d distinct names) -> %s md5 %s' % (fn, nb, nc, len(names), q, hashlib.md5(''.join(keep).encode()).hexdigest()[:8]))
open(AOUT, 'w').write(' '.join(out) + '\n')
print('exname %s (%d names): %s; args %s -> %s (%d entries, md5 %s)' % (EXF, len(EXN), dict(tot), AIN, AOUT, len(out), hashlib.md5(open(AOUT, 'rb').read()).hexdigest()[:8]))
