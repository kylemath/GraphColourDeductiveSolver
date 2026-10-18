import os, sys
D='/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge'
g={'__file__': os.path.join(D,'wheeldis','wlp.py')}; sv=sys.argv; sys.argv=['x']
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'wlpdefs.py')).read(), g); sys.argv=sv
isR5, isR6 = g['isR5'], g['isR6']
