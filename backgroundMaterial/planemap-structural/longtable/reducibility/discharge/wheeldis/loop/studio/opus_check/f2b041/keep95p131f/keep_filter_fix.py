"""(keep95p131f: header rule fixed to any non-indented line whose 2nd field is r=.. or a digit; the old pattern missed q7-_ and hash names) s52c cover check (coordinator 21 Oct 12:55Z): copies of every cpat= file of an args file keeping ONLY the cfast blocks whose
header name is in KEEP (a block = a header line '<name> r=..' plus the indented lines after it; other lines kept as they are).
pat= (D) files are unchanged. Writes OUTDIR/<i>_<basename> and OUTDIR/args.txt. Usage: python3 keep_filter.py ARGS KEEPFILE OUTDIR [DROP]"""
import sys, os, re
args, keepf, out = sys.argv[1], sys.argv[2], sys.argv[3]; drop = set(sys.argv[4].split(',')) if len(sys.argv) > 4 else set()
keep = {l.split()[0] for l in open(keepf) if l.strip() and not l.startswith('#')} - drop
os.makedirs(out, exist_ok=True); toks = open(args).read().split(); new = []; found = set(); stats = []
for i, t in enumerate(toks):
    if not t.startswith('cpat='): new.append(t); continue
    p = t[5:]; o = os.path.join(out, '%03d_%s' % (i, os.path.basename(p))); kept = dropped = 0; cur_keep = True; buf = []
    for line in open(p, errors='ignore'):
        _t = line.split(); m = (not line[:1].isspace() and len(_t) >= 2 and (_t[1].startswith('r=') or _t[1].isdigit())) and _t[0]
        if m: cur_keep = m in keep; kept += cur_keep; dropped += not cur_keep; found |= {m} & keep
        elif not line.startswith(' '): cur_keep = True
        if cur_keep: buf.append(line)
    open(o, 'w').write(''.join(buf)); new.append('cpat=' + o); stats.append((os.path.basename(p), kept, dropped))
open(os.path.join(out, 'args.txt'), 'w').write(' '.join(new) + '\n')
print('keep %d names (dropped by request: %s); found in cpat files %d; missing %s' % (len(keep), sorted(drop), len(found), sorted(keep - found)))
print('blocks kept / dropped per file (nonzero kept): %s' % [s for s in stats if s[1]])
