# W16: Studio-side lower check (st21_w10 LOWER_ONLY) of a certificate. usage: python3 -I st21_lower.py CERT EXPECT_T FAM ARGS [EXPECT_PAT]
import sys, os; sys.path.insert(0, '/tmp/swarm-W16/code')
import load21
cert, et, fam, args = sys.argv[1:5]; ep = sys.argv[5] if len(sys.argv) > 5 else None
extra = {'EXPECT_PAT': ep} if ep else {}
if fam == 'base': ns = load21.load(cert, et, fam=False, args=args, extra=extra)
elif fam == 'rrz': extra.update(Q7='0', Q7M='0'); ns = load21.load(cert, et, fam=True, args=args, extra=extra)
else: ns = load21.load(cert, et, fam=True, args=args, extra=extra)
