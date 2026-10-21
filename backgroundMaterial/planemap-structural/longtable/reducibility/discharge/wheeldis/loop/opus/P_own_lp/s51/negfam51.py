import sys, json, collections, re
E=sys.argv[1]; cert=sys.argv[2]; sys.argv=[E+'/pcheck.py','lowerR2']+sys.argv[3:]+['cert='+cert,'norepair']
src=open(E+'/pcheck.py').read(); last=src.rstrip().rsplit('\n',1)
G={'__file__':E+'/pcheck.py','__name__':'x'}; exec(compile(last[0],E+'/pcheck.py','exec'),G)
p2=open(E+'/prelay2.py').read(); f=re.search(r'\ndef cmd_lowerR2\(\):\n(.*?)\n(?=\S)', p2, re.S).group(0)
OLD="    if neg: log('  negative reduced costs:', len(neg), sorted(neg, key=lambda kv: kv[1])[:5])"
f=f.replace(OLD,"    CAP_['neg']=neg; CAP_['tot']=tot; CAP_['tco']=tco\n"+OLD); G['CAP_']={}; exec(f,G); G['cmd_lowerR2']()
neg=G['CAP_']['neg']; print('neg by family', collections.Counter(k[0] for k,_ in neg)); print('worst', min(float(v) for _,v in neg))
tot=G['CAP_']['tot']; tco=G['CAP_']['tco']
xq=[float(-v/tco) for k,v in tot.items() if k[0]=='XQ' and v]; print('XQ columns with rc != 0:', len(xq), 'sum |rc|', sum(abs(x) for x in xq))
