import json,time,sys
from fractions import Fraction as Fr
from bb_tools import *
rows=[];t0=time.time()
wd=[0,1,2]*2
qs=[Fr(a) for a in sys.argv[1].split(',')]
x=Fr(sys.argv[2])
for q in qs:
    signs=[]; first_neg=None
    for L in range(12,49,3):
        N=core_numerator(wd,L,q,x); s=int(N>0)-int(N<0); signs.append((L,s))
        print("q=%s x=%s L=%d sign=%+d (%.0fs)"%(q,x,L,s,time.time()-t0),flush=True)
        if s<0:
            first_neg=L; break
    rows.append({'word':wd,'q':str(q),'x':str(x),'signs':signs,'first_negative_L_on_grid':first_neg})
    json.dump(rows,open('/home/claude/bunkbed/v02/data/explore_qlt1_map_%s_x%s.json'%(sys.argv[1].replace(',','_').replace('/','o'),str(x).replace('/','o')),'w'),indent=1)
