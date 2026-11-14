import json
S='atlas/'
css=open(S+'css.txt').read()
extra='''
.proofbar{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px}
.proofbar button{font:inherit;font-size:14px;padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}
.proofbar button.on{background:var(--accent);border-color:var(--accent);color:#fff}
.famhead{background:var(--chip, rgba(127,127,127,.12));font-weight:600;cursor:pointer}
.treegrid{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:18px;align-items:start;margin-top:10px}
@media(max-width:900px){.treegrid{grid-template-columns:1fr}}
#treeg svg{width:100%;height:auto;display:block;max-width:none}\n#nestg svg{max-width:none;width:auto}\n.legend svg{display:inline-block;width:26px;max-width:26px;vertical-align:middle}
#tdetail{display:flex;flex-direction:column;gap:12px;min-width:0}
#tdetail .pics svg{max-width:100%}
.chg{margin:4px 0 0;padding-left:18px;font-family:var(--mono);font-size:13px}
.pill.N2{color:var(--t6)}
#nestsel{margin-top:10px;display:flex;flex-direction:column;gap:6px}
.gsvg svg{max-width:none;width:auto}\n.gmini{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px;margin-top:6px}\n.gmini button{font:inherit;font-family:var(--mono);font-size:11px;background:var(--panel);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:6px;cursor:pointer;display:flex;flex-direction:column;gap:4px;text-align:left}\n.gmini button:hover{border-color:var(--accent)}\n.gmini svg{max-width:100%;width:100%;height:auto}\n.row.sub{padding-left:28px;color:inherit;max-width:none;margin:0}
'''
body=open(S+'body3.html').read()
data=open('db/atlas4.json').read().replace('</','<\\/')
body=body.replace('__DATA__',data)
html=('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
 '<title>Discharging Rule Atlas</title>'
 '<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap" rel="stylesheet">'
 '<style>'+css+extra+'</style></head><body>'+body+'</body></html>')
open(S+'rule-atlas.html','w').write(html)
import re
scripts=re.findall(r'<script>(.*?)</script>',body,re.S)
open(S+'check.js','w').write('\n'.join(scripts))
print(len(html))
